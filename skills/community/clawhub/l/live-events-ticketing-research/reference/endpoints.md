# live-events-ticketing-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**22 endpoints across 2 platform group(s).**

## SeatGeek (11)

### `seatgeek_categories`

- **HTTP:** `GET /seatgeek/categories`
- **What:** List SeatGeek's event categories. Returns SeatGeek's full event-category tree (e.g. Sports > Baseball > MLB, Concerts, Theater), root and leaf nodes together. Each category's id is the value seatgeek-events-by-category's taxonomy_id parameter accepts.
- **Params:** _none_

### `seatgeek_cities`

- **HTTP:** `GET /seatgeek/cities`
- **What:** List SeatGeek's curated metro areas. Returns SeatGeek's own curated "browse by city" directory (87 metro areas as of 2026-09-15): id, name, state, country, coordinates, and which verticals (concerts/sports/theater) it supports. Each city's lat/lon pairs directly with GET /seatgeek/events-near.
- **Params:** _none_

### `seatgeek_event`

- **HTTP:** `GET /seatgeek/event`
- **What:** Get a SeatGeek event's detail. Returns one SeatGeek event's full detail: title, timing, venue, performers, category taxonomy, and SeatGeek's own live secondary-market pricing snapshot (listing/ticket counts, average/median/lowest/highest price). id is SeatGeek's own numeric event id, obtained from a search or performer-events result. Pricing is an aggregate snapshot only -- no per-seat listing rows and no checkout/purchase flow.
- **Params:** `id` (integer, **required**) — SeatGeek's own numeric event id

### `seatgeek_events_by_category`

- **HTTP:** `GET /seatgeek/events-by-category`
- **What:** Browse SeatGeek events by category. Returns one page of SeatGeek events under a category/taxonomy, soonest first. taxonomy_id is a SeatGeek category id from GET /seatgeek/categories, e.g. 1010100 for MLB.
- **Params:** `page` (integer, optional) — 1-based page number; `per_page` (integer, optional) — Results per page, 1-50; `taxonomy_id` (integer, **required**) — A SeatGeek taxonomy id from GET /seatgeek/categories

### `seatgeek_events_near`

- **HTTP:** `GET /seatgeek/events-near`
- **What:** Browse SeatGeek events near a coordinate. Returns one page of SeatGeek events near a coordinate, soonest first -- the same call its city pages and homepage location-based sections make. Pair with GET /seatgeek/cities for a curated list of coordinates, or pass any coordinate directly.
- **Params:** `lat` (number, **required**) — Latitude; `lon` (number, **required**) — Longitude; `page` (integer, optional) — 1-based page number; `per_page` (integer, optional) — Results per page, 1-50

### `seatgeek_performer`

- **HTTP:** `GET /seatgeek/performer`
- **What:** Get a SeatGeek performer's detail. Returns one SeatGeek performer's (sports team, artist, or show) full detail by direct id lookup: name, type, image, popularity, home venue id, upcoming-event counts, and category taxonomy. id is SeatGeek's own numeric performer id, obtained from a search result. Use this when you already have a bare performer id and want to skip a search round-trip; seatgeek-search returns the same fields for a query.
- **Params:** `id` (integer, **required**) — SeatGeek's own numeric performer id

### `seatgeek_performer_events`

- **HTTP:** `GET /seatgeek/performer-events`
- **What:** Get a SeatGeek performer's event schedule. Returns one page of a SeatGeek performer's (sports team, artist, or show) upcoming event schedule, soonest first. performer_id is SeatGeek's own numeric performer id, obtained from a search result (e.g. 1 for the Los Angeles Dodgers).
- **Params:** `page` (integer, optional) — 1-based page number; `per_page` (integer, optional) — Results per page, 1-50; `performer_id` (integer, **required**) — SeatGeek's own numeric performer id

### `seatgeek_search`

- **HTTP:** `GET /seatgeek/search`
- **What:** Search SeatGeek events, performers, and venues. Free-text search across SeatGeek's own catalog of events, performers (sports teams, artists, and shows), and venues -- the same call the site's own search box and search-results page use. Any of the three result lists may come back empty for a query with no matches in that type.
- **Params:** `limit` (integer, optional) — Maximum results per result type (events/performers/venues), 1-50; `q` (string, **required**) — Free-text search query

### `seatgeek_trending`

