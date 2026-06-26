# Invoice & Payment Chaser

## Overview
Monitor overdue invoices across Xero and QuickBooks, send automated chase sequences
via email and WhatsApp, escalate major accounts, generate aged debtor reports, and
stop chasing the moment payment is received.

UK-focused: Late Payment of Commercial Debts Act 1998 awareness built in. Statutory
interest calculation included. All correspondence in UK English.

Not limited to product sellers — works for any UK business that invoices clients:
freelancers, agencies, consultants, tradespeople, and service businesses.

---

## Trigger Phrases

Chasing:
- "check overdue invoices" / "what invoices are overdue"
- "chase invoices" / "send payment reminders"
- "chase [client name]"
- "who owes me money"
- "run the payment chaser"

Reports:
- "aged debtor report" / "show aged debtors"
- "how much is outstanding" / "total overdue"
- "payment report" / "cash flow summary"
- "who hasn't paid"

Individual invoice:
- "chase invoice [number]"
- "mark invoice [number] as paid"
- "stop chasing [client name]"
- "add dispute note to [invoice]"

Configuration:
- "show my chase sequence"
- "update my payment terms"
- "set chase schedule"

---

## Configuration (ask on first use if not set)
Check memory for the following before running any workflow.
If missing, ask the user once and store under `invoice_config`.

```
ACCOUNTING_PLATFORM      # xero | quickbooks | both
XERO_CLIENT_ID           # From your Xero app — developer.xero.com/app/manage
XERO_CLIENT_SECRET       # From your Xero app — keep secret, never expose
XERO_ACCESS_TOKEN        # OAuth access token — fetched automatically, auto-refreshed
XERO_REFRESH_TOKEN       # OAuth refresh token — stored securely, never shown
XERO_TENANT_ID           # Xero organisation ID — fetched automatically after auth
QB_CLIENT_ID             # From your QuickBooks app — developer.intuit.com
QB_CLIENT_SECRET         # From your QuickBooks app — keep secret, never expose
QB_ACCESS_TOKEN          # QuickBooks OAuth access token — auto-refreshed
QB_REFRESH_TOKEN         # QuickBooks OAuth refresh token — stored securely
QB_REALM_ID              # QuickBooks company ID — fetched automatically after auth

EMAIL_PROVIDER           # imap | gmail_oauth
IMAP_HOST                # e.g. imap.gmail.com or mail.company.co.uk
IMAP_PORT                # Default: 993
IMAP_USERNAME            # Your email address
IMAP_PASSWORD            # App password
SMTP_HOST                # e.g. smtp.gmail.com or mail.company.co.uk
SMTP_PORT                # Default: 587

BUSINESS_NAME            # Used in email sign-offs
OWNER_NAME               # Signatory name on chase emails
FROM_EMAIL               # e.g. accounts@mycompany.co.uk
PAYMENT_TERMS_DAYS       # Default: 30 (days after invoice date payment is due)
CURRENCY                 # Default: GBP

CHASE_ENABLED            # Default: true — automatically send chase emails on schedule
APPROVAL_REQUIRED        # Default: true — owner approves each chase before sending
WHATSAPP_CHASE_THRESHOLD # Default: £500 — chase via WhatsApp for invoices above this
STOP_CHASE_ON_DISPUTE    # Default: true — pause chasing if dispute flag is set
LATE_PAYMENT_INTEREST    # Default: true — calculate and mention statutory interest
                         # on invoices overdue 30+ days (Late Payment of Commercial
                         # Debts Act 1998 — 8% over Bank of England base rate)
PAYMENT_LINK_ENABLED     # Default: false — include Stripe payment link in chase emails
STRIPE_PAYMENT_LINK      # Your Stripe payment link URL (if PAYMENT_LINK_ENABLED = true)
```

Never log or repeat access tokens or refresh tokens back to the user.

### Token refresh
Both Xero and QuickBooks OAuth tokens expire after 30 minutes (access token) and
60 days (refresh token). The skill automatically refreshes access tokens using the
stored refresh token before each API call. If the refresh token has expired (after
60 days of inactivity), prompt the user to re-authenticate via CONFIG.md.

---

## Invoice Status Definitions

Use these consistently across all workflows:

