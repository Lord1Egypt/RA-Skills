# multi-sport-match-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**39 endpoints across 2 platform group(s).**

## Flashscore (24)

### `flashscore_calendar`

- **HTTP:** `GET /flashscore/calendar`
- **What:** Flashscore season calendar. Returns public tournament calendar entries for the current season, sorted by start date, with date ranges, UTC start and end times, host country, winners and winner paths when decided, and competition paths.
- **Params:** `category` (string, **required**) — Calendar category from flashscore-calendar-categories

### `flashscore_calendar_categories`

- **HTTP:** `GET /flashscore/calendar-categories`
- **What:** Flashscore season calendar categories. Lists the Flashscore season calendar sections currently available, covering ATP, WTA, golf, badminton and Formula 1. Each category has its `key`, name, sport and canonical path. Use a `key` with the Flashscore calendar endpoint. It takes no parameters.
- **Params:** _none_

### `flashscore_competitions`

- **HTTP:** `GET /flashscore/competitions`
- **What:** Flashscore competitions by sport and date. Discovers competitions present in a selected sport's score feed, including the provider competition id, label, region, canonical path, and event count. This is the active feed-date inventory, not an archive of inactive or historical seasons.
- **Params:** `day_offset` (integer, optional) — Days from today; -7 to 7; defaults to 0; `sport` (string, **required**) — Sport key

### `flashscore_match_h2h`

- **HTTP:** `GET /flashscore/match-h2h`
- **What:** Flashscore match head-to-head and recent results. Returns Flashscore's public head-to-head and recent-results feed for a match id copied from a Flashscore match URL. The raw upstream feed is preserved as text because its format is not JSON.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_highlights`

- **HTTP:** `GET /flashscore/match-highlights`
- **What:** Flashscore match highlights. Returns public highlight identifiers, metadata, and video links as the provider's raw delimited text. Video content is not fetched or included. Matches without available highlights return not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_info`

- **HTTP:** `GET /flashscore/match-info`
- **What:** Flashscore match venue and broadcast information. Returns the public match information feed, including available venue, city, capacity, and broadcast listings, as the provider's raw delimited text.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_lineups`

- **HTTP:** `GET /flashscore/match-lineups`
- **What:** Flashscore match lineups and formations. Returns each side's confirmed formation, starters and substitutes with positions, in-match ratings and incidents such as cards and substitutions, plus coaches and the substitutions made. Lineups usually appear shortly before kickoff for covered matches; a match with no lineup players on either side returns not found. Use flashscore-match-predicted-lineups for expected lineups before they are confirmed.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_news`

- **HTTP:** `GET /flashscore/match-news`
- **What:** Flashscore match news references. Returns article references from the public news layout associated with a match. Article content is not included; use the article id with flashscore-news-article for public metadata.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_standings`

- **HTTP:** `GET /flashscore/match-standings`
- **What:** Flashscore match league standings. Returns the match-linked table feed. Select overall, home/away, form, over/under, half-time/full-time, live table, or top scorers; the raw provider format is preserved. Defaults to overall.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id; `view` (string, optional) — Standings/table view; defaults to overall

### `flashscore_match_stats`

- **HTTP:** `GET /flashscore/match-stats`
- **What:** Flashscore match statistics. Returns Flashscore's public delimited statistics feed for a match id copied from a Flashscore match URL. The raw upstream feed is preserved as text because its format is not JSON.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_navigation`

- **HTTP:** `GET /flashscore/navigation`
- **What:** Flashscore sport, category, country, and competition navigation. Returns the first-party category hierarchy and competition links for a public Flashscore sport or category page. Start with / or a sport path from flashscore-sports, then follow returned paths to enumerate region, country, category, and competition pages. Country/category lists reflect the current upstream navigation.
- **Params:** `path` (string, optional) — Relative Flashscore navigation path; defaults to /. Use a path returned by flashscore-sports or flashscore-navigation.

### `flashscore_news`

