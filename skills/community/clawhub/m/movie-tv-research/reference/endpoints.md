# movie-tv-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**124 endpoints across 7 platform group(s).**

## Box Office Mojo (21)

### `boxofficemojo_brand`

- **HTTP:** `GET /boxofficemojo/brand`
- **What:** Box Office Mojo brand detail. Returns release rows from a Box Office Mojo brand page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo brand id; `offset` (integer, optional) — Row offset for pagination (page size 100); `path` (string, optional) — Box Office Mojo brand path; `sort` (string, optional) — Sort field; `sortDir` (string, optional) — Sort direction; `url` (string, optional) — Absolute https://www.boxofficemojo.com brand URL

### `boxofficemojo_brands`

- **HTTP:** `GET /boxofficemojo/brands`
- **What:** Box Office Mojo brand chart. Returns Box Office Mojo's brand chart, ranked, with each brand's `name`, `id`, `path`, `url`, release count and lifetime gross (an integer in `lifetime_gross`, the displayed text in `lifetime_gross_raw`). Reorder with `sort` (`totalGross`, `numReleases` or `grossToDate`) and `sortDir` (`asc` or `desc`); they are echoed back only when applied.
- **Params:** `sort` (string, optional) — Sort field; `sortDir` (string, optional) — Sort direction

### `boxofficemojo_calendar`

- **HTTP:** `GET /boxofficemojo/calendar`
- **What:** Box Office Mojo domestic release schedule. Returns Box Office Mojo's domestic release schedule for one month, grouped by date. `year` (1921 to 2100) and `month` (1 to 12) are both required. Each release has its title, `release_url`, `distributor`, `scale`, `genres`, `cast` and poster image URLs when present.
- **Params:** `month` (integer, **required**) — Calendar month, 1 through 12; `year` (integer, **required**) — Calendar year, from 1921 through 2100

### `boxofficemojo_calendar_changes`

- **HTTP:** `GET /boxofficemojo/calendar/changes`
- **What:** Box Office Mojo domestic release schedule changes. Returns Box Office Mojo's list of changes to the domestic release schedule, grouped by change date. `offset` pages through the list in steps of 30, from 0 to 780. Each change has the release, `distributor`, `scale`, `old_date` and `new_date`, and `range` shows the position in the list.
- **Params:** `offset` (integer, optional) — Changes page offset. Allowed values: 0, 30, 60, ... 780

### `boxofficemojo_calendar_date`

- **HTTP:** `GET /boxofficemojo/calendar/date`
- **What:** Box Office Mojo domestic release schedule date. Returns the releases scheduled on one date in Box Office Mojo's domestic release schedule. `date` is required, in `YYYY-MM-DD` form. Each release has its title, `release_url`, `distributor`, `scale`, `genres`, `cast` and poster image URLs when present. A date with no scheduled releases returns a not-found error.
- **Params:** `date` (string, **required**) — Calendar date in YYYY-MM-DD format

### `boxofficemojo_date_domestic`

- **HTTP:** `GET /boxofficemojo/date/domestic`
- **What:** Box Office Mojo domestic daily box office. Returns rows from Box Office Mojo's domestic daily chart. Empty upstream daily pages return a typed not-found error rather than an empty success.
- **Params:** `date` (string, **required**) — Domestic box office date in YYYY-MM-DD format

### `boxofficemojo_franchise`

- **HTTP:** `GET /boxofficemojo/franchise`
- **What:** Box Office Mojo franchise detail. Returns release rows from a Box Office Mojo franchise page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo franchise id; `offset` (integer, optional) — Row offset for pagination (page size 100); `path` (string, optional) — Box Office Mojo franchise path; `sort` (string, optional) — Sort field; `sortDir` (string, optional) — Sort direction; `url` (string, optional) — Absolute https://www.boxofficemojo.com franchise URL

### `boxofficemojo_franchises`

- **HTTP:** `GET /boxofficemojo/franchises`
- **What:** Box Office Mojo franchise chart. Returns Box Office Mojo's franchise chart, ranked, with each franchise's `name`, `id`, `path`, `url`, release count and lifetime gross (an integer in `lifetime_gross`, the displayed text in `lifetime_gross_raw`). Reorder with `sort` (`totalGross`, `numReleases` or `grossToDate`) and `sortDir` (`asc` or `desc`); they are echoed back only when applied.
- **Params:** `sort` (string, optional) — Sort field; `sortDir` (string, optional) — Sort direction

### `boxofficemojo_genre`

- **HTTP:** `GET /boxofficemojo/genre`
- **What:** Box Office Mojo genre detail. Returns release rows from a Box Office Mojo genre page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo genre id; `offset` (integer, optional) — Row offset for pagination (page size 100); `path` (string, optional) — Box Office Mojo genre path; `sort` (string, optional) — Sort field; `sortDir` (string, optional) — Sort direction; `url` (string, optional) — Absolute https://www.boxofficemojo.com genre URL

### `boxofficemojo_genres`

- **HTTP:** `GET /boxofficemojo/genres`
- **What:** Box Office Mojo genre chart. Returns Box Office Mojo's genre chart, ranked, with each genre's `name`, `id`, `path`, `url`, release count and lifetime gross (an integer in `lifetime_gross`, the displayed text in `lifetime_gross_raw`). Reorder with `sort` (`totalGross`, `numTitles` or `grossToDate`) and `sortDir` (`asc` or `desc`); they are echoed back only when applied.
- **Params:** `sort` (string, optional) — Sort field; `sortDir` (string, optional) — Sort direction

### `boxofficemojo_lifetime_grosses`

- **HTTP:** `GET /boxofficemojo/lifetime-grosses`
- **What:** Box Office Mojo lifetime gross chart. Returns one page of Box Office Mojo's lifetime gross chart of movies. `area` is `worldwide` (default) or `domestic`, and `offset` pages in steps of 200 from 0 to 800. Each row has `rank`, `title`, `title_id`, `year` and `lifetime_gross` as an integer, with the displayed text in `lifetime_gross_raw`.
- **Params:** `area` (string, optional) — Chart area. Allowed values: worldwide, domestic; `offset` (integer, optional) — Chart page offset. Allowed values: 0, 200, 400, 600, 800

### `boxofficemojo_release`

- **HTTP:** `GET /boxofficemojo/release`
- **What:** Box Office Mojo release detail. Returns Box Office Mojo release summary fields and domestic daily rows from a release page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo release id; `path` (string, optional) — Box Office Mojo release path; `url` (string, optional) — Absolute https://www.boxofficemojo.com release URL

### `boxofficemojo_release_group`

- **HTTP:** `GET /boxofficemojo/release-group`
- **What:** Box Office Mojo release group detail. Returns market release rows grouped by region from a Box Office Mojo release-group page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo release-group id; `path` (string, optional) — Box Office Mojo release-group path; `url` (string, optional) — Absolute https://www.boxofficemojo.com release-group URL

### `boxofficemojo_showdown`

- **HTTP:** `GET /boxofficemojo/showdown`
- **What:** Box Office Mojo showdown detail. Returns release comparison metrics from a Box Office Mojo showdown page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo showdown id; `path` (string, optional) — Box Office Mojo showdown path; `url` (string, optional) — Absolute https://www.boxofficemojo.com showdown URL

### `boxofficemojo_showdowns`

- **HTTP:** `GET /boxofficemojo/showdowns`
- **What:** Box Office Mojo showdowns. Returns Box Office Mojo's showdowns, which compare groups of movies. Each row has the showdown `name`, `showdown_id`, `path`, `url`, `num_releases`, `total_gross` and the `top_release` with its gross, when Box Office Mojo shows them. Takes no parameters.
- **Params:** _none_

### `boxofficemojo_title`

- **HTTP:** `GET /boxofficemojo/title`
- **What:** Box Office Mojo title detail. Returns Box Office Mojo title release-group and market-gross tables from a title page. Pass exactly one of `id`, `path`, or `url`.
- **Params:** `id` (string, optional) — Box Office Mojo title id; `path` (string, optional) — Box Office Mojo title path; `url` (string, optional) — Absolute https://www.boxofficemojo.com title URL

### `boxofficemojo_weekend_domestic`

- **HTTP:** `GET /boxofficemojo/weekend/domestic`
- **What:** Box Office Mojo domestic weekend box office. Returns rows from Box Office Mojo's domestic weekend chart. Empty upstream weekend pages return a typed not-found error rather than an empty success.
- **Params:** `week` (integer, **required**) — Weekend number, 1 through 53; `year` (integer, **required**) — Domestic weekend year, from 1982 through 2100

### `boxofficemojo_weekend_domestic_by_distributor`

- **HTTP:** `GET /boxofficemojo/weekend/domestic/by-distributor`
- **What:** Box Office Mojo domestic weekend by distributor. Returns distributor rows from Box Office Mojo's domestic weekend by-distributor chart. Empty upstream weekend pages return a typed not-found error rather than an empty success.
- **Params:** `week` (integer, **required**) — Weekend number, 1 through 53; `year` (integer, **required**) — Domestic weekend year, from 1982 through 2100

### `boxofficemojo_weekend_domestic_estimates`

- **HTTP:** `GET /boxofficemojo/weekend/domestic/estimates`
- **What:** Box Office Mojo domestic weekend estimates. Returns estimate-vs-actual rows from Box Office Mojo's domestic weekend estimates chart. Empty upstream weekend pages return a typed not-found error rather than an empty success.
- **Params:** `week` (integer, **required**) — Weekend number, 1 through 53; `year` (integer, **required**) — Domestic weekend year, from 1982 through 2100

