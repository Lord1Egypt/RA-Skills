---
name: invoice-chaser
version: 1.0.0
description: "Generate escalating payment reminder emails that match days-past-due. Four stages: friendly, firm, urgent, final notice. Supports contractor, professional, and general business verticals."
triggers:
  - invoice
  - payment reminder
  - overdue
  - past due
  - collections
  - accounts receivable
  - chase payment
  - follow up on invoice
  - late payment
  - outstanding balance
tools:
  - read_file
  - write_file
metadata:
  openclaw:
    emoji: "💸"
    homepage: https://gaffneyits.com/openclaw
    os: ["darwin", "linux", "win32"]
    autostart: false
    tags:
      - billing
      - invoicing
      - collections
      - email
      - small-business
      - contractor
      - accounts-receivable
---

# Invoice Chaser

Generate professional, escalating payment reminder emails based on how overdue an invoice is. Built by a developer who ships billing automation to real businesses.

## When to Use This Skill

Use this skill when the user asks to:
- Write a payment reminder email
- Follow up on an unpaid or overdue invoice
- Chase a late payment
- Draft a collections email
- Create reminder sequences for outstanding balances
- Generate past-due notices

## Information to Gather

Before generating a reminder, collect these details from the user. Ask for anything missing — do NOT guess or leave placeholders:

### Required
| Field | Description |
|-------|-------------|
| `client_name` | Who owes the money |
| `invoice_number` | The invoice identifier |
| `balance_due` | Amount owed (include currency symbol) |
| `due_date` | Original payment due date |
| `business_name` | The user's company or name |

### Optional (use if provided)
| Field | Description |
|-------|-------------|
| `days_overdue` | Days past due (calculate from due_date if not given) |
| `business_phone` | Contact phone number |
| `business_email` | Contact email |
| `payment_link` | URL where client can pay |
| `payment_plan_link` | URL for payment plan setup |
| `project_name` | For contractor invoices — the job or project |
| `contract_number` | For contractor invoices — the contract ref |
| `matter_number` | For professional services — the case/matter ref |

### Vertical Detection
Determine the vertical from context:
- **contractor** — mentions: project, job site, draw, lien, subcontractor, construction, renovation, trade work
- **professional** — mentions: firm, engagement, matter, retainer, counsel, consulting, advisory
- **general** — everything else (default)

## Escalation Stages

Calculate days overdue from `due_date` relative to today. Select the appropriate stage:

| Stage | Trigger | Tone |
|-------|---------|------|
| **friendly** | 1–7 days overdue | Warm, assumes oversight. "Just a quick reminder..." |
| **firm** | 8–21 days overdue | Direct but polite. States the facts, requests prompt payment. |
| **urgent** | 22–45 days overdue | Serious. Mentions consequences. Offers payment plan as off-ramp. |
| **final** | 46+ days overdue | Formal. States 7-day deadline. Mentions "additional remedies" without specifics. |

If the user explicitly requests a specific stage, use that stage regardless of days overdue.

## Generation Rules

1. **Never fabricate information.** If you don't have the client name, ask — don't write "Dear Valued Customer."
2. **Never include legal threats in friendly or firm stages.** No mentions of attorneys, liens, lawsuits, or collections agencies until the final stage.
3. **Never use the word "debt" in friendly or firm stages.** Use "balance," "invoice," or "amount due."
4. **Always include payment_link if provided.** Make it easy to pay.
5. **Offer payment_plan_link in urgent and final stages** if the user has one.
6. **Keep emails under 150 words.** Short emails get read. Long emails get ignored.
7. **Match the vertical's tone:**
   - Contractor: Direct, blue-collar professional. First names. "We know things get busy."
   - Professional: Formal, uses "Dear" and "Regards." References "engagement" or "matter."
   - General: Friendly and straightforward. Balanced formality.

## Output Format

Always output in this exact structure:

```
**Stage:** [friendly/firm/urgent/final]
**Vertical:** [contractor/professional/general]
**Days Overdue:** [number]

---

**Subject:** [email subject line]

**Body:**

[email body text]
```

Then ask: "Want me to adjust the tone, try a different stage, or generate the next stage in the sequence?"

## Multi-Email Sequence

If the user asks for a "full sequence" or "all stages," generate all 4 stages in order with a horizontal rule (`---`) between each. Label each clearly.

## Templates by Vertical and Stage

### Contractor — Friendly
**Subject:** Payment Reminder — {{project_name}} (Invoice {{invoice_number}})

Hi {{client_name}},

Just a quick reminder that Invoice {{invoice_number}} for {{balance_due}} on {{project_name}} was due on {{due_date}}. We know things get busy — wanted to make sure this didn't slip through your AP cycle.

You can pay easily here: {{payment_link}}

If you have any questions, call us at {{business_phone}} or reply to this email.

Thanks,
{{business_name}}

### Contractor — Firm
**Subject:** Past Due — {{balance_due}} for {{project_name}}

{{client_name}},

This is a follow-up regarding Invoice {{invoice_number}} for {{balance_due}}, now {{days_overdue}} days past due. Per our contract terms, we kindly request prompt payment.