| Status | Definition |
|--------|-----------|
| `current` | Invoice due date has not yet passed |
| `overdue_1_7` | 1–7 days overdue — grace period, first chase |
| `overdue_8_30` | 8–30 days overdue — second chase |
| `overdue_31_60` | 31–60 days overdue — third chase, statutory interest applies |
| `overdue_60_plus` | 60+ days overdue — final notice, escalate |
| `disputed` | Owner has flagged as disputed — chasing paused |
| `paid` | Payment received — remove from chase queue |
| `written_off` | Owner has written off the debt |

Calculate `days_overdue` as: `today - invoice.DueDate`

Always use the `DueDate` field returned by the API — both Xero and QuickBooks
store this directly on each invoice and it reflects any custom payment terms
(e.g. 14 days, 60 days, end of month) set per invoice or client.
Only fall back to `invoice_date + PAYMENT_TERMS_DAYS` if `DueDate` is null or
not returned by the API (rare edge case).

Do NOT override or recalculate `DueDate` using `PAYMENT_TERMS_DAYS` — this
would give wrong results for invoices with non-standard terms.

---

## Chase Sequence

Default sequence — apply unless the owner has customised it:

| Stage | Trigger | Channel | Tone |
|-------|---------|---------|------|
| Stage 1 — Friendly reminder | 1 day overdue | Email | Polite, assumes oversight |
| Stage 2 — Follow-up | 8 days overdue | Email | Firmer, requests confirmation |
| Stage 3 — Formal notice | 31 days overdue | Email + WhatsApp* | Formal, mentions statutory interest |
| Stage 4 — Final demand | 61 days overdue | Email + WhatsApp* | Final, mentions debt collection |

*WhatsApp only if invoice value ≥ `WHATSAPP_CHASE_THRESHOLD`

Owner can customise: "change my chase sequence to 3, 10, 21, 45 days"

---

## Workflow A — Fetch and Triage Overdue Invoices

Triggered by: "check overdue invoices", "who owes me money", "run the payment chaser",
or via heartbeat if configured.

### Step 1 — Fetch invoices from Xero

Refresh access token if needed:
```
POST https://identity.xero.com/connect/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&client_id={XERO_CLIENT_ID}
&client_secret={XERO_CLIENT_SECRET}
&refresh_token={XERO_REFRESH_TOKEN}
```
Store the new `access_token` and `refresh_token` in memory.

Fetch all outstanding invoices:
```
GET https://api.xero.com/api.xro/2.0/Invoices?where=Status%3D%22AUTHORISED%22%20AND%20Type%3D%22ACCREC%22&order=DueDate%20ASC
Xero-Tenant-Id: {XERO_TENANT_ID}
Authorization: Bearer {XERO_ACCESS_TOKEN}
Accept: application/json
```

Filter to invoices where `AmountDue > 0`.
Calculate `days_overdue` for each.
Assign status from the Invoice Status Definitions table.

Key fields to extract per invoice:
- `InvoiceID`, `InvoiceNumber`, `Reference`
- `Contact.Name`, `Contact.EmailAddress`, `Contact.Phones`
- `Date`, `DueDate`, `AmountDue`, `AmountPaid`, `Total`
- `LineItems` (for context in chase emails)
- `CurrencyCode`

### Step 2 — Fetch invoices from QuickBooks (if configured)

Refresh QBO access token:
```
POST https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
Authorization: Basic {base64(QB_CLIENT_ID:QB_CLIENT_SECRET)}
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token={QB_REFRESH_TOKEN}
```

Fetch overdue invoices via QuickBooks Query API:
```
GET https://quickbooks.api.intuit.com/v3/company/{QB_REALM_ID}/query
  ?query=SELECT%20*%20FROM%20Invoice%20WHERE%20Balance%20%3E%200%20ORDER%20BY%20DueDate%20ASC
Authorization: Bearer {QB_ACCESS_TOKEN}
Accept: application/json
```

Map QuickBooks fields to consistent internal format:
- `Id` → `InvoiceID`
- `DocNumber` → `InvoiceNumber`
- `CustomerRef.name` → `Contact.Name`
- `BillEmail.Address` → `Contact.EmailAddress`
- `DueDate` → `DueDate`
- `Balance` → `AmountDue`
- `TotalAmt` → `Total`

