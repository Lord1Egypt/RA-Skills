# Gougoubi Create Prediction

Use this skill when the user wants to publish a new Gougoubi public prediction market from a small input surface.

Best for:

- market title plus deadline only
- automatic rules and tags
- deterministic group-first creation flow

Not for:

- adding conditions to an existing proposal
- activation, LP, settlement, or claims

Typical input:

```json
{
  "marketName": "Will BTC close above $100k on 2026-12-31?",
  "deadlineIsoUtc": "2026-12-30T16:00:00Z"
}
```

Script entry:

- `scripts/pbft-create-from-polymarket.mjs`
- `node scripts/pbft-create-from-polymarket.mjs --help`
- `node scripts/pbft-create-from-polymarket.mjs "<polymarket url>" --dry-run`
