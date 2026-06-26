# Rally Data Model

## PortfolioState
```json
{
  "portfolio_id": "string",
  "as_of": "string (ISO 8601)",
  "holdings": [
    {
      "symbol": "string",
      "shares": "number",
      "cost_basis": "number",
      "current_price": "number",
      "acquisition_date": "string (ISO 8601)",
      "sector": "string (GICS sector)",
      "trailing_high": "number",
      "trailing_high_date": "string (ISO 8601)",
      "current_atr_14": "number | null"
    }
  ],
  "cash": "number",
  "cash_target_pct": "number",
  "constraints": "object",
  "peak_value": "number",
  "peak_value_date": "string (ISO 8601)",
  "drawdown_reduction_active": "boolean"
}
```

## ResearchCandidate
```json
{
  "symbol": "string",
  "name": "string",
  "sector": "string (GICS sector)",
  "signals": "object",
  "signal_scores": {
    "quality": "number",
    "momentum": "number",
    "safety": "number",
    "reversion": "number",
    "congressional_flow": "number | null"
  },
  "composite_score": "number",
  "percentile_rank": "number",
  "confidence": "number",
  "realized_vol": "number | null",
  "momentum_path_r2": "number",
  "next_earnings_date": "string (ISO 8601) | null",
  "scoring_method": "sector_blended",
  "congressional_trades": {
    "distinct_buyers": "number",
    "distinct_sellers": "number",
    "cluster_detected": "boolean",
    "committee_weighted": "boolean",
    "data_source": "string",
    "data_as_of": "string (ISO 8601)"
  },
  "evidence_refs": ["string"]
}
```

## AllocationPlan
```json
{
  "plan_id": "string",
  "timestamp": "string (ISO 8601)",
  "regime": "normal | cautious | defensive",
  "regime_detail": {
    "composite_score": "number",
    "signal_scores": {
      "trend": "number",
      "credit": "number",
      "volatility": "number",
      "breadth": "number"
    },
    "signals_unavailable": ["string"],
    "confidence_floor_applied": "number"
  },
  "sizing_method": "score_vol_weighted | score_weighted | equal_weight",
  "cash_target_pct": "number",
  "targets": [
    {
      "symbol": "string",
      "sector": "string (GICS sector)",
      "target_pct": "number",
      "rationale": "string",
      "evidence_refs": ["string"]
    }
  ],
  "sector_allocations": {
    "sector_name": "number (aggregate pct)"
  },
  "constraints_applied": "object",
  "risk_checks": "object",
  "rebalance_triggers_fired": ["string"],
  "turnover_pct": "number",
  "deferred_changes": ["string (symbols deferred due to turnover cap)"],
  "correlation_penalties": [
    {
      "pair": ["string", "string"],
      "correlation": "number",
      "action": "penalized | dropped"
    }
  ],
  "earnings_actions": [
    {
      "symbol": "string",
      "action": "hold_through | reduced | entry_deferred",
      "earnings_date": "string (ISO 8601)",
      "original_weight": "number",
      "adjusted_weight": "number"
    }
  ]
}
```

## TradePlan
```json
{
  "plan_id": "string",
  "timestamp": "string (ISO 8601)",
  "allocation_plan_id": "string",
  "orders": [
    {
      "symbol": "string",
      "action": "buy | sell",
      "shares": "number",
      "rationale": "string",
      "is_emergency": "boolean",
      "holding_period": "short_term | long_term | null"
    }
  ],
  "execution_enabled": "boolean",
  "estimated_turnover_pct": "number"
}
```

## WashSaleExclusion
```json
{
  "symbol": "string",
  "sale_date": "string (ISO 8601)",
  "sale_price": "number",
  "loss_amount": "number",
  "reentry_eligible_date": "string (ISO 8601)",
  "reason": "tlh | emergency_sell | rebalance",
  "is_substantially_identical": "boolean",
  "parent_symbol": "string | null",
  "relationship": "string (share_class | sector_etf | null)"
}
```

## FactorIC
```json
{
  "run_id": "string",
  "timestamp": "string (ISO 8601)",
  "category": "quality | momentum | safety | reversion | congressional_flow",
  "ic_value": "number",
  "forward_return_period_days": "number",
  "rolling_avg_ic": "number",
  "alert_active": "boolean"
}
```