### Step 3 — Check for recent payments (real-time sync)

Before displaying, verify each flagged invoice hasn't been paid since the last check.
For Xero, re-fetch each invoice individually if `days_overdue` seems inconsistent:
```
GET https://api.xero.com/api.xro/2.0/Invoices/{InvoiceID}
```
Remove any invoices where `AmountDue = 0` or `Status = "PAID"` from the chase list.
Update `payment_log` memory to record the payment with date and amount.

### Step 4 — Display aged debtor summary

```
💰 Overdue invoices — 18 Apr 2026

Total outstanding:   £8,340.00 across 6 invoices

🔴 Overdue 60+ days (1):
  · Apex Design Ltd     INV-0089   £2,400.00   74 days   ⚠️ Final demand stage

🟠 Overdue 31–60 days (2):
  · Blue Wave Agency    INV-0094   £1,850.00   38 days   📨 Stage 3 due
  · Thornton & Co       INV-0091   £750.00     33 days   📨 Stage 3 due

🟡 Overdue 8–30 days (2):
  · Metro Retail Group  INV-0097   £2,100.00   12 days   📨 Stage 2 due
  · Harlow Consulting   INV-0098   £640.00     9 days    📨 Stage 2 due

🟢 Overdue 1–7 days (1):
  · Patel & Partners    INV-0101   £600.00     2 days    📨 Stage 1 due

Reply:
  "send all due"     — send all chase emails that are due today
  "chase [name]"     — chase a specific client
  "aged report"      — full aged debtor breakdown
  "stop [name]"      — pause chasing a specific client
```

### Step 5 — Store in memory
Store current invoice list under `invoice_chase_queue`:
```json
{
  "last_checked": "{ISO datetime}",
  "invoices": [
    {
      "id": "{InvoiceID}",
      "number": "{InvoiceNumber}",
      "client": "{Contact.Name}",
      "email": "{Contact.EmailAddress}",
      "phone": "{Contact.Phone}",
      "amount_due": {AmountDue},
      "due_date": "{YYYY-MM-DD}",
      "days_overdue": {n},
      "status": "{status}",
      "last_chased": "{ISO date or null}",
      "chase_stage": {1|2|3|4},
      "disputed": false,
      "platform": "xero|quickbooks"
    }
  ]
}
```

---

## Workflow B — Send Chase Emails

Triggered by: "send all due", "chase invoices", "chase [client name]",
or automatically via heartbeat.

### Step 1 — Determine which invoices need chasing today

For each invoice in `invoice_chase_queue`:
- Is it `disputed = true`? → Skip (if STOP_CHASE_ON_DISPUTE = true)
- Is it `paid` or `written_off`? → Skip
- Determine the invoice's current stage from `days_overdue` using the stage thresholds
- Has `chase_stage` in memory already reached the current stage AND `last_chased`
  is within the last 7 days? → Skip (avoid re-chasing within same stage too quickly)
- Has `chase_stage` not yet reached the current stage? → Chase due (stage has escalated)
- Has `chase_stage` reached current stage AND `last_chased` is more than 7 days ago?
  → Re-chase at same stage (follow-up within stage is acceptable after 7 days)

Stage 4 (final demand) exception: never auto-send Stage 4 — always present to owner
for approval regardless of `APPROVAL_REQUIRED` setting or how many days have passed.

### Step 2 — Generate chase email for each invoice

Use the template matching the invoice's current stage.
Personalise with actual invoice data — amount, number, due date, days overdue.

**Stage 1 — Friendly reminder (1–7 days overdue):**
```
Subject: Payment reminder — {InvoiceNumber} — {BUSINESS_NAME}

Hi {first_name},

I hope you're well. I'm just dropping you a quick note as a friendly
reminder that invoice {InvoiceNumber} for £{AmountDue} was due on
{DueDate}.

If you've already processed this payment, please ignore this message —
it may simply be crossing in the post. If you have any questions about
the invoice, do let me know.

{IF PAYMENT_LINK_ENABLED}
For convenience, you can pay securely online here: {STRIPE_PAYMENT_LINK}
{ENDIF}

Many thanks,
{OWNER_NAME}
{BUSINESS_NAME}
{FROM_EMAIL}
```

