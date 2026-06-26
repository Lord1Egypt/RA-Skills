# Simple Invoice Example

**User:**
"Bill Acme Corp $500 for the logo design I did last week. Due on receipt."

**InvoiceGen (Internal State):**
- Checks `clients.json` for Acme Corp (Not found).
- Checks `business-profile.json` (Found: Cody, 123 Main St, cody@nolliolabs.com, Stripe Link).
- Checks `invoice-log.json` for last invoice (Found: INV-001, so this is INV-002).

**InvoiceGen (Response):**
"I'll get that set up! It looks like Acme Corp isn't in your client list yet.

What's their email address and physical address so I can add them? (You can skip the physical address if you don't need it on the invoice.)"

**User:**
"sarah@acme.com, just put New York, NY"

**InvoiceGen (Response):**
"Got it, saved Acme Corp to your clients. Here is the draft for **INV-002**:

**Billed To:** Acme Corp (sarah@acme.com)
**Date:** Oct 24, 2026
**Due:** On Receipt

| Description | Qty | Rate | Amount |
| :--- | :---: | ---: | ---: |
| Logo Design | 1 | $500.00 | $500.00 |

**Subtotal:** $500.00
**Total Due:** $500.00

Does this look good to generate the PDF?"

**User:**
"Looks perfect."

**InvoiceGen (Response):**
*(Generates PDF via `scripts/generate-invoice-pdf.py`)*

"Done! Your invoice is ready.

📄 **PDF Saved:** `invoices/INV-002-AcmeCorp.pdf`

Here is a draft email you can use to send it:

---
**Subject:** Invoice INV-002 for Logo Design

Hi Sarah,

I hope you're doing well! 

Attached is the invoice (INV-002) for the logo design project, totaling $500.00. Payment is due on receipt.

You can pay securely via the link on the invoice or let me know if you prefer another method.

Thanks again for the business!

Best,
Cody
---

Let me know when they pay so I can mark it as Paid in your dashboard!"