### `boxofficemojo_year_domestic`

- **HTTP:** `GET /boxofficemojo/year/domestic`
- **What:** Box Office Mojo domestic yearly box office. Returns the Box Office Mojo domestic box office chart for one year. `year` is required and runs from 1977 to 2100. Each row has `rank`, `release`, `release_date`, `distributor`, `theaters`, `gross`, `total_gross` and `new_this_year`, each gross also with its displayed text in a `_raw` field.
- **Params:** `year` (integer, **required**) — Domestic box office year, from 1977 through 2100

### `boxofficemojo_year_worldwide`

- **HTTP:** `GET /boxofficemojo/year/worldwide`
- **What:** Box Office Mojo worldwide yearly box office. Returns the Box Office Mojo worldwide box office chart for one year. `year` is required and runs from 1977 to 2100. Each row is a release group with its `rank`, `worldwide`, `domestic` and `foreign` grosses, the domestic and foreign shares, and `title_id`; each gross also has its displayed text in a `_raw` field.
- **Params:** `year` (integer, **required**) — Box office year, from 1977 through 2100

## IMDb (30)

### `imdb_charts`

- **HTTP:** `GET /imdb/charts`
- **What:** IMDb title charts. Returns an IMDb title chart, chosen with `chart`: `top_rated_movies` (default), `top_rated_tv_shows`, `most_popular_movies`, `most_popular_tv_shows`, `top_rated_english_movies` or `lowest_rated_movies`. `limit` sets the rows (default 25, max 250). Each title has its rank, id, year, rating, rating count and credits.
- **Params:** `chart` (string, optional) — IMDb chart; `limit` (integer, optional) — Rows to return, default 25, max 250

### `imdb_image_types`

- **HTTP:** `GET /imdb/image-types`
- **What:** IMDb image types. Lists every value the `type` parameter of the IMDb image endpoints accepts: `behind_the_scenes`, `event`, `poster`, `product`, `production_art`, `publicity`, `still_frame`, `unknown`. Each row carries a display label and a short description.
- **Params:** _none_

### `imdb_name`

- **HTTP:** `GET /imdb/name`
- **What:** IMDb name detail. Returns an IMDb person's profile. Pass exactly one of `id` (such as `nm0634240`) or `url`. The response has the name, biography, birth and death dates, birth place, professions, image and a known-for list of titles with year and credit category.
- **Params:** `id` (string, optional) — IMDb name id; `url` (string, optional) — Absolute https://www.imdb.com/name/<id>/ URL

### `imdb_name_awards`

- **HTTP:** `GET /imdb/name/awards`
- **What:** IMDb name awards. Returns the awards IMDb lists for a person. Pass exactly one of `id` or `url`. Each row has the event, year, category, `win` or `nomination` result, award name, recipients and related titles. `total` is the count IMDb lists, and `has_more` is true when fewer rows are returned.
- **Params:** `id` (string, optional) — IMDb name id; `url` (string, optional) — Absolute https://www.imdb.com/name/<id>/ URL

### `imdb_name_credits`

- **HTTP:** `GET /imdb/name/credits`
- **What:** IMDb name credits. Returns a person's IMDb filmography, grouped into sections such as Actor, Director and Self. Pass exactly one of `id` or `url`. Each credit has its title, year, role and episode count. A section returns up to 100 credits, so `total` can exceed the rows returned.
- **Params:** `id` (string, optional) — IMDb name id; `url` (string, optional) — Absolute https://www.imdb.com/name/<id>/ URL

### `imdb_name_images`

- **HTTP:** `GET /imdb/name/images`
- **What:** IMDb name images. Returns image metadata from a person's media index, including the original image URL, dimensions, caption and credited people. Filter by image type with `type`, which accepts a single value or a comma-separated list of: `behind_the_scenes`, `event`, `poster`, `product`, `production_art`, `publicity`, `still_frame`, `unknown`. Omit `type` to return every type. Limit defaults to 50 and clamps to 1000. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb name id; `limit` (integer, optional) — Rows to return, default 50, max 1000; `type` (string, optional) — Image type filter, single value or comma-separated list; `url` (string, optional) — Absolute https://www.imdb.com/name/<id>/ URL

### `imdb_name_videos`

- **HTTP:** `GET /imdb/name/videos`
- **What:** IMDb name video metadata. Returns public person video metadata and thumbnail URLs only; playback URLs and media manifests are never returned. IMDb caps the upstream slice at 100 and provides no usable continuation cursor, so `total` can exceed returned rows and `has_more` reports that condition. Limit defaults to 50 and clamps to 100. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb name id; `limit` (integer, optional) — Rows to return, default 50, max 100; `url` (string, optional) — Absolute https://www.imdb.com/name/<id>/ URL

### `imdb_search`

- **HTTP:** `GET /imdb/search`
- **What:** IMDb title search. Searches IMDb titles by `query`, returning up to `limit` rows (default 10, max 20). Each result has the title id, title, URL, year, title type, image and a description holding the lead cast. A query with no matches returns an empty `results` list.
- **Params:** `limit` (integer, optional) — Rows to return, default 10, max 20; `query` (string, **required**) — Search query

### `imdb_search_title`

- **HTTP:** `GET /imdb/search/title`
- **What:** IMDb advanced title search. Returns IMDb advanced title-search results (imdb.com/search/title/). At least one filter is required; sort/limit alone are not enough. Limit defaults to 25 and clamps to 50; only IMDb's first page of results is returned (see `total`/`has_more`), there is no deeper cursor pagination. Genre/company/certificate/country/language/keyword/characters/role are include-only lists; there is no exclude support. Unsupported: genre exclude, three curated `groups` values (best-picture-nominee, best-director-nominee, national-film-registry), and the non-plot "page topic" search fields.
- **Params:** `certificates` (string, optional) — Comma-separated `COUNTRY:RATING` certificate pairs, e.g. `US:PG-13`; `characters` (string, optional) — Comma-separated character names; `colors` (string, optional) — Comma-separated color info: `color`, `black_and_white`, `colorized`, `aces`; `companies` (string, optional) — Comma-separated IMDb company ids, format `co########`; `countries` (string, optional) — Comma-separated ISO country codes; `genres` (string, optional) — Comma-separated genres (include-only): `Action`, `Adventure`, `Animation`, `Biography`, `Comedy`, `Crime`, `Documentary`, `Drama`, `Family`, `Fantasy`, `Film-Noir`, `Game-Show`, `History`, `Horror`, `Music`, `Musical`, `Mystery`, `News`, `Reality-TV`, `Romance`, `Sci-Fi`, `Short`, `Sport`, `Talk-Show`, `Thriller`, `War`, `Western`; `groups` (string, optional) — Comma-separated awards/curated-list groups: `oscar_winner`, `oscar_nominee`, `emmy_winner`, `emmy_nominee`, `golden_globe_winner`, `golden_globe_nominee`, `best_picture_winner`, `best_director_winner`, `razzie_winner`, `razzie_nominee`, `top_100`, `top_250`, `top_1000`, `bottom_100`, `bottom_250`, `bottom_1000`; `include_adult` (boolean, optional) — Include adult titles. Defaults to excluded; `keywords` (string, optional) — Comma-separated plot keywords; `languages` (string, optional) — Comma-separated ISO language codes; `limit` (integer, optional) — Rows to return, default 25, max 50; `max_popularity` (integer, optional) — Maximum IMDb popularity rank; `max_runtime` (integer, optional) — Maximum runtime in minutes; `max_user_rating` (number, optional) — Maximum IMDb user rating, 0-10; `max_votes` (integer, optional) — Maximum number of user rating votes; `min_popularity` (integer, optional) — Minimum IMDb popularity rank (1 is most popular); `min_runtime` (integer, optional) — Minimum runtime in minutes; `min_user_rating` (number, optional) — Minimum IMDb user rating, 0-10; `min_votes` (integer, optional) — Minimum number of user rating votes; `plot` (string, optional) — Plot text search term; `release_date_from` (string, optional) — Release date lower bound: YYYY, YYYY-MM, or YYYY-MM-DD; `release_date_to` (string, optional) — Release date upper bound: YYYY, YYYY-MM, or YYYY-MM-DD; `role` (string, optional) — Comma-separated cast/crew IMDb name ids, format `nm########`; `sort` (string, optional) — One of `moviemeter`, `alpha`, `user_rating`, `num_votes`, `boxoffice_gross_us`, `runtime`, `year`, `release_date`; `sort_order` (string, optional) — `asc` or `desc`. Defaults to `asc` when sort is set; `sound_mixes` (string, optional) — Comma-separated sound mix names: `12-Track Digital Sound`, `3 Channel Stereo`, `4-Track Stereo`, `6-Track Stereo`, `70 mm 6-Track`, `AGA Sound System`, `Auro 11.1`, `CDS`, `Chronophone`, `Cinematophone`, `Cinephone`, `Cinerama 7-Track`, `Cinesound`, `D-Cinema 48kHz 5.1`, `Datasat`, `De Forest Phonofilm`, `Digitrac Digital Audio System`, `Dolby`, `Dolby Atmos`, `Dolby Digital`, `Dolby Digital EX`, `Dolby SR`, `Dolby Stereo`, `Dolby Surround 7.1`, `DTS`, `DTS 70 mm`, `DTS Stereo`, `DTS-ES`, `IMAX 6-Track`, `Kinoplasticon`, `LC-Concept Digital Sound`, `Matrix Surround`, `Mono`, `Perspecta Stereo`, `Phono-Kinema`, `SDDS`, `Sensurround`, `Silent`, `Sonics-DDP`, `Sonix`, `Stereo`, `Ultra Stereo`, `Vitaphone`; `title` (string, optional) — Title-name substring match; `title_type` (string, optional) — Comma-separated title types: `feature`, `tvSeries`, `short`, `tvEpisode`, `tvMiniSeries`, `tvMovie`, `tvSpecial`, `tvShort`, `videoGame`, `video`, `musicVideo`, `podcastSeries`, `podcastEpisode`