**Stage 2 — Follow-up (8–30 days overdue):**
```
Subject: Outstanding payment — {InvoiceNumber} — {BUSINESS_NAME}

Hi {first_name},

I'm following up on my previous message regarding invoice {InvoiceNumber}
for £{AmountDue}, which was due on {DueDate} and is now {days_overdue}
days outstanding.

Could you let me know the expected payment date, or confirm if there
are any issues with the invoice I can help resolve?

{IF PAYMENT_LINK_ENABLED}
You can pay securely online here: {STRIPE_PAYMENT_LINK}
{ENDIF}

I look forward to hearing from you.

Best regards,
{OWNER_NAME}
{BUSINESS_NAME}
{FROM_EMAIL}
```

**Stage 3 — Formal notice (31–60 days overdue):**
```
Subject: Formal payment notice — {InvoiceNumber} — {BUSINESS_NAME}

Dear {first_name},

I am writing to formally notify you that invoice {InvoiceNumber} for
£{AmountDue} remains unpaid. This invoice was due on {DueDate} and is
now {days_overdue} days overdue.

{IF LATE_PAYMENT_INTEREST = true}
Under the Late Payment of Commercial Debts (Interest) Act 1998, we
reserve the right to charge statutory interest of 8% above the Bank of
England base rate on overdue commercial debts. We also reserve the right
to claim a fixed debt recovery charge of £{recovery_cost} (applicable to
debts of this size under the Late Payment of Commercial Debts Regulations
2013). Should this invoice remain unpaid, we may add these amounts to the
outstanding balance.
{ENDIF}

Please arrange payment within 7 days of this notice. If there is a
dispute regarding this invoice, please contact me immediately so we
can resolve the matter.

{IF PAYMENT_LINK_ENABLED}
Pay online: {STRIPE_PAYMENT_LINK}
{ENDIF}

Yours sincerely,
{OWNER_NAME}
{BUSINESS_NAME}
{FROM_EMAIL}
```

**Stage 4 — Final demand (61+ days overdue):**
```
Subject: FINAL DEMAND — Invoice {InvoiceNumber} — {BUSINESS_NAME}

Dear {first_name},

This is a final demand for payment of invoice {InvoiceNumber} for
£{AmountDue}, now {days_overdue} days overdue.

Despite previous correspondence, this invoice remains unpaid. If
payment is not received within 7 days of this notice, we will have
no alternative but to pursue this debt through formal channels,
which may include:

  · Referral to a debt collection agency
  · County Court Judgment (CCJ) proceedings
  · Statutory demand under the Insolvency Act 1986

{IF LATE_PAYMENT_INTEREST = true}
Please note that the following additional amounts are now claimable
under the Late Payment of Commercial Debts (Interest) Act 1998 and
the Late Payment of Commercial Debts Regulations 2013:

  Statutory interest ({calculated_rate}% per annum):  £{interest_amount}
  Fixed debt recovery charge:                          £{recovery_cost}
  Total amount now claimable:                          £{total_claimable}
{ENDIF}

We would strongly prefer to resolve this amicably. Please contact
me immediately on {FROM_EMAIL} if you wish to discuss payment.

{IF PAYMENT_LINK_ENABLED}
Pay now: {STRIPE_PAYMENT_LINK}
{ENDIF}

Yours sincerely,
{OWNER_NAME}
{BUSINESS_NAME}
{FROM_EMAIL}
```

**Statutory interest and recovery cost calculation:**
```
rate = 0.08 + bank_of_england_base_rate  (fetch current rate via web search if possible)
daily_rate = rate / 365
interest_amount = AmountDue × daily_rate × days_overdue

recovery_cost = 40   if AmountDue < 1000
recovery_cost = 70   if AmountDue >= 1000 and AmountDue < 10000
recovery_cost = 100  if AmountDue >= 10000

total_claimable = AmountDue + interest_amount + recovery_cost
calculated_rate = (rate × 100) formatted to 2 decimal places (e.g. "13.25")
```
If Bank of England base rate cannot be fetched, use 4.75% as the conservative
default (search the web for the current rate before sending Stage 3/4 emails —
it changes periodically).

### Step 3 — Preview before sending (if APPROVAL_REQUIRED = true)

