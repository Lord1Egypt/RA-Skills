# openclaw-meta-ads

Shared Meta Ads skill for OpenClaw agents.

## Goal

Give agents a practical, production-safe way to analyze Meta Ads accounts, inspect campaign structure, review performance, audit lead flow, and recommend improvements without mixing in account-specific business rules.

## What this skill does well

- account and campaign reporting
- insights analysis
- audit workflows
- lead-form review
- creative and audience diagnostics
- optimization guidance grounded in practical heuristics

## What this skill is not

- a Poseidon-only skill
- a replacement for business-specific campaign strategy docs
- a license to make live account changes without approval
- a place to store tokens or account secrets

## Structure

```text
openclaw-meta-ads/
├── SKILL.md
├── README.md
├── references/
│   ├── api-setup.md
│   ├── account-structure.md
│   ├── insights-queries.md
│   ├── audit-workflows.md
│   ├── optimization.md
│   └── browser-fallback.md
└── scripts/
    ├── get_account_info.py
    ├── get_campaigns.py
    ├── get_insights.py
    └── get_leads.py
```

## Practical use order

1. verify token, account ID, and permissions
2. run read-only account or insights queries
3. audit the area in question
4. recommend actions
5. only make live changes with explicit approval

## Notes

- Keep account-specific learnings in the relevant agent or project docs.
- Keep the shared skill general.
- This v1 is intentionally docs-first. Add scripts later only when the API calls are stable and worth standardizing.
- If API access is unavailable, use the browser fallback only when explicitly needed.
