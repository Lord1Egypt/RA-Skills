---
name: multi-sport-match-research
description: Compare public fixtures, live scores, match statistics, standings, and head-to-head records using Crawlora Flashscore and LiveScore tools. Use for multi-sport score checks, a sourced match preview or recap, or reconciling different scoreboard providers.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Multi-sport match research

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

## Access and contract

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the named Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact tool names, methods,
and parameters. Check application `code` as well as HTTP status; payloads are
inside `data`. Stop on authentication errors, back off on `429`, and retry a
transient upstream failure once. Bound pages and calls by the requested scope
and credit budget. Preserve source URLs, identifiers, and collection times.

Use Flashscore and LiveScore for fixtures, score snapshots, previews, and
recaps. Choose the provider whose documented sport and match surfaces fit the
request; both are optional sources, not a required double fetch.

For a detailed post-match football performance report from SofaScore statistics,
incidents, and lineups, use football-match-performance-analysis when installed.
This skill remains focused on Flashscore/LiveScore identity, coverage, and
provider reconciliation.

## Resolve the event and collect bounded evidence

1. Discover accepted sports, competitions, seasons, stages, or calendar categories
   through each provider's discovery routes. Flashscore sport keys and LiveScore
   sport IDs differ; never carry one provider's code or entity ID into the other.
2. Find candidates using Flashscore search/competitions or LiveScore schedules/live
   scores. Match competition, participants, scheduled date, and timezone before
   treating two records as the same event. Include women's/youth/reserve labels.
3. Flashscore match routes use its eight-character match ID. LiveScore match detail
   uses the five path segments following `/en/` in a returned match URL; it is not
   a numeric Flashscore ID or the full URL. Follow the reference for each route's
   own ID and path fields.
4. Request only the relevant score, match info, statistics, lineups, incidents,
   standings, head-to-head, or news surfaces. Flashscore calendar categories are
   a narrower set than its sports. LiveScore `timezone_offset` is a numeric UTC
   offset; compute it for the requested date rather than passing an IANA name.
5. Preserve upstream match status and observation time. Use returned cursors for
   paged LiveScore feeds; do not assume a single live page contains every match.

```sh
scripts/crawlora.sh /flashscore/search q="Arsenal"
scripts/crawlora.sh /flashscore/calendar-categories
scripts/crawlora.sh /livescore/sports
scripts/crawlora.sh /livescore/live-scores sport=soccer timezone_offset=0
# Select an actual result before:
# scripts/crawlora.sh /flashscore/match-info id="$FLASHSCORE_ID"
# scripts/crawlora.sh /livescore/match path="$LIVESCORE_MATCH_PATH"
```

## Report comparable observations

Keep period scores, aggregate ties, extra time, and shootouts distinct. Attribute
provider discrepancies and retain both timestamps rather than choosing a winner
from two asynchronous snapshots. Recent form and head-to-head are descriptive
samples, not forecasts. Do not interpret an empty or failed response as a 0-0
score, no scheduled match, or confirmed cancellation. Return the matched event,
status/time, sourced score or preview evidence, unresolved conflicts, and limits.
Any repeated polling or notification setup must follow the user's requested
interval and budget; a score check alone does not request a monitor.
