---
name: aso-audit
description: >-
  Audit and improve an app's App Store discoverability through MetaRun:
  keyword rankings per country, metadata lint, rival tracking, real Apple
  search analytics, and answer-engine (AI assistant) visibility. Trigger
  phrases: "ASO audit", "why am I not ranking", "check my keywords",
  "does ChatGPT recommend my app", "compare me to competitors".
metadata:
  openclaw:
    homepage: https://metarun.dev/agents
    primaryEnv: METARUN_TOKEN
    envVars:
      - name: METARUN_TOKEN
        required: false
        description: MetaRun personal access token (Settings, MCP). Not needed after `npx metarun login`, which stores it in ~/.metarun/config.json.
    requires:
      anyBins:
        - npx
---

# ASO audit: where the app is found, and where it is invisible

You are auditing discoverability through MetaRun. Two different battlefields,
audited together: App Store SEARCH (rankings for typed keywords) and ANSWER
ENGINES (whether an AI assistant names the app when asked "best X app").
They move independently; a strong rank with zero assistant visibility is a
finding, not a contradiction.

## Ground rules

- Tools run over MetaRun's MCP server or `npx metarun run <tool> '<json>'`.
  Fetch unfamiliar schemas with `npx metarun tools <tool-name> --json`.
- This mission MEASURES and DIAGNOSES. Nothing here posts, publishes, or
  seeds content anywhere, and metadata fixes are staged through previews the
  user confirms; that separation is a MetaRun product principle, state it if
  the user asks for astroturfing.
- Answer-engine scans (`aeo_scan_answers`) are METERED against the user's
  plan. Say so before running one; suggest, never auto-fire.

## The mission

### 1. Search rankings, as they stand

- `aso_list_tracked_keywords` -> what is already watched. Nothing tracked?
  `aso_suggest_keywords` proposes terms from the listing; confirm with the
  user, then `aso_track_keywords`.
- `aso_scan_ranks` refreshes tracked ranks; `aso_check_rank` spot-checks any
  term/territory live. `aso_keyword_history` shows the trend;
  `aso_keyword_leaders` shows who owns the term.

### 2. Metadata quality

- `aso_lint_metadata` runs the rulebook over the live listing: wasted
  keyword characters, duplication across fields, budget violations.
- `aso_cross_locale_plan` finds free keyword real estate: each storefront
  indexes extra locales (US reads nine), so unused locale slots are extra
  100-character keyword fields. Fixes stage via the localize-listing
  mission's preview/apply pairs.

### 3. Ground truth from Apple

- `aso_get_search_performance` returns MEASURED search vs browse
  impressions, product-page views, and per-territory conversion, plus a
  featuring detector. If it reports not_enabled, offer
  `aso_enable_search_analytics` (needs an Admin key; Apple's first reports
  take 1-2 days).

### 4. Rivals

- `aso_scan_rivals` diffs tracked competitors' listings against their last
  snapshot: renamed apps, new subtitles, screenshot count changes. A rival
  suddenly bidding on a keyword shows up here before it shows in ranks.

### 5. The second store: answer engines

- `aeo_visibility_report` -> current share of voice: which assistants name
  the app, at what position, versus which rivals.
- `aeo_suggest_questions` composes the buyer questions worth tracking (from
  category, tracked keywords, and rivals); `aeo_track_questions` commits
  them; `aeo_scan_answers` (metered, confirm first) probes the live engine.
- `aeo_source_gap` is the actionable end: the ranked list of web sources the
  assistant actually read, and which of them omit the app. That list is the
  user's off-platform work queue; MetaRun will not do that outreach.

### 6. Report

One page, ranked by leverage: quick metadata wins (with staged previews
ready), rank trends worth watching, the Apple-measured funnel, rival moves,
and the answer-engine gap with its source list. Every recommended write goes
through preview -> user confirm -> apply; nothing is auto-applied.

## Beyond this mission

The Sentinel watches tracked ranks in the background and files findings:
`aso_list_sentinel_findings`. Scheduled promotional text runs through
`aso_schedule_promo_text`. Discover more: `npx metarun tools aso`.
