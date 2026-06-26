---
name: gptsportswriter
description: Generate sports betting research reports using live odds, matchup context, and public/news sources. Supports premium mode with API-backed odds/news and free fallback mode with public-source workflows. Use for best bets of the day, matchup breakdowns, sportsbook-style summaries, and structured betting reports. Prefer this skill for research and summaries, not for placing bets or claiming guaranteed outcomes.
---

# GPTSportswriter

## Overview

Use this skill to generate structured sports betting research reports.
It can operate in:
- **premium mode** with API-backed odds and news context
- **free mode** with public-source workflows and extraction helpers

The goal is to surface current matchups, betting angles, and relevant context in a clean format without pretending certainty.

## Data Priority

The skill supports three modes:
- **auto** (default): use paid sources when configured, otherwise fall back
- **premium**: require paid sources
- **free**: use only free/public sources

1. **Primary source in premium/auto mode: The Odds API**
   - Use it first for:
     - today's matchups
     - moneylines
     - spreads
     - totals
     - sportsbook availability
   - Treat this as the source of truth for what games and lines actually exist right now.

2. **Secondary source in premium/auto mode: AskNews + web search**
   - Use AskNews first for:
     - recent sports articles
     - matchup previews
     - injury/news context
     - broader same-day coverage summaries
   - Use web search as a fallback or supplement for:
     - betting previews
     - source consensus and disagreement
     - extra matchup-specific context
   - Do not let article coverage override current market reality when the odds data says otherwise.

3. **Free mode fallback**
   - Use public odds/news pages when the user does not want paid services or when no API keys are configured.
   - Prefer public pages from sources like:
     - Covers
     - OddsShark
     - Yahoo Sports
     - AP
     - ESPN
     - CBS Sports
   - Be explicit that free-mode odds can be more stale and less precise.

## Workflow

1. Identify the slate.
   - If the user says "today," use today's games only.
   - If the user names a league, focus there.
   - If the request is broad, cover major in-season sports.
   - For Premier League soccer, use the Odds API sport key `soccer_epl`.

2. Pull current odds and matchups first.
   - Use The Odds API to get the current slate.
   - Prefer commonly used U.S. books when comparing prices.
   - Note where prices differ meaningfully by book.

3. Search for context.
   - First use `scripts/fetch_asknews.py` for article context.
   - Then, if needed, search the web for combinations like:
     - `best bets today [sport]`
     - `[league] picks today odds`
     - `[matchup] betting preview`
     - `[team] injuries betting line`
   - Prefer same-day results.
   - Pull multiple sources before summarizing.

4. Cross-check before recommending anything.
   - Look for overlap between current odds and web consensus.
   - Separate consensus picks from one-off hot takes.
   - Note line sensitivity explicitly.
   - If a good angle depends on getting a better number at a specific book, say that.

5. Write the summary.
   - Include the event, market, current line range, and the reasoning in one or two lines.
   - Mention uncertainty, injuries, schedule spots, or stale-preview risk when relevant.
   - Keep it readable and useful, not breathless.

## Required Structured Output

Unless the user explicitly asks for a different format, use this exact output shape:

**GPTSportswriter — Best Betting Advice of the Day**
**Date:** [today]
**Scope:** Broad daily slate across in-season sports

**Top Looks Today**
1. **[Event or matchup]**
   - **Market:** [spread / moneyline / total / prop]
   - **Lean:** [the recommended side or angle]
   - **Current odds:** [best current range found]
   - **Why this play:** [1-2 short sentences]
   - **Confidence:** Low / Medium / High

2. **[Event or matchup]**
   - **Market:** [spread / moneyline / total / prop]
   - **Lean:** [the recommended side or angle]
   - **Current odds:** [best current range found]
   - **Why this play:** [1-2 short sentences]
   - **Confidence:** Low / Medium / High