### `imdb_title`

- **HTTP:** `GET /imdb/title`
- **What:** IMDb title detail. Returns an IMDb title's details. Pass exactly one of `id` (such as `tt1375666`) or `url`. The response has the title, type, year, release date, runtime, genres, plot, content rating, rating and count, popularity rank, directors and up to three lead cast. Rating and cast fields appear only when present.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_awards`

- **HTTP:** `GET /imdb/title/awards`
- **What:** IMDb title awards. Returns the awards IMDb lists for a title. Pass exactly one of `id` or `url`. Each row has the event, year, category, `win` or `nomination` result, award name, recipients and notes. `total` is the number IMDb lists and `has_more` is true when only part is returned.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_box_office`

- **HTTP:** `GET /imdb/title/box-office`
- **What:** IMDb title box office summary. Returns a title's public box-office summary: lifetime gross by market (domestic, international, worldwide), the domestic opening weekend, and the production budget. IMDb reports each figure independently, so a real title with no box office data (most TV series, many non-theatrical titles) returns `has_box_office: false` with every figure omitted rather than an error. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_company_credits`

- **HTTP:** `GET /imdb/title/company-credits`
- **What:** IMDb title company credits. Returns the company credits IMDb lists for a title, in sections such as production companies and distributors. Pass exactly one of `id` or `url`. Each company has its name, URL and a qualifier note. `total` is the count IMDb lists, so a short list is normal on popular titles.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_connections`

- **HTTP:** `GET /imdb/title/connections`
- **What:** IMDb title connections. Returns a bounded slice of a title's public connections: other titles it references or is referenced by, such as remakes, spin-offs, "featured in" clips, and "edited into" compilations. `category` is upstream-supplied free text, not a closed enum. IMDb's connections list can run to hundreds or thousands of rows, so `total` can exceed the returned rows and `has_more` reports that condition. Limit defaults to 50 and clamps to 250. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb title id; `limit` (integer, optional) — Rows to return, default 50, max 250; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_credits`

- **HTTP:** `GET /imdb/title/credits`
- **What:** IMDb title credits. Returns the full cast and crew IMDb lists for a title, in named sections. Pass exactly one of `id` or `url`. Each credit has a name, IMDb name URL, role and, for cast, the character. The cast returns up to 2,000 rows and other sections up to 100.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_episodes`

- **HTTP:** `GET /imdb/title/episodes`
- **What:** IMDb title episodes. Returns public IMDb episode rows for a series title. Limit defaults to 10 and clamps to 20. Optional `season` filters the episodes returned. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb title id; `limit` (integer, optional) — Rows to return, default 10, max 20; `season` (integer, optional) — Season number to request; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_filming_locations`

- **HTTP:** `GET /imdb/title/filming-locations`
- **What:** IMDb title filming locations. Returns the filming locations IMDb lists for a title. Pass exactly one of `id` or `url`. Each location has its text and an optional note. `total` is the count IMDb lists, `has_more` shows when the list is cut short, and a title with none returns an empty list with `total` 0.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_goofs`

- **HTTP:** `GET /imdb/title/goofs`
- **What:** IMDb title goofs. Returns the goofs IMDb lists for a title. Pass exactly one of `id` or `url`. Each entry in `facts` has the text, a `spoiler` flag and, when IMDb groups it, a category such as Continuity. `total` is the count IMDb lists and `has_more` is true when only part is returned.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_images`

- **HTTP:** `GET /imdb/title/images`
- **What:** IMDb title images. Returns image metadata from a title's media index, including the original image URL, dimensions, caption and credited people. Filter by image type with `type`, which accepts a single value or a comma-separated list of: `behind_the_scenes`, `event`, `poster`, `product`, `production_art`, `publicity`, `still_frame`, `unknown`. Omit `type` to return every type. Limit defaults to 50 and clamps to 1000. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb title id; `limit` (integer, optional) — Rows to return, default 50, max 1000; `type` (string, optional) — Image type filter, single value or comma-separated list; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_keywords`

- **HTTP:** `GET /imdb/title/keywords`
- **What:** IMDb title keywords. Returns the plot keywords IMDb lists for a title. Pass exactly one of `id` or `url`. Each keyword has its text and an IMDb search URL for that keyword. `total` is the count IMDb lists, so a short list is normal on popular titles.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_parental_guide`

- **HTTP:** `GET /imdb/title/parental-guide`
- **What:** IMDb title parental guide. Returns the IMDb parental guide for a title. Pass exactly one of `id` or `url`. Categories such as violence, profanity and frightening scenes carry a severity of `none`, `mild`, `moderate` or `severe` and the guide text. A `summary` gives counts and the highest severity. Spoiler items are excluded.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_public_facts_analysis`

- **HTTP:** `GET /imdb/title/public-facts-analysis`
- **What:** IMDb title public facts analysis. Returns derived public-page summary metrics for IMDb trivia, goofs, quotes, keywords, filming locations, and company credits. This endpoint is not viewing advice. Pass exactly one of `id` or `url`. The six sections are gathered from six independent sources, so a section that cannot be fetched is omitted and named in `missing_sections` with `partial` set to `true`, rather than failing the whole response; an error is returned only when no section could be fetched. Callers that require a complete analysis should check `partial`.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_quotes`

- **HTTP:** `GET /imdb/title/quotes`
- **What:** IMDb title quotes. Returns the quotes IMDb lists for a title. Pass exactly one of `id` or `url`. Each entry in `facts` is a whole exchange, with lines prefixed by the speaker, plus a `spoiler` flag. `total` is the count IMDb lists, so a short list is normal on popular titles.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_ratings`

- **HTTP:** `GET /imdb/title/ratings`
- **What:** IMDb title ratings breakdown. Returns IMDb's aggregate rating, vote count, ten rating buckets, and country rating summaries. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute IMDb title URL

### `imdb_title_release_info`

- **HTTP:** `GET /imdb/title/release-info`
- **What:** IMDb title release info. Returns the release dates and alternate titles IMDb lists for a title. Pass exactly one of `id` or `url`. Releases have a country, date and note; alternate titles have a country, title and type. Both lists are often shorter than `total` and `alternate_titles_total`.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_reviews`

- **HTTP:** `GET /imdb/title/reviews`
- **What:** IMDb title user reviews. Returns public IMDb user review rows. Limit defaults to 10 and clamps to 20. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb title id; `limit` (integer, optional) — Rows to return, default 10, max 20; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_similar`

- **HTTP:** `GET /imdb/title/similar`
- **What:** IMDb similar titles. Returns the titles in IMDb's More like this recommendations for a title. Pass exactly one of `id` (such as `tt0111161`) or `url`. Each title has its id, name, URL, year, type, runtime, content rating, rating, rating count and image.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute IMDb title URL

### `imdb_title_technical_specs`

