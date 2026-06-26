---
name: openclaw-meta-ads
description: Shared Meta Ads skill for OpenClaw agents. Analyze Meta (Facebook and Instagram) ad accounts, campaigns, ad sets, ads, insights, and lead-form data with a production-safe read-first workflow. Use when an agent needs Meta Ads reporting, account audits, creative or audience diagnostics, lead-form review, or recommendations before live ad changes. Require explicit approval before any write action.
---

# OpenClaw Meta Ads

Use this skill for Meta Ads work across agents.

This is a shared skill, not a Poseidon-only skill.
Keep account-specific tokens, account IDs, and business rules outside the core skill.

## Use this skill for

- account and campaign performance reporting
- insights analysis
- campaign, ad set, and ad diagnostics
- lead-form and lead pipeline review
- creative and audience review
- structured recommendations before live changes

## Default stance

Start read-only.
Analyze first, recommend second, change last.
Do not make live Meta Ads changes without explicit approval.

## Access model

Meta account access is agent-specific.
The skill is shared, but each agent should use its own token, account ID, and permissions.
If credentials or permissions are missing, stop and fix access before pretending the skill can do real work.

## Setup and references

Read only what you need:
- `references/api-setup.md` for token, permission, and connection basics
- `references/account-structure.md` for campaign, ad set, ad, creative, insights, and leads structure
- `references/insights-queries.md` for common query patterns
- `references/audit-workflows.md` for practical review flows
- `references/optimization.md` for optimization heuristics and common mistakes
- `references/browser-fallback.md` only when API access is unavailable or UI confirmation is explicitly needed

## Safety rules

- never expose tokens or secrets in files or chat
- prefer read-only analysis before any operational change
- require explicit approval for pausing, enabling, editing, budget changes, or creative changes
- treat optimization guidance as heuristic, not universal truth
- scrub lead data for PII before broader reasoning when needed

## Output style

Lead with findings and recommended actions.
Keep reports practical:
- what is happening
- what looks wrong
- what to check next
- what to change, if approved
