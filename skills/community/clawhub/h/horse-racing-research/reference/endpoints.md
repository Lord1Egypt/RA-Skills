# horse-racing-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**16 endpoints across 2 platform group(s).**

## DraftKings Racing (3)

### `draftkings_racing_race_info`

- **HTTP:** `GET /draftkings/racing/race/{race_id}`
- **What:** DraftKings Racing race card and results. Returns public race-card details for one race ID from DraftKings Racing, including entries, horse identifiers, morning-line and live odds, and finish positions when posted. It excludes pools, probable payouts, bet-form IDs, real-time WebSocket requests, favorites, and participant personal names.
- **Params:** `race_id` (integer, **required**) — Race ID from the public Racing schedule

### `draftkings_racing_schedule`

- **HTTP:** `GET /draftkings/racing/schedule`
- **What:** DraftKings Racing schedule. Returns public race-card metadata from the DraftKings Racing homepage, including track, race number, scheduled post time, and status. Favorite-track and wager data are excluded.
- **Params:** _none_

### `draftkings_racing_tracks`

- **HTTP:** `GET /draftkings/racing/tracks`
- **What:** DraftKings Racing tracks. Returns the public All Tracks directory with track type, status, schedule count, and country metadata. Favorite IDs, runner details, and wagering controls are excluded.
- **Params:** _none_

## FanDuel (13)

### `fanduel_racing_carryover_pools`

- **HTTP:** `GET /fanduel/racing/carryover-pools`
- **What:** FanDuel Racing carry-over pools. Lists the multi-race pools that carried over (Pick 3 to Pick 6, Super High Five, Superfecta, Daily Double) with the amount, the track, the race the pool pays on and that race's minutes to post and status. Largest pool first. `status` filters by the status of the race the pool pays on.
- **Params:** `limit` (integer, optional) — Items per page, 1 to 200; default 50; `page` (integer, optional) — Page number, from 1; default 1, at most 10000; `status` (string, optional) — Keep only pools whose race has these statuses (repeat the parameter or comma-separate): `O` Open, `IC` Up Next, `SK` Race Off, `RO` Race Official; `track` (string, optional) — Keep only these track codes (repeat the parameter or comma-separate), such as `LRL`; list codes with the `tracks` route

### `fanduel_racing_filters`

- **HTTP:** `GET /fanduel/racing/filters`
- **What:** FanDuel Racing filter values. Counts today's races by country, race type, status, surface and class, and lists the sort names, so every value the other racing routes accept is discoverable. Statuses, race types, surfaces, classes and countries are data-driven sets, so the counts are today's live inventory; a country appears here only while it is racing.
- **Params:** _none_

### `fanduel_racing_horse`

- **HTTP:** `GET /fanduel/racing/horse`
- **What:** FanDuel Racing horse career. Returns a horse's career record (starts, wins, top-three finishes, win percentage) and its past races newest first, each with the race conditions and the horse's own result line: finish position, post-race report, beaten lengths and starting price when the track reports them. Needs the horse's `id` from the `search` route; an unknown id returns 404.
- **Params:** `id` (string, **required**) — Horse id (`id` of a `runner` result of the `search` route), such as `1002257`; `limit` (integer, optional) — Races per page, 1 to 200; default 50; `page` (integer, optional) — Page of races, from 1; default 1, at most 10000

### `fanduel_racing_past_race`

- **HTTP:** `GET /fanduel/racing/past-race`
- **What:** FanDuel Racing past race result. Returns one past race in full: conditions, the finish order with win, place and show payoffs, beaten lengths, starting price and the post-race report of each runner, the payoff of every wager type, and every entry with its morning-line and final odds and its horse, jockey, trainer, owner and pedigree. Needs a date, a track code and a race number from the `past-races` route; a race that did not run returns 404. A race whose results the service no longer holds returns no `results`.
- **Params:** `date` (string, **required**) — Day as `YYYY-MM-DD`, from `2008-01-01`; `number` (string, **required**) — Race number, 1 to 99; `track` (string, **required**) — Track code such as `BEL`

### `fanduel_racing_past_races`

- **HTTP:** `GET /fanduel/racing/past-races`
- **What:** FanDuel Racing past races of a day. Lists the races that ran on a date, at one track or at every track (558 races on 2026-10-02), with number, post time, conditions, distance, purse, surface and runner count; it has no results, so read a race with the `past-race` route. Results go back to 2008. A date with no races returns an empty list; today's date is empty until a race is official.
- **Params:** `date` (string, **required**) — Day as `YYYY-MM-DD`, from `2008-01-01`; `limit` (integer, optional) — Races per page, 1 to 200; default 50; `page` (integer, optional) — Page number, from 1; default 1, at most 10000; `track` (string, optional) — Track code such as `BEL`; omit for every track

