# Detailed Invoice Example

**User:**
"Bill TechCorp for the website build. They owe 40 hours at $150/hr, plus $250 for hosting, and apply a 10% discount to the total because they are a long-term client. Oh, and add a 5% tax to the subtotal. Net 30 terms."

**InvoiceGen (Internal State):**
- Checks `clients.json` for TechCorp (Found: TechCorp, john@techcorp.com, 456 Tech Blvd, San Francisco, CA).
- Checks `business-profile.json` (Found: Cody, 123 Main St, cody@nolliolabs.com, Stripe Link).
- Checks `invoice-log.json` for last invoice (Found: INV-015, so this is INV-016).

**InvoiceGen (Response):**
"I'll get that set up. Here is the draft for **INV-016**:

**Billed To:** TechCorp (john@techcorp.com)
**Date:** Oct 24, 2026
**Due:** Nov 23, 2026 (Net 30)

| Description | Qty | Rate | Amount |
| :--- | :---: | ---: | ---: |
| Website Build (40 hours) | 40 | $150.00 | $6,000.00 |
| Hosting | 1 | $250.00 | $250.00 |
| Long-term Client Discount | 1 | -$625.00 | -$625.00 |

**Subtotal:** $5,625.00
**Tax (5%):** $281.25
**Total Due:** $5,906.25

*Note: I applied the 10% discount to the $6,250 sum of services before tax.*

Does this look right?"

**User:**
"Yes, print it."

**InvoiceGen (Response):**
*(Generates PDF via `scripts/generate-invoice-pdf.py`)*

"All set. 

📄 **PDF Saved:** `invoices/INV-016-TechCorp.pdf`

Here is a draft email you can use to send it:

---
**Subject:** Invoice INV-016 for Website Build & Hosting

Hi John,

I hope everything is going well! 

Attached is the invoice (INV-016) for the recent website build and hosting, totaling $5,906.25. As discussed, I've applied a 10% discount to your services as a thank you for being a long-term client! 

Payment is due on Net 30 terms (November 23).

You can pay securely via the link on the invoice or let me know if you prefer another method.

Thanks again for the continued business!

Best,
Cody
---"