# podcast-topic-landscape — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**11 endpoints across 3 platform group(s).**

## Datasets (3)

### `datasets_apple_podcasts_shows_facets`

- **HTTP:** `GET /datasets/apple-podcasts-shows/facets`
- **What:** Facet Apple Podcasts shows dataset. Returns value counts for one field of the Apple Podcasts shows dataset, chosen by the required `facet`: `genre`, `genre_id`, `country`, `content_advisory_rating` or `run_id`. The counts honour the search filters (`q`, `genre`, `country`, `min_track_count` and others) and cover the top 50 values.
- **Params:** `country` (string, optional) — Exact storefront country filter, max 128 characters; `explicitness` (string, optional) — Exact explicitness filter, max 128 characters; `facet` (string, **required**) — Facet enum: genre, genre_id, country, content_advisory_rating, run_id; `genre` (string, optional) — Exact primary-genre filter, max 128 characters; `genre_id` (string, optional) — Exact Apple Podcasts genre id filter, max 128 characters; `min_track_count` (integer, optional) — Minimum episode count (track_count), 0 or greater; `q` (string, optional) — Full-text query over show title and artist name, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters

### `datasets_apple_podcasts_shows_item`

- **HTTP:** `GET /datasets/apple-podcasts-shows/items/{id}`
- **What:** Get an Apple Podcasts show from dataset. Returns one Apple Podcasts show from the dataset by its numeric show `id`. The record has show and artist names, genres, country, episode count (`track_count`), release date, feed URL, artwork and Apple URL. An id not in the dataset returns 404.
- **Params:** `id` (string, **required**) — Apple Podcasts numeric show id (e.g. 173001861)

### `datasets_apple_podcasts_shows_search`