### `fanduel_racing_past_tracks`

- **HTTP:** `GET /fanduel/racing/past-tracks`
- **What:** FanDuel Racing tracks with past results. Lists the tracks that have past results. With `date` it returns the tracks that ran that day with their race count and race types; with `track` it returns that track and the dates it ran (newest first, paged by `page` and `limit`, back to 2008); with neither it returns every track (786 on 2026-10-24). An unknown track returns 404.
- **Params:** `date` (string, optional) — Day as `YYYY-MM-DD`, from `2008-01-01`; `limit` (integer, optional) — Items per page, 1 to 200; default 50; `page` (integer, optional) — Page number, from 1; default 1, at most 10000; `track` (string, optional) — Track code such as `BEL`; adds the dates the track ran

### `fanduel_racing_race`

- **HTTP:** `GET /fanduel/racing/race`
- **What:** FanDuel Racing race detail. Returns one race in full: its conditions, every entry with morning-line and current odds (fractional and decimal), recent price history, runners (jockey, trainer, owner, pedigree, weight, age, scratch and jockey-change flags, win probability), pool totals, probable payouts, will-pays for multi-race bets, the wagers it accepts with their limits, and, once it is official, the finish order and payoffs. Pools, probables and will-pays appear only when the track reports them (mostly official and Up Next races). Pass `include` to add optional groups: `handicapping` (speed, class, pace, jockey-trainer record, power rating, career record and the favorite rank of every runner), `timeform` (Timeform analyst and production comments, tissue price, flags and, once official, how each finisher was beaten, its starting price and a post-race report) and `pool_grids` (the money bet on each entry's pairings in every pool, mostly once the race is official). A race that is not on today's card returns 404.
- **Params:** `include` (string, optional) — Optional groups to add (repeat the parameter or comma-separate): `handicapping` per-runner handicapping figures and favorite rank, `timeform` Timeform comments, tissue price, flags and finisher timing, `pool_grids` per-entry pool pairings. Other values return `400`; `number` (string, **required**) — Race number, 1 to 99, such as `2`; `track` (string, **required**) — Track code from the `tracks` route, such as `LRL`

### `fanduel_racing_races`

- **HTTP:** `GET /fanduel/racing/races`
- **What:** FanDuel Racing races. Lists today's races (about 500 across all tracks) with track, number, post time, minutes to post, status, race type, surface, class, distance, purse and runner count. Filter by track, country, race type, status, open or closed, or the next N minutes; sort by minutes to post, post time or race number. `total` counts every match so `page` and `limit` page through them.
- **Params:** `country` (string, optional) — Keep only races or tracks in these countries (repeat the parameter or comma-separate): upper-case three-letter codes such as `USA`, `GBR`, `AUS`. Today's codes are listed in the `filters` route's `countries`; lower-case or two-letter values return `400`; `exclude_country` (string, optional) — Drop these countries (repeat the parameter or comma-separate), same codes as `country`; `limit` (integer, optional) — Items per page, 1 to 200; default 50; `open` (boolean, optional) — `true` for races still open for betting (`O` and `IC`), `false` for off or official races; omit for both; `order` (string, optional) — `asc` or `desc`; default `asc`. Only valid together with `sort`; `page` (integer, optional) — Page number, from 1; default 1, at most 10000; `race_type` (string, optional) — Keep only these race types (repeat the parameter or comma-separate): `T` Thoroughbred, `H` Harness, `Q` QuarterHorse, `L` Thoroughbred LARC; `sort` (string, optional) — Sort: `mtp` (minutes to post), `post_time`, `race_number`; default is the service's own order; `status` (string, optional) — Keep only these race statuses (repeat the parameter or comma-separate): `O` Open, `IC` Up Next, `SK` Race Off, `RO` Race Official; `track` (string, optional) — Keep only these track codes (repeat the parameter or comma-separate), such as `LRL`; list codes with the `tracks` route; `within_minutes` (integer, optional) — Keep races that post within this many minutes, 1 to 1440

### `fanduel_racing_results`

- **HTTP:** `GET /fanduel/racing/results`
- **What:** FanDuel Racing results. Returns today's official races with their results: winning time, finish order with win, place and show payoffs, and the payoff of every wager type. A race the service reports as refunded has no finishers and one payoff whose selection is `Refund`. Filter by track, country and race type.
- **Params:** `country` (string, optional) — Keep only races or tracks in these countries (repeat the parameter or comma-separate): upper-case three-letter codes such as `USA`, `GBR`, `AUS`. Today's codes are listed in the `filters` route's `countries`; lower-case or two-letter values return `400`; `exclude_country` (string, optional) — Drop these countries (repeat the parameter or comma-separate), same codes as `country`; `limit` (integer, optional) — Items per page, 1 to 200; default 50; `page` (integer, optional) — Page number, from 1; default 1, at most 10000; `race_type` (string, optional) — Keep only these race types (repeat the parameter or comma-separate): `T` Thoroughbred, `H` Harness, `Q` QuarterHorse, `L` Thoroughbred LARC; `track` (string, optional) — Keep only these track codes (repeat the parameter or comma-separate), such as `LRL`; list codes with the `tracks` route

### `fanduel_racing_search`

- **HTTP:** `GET /fanduel/racing/search`
- **What:** FanDuel Racing search by name. Finds horses, jockeys, trainers and owners whose name contains the text (3 to 64 characters), with a horse's `id` and birth year and the date, race and track of each one's last start. Use a horse's `id` with the `horse` route. The service returns every match (several hundred owners for a common surname), so the list is paged here: horses first, then jockeys, trainers and owners, each group sorted by `sort` and `order`. Jockeys, trainers and owners have no id.
- **Params:** `limit` (integer, optional) — Items per page, 1 to 200; default 50; `order` (string, optional) — `asc` or `desc`; default `asc`; `page` (integer, optional) — Page number, from 1; default 1, at most 10000; `q` (string, **required**) — Name text, 3 to 64 characters; matching is case-insensitive; `sort` (string, optional) — Sort within each kind; default `name`; `type` (string, optional) — Keep one kind (any other value silently finds nothing upstream, so it returns `400`)

### `fanduel_racing_track`

- **HTTP:** `GET /fanduel/racing/track`
- **What:** FanDuel Racing track and its races. Returns one track on today's card with every race it runs: number, post time, minutes to post, status, race type, surface, class, distance, purse and runner count. A code that is not racing today returns 404.
- **Params:** `code` (string, **required**) — Track code from the `tracks` route (`tracks[].code`), such as `LRL`

### `fanduel_racing_tracks`

- **HTTP:** `GET /fanduel/racing/tracks`
- **What:** FanDuel Racing tracks today. Returns the tracks racing today (Australia, Canada, France, Great Britain, Ireland, Sweden, the U.S. and more) with country, state, race count, race types, whether the card is finished, and the race each track is on (number, minutes to post, post time, status). Filter by country, race type, track code, finished and featured; sort by name, minutes to post, minutes to post of the next wagerable race, or IVR code.
- **Params:** `code` (string, optional) — Keep only these track codes (repeat the parameter or comma-separate), such as `LRL`; `country` (string, optional) — Keep only races or tracks in these countries (repeat the parameter or comma-separate): upper-case three-letter codes such as `USA`, `GBR`, `AUS`. Today's codes are listed in the `filters` route's `countries`; lower-case or two-letter values return `400`; `exclude_country` (string, optional) — Drop these countries (repeat the parameter or comma-separate), same codes as `country`; `featured` (boolean, optional) — `true` for the Sportsbook's featured tracks only, `false` for the others; omit for both; `finished` (boolean, optional) — `true` for tracks whose card is over, `false` for tracks still racing; omit for both; `limit` (integer, optional) — Items per page, 1 to 200; default 50; `order` (string, optional) — `asc` or `desc`; default `asc`. Only valid together with `sort`; `page` (integer, optional) — Page number, from 1; default 1, at most 10000; `race_type` (string, optional) — Keep only these race types (repeat the parameter or comma-separate): `T` Thoroughbred, `H` Harness, `Q` QuarterHorse, `L` Thoroughbred LARC; `sort` (string, optional) — Sort: `name`, `mtp` (minutes to post of the current race), `wagerable_mtp`, `ivr`; default is the service's own order

### `fanduel_racing_wager_types`

- **HTTP:** `GET /fanduel/racing/wager-types`
- **What:** FanDuel Racing wager types. Lists every wager type the racing service offers (71 on 2026-10-24: Win, Place, Show, Exacta, Trifecta, Superfecta, Daily Double, the Pick bets, Quinella and the international Tote bets) with its code, name, description, group, and structure: legs, columns, positions, and whether it is a box, key or wheel.
- **Params:** _none_
