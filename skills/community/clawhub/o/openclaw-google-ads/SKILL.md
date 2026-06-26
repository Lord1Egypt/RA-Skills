---
name: openclaw-google-ads
description: Shared Google Ads API skill for OpenClaw agents. Query account, campaign, ad group, keyword, search term, and performance data with local scripts and GAQL examples. Use when an agent needs Google Ads reporting, campaign audits, wasted spend checks, conversion-tracking review, or production-safe campaign analysis. Prefer read-first analysis and require explicit approval before live account changes.
---

# OpenClaw Google Ads

Use this skill for Google Ads API work across agents.

This is a shared skill, not a Sea Cool-only skill.
Keep account-specific practices in project docs or memory, not in the core skill.

## Use this skill for

- campaign and account performance reporting
- account health audits
- wasted spend review
- search term and keyword analysis
- conversion tracking review
- structured GAQL querying
- production-safe recommendations before live changes

## Default stance

Start read-only.
Analyze first, recommend second, change last.
Do not make live account changes without explicit approval.

## Access model

Google Ads API Basic Access is suitable for real production use.
If credentials are missing or invalid, stop and fix access before pretending the skill can do real work.

## Setup and references

Read only what you need:
- `references/api-setup.md` for credentials, auth flow, and connection testing
- `references/gaql-examples.md` for query patterns
- `references/audit-workflows.md` for practical account review flows
- `references/optimization.md` for optimization heuristics and common mistakes
- `references/browser-fallback.md` only when API access is unavailable or UI confirmation is explicitly needed

## Available scripts

- `scripts/authenticate.py`
- `scripts/gaql_query.py`
- `scripts/get_account_summary.py`
- `scripts/get_campaigns.py`

Use scripts for repeatable API work.
Use references for judgment.

## Safety rules

- never expose tokens or credentials in files or chat
- prefer read-only analysis before any operational change
- require explicit approval for pausing, enabling, editing, or budget changes
- treat optimization advice as heuristics, not universal truth
- when customer-identifying data appears in exported reports or account notes, apply PII protection before broader model use

## Output style

Lead with findings and recommended actions.
Keep reports practical:
- what is happening
- what looks wrong
- what to check next
- what to change, if approved