```
📧 Chase ready — {n} emails

Stage 1 (friendly reminder):
  · Patel & Partners   INV-0101   £600.00   2 days
    To: raj.patel@patelpartners.co.uk

Stage 2 (follow-up):
  · Metro Retail Group INV-0097   £2,100.00  12 days
    To: accounts@metroretail.co.uk
  · Harlow Consulting  INV-0098   £640.00    9 days
    To: claire.harlow@harlowconsulting.co.uk

Stage 3 (formal notice):
  · Blue Wave Agency   INV-0094   £1,850.00  38 days   ⚠️ Interest: £24.56
    To: finance@bluewave.co.uk
  · Thornton & Co      INV-0091   £750.00    33 days   ⚠️ Interest: £8.65
    To: accounts@thorntonco.co.uk

Total being chased: £5,940.00

Send all? YES / review each one / skip
```

If APPROVAL_REQUIRED = false, send immediately and report results.

### Step 4 — Send emails

Use SMTP (same pattern as Customer Support Triage skill).

RFC 2822 format with proper headers:
```
From: {OWNER_NAME} <{FROM_EMAIL}>
To: {Contact.EmailAddress}
Subject: {stage_subject}
Content-Type: text/plain; charset=UTF-8

{email_body}
```

### Step 5 — WhatsApp chase (for high-value invoices)

If invoice amount ≥ `WHATSAPP_CHASE_THRESHOLD` AND stage ≥ 3:
Send a WhatsApp message via OpenClaw's configured channel:

```
💰 Payment chase — {client_name}

Invoice: {InvoiceNumber}
Amount:  £{AmountDue}
Overdue: {days_overdue} days

Stage {n} chase email just sent to {email}.

If no response within 48 hours, consider a direct call.
Client phone: {phone_if_available}
```

### Step 6 — Update memory and log

After sending each chase:
- Update `chase_stage` and `last_chased` in `invoice_chase_queue`
- Add entry to `chase_log`:
```json
{
  "invoice_id": "{id}",
  "invoice_number": "{number}",
  "client": "{name}",
  "amount": {AmountDue},
  "stage": {n},
  "sent_at": "{ISO datetime}",
  "channel": "email | email+whatsapp",
  "outcome": "sent | skipped | failed"
}
```

Confirm to owner:
```
✅ Chase emails sent — {n} invoices

  Patel & Partners     INV-0101   £600.00   Stage 1 ✅
  Metro Retail Group   INV-0097   £2,100.00  Stage 2 ✅
  Harlow Consulting    INV-0098   £640.00    Stage 2 ✅
  Blue Wave Agency     INV-0094   £1,850.00  Stage 3 ✅ + WhatsApp
  Thornton & Co        INV-0091   £750.00    Stage 3 ✅ + WhatsApp

Total chased: £5,940.00
Next run: tomorrow (Apex Design Ltd — Stage 4 final demand)
```

---

## Workflow C — Aged Debtor Report

Triggered by: "aged report", "aged debtor report", "how much is outstanding",
"cash flow summary".

Pull from `invoice_chase_queue` memory. If stale (>4 hours), re-fetch from API first.

```
📊 Aged Debtor Report — 18 Apr 2026

Total outstanding:    £8,340.00 (6 invoices)

Breakdown by age:
  Current (not yet due):   £0
  1–30 days overdue:       £3,340.00   40%   (3 invoices)
  31–60 days overdue:      £2,600.00   31%   (2 invoices)
  60+ days overdue:        £2,400.00   29%   (1 invoice)

By client:
  Apex Design Ltd          £2,400.00   74 days   🔴 Final demand
  Metro Retail Group       £2,100.00   12 days   🟡 Stage 2
  Blue Wave Agency         £1,850.00   38 days   🟠 Stage 3
  Thornton & Co              £750.00   33 days   🟠 Stage 3
  Harlow Consulting          £640.00    9 days   🟡 Stage 2
  Patel & Partners           £600.00    2 days   🟢 Stage 1

Chase history this month:
  Emails sent:     12
  Payments received after chase: 3 (£4,200.00)
  Avg days to pay after Stage 1: 8 days
  Avg days to pay after Stage 2: 14 days

⚠️ Apex Design Ltd has been at Stage 4 for 13 days with no response.
   Consider: debt collection referral or CCJ proceedings.
```