- **HTTP:** `GET /flashscore/news`
- **What:** Flashscore News listings by section. Returns article previews from a public Flashscore News section. Use flashscore-news-categories to discover valid category keys. Page numbers follow the site's Show more pagination; article body text is not included.
- **Params:** `category` (string, optional) — News section key; defaults to all; `page` (integer, optional) — 1-based page, 1 to 100; defaults to 1

### `flashscore_news_article`

- **HTTP:** `GET /flashscore/news-article`
- **What:** Flashscore news article metadata. Returns public article metadata and image credits for an article id from a Flashscore match news listing. Article body text is not included.
- **Params:** `id` (string, **required**) — Eight-character Flashscore article id

### `flashscore_news_categories`

- **HTTP:** `GET /flashscore/news-categories`
- **What:** Flashscore News categories. Returns the exact currently usable public News section keys, names, and source paths from the live navigation inventory. Olympic Games is excluded because its linked page currently returns 404.
- **Params:** _none_

### `flashscore_ranking_categories`

- **HTTP:** `GET /flashscore/ranking-categories`
- **What:** Flashscore ranking categories. Lists the Flashscore ranking categories currently available, including the tennis live-rankings pages. Each category has its `key`, name, sport, page path and a `live` flag. Use a `key` with the Flashscore rankings endpoint. It takes no parameters.
- **Params:** _none_

### `flashscore_rankings`

- **HTTP:** `GET /flashscore/rankings`
- **What:** Flashscore rankings. Returns the first-party ranking feed pages for a supported ranking category. When page one is full, page two is included to cover the remaining rows.
- **Params:** `category` (string, **required**) — Ranking category from flashscore-ranking-categories

### `flashscore_scores`

- **HTTP:** `GET /flashscore/scores`
- **What:** Flashscore scores and fixtures by sport. Returns the public score feed for one sport and date-picker day offset. The upstream field-delimited text is preserved because field semantics vary by sport. Use flashscore-sports to discover sport keys, flashscore-navigation for the current category/country/competition directory, and flashscore-competitions for competitions on the selected date.
- **Params:** `day_offset` (integer, optional) — Days from today; -7 to 7; defaults to 0; `sport` (string, **required**) — Sport key

### `flashscore_search`

- **HTTP:** `GET /flashscore/search`
- **What:** Flashscore search. Searches the same public entity index used by Flashscore's search box. Results can include teams, players, and tournament templates across supported sports.
- **Params:** `q` (string, **required**) — Search phrase (2 to 80 characters)

### `flashscore_sports`

- **HTTP:** `GET /flashscore/sports`
- **What:** Flashscore sports and live category counts. Returns every sport category visible in Flashscore's score navigation, with sport id, caller key, page path, and current event/competition counts. Counts are a live snapshot and may be zero when the sport has no fixtures in the current feed window.
- **Params:** _none_

### `flashscore_top_search`

- **HTTP:** `GET /flashscore/top-search`
- **What:** Flashscore top search entities. Returns the ten-or-fewer public team, player, and tournament results shown in Flashscore's search overlay. This is a changing curated list, not a complete entity directory.
- **Params:** _none_

### `flashscore_tournament_events`

- **HTTP:** `GET /flashscore/tournament-events`
- **What:** Flashscore tournament season results or fixtures. Returns a page of the public results or fixtures feed for any supported sport and competition path. Page 1 is embedded in the public tournament page; later pages follow its Show more feed sequence. Sum event_count from successive pages until total_events is reached.
- **Params:** `page` (integer, optional) — 1-based page; defaults to 1; `path` (string, **required**) — Relative Flashscore competition season results or fixtures path

### `flashscore_tournament_seasons`

- **HTTP:** `GET /flashscore/tournament-seasons`
- **What:** Flashscore tournament archive seasons. Lists the seasons and winners (both players for doubles) from a public competition archive page. Discover archive paths through flashscore-navigation or flashscore-competitions. Each returned results_path and fixtures_path can be passed to flashscore-tournament-events to retrieve season event feeds.
- **Params:** `path` (string, **required**) — Relative Flashscore competition archive path ending in /archive/

