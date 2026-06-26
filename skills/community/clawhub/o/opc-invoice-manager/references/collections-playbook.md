# Collections Playbook

> Structured cadence engine for following up on unpaid invoices.
> Load with `read_file("references/collections-playbook.md")` in collections mode.

---

## Collection Cadence

The skill executes this cadence based on invoice age relative to due date. Each stage has a defined timing, tone, and output.

### Stage Overview

| Stage | Timing | Tone | Action |
|-------|--------|------|--------|
| **Pre-due reminder** | 3 days before due date | Friendly | Courtesy reminder |
| **Due-date nudge** | Due date | Gentle | "Just a reminder" |
| **Early overdue** | 1–7 days overdue | Polite but clear | Overdue notice |
| **Mid overdue** | 8–21 days overdue | Firmer | Overdue notice + invoice attached |
| **Late overdue** | 22–45 days overdue | Formal escalation | Formal notice, mention late fee rights |
| **Final notice** | 45+ days overdue | Final | Last notice before external action |

---

## Email Templates by Stage

### Stage 1: Pre-Due Reminder (3 days before due)

**Subject**: Upcoming payment — {{invoice_number}} due {{due_date}}

```
Hi {{client_contact_name}},

Quick heads-up that invoice {{invoice_number}} for {{total_amount}} {{currency}}
is due on {{due_date}}.

Payment details are on the invoice, but let me know if you need anything
to process this.

Thanks,
{{your_name}}
```

**Tone notes**: Casual, helpful. No urgency. Framed as a courtesy.

---

### Stage 2: Due-Date Nudge (on due date)

**Subject**: Invoice {{invoice_number}} — due today ({{total_amount}} {{currency}})

```
Hi {{client_contact_name}},

Just a friendly reminder that invoice {{invoice_number}} for
{{total_amount}} {{currency}} is due today.

If payment is already on its way, please disregard this note.
Otherwise, here are the payment details:

{{payment_instructions}}

Let me know if you have any questions.

Best,
{{your_name}}
```

**Tone notes**: Still friendly. Assumes good intent ("if already on its way").

---

### Stage 3: Early Overdue (1–7 days)

**Subject**: Payment reminder — {{invoice_number}} ({{days_overdue}} days past due)

```
Hi {{client_contact_name}},

I wanted to follow up on invoice {{invoice_number}} for
{{outstanding_amount}} {{currency}}, which was due on {{due_date}}.

Could you let me know the status of this payment? If there's anything
holding it up on your end, I'm happy to help resolve it.

Payment details:
{{payment_instructions}}

Thanks,
{{your_name}}
```

**Tone notes**: Direct but understanding. Asks for status. Opens the door for the client to raise issues.

---

### Stage 4: Mid Overdue (8–21 days)

**Subject**: Overdue: Invoice {{invoice_number}} — {{outstanding_amount}} {{currency}} ({{days_overdue}} days past due)

```
Hi {{client_contact_name}},

I'm following up again on invoice {{invoice_number}} for
{{outstanding_amount}} {{currency}}, now {{days_overdue}} days past the
due date of {{due_date}}.

I've attached the invoice again for your reference.

Could you please confirm when I can expect payment? If there's an issue
with the invoice or the work it covers, I'd like to address it promptly.

{{payment_instructions}}

Thank you,
{{your_name}}
```

**Tone notes**: Firmer. "Following up again" signals persistence. Attaching the invoice removes "I can't find it" as an excuse. Directly asks for a payment date.

---

### Stage 5: Late Overdue (22–45 days)

**Subject**: Formal notice — Invoice {{invoice_number}} overdue ({{days_overdue}} days)

```
Hi {{client_contact_name}},

This is a formal notice regarding invoice {{invoice_number}} for
{{outstanding_amount}} {{currency}}, which has been outstanding for
{{days_overdue}} days past the due date of {{due_date}}.

{{#if late_fee_clause}}
Per our agreement, overdue invoices are subject to late fees of
{{late_fee_rate}}. I would prefer to resolve this without applying
additional charges.
{{/if}}

I need to receive payment or a confirmed payment date by {{deadline}}.
Please reply to this email with an update.

If there is a dispute regarding this invoice, please let me know
immediately so we can resolve it.

{{payment_instructions}}

Regards,
{{your_name}}
```

**Tone notes**: Formal. Mentions late fee rights (if contractual) as leverage without immediately applying them. Sets a deadline. The word "need" replaces "would appreciate."

---

### Stage 6: Final Notice (45+ days)

**Subject**: FINAL NOTICE — Invoice {{invoice_number}} — {{outstanding_amount}} {{currency}}

```
Dear {{client_contact_name}},

This is a final notice regarding invoice {{invoice_number}} for
{{outstanding_amount}} {{currency}}, which is now {{days_overdue}} days
overdue.

Despite previous reminders on {{reminder_dates}}, I have not received
payment or a response.

If I do not receive payment or a written response by {{final_deadline}},
I will need to consider further options, which may include engaging a
collections service or seeking legal advice.

I would much prefer to resolve this directly. Please contact me as soon
as possible.

{{payment_instructions}}

Regards,
{{your_name}}
```

**Tone notes**: Final and serious. References previous attempts. States consequences without being threatening. Still leaves room for resolution.

