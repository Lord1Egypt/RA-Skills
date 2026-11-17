# news-briefing-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**32 endpoints across 5 platform group(s).**

## GDELT (12)

### `gdelt_context`

- **HTTP:** `GET /gdelt/context`
- **What:** Sentence-level co-occurrence search across recent GDELT coverage. Searches the last 72 hours of GDELT-monitored news for sentences where every term of the required `query` appears together. Returns up to `maxrecords` rows (default 75, max 200), each with the matching sentence, its surrounding context, title, URL, domain, language and an `is_quote` flag. Filter with `domain`, `language`, `is_quote`, `timespan` or `from` and `to`, and order with `sort`.
- **Params:** `domain` (string, optional) — Convenience domain filter, appended to the query as domain:VALUE.; `from` (string, optional) — Start of an absolute time window. Accepts YYYY-MM-DD, RFC3339, or GDELT's raw YYYYMMDDHHMMSS. Cannot be combined with timespan; GDELT caps this endpoint's window at 72 hours.; `is_quote` (boolean, optional) — Only return sentences GDELT identified as a quotation.; `language` (string, optional) — Source-language filter (GDELT's searchlang parameter). Space-segmented languages only (excludes CJK and similar).; `maxrecords` (integer, optional) — Rows to return. GDELT's own hard cap is 200 for this endpoint (lower than gdelt-search's 250); there is no pagination cursor beyond it.; `query` (string, **required**) — GDELT query string. All terms must co-occur in the same sentence. Supports quoted phrases, (a OR b), domain:example.com.; `sort` (string, optional) — Result order.; `timespan` (string, optional) — Relative time window ending now, e.g. 30min, 6h, 3d. Cannot be combined with from/to. GDELT caps this endpoint's window at 72 hours.; `to` (string, optional) — End of an absolute time window. Same formats as from.

### `gdelt_search`

- **HTTP:** `GET /gdelt/search`
- **What:** Search global news coverage indexed by GDELT. Searches global news coverage indexed by GDELT for the required `query`, which accepts quoted phrases, `(a OR b)`, `theme:`, `tone<N` and `domain:`. Narrow with `country`, `language`, `domain`, and `timespan` or `from` and `to` (about the last 3 months are indexed). Returns up to `maxrecords` articles (default 75, max 250) with title, URL, domain, language, source country and `seen_at`.
- **Params:** `country` (string, optional) — Convenience source-country filter, appended to the query as sourcecountry:VALUE. Accepts a GDELT-recognized country name (no spaces) or 2-letter FIPS code.; `domain` (string, optional) — Convenience domain filter, appended to the query as domain:VALUE.; `from` (string, optional) — Start of an absolute time window. Accepts YYYY-MM-DD, RFC3339, or GDELT's raw YYYYMMDDHHMMSS. Cannot be combined with timespan; GDELT only indexes roughly the last 3 months.; `language` (string, optional) — Convenience source-language filter, appended to the query as sourcelang:VALUE. Accepts a GDELT-recognized language name or 3-letter code.; `maxrecords` (integer, optional) — Rows to return. GDELT's own hard cap is 250; there is no pagination cursor beyond it.; `query` (string, **required**) — GDELT query string. Supports GDELT's own search operators: quoted phrases, (a OR b), theme:NAME, tone<N / tone>N, near20:\; `sort` (string, optional) — Result order.; `timespan` (string, optional) — Relative time window ending now, e.g. 1h, 2d, 1w, 3m. Cannot be combined with from/to.; `to` (string, optional) — End of an absolute time window. Same formats as from.

### `gdelt_timeline`

- **HTTP:** `GET /gdelt/timeline`
- **What:** Coverage volume or tone over time for a GDELT query. Returns how coverage of the required GDELT `query` changes over time, as dated points. `metric` picks `volume` (the default, share of monitored articles), `volume_raw` (matching article count), `tone` (average sentiment), or `lang` and `country` for one series per language or country. Filter with `country`, `language`, `domain`, `timespan` or `from` and `to`; `smooth` runs 0 to 30 (default 0).
- **Params:** `country` (string, optional) — Convenience source-country filter, appended to the query as sourcecountry:VALUE.; `domain` (string, optional) — Convenience domain filter, appended to the query as domain:VALUE.; `from` (string, optional) — Start of an absolute time window. Accepts YYYY-MM-DD, RFC3339, or GDELT's raw YYYYMMDDHHMMSS. Cannot be combined with timespan.; `language` (string, optional) — Convenience source-language filter, appended to the query as sourcelang:VALUE.; `metric` (string, optional) — Timeline metric. lang and country return one series per language/country instead of one aggregate series.; `query` (string, **required**) — GDELT query string. Same syntax as gdelt-search's query.; `smooth` (integer, optional) — Moving-window smoothing applied to the timeline, in steps. 0 disables smoothing.; `timespan` (string, optional) — Relative time window ending now, e.g. 1h, 2d, 1w, 3m. Cannot be combined with from/to.; `to` (string, optional) — End of an absolute time window. Same formats as from.

### `gdelt_tonechart`

- **HTTP:** `GET /gdelt/tonechart`
- **What:** Sentiment histogram for a GDELT query. Returns a sentiment histogram for the required GDELT `query`: one bin per integer tone value, each with an article `count` and a short sample of top articles with title and URL. Filter with `country`, `language`, `domain`, and `timespan` or `from` and `to`. A tone value with no matching articles is absent rather than returned with a zero count.
- **Params:** `country` (string, optional) — Convenience source-country filter, appended to the query as sourcecountry:VALUE.; `domain` (string, optional) — Convenience domain filter, appended to the query as domain:VALUE.; `from` (string, optional) — Start of an absolute time window. Accepts YYYY-MM-DD, RFC3339, or GDELT's raw YYYYMMDDHHMMSS. Cannot be combined with timespan.; `language` (string, optional) — Convenience source-language filter, appended to the query as sourcelang:VALUE.; `query` (string, **required**) — GDELT query string. Same syntax as gdelt-search's query.; `timespan` (string, optional) — Relative time window ending now, e.g. 1h, 2d, 1w, 3m. Cannot be combined with from/to.; `to` (string, optional) — End of an absolute time window. Same formats as from.

### `gdelt_tv_concept_entities`

- **HTTP:** `GET /gdelt/tv-concept-entities`
- **What:** List GDELT Television 2.0 AI concept entities. Lists the Google Knowledge Graph concept entities GDELT recognises in US television captioning, most frequent first, up to `limit` entries (default 100, max 10000). Each has a display `label` and a `mid` code. Pass the `mid`, not the label, as `concept` to the GDELT TV search and chart endpoints. The list does not depend on any query.
- **Params:** `limit` (integer, optional) — Maximum entries to return, most-frequent first.

### `gdelt_tv_search`

- **HTTP:** `GET /gdelt/tv-search`
- **What:** Search US television news coverage (transcripts, captions, OCR, visual labels). Searches GDELT's US television news index on one required `station` (`CNN`, `MSNBC`, `FOXNEWS`, `BBCNEWS`, `KGO`, `KPIX` or `KNTV`). Match on `transcript`, `caption`, `concept`, `onscreen_text` or `visual`, with matching `exclude_` options. Returns up to `maxrecords` clips (default 50, max 3000) with show, station, timing, caption, transcript, onscreen text and clip URL. Results lag 24 to 48 hours.
- **Params:** `caption` (array, optional) — Search human-provided closed captioning (GDELT's cap: operator). Repeatable; multiple values are OR'd together.; `concept` (array, optional) — Search Google Knowledge Graph concepts extracted from captioning, by MID code (GDELT's capnlp: operator). Repeatable; multiple values are OR'd together.; `day_of_week` (integer, optional) — Limit to a day of week, 0 (Sunday) through 7 (Saturday), PST.; `exclude_caption` (array, optional) — Exclude clips whose closed captioning matches this value (GDELT's -cap: operator). Repeatable; every value must be absent.; `exclude_concept` (array, optional) — Exclude clips whose extracted concepts match this MID code (GDELT's -capnlp: operator). Repeatable; every value must be absent.; `exclude_onscreen_text` (array, optional) — Exclude clips whose OCR'd onscreen text matches this value (GDELT's -ocr: operator). Repeatable; every value must be absent.; `exclude_transcript` (array, optional) — Exclude clips whose speech-to-text transcript matches this value (GDELT's -asr: operator). Repeatable; every value must be absent.; `exclude_visual` (array, optional) — Exclude clips whose visual labels match this value (GDELT's -visual: operator). Repeatable; every value must be absent.; `from` (string, optional) — Start of an absolute time window. Accepts YYYY-MM-DD, RFC3339, or GDELT's raw YYYYMMDDHHMMSS. Cannot be combined with timespan.; `maxrecords` (integer, optional) — Rows to return. GDELT's own hard cap is 3000 for this endpoint; there is no pagination cursor beyond it.; `onscreen_text` (array, optional) — Search OCR'd onscreen text/chyrons (GDELT's ocr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `show` (string, optional) — Limit to an exact show name.; `sort` (string, optional) — Result order.; `station` (string, **required**) — Station to search.; `timespan` (string, optional) — Relative time window ending now, e.g. 1h, 7d, 3m, 1y. Cannot be combined with from/to. GDELT's TV archive starts July 6, 2010.; `to` (string, optional) — End of an absolute time window. Same formats as from.; `transcript` (array, optional) — Search machine-generated speech-to-text transcripts (GDELT's asr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `visual` (array, optional) — Search visual object/activity labels from computer vision (GDELT's visual: operator). Repeatable; multiple values are OR'd together.

### `gdelt_tv_showchart`

- **HTTP:** `GET /gdelt/tv-showchart`
- **What:** Top US television shows by coverage share for a query. Ranks US television shows by how much they covered a topic. At least one `station` is required, and a match is set with `transcript`, `caption`, `concept`, `onscreen_text` or `visual` (with `exclude_` counterparts), optionally limited by `show`, `timespan` or `from` and `to`. Returns shows with a `count`. Omitting the time window searches the archive back to July 2010.
- **Params:** `caption` (array, optional) — Search human-provided closed captioning (GDELT's cap: operator). Repeatable; multiple values are OR'd together.; `concept` (array, optional) — Search Google Knowledge Graph concepts extracted from captioning, by MID code (GDELT's capnlp: operator). Repeatable; multiple values are OR'd together.; `exclude_caption` (array, optional) — Exclude clips whose closed captioning matches this value (GDELT's -cap: operator). Repeatable; every value must be absent.; `exclude_concept` (array, optional) — Exclude clips whose extracted concepts match this MID code (GDELT's -capnlp: operator). Repeatable; every value must be absent.; `exclude_onscreen_text` (array, optional) — Exclude clips whose OCR'd onscreen text matches this value (GDELT's -ocr: operator). Repeatable; every value must be absent.; `exclude_transcript` (array, optional) — Exclude clips whose speech-to-text transcript matches this value (GDELT's -asr: operator). Repeatable; every value must be absent.; `exclude_visual` (array, optional) — Exclude clips whose visual labels match this value (GDELT's -visual: operator). Repeatable; every value must be absent.; `from` (string, optional) — Start of an absolute time window. Accepts YYYY-MM-DD, RFC3339, or GDELT's raw YYYYMMDDHHMMSS. Cannot be combined with timespan.; `onscreen_text` (array, optional) — Search OCR'd onscreen text/chyrons (GDELT's ocr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `show` (string, optional) — Limit to an exact show name.; `station` (array, **required**) — Required, repeatable. One or more stations, OR'd together.; `timespan` (string, optional) — Relative time window ending now, e.g. 1h, 7d, 3m, 1y. Cannot be combined with from/to. Omit both for GDELT's full archive (auto-resolution, back to July 6, 2010).; `to` (string, optional) — End of an absolute time window. Same formats as from.; `transcript` (array, optional) — Search machine-generated speech-to-text transcripts (GDELT's asr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `visual` (array, optional) — Search visual object/activity labels from computer vision (GDELT's visual: operator). Repeatable; multiple values are OR'd together.

### `gdelt_tv_stationchart`

- **HTTP:** `GET /gdelt/tv-stationchart`
- **What:** Compare US television news coverage across stations. Compares how much each US television station covered a topic. At least one `station` is required, and several are compared side by side. A match is set with `transcript`, `caption`, `concept`, `onscreen_text` or `visual` (with `exclude_` counterparts), optionally limited by `show`, `timespan` or `from` and `to`. Returns each station with a `count`.
- **Params:** `caption` (array, optional) — Search human-provided closed captioning (GDELT's cap: operator). Repeatable; multiple values are OR'd together.; `concept` (array, optional) — Search Google Knowledge Graph concepts extracted from captioning, by MID code (GDELT's capnlp: operator). Repeatable; multiple values are OR'd together.; `exclude_caption` (array, optional) — Exclude clips whose closed captioning matches this value (GDELT's -cap: operator). Repeatable; every value must be absent.; `exclude_concept` (array, optional) — Exclude clips whose extracted concepts match this MID code (GDELT's -capnlp: operator). Repeatable; every value must be absent.; `exclude_onscreen_text` (array, optional) — Exclude clips whose OCR'd onscreen text matches this value (GDELT's -ocr: operator). Repeatable; every value must be absent.; `exclude_transcript` (array, optional) — Exclude clips whose speech-to-text transcript matches this value (GDELT's -asr: operator). Repeatable; every value must be absent.; `exclude_visual` (array, optional) — Exclude clips whose visual labels match this value (GDELT's -visual: operator). Repeatable; every value must be absent.; `from` (string, optional) — Start of an absolute time window. Accepts YYYY-MM-DD, RFC3339, or GDELT's raw YYYYMMDDHHMMSS. Cannot be combined with timespan.; `onscreen_text` (array, optional) — Search OCR'd onscreen text/chyrons (GDELT's ocr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `show` (string, optional) — Limit to an exact show name.; `station` (array, **required**) — Required, repeatable. One or more stations, OR'd together.; `timespan` (string, optional) — Relative time window ending now, e.g. 1h, 7d, 3m, 1y. Cannot be combined with from/to. Omit both for GDELT's full archive (auto-resolution, back to July 6, 2010).; `to` (string, optional) — End of an absolute time window. Same formats as from.; `transcript` (array, optional) — Search machine-generated speech-to-text transcripts (GDELT's asr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `visual` (array, optional) — Search visual object/activity labels from computer vision (GDELT's visual: operator). Repeatable; multiple values are OR'd together.

### `gdelt_tv_stationdetails`

- **HTTP:** `GET /gdelt/tv-stationdetails`
- **What:** List GDELT Television 2.0 AI stations. Lists the television stations GDELT currently monitors, each with its `id`, short `label` and a `label_long` that includes its coverage dates. Use the ids as `station` in the GDELT TV endpoints. It takes no parameters.
- **Params:** _none_

### `gdelt_tv_timeline`

- **HTTP:** `GET /gdelt/tv-timeline`
- **What:** Airtime volume over time for US television news coverage. Returns the amount of US television news airtime matching the supplied query over time, using GDELT Television 2.0 AI timeline-volume data. A station is required. Supports the same caption, transcript, concept, and visual match operators as gdelt-tv-search; coverage and processing-delay caveats are documented there.
- **Params:** `caption` (array, optional) — Search human-provided closed captioning (GDELT's cap: operator). Repeatable; multiple values are OR'd together.; `concept` (array, optional) — Search Google Knowledge Graph concepts extracted from captioning, by MID code (GDELT's capnlp: operator). Repeatable; multiple values are OR'd together.; `exclude_caption` (array, optional) — Exclude clips whose closed captioning matches this value (GDELT's -cap: operator). Repeatable; every value must be absent.; `exclude_concept` (array, optional) — Exclude clips whose extracted concepts match this MID code (GDELT's -capnlp: operator). Repeatable; every value must be absent.; `exclude_onscreen_text` (array, optional) — Exclude clips whose OCR'd onscreen text matches this value (GDELT's -ocr: operator). Repeatable; every value must be absent.; `exclude_transcript` (array, optional) — Exclude clips whose speech-to-text transcript matches this value (GDELT's -asr: operator). Repeatable; every value must be absent.; `exclude_visual` (array, optional) — Exclude clips whose visual labels match this value (GDELT's -visual: operator). Repeatable; every value must be absent.; `from` (string, optional) — Start of an absolute time window. Accepts YYYY-MM-DD, RFC3339, or GDELT's raw YYYYMMDDHHMMSS. Cannot be combined with timespan.; `onscreen_text` (array, optional) — Search OCR'd onscreen text/chyrons (GDELT's ocr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `show` (string, optional) — Limit to an exact show name.; `station` (string, **required**) — Station to search.; `timespan` (string, optional) — Relative time window ending now, e.g. 1h, 7d, 3m, 1y. Cannot be combined with from/to. Omit both for GDELT's full archive (auto-resolution, back to July 6, 2010).; `to` (string, optional) — End of an absolute time window. Same formats as from.; `transcript` (array, optional) — Search machine-generated speech-to-text transcripts (GDELT's asr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `visual` (array, optional) — Search visual object/activity labels from computer vision (GDELT's visual: operator). Repeatable; multiple values are OR'd together.

### `gdelt_tv_visual_entities`

- **HTTP:** `GET /gdelt/tv-visual-entities`
- **What:** List GDELT Television 2.0 AI visual entities. Lists the computer-vision object and activity labels GDELT recognises in US television video, most frequent first, up to `limit` entries (default 100, max 10000). The label itself is the value to pass as `visual` to the GDELT TV search and chart endpoints. The list does not depend on any query.
- **Params:** `limit` (integer, optional) — Maximum entries to return, most-frequent first.

### `gdelt_tv_wordcloud`

- **HTTP:** `GET /gdelt/tv-wordcloud`
- **What:** Word cloud for US television news coverage. Returns a frequency-ranked word cloud for US television coverage. `channel` is required and picks what is counted: `transcript`, `caption`, `concept`, `onscreen_text` or `visual`; `station` is also required. Match with the same channel options (with `exclude_` counterparts) and limit by `show`, `day_of_week`, `timespan` or `from` and `to`. Each word has a `label` and `count`.
- **Params:** `caption` (array, optional) — Search human-provided closed captioning (GDELT's cap: operator). Repeatable; multiple values are OR'd together.; `channel` (string, **required**) — Required. Which match channel to build a word cloud from.; `concept` (array, optional) — Search Google Knowledge Graph concepts extracted from captioning, by MID code (GDELT's capnlp: operator). Repeatable; multiple values are OR'd together.; `day_of_week` (string, optional) — Limit to a day of week, 0 (Sunday) through 7 (Saturday), PST.; `exclude_caption` (array, optional) — Exclude clips whose closed captioning matches this value (GDELT's -cap: operator). Repeatable; every value must be absent.; `exclude_concept` (array, optional) — Exclude clips whose extracted concepts match this MID code (GDELT's -capnlp: operator). Repeatable; every value must be absent.; `exclude_onscreen_text` (array, optional) — Exclude clips whose OCR'd onscreen text matches this value (GDELT's -ocr: operator). Repeatable; every value must be absent.; `exclude_transcript` (array, optional) — Exclude clips whose speech-to-text transcript matches this value (GDELT's -asr: operator). Repeatable; every value must be absent.; `exclude_visual` (array, optional) — Exclude clips whose visual labels match this value (GDELT's -visual: operator). Repeatable; every value must be absent.; `from` (string, optional) — Start of an absolute time window. Accepts YYYY-MM-DD, RFC3339, or GDELT's raw YYYYMMDDHHMMSS. Cannot be combined with timespan.; `onscreen_text` (array, optional) — Search OCR'd onscreen text/chyrons (GDELT's ocr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `show` (string, optional) — Limit to an exact show name.; `station` (string, **required**) — Required. Station to search.; `timespan` (string, optional) — Relative time window ending now, e.g. 1h, 7d, 3m, 1y. Cannot be combined with from/to. GDELT's TV archive starts July 6, 2010.; `to` (string, optional) — End of an absolute time window. Same formats as from.; `transcript` (array, optional) — Search machine-generated speech-to-text transcripts (GDELT's asr: operator). Repeatable; multiple values are OR'd together. Short phrases only (GDELT caps each at 5 words).; `visual` (array, optional) — Search visual object/activity labels from computer vision (GDELT's visual: operator). Repeatable; multiple values are OR'd together.

## BBC (5)

### `bbc_article`

- **HTTP:** `GET /bbc/article`
- **What:** Get BBC News article content. Returns a BBC News article's public metadata and body paragraphs from a canonical article URL. Live pages are not supported.
- **Params:** `url` (string, **required**) — Canonical BBC News article URL

### `bbc_author`

- **HTTP:** `GET /bbc/author`
- **What:** Get a BBC News correspondent's profile. Returns a BBC News correspondent's profile from `url`, a canonical `bbc.co.uk/news/correspondents/<slug>` address: name, short `bio` and recent articles with title, URL, section and publication date when the page shows one. `published_at` is `YYYY-MM-DD` when the page gives a full date; items labelled only with a relative time, such as `2 days ago`, come back as written.
- **Params:** `url` (string, **required**) — Canonical BBC News correspondent URL

### `bbc_headlines`

- **HTTP:** `GET /bbc/headlines`
- **What:** Get BBC News section headlines. Returns fresh BBC News headlines for one section, `world` by default. `section` can be `all`, `world`, `uk`, `politics`, `business`, `health`, `science_and_environment`, `technology` or `entertainment_and_arts`; `all` can mix stories from several sections. Each item has a title, URL, summary and publication time when available.
- **Params:** `section` (string, optional) — BBC News RSS section, defaults to world

### `bbc_live`

- **HTTP:** `GET /bbc/live`
- **What:** Get a BBC News live-page text snapshot. Returns the current server-rendered text updates from one canonical BBC News live URL. It does not subscribe to updates or return broadcast, player, or stream data.
- **Params:** `url` (string, **required**) — Canonical BBC News live URL

### `bbc_search`

- **HTTP:** `GET /bbc/search`
- **What:** Search public BBC pages. Returns a bounded page of public BBC search-result metadata: title, URL, standfirst summary, display date, and a type of article, video, audio, live, topic, or page. Topic items are BBC topic hub pages rather than articles and carry no published_at. Media entries link only to their BBC landing pages; streams, downloads, and transcripts are not returned.
- **Params:** `page` (integer, optional) — Results page, defaults to 1; `q` (string, **required**) — Search query, up to 120 characters

## CNN (4)

### `cnn_article`

- **HTTP:** `GET /cnn/article`
- **What:** CNN article content. Returns a CNN article's headline, description, author, publication and update times, section, image, and body paragraphs. Provide a canonical cnn.com article URL.
- **Params:** `url` (string, **required**) — Canonical cnn.com article URL

### `cnn_author`

- **HTTP:** `GET /cnn/author`
- **What:** CNN profile page. Returns one CNN profile's byline metadata (name and title), bio paragraphs, social accounts, and recent articles/videos. Provide either a profile slug or a canonical cnn.com/profiles/<slug> URL.
- **Params:** `slug` (string, optional) — CNN profile slug, e.g. jake-tapper-profile (a slug without the -profile suffix is tried with it first, then as-is); `url` (string, optional) — Canonical cnn.com/profiles/<slug> URL, as an alternative to slug

### `cnn_headlines`

- **HTTP:** `GET /cnn/headlines`
- **What:** CNN section headlines. Returns the current CNN headline stream for one section, including title, article URL, description, publication time, and image when available.
- **Params:** `section` (string, optional) — CNN section. Allowed values: world, us, politics, business, health, entertainment, style, travel, sports, science, climate, weather, opinion. Default world.

### `cnn_live_story`

- **HTTP:** `GET /cnn/live-story`
- **What:** CNN live story updates. Returns a CNN live story from its canonical cnn.com live-news `url`: title, description, last update time and the posts in chronological order. Each post has an id, title, paragraphs of text, and published and updated times.
- **Params:** `url` (string, **required**) — Canonical cnn.com live-news URL

## Guardian (4)

### `guardian_article`

- **HTTP:** `GET /guardian/article`
- **What:** Get Guardian article content. Returns a Guardian article by `url`, a canonical `www.theguardian.com` article link. The response has the title, description, section, authors, lead image, publication and update times, and the body as `paragraphs`. Live-blog timelines are not supported.
- **Params:** `url` (string, **required**) — Canonical www.theguardian.com article URL

### `guardian_author`

- **HTTP:** `GET /guardian/author`
- **What:** Get Guardian contributor profile. Returns one Guardian contributor's public profile: name, bio, Twitter handle, byline image, and one page of their recent articles. Provide either the contributor's profile slug or the full profile page URL.
- **Params:** `page` (integer, optional) — 1-based article-history page, 1 to 100, defaults to 1; `slug` (string, optional) — Guardian contributor profile slug, e.g. hannah-devlin; `url` (string, optional) — Canonical https://www.theguardian.com/profile/<slug> page URL, as an alternative to slug

### `guardian_headlines`

- **HTTP:** `GET /guardian/headlines`
- **What:** Get Guardian section headlines. Returns recent Guardian headlines for one section. `section` is optional and defaults to `world`; the other values are `uk-news`, `us-news`, `politics`, `business`, `technology`, `environment`, `science`, `sport`, `culture`, `lifeandstyle` and `commentisfree`. Each item has a title, URL, summary, publication time and author, plus its section when available.
- **Params:** `section` (string, optional) — Guardian RSS section, defaults to world

### `guardian_topic`

- **HTTP:** `GET /guardian/topic`
- **What:** Get Guardian topic archive. Returns the stories on a public Guardian tag archive (20 per page, newest first, with total pages and results) or section front (a single curated page, is_front true). topic is a Guardian tag or section slug and page defaults to 1. resolved_topic reports the path actually served, which differs for edition-scoped fronts.
- **Params:** `page` (integer, optional) — 1-based archive page, 1 to 100, defaults to 1; `topic` (string, **required**) — Guardian tag or section slug

## Yahoo News (7)

### `yahoo_news_article`

- **HTTP:** `GET /yahoo-news/article`
- **What:** Yahoo News article content. Returns a single Yahoo News article's full content: headline, description, author, publish/update time, section, image, keywords, original publisher, and body paragraphs. Accepts a canonical yahoo.com/news article URL, such as one returned by the home or category story streams.
- **Params:** `url` (string, **required**) — Canonical www.yahoo.com/news article URL

### `yahoo_news_category`

- **HTTP:** `GET /yahoo-news/category`
- **What:** Yahoo News section story stream. Returns a Yahoo News section's story stream: title, destination URL, summary, source, publish time, comment count, and thumbnail images for each story. Sourced from Yahoo News's own server-rendered section pages.
- **Params:** `category` (string, **required**) — Yahoo News section

### `yahoo_news_comment_replies`

- **HTTP:** `GET /yahoo-news/comments/replies`
- **What:** Yahoo News comment replies. Returns a page of a comment's replies: author, body, reaction counts, and pin status, with sort order and cursor-based pagination. Sourced from Yahoo's own comment platform gateway.
- **Params:** `comment_id` (string, **required**) — Parent comment id (the id field returned by /yahoo-news/comments); `content_id` (string, **required**) — Article id (the id field returned by home/category/article); `count` (integer, optional) — Number of replies to return, default 10, clamped to 1..50; `cursor` (string, optional) — Pagination cursor from a previous response's next_cursor; `sort` (string, optional) — Sort order, defaults to newest

### `yahoo_news_comments`

- **HTTP:** `GET /yahoo-news/comments`
- **What:** Yahoo News article comments. Returns a page of an article's top-level comments: author, body, reaction counts, reply count, and pin status, with sort order and cursor-based pagination. Sourced from Yahoo's own comment platform gateway.
- **Params:** `content_id` (string, **required**) — Article id (the id field returned by home/category/article); `count` (integer, optional) — Number of comments to return, default 10, clamped to 1..50; `cursor` (string, optional) — Pagination cursor from a previous response's next_cursor; `sort` (string, optional) — Sort order, defaults to top

### `yahoo_news_home`

- **HTTP:** `GET /yahoo-news/home`
- **What:** Yahoo News homepage story stream. Returns Yahoo News's homepage "need to know" story stream: title, destination URL, summary, source, publish time, comment count, and thumbnail images for each story. Sourced from Yahoo News's own server-rendered homepage.
- **Params:** _none_

### `yahoo_news_related`

- **HTTP:** `GET /yahoo-news/related`
- **What:** Yahoo News related articles. Returns a page of articles Yahoo recommends alongside a given article -- the "you may also like" strip at the bottom of an article page -- with cursor-based pagination. Sourced from Yahoo's own recommendation gateway.
- **Params:** `content_id` (string, **required**) — Article id (the id field returned by home/category/article); `count` (integer, optional) — Number of related articles to return, default 10, clamped to 1..50; `cursor` (string, optional) — Pagination cursor from a previous response's next_cursor

### `yahoo_news_suggest`

- **HTTP:** `GET /yahoo-news/suggest`
- **What:** Yahoo News search autocomplete suggestions. Returns Yahoo News search-box autocomplete suggestions for the required partial query `q`, as a flat list of suggested news search terms in `suggestions`. `count` sets how many (default 10, clamped to 1 to 20). A query with no matches returns an empty array, not an error. The response also has `query` and `fetched_at`.
- **Params:** `count` (integer, optional) — Number of suggestions to return, default 10, clamped to 1..20; `q` (string, **required**) — Partial search query to autocomplete