- **HTTP:** `GET /imdb/title/technical-specs`
- **What:** IMDb title technical specs. Returns public IMDb technical specifications such as runtime, sound mix, color, and aspect ratio. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_trivia`

- **HTTP:** `GET /imdb/title/trivia`
- **What:** IMDb title trivia. Returns the trivia IMDb lists for a title. Pass exactly one of `id` or `url`. Each entry in `facts` has the text, a `spoiler` flag and, for grouped items, a category such as Director Trademark. `total` is the count IMDb lists and `has_more` is true when only part is returned.
- **Params:** `id` (string, optional) — IMDb title id; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

### `imdb_title_videos`

- **HTTP:** `GET /imdb/title/videos`
- **What:** IMDb title video metadata. Returns public title video metadata and thumbnail URLs only; playback URLs and media manifests are never returned. IMDb server-truncates this connection and exposes no usable continuation cursor, so `total` can exceed returned rows and `has_more` reports that condition. Limit defaults to 50 and clamps to 100. Pass exactly one of `id` or `url`.
- **Params:** `id` (string, optional) — IMDb title id; `limit` (integer, optional) — Rows to return, default 50, max 100; `url` (string, optional) — Absolute https://www.imdb.com/title/<id>/ URL

## JustWatch (21)

### `justwatch_age_certifications`

- **HTTP:** `GET /justwatch/age-certifications`
- **What:** Get JustWatch age certifications. Lists the JustWatch age certification technical names for a country, such as `PG-13` for the US. `country` is a two-letter code and defaults to `US`. An invalid country returns `400`, and an unexpectedly empty result returns `503`.
- **Params:** `country` (string, optional) — Two-letter country code

### `justwatch_discover`

- **HTTP:** `GET /justwatch/discover`
- **What:** Discover JustWatch titles. Returns popular movies and shows filtered by optional genre short names, provider short names, production countries, monetization types, and release year bounds. Combine `providers` with `production_countries` to build charts such as most popular Korean or Japanese titles on a given service. Type accepts only `all`, `movie`, or `show`; monetization_types accepts only `FLATRATE`, `FREE`, `ADS`, `RENT`, or `BUY`.
- **Params:** `country` (string, optional) — Two-letter country code; `genres` (string, optional) — Comma-separated JustWatch genre short names; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 20 and clamps to 50; `monetization_types` (string, optional) — Comma-separated monetization types: FLATRATE, FREE, ADS, RENT, BUY; `production_countries` (string, optional) — Comma-separated two-letter ISO production-country codes; `providers` (string, optional) — Comma-separated JustWatch provider short names; `type` (string, optional) — Title type: all, movie, show; `year_max` (integer, optional) — Maximum release year; `year_min` (integer, optional) — Minimum release year

### `justwatch_episode_by_id`

- **HTTP:** `GET /justwatch/episode/by-id`
- **What:** Get JustWatch episode by raw id. Looks up one JustWatch episode by its raw `id` (`tse` followed by digits, such as `tse5550494`), in the `country` (default `US`) and `language` (default `en`) you choose. Returns the title, year, episode number, description, poster, paths, and streaming offers with provider, monetization type, presentation type, price and currency. A valid id with no match returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `id` (string, **required**) — Raw JustWatch episode id matching tse[0-9]+; `language` (string, optional) — Two-letter language code

### `justwatch_episode_offers`

- **HTTP:** `GET /justwatch/episode/offers`
- **What:** Get JustWatch episode offers. Returns the streaming offers for one JustWatch episode `id` (`tse` followed by digits) across one to five comma-separated country codes in `countries` (default `US`), with `language` defaulting to `en`. Each country entry lists offers by provider, monetization type, presentation type, price and currency, with the episode details. An unknown id returns `404`.
- **Params:** `countries` (string, optional) — One to five comma-separated two-letter country codes; `id` (string, **required**) — Raw JustWatch episode id matching tse[0-9]+; `language` (string, optional) — Two-letter language code

### `justwatch_genre_titles`

- **HTTP:** `GET /justwatch/genre/titles`
- **What:** Get JustWatch genre titles. Lists popular JustWatch titles for one genre short name in `genre`, such as `act`. `type` is `all`, `movie` or `show` (default `all`), `limit` defaults to 20 and is capped at 50, and `country` and `language` default to `US` and `en`. Each title has its id, year, path, poster, production countries and offers. Find genre names with the genres endpoint.
- **Params:** `country` (string, optional) — Two-letter country code; `genre` (string, **required**) — JustWatch genre short name; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 20 and clamps to 50; `type` (string, optional) — Title type: all, movie, show

### `justwatch_genres`

- **HTTP:** `GET /justwatch/genres`
- **What:** Get JustWatch genres. Lists the JustWatch genres, each with its `short_name` (such as `act`) and a translated name in the `language` you choose (two-letter code, default `en`). Use the short names as the `genre` input of the genre titles endpoint. An invalid language returns `400`.
- **Params:** `language` (string, optional) — Two-letter language code

### `justwatch_monetization_titles`

- **HTTP:** `GET /justwatch/monetization/titles`
- **What:** Get JustWatch monetization titles. Returns popular titles for one monetization type. monetization_type accepts only `FLATRATE`, `FREE`, `ADS`, `RENT`, or `BUY`; type accepts only `all`, `movie`, or `show`.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 20 and clamps to 50; `monetization_type` (string, **required**) — Monetization type: FLATRATE, FREE, ADS, RENT, BUY; `type` (string, optional) — Title type: all, movie, show

### `justwatch_new`

- **HTTP:** `GET /justwatch/new`
- **What:** Get new JustWatch titles. Returns newly available movies and shows. Type accepts only `all`, `movie`, or `show`; limit defaults to 20 and clamps to 50.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 20 and clamps to 50; `type` (string, optional) — Title type: all, movie, show

### `justwatch_popular`

- **HTTP:** `GET /justwatch/popular`
- **What:** Get popular JustWatch titles. Returns popular movies and shows. Type accepts only `all`, `movie`, or `show`; limit defaults to 20 and clamps to 50.
- **Params:** `country` (string, optional) — Two-letter country code; `cursor` (string, optional) — Opaque next_cursor from the prior response; omit for the first page; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 20 and clamps to 50; `type` (string, optional) — Title type: all, movie, show

### `justwatch_provider_titles`

- **HTTP:** `GET /justwatch/provider/titles`
- **What:** Get JustWatch provider titles. Returns popular movies and shows available on one streaming provider, by JustWatch provider short name such as `nfx`, for a country (default `US`) and language (default `en`). Filter to movies or shows with `type` and cap results with `limit` (default 20, max 50). Each title has its name, year, type, poster, JustWatch URL and offers with price, currency and monetization type.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 20 and clamps to 50; `provider` (string, **required**) — JustWatch provider short name; `type` (string, optional) — Title type: all, movie, show

### `justwatch_providers`

- **HTTP:** `GET /justwatch/providers`
- **What:** Get JustWatch providers. Lists the streaming providers JustWatch tracks in a country. `country` is a two-letter code and defaults to `US`. Each provider has its id, clear name, short name, technical name and an absolute icon URL. An invalid country returns `400`.
- **Params:** `country` (string, optional) — Two-letter country code

### `justwatch_search`

- **HTTP:** `GET /justwatch/search`
- **What:** Search JustWatch titles. Searches JustWatch titles. Country must be a two-letter ISO code such as `US`; language must be a two-letter code such as `en`.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 10 and clamps to 25; `query` (string, **required**) — Search query

### `justwatch_season_by_id`

- **HTTP:** `GET /justwatch/season/by-id`
- **What:** Get JustWatch season by raw id. Looks up one JustWatch season by its raw `id` (`tss` followed by digits, such as `tss297253`), in the `country` (default `US`) and `language` (default `en`) you choose. Returns the season title, number, year, description, path, URL and poster. A valid id with no match returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `id` (string, **required**) — Raw JustWatch season id matching tss[0-9]+; `language` (string, optional) — Two-letter language code

### `justwatch_season_episodes`

- **HTTP:** `GET /justwatch/season/episodes`
- **What:** Get JustWatch season episodes. Lists the episodes of a JustWatch season given as `season_id` (`tss` followed by digits), with `country` defaulting to `US` and `language` to `en`. Each episode has its number, title, description and streaming offers with provider, price and currency. Path, URL and poster appear only when JustWatch has them for that episode. An unknown season returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `season_id` (string, **required**) — Raw JustWatch season id matching tss[0-9]+

### `justwatch_show_seasons`

- **HTTP:** `GET /justwatch/show/seasons`
- **What:** Get JustWatch show seasons. Lists the seasons of a JustWatch show given as `show_id` (`ts` followed by digits, such as `ts287292`), with `country` defaulting to `US` and `language` to `en`. Each season has its number, title, year, description, path and poster. The show itself comes back with genres, scoring, runtime and offers. An unknown show returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `language` (string, optional) — Two-letter language code; `show_id` (string, **required**) — Raw JustWatch show id matching ts[0-9]+

### `justwatch_title`

- **HTTP:** `GET /justwatch/title`
- **What:** Get JustWatch title details. Returns the details of a JustWatch movie or show. Pass exactly one of `path` (such as `/us/movie/inception`) or `url` (an absolute JustWatch address). The response has the title, year, genres, runtime, content rating, `scoring` (IMDb and TMDB scores, tomato meter, JustWatch rating) and current offers. Titles with no offers still return metadata; a missing page returns `404`.
- **Params:** `path` (string, optional) — JustWatch title path; `url` (string, optional) — Absolute https://www.justwatch.com title URL

### `justwatch_title_analysis`

- **HTTP:** `GET /justwatch/title/analysis`
- **What:** Analyze JustWatch title availability. Fetches a JustWatch title page and summarizes provider availability, monetization buckets, formats, price ranges, and best rent/buy/free/subscription options. Pass exactly one of `path` or `url`.
- **Params:** `path` (string, optional) — JustWatch title path; `url` (string, optional) — Absolute https://www.justwatch.com title URL

### `justwatch_title_by_id`

- **HTTP:** `GET /justwatch/title/by-id`
- **What:** Get JustWatch title by raw id. Looks up a JustWatch movie or show by its raw `id` (`tm` or `ts` followed by digits, such as `tm92641`), with `country` defaulting to `US` and `language` to `en`. Returns the title, year, genres, runtime, content rating, description, scoring, and offers with provider, monetization type, price and currency. A valid id with no match returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `id` (string, **required**) — Raw JustWatch movie/show id matching tm[0-9]+ or ts[0-9]+; `language` (string, optional) — Two-letter language code

### `justwatch_title_media`

- **HTTP:** `GET /justwatch/title/media`
- **What:** Get JustWatch title media. Returns the media for a JustWatch movie or show `id` (`tm` or `ts` followed by digits): credits with role, name, character and person id, video clips with provider and URL, and backdrop image URLs. `country` defaults to `US` and `language` to `en`. YouTube clips carry a watch URL. An unknown id returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `id` (string, **required**) — Raw JustWatch movie/show id matching tm[0-9]+ or ts[0-9]+; `language` (string, optional) — Two-letter language code

### `justwatch_title_offers`

- **HTTP:** `GET /justwatch/title/offers`
- **What:** Get JustWatch title offers. Returns the streaming offers for a JustWatch movie or show `id` across one to five comma-separated country codes in `countries` (default `US`), with `language` defaulting to `en`. Each country entry has its offers (provider, monetization type, presentation type, price, currency) and the title details. An unknown id returns `404`.
- **Params:** `countries` (string, optional) — One to five comma-separated two-letter country codes; `id` (string, **required**) — Raw JustWatch movie/show id matching tm[0-9]+ or ts[0-9]+; `language` (string, optional) — Two-letter language code

### `justwatch_title_similar`

- **HTTP:** `GET /justwatch/title/similar`
- **What:** Get similar JustWatch titles. Lists titles similar to a JustWatch movie or show `id` (`tm` or `ts` followed by digits). `limit` defaults to 10 and is capped at 25; `country` defaults to `US` and `language` to `en`. Each result has its id, type, title, year, path, poster, production countries and offers. An unknown id returns `404`.
- **Params:** `country` (string, optional) — Two-letter country code; `id` (string, **required**) — Raw JustWatch movie/show id matching tm[0-9]+ or ts[0-9]+; `language` (string, optional) — Two-letter language code; `limit` (integer, optional) — Maximum results, defaults to 10 and clamps to 25

## Letterboxd (7)

### `letterboxd_film`

- **HTTP:** `GET /letterboxd/film/{slug}`
- **What:** Get a Letterboxd film. Returns a Letterboxd film: synopsis, director, cast, genres, countries, languages, runtime, and aggregate member rating.
- **Params:** `slug` (string, **required**) — Letterboxd film slug

### `letterboxd_film_rating_histogram`

- **HTTP:** `GET /letterboxd/film/{slug}/rating-histogram`
- **What:** Get a Letterboxd film's rating distribution. Returns a film's full star-rating distribution (0.5 to 5.0 in half-star buckets) with counts and percentages.
- **Params:** `slug` (string, **required**) — Letterboxd film slug

### `letterboxd_film_reviews`

- **HTTP:** `GET /letterboxd/film/{slug}/reviews`
- **What:** Get a Letterboxd film's popular reviews. Returns popular reviews for a Letterboxd film by `slug`, up to `limit` (default 10, max 50). Each review has the username, display name, rating from 0.5 to 5.0 when the reviewer gave one, liked flag, date, text, spoiler flag, and like and comment counts.
- **Params:** `limit` (integer, optional) — Max reviews, default 10, max 50; `slug` (string, **required**) — Letterboxd film slug

### `letterboxd_film_similar`

- **HTTP:** `GET /letterboxd/film/{slug}/similar`
- **What:** Get films similar to a Letterboxd film. Lists films Letterboxd recommends as similar to the film given by `slug`, up to `limit` (default 10, max 50). Each film has its `slug`, title and Letterboxd URL. Use the slug to look up that film's details.
- **Params:** `limit` (integer, optional) — Max films, default 10, max 50; `slug` (string, **required**) — Letterboxd film slug

### `letterboxd_person`

- **HTTP:** `GET /letterboxd/person/{slug}`
- **What:** Get a Letterboxd person's filmography. Returns a person's Letterboxd filmography by `slug`, ranked by popularity for one credit role. `role` is `actor` (default) or `director`, and `limit` defaults to 10 with a max of 50. The response has the person's name, role, and films with `slug`, title and Letterboxd URL.
- **Params:** `limit` (integer, optional) — Max films, default 10, max 50; `role` (string, optional) — Credit role, default actor; `slug` (string, **required**) — Letterboxd person slug

### `letterboxd_popular`

- **HTTP:** `GET /letterboxd/popular`
- **What:** Get a Letterboxd popularity-ranked film chart. Returns a Letterboxd film chart ranked by popularity. Omit `period` for all-time, or set `day`, `week`, `month` or `year`. `genre` takes a genre slug, `decade` a value like `2010s`, and `limit` defaults to 10 with a max of 50. Each film has its `slug`, title and Letterboxd URL.
- **Params:** `decade` (string, optional) — Decade filter, e.g. 2010s; `genre` (string, optional) — Genre slug filter; `limit` (integer, optional) — Max films, default 10, max 50; `period` (string, optional) — Popularity window, omit for all-time

### `letterboxd_search`

- **HTTP:** `GET /letterboxd/search`
- **What:** Search Letterboxd. Searches Letterboxd for films, people, lists and tags by `q`, required. `type` can be set to `film` to return films only; `limit` defaults to 10 with a max of 50. Fields vary by result type: films carry `slug` and `year`, people carry `slug` and `role`, lists carry `owner`, and tags carry only a title and URL.
- **Params:** `limit` (integer, optional) — Max results, default 10, max 50; `q` (string, **required**) — Search query; `type` (string, optional) — Optional result type filter

## Metacritic (7)

### `metacritic_browse`

- **HTTP:** `GET /metacritic/browse`
- **What:** Browse Metacritic titles. Browse Metacritic titles by content type, optionally filtered by genre and ordered by Metascore, popularity, or release date. Returns paginated title cards with Metascore and user score.
- **Params:** `genre` (string, optional) — Genre filter (e.g. Action); `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Results per page (default 24, max 100); `sort` (string, optional) — Sort order; `type` (string, **required**) — Content type