**After Stage 6**: Escalate to accountant or legal counsel. The skill should recommend:
```
🧾 **ACCOUNTANT RECOMMENDED**: Invoice {{invoice_number}} is {{days_overdue}} days
overdue with no response after multiple collection attempts. Consider engaging a
collections service, writing off the debt, or seeking legal advice.
```

---

## Tone Adjustment

Client profiles include `reminder_tone_preference`. Adjust templates:

### Formal Tone
- Use "Dear" instead of "Hi"
- Full sentences, no contractions
- "I respectfully request" instead of "Could you"
- Sign off with "Yours sincerely" or "Regards"

### Friendly Tone
- Use "Hi" or "Hey"
- Conversational language
- "Just checking in" / "Quick nudge"
- Sign off with "Thanks!" or "Cheers"

### Minimal Tone
- Shortest possible communication
- Subject line does most of the work
- Body: 1-2 sentences max
- Example: "Hi — following up on INV-2026-003 ($5,000, due March 1). Any update on payment? Thanks, [Name]"

---

## Dispute Handling

When a client disputes an invoice, the skill should:

### 1. Acknowledge Immediately

**Subject**: Re: Invoice {{invoice_number}} — Acknowledging your concern

```
Hi {{client_contact_name}},

Thank you for letting me know about your concern with invoice
{{invoice_number}}. I want to make sure we resolve this promptly.

I understand the issue is: {{dispute_summary}}

I'll review this and get back to you by {{response_date}} with a
resolution or next steps.

In the meantime, I've paused collection follow-ups on this invoice.

Best,
{{your_name}}
```

### 2. Update Metadata

- Set `status` to `disputed`
- Record `dispute_reason` and `disputed_at`
- Pause the collection cadence for this invoice
- Set `collection_stage` to `dispute`

### 3. Resolution Paths

| Scenario | Action |
|----------|--------|
| Client is right — billing error | Issue credit note, create corrected invoice |
| Partial dispute — some items contested | Offer to split: pay undisputed portion now, resolve remainder |
| Client is wrong — work was delivered | Provide evidence (deliverables, approvals, contract terms) |
| Scope disagreement | Reference contract/SOW, propose discussion |
| Quality dispute | Offer to remedy the work, then re-invoice |

### 4. After Resolution

- If corrected: void original, issue new invoice, restart collection cadence
- If dismissed: resume collection cadence, document the resolution
- If partial: adjust amounts, document what was agreed

---

## Late Fee Calculation

**This is general guidance, not legal or tax advice. Maximum allowable rates vary by jurisdiction.**

### Simple Interest

```
Late fee = outstanding_amount × (annual_rate / 365) × days_overdue
```

Example: $10,000 at 18% annual, 30 days overdue:
```
$10,000 × (0.18 / 365) × 30 = $147.95
```

### Monthly Percentage

```
Late fee = outstanding_amount × monthly_rate × months_overdue
```

Example: $10,000 at 1.5%/month, 2 months:
```
$10,000 × 0.015 × 2 = $300.00
```

### Practical Application

- Only charge late fees if your contract explicitly allows it
- Notify the client before applying (use Stage 5 template)
- Add as a separate line item on a new invoice or statement
- Consider waiving for first offense with a good client
- **Escalate to accountant** if late fees have tax implications

---

## When to Escalate

### To Accountant
- Invoice is 60+ days overdue with no response
- Need to write off bad debt (tax implications)
- Dispute involves tax or regulatory questions
- Late fees accumulated need accounting treatment

### To Legal Counsel
- Client denies owing the amount despite clear contract
- Client is unresponsive after 90+ days and significant amount
- Contract has arbitration or jurisdiction clauses that matter
- Cease and desist or demand letter needed

### To Collections Agency
- All direct attempts exhausted (usually 90+ days)
- Amount justifies the agency's fee (typically 25-50% of collected amount)
- For small amounts: may not be worth it — consider writing off

---

## When to Write Off

Consider writing off when:
- Amount is small relative to collection effort
- Client has disappeared or gone bankrupt
- Legal action would cost more than the debt
- Relationship is not worth preserving and amount is immaterial

**Always consult an accountant** — write-offs have tax implications.

---

## Relationship Preservation

Collections is uncomfortable for solo entrepreneurs because clients are often also professional relationships. Principles:

1. **Separate the relationship from the transaction** — "I value working with you, and I also need to be paid for the work."
2. **Assume good intent first** — many late payments are process failures, not malice
3. **Be persistent but professional** — following up is not rude, it's business
4. **Offer solutions** — payment plans, partial payments, scope adjustments
5. **Know your line** — decide in advance what overdue threshold means you stop work
6. **Document everything** — keep a record of all communications
7. **Don't let one bad client change your approach** — most clients pay; don't punish good clients with aggressive terms because of one bad experience

---

## Collection Metrics to Track

| Metric | What It Tells You |
|--------|-------------------|
| DSO (Days Sales Outstanding) | Average time to collect |
| Collection rate | % of invoiced amounts collected |
| Overdue ratio | % of outstanding AR that's overdue |
| Dispute rate | % of invoices disputed |
| Bad debt rate | % of invoices written off |
| Average reminders to payment | How many nudges it typically takes |

---

*Reference for opc-invoice-manager. Not legal or financial advice.*
