def calculate_total(items, discount, tax_rate):
    subtotal = sum(it["price"] * it["qty"] for it in items)
    # bug: 折扣和税率被忽略
    return subtotal