- **HTTP:** `GET /datasets/apple-podcasts-shows/search`
- **What:** Search Apple Podcasts shows dataset. Searches the crawled public Apple Podcasts show catalog stored in a search index. One row per show. Discovered from a country x genre x collection chart grid and a search-term sweep — not a full catalog of every Apple Podcasts show. Sort enum: `relevance`, `popularity`, `track_count_desc`, `release_desc`, `title_asc`. Billing: this search costs 1 credit per record returned, with a minimum of 2 (an empty result costs 2, a full page of 100 costs 100).
- **Params:** `country` (string, optional) — Exact storefront country filter (the crawl's discovery storefront, e.g. us, gb), max 128 characters; `explicitness` (string, optional) — Exact explicitness filter as reported by Apple (e.g. explicit, cleaned), max 128 characters; `genre` (string, optional) — Exact primary-genre filter (e.g. Comedy, True Crime), max 128 characters; `genre_id` (string, optional) — Exact Apple Podcasts genre id filter (e.g. 1303 for Comedy), max 128 characters; `min_track_count` (integer, optional) — Minimum episode count (track_count), 0 or greater; `page` (integer, optional) — Page number, defaults to 1; `page_size` (integer, optional) — Page size, defaults to 20 and maxes at 100; page * page_size must be <= 10000; `q` (string, optional) — Full-text query over show title and artist name, max 256 characters; `run_id` (string, optional) — Exact crawl run-id filter, max 128 characters; `sort` (string, optional) — Sort enum: relevance, popularity, track_count_desc, release_desc, title_asc

## ApplePodcasts (4)

### `apple_podcasts_episodes_search`

- **HTTP:** `GET /apple-podcasts/episodes/search`
- **What:** Search Apple Podcasts episodes. Searches Apple Podcasts episodes by `term`, which is required. `country`, `lang`, `limit` and `page` (1-based) refine the search. Each episode has its `title`, `show_name`, `show_id`, `description`, `duration_millis`, `release_date`, `episode_url`, `preview_url`, `feed_url`, genres and artwork.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Number of episodes per page; `page` (integer, optional) — Search page number (1-based); `term` (string, **required**) — Search term

### `apple_podcasts_search`

- **HTTP:** `GET /apple-podcasts/search`
- **What:** Search Apple Podcasts shows. Searches Apple Podcasts shows by `term`, which is required. `country`, `lang`, `limit` and `page` (1-based) refine the search. Each show has `collection_name`, `artist_name`, `feed_url`, `primary_genre_name`, `genres`, `track_count`, `release_date`, content advisory rating and several artwork sizes.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Number of shows per page; `page` (integer, optional) — Search page number (1-based); `term` (string, **required**) — Search term

### `apple_podcasts_show`

- **HTTP:** `GET /apple-podcasts/show/{id}`
- **What:** Retrieve Apple Podcasts show details. Returns the details of one Apple Podcasts show by its Apple show `id`: `collection_name`, `artist_name`, `feed_url`, `primary_genre_name`, `genres`, `track_count`, `release_date`, content advisory rating and artwork. `country` and `lang` choose the storefront and language.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Podcasts show ID; `lang` (string, optional) — Result language tag

### `apple_podcasts_show_episodes`

- **HTTP:** `GET /apple-podcasts/show/{id}/episodes`
- **What:** Retrieve Apple Podcasts show episodes. Returns one Apple Podcasts show by its Apple show `id`, together with a list of its episodes. `limit` sets how many episodes to return; `country` and `lang` choose the storefront and language. Episodes have `title`, `description`, `duration_millis`, `release_date`, `episode_url` and `episode_guid`.
- **Params:** `country` (string, optional) — Two-letter storefront country code; `id` (string, **required**) — Apple Podcasts show ID; `lang` (string, optional) — Result language tag; `limit` (integer, optional) — Number of episodes to return

## SpotifyPodcasts (4)

### `spotify_podcasts_episode`

- **HTTP:** `GET /spotify-podcasts/episode`
- **What:** Retrieve Spotify podcast episode details. Returns public episode metadata. Provide either uri or id; defaults to a known public episode when omitted.
- **Params:** `id` (string, optional) — Spotify episode ID. Used when uri is omitted; `uri` (string, optional) — Spotify episode URI or open.spotify.com episode URL

### `spotify_podcasts_search`

- **HTTP:** `GET /spotify-podcasts/search`
- **What:** Search Spotify Podcasts. Searches Spotify podcasts for `q`, returning matching `shows`, `episodes` and `topResults`, with counts in `meta`. `limit` and `number_of_top_results` run 1 to 50. Optional flags (`include_pre_releases`, `include_audiobooks`, `include_authors`) widen the results. Episodes carry duration and release date; shows carry publisher.
- **Params:** `include_album_pre_releases` (boolean, optional) — Include album pre-release results; `include_audiobooks` (boolean, optional) — Include audiobooks; `include_authors` (boolean, optional) — Include authors; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `include_pre_releases` (boolean, optional) — Include pre-release results; `limit` (integer, optional) — Result limit, clamped to 1-50; `number_of_top_results` (integer, optional) — Top result limit, clamped to 1-50; `offset` (integer, optional) — Search offset; `q` (string, **required**) — Podcast search term

### `spotify_podcasts_show`

- **HTTP:** `GET /spotify-podcasts/show`
- **What:** Retrieve Spotify podcast show metadata. Returns metadata for one Spotify podcast show by `uri` (default `spotify:show:1QQJ7FElLE0K6CIfZNCxU4`): name, publisher, description, media type, explicit flag, `totalEpisodes`, cover images and Spotify URL. The two `include_` flags request extra content capability and content rating fields when Spotify supplies them.
- **Params:** `include_content_capability_trait` (boolean, optional) — Include content capability trait; `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `uri` (string, optional) — Spotify show URI

### `spotify_podcasts_show_episodes`

- **HTTP:** `GET /spotify-podcasts/show/episodes`
- **What:** Retrieve Spotify podcast show episodes. Returns the episodes of a Spotify podcast by show URI, with `offset` and `limit` (1-50). Each episode has its name, description, release date, duration in milliseconds, explicit and playable flags, Spotify URI, external URL and images; `total` gives the show's episode count.
- **Params:** `include_episode_content_ratings_v2` (boolean, optional) — Include Spotify episode content ratings v2; `limit` (integer, optional) — Episode limit, clamped to 1-50; `offset` (integer, optional) — Episode offset; `uri` (string, optional) — Spotify show URI
