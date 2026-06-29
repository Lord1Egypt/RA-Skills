---
name: market-trading-workflow
description: "Conservative World Cup fixture-trading workflow for ClawHub: discover a market, validate the matchup, price the edge, and trade only when safe."
version: 1.0.20
author: Hermes Agent
license: MIT
metadata:
  author: Hermes Agent
  version: "1.0.20"
  displayName: World Cup Head to Head Fixture Trader
  difficulty: intermediate
---

# World Cup Head to Head Fixture Trader

## Overview

Use this skill as a reusable playbook for World Cup fixture trading in ClawHub-compatible agents.
It bundles two layers:
- a research layer that estimates win / draw / loss probabilities for matchup-style markets and can enrich them with FotMob-style pre-match context when match ids are available
- an execution layer that discovers the live market, validates the fixture, and decides whether to trade or pass

Supporting notes live in `references/session-notes.md`.

It turns a market idea into a disciplined bet-or-pass decision:

1. discover the current market at runtime
2. resolve a fresh market id
3. fetch market context
4. compare fair value to market price
5. trade only if the fixture mapping is trustworthy and the edge is meaningful
6. otherwise pass cleanly with a reason

The research and discovery layers share one team-normalization module, so alias fixes land once and apply everywhere.

The workflow is intentionally conservative. A stale market, wrong fixture, or unresolved context is more dangerous than missing a marginal edge.

## Supporting files

- `references/session-notes.md` — bundled research/execution split, SDK compatibility fallback, and publishing lessons from this session.
- `references/team-name-normalization.md` — canonical aliases, regression examples, and the shared normalization rule.
- `references/world-cup-market-discovery.md` — live-slate discovery recipe, matchup parsing, and query caveats.
- `references/automated-slate-scan.md` — when to scan the slate automatically, how to filter by date, and the common alias pitfalls.
- `references/clawhub-publishing.md` — ClawHub publish checklist and verification steps.
- `references/stake-sizing-guidance.md` — when to size down moderate underdogs versus passing extreme longshots.
- `scripts/team_names.py` — single source of truth for canonical team names and query expansion.
- `scripts/team_name_smoke_test.py` — quick regression check for alias/canonicalization drift.

## How to use this skill

Start with the *fixture*, not the venue:
- identify the teams or outcome being traded
- discover the current market fresh
- normalize team names before comparing the model and market labels
- verify that the market question matches the intended event
- price the market against your own fair value
- only enter when the edge is strong enough to survive slippage and live-state changes

When the user asks for "today's games", "tomorrow's games", or "all games in the slate", use the automated slate scan first instead of waiting for them to name the teams. This is especially important when the relevant fixture is hidden behind a multilingual alias.

When the market or model uses different team names, canonicalize both through `scripts/team_names.py` first; do not maintain separate alias rules in the research and execution scripts.

If anything looks stale, mismatched, or ambiguous, skip the trade and report the blocker.

## When to use

Use this skill when you need to:
- keep trades conservative and explainable
- normalize multilingual team aliases and accented variants before pricing/discovery
- scan markets at runtime instead of hardcoding IDs
- decide whether to place a trade or return no bet
- include pre-match context like xG, injuries, lineups, and suspensions when the market context exposes a usable event or match id

## Core principles

1. **Use SimmerClient for trades.**
   Do not call Polymarket CLOB directly from the skill.

2. **Default to paper trading on sim.**
   Paper and live share the same trade/pass decision gates; `--live` only changes whether the executed order is real-money or paper on sim.

3. **Tag every trade.**
   Include `source` and `skill_slug` so P&L and rebuy protection work correctly.

4. **Report both sides.**
   Include `model_yes/model_no` and `market_yes/market_no` in summaries so the report is readable without manual subtraction.

5. **Paper trade on sim by default.**
   Use the same edge threshold and pass/trade logic for paper and live; if the venue is simulated, submit the paper trade and include the simulated fill result. Reserve `--live` for real-money execution only.
   Moderate underdog or draw-leaning plays can size down when the model is near the market and the side is not a true longshot.
   Do *not* downsize into extreme underdogs or 80/20-vs-90/10 style flips; those should usually pass unless the model truly supports the upset.

6. **Read secrets from env.**
   Never hardcode API keys or private credentials.

7. **Keep `skill_slug` aligned.**
   The slug in `clawhub.json`, `SKILL.md`, and runtime tags should match.

8. **Pass on uncertain mappings.**
   If the market lookup or fixture validation is fragile, do not force a bet.

## Suggested operating sequence

### Step 1: Discover
Find the active market using runtime search or tags.

### Step 2: Validate
Check the market page, question text, and event identity.

### Step 3: Price
Estimate fair probability and compare it to market price.

### Step 4: Gate
Require:
- trustworthy fixture mapping
- meaningful edge
- liquidity/slippage that still works
- live state that does not contradict the thesis
- the same pass/trade rule for paper and live; only the execution mode changes

### Step 5: Act or pass
If all gates pass, trade.
If any gate fails, return pass with a concrete reason.

## Reporting template

Use this format when summarizing a decision:

- **Market:** `<question or id>`
- **Model yes/no:** `<model_yes> / <model_no>`
- **Market yes/no:** `<market_yes> / <market_no>`
- **Edge:** `<edge>`
- **Confidence:** `<low/medium/high>`
- **Decision:** `<paper-trade / trade / pass>`
- **Reason:** `<exact blocker or thesis>`

## Common blockers

- stale or wrong market ID
- unresolved market context
- unparseable market question
- fixture mismatch
- team-name alias mismatch, including multilingual equivalents and accent variants (for example `South Korea` vs `Korea Republic`, `Bosnia` vs `Bosnia and Herzegovina`, `Ivory Coast` vs `Côte d'Ivoire`, or `Cape Verde` vs `Cabo Verde`)
- moderate underdogs or draw-leaning spots can size down
- extreme underdogs and 80/20-vs-90/10 style flips should usually pass unless the model truly supports the upset
- fragile underdog setup
- live state no longer supports the thesis
- execution blocked because the venue was not sim/live as requested

## Regression guardrails

- Keep canonical names and alias expansion in one shared module.
- Prefer multilingual alias groups and accent-stripped normalization for country names that are identical by locale rather than meaning.
- Add a smoke test whenever a new alias is discovered or a market search misroutes to the wrong team.
- If discovery returns multiple candidates, score the question text and pick the best match instead of taking the first hit.
- For slate requests, run the automated slate scan and keep only fixture-style questions with a parsed team pair.
- Use the raw market label in reports, but the canonical form for pricing/lookup.

## Publishing note

A ClawHub-ready skill folder should include:
- `SKILL.md`
- `clawhub.json`
- a main Python script
- `DISCLAIMER.md`

See `references/publishing-flow.md` for the repeatable login/logout/publish sequence, device-flow auth, and account-switching notes.
See `references/simmer-sdk-compat.md` for the runtime-safe discovery and trade-call pattern that works across older and newer `simmer-sdk` installs.

Use the official ClawHub publish command from inside the folder:

```bash
npx clawhub@latest publish . --slug market-trading-workflow --version 1.0.20
```

If publishing is blocked by an account policy, switch to a qualifying account and repeat the device-login flow before retrying publish.
If a device code expires, restart `clawhub login --device --no-browser` to get a fresh code.

