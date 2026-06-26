# Look Storage and Config

## Storage
```
~/openclaw/data/ocas-look/
  config.json
  state.json
  events.jsonl
  decisions.jsonl
  reports/
  artifacts/evidence/
  artifacts/drafts/
  artifacts/receipts/

~/openclaw/journals/ocas-look/
  YYYY-MM-DD/
    {run_id}.json
```

## Config Fields
- Capability toggles by domain
- Confidence thresholds
- Rate limits
- Privacy retention settings
- User profile: diet (vegetarian), location
- Event: capture-location-as-venue = false
- Commerce: auto_purchase = false, auto_order = false
- Drive: auto-file requires confirmation
- Maps: try-list name = "To try"
