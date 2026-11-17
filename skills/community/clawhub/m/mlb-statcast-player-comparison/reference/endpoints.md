# mlb-statcast-player-comparison — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**12 endpoints across 1 platform group(s).**

## MLB (12)

### `mlb_discovery`

- **HTTP:** `GET /mlb/discovery`
- **What:** Discover MLB sections and Stats API values. Returns MLB.com's live navigation tree, including hidden nodes labeled with visibility, and the MLB-only value sets for leagues, divisions, game types, roster types, standings types, stat groups, supported stat types, leader categories, MLB Pipeline prospect filters, league-stats hitter positions and player pools, and observed Baseball Savant leaderboard categories and filters including Top Performers, ABS Challenges, Expected Statistics, Outs Above Average, Arm Strength, Arm Value, Home Runs, Percentile Rankings, Pitch Movement, Rolling Windows, Pitcher Arm Angle, Year-to-Year Changes, Catcher Blocking, Catcher Framing, Catcher Throwing, First Base Receiving, and Fielding Run Value. Use these values to discover sections and supported filters before calling MLB endpoints.
- **Params:** _none_

### `mlb_player`

- **HTTP:** `GET /mlb/player`
- **What:** Get an MLB player. Returns an MLB player by numeric `id`. The response has the full name, position, bats and throws sides, birth date, city and country, current age, height, weight, jersey number, MLB debut date, active flag and current team. Unknown players return `404`.
- **Params:** `id` (string, **required**) — Numeric MLB player id

### `mlb_player_stats`

- **HTTP:** `GET /mlb/player-stats`
- **What:** Get MLB player season statistics. Returns one MLB player's statistics. `id` and `group` (`hitting`, `pitching`, `fielding`, `catching`, `running`, `game`, `team` or `streak`) are required. `season` defaults to the current year and `stat_type` to `season`. Other `stat_type` values cover career, game logs and splits. Use `start_date` with `end_date` for date ranges.
- **Params:** `end_date` (string, optional) — End date for byDateRange stat types; requires start_date; `game_type` (string, optional) — MLB game type; `group` (string, **required**) — Stat group; `id` (string, **required**) — Numeric MLB player id; `opponent_player_id` (string, optional) — Required by vsPlayer stat types; `opponent_team_id` (string, optional) — Required by vsTeam stat types; `season` (integer, optional) — Four-digit season; defaults to current year; `start_date` (string, optional) — Start date for byDateRange stat types; requires end_date; `stat_type` (string, optional) — Stats API stat type; defaults to season

### `mlb_search`

- **HTTP:** `GET /mlb/search`
- **What:** Search MLB players, teams, and content topics. Returns the same anonymous MLB typeahead categories used by MLB.com: player suggestions, team suggestions, content topics, and search terms. Queries need at least three characters.
- **Params:** `q` (string, **required**) — Search text; 3-100 characters

### `mlb_statcast_batted_ball`

- **HTTP:** `GET /mlb/statcast-batted-ball`
- **What:** Get Baseball Savant Batted Ball Profile rows. Returns the Batted Ball Profile table for batters, batting teams, pitchers, pitching teams, or league totals. Supports first-party season, game type, split, team, date, side, hand, pitch type, event threshold, and split-group threshold filters. The All-Star A game type is accepted by the live page query although its checkbox is hidden. Sorting and pagination are local. The league-average reference row is returned separately when requested; CSV and visualization controls are outside this JSON contract.
- **Params:** `bat_side` (string, optional) — Batter side; `date_end` (string, optional) — YYYY-MM-DD date range end (2015-04-05 through today); `date_start` (string, optional) — YYYY-MM-DD date range start (2015-04-05 through today); `game_types` (array, optional) — One or more game type codes; `include_league_average` (boolean, optional) — Include the first-party league-average reference row; `limit` (integer, optional) — Rows per page (1-500); `min` (string, optional) — Minimum batted-ball events; `min_split` (string, optional) — Minimum rows per split group; `offset` (integer, optional) — Zero-based row offset; `pitch_hand` (string, optional) — Pitcher throwing hand; `pitch_types` (array, optional) — One or more pitch type codes; `seasons` (array, optional) — One or more seasons; `sort` (string, optional) — Local table sort field; `sort_dir` (string, optional) — Sort direction; `split_year` (string, optional) — Split seasons into separate rows; `splits` (array, optional) — One or more split dimensions; `teams` (array, optional) — One or more MLB team ids; `type` (string, optional) — Row type

### `mlb_statcast_expected`

- **HTTP:** `GET /mlb/statcast-expected`
- **What:** Get Baseball Savant Expected Statistics. Returns the separate Expected Statistics leaderboard with batter, pitcher, and team views; season, team, batter-position, BIP/PA qualifier and threshold filters; local metric sorting; and pagination. League-average values are returned separately.
- **Params:** `filter_type` (string, optional) — Minimum qualifier type; `limit` (integer, optional) — Rows per page (1-500); `minimum` (string, optional) — Minimum BIP/PA threshold; `offset` (integer, optional) — Zero-based row offset; `position` (string, optional) — Batter position; only supported for type=batter; `sort` (string, optional) — Sort field; `sort_dir` (string, optional) — Sort direction; `team_id` (string, optional) — Optional MLB team id from mlb_teams; `type` (string, optional) — Leaderboard view; `year` (integer, optional) — Season from 2015 through the current season

