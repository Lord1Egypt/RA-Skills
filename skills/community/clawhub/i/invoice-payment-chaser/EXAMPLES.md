# Invoice & Payment Chaser — Examples

These examples show expected input/output for each workflow.
The agent should match or exceed this quality and consistency.

---

## Example 1 — Morning invoice check

**User:** "check overdue invoices"

**Agent:**
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
  · Harlow Consulting   INV-0098   £640.00      9 days   📨 Stage 2 due

🟢 Overdue 1–7 days (1):
  · Patel & Partners    INV-0101   £600.00      2 days   📨 Stage 1 due

Reply:
  "send all due"   — send all chase emails due today
  "chase [name]"   — chase a specific client
  "aged report"    — full breakdown
  "stop [name]"    — pause chasing a client
```

---

## Example 2 — Send all due chases with approval

**User:** "send all due"

**Agent:**
```
📧 Chase ready — 5 emails

Stage 1 (friendly reminder):
  · Patel & Partners     INV-0101   £600.00    2 days
    To: raj.patel@patelpartners.co.uk

Stage 2 (follow-up):
  · Metro Retail Group   INV-0097   £2,100.00  12 days
    To: accounts@metroretail.co.uk
  · Harlow Consulting    INV-0098   £640.00     9 days
    To: claire.harlow@harlowconsulting.co.uk

Stage 3 (formal notice — statutory interest applies):
  · Blue Wave Agency     INV-0094   £1,850.00  38 days   ⚠️ Interest: £24.56
    To: finance@bluewave.co.uk
  · Thornton & Co        INV-0091   £750.00    33 days   ⚠️ Interest: £8.65
    To: accounts@thorntonco.co.uk

Total being chased: £5,940.00

Apex Design Ltd (£2,400.00 — Stage 4) shown separately — needs your review
before sending a final demand.

Send all 5? YES / review each first / skip
```

**User:** "yes"

**Agent:**
```
✅ Chase emails sent — 5 invoices

  Patel & Partners     INV-0101   £600.00    Stage 1 ✅
  Metro Retail Group   INV-0097   £2,100.00  Stage 2 ✅
  Harlow Consulting    INV-0098   £640.00    Stage 2 ✅
  Blue Wave Agency     INV-0094   £1,850.00  Stage 3 ✅ + WhatsApp
  Thornton & Co        INV-0091   £750.00    Stage 3 ✅ + WhatsApp

Total chased: £5,940.00
Next: Apex Design Ltd (Stage 4 final demand) — awaiting your approval
```

---

## Example 3 — Stage 1 chase email content

```
Subject: Payment reminder — INV-0101 — Meridian Consulting

Hi Raj,

I hope you're well. I'm just dropping you a quick note as a friendly
reminder that invoice INV-0101 for £600.00 was due on 16 Apr 2026.

If you've already processed this payment, please ignore this message —
it may simply be crossing in the post. If you have any questions about
the invoice, do let me know.

Many thanks,
Sarah
Meridian Consulting
accounts@meridianconsulting.co.uk
```

---

## Example 4 — Stage 3 formal notice with statutory interest and recovery cost

```
Subject: Formal payment notice — INV-0094 — Meridian Consulting

Dear Tom,

I am writing to formally notify you that invoice INV-0094 for £1,850.00
remains unpaid. This invoice was due on 11 Mar 2026 and is now 38 days
overdue.

Under the Late Payment of Commercial Debts (Interest) Act 1998, we
reserve the right to charge statutory interest of 8% above the Bank of
England base rate on overdue commercial debts. We also reserve the right
to claim a fixed debt recovery charge of £70.00 (applicable to debts of
this size under the Late Payment of Commercial Debts Regulations 2013).
Should this invoice remain unpaid, we may add these amounts to the
outstanding balance.

Please arrange payment within 7 days of this notice. If there is a
dispute regarding this invoice, please contact me immediately so we
can resolve the matter.

Yours sincerely,
Sarah
Meridian Consulting
accounts@meridianconsulting.co.uk
```

---

## Example 5 — Stage 4 final demand (requires owner approval)

**Agent (Apex Design Ltd — 74 days — Stage 4):**
```
🔴 Final demand — Apex Design Ltd

Invoice:   INV-0089
Amount:    £2,400.00
Overdue:   74 days (since 03 Feb 2026)
Interest:  £62.04 (statutory, accruing daily at 12.75% p.a.)
Recovery:  £70.00 (fixed debt recovery cost — debts £1,000–£9,999)