### `metacritic_movie`

- **HTTP:** `GET /metacritic/movie/{slug}`
- **What:** Get a Metacritic movie. Returns a Metacritic movie: Metascore (critic) and user score with sentiment and review counts, genres, cast/crew, rating, runtime, release date, IMDb id, and trailer.
- **Params:** `slug` (string, **required**) — Metacritic movie slug

### `metacritic_movie_critic_reviews`

- **HTTP:** `GET /metacritic/movie/{slug}/critic-reviews`
- **What:** List a Metacritic movie's critic reviews. Lists critic reviews for a Metacritic movie by `slug` (such as `oppenheimer`). Each review has the publication, score, quote, author, date and source URL. `sort` is `date` (default), `score` or `publication`; `page` defaults to 1 and `per_page` to 20 with a max of 50. The response includes the `total` count.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Results per page (default 20, max 50); `slug` (string, **required**) — Metacritic movie slug; `sort` (string, optional) — Sort order

### `metacritic_movie_user_reviews`

- **HTTP:** `GET /metacritic/movie/{slug}/user-reviews`
- **What:** List a Metacritic movie's user reviews. Returns paginated user reviews for a movie: author, score (0-10), quote, date, helpfulness, and spoiler flag.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Results per page (default 20, max 50); `slug` (string, **required**) — Metacritic movie slug; `sort` (string, optional) — Sort order

### `metacritic_tv`

- **HTTP:** `GET /metacritic/tv/{slug}`
- **What:** Get a Metacritic TV show. Returns a Metacritic TV show: Metascore (critic) and user score with sentiment and review counts, genres, networks, season count, rating, release date, IMDb id, and trailer.
- **Params:** `slug` (string, **required**) — Metacritic TV show slug

### `metacritic_tv_critic_reviews`

- **HTTP:** `GET /metacritic/tv/{slug}/critic-reviews`
- **What:** List a Metacritic TV show's critic reviews. Lists critic reviews for a Metacritic TV show by `slug` (such as `breaking-bad`). Each review has the publication, score, quote, author, date and source URL. `sort` is `date` (default), `score` or `publication`; `page` defaults to 1 and `per_page` to 20 with a max of 50. The response includes the `total` count.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Results per page (default 20, max 50); `slug` (string, **required**) — Metacritic TV show slug; `sort` (string, optional) — Sort order

### `metacritic_tv_user_reviews`

- **HTTP:** `GET /metacritic/tv/{slug}/user-reviews`
- **What:** List a Metacritic TV show's user reviews. Returns paginated user reviews for a TV show: author, score (0-10), quote, date, helpfulness, and spoiler flag.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `per_page` (integer, optional) — Results per page (default 20, max 50); `slug` (string, **required**) — Metacritic TV show slug; `sort` (string, optional) — Sort order

## Rotten Tomatoes (29)

### `rottentomatoes_browse_filters`

- **HTTP:** `GET /rottentomatoes/browse/filters`
- **What:** Rotten Tomatoes browse filter discovery. Returns every filter and accepted value exposed by the selected live Rotten Tomatoes browse page. Call this before building filtered movie or TV browse requests; values differ by list and update with the site's menus.
- **Params:** `list` (string, optional) — Browse list: movies_in_theaters, movies_at_home, movies_coming_soon, tv_series_browse

### `rottentomatoes_browse_movies`

- **HTTP:** `GET /rottentomatoes/browse/movies`
- **What:** Rotten Tomatoes movie discovery rows. Returns movie rows from Rotten Tomatoes' browse listing. Use `/rottentomatoes/browse/filters` to discover current values for each list. Filters accept comma-separated values; pagination uses the opaque `after` cursor from the previous response.
- **Params:** `affiliates` (string, optional) — Comma-separated streaming/service values from browse/filters; `after` (string, optional) — Opaque next-page cursor returned in data.page_info.end_cursor; `audience` (string, optional) — Comma-separated Popcornmeter values from browse/filters; `critics` (string, optional) — Comma-separated Tomatometer values from browse/filters; `genres` (string, optional) — Comma-separated genre values from browse/filters; `limit` (integer, optional) — Rows to return, default 30 (one full page), max 30. The cursor always moves past the whole 30-row page, so keep the default when paging; `list` (string, optional) — Movie browse list: movies_in_theaters, movies_at_home, movies_coming_soon; `ratings` (string, optional) — Comma-separated content ratings from browse/filters; `sort` (string, optional) — Sort value from the selected list's browse/filters response

