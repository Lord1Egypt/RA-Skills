# ADP Invoice/Receipt Extraction — Field Schema Reference

This document defines the fixed field schema returned by ADP for invoice/receipt extraction. The `field_key` values are immutable identifiers used for field mapping configuration.

---

## Header Fields

| field_key | Default field_name | Type | Description |
|-----------|-------------------|------|-------------|
| `invoice_number` | Invoice Number | string | Unique invoice identifier |
| `invoice_date` | Invoice Date | string (YYYY-MM-DD) | Date the invoice was issued |
| `supplier_name` | Supplier Name | string | Name of the supplier/vendor |
| `supplier_vat_number` | Supplier VAT Number | string | Tax identification number of the supplier |
| `customer_name` | Customer Name | string | Name of the buyer/customer |
| `customer_vat_number` | Customer VAT Number | string | Tax identification number of the customer |
| `currency` | Currency | string (ISO 4217) | Currency code (e.g., USD, EUR, CNY) |
| `total_without_tax` | Total (Excl. Tax) | string | Total amount before tax |
| `vat_rate` | VAT Rate | string | Tax rate percentage |
| `total_amount` | Total Amount | string | Total amount including tax |
| `amount_due` | Amount Due | string | Amount payable |

---

## Line Item Fields (within `table_values`)

The `line_items` field in ADP output contains a `table_values` array. Each row is an array of field objects with the following keys:

| field_key | Default field_name | Type | Description |
|-----------|-------------------|------|-------------|
| `line_items_item_code` | Item Code | string | Product/service code or SKU |
| `line_items_description` | Description | string | Line item description |
| `line_items_quantity` | Quantity | string | Quantity of items |
| `line_items_unit_price` | Unit Price | string | Price per unit |
| `line_items_total_amount` | Line Total | string | Total amount for this line |

---

## ADP Output JSON Structure

Each extracted document returns an array of field objects:

```json
[
  {
    "field_key": "invoice_number",
    "field_name": "Invoice Number",
    "field_values": [
      {
        "field_value": "MK-2026-03077",
        "field_confidence": 1.0,
        "references": []
      }
    ]
  },
  ...
  {
    "field_key": "line_items",
    "field_name": "Line Items",
    "field_confidence": 1.0,
    "references": [],
    "table_values": [
      [
        { "field_key": "line_items_item_code", "field_name": "Item Code", "field_values": [...] },
        { "field_key": "line_items_description", "field_name": "Description", "field_values": [...] },
        { "field_key": "line_items_quantity", "field_name": "Quantity", "field_values": [...] },
        { "field_key": "line_items_unit_price", "field_name": "Unit Price", "field_values": [...] },
        { "field_key": "line_items_total_amount", "field_name": "Line Total", "field_values": [...] }
      ]
    ]
  }
]
```

---

## Field Mapping Rules

- **Key** (`field_key`): Fixed ADP identifier. Used by the Skill to match ADP output to mapping configuration. **Cannot be modified.**
- **Value** (user-defined display name): Determines Excel column headers or target field names in business systems. **Freely modifiable by user.**
- If no mapping is configured, the Skill uses ADP's raw `field_name` as the display name.
- All `field_value` entries are strings. Numeric conversion (if needed) is handled at the output stage.
- `field_confidence` ranges from 0.0 to 1.0; values below 0.8 should be flagged for user review.

---

## Example `field_map.json`

```json
{
  "invoice/receipt": {
    "invoice_number":             "Invoice Number",
    "invoice_date":               "Invoice Date",
    "supplier_name":              "Supplier Name",
    "supplier_vat_number":        "Supplier VAT Number",
    "customer_name":              "Customer Name",
    "customer_vat_number":        "Customer VAT Number",
    "currency":                   "Currency",
    "total_without_tax":          "Total (Excl. Tax)",
    "vat_rate":                   "VAT Rate",
    "total_amount":               "Total Amount",
    "amount_due":                 "Amount Due",
    "line_items_item_code":       "Item Code",
    "line_items_description":     "Description",
    "line_items_quantity":        "Quantity",
    "line_items_unit_price":      "Unit Price",
    "line_items_total_amount":    "Line Total"
  }
}
```

> For API push mode (Mode C), the values in this mapping become the field names in the POST request body sent to the business system.