---

## Workflow D — Mark Invoice as Paid

Triggered by: "mark invoice [number] as paid", "invoice [number] has been paid",
or automatically when payment is detected during a sync.

### Option 1 — Detected automatically during Workflow A sync
When `AmountDue = 0` or `Status = "PAID"` is found during a fetch, mark as paid
in memory and notify owner:
```
✅ Payment received — INV-0097

Metro Retail Group paid £2,100.00
Removed from chase queue.
Outstanding balance: £6,240.00
```

### Option 2 — Manual mark (if payment received outside the system)
Update the invoice status in memory immediately.
Optionally update the invoice in Xero/QuickBooks:

Xero — mark as paid (use the dedicated Payments endpoint):
```
PUT https://api.xero.com/api.xro/2.0/Invoices/{InvoiceID}/Payments
Xero-Tenant-Id: {XERO_TENANT_ID}
Authorization: Bearer {XERO_ACCESS_TOKEN}
Content-Type: application/json

{
  "Account": { "Code": "{bank_account_code}" },
  "Date": "{today_YYYY-MM-DD}",
  "Amount": {AmountDue},
  "Reference": "Marked paid via OpenClaw"
}
```

Note: Xero requires a bank account code (e.g. `"090"` for the default bank account)
to record a payment against a specific account. If the owner hasn't configured one,
update the status in `invoice_chase_queue` memory only and flag for manual
reconciliation in Xero:
```
⚠️ Marked as paid in OpenClaw memory.
To reconcile in Xero, please record the payment manually:
Xero Admin → Invoices → {InvoiceNumber} → Add Payment
```

---

## Workflow E — Dispute Management

Triggered by: "add dispute note to [invoice]", "pause chasing [client]",
"[client] is disputing the invoice", "stop chasing [name]".

### Mark as disputed
Update `invoice_chase_queue` to set `disputed = true` for the invoice.
Add a note to memory:
```json
{
  "invoice_id": "{id}",
  "dispute_note": "{owner's description}",
  "flagged_at": "{ISO date}"
}
```

Confirm:
```
⏸️ Chasing paused — Apex Design Ltd (INV-0089)

Reason: {dispute note}
All automated chases suspended until you resume.

Reply "resume chasing Apex Design" to restart,
or "write off INV-0089" to remove from queue entirely.
```

If `STOP_CHASE_ON_DISPUTE = false`, still note the dispute but continue chasing.

### Resume chasing
Triggered by: "resume chasing [client]"
Sets `disputed = false`, resets chase to appropriate stage based on current `days_overdue`.

### Write off
Triggered by: "write off [invoice]"
Confirm before action — this removes the invoice from all future chasing.
Optionally update Xero/QuickBooks status to VOIDED or write-off account code.

---

## Workflow F — Payment Chase Report

Triggered by: "payment report", "how much have I collected this month",
"chase effectiveness report".

Pull from `chase_log` memory.

```
📊 Payment chase report — April 2026

Invoices chased:     18
Payments received:    7  (£12,400.00 collected)
Still outstanding:   11  (£8,340.00)
Collection rate:     60%

By stage effectiveness:
  Stage 1 responses:  4 of 6 paid within 5 days   (67%)
  Stage 2 responses:  2 of 5 paid within 7 days   (40%)
  Stage 3 responses:  1 of 4 paid within 14 days  (25%)
  Stage 4 responses:  0 of 3 paid                  (0%)

⚠️ Stage 4 (final demand) has 0% effectiveness this month.
   3 invoices totalling £5,100 may need debt collection referral.

Average days to payment after first chase: 11 days
Fastest paying client: Patel & Partners (3 days after Stage 1)
Slowest: Apex Design Ltd (still unpaid — 74 days)
```

---

## Workflow G — Heartbeat (Proactive Monitoring)

Configure OpenClaw's heartbeat to check for newly overdue invoices automatically.

Recommended schedule:
- Daily at 08:00 UK time — check for newly overdue invoices and any that have
  crossed into a new chase stage overnight

