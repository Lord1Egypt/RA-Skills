---
name: investor-memo-generator
description: >
  Generate investor-ready memos, executive summaries, and pitch narrative documents from raw financial data,
  cap tables, and startup metrics. Produces one-pagers, term sheet summaries, SAFE/note summaries, board
  update memos, and LP update letters. Structures narrative around traction, financials, and use of funds.
  Use when a founder or CFO needs to turn a financial model or data dump into a polished investor document.
  NOT for: building the underlying financial model (use startup-financial-model), cap table math (use
  cap-table-manager), legal document drafting (requires attorney), or generating pitch decks with slides
  (output is text/markdown, not slide formats).
version: 1.0.0
author: PrecisionLedger
tags:
  - finance
  - investors
  - startups
  - memos
  - fundraising
  - narrative
---

# Investor Memo Generator Skill

Transform raw financial data, metrics, and context into polished investor-ready documents. This skill guides Sam Ledger through structured memo creation — from one-pagers to board updates — with narrative framing that communicates traction, financials, and opportunity clearly.

---

## When to Use This Skill

**Trigger phrases:**
- "Write an investor memo for…"
- "Draft a board update / LP letter"
- "Summarize our financials for investors"
- "Turn this model into an investor narrative"
- "Prepare a one-pager for [company]"
- "Write a use-of-funds summary"
- "Draft a SAFE / term sheet summary"

**Use when:**
- Founder has financial model data and needs investor narrative
- Board meeting is coming and CEO needs a written update
- LP update letter is due (fund managers)
- Post-close SAFE/note summary needed for investor records
- Executive summary needed for data room

**Do NOT use when:**
- The underlying financial model doesn't exist yet → use `startup-financial-model` first
- Cap table needs to be built → use `cap-table-manager` first
- Legal binding term sheet needed → requires attorney review
- Slide deck / PowerPoint format needed → output is markdown/text only
- Public company investor relations → different regulatory requirements (10-K, 8-K, etc.)

---

## Document Types Supported

### 1. Investor One-Pager
Single-page executive summary: company overview, problem/solution, traction, team, ask, use of funds.

### 2. Board Update Memo
Structured monthly/quarterly update: KPIs vs plan, financial snapshot, key wins, risks, decisions needed.

### 3. LP Update Letter
For fund managers: portfolio performance, notable developments, capital calls/distributions, outlook.

### 4. SAFE / Convertible Note Summary
Plain-English summary of deal terms: valuation cap, discount, MFN, pro-rata rights, maturity.

### 5. Use-of-Funds Narrative
Breakdown of how raised capital will be deployed: headcount, product, sales/marketing, infrastructure, runway math.

### 6. Data Room Executive Summary
Multi-page document for serious investors: company background, market, product, financials, team, risks.

---

## Inputs Required

### Minimum (One-Pager or Board Update)
```
Company name & stage (pre-seed, seed, Series A…)
Monthly revenue (current + 3-month trend)
Burn rate / runway in months
Headcount
Key metric (MAU, ARR, units sold, etc.)
Fundraising ask (if applicable)
```

### Full (Data Room / Executive Summary)
```
All minimum inputs above, PLUS:
- Market size (TAM/SAM/SOM)
- Unit economics (CAC, LTV, payback period)
- Historical P&L (last 12 months)
- Forward projections (18-24 months)
- Cap table summary (post-round if applicable)
- Founder bios (2-3 sentences each)
- Competitive landscape
- Use of funds breakdown
```

---

## Output Formats

**Markdown** (default) — ready to paste into Notion, Google Docs, or any CMS
**Plain text** — for email body or simple documents
**Structured JSON** — for downstream automation or CRM entry

---

## Memo Templates

### One-Pager Template

```markdown
# [Company Name] — Investor Summary
*[Month Year] | [Stage] | Raising $[Amount]*

---

## The Opportunity
[2-3 sentences: problem + why now + market size signal]

## What We Do
[1-2 sentences: product/service in plain English]

## Traction
- **Revenue:** $[X]/mo (↑[%] MoM)
- **Customers:** [N] ([segment])
- **Key Metric:** [metric] = [value]
- **Runway:** [N] months at current burn

## Business Model
[1 sentence: how you make money]

## The Ask
**Raising:** $[Amount] | **Instrument:** [SAFE / Priced Round]
**Valuation Cap / Pre-money:** $[X]M
**Use of Funds:** [3-4 bullet breakdown]

## Team
- **[Name]**, CEO — [2-line bio]
- **[Name]**, CTO — [2-line bio]

## Contact
[Name] | [Email] | [Website]
```

---

### Board Update Memo Template

```markdown
# [Company Name] — Board Update [Month Year]

**Prepared by:** [CEO Name]
**Date:** [Date]
**Attendees:** [List]

---

## Executive Summary
[3-4 sentences: overall state of the business, tone-setting]

## KPIs vs Plan

| Metric | Plan | Actual | Δ |
|--------|------|--------|---|
| MRR | $X | $X | +/-% |
| Burn | $X | $X | +/-% |
| Headcount | N | N | +/- |
| [Key Metric] | X | X | +/-% |

## Financial Snapshot
- **Cash on Hand:** $[X] (as of [date])
- **Runway:** [N] months
- **Net Burn:** $[X]/mo
- **Revenue:** $[X] MRR / $[X] ARR

## Key Wins This Period
1. [Win 1]
2. [Win 2]
3. [Win 3]

## Risks & Concerns
1. [Risk 1] — Mitigation: [action]
2. [Risk 2] — Mitigation: [action]

## Decisions Needed
1. [Decision 1]
2. [Decision 2]

## Next 30-Day Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

---

### Use-of-Funds Template

```markdown
## Use of Funds — $[Total Raise]

