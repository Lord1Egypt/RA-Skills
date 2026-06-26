---
name: portfolio-analytics
description: Computes portfolio risk and exposure metrics before sizing and rebalance decisions.
compatibility: Requires local holdings and price-history CSVs and optional benchmark/sector CSVs.
---

# Portfolio Analytics

## Purpose

Compute quantitative portfolio risk analytics before sizing and rebalance decisions.

## Scope

- Holdings and weights.
- Historical price/return series.
- Optional benchmark.
- Optional sector map.
- Optional liquidity fields.

## Non-goals

- No automatic rebalance.
- No absolute trade instructions.
- No live data fetching.

## Input contract

Required inputs:
- `HOLDINGS_CSV`: rows with portfolio holdings and position weights or fields sufficient to compute weights.
- `PRICE_CSV`: historical prices or returns for held symbols.

Optional inputs:
- `BENCHMARK_CSV`: benchmark prices or returns for beta and relative-risk context.
- `SECTOR_MAP_CSV`: symbol-to-sector mapping for sector exposure.
- Liquidity fields: average daily value, average volume, free float, or similar liquidity context when available.

## Execution workflow

1. Validate input files, required columns, date coverage, and symbol coverage.
2. Run `scripts/analyze_portfolio.py` with explicit holdings, price history, and optional benchmark or sector inputs.
3. Inspect metrics for risk level, concentration, correlation, benchmark sensitivity, and data limitations.
4. Prepare a handoff bundle for downstream sizing, rebalance, or risk-management review.

## Required output format

1. `Portfolio Metrics`
   - Total portfolio value or normalized weight base, number of holdings, volatility, annualized return when supported, max drawdown, and risk-adjusted metrics when supported.

2. `Benchmark Metrics`
   - Benchmark volatility, benchmark drawdown, portfolio beta, tracking error, and relative return when benchmark data exists.

3. `Correlation Summary`
   - Average pairwise correlation, highest correlated pairs, and diversification observations.

4. `Concentration Risk`
   - Top positions, top-position weight, top-five weight, Herfindahl-Hirschman Index, and concentration warnings.

5. `Sector Exposure`
   - Sector weights and sector concentration when sector mapping exists.

6. `Top Risk Contributors`
   - Holdings with the largest estimated contribution to portfolio volatility or drawdown risk.

7. `Confidence and Data Gaps`
   - Confidence level, missing inputs, stale data, short history, incomplete holdings, missing sector data, missing liquidity data, or missing benchmark data.

8. `Handoff Bundle`
   - Include the exact marker fields listed in `Handoff bundle`.

## Shared confidence rubric

- `High`: holdings are complete, weights reconcile, price history is long enough for the stated horizon, benchmark is available when beta or relative risk is discussed, and sector/liquidity coverage is broad.
- `Medium`: holdings and prices are usable, but one major input is partial, such as benchmark availability, sector mapping, liquidity coverage, or price-history length.
- `Low`: holdings are incomplete, weights do not reconcile, price history is short, benchmark is missing for beta-sensitive claims, or sector/liquidity coverage is sparse.

## Guardrails

- Do not infer precise beta without benchmark data.
- Downgrade confidence for short price history or thin symbol coverage.
- Treat analytics as context for sizing, rebalance, and risk-management decisions, not as commands.

## Handoff bundle

Include these exact marker fields:
- `as_of_date`
- `holdings`
- `weights`
- `portfolio_metrics`
- `benchmark_metrics`
- `correlation_summary`
- `concentration_risk`
- `sector_exposure`
- `top_risk_contributors`
- `confidence`
- `data_gaps`

## Trigger examples

- "Analyze this portfolio's volatility, drawdown, and concentration before I resize positions."
- "Compute portfolio beta and sector exposure using these holdings and benchmark files."
- "Review my current holdings for correlation, top risk contributors, and data gaps."