In HEARTBEAT.md add:
```
- Check invoice chase queue. Fetch latest from Xero/QuickBooks.
- If any invoices have become newly overdue or crossed a stage threshold, notify me.
- If APPROVAL_REQUIRED = true, show me the draft chases for approval before sending.
- If APPROVAL_REQUIRED = false, send due chases automatically and summarise.
- Always notify me if a Stage 4 (final demand) invoice has had no response in 7 days.
- Notify me immediately if any previously overdue invoice shows payment received.
```

**Payment received alert (highest priority heartbeat message):**
```
✅ Payment received! — {client_name}

Invoice: {InvoiceNumber}
Amount:  £{amount} (was {days_overdue} days overdue)

Outstanding balance reduced to: £{new_total}
```

---

## UK Late Payment Law Reference

Apply throughout. Never suggest ignoring these rights.

| Law | What it provides | When it applies |
|-----|-----------------|----------------|
| Late Payment of Commercial Debts (Interest) Act 1998 | 8% + BoE base rate interest on overdue B2B invoices | Business-to-business transactions only |
| Late Payment of Commercial Debts Regulations 2013 | Fixed debt recovery costs (£40 for debts <£1,000; £70 for £1,000–£9,999; £100 for £10,000+) | B2B only |
| Consumer Rights Act 2015 | Different rules for B2C | Business-to-consumer only |

**Fixed debt recovery costs** — can be claimed in addition to the invoice amount:
- Debt under £1,000 → claim additional £40
- Debt £1,000–£9,999 → claim additional £70
- Debt £10,000+ → claim additional £100

These can be mentioned in Stage 3/4 emails to increase urgency. The skill will
calculate and include them when `LATE_PAYMENT_INTEREST = true`.

**Important caveats:**
- These rights apply to B2B transactions only. If the debtor is a consumer
  (individual, not a business), different rules apply.
- This skill provides information only — it is not legal advice.
- For debts going to court or debt collectors, recommend the owner takes
  proper legal advice.

---

## Error Handling

| Error | Cause | Action |
|-------|-------|--------|
| Xero 401 | Access token expired | Auto-refresh using refresh token |
| Xero 403 | Wrong tenant ID or insufficient scope | Ask user to re-check Xero app permissions |
| Xero 429 | Rate limit (60 calls/minute) | Wait 60s, retry |
| QB 401 | Access token expired | Auto-refresh using refresh token |
| QB 429 | Rate limit | Wait 60s, retry |
| SMTP send failed | Wrong credentials or port | Verify app password, check SMTP settings |
| Invoice not found | ID mismatch or deleted | Re-fetch full list, update memory |
| Payment recorded but invoice still shows overdue | Sync delay | Re-fetch individual invoice after 5 minutes |

Required Xero API scopes (set in Xero app):
- `accounting.transactions` — read and update invoices
- `accounting.contacts` — read contact details
- `accounting.settings` — read bank account codes (for marking paid)

Required QuickBooks API scopes:
- `com.intuit.quickbooks.accounting` — full accounting access

---

## Memory Instructions

Store and maintain:
- `invoice_chase_queue`: current list of all overdue invoices with chase status
- `chase_log`: log of every chase sent — used for effectiveness reports
- `invoice_config`: all configuration values
- `dispute_notes`: map of invoice ID → dispute description and date
- `payment_log`: record of payments received during monitoring — used to show
  "collected this month" figures even if Xero/QuickBooks data is cleared

Update `invoice_chase_queue` on every Workflow A run.
Prune `chase_log` entries older than 12 months.
Never prune `payment_log` — payment history is valuable long-term.

---

## Tone & Communication (to owner)

- 💰 invoice summary · 📧 chase email · ✅ paid · ⏸️ paused · 🔴 final demand · 📊 report · ⚠️ alert
- Always show amount in £ — never raw numbers without currency
- For Stage 4 (final demand), always flag as needing owner attention — never auto-send
  without approval regardless of APPROVAL_REQUIRED setting
- When a payment comes in: celebrate it briefly — "✅ £2,100 received from Metro Retail!"
- When reporting aged debtors: be matter-of-fact, not alarming — state the facts and
  suggest next action
- Dates always in DD MMM YYYY format
- Never send a chase email on a Saturday, Sunday, or UK bank holiday — queue it for
  the next working day instead
