# openclaw-google-ads

Shared Google Ads API skill for OpenClaw agents.

## Goal

Give agents a practical, production-safe way to analyze Google Ads accounts, run structured queries, audit account health, and recommend improvements without mixing in account-specific business rules.

## What this skill does well

- account and campaign reporting
- GAQL-based querying
- audit workflows
- wasted spend analysis
- conversion tracking review
- optimization guidance grounded in practical heuristics

## What this skill is not

- a Sea Cool-only skill
- a replacement for business-specific campaign strategy docs
- a license to make live account changes without approval
- a place to store credentials

## Structure

```text
openclaw-google-ads/
├── SKILL.md
├── README.md
├── requirements.txt
├── references/
│   ├── api-setup.md
│   ├── gaql-examples.md
│   ├── audit-workflows.md
│   ├── optimization.md
│   └── browser-fallback.md
└── scripts/
    ├── authenticate.py
    ├── gaql_query.py
    ├── get_account_summary.py
    └── get_campaigns.py
```

## Practical use order

1. verify credentials and connection
2. run read-only summary or GAQL queries
3. audit the account or campaign area in question
4. recommend actions
5. only make live changes with explicit approval

## Notes

- Keep account-specific learnings in the relevant agent or project docs.
- Keep the shared skill general.
- If API access is unavailable, use the browser fallback only when explicitly needed.