If you need to arrange a payment plan, we're happy to work something out — just reach out to us at {{business_phone}}.

Pay here: {{payment_link}}

{{business_name}}

### Contractor — Urgent
**Subject:** Urgent: Outstanding Balance on {{project_name}}

{{client_name}},

Invoice {{invoice_number}} for {{balance_due}} is now {{days_overdue}} days past due. We need to resolve this promptly. Continued delays may affect project scheduling per our contract terms.

If you're experiencing cash flow issues, we can set up a payment plan: {{payment_plan_link}}

Otherwise, please remit payment today: {{payment_link}}

Contact us immediately at {{business_phone}}.

{{business_name}}

### Contractor — Final
**Subject:** Final Notice — Invoice {{invoice_number}} for {{project_name}}

{{client_name}},

This is a final notice regarding the outstanding balance of {{balance_due}} on Invoice {{invoice_number}} for {{project_name}}, now {{days_overdue}} days past due.

Without payment or a payment arrangement within 7 business days, we will pursue all available remedies under our contract.

We would prefer to resolve this directly. Please pay at {{payment_link}} or call {{business_phone}} to discuss options.

{{business_name}}

### Professional — Friendly
**Subject:** Reminder — Invoice {{invoice_number}} from {{business_name}}

Dear {{client_name}},

We wanted to bring to your attention that Invoice {{invoice_number}} for {{balance_due}} was due on {{due_date}}.

You can view and pay the invoice here: {{payment_link}}

Please don't hesitate to contact us at {{business_phone}} if you have any questions.

Best regards,
{{business_name}}

### Professional — Firm
**Subject:** Past Due Notice — Invoice {{invoice_number}} ({{balance_due}})

Dear {{client_name}},

Invoice {{invoice_number}} for {{balance_due}} is now {{days_overdue}} days past the agreed terms. We kindly request your prompt attention to this matter.

If there are any concerns regarding the invoice, please contact us at {{business_phone}} so we can resolve them.

Pay here: {{payment_link}}

Regards,
{{business_name}}

### Professional — Urgent
**Subject:** Second Notice — Overdue Balance Requires Attention

Dear {{client_name}},

This is a second follow-up regarding Invoice {{invoice_number}} for {{balance_due}}, now {{days_overdue}} days past due.

We value our working relationship and want to resolve this matter promptly. If you need to arrange a payment plan, please let us know: {{payment_plan_link}}

Otherwise, please remit payment at your earliest convenience: {{payment_link}}

{{business_name}}

### Professional — Final
**Subject:** Final Notice — Invoice {{invoice_number}}

Dear {{client_name}},

This is our final communication regarding the overdue balance of {{balance_due}} on Invoice {{invoice_number}}, now {{days_overdue}} days past due.

Without payment or a payment arrangement within 7 business days, we will be forced to pursue additional remedies to recover this amount. We would greatly prefer to resolve this directly.

Please pay at {{payment_link}} or contact {{business_phone}} immediately.

{{business_name}}

### General — Friendly
**Subject:** Friendly Reminder — Invoice {{invoice_number}}

Hi {{client_name}},

Just a friendly reminder that Invoice {{invoice_number}} for {{balance_due}} was due on {{due_date}}.

You can pay easily here: {{payment_link}}

Questions? Reach us at {{business_phone}} or {{business_email}}.

Thanks!
{{business_name}}

### General — Firm
**Subject:** Payment Overdue — Invoice {{invoice_number}}

{{client_name}},

Invoice {{invoice_number}} for {{balance_due}} is now {{days_overdue}} days past due. We'd appreciate prompt payment.

If you need to set up a payment plan, we can work with you — just reach out at {{business_phone}}.

Pay here: {{payment_link}}

{{business_name}}

### General — Urgent
**Subject:** Urgent — Your Account Requires Attention

{{client_name}},

This is an important notice. Your balance of {{balance_due}} (Invoice {{invoice_number}}) is now {{days_overdue}} days overdue. Please resolve this as soon as possible to avoid further action.

We're happy to set up a payment plan if that helps: {{payment_plan_link}}

Pay now: {{payment_link}}
Call us: {{business_phone}}

{{business_name}}

### General — Final
**Subject:** Final Notice — Invoice {{invoice_number}}

{{client_name}},

This is a final notice. Your balance of {{balance_due}} on Invoice {{invoice_number}} is {{days_overdue}} days past due.

If we do not receive payment or hear from you within 7 business days, we will pursue additional steps to recover this amount. We'd prefer to resolve this now.

Pay at {{payment_link}} or call {{business_phone}} today.

{{business_name}}

## Stop Conditions

- Do NOT generate if the user hasn't provided at least: client_name, invoice_number, balance_due, and business_name
- Do NOT generate legal advice. These are reminder emails, not legal documents.
- Do NOT claim to be an attorney or collections agency
- If the user asks for something beyond email reminders (filing liens, going to court, reporting to credit bureaus), say: "That's outside what this skill covers. You should consult with a collections attorney for legal remedies."