### `flashscore_tournament_standings`

- **HTTP:** `GET /flashscore/tournament-standings`
- **What:** Flashscore competition standings table. Returns a competition-level table feed independent of a match id. Discover the stage-specific view values with flashscore-tournament-standings-views. Data remains in Flashscore's raw delimited format.
- **Params:** `path` (string, **required**) — Relative Flashscore competition path from flashscore-navigation or flashscore-competitions; omit /standings/; `view` (string, optional) — View returned by flashscore-tournament-standings-views; defaults to overall

### `flashscore_tournament_standings_views`

- **HTTP:** `GET /flashscore/tournament-standings-views`
- **What:** Flashscore competition standings view discovery. Returns the table views currently exposed on a public Flashscore competition standings page. The view set varies by competition and stage; use a returned value with flashscore-tournament-standings.
- **Params:** `path` (string, **required**) — Relative Flashscore competition path from flashscore-navigation or flashscore-competitions; omit /standings/

## LiveScore (15)

### `livescore_competition`

- **HTTP:** `GET /livescore/competition`
- **What:** LiveScore competition page and section data. Returns public competition or stage page data and its visible sections. Competition ids and tabs vary by sport; discover English sitemap-listed paths, including cricket stage pages, with /livescore/competitions.
- **Params:** `path` (string, **required**) — Three to five lowercase path segments following /en/, such as football/england/premier-league or football/england/premier-league/standings

### `livescore_competitions`

- **HTTP:** `GET /livescore/competitions`
- **What:** LiveScore competition page directory. Returns English competition pages listed in LiveScore's public competition sitemaps plus competition-shaped pages listed in the English cricket sport sitemap. The sitemap index has dedicated competition sitemaps for soccer, hockey, basketball, and tennis; cricket discovery remains partial and dynamic.
- **Params:** _none_

### `livescore_live_scores`

- **HTTP:** `GET /livescore/live-scores`
- **What:** LiveScore live scores by sport. Returns current live sections for a supported sport. Empty Sctns is a valid result when there are no live events. Use Nav and the final section Id for cursor paging.
- **Params:** `cursor` (string, optional) — Section Id from the prior paged response, e.g. s-26031; `direction` (string, optional) — Page direction in paged mode; `paging` (boolean, optional) — Request a paged live feed; defaults to false; `sport` (string, **required**) — LiveScore sport id; `timezone_offset` (integer, optional) — UTC offset in hours from -12 through 14; defaults to 0

### `livescore_match`

- **HTTP:** `GET /livescore/match`
- **What:** LiveScore match details. Returns the event data embedded in a public LiveScore match page. Data uses LiveScore's event payload shape; available fields vary by event and stage.
- **Params:** `path` (string, **required**) — Five path segments following /en/ in a LiveScore match URL

### `livescore_match_stats`

- **HTTP:** `GET /livescore/match-stats`
- **What:** LiveScore match statistics. Returns the statistics section for a LiveScore match when the source exposes it.
- **Params:** `path` (string, **required**) — Five-segment path after /en/ from a LiveScore match URL

### `livescore_news`

- **HTTP:** `GET /livescore/news`
- **What:** LiveScore news by category or topic. Returns the article cards for one LiveScore news route. `category` is required: `all` for the home feed, or a lowercase route path of up to six segments, such as `football/premier-league`, found via `livescore-news-categories`. The response carries `source_url` and the page `data`. Some articles link to third-party publishers, article bodies are not returned, and unknown paths return not found or an upstream error.
- **Params:** `category` (string, **required**) — all or a lowercase path from /livescore/news-categories; up to six segments

### `livescore_news_article`

- **HTTP:** `GET /livescore/news-article`
- **What:** LiveScore news article. Returns the public full article record, including the article's structured content when supplied by LiveScore. Copy the path following /en/news/ from an article slug in /livescore/news.
- **Params:** `path` (string, **required**) — Two to eight lowercase path segments after /en/news/, copied from an article slug

