---
name: intelligence-desk-brief
description: Generate a portfolio-aware daily or on-demand risk analysis brief from public market data, company updates, earnings material, and macro context, then emit a host-consumable handoff for persistence. Every brief should open by restating the user's portfolio or watchlist and the industries or themes they care about, then explain what changed, which exposures matter, and what to make of it.
author: Prasham Shah
version: 1.0.0
requires:
  - python3
config:
  - name: CIVIC_CLIENT_ID
    description: Optional host-provided Civic client identifier for workspace and access boundary setup
    required: false
  - name: APIFY_API_TOKEN
    description: API token for Apify-backed retrieval and first-run task bootstrap when live providers are enabled
    required: true
  - name: APIFY_TASK_ID
    description: Optional manual override for the primary Apify task ID if host bootstrap is unavailable
    required: false
  - name: APIFY_X_TASK_ID
    description: Optional manual override for the X signals Apify task ID if host bootstrap is unavailable
    required: false
  - name: NOTION_PARENT_PAGE_ID
    description: Optional default host-managed Notion destination identifier for brief handoff
    required: false
examples:
  - "Create my daily Portfolio Risk Desk for NVDA, AMD, TSM, ASML and focus on AI infrastructure and semiconductors."
  - "Give me my daily brief for cybersecurity and tell me what changed in the risk map for my holdings."
  - "Compare the latest developments across cloud software and identify the most important cross-holding read-throughs for my watchlist."
  - "What changed since yesterday for my semis portfolio, and what should I make of it if rates keep moving higher?"
---

# Portfolio Risk Desk

## Positioning

This skill should be presented externally as `Portfolio Risk Desk`. The internal identifier can remain `intelligence-desk-brief` where needed for filenames or metadata.

## Purpose

This skill turns public market information into a portfolio-aware daily or on-demand analysis brief. It does not make decisions for the user. It maps a user's holdings and themes to simplified exposures, gathers supporting evidence, compares what changed over time, and explains the likely portfolio implications so the human can decide.

Every brief should begin by orienting the reader: clearly restate the portfolio or watchlist in scope and the industries or themes of interest before the analysis starts. The brief may still answer what happened, but its main job is to explain what to make of those changes for the user's exposures, drivers, and scenario risks.

This is a simplified public-markets research assistant, not an institutional-grade risk model. It produces factor-style decomposition, scenario analysis, peer read-throughs, and structured evidence from public information.

## Architecture boundary

This repo is the skill package. It owns retrieval, normalization, ranking, synthesis, rendering, and the host handoff payload.

OpenClaw or ClawHub should own:
- user authentication and workspace scoping
- provider secret management
- Redis-backed memory orchestration
- Notion API writes and persistence
- first-run Apify task bootstrap using the user's `APIFY_API_TOKEN`

That means this skill generates the brief and a stable handoff contract, while the host is responsible for executing Redis and Notion side effects.

## When to use

Use this skill when the user wants:
- A daily or on-demand brief for a portfolio, watchlist, or theme that goes beyond summarization
- A portfolio-aware read on which exposures, factors, and risk drivers matter most right now
- A sector pulse for an industry such as semiconductors, AI infrastructure, cybersecurity, cloud software, luxury retail, or fintech
- Peer read-throughs from one company update to other names
- A concise explanation of what changed, why it matters, and how the risk map has shifted since the last brief
- A simple scenario lens such as rates up, oil down, AI capex slowing, or one major holding missing expectations
- Delivery of the brief through a host-managed Notion handoff

Do not use this skill for:
- Trade execution
- Price targets or investment advice
- Fabricating missing evidence
- Hard claims without source support
- Claiming precise institutional-style factor or VaR modeling

## Inputs

The skill accepts:
- `portfolio_name` (optional)
- `holdings`: list of tickers
- `watchlist`: list of tickers
- `themes`: list of industries or themes
- `brief_type`: `daily`, `on_demand`, or `earnings_reaction`
- `lookback_hours`: integer, default 24 for daily and 72 for on-demand
- `delivery_target`: `notion` or `inline`
- `max_items_per_theme`: integer, default 8
- `benchmark_or_comparison_lens` (optional): index, peer basket, or prior brief comparison lens
- `scenario_questions` (optional): stress questions such as rates up 50 bps or a named company missing expectations