| Category | Amount | % | Purpose |
|----------|--------|---|---------|
| Engineering / Product | $X | X% | [Hire N engineers, build Y feature] |
| Sales & Marketing | $X | X% | [CAC payback, channel expansion] |
| Operations | $X | X% | [Infrastructure, tooling] |
| G&A / Reserve | $X | X% | [Legal, accounting, buffer] |
| **Total** | **$X** | **100%** | |

**Runway Impact:** This raise extends runway from [current N months] to [projected N months], through [date], at which point we project [milestone: profitability / Series A readiness / etc.]

**Key Milestone Unlocked:** [What reaching the end of this runway proves to the next round investor]
```

---

### SAFE Summary Template

```markdown
## SAFE Terms Summary — [Company Name]

**Date Signed:** [Date]
**Investor:** [Name / Entity]
**Investment Amount:** $[X]

**Key Terms:**
- **Instrument:** Post-Money SAFE (YC Standard)
- **Valuation Cap:** $[X]M
- **Discount Rate:** [X]% (or None)
- **MFN:** Yes / No
- **Pro-Rata Rights:** Yes / No (threshold: $[X] investment)

**Conversion Trigger:** Equity Financing ≥ $[X]M
**Dissolution Priority:** Returns investor principal before common in dissolution event

**Notes:**
[Any custom provisions, side letters, or non-standard terms]

*This is a plain-English summary for record-keeping. The executed SAFE document governs all legal terms.*
```

---

## Narrative Framing Principles

### The Investor Memo Spine
Every strong investor memo hits these beats in order:
1. **Why now** — timing signal that makes this the right moment
2. **Why us** — team + unfair advantage
3. **Proof** — traction that de-risks the bet
4. **Math** — the numbers hold up under scrutiny
5. **Ask** — specific, sized, with clear use

### Common Mistakes to Flag
- Projections without assumptions → always show the assumptions
- "Conservative" projections that still assume 10x growth → call out the tension
- Vague use-of-funds ("growth") → force specific allocation
- Missing unit economics → CAC/LTV must appear for B2B/SaaS
- Round-numbered runway → calculate actual months from burn + cash

### Language Guidance
- Replace "disrupt" with specific market dynamics
- Replace "unique" with the actual differentiation
- Replace "traction" with the number
- Use "we" sparingly — the memo speaks, not just the founder
- Quantify everything that can be quantified

---

## Workflow

### Step 1: Gather Inputs
Collect the inputs listed above. If any critical inputs are missing, ask for them before drafting. Don't fabricate metrics.

### Step 2: Choose Document Type
Match the user's need to the document type. Confirm if ambiguous.

### Step 3: Draft with Template
Use the appropriate template as scaffold. Fill with actual data. Flag any gaps with `[NEED: ...]` placeholders.

### Step 4: Narrative Layer
Apply the Investor Memo Spine framework. Ensure the document tells a coherent story, not just a data dump.

### Step 5: Quality Check
- [ ] All numbers sourced from actual data (no estimates unless labeled)
- [ ] Projections show assumptions
- [ ] Unit economics present (if B2B/SaaS)
- [ ] Use-of-funds sums to raise amount
- [ ] Runway math is correct
- [ ] No legal claims (no "guaranteed returns", no securities language)
- [ ] Legal disclaimer if needed: "This is not an offer to sell securities."

### Step 6: Format & Deliver
Default output: Markdown. Ask user if they want plain text or JSON.

---

## Integration Points

| Upstream Skill | What It Provides |
|----------------|------------------|
| `startup-financial-model` | P&L, cash flow, runway math, projections |
| `cap-table-manager` | Cap table snapshot, dilution, round sizing |
| `kpi-alert-system` | Live KPI data for board updates |
| `budget-vs-actual` | Actuals vs plan for board update KPI table |

---

## Legal Disclaimer Boilerplate

For any memo that could be construed as a securities offering:

> *This document is for informational purposes only and does not constitute an offer to sell or a solicitation of an offer to buy any securities. Any offering of securities will be made only pursuant to definitive subscription documents. This summary is not a complete description of all material terms of any investment.*

Include this when: the document includes fundraising terms, investor ask, or projected returns.

---

## Examples

### Example 1: Quick One-Pager Request
**Input:** "Sam, write a one-pager for Apex AI. We're raising $1.5M SAFE at $8M cap. $42K MRR, growing 18% MoM. 3 months runway. B2B SaaS for construction PM teams."

**Action:** Use One-Pager template. Fill all known fields. Flag missing: team bios, TAM, CAC/LTV. Output markdown.

### Example 2: Board Update
**Input:** "Monthly board update for March. MRR hit $180K (plan was $165K). Burn $95K (was $88K due to new hire). Cash $1.1M. Big win: closed Acme Corp ($18K ACV)."

**Action:** Use Board Update template. Calculate runway (1.1M / 95K = 11.6 months). Flag: what decisions needed? What are Q2 priorities?

### Example 3: SAFE Post-Close Summary
**Input:** "Angel signed a $50K SAFE, $6M cap, 20% discount, MFN, no pro-rata."

**Action:** Use SAFE Summary template. Fill all terms. Add legal disclaimer boilerplate.

---

*PrecisionLedger — Precision. Integrity. Results.*