Total claimable: £2,532.04

Previous chases: Stage 1 (21 Feb), Stage 2 (28 Feb), Stage 3 (21 Mar)
Responses received: 0

Draft final demand ready. This requires your approval before sending.

SEND — send final demand email
CALL  — flag for direct phone call first
HOLD  — pause for 7 more days
WRITE OFF — remove from chase queue
```

**User:** "send"

**Agent:**
```
✅ Final demand sent — Apex Design Ltd

INV-0089 · £2,400.00 · 74 days overdue
To: accounts@apexdesign.co.uk

If no response or payment within 7 days (by 25 Apr), consider:
  · Debt collection agency referral
  · County Court Judgment (CCJ) application
  · Statutory demand (Insolvency Act 1986) for debts over £750

Reply "debt collection options" for more information.
```

---

## Example 6 — Payment received notification

**Agent (during heartbeat sync):**
```
✅ Payment received! — Metro Retail Group

Invoice: INV-0097
Amount:  £2,100.00 (was 12 days overdue)
Paid:    18 Apr 2026

Removed from chase queue.
Outstanding balance reduced to: £6,240.00

Remaining overdue: 5 invoices · £6,240.00
```

---

## Example 7 — Dispute management

**User:** "Apex Design are disputing INV-0089, they say we didn't deliver the final phase"

**Agent:**
```
⏸️ Chasing paused — Apex Design Ltd (INV-0089)

Dispute note: "Client claims final phase not delivered"
Flagged: 18 Apr 2026

All automated chases suspended until you resolve this or resume.

Next steps:
  "resume chasing Apex Design" — restart chase sequence
  "write off INV-0089"         — remove from queue
  "add note to INV-0089"       — add further detail to the dispute record
```

---

## Example 8 — Aged debtor report

**User:** "aged report"

**Agent:**
```
📊 Aged Debtor Report — 18 Apr 2026

Total outstanding:    £8,340.00 (6 invoices)

By age:
  1–30 days:    £3,340.00   40%   (3 invoices)
  31–60 days:   £2,600.00   31%   (2 invoices)
  60+ days:     £2,400.00   29%   (1 invoice)

By client:
  Apex Design Ltd        £2,400.00   74 days   🔴 Final demand
  Metro Retail Group     £2,100.00   12 days   🟡 Stage 2
  Blue Wave Agency       £1,850.00   38 days   🟠 Stage 3
  Thornton & Co            £750.00   33 days   🟠 Stage 3
  Harlow Consulting        £640.00    9 days   🟡 Stage 2
  Patel & Partners         £600.00    2 days   🟢 Stage 1

This month:
  Collected after chasing:   £4,200.00 (3 payments)
  Still outstanding:         £8,340.00

⚠️ Apex Design Ltd — 74 days, 3 chases sent, 0 responses.
   Stage 4 final demand has been sent. Consider debt collection.
```

---

## Example 9 — Chase effectiveness report

**User:** "payment report"

**Agent:**
```
📊 Chase effectiveness — April 2026

Invoices chased:      18
Payments received:     7   £12,400.00 collected
Still outstanding:    11   £8,340.00
Collection rate:      60%

By stage:
  Stage 1:   4 of 6 paid within 5 days    (67%) ✅
  Stage 2:   2 of 5 paid within 7 days    (40%) 🟡
  Stage 3:   1 of 4 paid within 14 days   (25%) 🟠
  Stage 4:   0 of 3 paid                   (0%) 🔴

⚠️ Stage 4 has 0% effectiveness this month.
   3 invoices (£5,100) may need debt collection referral.

Fastest payer:  Patel & Partners — paid 3 days after Stage 1
Slowest:        Apex Design Ltd — 74 days, still unpaid
Best month:     Feb 2026 — 78% collection rate (£18,200 recovered)
```

---

## Email Tone Benchmarks

| Stage | ✅ Good opening | ❌ Avoid |
|-------|----------------|---------|
| Stage 1 | "I'm just dropping you a quick note as a friendly reminder" | "You have failed to pay invoice..." |
| Stage 2 | "I'm following up on my previous message regarding..." | "As mentioned in my last email..." |
| Stage 3 | "I am writing to formally notify you that..." | "I am very disappointed that..." |
| Stage 4 | "This is a final demand for payment of..." | "Unless you pay immediately I will sue you" |

Stage 4 must always include specific next steps (CCJ, debt collection) — vague
threats are ineffective and may not be legally sound.
