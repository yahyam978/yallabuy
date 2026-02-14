import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="حاسبة شحن YallaBuy", page_icon="📦")

# تنسيق العناوين باللغة العربية
st.markdown("""
    <style>
    .main { text-align: right; }
    div.stButton > button:first-child { background-color: #ff4b4b; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("📦 حاسبة صافي ربح الأوردر")
st.write("احسب الـ Net Amount بعد خصم الشحن وضريبة القيمة المضافة (48%)")

# قاعدة البيانات (Zones & Rates)
zones_data = {
    "Zone 1: القاهرة والجيزة": {"under_5": 50, "under_10": 60},
    "Zone 2: الإسكندرية والقناة (بورسعيد، إسماعيلية، سويس)": {"under_5": 55, "under_10": 65},
    "Zone 3: الدلتا والمدن الجديدة (العبور، 10 رمضان، أكتوبر...)": {"under_5": 60, "under_10": 70},
    "Zone 4: مصر الوسطى (الفيوم، بني سويف، المنيا، أسيوط، سوهاج)": {"under_5": 70, "under_10": 80},
    "Zone 5: مصر العليا والمناطق السياحية (قنا، الأقصر، أسوان، البحر الأحمر، سيناء)": {"under_5": 80, "under_10": 90},
    "Zone 6: المناطق النائية والحدودية": {"under_5": 100, "under_10": 110}
}

# --- مدخلات المستخدم ---
with st.container():
    order_price = st.number_input("تمن الأوردر اللي العميل دفعه (ج.م):", min_value=0.0, step=10.0)
    
    selected_zone = st.selectbox("اختر منطقة التوصيل:", list(zones_data.keys()))
    
    is_heavy = st.radio("وزن الشحنة:", 
                         ["أقل من أو يساوي 5 كيلو", "أكبر من 5 كيلو (حتى 10 كيلو)"],
                         horizontal=True)

# تحويل اختيار الوزن لمفتاح البحث في البيانات
weight_bracket = "under_5" if "أقل" in is_heavy else "under_10"

# --- الحسابات ---
if st.button("احسب الصافي"):
    if order_price > 0:
        base_shipping = zones_data[selected_zone][weight_bracket]
        tax_multiplier = 1.48 # الضريبة 48%
        shipping_with_tax = base_shipping * tax_multiplier
        net_amount = order_price - shipping_with_tax
        
        # عرض النتائج في كروت منظمة
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("تكلفة الشحن (+ الضريبة)", f"{shipping_with_tax:.2f} ج.م")
        with col2:
            st.metric("صافي المبلغ (Net)", f"{net_amount:.2f} ج.م", delta_color="normal")
            
        st.success(f"تم خصم {shipping_with_tax:.2f} ج.م (شاملة ضريبة 48%) من إجمالي {order_price} ج.م")
    else:
        st.warning("برجاء إدخال مبلغ الأوردر أولاً")
