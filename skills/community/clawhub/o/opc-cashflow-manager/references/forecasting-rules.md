# Cash Flow Forecasting Rules

Rules for probability-weighted cash flow forecasting. Solo founders live and die by cash timing — these rules enforce conservative, reality-based projections.

---

## Core Principle

**Cash ≠ Revenue.** An invoice sent is not money received. A verbal agreement is not a signed contract. A pipeline lead is not income. Every inflow gets a probability weight before it enters any forecast.

---

## Confidence → Probability Mapping

| Confidence | Probability Range | Default | Examples |
|------------|-------------------|---------|----------|
| **high** | 0.90 – 1.00 | 0.95 | Signed contract with payment terms, sent invoice (current), recurring client confirmed, deposit received |
| **medium** | 0.50 – 0.70 | 0.60 | Verbal agreement, proposal sent and acknowledged, likely renewal (no confirmation), milestone approaching |
| **low** | 0.10 – 0.30 | 0.20 | Pipeline lead, first contact / discovery call, speculative opportunity, referral not yet contacted |

**When no confidence is specified, default to medium (0.60).** Never assume high confidence without evidence.

Override rules:
- If a client has paid late 3+ times → downgrade confidence one level
- If invoice is overdue > 30 days → downgrade from high to medium
- If invoice is overdue > 60 days → downgrade to low
- If client is in dispute → set to low (0.1)

---

## Three-Scenario Model

Every forecast produces three scenarios. **Never show only one scenario.**

| Scenario | Inflow Factor | Outflow Factor | Use Case |
|----------|---------------|----------------|----------|
| **Base** | 1.0 | 1.0 | Expected case — probability weights applied as-is |
| **Conservative** | 0.7 | 1.1 | Pessimistic — 30% less income, 10% more expenses |
| **Aggressive** | 1.3 | 0.9 | Optimistic — 30% more income, 10% less expenses |

Calculation per scenario:
```
weighted_inflows = Σ(amount × probability_factor × scenario.inflow_factor)
total_outflows = Σ(committed + recurring_for_period) × scenario.outflow_factor
projected_cash = opening_cash + weighted_inflows - total_outflows
```

**Default display: conservative scenario first.** The founder should plan for the worst case and be pleasantly surprised.

---

## Forecast Granularity

| Period | Granularity | Rationale |
|--------|-------------|-----------|
| Week 1–4 (current month) | Weekly | Cash timing matters day-by-day in the near term |
| Month 2–4 | Monthly | Precision decreases with distance; monthly is sufficient |

For weekly breakdown:
- Assign each inflow/outflow to the week containing its expected_date/due_date
- If no specific date, distribute evenly across the month

---

## Inflow Timing Rules

| Inflow Type | Expected Date Logic |
|-------------|-------------------|
| Sent invoice (current) | Use due_date from invoice |
| Sent invoice (overdue) | Use today + 14 days (optimistic recovery) |
| Verbal agreement | Stated date + 14-day buffer |
| Proposal sent | Stated date + 21-day buffer |
| Pipeline lead | Stated date + 30-day buffer, low confidence |
| Recurring client | Use historical average payment date (or contract terms if no history) |
| Deposit/milestone | Use contract milestone date |

**Never use the "best case" date.** Always add a timing buffer for anything below high confidence.

---

## Outflow Timing Rules

| Outflow Type | Date Logic |
|--------------|-----------|
| Fixed date (rent, subscriptions) | Exact due_date |
| Variable (utilities, usage-based) | Last 3-month average amount, same due date pattern |
| One-time (equipment, services) | Exact date or user estimate |
| Tax payments | Known quarterly dates (or user-specified) |
| Recurring auto-generate | Use next_due_date, then advance by frequency |

---

## Recurring Expansion

For forecast periods beyond the current month, expand recurring_commitments:

```
For each recurring item:
  current_date = next_due_date
  while current_date <= forecast_end:
    add to outflows for that period
    advance current_date by frequency
```

Frequency advancement:
- weekly: +7 days
- biweekly: +14 days
- monthly: +1 month (same day, cap at month end)
- quarterly: +3 months
- annual: +12 months

---

## Weighted Amount Calculation

```
weighted_amount = Decimal(amount) × Decimal(probability_factor)
```

Always use Decimal for calculation. Store weighted_amount as decimal-safe string.

Round only for display (2 decimal places). Never round during intermediate calculations.

---

## Invoice Import Rules (from opc-invoice-manager)

When importing invoices as expected_inflows:

| Invoice Status | → Inflow Confidence | → Probability |
|----------------|---------------------|---------------|
| sent (current, not overdue) | high | 0.95 |
| sent (overdue 1–30 days) | medium | 0.60 |
| sent (overdue 31–60 days) | low | 0.30 |
| sent (overdue 60+ days) | low | 0.10 |
| partial | high (for remaining) | 0.80 |
| disputed | low | 0.10 |
| draft | — (skip, not sent yet) | — |
| paid | — (skip, already received) | — |
| void | — (skip) | — |

Use `outstanding_amount` (not `total_amount`) for partial invoices.

---

## Don't Do This

1. **Don't count pipeline as revenue.** A lead is not income. Use low confidence (0.2) maximum.
2. **Don't ignore seasonality.** If December is always slow, adjust medium-confidence inflows down.
3. **Don't assume on-time payment.** Even high-confidence inflows should use 0.95, not 1.0.
4. **Don't hide the conservative scenario.** Always show it. Always show it first.
5. **Don't mix cash and accrual.** This is a cash flow tool. Revenue recognized ≠ cash received.
6. **Don't round during calculation.** Use Decimal throughout. Round only for final display.
7. **Don't forecast beyond 4 months.** Accuracy degrades rapidly. Show 4 months max.
8. **Don't skip the alerts.** Every forecast run must check alert thresholds and surface warnings.