### `rottentomatoes_browse_tv`

- **HTTP:** `GET /rottentomatoes/browse/tv`
- **What:** Rotten Tomatoes TV discovery rows. Returns TV series rows from Rotten Tomatoes' browse listing. Use `/rottentomatoes/browse/filters?list=tv_series_browse` to discover current filters; pagination uses the opaque `after` cursor from the previous response.
- **Params:** `affiliates` (string, optional) — Comma-separated streaming/service values from browse/filters; `after` (string, optional) — Opaque next-page cursor returned in data.page_info.end_cursor; `audience` (string, optional) — Comma-separated Popcornmeter values from browse/filters; `critics` (string, optional) — Comma-separated Tomatometer values from browse/filters; `genres` (string, optional) — Comma-separated genre values from browse/filters; `limit` (integer, optional) — Rows to return, default 30 (one full page), max 30. The cursor always moves past the whole 30-row page, so keep the default when paging; `list` (string, optional) — TV browse list: tv_series_browse; `ratings` (string, optional) — Comma-separated content ratings from browse/filters; `sort` (string, optional) — Sort value from browse/filters

### `rottentomatoes_critic`

- **HTTP:** `GET /rottentomatoes/critic`
- **What:** Rotten Tomatoes critic profile. Returns one Rotten Tomatoes critic's profile: display name, initials, vanity, encrypted critic id, biography, website, top-critic and Tomatometer-approved flags, review and publication counts, follower/following counts, critics groups, the publications they write for and their most recent reviews. The profile is read directly from Rotten Tomatoes' feed (normally a second or two), with a slower browser fallback when the feed cannot be read. An unknown critic path returns 404. Pass exactly one of `path` or `url`.
- **Params:** `path` (string, optional) — Rotten Tomatoes critic path: /critic/{slug}. /critics/{slug} (the form critics/authors returns) and /profiles/critic/{slug} are accepted too; `url` (string, optional) — Absolute https://www.rottentomatoes.com critic URL

### `rottentomatoes_critic_publications`

- **HTTP:** `GET /rottentomatoes/critic/publications`
- **What:** Rotten Tomatoes critic publications. Returns the publications one Rotten Tomatoes critic writes for: publication name, editorial site URL, logo image, encrypted and numeric publication ids, and the top-publication and Tomatometer-approved flags. The list is read directly from Rotten Tomatoes' feed (normally a second or two), with a slower browser fallback when the feed cannot be read. Only the first page is served today; `data.page_info.end_cursor` reports that more exist. An unknown critic path returns 404. Pass exactly one of `path` or `url`.
- **Params:** `path` (string, optional) — Rotten Tomatoes critic path: /critic/{slug}. /critics/{slug} (the form critics/authors returns) and /profiles/critic/{slug} are accepted too; `url` (string, optional) — Absolute https://www.rottentomatoes.com critic URL

### `rottentomatoes_critic_reviews`

- **HTTP:** `GET /rottentomatoes/critic/reviews`
- **What:** Rotten Tomatoes reviews by one critic. Returns the movie reviews published by one critic, newest first. Each review carries a stable `id`, ISO `created_at`/`updated_at`, the publication, the original article URL and a `media` object naming the reviewed title (with its path, URL and poster). The list is pageable `limit` reviews at a time: pass `data.page_info.end_cursor` as `after` and keep `limit` the same while paging. It is read directly from Rotten Tomatoes' review feed (`data.transport` is `feed_api`, normally a second or two), with a slower browser fallback (`browser_render`, at most five pages) when the feed cannot be read. A critic with no reviews returns 200 with an empty `reviews` array; an unknown critic path returns 404. `data.subject.kind` is `critic` and `data.subject.title` is the reviewer's display name as Rotten Tomatoes prints it.
- **Params:** `after` (string, optional) — Pagination cursor: pass data.page_info.end_cursor from the previous response, with the same limit. Lists can be paged through the available reviews.; `limit` (integer, optional) — Reviews per page, default 10, max 20. Keep it the same on every page of one walk: the cursor is a page index times this value.; `path` (string, optional) — Rotten Tomatoes critic path: /critic/{slug}. /critics/{slug} (the form critics/authors returns) and /profiles/critic/{slug} are accepted too; `url` (string, optional) — Absolute https://www.rottentomatoes.com critic URL

### `rottentomatoes_critics_authors`

- **HTTP:** `GET /rottentomatoes/critics/authors`
- **What:** Rotten Tomatoes critic directory. Returns current or inactive critics from Rotten Tomatoes' public author directory. Browse one letter or search by name; use `next_cursor` as `after` or `previous_cursor` as `before`, as indicated by the corresponding page flag. The letter values come from the live directory controls.
- **Params:** `after` (string, optional) — Opaque cursor from data.next_cursor; `before` (string, optional) — Opaque cursor from data.previous_cursor; cannot be combined with after; `inactive` (boolean, optional) — Include the site's inactive critics list; `letter` (string, optional) — Directory letter. Omit when using search; default a.; `limit` (integer, optional) — Rows per page, default 100, range 1 to 100; `search` (string, optional) — Search critics by name; cannot be combined with letter

### `rottentomatoes_editorial_content`

- **HTTP:** `GET /rottentomatoes/editorial/content`
- **What:** Rotten Tomatoes editorial content listing. Lists paginated editorial records from the selected public content type. The pages collection lists public editorial section and campaign indexes. Use the editorial types endpoint to discover accepted type values.
- **Params:** `include_children` (boolean, optional) — For categories only, include child categories; default false; `limit` (integer, optional) — Rows per page, default 20, range 1 to 100; `operator` (string, optional) — Whether any or all selected terms must match; default OR; `page` (integer, optional) — One-based result page from 1 to 10000; default 1; `query` (string, optional) — Optional text filter; maximum 200 bytes; `taxonomy` (string, optional) — Optional editorial taxonomy; discover type support from /rottentomatoes/editorial/taxonomies; `term_ids` (string, optional) — Comma-separated positive term IDs; required with taxonomy; `type` (string, **required**) — Editorial content type

### `rottentomatoes_editorial_detail`

- **HTTP:** `GET /rottentomatoes/editorial/detail`
- **What:** Rotten Tomatoes editorial article detail. Returns the public body, paragraphs, headings, links, images, and video embeds from an Editorial article, gallery, guide, on-the-go article, or preview. Discover paths from editorial content collections. The response body_html preserves public Gutenberg/ranked-list markup.
- **Params:** `path` (string, **required**) — Discovered Editorial content path

### `rottentomatoes_editorial_search`

- **HTTP:** `GET /rottentomatoes/editorial/search`
- **What:** Rotten Tomatoes editorial search. Searches public Rotten Tomatoes editorial content, including articles and guides. Results include content subtype plus total-page metadata.
- **Params:** `limit` (integer, optional) — Rows per page, default 10, range 1 to 100; `page` (integer, optional) — One-based result page from 1 to 10000; default 1; `query` (string, **required**) — Editorial search text; maximum 200 bytes

### `rottentomatoes_editorial_section`

- **HTTP:** `GET /rottentomatoes/editorial/section`
- **What:** Rotten Tomatoes editorial section archive. Returns the rendered article cards for a discovered editorial page, RT hub, or hub subpage. Discover paths through editorial content types `pages`, `rt-hub`, and `hub-subpage`. Static pages use `articles_page` pagination upstream; hubs use `/page/{n}/`.
- **Params:** `page` (integer, optional) — One-based page, default 1; `path` (string, **required**) — Discovered editorial section path

### `rottentomatoes_editorial_taxonomies`

- **HTTP:** `GET /rottentomatoes/editorial/taxonomies`
- **What:** Rotten Tomatoes editorial taxonomy discovery. Returns the complete set of public editorial term vocabularies accepted by the term discovery endpoint, with the content types each taxonomy filters.
- **Params:** _none_

### `rottentomatoes_editorial_terms`

- **HTTP:** `GET /rottentomatoes/editorial/terms`
- **What:** Rotten Tomatoes editorial taxonomy terms. Pages public terms from one discovered editorial taxonomy. All taxonomy values are listed by `/rottentomatoes/editorial/taxonomies`; `parent` is accepted only for `categories`, while `offset` is supported by all other taxonomies.
- **Params:** `exclude` (string, optional) — Comma-separated positive term IDs to exclude; `hide_empty` (boolean, optional) — When true, omit terms with no assigned content; `include` (string, optional) — Comma-separated positive term IDs to include; `limit` (integer, optional) — Terms per page, default 20, range 1 to 100; `offset` (integer, optional) — Zero-based offset; accepted except for categories; `order` (string, optional) — Term sort direction; `orderby` (string, optional) — Term sort key; `page` (integer, optional) — One-based page, default 1; `parent` (integer, optional) — Category parent ID; accepted only for categories; `post` (integer, optional) — Filter to terms assigned to this content record; `search` (string, optional) — Optional term search; maximum 200 bytes; `slug` (string, optional) — Optional term slug or comma-separated slugs; `taxonomy` (string, **required**) — Editorial taxonomy value

### `rottentomatoes_editorial_types`

