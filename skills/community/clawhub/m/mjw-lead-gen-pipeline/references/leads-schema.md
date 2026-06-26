# leads.md Schema

## File Location
`~/workspace/leads.md`

## Format

```markdown
# Leads — [Trade] in [City, State]
_Last updated: YYYY-MM-DD_

## Summary
- Total qualified: X
- Built: X
- Deployed: X
- Pitched: X
- Replied: X

## Leads

| # | Business | Phone | Address | Trade | Has Site? | Site Notes | Demo URL | Status | Pitched At | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Apex Plumbing | (555) 123-4567 | 123 Main St, Austin TX | Plumber | No | — | http://187.x.x.x:8090 | deployed | — | |
| 2 | Bob's Electric | (555) 987-6543 | 456 Oak Ave, Austin TX | Electrician | Yes | Broken mobile, no SSL | http://187.x.x.x:8091 | pitched | 2026-04-04 | |
```

## Status Flow

```
qualified → built → deployed → pitched → replied → closed
                                                  ↘ lost
```

## Notes Column

Use for: reply content, follow-up dates, special instructions, client objections.
