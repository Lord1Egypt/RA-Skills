# Document conversion fields

Author: Daniel Hallman

Use this reference to check the fields and document numbers returned by a conversion or payment calculation. These tools prepare documents from supplied details; they do not move money.

## State Transition Diagram

```text
[Estimate / Quote]  (EST-2026-XXXX, status: draft/valid)
       |
       | convert_document(target_type: "invoice", due_days: 14/30)
       v
  [Tax Invoice]     (INV-2026-XXXX, status: pending)
       |
       +-----------------------+-----------------------+
       | record_payment        | record_payment        | convert_document
       | (amount < total)      | (amount >= total)     | (target_type: "credit_note")
       v                       v                       v
[Partially Paid Inv]    [Settled Invoice /]     [Credit Note / Refund]
(status: partial,        [Official Receipt]     (CRD-2026-XXXX,
 balance_due > 0)       (REC-2026-XXXX,          status: refunded/credited)
                         balance_due == 0,
                         status: paid)
```

## Field changes
1. **Estimate -> Invoice (`convert_document`):**
   - Document type changes to `invoice`.
   - Prefix changes from `EST-` to `INV-`.
   - `issue_date` updates to today.
   - `due_date` calculated as `issue_date + due_days`.
   - `payment_status` becomes `pending`.
   - If `payment_link` is provided, `payment_qr_code` is set to `true`.

2. **Invoice -> Partial Payment (`record_payment`):**
   - `amount_paid` stores cumulative paid sum.
   - `balance_due = grand_total - amount_paid`.
   - `payment_status` set to `partial`.
   - `is_paid` remains `false`.
   - Transaction reference and payment method recorded.

3. **Invoice -> Paid in Full (`record_payment`):**
   - `amount_paid` equals `grand_total`.
   - `balance_due` becomes `0.00`.
   - `payment_status` set to `paid`.
   - `is_paid` becomes `true`.
   - Visual watermark stamped: `PAID IN FULL`.

4. **Invoice -> Official Receipt (`convert_document(target_type: "receipt")`):**
   - Prefix changes from `INV-` to `REC-`.
   - Title updates to `OFFICIAL PAYMENT RECEIPT`.
   - Shows zero balance due and payment settlement receipt footer.

5. **Invoice -> Credit Note (`convert_document(target_type: "credit_note")`):**
   - Prefix changes to `CRD-`.
   - Title updates to `CREDIT NOTE`.
   - Retains counterparty data, references original invoice number, and displays credit reason.