## Operating rules

1. Gather evidence first, synthesize second.
2. Separate facts from interpretation.
3. Rank relevance by user holdings, theme match, recency, cross-name impact, and change versus prior briefs when memory exists.
4. Prefer primary or direct-source material when available.
5. If support is weak, say it is weak.
6. Never recommend a trade. End with watchpoints, not commands.
7. Include source links or source titles for every key item.
8. Start the brief with a short user-focus snapshot that restates the portfolio or watchlist and the industries or themes being tracked.
9. Treat news as supporting evidence, not the main product.
10. Make explicit what changed, what exposures matter now, and what the user should monitor next.

## Workflow

1. Resolve tickers, company names, industries, and user-priority themes.
2. Map each holding or watchlist name to simplified exposures and factor buckets such as AI capex, semiconductor demand, rates sensitivity, consumer demand, China or regulatory exposure, supply-chain concentration, and earnings revision sensitivity.
3. Pull macro, company, peer, and public-web signals through Apify-backed collection, with X used as a complementary fast-moving signal source when available.
4. If live retrieval is enabled and task IDs are missing, bootstrap the user's saved Apify tasks from `APIFY_API_TOKEN`.
5. Normalize the evidence into structured notes that separate facts, interpretation, and confidence.
6. In OpenClaw, use memory tooling such as `memory_recall` to retrieve prior relevant notes and prior brief context before final synthesis when memory is available.
7. Score items by relevance, recency, impact, and change in the portfolio risk map.
8. Draft the brief in the required output template with exposures first, then changes, then scenarios, then evidence.
9. In OpenClaw, persist the most important resulting brief context through memory tooling such as `memory_store` so later runs can compare against it.
10. Deliver inline or emit a host-managed Notion handoff.

## OpenClaw Memory Guidance

When running inside OpenClaw or ClawHub with Redis-backed memory tooling available:
- Use `memory_recall` before drafting the final brief to retrieve recent prior brief context for the same portfolio/watchlist and themes.
- Prefer recalled brief summaries, dominant factors, top drivers, unresolved watchpoints, and recent high-signal items over generic conversation memory.
- Use `memory_store` after producing the brief to persist:
  - portfolio/watchlist and themes
  - summary
  - dominant factors
  - top drivers and read-throughs
  - risk-map changes
  - unresolved watchpoints
- Treat memory as a product aid, not as a license to make unsupported claims.
- If memory is unavailable or returns weak/noisy context, degrade gracefully and say the comparison is first-run or limited.

## Stack roles

- `Civic`: host-level least-privilege OAuth layer that helps constrain what the agent can access or do on behalf of the user.
- `Redis`: host-managed memory layer for prior briefs, normalized evidence, change logs, and cross-day comparison.
- `Apify`: broad public-web retrieval and scraping layer for company, macro, industry, and market evidence.
- `Apify tasks`: user-scoped saved tasks that can be created automatically during onboarding or set manually as a fallback.
- `X`: complementary high-velocity signal layer for official accounts, management commentary, and market-adjacent chatter. For MVP, this can be collected through Apify-backed workflows, with direct integration evaluated later.
- `Contextual AI`: optional comparison point or future enhancement for testing richer retrieval quality and memory continuity over time. It should be framed as an evaluation path, not a core dependency.
- `Notion`: host-managed persistence destination that consumes the handoff produced by this skill.

## Output requirements

Every brief must contain these sections:
- User focus snapshot
- Current exposure map
- Dominant factors
- What changed since last brief
- Key drivers and cross-holding read-throughs
- Scenario analysis
- Signal vs noise
- Open questions and watchpoints
- Evidence and sources

The executive summary should reiterate the portfolio or watchlist and the industries or themes so the user is immediately grounded in what the brief is about. It should also say what changed and what to make of it for the current portfolio risk map.

The exposure map should make dominant factors easy to scan, and every scenario should carry an explicit confidence level so the brief does not present speculative pathways too assertively.

Keep the brief concise, analysis-first, evidence-led, and explicit about uncertainty.