### `mlb_statcast_percentile`

- **HTTP:** `GET /mlb/statcast-percentile`
- **What:** Get Baseball Savant Percentile Rankings. Returns batter or pitcher percentile rankings. Type, season, and team are first-party table filters. Repeated pctl filters, table sorting, and pagination are applied locally to the embedded rows. Use mlb_discovery for exact type-specific fields, comparators, seasons, and team ids. CSV is a separate download.
- **Params:** `limit` (integer, optional) — Rows per page (1-500); `offset` (integer, optional) — Zero-based row offset; `pctl` (array, optional) — Repeated field-comparator-value filter from the type-specific field set in mlb_discovery; value range 0-100; `sort` (string, optional) — Local sort field from the type-specific set in mlb_discovery; `sort_dir` (string, optional) — Local sort direction; `team` (string, optional) — MLB team id; blank selects all teams; `type` (string, optional) — Table type; `year` (string, optional) — Season

### `mlb_statcast_pitch_arsenal`

- **HTTP:** `GET /mlb/statcast-pitch-arsenal`
- **What:** Get Baseball Savant Pitch Arsenal Stats. Returns pitcher or batter pitch-level arsenal leaderboards. Season, team, pitch type, minimum PA, and minimum-pitch qualification filters are replayed against the anonymous first-party table; sorting and pagination are applied locally. Use mlb_discovery for the full selector set. Player rows can be expanded with mlb-statcast-pitch-arsenal-details.
- **Params:** `limit` (integer, optional) — Rows per page (1-500); `min_pa` (string, optional) — Minimum plate appearances; `min_pitches` (string, optional) — Minimum pitches; q means qualified; `offset` (integer, optional) — Zero-based row offset; `pitch_type` (string, optional) — Pitch code; blank means all pitch types; `sort` (string, optional) — Local sort field; `sort_dir` (string, optional) — Local sort direction; `team_id` (string, optional) — MLB team id from mlb_teams; `type` (string, optional) — Row type; `year` (string, optional) — Season

### `mlb_statcast_pitch_movement`

- **HTTP:** `GET /mlb/statcast-pitch-movement`
- **What:** Get Baseball Savant Pitch Movement rows. Returns pitcher-level pitch movement table rows for the selected season, pitch type, throwing hand, and minimum pitch count. Sorting and pagination are applied locally. The page's X/Z visualization axes and CSV download are separate presentation formats and are not returned by this JSON table contract.
- **Params:** `hand` (string, optional) — Pitcher throwing hand; omit for both; `limit` (integer, optional) — Rows per page (1-500); `min` (string, optional) — Minimum pitch count; `offset` (integer, optional) — Zero-based row offset; `pitch_type` (string, optional) — Pitch class; `sort` (string, optional) — Local table sort field; `sort_dir` (string, optional) — Sort direction; `year` (string, optional) — Season

### `mlb_statcast_rolling`

- **HTTP:** `GET /mlb/statcast-rolling`
- **What:** Get Baseball Savant Rolling Windows rows. Returns the six embedded Batter/Pitcher rolling-window tables, filtered by metric, role, and plate-appearance window. Each group is sorted by the selected metric delta in the same direction as the first-party page and paginated independently. The upstream page has no season, team, or game-type filters.
- **Params:** `limit` (integer, optional) — Rows per group (1-500); `metric` (string, optional) — Displayed metric; `offset` (integer, optional) — Zero-based row offset per group (0-5000); `role` (string, optional) — Optional player role; omit for both; `window_pa` (string, optional) — Optional rolling plate-appearance window; omit for all

### `mlb_statcast_year_to_year`

- **HTTP:** `GET /mlb/statcast-year-to-year`
- **What:** Get Baseball Savant Year-to-Year Changes. Returns one of Baseball Savant's Year-to-Year Changes tables for batters, pitchers, batting teams, or pitching teams. Select one of the live statistic types and comparison start years; the page data contains available yearly values and differences. Table sorting and pagination are applied locally. Use mlb_discovery for all accepted group, type, and year values.
- **Params:** `group` (string, optional) — Table group; `limit` (integer, optional) — Rows per page (1-500); `offset` (integer, optional) — Zero-based row offset (0-5000); `sort` (string, optional) — Local sortable column; name_display_last_first, year_YYYY, TYPE_YYYY, or TYPE_diff_YYYY. Defaults to the selected metric's difference for the selected comparison year.; `sort_dir` (string, optional) — Sort direction; defaults to Batter descending and Pitcher ascending; `type` (string, optional) — Statistic type; `year` (string, optional) — Comparison start year; compares this season with the following year

### `mlb_teams`

- **HTTP:** `GET /mlb/teams`
- **What:** List MLB teams. Lists the 30 MLB clubs for a `season` (four-digit year, default the current year). Each team has its id, name, club name, location, abbreviation, league, division, venue, first year of play and active flag.
- **Params:** `season` (integer, optional) — Four-digit season; defaults to current year
