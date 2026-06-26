---
name: invoice-automation
description: >
  AR/AP invoice automation for PrecisionLedger. Handles aging analysis, automated
  follow-up sequencing, payment matching, and collection priority scoring. Use when
  you need to: (1) generate AR/AP aging reports from invoice data, (2) draft or send
  overdue payment follow-ups, (3) match incoming payments to open invoices, (4) score
  and prioritize collections. NOT for: entering invoices into QBO or any client system
  (read-only), sending client communications without Irfan approval, or replacing
  judgment on dispute resolution.
metadata:
  author: PrecisionLedger
  version: "1.0.0"
  tags:
    - accounting
    - finance
    - AR
    - AP
    - collections
    - invoicing
---

# Invoice Automation Skill

Automates the invoice lifecycle: aging analysis → follow-up sequencing → payment matching → collection priority scoring.

---

## 1. AR/AP Aging Analysis

### What It Does
Buckets open invoices into aging bands (Current, 1–30, 31–60, 61–90, 90+) and computes exposure at each band.

### Input Format
Accepts CSV, JSON, or inline data with at minimum:
- `invoice_id`
- `client_name` (or `vendor_name` for AP)
- `invoice_date`
- `due_date`
- `amount`
- `amount_paid` (optional; defaults to 0)

### Aging Report Output
```
AR AGING SUMMARY — As of 2026-03-15
=====================================
Client           Current    1-30d    31-60d    61-90d    90+d     Total
────────────────────────────────────────────────────────────────────────
Acme Corp         $0       $4,200    $0        $8,500    $0       $12,700
Beta LLC        $15,000     $0       $2,100    $0        $5,000   $22,100
...

TOTALS          $15,000    $4,200   $2,100    $8,500    $5,000   $34,800
Weighted DSO: 47 days
```

### How to Trigger
> "Run aging on this invoice list: [paste CSV or describe source]"
> "What's our AR aging as of today?"
> "Show AP aging for last month"

---

## 2. Automated Follow-Up Sequencing

### Sequence Logic

| Days Past Due | Action                          | Tone         |
|---------------|---------------------------------|--------------|
| 1–7           | Friendly reminder               | Warm         |
| 8–21          | Polite escalation               | Professional |
| 22–45         | Firm demand with late fee notice | Direct       |
| 46–90         | Final notice + payment plan offer | Firm        |
| 90+           | Escalate to collections/legal   | Formal       |

### Draft Follow-Up Email Templates

**Stage 1 — Friendly Reminder (1–7 days past due)**
```
Subject: Invoice #[INV-ID] — Friendly Payment Reminder

Hi [Client Name],

Just a quick note — Invoice #[INV-ID] for $[AMOUNT], due [DUE DATE], appears to still be outstanding.

If payment has already been sent, please disregard. Otherwise, you can pay via [PAYMENT METHOD].

Let us know if you have any questions.

Best,
[Firm Name]
```

**Stage 2 — Polite Escalation (8–21 days)**
```
Subject: Invoice #[INV-ID] — Payment Follow-Up

Hi [Client Name],

We noticed Invoice #[INV-ID] for $[AMOUNT] is now [X] days past due.

Please arrange payment at your earliest convenience or reach out to discuss any issues.

[PAYMENT LINK]

Thank you,
[Firm Name]
```

**Stage 3 — Firm Demand (22–45 days)**
```
Subject: OVERDUE — Invoice #[INV-ID] Requires Immediate Attention

[Client Name],

Invoice #[INV-ID] for $[AMOUNT] is now [X] days overdue. Per our agreement, a late fee of [LATE FEE %] has been applied.

Updated balance: $[NEW AMOUNT]

Please remit payment within 5 business days to avoid further action.

[PAYMENT LINK]

PrecisionLedger Accounting
```

**Stage 4 — Final Notice + Payment Plan (46–90 days)**
```
Subject: Final Notice — Invoice #[INV-ID]

[Client Name],

This is a final notice regarding Invoice #[INV-ID], now [X] days past due. Outstanding balance: $[AMOUNT].

We are prepared to offer a structured payment plan. Contact us within 48 hours to arrange:
- [PAYMENT PLAN OPTION 1]
- [PAYMENT PLAN OPTION 2]

Failure to respond will result in referral to collections.

PrecisionLedger Accounting
```

### How to Trigger
> "Draft follow-up emails for all invoices 30+ days past due"
> "Generate a Stage 2 follow-up for Acme Corp Invoice #1042"
> "What's the next action for client Beta LLC?"

