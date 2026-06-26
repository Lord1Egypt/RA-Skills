# Decision-Support Contract

## Discovery Mode

Return a compact structured block with:

```json
{
  "run_id": "...",
  "timestamp": "...",
  "scan_scope": "...",
  "markets_scanned": 0,
  "priority_count": 0,
  "delta_vs_previous_scan": {
    "new": [],
    "upgraded": [],
    "downgraded": [],
    "removed": [],
    "unchanged": []
  },
  "watchlist": [],
  "top_opportunities": [
    {
      "market_id": "...",
      "event_slug": "...",
      "question": "...",
      "preferred_side": "yes|no",
      "ask": 0.0,
      "fair": 0.0,
      "edge": 0.0,
      "spread": 0.0,
      "data_status": "tradable|watch|unpriced",
      "priority": "high|medium",
      "analysis_note": "..."
    }
  ]
}
```

Rules:

- `top_opportunities` may be empty
- do not pad with weak ideas
- one binary market should contribute at most one preferred side
- avoid letting one event dominate the entire list unless that concentration is clearly intended
- this output identifies review candidates, not final trade instructions

## Deep Analysis Mode

Return a compact structured block with:

```json
{
  "market_id": "...",
  "question": "...",
  "data_status": "tradable|watch|unpriced",
  "orderbook_summary": {
    "best_bid_yes": 0.0,
    "best_ask_yes": 0.0,
    "best_bid_no": 0.0,
    "best_ask_no": 0.0,
    "spread_yes": 0.0,
    "spread_no": 0.0
  },
  "fair": {
    "fair_yes": 0.0,
    "fair_no": 0.0
  },
  "pricing_view": {
    "yes_vs_ask": 0.0,
    "no_vs_ask": 0.0,
    "preferred_side": "yes|no|none"
  },
  "review_priority": "high_priority_review|watch|low_priority",
  "analysis_summary": "...",
  "risk_flags": ["..."]
}
```

Rules:

- `high_priority_review` means the market deserves human or higher-level system attention soon
- `watch` means there is a possible idea but current state is not yet good enough
- `low_priority` means the edge is absent, too weak, or not worth active attention
- do not emit direct execution commands such as `buy_yes`, `buy_no`, or `skip`

## Cooldown Memory

When the skill loops, track at least:

- `market_id`
- last review priority
- last recommendation timestamp
- last deep-analysis timestamp
- last fair snapshot
- last top-of-book snapshot

If these are materially unchanged, do not repeat the same output.