- **HTTP:** `GET /rottentomatoes/editorial/types`
- **What:** Rotten Tomatoes editorial content types. Lists the editorial content types Rotten Tomatoes accepts as `type` on its editorial content endpoint, each with a `value` and `label` (for example `article`, `guide`, `gallery`, `rt-hub` and `pages`). The set was last verified on 2026-09-26, shown in `verified_at`. The `pages` type returns metadata and permalinks, not page bodies.
- **Params:** _none_

### `rottentomatoes_episode`

- **HTTP:** `GET /rottentomatoes/episode`
- **What:** Rotten Tomatoes episode detail. Returns Rotten Tomatoes TV episode metadata, scorecard data, parent series/season metadata, and public video metadata. Pass exactly one of `path` or `url`.
- **Params:** `path` (string, optional) — Rotten Tomatoes episode path; `url` (string, optional) — Absolute https://www.rottentomatoes.com episode URL

### `rottentomatoes_episode_reviews`

- **HTTP:** `GET /rottentomatoes/episode/reviews`
- **What:** Rotten Tomatoes TV episode critic reviews. Returns the critic reviews of one TV episode, newest first, read the same way as the season and movie feeds. Reviews carry a stable `id`, ISO `created_at`/`updated_at`, the critic identity and the original article URL. The list is pageable `limit` reviews at a time: pass `data.page_info.end_cursor` as `after` and keep `limit` the same while paging. It is read directly from Rotten Tomatoes' review feed (`data.transport` is `feed_api`, normally about a second), with a slower browser fallback (`browser_render`, at most five pages) when the feed cannot be read. Episode review lists are often small or empty: an episode nobody has reviewed yet returns 200 with an empty `reviews` array. `data.subject` identifies the episode.
- **Params:** `after` (string, optional) — Pagination cursor: pass data.page_info.end_cursor from the previous response, with the same limit. Critic cursors are base64 page indexes; audience cursors are opaque keyset values that should be passed back unchanged. The feed has no 500-review ceiling; browser fallback is capped at five pages.; `limit` (integer, optional) — Reviews per page, default 10, max 20. Keep it the same on every page of one walk: the cursor is a page index times this value.; `path` (string, optional) — Rotten Tomatoes episode path; `type` (string, optional) — Review list: critics (default), top-critics or audience.; `url` (string, optional) — Absolute https://www.rottentomatoes.com episode URL

### `rottentomatoes_movie`

- **HTTP:** `GET /rottentomatoes/movie`
- **What:** Rotten Tomatoes movie detail. Returns Rotten Tomatoes movie metadata, scorecard data, and representative audience reviews. Pass exactly one of `path` or `url`.
- **Params:** `path` (string, optional) — Rotten Tomatoes movie path; `url` (string, optional) — Absolute https://www.rottentomatoes.com movie URL

### `rottentomatoes_movie_reviews`

- **HTTP:** `GET /rottentomatoes/movie/reviews`
- **What:** Rotten Tomatoes movie reviews. Returns Rotten Tomatoes movie reviews, newest first. All four `type` values return the full review feed in one request: each review carries a stable `id`, ISO `created_at`/`updated_at` timestamps, the critic identity and the original article URL, and the list is pageable `limit` reviews at a time: pass `data.page_info.end_cursor` back as `after` for the next page and keep `limit` the same while paging. `data.transport` is `feed_api` for that path. A title with no reviews yet, or a top-critics or audience list that is still empty, returns 200 with an empty `reviews` array. If the feed cannot be read the service loads the movie's own review page the way a visitor's browser does and reads the list that page receives (`transport: browser_render`, slower, at most five pages); if that also fails for the first page, the movie page's embedded sample of about 6 reviews is served with `render_error` set (`transport: public_page`) and the call is not charged. `data.subject.kind` is `movie`, and `data.movie` remains present for compatibility. `data.fetched_at` and the `X-Cache` and `X-Availability-Last-Success-*` response headers show how fresh the data is. Pass exactly one of `path` or `url`. Supported `type` values are `critics`, `top-critics`, `audience`, and `verified-audience`.
- **Params:** `after` (string, optional) — Pagination cursor: pass data.page_info.end_cursor from the previous response. Critic cursors are base64 page indexes; audience cursors are opaque keyset values that should be passed back unchanged. The feed has no 500-review ceiling; browser fallback is capped at five pages. Invalid cursors are rejected before upstream work.; `limit` (integer, optional) — Reviews per page, default 10, max 20. Keep it the same on every page of one walk: the critic cursor is a page index times this value.; `path` (string, optional) — Rotten Tomatoes movie path; `type` (string, optional) — Review type: critics, top-critics, audience, verified-audience; `url` (string, optional) — Absolute https://www.rottentomatoes.com movie URL

### `rottentomatoes_movie_videos`

- **HTTP:** `GET /rottentomatoes/movie/videos`
- **What:** Rotten Tomatoes movie videos and trailers. Returns the videos Rotten Tomatoes lists for one movie: trailers and clips with the video id, title, kind (`TRAILER`/`OTHER`), duration, thumbnail, playable stream/playlist URL and the video page URL. The primary video reference is read from the movie page and the list comes from Rotten Tomatoes' open JSON endpoint (`/cnapi/videos`), so it is as fast as other endpoints. A movie with no listed video returns an empty `data.videos` rather than an error. `data.fetched_at` is the UTC time the data was fetched. Pass exactly one of `path` or `url`.
- **Params:** `path` (string, optional) — Rotten Tomatoes movie path; `url` (string, optional) — Absolute https://www.rottentomatoes.com movie URL

### `rottentomatoes_movies`

- **HTTP:** `GET /rottentomatoes/movies`
- **What:** Rotten Tomatoes movie details, several at once. Returns the details of up to 20 Rotten Tomatoes movies in one call, in the order requested. Each entry carries the title, synopsis, path and URL, `ems_id`, runtime, release date/year, production companies, the release runs with distributors, the Tomatometer and Popcornmeter scores, the score variants for all critics, top critics, all audience and verified audience, the critics and audience consensus, and `where_to_watch`: the public streaming, rental and purchase offers with provider name, link, licence, quality, price and availability date. Those are public provider pages, not playable media URLs. Identifiers that resolve to nothing are listed in `data.not_found` instead of failing the call. Pass exactly one of `ids` (Rotten Tomatoes `ems_id` values) or `paths` (Rotten Tomatoes movie paths or URLs); the `paths` form resolves each path first, so it costs one extra upstream read per path. The headline Tomatometer and Popcornmeter carry no counts; review and rating counts are in the score variants (for the number of critic reviews read `scores.critics_all.review_count`). Review samples are not returned here: use `/rottentomatoes/movie/reviews` for reviews. `data.fetched_at` is the UTC fetch time.
- **Params:** `ids` (string, optional) — Comma-separated Rotten Tomatoes ems_id values, 1 to 20; `paths` (string, optional) — Comma-separated Rotten Tomatoes movie paths or URLs, 1 to 20

### `rottentomatoes_person`

- **HTTP:** `GET /rottentomatoes/person`
- **What:** Rotten Tomatoes person detail and filmography. Returns Rotten Tomatoes celebrity/person metadata and filmography rows. Pass exactly one of `path` or `url`.
- **Params:** `after` (string, optional) — Filmography pagination cursor: pass data.page_info.end_cursor from the previous response.; `limit` (integer, optional) — Filmography page size. Defaults to 20; a value above 100 is lowered to 100; a negative value is rejected.; `media_type` (string, optional) — Filmography list to page: movie or tv. Omit to use the page's embedded first page.; `path` (string, optional) — Rotten Tomatoes person path; `sort` (string, optional) — Filmography sort order. Omit for newest.; `url` (string, optional) — Absolute https://www.rottentomatoes.com person URL

### `rottentomatoes_publication`

- **HTTP:** `GET /rottentomatoes/publication`
- **What:** Rotten Tomatoes publication profile. Returns one Rotten Tomatoes publication: its name, encrypted id, editorial page, image, whether it is a top publication and Tomatometer approved, its follower and review counts, and the critics who write for it with their names, encrypted ids, profile URLs and top-critic flags. Take the `id` from `encrypted_publication_id` (or `publication_id`) on any review row returned by the review endpoints. `data.fetched_at` is the UTC fetch time.
- **Params:** `id` (string, **required**) — Publication id: encrypted_publication_id or publication_id

### `rottentomatoes_publication_reviews`

- **HTTP:** `GET /rottentomatoes/publication/reviews`
- **What:** Rotten Tomatoes publication reviews. Returns the critic reviews one Rotten Tomatoes publication has published, newest first: stable review ids, ISO `created_at`/`updated_at` times, the critic identity, the publication name, the quote, the score sentiment and the original article URL. Pass `data.page_info.end_cursor` back as `after` for the next page, with the same `limit` (max 20). `data.subject.kind` is `publication` and `data.subject.title` is the outlet's name. An empty list is a `200` with no reviews. The `id` must be the encrypted publication id (`encrypted_publication_id` on any review row); a numeric id is rejected. `data.fetched_at` is the UTC fetch time.
- **Params:** `after` (string, optional) — Pagination cursor: pass data.page_info.end_cursor from the previous response; `id` (string, **required**) — Publication id: encrypted_publication_id; `limit` (integer, optional) — Reviews per page, default 10, max 20. Keep it the same on every page of one walk.

### `rottentomatoes_search`