---

## 3. Payment Matching

### Logic
Matches incoming payments to open invoices using:
1. **Exact match** — payment amount = invoice amount (highest confidence)
2. **Partial match** — payment covers multiple invoices (sum match within tolerance)
3. **Fuzzy match** — memo/reference field matches invoice ID or client name
4. **Unmatched** — flag for manual review

### Input
- Bank feed export or payment notification data
- Open invoice list

### Output
```
PAYMENT MATCHING RESULTS — 2026-03-15
======================================
Payment ID  Amount    Matched To         Confidence  Status
──────────────────────────────────────────────────────────
PMT-2201    $4,200   INV-1042 (Acme)    HIGH        ✅ Matched
PMT-2202    $10,000  INV-1038 + INV-1039 MEDIUM     ⚠️  Review
PMT-2203    $750     —                  NONE        ❌ Unmatched
```

### How to Trigger
> "Match today's payments to open invoices: [paste bank data]"
> "We received $10k from Beta LLC — which invoices does that cover?"
> "Show me all unmatched payments this month"

---

## 4. Collection Priority Matrix

### Scoring Factors

| Factor                  | Weight | Description                              |
|-------------------------|--------|------------------------------------------|
| Days past due           | 40%    | Older = higher priority                  |
| Invoice amount          | 30%    | Larger balances prioritized              |
| Client payment history  | 20%    | Chronic late payers scored higher        |
| Dispute flag            | 10%    | Disputed invoices deprioritized          |

### Priority Tiers

| Score   | Tier       | Action                              |
|---------|------------|-------------------------------------|
| 80–100  | 🔴 Critical | Immediate escalation, daily follow-up |
| 60–79   | 🟠 High     | Weekly follow-up, payment plan offer  |
| 40–59   | 🟡 Medium   | Standard sequence, monitor            |
| 0–39    | 🟢 Low      | Automated reminder only               |

### Output
```
COLLECTION PRIORITY MATRIX — 2026-03-15
=========================================
Rank  Client        Invoice     Amount    DPD   Score  Tier
─────────────────────────────────────────────────────────────
1     Acme Corp     INV-1021   $8,500     68    87     🔴 Critical
2     Gamma LLC     INV-1035   $5,000     91    83     🔴 Critical
3     Beta LLC      INV-1039   $2,100     34    61     🟠 High
4     Delta Inc     INV-1042   $4,200     12    44     🟡 Medium
```

### How to Trigger
> "Generate collection priority matrix from current AR aging"
> "Who should we call first today?"
> "Score this invoice list for collection priority"

---

## 5. Workflow Examples

### Full AR Review
```
User: Run full AR review — aging, priorities, and draft follow-ups for top 3 past due.
Sam: [Runs aging] → [Scores matrix] → [Drafts 3 follow-up emails by stage] → presents for approval
```

### Single Client Deep Dive
```
User: Full invoice status for Acme Corp
Sam: [Pulls all open invoices] → [Aging position] → [Payment history] → [Next action recommendation]
```

### Payment Application
```
User: Got a $12,700 wire from Acme — apply it
Sam: [Matches to INV-1021 $8,500 + INV-1042 $4,200] → [Confirms match] → [Notes for QBO entry by human]
```

---

## 6. Negative Boundaries — When NOT to Use

- ❌ **Do not** enter or post transactions in QBO, Xero, or any client accounting system (read-only rule)
- ❌ **Do not** send follow-up emails without Irfan reviewing and approving drafts first
- ❌ **Do not** make collection calls (use output as briefing for human follow-up)
- ❌ **Do not** write off bad debt or adjust invoice balances without explicit instruction
- ❌ **Do not** resolve billing disputes — flag and escalate to Irfan
- ❌ **Do not** use for payroll, tax filings, or regulatory submissions (use compliance-monitor skill)

---

## 7. Data Formats

### Accepted CSV Schema
```csv
invoice_id,client_name,invoice_date,due_date,amount,amount_paid,status,notes
INV-1042,Acme Corp,2026-01-15,2026-02-15,4200.00,0.00,open,
INV-1038,Beta LLC,2026-02-01,2026-03-01,2100.00,0.00,open,disputed
```

### Output Delivery
- Console/chat: formatted tables
- File export: `memory/ar-aging-YYYY-MM-DD.md` or CSV on request
- Approval gate: all follow-up drafts held pending Irfan sign-off before any send

---

_Part of the PrecisionLedger OS — Precision. Integrity. Results._
