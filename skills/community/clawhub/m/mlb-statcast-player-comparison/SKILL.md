---
name: mlb-statcast-player-comparison
description: Compare MLB players using Crawlora Statcast leaderboards and player statistics with board-specific discovery, season, role, qualification, metric units, and sample controls. Use for an observed performance brief, pitch-arsenal comparison, or role-specific player shortlist.
---

# MLB Statcast player comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Build a role-specific performance comparison for selected players or a declared
cohort. Establish season/date window, batter versus pitcher/fielding role,
competition scope, qualification, and metrics before retrieving leaderboards.

## Discover boards, identities, and qualification

- Use `mlb_discovery` for board-specific selectors/fields and MLB search/team/player
  routes for identity. Keep numeric player/team IDs distinct from a leaderboard's
  local row/entity keys. A matching display name does not resolve the player.
- Each board has its own season coverage, role values, team parameter, thresholds,
  split/grouping, and sorting fields. Do not copy `team_id` into a board expecting
  `team`, or reuse batter fields in a pitcher table. Request only the relevant
  expected/percentile/arsenal/batted-ball/movement/rolling views.
- Qualification depends on the board: plate appearances, balls in play, pitches,
  or other events differ. `minimum=q` means the source's qualification rule, not
  the same sample size for all boards. Preserve the selected thresholds, event
  count/denominator, role, year, and returned league-average context.
- Some boards return league-wide tables with local sorting/pagination rather
  than an arbitrary `player_id` filter. Match selected players in actual returned
  rows; do not invent unsupported input fields or assume a top-N page includes
  every eligible player. Keep `total`, offset, limit, and missing-player reasons.

```sh
scripts/crawlora.sh /mlb/discovery
scripts/crawlora.sh /mlb/statcast-expected type=batter year=2025 filter_type=bip minimum=q limit=10
scripts/crawlora.sh /mlb/statcast-percentile type=batter year=2025 limit=10
# Resolve player identity before joining rows from different boards.
```

## Compare metrics on their actual bases

Preserve raw metric labels, units, direction, and calculation scope. Expected
statistics are provider models, not realised outcomes or promised future results.
A percentile is a relative ranking in its source cohort, not a success probability;
its year/type denominator can differ from another board. Do not average percentiles
or convert them into a universal talent score without an explicit justified rubric.

Pitch usage, whiff rates, run values, velocity/spin/movement, and batted-ball
metrics have different units and favorable directions. Compare equivalent pitch
families, role, event windows, and board definitions; do not merge a pitch-specific
row into a whole-player mean without its actual weights. Rolling windows are
plate-appearance samples rather than equal calendar time; do not claim a calendar
trend from a mislabeled window. Year-to-year views need matched definitions and
coverage, with rule/measurement changes retained as limits.

Return identity/scope and metric tables, board/qualification evidence, event
counts, league context, supplied-versus-calculated values, and unknowns. Disclose
weights for a requested ranking and keep small samples visible. These observations
do not establish injury, future performance, transfer value, or a complete scouting
assessment; no betting or account action is part of a comparison request.
