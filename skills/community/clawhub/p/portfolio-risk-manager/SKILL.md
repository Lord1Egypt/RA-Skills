---
name: portfolio-risk-manager
description: Establishes portfolio discipline through a mini IPS, risk budgeting, and no-margin position sizing for Vietnam equity investors; converts recommendations into conditional triggers, invalidation rules, horizon, and confidence.
metadata: {"openclaw":{"emoji":"🛡️"}}
disable-model-invocation: false
---

# Portfolio Risk Manager (No Margin, No Sector Preference)

## Purpose

Use this skill as the portfolio constitution and risk-budgeting layer. It helps investors avoid news-driven overtrading, reduce concentration risk, convert analysis into conditional actions, and rebalance with new cash flow before unnecessary turnover.

## Scope

- Vietnam equity investors.
- No margin or leverage.
- No derivatives.
- No forced sector preference.
- User-confirmed watchlist only (`ACTIVE_WATCHLIST`).

## Non-goals

- Do not issue absolute buy/sell instructions.
- Do not propose margin, derivatives, or leverage.
- Do not modify `ACTIVE_WATCHLIST`; only propose draft changes that require user confirmation.

## Input contract

Minimum required inputs:
- `ACTIVE_WATCHLIST`: user-confirmed tickers.
- `MONTHLY_CASH_INFLOW_VND`: monthly contribution amount. If missing, assume `10000000` and disclose the assumption.

Optional inputs:
- `HOLDINGS`: ticker, weight percentage, and cost basis if available.
- `RISK_PROFILE`: horizon and maximum drawdown target.
- `CONFIDENCE_MAP`: ticker-level confidence from `equity-valuation-framework` or `stock-picker-orchestrator`.

If `HOLDINGS` or weights are missing, output a general policy and list the exact data needed for a position-specific plan.

## Output format (required)

Return exactly these five sections:

### 1) IPS Mini
- Objective
- Horizon
- Target maximum drawdown
- 6-10 discipline rules

### 2) Sizing Policy
Default policy unless the user provides a different risk profile:
- `max_single_name_weight_pct`: 10-12%
- `starter_position_pct`: 2-3%
- `add_on_step_pct`: 1-3% per confirmation event
- `cash_buffer_pct`: 5%
- `leverage_pct`: 0%
- `target_weight_pct`
- `max_weight_pct`
- `estimated_trade_value_vnd`
- `requires_user_confirmation`

### 3) Per-Ticker Risk Plan
For each watchlist ticker:
- Horizon
- Trigger to add risk
- Trigger to reduce risk
- Invalidation condition
- Confidence and data gaps

### 4) Rebalance Plan
- Cadence: monthly review
- Drift threshold: 5 percentage points from target weight unless the user specifies otherwise
- Prefer new cash flow for rebalancing before selling existing positions

### 5) Next Review Checklist
Provide 3-8 items covering important triggers, data to verify, and upcoming events to monitor.

## Guardrails

- Treat `ACTIVE_WATCHLIST` as the single source of truth.
- Use conditional action framing, not absolute trading instructions.
- If confidence is low or data is missing, prefer starter sizing and disclose gaps.
- Separate `Fact`, `Assumption`, and `Inference`.
- Recommendation labels may be converted into target weights, but target-state updates require explicit user approval and must be routed through `institutional-governance`.
- Broker execution is disabled in the current phase.
- Treat approved target state as a portfolio planning record, not a broker order.

## Workflow

1. Build the IPS mini from the user's constraints.
2. Set the sizing policy.
3. Map each watchlist ticker to triggers and invalidation conditions using available macro, news, valuation, and confidence inputs.
4. Define the rebalance cadence and drift threshold.
5. Return the checklist and unresolved data gaps.