- **HTTP:** `GET /seatgeek/trending`
- **What:** Get SeatGeek's trending-near-you events. Returns SeatGeek's ranked "trending near you" events for the required `lat` and `lon`. Each item has the event name, URL and image, local and UTC start times, `lowest_price` on the secondary market where available, current `rank` and `rank_change`. The list is identified by `list_id`, `list_type` and `list_display_name`.
- **Params:** `lat` (number, **required**) — Latitude; `lon` (number, **required**) — Longitude

### `seatgeek_venue`

- **HTTP:** `GET /seatgeek/venue`
- **What:** Get a SeatGeek venue's detail. Returns one SeatGeek venue's full detail: address, city/state/country, timezone, capacity, coordinates, and upcoming-event counts. id is SeatGeek's own numeric venue id, obtained from a search or event result.
- **Params:** `id` (integer, **required**) — SeatGeek's own numeric venue id

### `seatgeek_venue_events`

- **HTTP:** `GET /seatgeek/venue-events`
- **What:** Get a SeatGeek venue's event schedule. Returns one page of a SeatGeek venue's upcoming event schedule, soonest first. venue_id is SeatGeek's own numeric venue id, obtained from a search or event result (e.g. 1 for UNIQLO Field at Dodger Stadium).
- **Params:** `page` (integer, optional) — 1-based page number; `per_page` (integer, optional) — Results per page, 1-50; `venue_id` (integer, **required**) — SeatGeek's own numeric venue id

## StubHub (11)

### `stubhub_carousel`

- **HTTP:** `GET /stubhub/carousel`
- **What:** List StubHub performer discovery carousels. Returns the performer-page alternative, recently viewed, maybe-interested, and trending-event carousel sections. Obtain performer_slug and performer_id from a real StubHub performer URL or another StubHub result.
- **Params:** `category_id` (integer, **required**) — StubHub category id; `lat` (number, **required**) — Latitude; `lon` (number, **required**) — Longitude; `max` (integer, optional) — Maximum items per carousel section; defaults to 10; `performer_id` (integer, **required**) — StubHub performer numeric id; `performer_slug` (string, **required**) — StubHub performer URL slug; `top_level_category_id` (integer, **required**) — Top-level category: 1 (Theater), 2 (Sports), or 3 (Concerts)

### `stubhub_categories`

- **HTTP:** `GET /stubhub/categories`
- **What:** List StubHub's location-scoped category prices. Lists categories with currently-listed minimum ticket prices for a location and date range. This is a changing location/date-scoped feed, not the complete navigation taxonomy; use stubhub-navigation-categories for the full Theater, Sports, and Concerts tree.
- **Params:** `from` (string, optional) — Start of the date range: RFC3339 or a bare date (e.g. 2026-09-15). Defaults to now.; `lat` (number, **required**) — Latitude, -90 to 90; `lon` (number, **required**) — Longitude, -180 to 180; `to` (string, optional) — End of the date range, same accepted formats as from. Defaults to 14 days after from.

### `stubhub_category_events`

- **HTTP:** `GET /stubhub/category-events`
- **What:** List StubHub events in one category near a location. Lists paginated events in a single StubHub category (a sport league, team, or a top-level vertical -- use stubhub-categories to discover category ids) filtered by location, radius, and date range. A zero count with an empty events list is a valid no-results response.
- **Params:** `category_id` (integer, **required**) — A category id from stubhub-categories; `from` (string, optional) — Start of the date range: RFC3339 or a bare date (e.g. 2026-09-15). Defaults to now.; `include_parking_passes` (boolean, optional) — Also include parking-pass-only listings alongside regular events; `lat` (number, **required**) — Latitude, -90 to 90; `lon` (number, **required**) — Longitude, -180 to 180; `page` (integer, optional) — One-based result page; `radius_miles` (integer, optional) — Search radius in miles from lat/lon; `to` (string, optional) — End of the date range, same accepted formats as from. Defaults to 14 days after from.

### `stubhub_explore`

