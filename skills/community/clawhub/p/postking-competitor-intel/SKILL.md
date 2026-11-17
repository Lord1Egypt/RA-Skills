---
name: postking-competitor-intel
description: Discover, register, and analyze a brand's competitors on PostKing — probe rival domains, classify candidates, and pull comparison intelligence.
license: MIT-0
compatibility: "Works with any MCP-compatible client connected to postking-mcp (local stdio or hosted at https://mcp.postking.app/mcp); the pking CLI is an optional fast path when a shell is available."
metadata:
  icon: https://raw.githubusercontent.com/bitsandtea/postking-skills/main/assets/icons/postking-competitor-intel.svg
  category: marketing
---

# Competitor Intelligence

Build a competitive-intelligence picture for a brand in PostKing — discover rivals, classify them, register and analyze them, and review the resulting comparison/overview data.

Once competitors are registered on the brand, PostKing's SEO clustering automatically becomes competitor-aware — see the `postking-seo` skill for how registered competitors then shape keyword clustering (product-fit classification + competitor "conquest" brief plans).

## When to Use

Use this skill when a user wants to know who their competitors are, wants specific domains tracked and analyzed, or wants a head-to-head comparison or landscape overview against registered rivals.

## When NOT to Use

Not for keyword/content work itself — once competitors are registered, hand off to `postking-seo` for competitor-aware clustering and conquest briefs. Not for generic brand content — that's `postking-social`/`postking`.

## Minimal tool subset

This skill needs 7 core tools:

- `competitor_probe` — discover candidate rival domains for the brand.
- `competitor_probe_status` — poll the probe.
- `competitor_probe_classify` — classify each candidate as direct / similar / not_relevant.
- `competitor_add` — register up to 20 domains as tracked competitors (async).
- `competitor_analyze` — re-run analysis on existing, pending/failed BrandCompetitor rows (async). Requires `brandCompetitorIds` (array of 1–20 tracked-competitor row IDs) — get them from `competitor_add`'s result or `competitor_list`.
- `competitor_list` — review registered competitors and their status.
- `get_job` — poll any async operation.

**Going deeper (optional)** — read/refresh intelligence on already-registered competitors:

- `competitor_get_comparison` — head-to-head keyword comparison against a competitor.
- `competitor_recompute_comparison` — refresh that comparison.
- `competitor_get_overview` — AI-synthesized landscape summary.
- `competitor_generate_overview` — (re)generate that overview (async).
- `competitor_comparison_sources` — the SEO sources feeding a comparison.
- `competitor_update` — edit a competitor row (e.g. toggle exclusion flags).
- `competitor_delete` — remove a competitor.

## Prerequisites

1. Authenticated with credits — see the `postking-getting-started` skill.
2. A brand already onboarded — see the `postking-getting-started` skill.

## Procedure

> "Find our competitors and register them."

Async tools return `{ operationId, status }` — poll `get_job({ operationId })` until `state` is `completed`, `failed`, `partially_failed`, or `cancelled`. `competitor_probe` returns `{ started: true }`; poll `competitor_probe_status` instead.

1. **Probe.** `competitor_probe({ brandId })` — kicks off discovery of candidate rival domains. Returns `{ started: true }`.
2. **Poll.** `competitor_probe_status({ brandId })` — poll until the probe completes.
3. **Classify.** `competitor_probe_classify({ brandId })` — classifies each discovered candidate as `direct`, `similar`, or `not_relevant`. Review the results with the user before adding — don't blindly register every candidate.
4. **Add.** `competitor_add({ brandId, domains: [...] })` — registers up to 20 domains as tracked competitors; each domain triggers its own crawl + profile analysis. Async, poll `get_job`.
5. **Get the tracked-competitor IDs.** `competitor_list({ brandId, detail: "medium" })` — returns each registered competitor's `id` and `analysisState`.
6. **Analyze (retry pending/failed rows).** `competitor_analyze({ brandId, brandCompetitorIds: [...] })` — `brandCompetitorIds` is required: 1–20 BrandCompetitor row IDs from step 5 (or directly from `competitor_add`'s result) whose `analysisState` is `pending` or `failed`. Async, poll `get_job`.
7. **Review.** `competitor_list({ brandId, detail: "medium" })` — status + analysis state per competitor.
8. **(Optional) Go deeper.** `competitor_get_comparison` / `competitor_recompute_comparison` for head-to-head keyword comparison against a specific competitor; `competitor_get_overview` / `competitor_generate_overview` (async, poll `get_job`) for an AI-synthesized landscape summary; `competitor_comparison_sources` for the SEO sources feeding the comparison; `competitor_update` (e.g. toggle exclusion flags) or `competitor_delete` to manage the list.

Next: with competitors registered, run the SEO pipeline in the `postking-seo` skill — clustering will now automatically flag competitor-dominated clusters and draft conquest briefs.

## CLI fast path

Most competitor management has a `pking competitors` CLI equivalent — it's not MCP-only:

```
pking competitors list [--brand <id>]
pking competitors add <domain1> <domain2> ...   [--no-wait]   # register up to 20 domains, async
pking competitors import --file <path>          [--no-wait]   # bulk-import domains from a file
pking competitors delete <id> --destructive
pking competitors refresh                       [--no-wait]   # re-analyze all (async)
pking competitors comparison                                  # head-to-head keyword comparison
pking competitors comparison recompute                        # refresh that comparison
pking competitors sample                                      # example competitor card
```

Discovery and read-only intelligence genuinely have no CLI path today — `competitor_probe`, `competitor_probe_status`, `competitor_probe_classify`, `competitor_get_overview`, `competitor_generate_overview`, and `competitor_comparison_sources` are MCP-only; drive those steps via MCP tool calls.

## Expected Output

A set of registered, classified, analyzed competitors on the brand, plus (optionally) a saved head-to-head comparison and landscape overview.

## Pitfalls

- `INSUFFICIENT_CREDITS` — point the user to the `postking-getting-started` skill's billing section (`billing_list_packs` → `billing_topup`).
- `RATE_LIMITED` — back off using the `retryAfter` value from the error envelope before retrying.
- `UNAUTHORIZED` — re-run the login flow described in the `postking-getting-started` skill.
- Assuming all `competitor_*` tools lack a CLI equivalent — only the discovery/probe and read-only overview/comparison-sources tools do; `list/add/import/delete/refresh/comparison/recompute/sample` all have `pking competitors` commands.

## Verification

- `competitor_list({ brandId })` should return successfully and reflect any domains just added.
- After `competitor_analyze` completes, `competitor_list({ brandId, detail: "medium" })` should show updated `analysisState` values.