- **HTTP:** `GET /rottentomatoes/search`
- **What:** Rotten Tomatoes movie search. Searches Rotten Tomatoes movies by the required `query`, returning up to `limit` rows (default 10, max 20). Each row has the title, URL, release year or start and end year, `tomatometer_score` and sentiment, `certified_fresh`, cast and image. No matches returns an empty `results` array.
- **Params:** `limit` (integer, optional) — Rows to return, default 10, max 20; `query` (string, **required**) — Search query

### `rottentomatoes_season`

- **HTTP:** `GET /rottentomatoes/season`
- **What:** Rotten Tomatoes season detail. Returns Rotten Tomatoes TV season metadata, scorecard data, parent series metadata, and episode rows. Pass exactly one of `path` or `url`.
- **Params:** `path` (string, optional) — Rotten Tomatoes season path; `url` (string, optional) — Absolute https://www.rottentomatoes.com season URL

### `rottentomatoes_season_reviews`

- **HTTP:** `GET /rottentomatoes/season/reviews`
- **What:** Rotten Tomatoes TV season critic reviews. Returns the critic reviews of one TV season, newest first. Each review has a stable `id`, ISO `created_at`/`updated_at` timestamps, the critic identity and the original article URL. The list is pageable `limit` reviews at a time: pass `data.page_info.end_cursor` as `after` and keep `limit` the same while paging. It is read directly from Rotten Tomatoes' review feed (`data.transport` is `feed_api`, normally about a second); if the feed cannot be read, the service may fall back to loading the season's reviews page in a browser (`transport: browser_render`, much slower and at most five pages deep). A season with no critic reviews yet returns 200 with an empty `reviews` array. `data.subject` identifies the season. `data.fetched_at`, `X-Cache` and `X-Availability-Last-Success-*` describe freshness. Pass exactly one of `path` or `url`.
- **Params:** `after` (string, optional) — Pagination cursor: pass data.page_info.end_cursor from the previous response. Critic cursors are base64 page indexes; audience cursors are opaque keyset values that should be passed back unchanged. The feed has no 500-review ceiling; browser fallback is capped at five pages.; `limit` (integer, optional) — Reviews per page, default 10, max 20. Keep it the same on every page of one walk: the cursor is a page index times this value.; `path` (string, optional) — Rotten Tomatoes season path; `type` (string, optional) — Review list: critics (default), top-critics or audience.; `url` (string, optional) — Absolute https://www.rottentomatoes.com season URL

### `rottentomatoes_series`

- **HTTP:** `GET /rottentomatoes/series`
- **What:** Rotten Tomatoes series detail. Returns Rotten Tomatoes TV series metadata and scorecard data. Pass exactly one of `path` or `url`.
- **Params:** `path` (string, optional) — Rotten Tomatoes series path; `url` (string, optional) — Absolute https://www.rottentomatoes.com series URL

### `rottentomatoes_sitemap_urls`

- **HTTP:** `GET /rottentomatoes/sitemap/urls`
- **What:** Rotten Tomatoes sitemap URL page. Returns a page of URLs from one child sitemap. Discover valid `name` values with `rottentomatoes-sitemaps`; use offset/limit to page through the complete sitemap.
- **Params:** `limit` (integer, optional) — URLs to return, default 100, max 500; `name` (string, **required**) — Sitemap name returned by /rottentomatoes/sitemaps; `offset` (integer, optional) — Zero-based offset, default 0

### `rottentomatoes_sitemaps`

- **HTTP:** `GET /rottentomatoes/sitemaps`
- **What:** Rotten Tomatoes sitemap discovery. Returns the live sitemap index and every named child sitemap, including movie, TV series, season, episode, person, critic, publication, browse-list, and static route inventories.
- **Params:** _none_

## TMDB (9)

### `tmdb_collection`

- **HTTP:** `GET /tmdb/collection/{id}`
- **What:** Get a TMDB collection. Returns a TMDB collection (a movie franchise grouping) by `id`, which can be the collection id or an id-slug. The response has the collection title, overview, `uri` and `source_url`, plus its member movies, each with id, title, overview, poster URL, release date and `uri`.
- **Params:** `id` (string, **required**) — TMDB collection id or id-slug

### `tmdb_genres`

- **HTTP:** `GET /tmdb/genres`
- **What:** List TMDB browse genres. Returns every genre ID for TMDB movie and TV browse pages. Use movie values only with movie list filters and TV values only with TV list filters.
- **Params:** _none_

### `tmdb_movie`

- **HTTP:** `GET /tmdb/movie/{id}`
- **What:** Get a TMDB movie. Returns a TMDB movie: overview, tagline, genres, countries, runtime, budget/revenue, top-billed cast, top crew (director/writer), and aggregate rating.
- **Params:** `id` (string, **required**) — TMDB movie id

### `tmdb_movie_list`

- **HTTP:** `GET /tmdb/movie/list`
- **What:** Get a TMDB movie chart. Returns a page of TMDB movies from the `category` chart (`popular` by default, or `top_rated`, `now_playing`, `upcoming`), optionally refined by `sort_by`, `with_genres`, `original_language`, release dates, rating, votes and runtime. `limit` defaults to 10 (max 20). Each movie has id, title, overview, poster, release date and `uri`; `has_next_page` signals more pages.
- **Params:** `category` (string, optional) — Movie chart, default popular; `date_from` (string, optional) — Release date lower bound (YYYY-MM-DD); `date_to` (string, optional) — Release date upper bound (YYYY-MM-DD); `include_adult` (boolean, optional) — Include adult titles; `limit` (integer, optional) — Max movies, default 10, max 20; `max_rating` (number, optional) — Maximum rating, 0-10; `max_runtime` (integer, optional) — Maximum runtime in minutes; `min_rating` (number, optional) — Minimum rating, 0-10; `min_runtime` (integer, optional) — Minimum runtime in minutes; `min_votes` (integer, optional) — Minimum vote count; `original_language` (string, optional) — Two-letter original-language code; `page` (integer, optional) — 1-based page, default 1; `sort_by` (string, optional) — Sort order; `with_genres` (string, optional) — Comma- or pipe-separated movie genre ids: 28,12,16,35,80,99,18,10751,14,36,27,10402,9648,10749,878,10770,53,10752,37

### `tmdb_person`

- **HTTP:** `GET /tmdb/person/{id}`
- **What:** Get a TMDB person. Returns a TMDB person by `id`: name, biography, birth date, photo URL and a filmography of movie and TV credits, most prominent first. `limit` caps the credits (default 10, max 20). Each credit has its `type` (`movie` or `tv`), id, title and `uri`. The biography may include a Wikipedia CC-BY-SA attribution note.
- **Params:** `id` (string, **required**) — TMDB person id; `limit` (integer, optional) — Max filmography credits, default 10, max 20

### `tmdb_person_list`

- **HTTP:** `GET /tmdb/person/list`
- **What:** List popular people on TMDB. Returns one page from TMDB's Popular People directory, including each person's id, name, known-for titles, profile image, and detail URL.
- **Params:** `limit` (integer, optional) — Max people, default 10, max 20; `page` (integer, optional) — 1-based page, default 1

### `tmdb_search`

- **HTTP:** `GET /tmdb/search`
- **What:** Search TMDB. Searches TMDB movies, TV shows, people, and collections. An unscoped query interleaves results across all four types rather than returning whichever type happens to rank first.
- **Params:** `limit` (integer, optional) — Max results, default 10, max 20; `page` (integer, optional) — 1-based results page, default 1; `query` (string, **required**) — Search query; `type` (string, optional) — Optional result type filter

### `tmdb_tv`

- **HTTP:** `GET /tmdb/tv/{id}`
- **What:** Get a TMDB TV show. Returns a TMDB TV show: overview, tagline, genres, countries, episode count, first/last air year, top-billed cast, top crew (creator), and aggregate rating.
- **Params:** `id` (string, **required**) — TMDB TV show id

### `tmdb_tv_list`

- **HTTP:** `GET /tmdb/tv/list`
- **What:** Get a TMDB TV chart. Returns a page of TMDB TV shows from the `category` chart (`popular` by default, or `top_rated`, `airing_today`, `on_the_air`), optionally refined by `sort_by`, `with_genres`, `original_language`, first-air-date bounds `date_from` and `date_to`, rating, votes and runtime. `limit` defaults to 10 (max 20). A filtered page with no matches returns an empty `shows` array.
- **Params:** `category` (string, optional) — TV chart, default popular; `date_from` (string, optional) — First-air date lower bound (YYYY-MM-DD); `date_to` (string, optional) — First-air date upper bound (YYYY-MM-DD); `include_adult` (boolean, optional) — Include adult titles; `limit` (integer, optional) — Max shows, default 10, max 20; `max_rating` (number, optional) — Maximum rating, 0-10; `max_runtime` (integer, optional) — Maximum runtime in minutes; `min_rating` (number, optional) — Minimum rating, 0-10; `min_runtime` (integer, optional) — Minimum runtime in minutes; `min_votes` (integer, optional) — Minimum vote count; `original_language` (string, optional) — Two-letter original-language code; `page` (integer, optional) — 1-based page, default 1; `sort_by` (string, optional) — Sort order; `with_genres` (string, optional) — Comma- or pipe-separated TV genre ids: 10759,16,35,80,99,18,10751,10762,9648,10763,10764,10765,10766,10767,10768,37
