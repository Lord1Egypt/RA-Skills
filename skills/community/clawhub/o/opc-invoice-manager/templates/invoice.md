# Invoice {{invoice_number}}

---

|  |  |
|---|---|
| **From** | {{your_entity_name}} |
|  | {{your_entity_address}} |
|  | {{your_entity_email}} |
|  | Tax ID: {{your_tax_id}} |

|  |  |
|---|---|
| **Bill To** | {{client_name}} |
|  | {{client_billing_address}} |
|  | Attn: {{client_contact_name}} |
|  | {{client_email}} |

---

| Field | Value |
|-------|-------|
| **Invoice Number** | {{invoice_number}} |
| **Issue Date** | {{issue_date}} |
| **Due Date** | {{due_date}} |
| **Payment Terms** | {{payment_terms}} |
| **Reference / PO** | {{reference_number}} |
| **Currency** | {{currency}} |
| **Service Period** | {{service_period_label}} |

---

## Line Items

| # | Description | Type | Qty | Unit Price | Amount |
|---|-------------|------|----:|------------|-------:|
| {{n}} | {{description}} | {{type}} | {{quantity}} | {{unit_price}} | {{amount}} |

---

|  |  |
|---:|---:|
| **Subtotal** | {{subtotal}} {{currency}} |
| {{tax_name}} ({{tax_rate}}) | {{tax_amount}} {{currency}} |
| **Discount** ({{discount_description}}) | -{{discount_amount}} {{currency}} |
| **Total Due** | **{{total_amount}} {{currency}}** |

---

## Payment Instructions

{{payment_instructions}}

## Notes

{{notes}}

---

*{{invoice_number}} — Issued {{issue_date}} — Due {{due_date}}*
