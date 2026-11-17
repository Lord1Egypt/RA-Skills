# receipt_line_items Table (23 columns)

Used for storing parsed email receipt line items (e.g., Rainbow Grocery eReceipts).

**Correct INSERT pattern:**
```python
styx.execute('''
    INSERT INTO receipt_line_items (
        transaction_id, message_id, receipt_number,
        plu_upc, product_name, brand, category, subcategory,
        department, price, tax_code,
        quantity, unit_price, weight_lb, price_per_lb,
        is_bulk, is_organic, source_receipt_date,
        match_method, match_confidence, merchant_name, created_at
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
''', (tx_id, msg_id, receipt_num, plu, name, brand, cat, subcat,
      dept, price, tax, qty, unit_p, wlb, pplb,
      is_bulk, is_org, date, method, conf, 'Merchant Name'))
```

**Gotcha — "table has 23 columns but N values supplied"**: Omit `id` (auto-increment) but include all other 22 columns. Always list columns explicitly. Use `CURRENT_TIMESTAMP` for `created_at`. `merchant_name` is required.