3. **[Event or matchup]**
   - **Market:** [spread / moneyline / total / prop]
   - **Lean:** [the recommended side or angle]
   - **Current odds:** [best current range found]
   - **Why this play:** [1-2 short sentences]
   - **Confidence:** Low / Medium / High

**Consensus Signals**
- [short bullet on where multiple sources overlap]
- [short bullet on a repeated theme or angle]

**Watch-Outs**
- [injury/news uncertainty]
- [line movement or stale odds risk]
- [source disagreement or thin support]

**Bottom Line**
- [one short paragraph with the overall takeaway]

## Fallback Rules

- If The Odds API is unavailable, say that plainly and fall back to web-only summaries.
- If you only find one or two credible angles, do not force a third pick.
- If sources are weak or old, say that clearly in **Bottom Line**.
- If the user asks for only one best bet, still include:
  - Market
  - Lean
  - Current odds
  - Why this play
  - Main caveat
  - Confidence

## Standards

- Do not claim guaranteed wins.
- Do not fabricate odds, records, injuries, or sportsbook prices.
- Prefer "sources are leaning" over "this will hit."
- If the market has already moved away from the good number, say so.
- If the web results are thin or conflicting, say so plainly.

## The Odds API Notes

- Use the configured `THE_ODDS_API_KEY` from environment.
- Prefer current pregame markets where available.
- Compare multiple bookmakers before quoting a range.
- Be explicit when a price is widely available versus only available at one book.
- Use `scripts/fetch_odds.py` to fetch and normalize live odds before writing the summary.

### Script usage

Fetch normalized odds:

```bash
python3 scripts/fetch_odds.py --mode auto --sports baseball_mlb basketball_nba --pretty
```

Generate an automatic ranked report:

```bash
python3 scripts/generate_report.py --mode auto --sports baseball_mlb basketball_nba
```

Generate a deeper report with extra context:

```bash
python3 scripts/generate_report.py --mode auto --sports baseball_mlb --detail deep
```

MLB deep mode currently adds:
- weather context
- article-based key players / injuries / trend context
- extra matchup summary for top picks

Force free mode:

```bash
python3 scripts/generate_report.py --mode free --sports baseball_mlb
```

Get free-source hints directly:

```bash
python3 scripts/fetch_free_context.py --sports baseball_mlb basketball_nba
```

Get free-mode odds-search queries:

```bash
python3 scripts/fetch_free_odds.py --sports baseball_mlb basketball_nba
```

Parse rough public-odds text into event candidates:

```bash
python3 scripts/parse_free_odds.py sample.txt
```

Public-page fetch pipeline:

```bash
python3 scripts/free_pipeline.py --sport baseball_mlb
```

Targeted Covers MLB event extraction:

```bash
python3 scripts/extract_covers_mlb.py page.html
```

Targeted Covers MLB line snapshot extraction:

```bash
python3 scripts/extract_covers_mlb_lines.py page.html
```

Free-mode MLB prototype report:

```bash
python3 scripts/generate_report.py --mode free --sports baseball_mlb
```

Fetch AskNews article context:

```bash
python3 scripts/fetch_asknews.py 'Knicks Hornets betting preview March 26 2026' --n-articles 5
```

Send the report by email:

```bash
bash scripts/send_daily_report.sh
```

Default behavior:
- reads `THE_ODDS_API_KEY` from environment
- queries MLB, NBA, and NHL by default
- compares FanDuel, DraftKings, and BetMGM
- `fetch_odds.py` returns normalized game objects with:
  - best available moneyline by team
  - spread ranges by team
  - total ranges for Over and Under
  - per-book market details
- `generate_report.py` builds:
  - best-price ranking
  - automatic per-game candidate selection
  - automatic top-3 formatted report output

## Useful search habits

- Use freshness filters when available.
- Search by sport + date + `best bets`.
- Search matchup previews separately when a pick looks interesting.
- If injury news may matter, search that team and player status directly before finalizing.