### `livescore_news_categories`

- **HTTP:** `GET /livescore/news-categories`
- **What:** LiveScore news categories. Returns all current public news routes from LiveScore's own category sitemap files, including sports, competitions, tips, daily team feeds, and teams. The values update with the source sitemap.
- **Params:** _none_

### `livescore_news_feed`

- **HTTP:** `GET /livescore/news-feed`
- **What:** LiveScore global RSS news feed. Returns latest public news items from LiveScore's global RSS feed. The source feed may include multiple sports and has no verified category filter. Set include_content=true to include each RSS item's full content:encoded body.
- **Params:** `include_content` (boolean, optional) — Include full RSS article content when available

### `livescore_player`

- **HTTP:** `GET /livescore/player`
- **What:** LiveScore player profile. Returns the public overview profile data for a player linked from a team squad, including player identity, current team/competition, career teams, recent-match context, and player league summary when supplied.
- **Params:** `path` (string, **required**) — season-stats/player-slug/numeric-player-id path copied from a public LiveScore player link

### `livescore_scores`

- **HTTP:** `GET /livescore/scores`
- **What:** LiveScore scores and fixtures by sport and date. Returns either the unpaged full-day scoreboard or one cursor-paged UI-style section page for a supported sport and date. The response's Nav values indicate whether another page is available; use the last returned section Id as cursor. Sport ids are discoverable from /livescore/sports.
- **Params:** `cursor` (string, optional) — Section Id from the prior paged response, e.g. s-26031; `date` (string, **required**) — Calendar date in YYYYMMDD format; `direction` (string, optional) — Page direction in paged mode; `paging` (boolean, optional) — Request one UI-style page; defaults to false (full-day feed); `sport` (string, **required**) — LiveScore sport id; `timezone_offset` (integer, optional) — UTC offset in hours from -12 through 14; defaults to 0

### `livescore_scores_toc`

- **HTTP:** `GET /livescore/scores-toc`
- **What:** LiveScore score date table of contents. Returns the event, player, section, and competition identifiers indexed by a sport and date. These IDs are date-specific and can help callers enumerate score-page sections.
- **Params:** `date` (string, **required**) — Calendar date in YYYYMMDD format; `sport` (string, **required**) — LiveScore sport id; `timezone_offset` (integer, optional) — UTC offset in hours from -12 through 14; defaults to 0

### `livescore_search`

- **HTTP:** `GET /livescore/search`
- **What:** Search LiveScore teams, competitions, and regions. Searches the public LiveScore index for a free-text term, or browse its current team, competition-stage, and region-category sections with an empty query. Results are dynamic, limited per section, and are not a complete historical competition directory. Use /livescore/sports to discover all supported sport tokens.
- **Params:** `limit` (integer, optional) — Optional results per section (1 to 100). Defaults to 10 for a text query or 50 when query is empty.; `query` (string, optional) — Optional free-text team, competition, or region term (up to 100 characters). Omit or leave empty to browse current results.; `sport` (string, **required**) — LiveScore sport token

### `livescore_sports`

- **HTTP:** `GET /livescore/sports`
- **What:** LiveScore supported sports. Lists the five sports in LiveScore's fixture navigation, with no inputs. The ids are `soccer` (shown as Football on the site), `hockey`, `basketball`, `tennis` and `cricket`. Use an id as the sport input of the LiveScore scores endpoint.
- **Params:** _none_

### `livescore_team`

- **HTTP:** `GET /livescore/team`
- **What:** LiveScore team page and section data. Returns a public team page section such as overview, fixtures, results, standings, squad, player stats, or team stats. Tab paths and competition-specific identifiers are supplied by the source page; copy a team tab href from LiveScore.
- **Params:** `path` (string, **required**) — Five to nine lowercase path segments following /en/ from a public LiveScore team page or linked tab