- **HTTP:** `GET /stubhub/explore`
- **What:** Discover StubHub events near a location. Discovers events near a location within a date range, optionally bounded by ticket price and by category. A zero count with an empty events list is a valid no-results response.
- **Params:** `category_id` (integer, optional) — Filter to one category/subcategory id. stubhub-categories discovers ids with a currently-listed event nearby, but only a small subset -- known-good ids: NBA 6453, MLB 6456, NFL 5084, NHL 4871, MLS 5062, Tennis 1012, Golf 1009 (Sports); Pop/Rock 260542, Alternative Music 1059, Classical 1014, R&B 1027, Rap and Hip-Hop Music 1026 (Concerts); Comedy 1015, Musicals 1017, Plays 358959, Family 2294 (Theater); Festival Tickets 1023 (works alone, no top_level_category_id needed); `from` (string, optional) — Start of the date range: RFC3339 or a bare date (e.g. 2026-09-15). Defaults to now.; `lat` (number, **required**) — Latitude, -90 to 90; `lon` (number, **required**) — Longitude, -180 to 180; `price_max` (integer, optional) — Maximum ticket price filter; `price_min` (integer, optional) — Minimum ticket price filter; `to` (string, optional) — End of the date range, same accepted formats as from. Defaults to 14 days after from.; `top_level_category_id` (integer, optional) — Filter to one top-level vertical

### `stubhub_navigation_categories`

- **HTTP:** `GET /stubhub/navigation-categories`
- **What:** List StubHub's complete top-level navigation tree. Lists the nested navigation taxonomy for one StubHub top-level category. The upstream accepts exactly category_id 1 (Theater), 2 (Sports), or 3 (Concerts). Use the returned ids and URLs to discover category and subcategory pages.
- **Params:** `category_id` (integer, **required**) — Top-level category: 1=Theater, 2=Sports, 3=Concerts

### `stubhub_performer_events`

- **HTTP:** `GET /stubhub/performer-events`
- **What:** List a StubHub performer or team's upcoming events. Lists a performer or team's own upcoming schedule (event name, date, venue, starting price) from their StubHub page. Obtain a real performer_slug+performer_id pair from stubhub-trending's url field (e.g. https://www.stubhub.com/kansas-city-chiefs-tickets/performer/6063 -- slug "kansas-city-chiefs-tickets", id 6063). A zero count with an empty events list is a valid no-upcoming-events response.
- **Params:** `performer_id` (integer, **required**) — The performer's numeric id; `performer_slug` (string, **required**) — The performer's URL slug, e.g. kansas-city-chiefs-tickets

### `stubhub_search`

- **HTTP:** `GET /stubhub/search`
- **What:** Search StubHub for performers, events, and groupings. Searches StubHub's anonymous grouped-search endpoint. Results are returned in StubHub's own performer/grouping/event result groups; the upstream request uses multipart form data and requires no cookies or CSRF token.
- **Params:** `query` (string, **required**) — Search query

### `stubhub_suggested_searches`

- **HTTP:** `GET /stubhub/suggested-searches`
- **What:** List StubHub's current search suggestions. Returns StubHub's short, changing list of performers, groupings, and categories currently suggested by its search UI. It takes no query parameters.
- **Params:** _none_

### `stubhub_trending`

- **HTTP:** `GET /stubhub/trending`
- **What:** List StubHub's currently-featured trending performers. Lists the performers/teams StubHub itself is currently featuring on its homepage hero rotation, each with a follower/favorites count and its upcoming event date range. A zero count with an empty performers list is a valid no-results response.
- **Params:** `top_level_category_id` (integer, optional) — Filter to one top-level vertical

### `stubhub_trending_events`

- **HTTP:** `GET /stubhub/trending-events`
- **What:** List StubHub's currently-trending individual events. Lists a paginated global feed of StubHub's currently-trending individual events (name, date, venue, canonical URL), optionally filtered to one top-level category vertical. Distinct from stubhub-trending, which rotates featured performers/teams rather than individual events. A zero count with an empty events list is a valid no-results response.
- **Params:** `page` (integer, optional) — One-based result page; `top_level_category_id` (integer, optional) — Filter to one top-level vertical

### `stubhub_venue_events`

- **HTTP:** `GET /stubhub/venue-events`
- **What:** List a StubHub venue's upcoming events. Lists a venue's own upcoming event calendar (event name, date, starting price) from its StubHub page. Obtain a real venue_slug+venue_id pair from another endpoint's event url field (e.g. https://www.stubhub.com/geha-field-at-arrowhead-stadium-tickets/venue/4467/ -- slug "geha-field-at-arrowhead-stadium-tickets", id 4467). A zero count with an empty events list is a valid no-upcoming-events response.
- **Params:** `venue_id` (integer, **required**) — The venue's numeric id; `venue_slug` (string, **required**) — The venue's URL slug, e.g. geha-field-at-arrowhead-stadium-tickets
