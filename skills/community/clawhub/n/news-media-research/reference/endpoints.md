# news-media-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**990 endpoints across 205 platform group(s).**

## Al Jazeera (5)

### `aljazeera_article`

- **HTTP:** `GET /aljazeera/article`
- **What:** Get Al Jazeera article content. Returns an Al Jazeera article by `url`, a canonical dated `www.aljazeera.com` address such as `/news/2026/9/20/example-slug`: title, description, publication and update times, section, credited authors, lead image and body `paragraphs`. Live-blog URLs return their opening summary bullets as the body; a video page with no article text returns `503` and a malformed URL `400`.
- **Params:** `url` (string, **required**) — Canonical www.aljazeera.com article URL

### `aljazeera_author`

- **HTTP:** `GET /aljazeera/author`
- **What:** Get an Al Jazeera author's profile and recent articles. Returns one Al Jazeera author's public profile (name, job title, bio when available) and one page of their recent articles, identified by an author slug or a canonical author URL.
- **Params:** `page` (integer, optional) — 1-based page number of the author's article list; overrides any page embedded in url; `slug` (string, optional) — Al Jazeera author slug; `url` (string, optional) — Canonical https://www.aljazeera.com/author/<slug> URL, as an alternative to slug

### `aljazeera_categories`

- **HTTP:** `GET /aljazeera/categories`
- **What:** Get Al Jazeera section navigation. Lists Al Jazeera's current section navigation, each entry with a `name`, `slug` and `url`. A slug has one segment (`news`, `middle-east`) or two (`tag/human-rights`), and any returned `slug` can be passed as the `topic` parameter of `aljazeera-topic`.
- **Params:** _none_

### `aljazeera_headlines`

- **HTTP:** `GET /aljazeera/headlines`
- **What:** Get Al Jazeera site-wide headlines. Returns recent Al Jazeera text-news headlines from across the site, with no input needed. Each item has a title, canonical URL, summary, publication time and the section when present. Video items are excluded because the article endpoint supports text stories only.
- **Params:** _none_

### `aljazeera_topic`

- **HTTP:** `GET /aljazeera/topic`
- **What:** Get Al Jazeera section headlines. Returns the newest public Al Jazeera stories from one section archive page. topic is a section slug; use aljazeera-categories for the current value space.
- **Params:** `topic` (string, **required**) — Al Jazeera section slug

## Axios (3)

### `axios_article`

- **HTTP:** `GET /axios/article`
- **What:** Get Axios article content. Returns a public Axios article's metadata and full body paragraphs from a canonical article URL. Subscriber-only stories with no free preview return a 403 permission error instead of an empty body.
- **Params:** `url` (string, **required**) — Canonical www.axios.com article URL

### `axios_categories`

- **HTTP:** `GET /axios/categories`
- **What:** Get Axios topic navigation. Returns Axios's full public topic and subtopic navigation tree. Use a subtopic's topic value directly as the topic parameter on axios-headlines.
- **Params:** _none_

### `axios_headlines`

- **HTTP:** `GET /axios/headlines`
- **What:** Get Axios topic headlines. Returns the newest public Axios stories on one topic or subtopic page. topic is a topic slug (e.g. technology) or a topic/subtopic path (e.g. technology/automation-and-ai) -- see axios-categories for the full known value space.
- **Params:** `topic` (string, **required**) — Axios topic slug or topic/subtopic path

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

## Bloomberg (6)

### `bloomberg_article`

- **HTTP:** `GET /bloomberg/article`
- **What:** Get a Bloomberg article's content. Returns a public Bloomberg article by `url`: title, description, publication and update times, section, categories, authors, image, `is_premium` and the body `paragraphs` in order. Subscriber-only articles that Bloomberg shows as a truncated preview return `403`, an article with no body returns `503`, and non-article or non-Bloomberg URLs return `400`.
- **Params:** `url` (string, **required**) — Canonical Bloomberg article URL

### `bloomberg_author`

- **HTTP:** `GET /bloomberg/author`
- **What:** Get a Bloomberg author's profile. Returns a Bloomberg author's profile from `url`, a canonical `https://www.bloomberg.com/authors/<id>/<slug>` address, where `<id>` is an opaque token Bloomberg assigns and cannot be guessed. The response has `name`, `title`, `bio` and recent content with title, URL, `type`, `section`, full `byline` and publication and update times.
- **Params:** `url` (string, **required**) — Canonical Bloomberg author URL

### `bloomberg_categories`

- **HTTP:** `GET /bloomberg/categories`
- **What:** List Bloomberg editorial categories. Lists Bloomberg's public editorial navigation categories discovered from its embedded navigation state. Each returned section slug is accepted by /bloomberg/headlines; product, account, newsletter, and sponsored-content links are excluded.
- **Params:** _none_

### `bloomberg_headlines`

- **HTTP:** `GET /bloomberg/headlines`
- **What:** Get the latest stories in a Bloomberg section. Returns current Bloomberg story cards for one editorial section. `section` is required and takes a slug from the Bloomberg categories list, such as `markets`, `economics` or `politics`. Each item has a title and canonical URL, and may also carry a description, image and publication time.
- **Params:** `section` (string, **required**) — Section slug from /bloomberg/categories

### `bloomberg_news`

- **HTTP:** `GET /bloomberg/news`
- **What:** Get the latest Bloomberg stories. Returns Bloomberg's current news feed: the newest stories across all sections, each with its title, canonical URL, and publication time.
- **Params:** _none_

### `bloomberg_news_sitemaps`

- **HTTP:** `GET /bloomberg/news-sitemaps`
- **What:** List Bloomberg monthly news sitemaps. Lists Bloomberg's monthly news sitemaps, each with its `url` and `last_modified` date. Use them to find historical news beyond the rolling latest feed at `/bloomberg/news`. Takes no parameters.
- **Params:** _none_

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

## FT (6)

### `ft_article`

- **HTTP:** `GET /ft/article`
- **What:** Get a Financial Times article's content. Returns one public Financial Times article's metadata and body paragraphs from a canonical article URL. Subscriber-only articles that the FT serves as a subscription page are not available.
- **Params:** `url` (string, **required**) — Canonical FT article URL

### `ft_author`

- **HTTP:** `GET /ft/author`
- **What:** Get an FT author profile. Returns one Financial Times contributor's public byline profile (name, job title, email, social accounts) plus one page of their recent articles. FT author pages carry no bio paragraph, only this byline metadata.
- **Params:** `page` (integer, optional) — 1-based page number of the author's article list; `slug` (string, optional) — Author URL slug, e.g. martin-wolf; `url` (string, optional) — Canonical www.ft.com/<slug> author URL; alternative to slug

### `ft_categories`

- **HTTP:** `GET /ft/categories`
- **What:** List Financial Times sections. Lists every Financial Times section accepted by /ft/headlines, grouped by top-level section, with each section's slug, display name, and landing-page URL.
- **Params:** _none_

### `ft_headlines`

- **HTTP:** `GET /ft/headlines`
- **What:** Get the latest stories in a Financial Times section. Returns one page of a Financial Times section front: each story's title, canonical URL, summary, section tag, publication time, and lead image. Section must be a slug returned by /ft/categories.
- **Params:** `page` (integer, optional) — Results page; `section` (string, **required**) — Section slug from /ft/categories

### `ft_news`

- **HTTP:** `GET /ft/news`
- **What:** Get the latest Financial Times stories. Returns the Financial Times' current news feed: the newest stories across all sections, each with its title, canonical URL, and publication time.
- **Params:** _none_

### `ft_search`

- **HTTP:** `GET /ft/search`
- **What:** Search Financial Times articles. Returns one page of Financial Times search results: each story's title, canonical URL, summary, section tag, publication time, and lead image. Results can be ordered by relevance or date and filtered by publication window.
- **Params:** `date_range` (string, optional) — Publication-window filter; `page` (integer, optional) — Results page; `q` (string, **required**) — Search keywords; `sort` (string, optional) — Result ordering

## ForeignAffairs (5)

### `foreignaffairs_article`

- **HTTP:** `GET /foreignaffairs/article`
- **What:** Extract a Foreign Affairs article. Returns public article metadata and ordered body paragraphs from a canonical Foreign Affairs article URL. Incomplete, truncated, challenge, or contaminated upstream HTML is rejected as an upstream error.
- **Params:** `url` (string, **required**) — Canonical Foreign Affairs article URL

### `foreignaffairs_author`

- **HTTP:** `GET /foreignaffairs/author`
- **What:** Get a Foreign Affairs author profile. Returns one Foreign Affairs contributor's public profile: name, bio, and the recent articles listed on their contributor page. Foreign Affairs does not paginate this page; it shows a fixed recent-article list.
- **Params:** `slug` (string, optional) — Author slug, e.g. robert-kagan; `url` (string, optional) — Canonical foreignaffairs.com/authors/<slug> URL; alternative to slug

### `foreignaffairs_headlines`

- **HTTP:** `GET /foreignaffairs/headlines`
- **What:** Get Foreign Affairs site-wide headlines. Returns fresh Foreign Affairs headlines from the site's public, site-wide RSS feed. Article pages and account state are not required.
- **Params:** _none_

### `foreignaffairs_topic`

- **HTTP:** `GET /foreignaffairs/topic`
- **What:** Get a Foreign Affairs topic feed. Returns the newest items from one Foreign Affairs topic RSS feed. Discover accepted values with foreignaffairs-topics; unknown topic values are rejected before upstream I/O.
- **Params:** `topic` (string, **required**) — Foreign Affairs topic slug from foreignaffairs-topics

### `foreignaffairs_topics`

- **HTTP:** `GET /foreignaffairs/topics`
- **What:** List Foreign Affairs topic feeds. Lists the 19 Foreign Affairs topics accepted by the topic endpoint, such as `economics`, `nato`, `sanctions` and `us-foreign-policy`. Each topic has its `slug`, display name and RSS `feed_url`. It takes no parameters.
- **Params:** _none_

## ForeignPolicy (8)

### `foreignpolicy_article`

- **HTTP:** `GET /foreignpolicy/article`
- **What:** Get Foreign Policy article content. Returns a public Foreign Policy article's metadata and full body paragraphs from a canonical article URL. is_gated reports the site's own content-tier marker; the full body is always returned regardless, since Foreign Policy serves it in full to anonymous requests either way.
- **Params:** `url` (string, **required**) — Canonical foreignpolicy.com article URL

### `foreignpolicy_author`

- **HTTP:** `GET /foreignpolicy/author`
- **What:** Get a Foreign Policy author profile. Returns one Foreign Policy contributor's public profile: name, bio, and their recent articles. Further articles load behind a client-side control this endpoint does not follow, so this is the author page's initial recent-article list, not the contributor's full history.
- **Params:** `slug` (string, optional) — Author slug, e.g. anne-applebaum; `url` (string, optional) — Canonical foreignpolicy.com/author/<slug>/ URL; alternative to slug

### `foreignpolicy_headlines`

- **HTTP:** `GET /foreignpolicy/headlines`
- **What:** Get Foreign Policy site-wide headlines. Returns fresh headlines from Foreign Policy's public, site-wide RSS feed. There is no section parameter: use foreignpolicy-topic to scope to one category or tag.
- **Params:** _none_

### `foreignpolicy_live`

- **HTTP:** `GET /foreignpolicy/live`
- **What:** List Foreign Policy Live conversations. Returns Foreign Policy's public FP Live conversation directory. The upstream renders the complete all-conversations list and applies year filtering in the browser.
- **Params:** _none_

### `foreignpolicy_live_detail`

- **HTTP:** `GET /foreignpolicy/live-detail`
- **What:** Get a Foreign Policy Live conversation. Returns one public FP Live conversation by the slug returned by foreignpolicy-live, including its description and any embedded video highlight metadata.
- **Params:** `live` (string, **required**) — Foreign Policy FP Live conversation slug

### `foreignpolicy_project`

- **HTTP:** `GET /foreignpolicy/project`
- **What:** Get a Foreign Policy project hub. Returns a public Foreign Policy curated project hub and its current article cards. Use foreignpolicy-projects to discover live project slugs.
- **Params:** `project` (string, **required**) — Foreign Policy project slug

### `foreignpolicy_projects`

- **HTTP:** `GET /foreignpolicy/projects`
- **What:** List Foreign Policy project hubs. Returns one page of Foreign Policy's live public project directory. Follow next_page until it is zero to enumerate the current project slug space, then pass a slug to foreignpolicy-project.
- **Params:** `page` (integer, optional) — 1-based project-directory page, defaults to 1

### `foreignpolicy_topic`

- **HTTP:** `GET /foreignpolicy/topic`
- **What:** Get Foreign Policy category or tag archive. Returns one page of a public Foreign Policy category or tag archive (newest first). type selects the archive namespace and defaults to category; topic is the slug within it; page is 1-based.
- **Params:** `page` (integer, optional) — 1-based archive page, defaults to 1; `topic` (string, **required**) — Foreign Policy category or tag slug; `type` (string, optional) — Archive namespace, defaults to category

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

## Harvard Business Review (4)

### `hbr_article`

- **HTTP:** `GET /hbr/article`
- **What:** Get Harvard Business Review article content. Returns a public Harvard Business Review article's metadata and full body text from a canonical article URL. from_magazine flags articles originally published in the print magazine.
- **Params:** `url` (string, **required**) — Canonical hbr.org article URL

### `hbr_categories`

- **HTTP:** `GET /hbr/categories`
- **What:** Get Harvard Business Review topic taxonomy. Returns Harvard Business Review's full public topic taxonomy, grouped into Subject, Industry, and Geography. Use a topic's slug directly as the topic parameter on hbr-topic.
- **Params:** _none_

### `hbr_headlines`

- **HTTP:** `GET /hbr/headlines`
- **What:** Get Harvard Business Review latest headlines. Returns the latest items from Harvard Business Review's site-wide The Latest stream, with no parameters. Each item has its `title`, `url`, `summary`, `topic`, `content_type` (for example Digital Article), and `authors` and an `image_url` when available. Items carry no publication time.
- **Params:** _none_

### `hbr_topic`

- **HTTP:** `GET /hbr/topic`
- **What:** Get Harvard Business Review topic archive. Returns the newest public Harvard Business Review articles on one topic archive page. topic is a "<group>/<slug>" value -- see hbr-categories for the full known value space.
- **Params:** `topic` (string, **required**) — Harvard Business Review topic slug

## Los Angeles Times (4)

### `latimes_article`

- **HTTP:** `GET /latimes/article`
- **What:** Get Los Angeles Times article content. Returns a Los Angeles Times article's public metadata and body paragraphs from a canonical article URL, read from the page's NewsArticle structured data.
- **Params:** `url` (string, **required**) — Canonical Los Angeles Times article URL

### `latimes_author`

- **HTTP:** `GET /latimes/author`
- **What:** Get a Los Angeles Times author profile. Returns a Los Angeles Times author profile by `url`, a canonical `https://www.latimes.com/people/<slug>` link; other hosts or paths return a bad-request error. The response has the `name`, `job_title`, `bio`, `email`, `image_url`, `social_accounts` and recent articles with title, URL, summary, publication time and lead image. Accounts the page does not list are absent.
- **Params:** `url` (string, **required**) — Canonical Los Angeles Times author URL

### `latimes_headlines`

- **HTTP:** `GET /latimes/headlines`
- **What:** Get Los Angeles Times section headlines. Returns fresh headlines from a public Los Angeles Times section RSS feed: title, canonical URL, summary, author, publication time, and lead image. section defaults to main.
- **Params:** `section` (string, optional) — Section slug from latimes-sections, defaults to main

### `latimes_sections`

- **HTTP:** `GET /latimes/sections`
- **What:** List Los Angeles Times section feeds. Returns the complete set of section slugs accepted by latimes-headlines, each with its display name and public RSS feed URL.
- **Params:** _none_

## NPR (5)

### `npr_article`

- **HTTP:** `GET /npr/article`
- **What:** Get NPR article content. Returns an NPR article by canonical `url` in the form `https://www.npr.org/YYYY/MM/DD/...`: title, description, section, authors, lead image, publication and update times, and body `paragraphs`. Tracking query strings and fragments are ignored; other hosts, encoded paths and non-article paths are rejected.
- **Params:** `url` (string, **required**) — Canonical www.npr.org article URL

### `npr_author`

- **HTTP:** `GET /npr/author`
- **What:** Get an NPR author profile. Returns an NPR author profile from a required `url` in the form `https://www.npr.org/people/<id>/<slug>`. The response has `name`, `job_title`, `bio` and the recent stories listed under Stories By, each with title, URL, summary, publication date and a lead image where the card has one. Other hosts or paths return a bad-request error.
- **Params:** `url` (string, **required**) — Canonical www.npr.org author URL

### `npr_categories`

- **HTTP:** `GET /npr/categories`
- **What:** Get NPR section navigation. Lists the sections in NPR's current navigation, each with its name, slug and URL. Pass a returned `slug` as the `topic` parameter of `npr-topic`. The list is not a fixed set, so it follows whatever sections NPR currently shows.
- **Params:** _none_

### `npr_headlines`

- **HTTP:** `GET /npr/headlines`
- **What:** Get NPR site-wide headlines. Returns the current NPR headlines across the site, with no parameters and no section filter. Each item has a title, canonical URL, summary, publication time and author when one is given.
- **Params:** _none_

### `npr_topic`

- **HTTP:** `GET /npr/topic`
- **What:** Get NPR section headlines. Returns the newest public NPR stories from one section archive page. topic is a section slug; use npr-categories for the current value space.
- **Params:** `topic` (string, **required**) — NPR section slug

## New York Times (5)

### `nyt_article`

- **HTTP:** `GET /nyt/article`
- **What:** Get a New York Times article's content. Returns a New York Times article by canonical `url`, with `title`, `description`, `published_at`, `updated_at`, `section`, `authors`, `keywords`, `image_url` and the body `paragraphs` in order. Query strings and fragments are stripped. A subscription barrier returns `403`, and non-article or non-NYT URLs return `400`.
- **Params:** `url` (string, **required**) — Canonical NYT article URL

### `nyt_author`

- **HTTP:** `GET /nyt/author`
- **What:** Get a New York Times contributor profile. Returns one New York Times contributor's public byline page: name, tagline, About/Contact panels, and their recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical NYT author URL

### `nyt_categories`

- **HTTP:** `GET /nyt/categories`
- **What:** List New York Times navigation categories. Lists the public New York Times editorial navigation taxonomy, including top-level categories and nested destinations. Use /nyt/sections for the separately verified RSS-backed section values accepted by /nyt/headlines; product links, newsletters, and podcasts are not included as article categories.
- **Params:** _none_

### `nyt_headlines`

- **HTTP:** `GET /nyt/headlines`
- **What:** Get the latest stories in a New York Times section. Returns a New York Times section RSS feed: each story's title, canonical URL, description, author, publication time, and lead image. Section must be a slug returned by /nyt/sections.
- **Params:** `section` (string, **required**) — Section slug from /nyt/sections

### `nyt_sections`

- **HTTP:** `GET /nyt/sections`
- **What:** List New York Times sections. Lists the New York Times section slugs accepted by `nyt-headlines`, such as `World` and `Business`, each with its display `name` and `url`. It covers only the sections that endpoint takes; use `nyt-categories` for the broader site navigation, including Politics, DealBook and Wirecutter.
- **Params:** _none_

## Politico (5)

### `politico_article`

- **HTTP:** `GET /politico/article`
- **What:** Get Politico article content. Returns a Politico article by its canonical `url`, in the form `https://www.politico.com/news/YYYY/MM/DD/slug`. The response has the title, description, authors, publication and update times, lead image URL and the body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical www.politico.com article URL

### `politico_author`

- **HTTP:** `GET /politico/author`
- **What:** Get a Politico staff author profile. Returns one Politico staff author's public profile: name, job title, bio, headshot, and their most recent bylined articles. Politico staff pages expose a fixed-size recent-articles list with no pagination.
- **Params:** `slug` (string, optional) — Politico staff slug, e.g. mark-satter; `url` (string, optional) — Canonical www.politico.com/staff/<slug> URL, as an alternative to slug

### `politico_categories`

- **HTTP:** `GET /politico/categories`
- **What:** Get Politico section navigation. Returns Politico's full public section navigation tree, grouped the same way the site's own nav menu groups it. Use a section's slug directly as the topic parameter on politico-topic.
- **Params:** _none_

### `politico_headlines`

- **HTTP:** `GET /politico/headlines`
- **What:** Get Politico site-wide headlines. Returns the latest Politico stories across the whole site, not limited to one section. Takes no parameters. Each item has its title, URL, a short summary, publication time and author.
- **Params:** _none_

### `politico_topic`

- **HTTP:** `GET /politico/topic`
- **What:** Get Politico section archive. Returns the newest public Politico stories on one section archive page. topic is a section slug -- see politico-categories for the full known value space.
- **Params:** `topic` (string, **required**) — Politico section slug

## Reuters (6)

### `reuters_article`

- **HTTP:** `GET /reuters/article`
- **What:** Get a Reuters article's content. Returns one normal Reuters article's public metadata and body paragraphs from a canonical article URL. Live blogs, video and podcast pages, and subscriber-only or bot-challenged responses are not supported.
- **Params:** `url` (string, **required**) — Canonical Reuters article URL

### `reuters_articles`

- **HTTP:** `GET /reuters/articles`
- **What:** Get recent Reuters articles. Returns a page of recent Reuters articles: canonical URL, update time, and the lead image URL when available, plus the title when Reuters publishes one in this index (currently it does not). The index covers the most recent 10,000 articles. Use /reuters/news for a title-bearing feed of fresh stories, or /reuters/article for one article's title and text.
- **Params:** `page` (integer, optional) — Results page, 100 items per page

### `reuters_author`

- **HTTP:** `GET /reuters/author`
- **What:** Get a Reuters author profile. Returns a Reuters author's profile by canonical `url` (`https://www.reuters.com/authors/<slug>/`): name, company, editorial email, social accounts, profile image, `total_articles` and the first 20 recent articles, each with title, URL, summary, publication time and an image when the story card has one. Accounts the page does not list are absent.
- **Params:** `url` (string, **required**) — Canonical Reuters author URL

### `reuters_news`

- **HTTP:** `GET /reuters/news`
- **What:** Get fresh Reuters headlines. Returns fresh Reuters headlines with title, canonical URL, publication and update times, and the lead image when Reuters publishes one. Covers the most recent stories from Reuters' public news feed.
- **Params:** `page` (integer, optional) — Results page, 50 items per page

### `reuters_section`

- **HTTP:** `GET /reuters/section`
- **What:** Get recent articles in a Reuters section. Returns a page of one top-level Reuters section's recent articles: canonical URL, update time, lead image URL, and image caption. This feed does not publish titles; use /reuters/news for a title-bearing feed of fresh stories.
- **Params:** `page` (integer, optional) — Results page, 100 items per page; `section` (string, **required**) — Top-level Reuters section

### `reuters_sections`

- **HTTP:** `GET /reuters/sections`
- **What:** List Reuters sections. Lists the top-level Reuters sections accepted by the `section` parameter of `/reuters/section`, returned under `items`. Each entry has a `slug`, a display `name` and the landing-page `url`. Takes no parameters.
- **Params:** _none_

## Washington Post (5)

### `wapo_article`

- **HTTP:** `GET /wapo/article`
- **What:** Get a Washington Post article's content. Returns one public Washington Post article's metadata and body paragraphs from a canonical article URL. Metered articles that the site truncates are not available.
- **Params:** `url` (string, **required**) — Canonical Washington Post article URL

### `wapo_author`

- **HTTP:** `GET /wapo/author`
- **What:** Get a Washington Post staff author profile. Returns one Washington Post staff author's public profile: byline metadata, bio, contact/social links, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Washington Post people slug, e.g. adam-taylor; `url` (string, optional) — Canonical washingtonpost.com/people/<slug>/ URL, optionally with a ?page= query; alternative to slug

### `wapo_headlines`

- **HTTP:** `GET /wapo/headlines`
- **What:** Get the latest stories in a Washington Post section. Returns the first page of a Washington Post section front: each story's title, canonical URL, description, section, publication time, and lead image. Section must be a path returned by /wapo/sections.
- **Params:** `section` (string, **required**) — Section path from /wapo/sections

### `wapo_news`

- **HTTP:** `GET /wapo/news`
- **What:** Get the latest Washington Post stories. Returns the current Washington Post news list with no parameters. Each item has its `title`, canonical `url`, `published_at` and `last_modified`, the last when the publisher supplies it. Items do not include summaries or authors.
- **Params:** _none_

### `wapo_sections`

- **HTTP:** `GET /wapo/sections`
- **What:** List Washington Post sections. Lists the Washington Post sections accepted by `wapo-headlines`. Each has a path `slug` such as `politics` or `business/technology`, a display `name` and a landing-page `url`. Use it to find valid `section` values. Takes no parameters.
- **Params:** _none_

## ABC News Australia (5)

### `abcau_article`

- **HTTP:** `GET /abcau/article`
- **What:** Get ABC News Australia article content. Returns an ABC News Australia article by `url`, a canonical `abc.net.au` address in the form `/news/<date>/<slug>/<id>`: title, description, publication time, section, authors, image and the body `paragraphs`. Rolling live-blog posts, whose slug ends `-live-blog`, return an error instead of partial content.
- **Params:** `url` (string, **required**) — Canonical ABC News Australia article URL

### `abcau_author`

- **HTTP:** `GET /abcau/author`
- **What:** Get an ABC News Australia author profile. Returns an ABC News Australia author profile from `url`, a canonical `https://www.abc.net.au/news/<slug>/<id>` address: name, `biography`, `image_url` and recent articles. Not every author has a headshot or biography, and wire or staff bylines often have neither.
- **Params:** `url` (string, **required**) — Canonical ABC News Australia author URL

### `abcau_headlines`

- **HTTP:** `GET /abcau/headlines`
- **What:** Get ABC News Australia section headlines. Returns current headlines for one ABC News Australia section. `section` is required and takes one of 15 slugs, including `justin`, `politics`, `rural`, `analysis-and-opinion` and `australia`. Each item has a title and URL, and may also carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — ABC News Australia section slug

### `abcau_news`

- **HTTP:** `GET /abcau/news`
- **What:** Get ABC News Australia top stories. Returns the current ABC News Australia top stories, with no input needed. Each item has a title and canonical URL, and may also carry a summary, author, publication time and image.
- **Params:** _none_

### `abcau_sections`

- **HTTP:** `GET /abcau/sections`
- **What:** Get ABC News Australia sections. Lists the 15 ABC News Australia section slugs accepted by `abcau-headlines`, from `justin` and `world` to `backstory` and `australia`. Each entry has a `slug`, a display `name` (for example `Just In`) and the section's page `url`.
- **Params:** _none_

## ABC News (5)

### `abcnews_article`

- **HTTP:** `GET /abcnews/article`
- **What:** Get ABC News article content. Returns public ABC News article metadata and body paragraphs from a canonical article URL. Accepts both the "story?id=..." and "wireStory/..." canonical URL shapes.
- **Params:** `url` (string, **required**) — Canonical ABC News article URL

### `abcnews_author`

- **HTTP:** `GET /abcnews/author`
- **What:** Get an ABC News author profile. Returns an ABC News author's profile: name, job title/biography when the page carries one, and social links, from a canonical author URL. Does not include a list of the author's recent articles.
- **Params:** `url` (string, **required**) — Canonical ABC News author URL

### `abcnews_headlines`

- **HTTP:** `GET /abcnews/headlines`
- **What:** Get ABC News section headlines. Returns the current headlines for one ABC News section. `section` is required and must be `us`, `world`, `politics`, `business`, `technology`, `entertainment`, `health` or `sports`. Each item has a title and URL, and may also carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — ABC News section slug

### `abcnews_news`

- **HTTP:** `GET /abcnews/news`
- **What:** Get ABC News top stories. Returns the current ABC News top stories, with no input needed. Each item has a title and canonical URL, and may also carry a summary, author, publication time and image.
- **Params:** _none_

### `abcnews_sections`

- **HTTP:** `GET /abcnews/sections`
- **What:** Get ABC News sections. Lists the 8 core ABC News sections that `abcnews-headlines` accepts: `us`, `world`, `politics`, `business`, `technology`, `entertainment`, `health` and `sports`. Each entry has a `slug`, a display `name` and the section's page `url`.
- **Params:** _none_

## AL.com (3)

### `alcom_headlines`

- **HTTP:** `GET /alcom/headlines`
- **What:** Get AL.com section headlines. Returns current headlines from one of AL.com's section feeds. Summaries are brief publisher teasers, not full article text.
- **Params:** `section` (string, **required**) — AL.com editorial section

### `alcom_news`

- **HTTP:** `GET /alcom/news`
- **What:** Get AL.com top stories. Returns current AL.com News stories. Summaries are brief publisher teasers, not full article text.
- **Params:** _none_

### `alcom_sections`

- **HTTP:** `GET /alcom/sections`
- **What:** Get AL.com editorial sections. Lists the three top-level editorial sections in AL.com's navigation: `news`, `sports` and `life`. Each has a `slug`, a display `name` and the section's page `url`, and the slugs are the values `alcom-headlines` accepts for `section`.
- **Params:** _none_

## Android Authority (4)

### `androidauthority_article`

- **HTTP:** `GET /androidauthority/article`
- **What:** Get Android Authority article content. Returns an Android Authority article by `url`, a canonical `androidauthority.com` address whose path is one slug ending in the numeric post id: title, description, publication and update times, section, authors, image and body `paragraphs`, with TL;DR and pros/cons bullets as separate entries. Section, tag and author pages are rejected, and an unknown post id returns not-found.
- **Params:** `url` (string, **required**) — Canonical Android Authority article URL

### `androidauthority_headlines`

- **HTTP:** `GET /androidauthority/headlines`
- **What:** Get Android Authority section headlines. Returns the newest 10 to 20 stories from one Android Authority section hub. `section` is required and takes a slug such as `reviews`, `how-to`, `smartwatches` or `android-phones`. Each item has a title, URL, author and image; `summary` appears on the lead story of a hub, and `published_at` only on stories more than a day old.
- **Params:** `section` (string, **required**) — Android Authority section slug

### `androidauthority_news`

- **HTTP:** `GET /androidauthority/news`
- **What:** Get Android Authority top stories. Returns about 80 of the latest Android Authority stories from across the site, newest first, with no input needed. Each has a title, canonical URL, standfirst `summary`, exact publication time, byline `author` and lead image. The headlines endpoint covers a single section.
- **Params:** _none_

### `androidauthority_sections`

- **HTTP:** `GET /androidauthority/sections`
- **What:** Get Android Authority sections. Lists the 44 Android Authority sections that `androidauthority-headlines` accepts: the content-type hubs (`news`, `reviews`, `best`, `how-to`, `features`, `deals`, `authority-insights`), the top-level topic hubs and their sub-hubs. Each has a `slug`, display `name` and page `url`. Tag archives are not sections.
- **Params:** _none_

## AP News (6)

### `apnews_article`

- **HTTP:** `GET /apnews/article`
- **What:** Get AP News article content. Returns public AP News article metadata and body paragraphs. The service does not bypass authentication or access controls. Billing is 2 credits, or 10 credits when browser rendering is required.
- **Params:** `url` (string, **required**) — Canonical AP News article URL

### `apnews_author`

- **HTTP:** `GET /apnews/author`
- **What:** Get an AP News author profile. Returns an AP News author's byline metadata, biography, and recent articles from a canonical author URL. The service does not bypass authentication or access controls. Billing is 1 credit, or 5 credits when browser rendering is required.
- **Params:** `url` (string, **required**) — Canonical AP News author URL

### `apnews_fact_check`

- **HTTP:** `GET /apnews/fact-check`
- **What:** Get AP News fact checks. Returns current headlines from AP News' public Fact Check page. The service does not bypass authentication or access controls. Billing is 1 credit, or 5 credits when browser rendering is required.
- **Params:** _none_

### `apnews_headlines`

- **HTTP:** `GET /apnews/headlines`
- **What:** Get AP News section headlines. Returns AP News headlines from a public editorial hub. The service does not bypass authentication or access controls. Billing is 1 credit, or 5 credits when browser rendering is required.
- **Params:** `section` (string, **required**) — AP News section slug

### `apnews_news`

- **HTTP:** `GET /apnews/news`
- **What:** Get AP News top stories. Returns AP News top stories from the public AP News Top News hub. The service does not bypass authentication or access controls. Billing is 1 credit, or 5 credits when browser rendering is required.
- **Params:** _none_

### `apnews_sections`

- **HTTP:** `GET /apnews/sections`
- **What:** Get AP News sections. Lists the 11 AP News hubs accepted by `apnews-headlines`: `ap-top-news`, `us-news`, `world-news`, `politics`, `business`, `technology`, `science`, `health`, `sports`, `entertainment` and `lifestyle`. Each has a `slug`, display `name` and hub `url`. The Fact Check page is served by `apnews-fact-check` instead.
- **Params:** _none_

## Ars Technica (5)

### `arstechnica_article`

- **HTTP:** `GET /arstechnica/article`
- **What:** Get Ars Technica article content. Returns public Ars Technica article metadata and body paragraphs from a canonical article URL. The service does not bypass authentication or access controls.
- **Params:** `url` (string, **required**) — Canonical Ars Technica article URL

### `arstechnica_author`

- **HTTP:** `GET /arstechnica/author`
- **What:** Get an Ars Technica contributor profile. Returns an Ars Technica contributor's byline metadata (name, job title, headshot, contact email), biography, and recent articles from a canonical author URL. The service does not bypass authentication or access controls.
- **Params:** `url` (string, **required**) — Canonical Ars Technica contributor URL

### `arstechnica_headlines`

- **HTTP:** `GET /arstechnica/headlines`
- **What:** Get Ars Technica section headlines. Returns recent Ars Technica headlines for one section. `section` is required and takes `ai`, `apple`, `cars`, `culture`, `features`, `gadgets`, `gaming`, `health`, `information-technology`, `reviews`, `science`, `security`, `space`, `staff` or `tech-policy`. Each item has a title and URL, and may also carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Ars Technica section slug

### `arstechnica_news`

- **HTTP:** `GET /arstechnica/news`
- **What:** Get Ars Technica top stories. Returns the latest Ars Technica stories, with no input needed. Each item has a title and canonical URL, and may also carry a summary, author, publication time and lead image.
- **Params:** _none_

### `arstechnica_sections`

- **HTTP:** `GET /arstechnica/sections`
- **What:** Get Ars Technica sections. Returns the Ars Technica section inventory: the site's own current navigation and RSS-feed-directory sections (AI, Gadgets, Science, Security, Space, and others), each linking to its public RSS feed.
- **Params:** _none_

## Barrons (4)

### `barrons_article`

- **HTTP:** `GET /barrons/article`
- **What:** Get a Barron's article's content. Returns one Barron's article's title, byline, section, publication time, word count, and body paragraphs, recovered from a public web-archive snapshot of the article. Barron's serves only the first paragraphs of an article at the origin, so an article is returned only when a full-text archive snapshot exists; an article without one returns 404.
- **Params:** `url` (string, **required**) — Canonical Barron's article URL

### `barrons_headlines`

- **HTTP:** `GET /barrons/headlines`
- **What:** Get the latest stories in a Barron's topic. Returns one page of a Barron's topic's headlines: each story's title, canonical URL, summary, publication time, authors, and lead image. Section must be a slug returned by /barrons/topics.
- **Params:** `page` (integer, optional) — Results page; `section` (string, **required**) — Barron's topic slug from /barrons/topics

### `barrons_news`

- **HTTP:** `GET /barrons/news`
- **What:** Get the latest Barron's stories. Returns Barron's current cross-section news feed: the newest stories across every section, each with its title, canonical URL, and publication time.
- **Params:** _none_

### `barrons_topics`

- **HTTP:** `GET /barrons/topics`
- **What:** List Barron's topics. Lists Barron's editorial topics, each with its `slug`, display `name` and landing-page `url`. The list is long and changes over time. Every `slug` is a valid `section` value for `/barrons/headlines`. Takes no parameters.
- **Params:** _none_

## Billboard (5)

### `billboard_article`

- **HTTP:** `GET /billboard/article`
- **What:** Get Billboard article content. Returns public Billboard article metadata and body paragraphs from a canonical article URL. Billboard Pro articles are returned in full when the public page serves the full body; a teaser-only page is flagged paywalled.
- **Params:** `url` (string, **required**) — Canonical Billboard article URL

### `billboard_author`

- **HTTP:** `GET /billboard/author`
- **What:** Get a Billboard author profile. Returns a Billboard author's byline metadata, biography, and recent articles (sourced from the author's own public RSS feed) from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical Billboard author URL

### `billboard_headlines`

- **HTTP:** `GET /billboard/headlines`
- **What:** Get Billboard section headlines. Returns the 10 most recent items from one Billboard section. `section` is required and takes a slug such as `chart-beat`, `country`, `rb-hip-hop`, `streaming` or `touring`. Parent sections such as `music` and `business` overlap with their subsections, so one item can appear under several. Items carry title, URL, summary, author and time.
- **Params:** `section` (string, **required**) — Billboard section slug

### `billboard_news`

- **HTTP:** `GET /billboard/news`
- **What:** Get Billboard top stories. Returns the latest Billboard stories, with no input needed. Each item has a title and canonical URL, plus a publication time, summary and image when Billboard provides them.
- **Params:** _none_

### `billboard_sections`

- **HTTP:** `GET /billboard/sections`
- **What:** Get Billboard sections. Returns the public Billboard section inventory: every music, business, culture, media and Spanish-language category plus Billboard Pro, each linking to its public RSS feed.
- **Params:** _none_

## Birmingham Mail (5)

### `birminghammail_article`

- **HTTP:** `GET /birminghammail/article`
- **What:** Get Birmingham Mail article content. Returns public Birmingham Mail article metadata (including the section) and body paragraphs from a canonical article URL. Photo-gallery URLs are rejected.
- **Params:** `url` (string, **required**) — Canonical Birmingham Mail article URL

### `birminghammail_author`

- **HTTP:** `GET /birminghammail/author`
- **What:** Get a Birmingham Mail author profile. Returns one Birmingham Mail author's public profile: name, job title, bio, email, X/Twitter handle, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page number of the author's article list (1 to 100); overrides any pageNumber in url; `slug` (string, optional) — Author slug, e.g. stephanie-balloo; `url` (string, optional) — Canonical birminghammail.co.uk/authors/<slug>/ URL; alternative to slug

### `birminghammail_headlines`

- **HTTP:** `GET /birminghammail/headlines`
- **What:** Get Birmingham Mail section headlines. Returns fresh headlines from one public Birmingham Mail section. Photo galleries are omitted because they have no readable article body.
- **Params:** `section` (string, **required**) — Birmingham Mail section slug

### `birminghammail_news`

- **HTTP:** `GET /birminghammail/news`
- **What:** Get Birmingham Mail top stories. Returns fresh Birmingham Mail top stories from the public home RSS feed. Photo galleries are omitted because they have no readable article body.
- **Params:** _none_

### `birminghammail_sections`

- **HTTP:** `GET /birminghammail/sections`
- **What:** Get Birmingham Mail sections. Lists the 23 Birmingham Mail sections that `birminghammail-headlines` accepts, such as `news/midlands-news`, `black-country`, `sport/football/transfer-news` and `whats-on`. Each has a `slug`, a display `name` and the feed `url`. Only sections with a recently updated feed are included (last verified 2026-09-25), and each returns up to about 25 entries.
- **Params:** _none_

## Bleacher Report (5)

### `bleacherreport_article`

- **HTTP:** `GET /bleacherreport/article`
- **What:** Get Bleacher Report article content. Returns public Bleacher Report article metadata and body paragraphs from a canonical article URL. Bleacher Report serves full articles to anonymous readers, so no article is paywalled.
- **Params:** `url` (string, **required**) — Canonical Bleacher Report article URL

### `bleacherreport_author`

- **HTTP:** `GET /bleacherreport/author`
- **What:** Get a Bleacher Report writer profile. Returns a Bleacher Report writer's profile, identified by `slug` (such as `scott-polacek`) or a canonical `bleacherreport.com/writers/<slug>` `url`; exactly one is required. The response has name, role, biography, photo and about 20 latest stories with title, URL and thumbnail. Publication times are not shown on the profile, so `published_at` is omitted; an unknown slug returns 404.
- **Params:** `slug` (string, optional) — Writer slug, e.g. scott-polacek; `url` (string, optional) — Canonical bleacherreport.com/writers/<slug> URL; alternative to slug

### `bleacherreport_headlines`

- **HTTP:** `GET /bleacherreport/headlines`
- **What:** Get Bleacher Report section headlines. Returns the stories on one Bleacher Report league or sub-hub page, newest first. `section` is required and takes a slug such as `nfl`, `nba-draft`, `formula-1` or `recruiting`. Each has a headline, article URL and publication time, plus thumbnail and blurb when present. Busy leagues return 100 or more stories, quiet ones only a few.
- **Params:** `section` (string, **required**) — Bleacher Report section slug

### `bleacherreport_news`

- **HTTP:** `GET /bleacherreport/news`
- **What:** Get Bleacher Report top stories. Returns around 180 Bleacher Report sports stories from roughly the last day or two, newest first, with no input needed. Each has a title, canonical article URL and publication time. Live blogs are excluded because they are not article pages.
- **Params:** _none_

### `bleacherreport_sections`

- **HTTP:** `GET /bleacherreport/sections`
- **What:** Get Bleacher Report sections. Lists the 30 Bleacher Report sections that `bleacherreport-headlines` accepts: 18 league and sport hubs such as `nfl`, `tennis` and `olympics`, plus 12 sub-hubs such as `nba-draft` and `bracketology`. Each has a `slug`, display `name` and landing-page `url`. Team pages, scores, standings and MotoGP are not included.
- **Params:** _none_

## Boston Globe (1)

### `bostonglobe_news`

- **HTTP:** `GET /bostonglobe/news`
- **What:** Get Boston Globe top stories. Returns recent Boston Globe story metadata and summaries. Article bodies, sections, headlines-by-section, and author profiles are not exposed, and some stories require a subscription.
- **Params:** _none_

## Breitbart (5)

### `breitbart_article`

- **HTTP:** `GET /breitbart/article`
- **What:** Get Breitbart article content. Returns a Breitbart article by `url`, a canonical `https://www.breitbart.com/<section>/<yyyy>/<mm>/<dd>/<slug>/` address. The response has the title, description, publication and update times, section, image, `authors` and the body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical Breitbart article URL

### `breitbart_author`

- **HTTP:** `GET /breitbart/author`
- **What:** Get a Breitbart author profile. Returns one Breitbart author/contributor's public profile: name, a short bio/role line when the page carries one, and their recent articles.
- **Params:** `page` (integer, optional) — 1-based page of articles to return; defaults to 1; `slug` (string, optional) — Author slug, e.g. joshua-klein; `url` (string, optional) — Canonical breitbart.com/author/<slug>/ URL, optionally with a /page/<n>/ segment; alternative to slug

### `breitbart_headlines`

- **HTTP:** `GET /breitbart/headlines`
- **What:** Get Breitbart section headlines. Returns current headlines from one Breitbart section hub. `section` is required and takes one of 21 slugs, such as `politics`, `border`, `the-media` or `europe`. The `world-news`, `news` and `on-the-hill-exclusive-video` hubs aggregate stories, so their links point to articles under whichever section owns each story.
- **Params:** `section` (string, **required**) — Breitbart section slug

### `breitbart_news`

- **HTTP:** `GET /breitbart/news`
- **What:** Get Breitbart top stories. Returns the latest Breitbart top stories from across the site, with no input needed. Each item has a title and canonical URL, and may also carry a summary, publication time, author and image.
- **Params:** _none_

### `breitbart_sections`

- **HTTP:** `GET /breitbart/sections`
- **What:** Get Breitbart sections. Lists the 21 Breitbart sections accepted by `breitbart-headlines`, including `politics`, `economy`, `border`, `national-security`, `the-media`, `world-news` and `america250`. Each has a `slug`, a display `name` and the section's page `url`. The list was verified on 2026-09-23.
- **Params:** _none_

## Business Insider (5)

### `businessinsider_article`

- **HTTP:** `GET /businessinsider/article`
- **What:** Get Business Insider article content. Returns a Business Insider article by canonical `url`: title, description, publication and update times, section, authors, image and the body `paragraphs`. Subscriber-only or blocked content returns an error instead of partial text.
- **Params:** `url` (string, **required**) — Canonical Business Insider article URL

### `businessinsider_author`

- **HTTP:** `GET /businessinsider/author`
- **What:** Get a Business Insider author profile. Returns a Business Insider author's profile, identified by `slug` (the last segment of the author's page address) or a canonical `https://www.businessinsider.com/author/<slug>` `url`; exactly one is required. The response has name, job title, bio, image, `social_accounts` and one page of recent articles with title, URL and summary. Accounts the author does not list are simply absent.
- **Params:** `slug` (string, optional) — Author slug; `url` (string, optional) — Canonical businessinsider.com/author/<slug> URL; alternative to slug

### `businessinsider_headlines`

- **HTTP:** `GET /businessinsider/headlines`
- **What:** Get Business Insider section headlines. Returns fresh headlines for one Business Insider section. `section` is required and is one of `business`, `markets`, `technology`, `politics`, `strategy`, `finance`, `science`, `lifestyle` or `reviews`. Each item has a title and URL, and may also carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Business Insider section slug

### `businessinsider_news`

- **HTTP:** `GET /businessinsider/news`
- **What:** Get Business Insider top stories. Returns the latest Business Insider top stories, with no input needed. Each item has a title and canonical URL, and may also carry a summary, author, publication time and image.
- **Params:** _none_

### `businessinsider_sections`

- **HTTP:** `GET /businessinsider/sections`
- **What:** Get Business Insider sections. Lists the Business Insider editorial sections accepted by `businessinsider-headlines`, such as `business`, `markets` and `technology`. Each entry has a stable `slug`, a display `name` and the section's page `url`.
- **Params:** _none_

## Business Standard (5)

### `businessstandard_article`

- **HTTP:** `GET /businessstandard/article`
- **What:** Get Business Standard article content. Returns public Business Standard article metadata and body paragraphs from a canonical article URL. A story Business Standard marks premium (subscriber-only) returns a permission error instead of a body.
- **Params:** `url` (string, **required**) — Canonical Business Standard article URL

### `businessstandard_author`

- **HTTP:** `GET /businessstandard/author`
- **What:** Get a Business Standard author profile. Returns a Business Standard author's profile from `url`, a canonical `https://www.business-standard.com/author/<slug>` address: name, designation, biography, image, and Twitter, Facebook, LinkedIn and YouTube links where listed, plus about 20 recent stories. Stories carry a title, URL and optionally summary, date and a `premium` flag for subscriber-only text. An unknown author returns `404`.
- **Params:** `url` (string, **required**) — Canonical Business Standard author URL

### `businessstandard_headlines`

- **HTTP:** `GET /businessstandard/headlines`
- **What:** Get Business Standard section headlines. Returns recent headlines for one Business Standard section: up to 35 stories, or 100 for `latest-news`. `section` is required and takes one of 25 slugs such as `companies`, `markets`, `cricket` or `todays-paper`. Some stories are premium (subscriber-only), and requesting one from the article endpoint returns `403`.
- **Params:** `section` (string, **required**) — Business Standard section slug

### `businessstandard_news`

- **HTTP:** `GET /businessstandard/news`
- **What:** Get Business Standard top stories. Returns Business Standard top stories from its home page, with no input needed: title, canonical URL and, where present, publication time, summary, author and image. Some listed stories are premium (subscriber-only), and requesting one from the article endpoint returns `403`.
- **Params:** _none_

### `businessstandard_sections`

- **HTTP:** `GET /businessstandard/sections`
- **What:** Get Business Standard sections. Lists the 25 Business Standard section slugs accepted by `businessstandard-headlines`, from `latest-news`, `companies` and `markets` to `cricket`, `immigration` and `todays-paper`. Each entry has a `slug`, a display `name` and the section's page `url`.
- **Params:** _none_

## CBC News (5)

### `cbc_article`

- **HTTP:** `GET /cbc/article`
- **What:** Get CBC News article content. Returns public CBC News or CBC Sports story metadata and body paragraphs from a canonical story URL. Live-updates pages are not supported.
- **Params:** `url` (string, **required**) — Canonical CBC News or CBC Sports story URL

### `cbc_author`

- **HTTP:** `GET /cbc/author`
- **What:** Get a CBC journalist profile. Returns a CBC journalist's profile, identified by `slug` (ending in CBC's author id, such as `darren-major-1.4462710`) or a `https://www.cbc.ca/author/<slug>` `url`; exactly one is required and an unknown author returns 404. The response has name, title, biography, photo, profile links and usually 10 latest articles, with `has_more_articles` showing whether older ones exist.
- **Params:** `slug` (string, optional) — Author slug, e.g. darren-major-1.4462710; `url` (string, optional) — Canonical https://www.cbc.ca/author/<slug> URL; alternative to slug

### `cbc_headlines`

- **HTTP:** `GET /cbc/headlines`
- **What:** Get CBC News section headlines. Returns fresh CBC News or CBC Sports headlines from one public section RSS feed. Video, radio, and live-updates links are omitted.
- **Params:** `section` (string, **required**) — CBC section slug

### `cbc_news`

- **HTTP:** `GET /cbc/news`
- **What:** Get CBC News top stories. Returns fresh CBC News top stories with no input needed: title, canonical story URL, publication time, byline when given and lead image. Only stories the article endpoint accepts are returned, so video player pages, CBC Radio, Music and Books links and live-updates pages are omitted.
- **Params:** _none_

### `cbc_sections`

- **HTTP:** `GET /cbc/sections`
- **What:** Get CBC News sections. Lists the 35 CBC News sections that `cbc-headlines` accepts: 8 national desks such as `politics` and `world`, 21 regional newsrooms such as `toronto` and `nova-scotia`, and 6 CBC Sports feeds such as `sports-nhl`. Each has a `slug`, a display `name` and the feed `url`. Top stories come from `cbc-news`, not a section.
- **Params:** _none_

## CBR (5)

### `cbr_article`

- **HTTP:** `GET /cbr/article`
- **What:** Get CBR article content. Returns a CBR article by `url`, a canonical `cbr.com` address of the form `/<slug>/`: title, description, publication and update times, section, authors, image and the body `paragraphs`. Section, video, author and category pages are rejected as invalid. `paywalled` is `true` only if the page declares the article not free, and then `paragraphs` may be a teaser.
- **Params:** `url` (string, **required**) — Canonical CBR article URL

### `cbr_author`

- **HTTP:** `GET /cbr/author`
- **What:** Get a CBR author profile. Returns a CBR author profile from `url`, a canonical `https://www.cbr.com/author/<slug>/` address; paginated `/page/N/` URLs are rejected. The response has name, `title`, biography, image, `social_links` and about 20 items from the profile's Latest module, with no older pages available.
- **Params:** `url` (string, **required**) — Canonical CBR author URL

### `cbr_headlines`

- **HTTP:** `GET /cbr/headlines`
- **What:** Get CBR section headlines. Returns fresh headlines from one public CBR RSS section. Video pages, if a section ever returns them, have type video and are not readable through the article endpoint.
- **Params:** `section` (string, **required**) — CBR RSS section slug

### `cbr_news`

- **HTTP:** `GET /cbr/news`
- **What:** Get CBR top stories. Returns about 10 of the latest CBR stories from the site's main feed, with no input needed. Each has a title, canonical URL, summary, publication time, author names (co-authors joined with a comma) and lead image.
- **Params:** _none_

### `cbr_sections`

- **HTTP:** `GET /cbr/sections`
- **What:** Get CBR RSS sections. Lists the 28 CBR section slugs accepted by `cbr-headlines`, grouped by movies, TV, comics, anime and games with news, reviews, features and lists variants, plus `lists` and `cbr-exclusives`. Each entry has a `slug` (for example `news-movies` or `comics/reviews`), a display `name` and the feed `url`.
- **Params:** _none_

## CBS News (5)

### `cbsnews_article`

- **HTTP:** `GET /cbsnews/article`
- **What:** Get CBS News article content. Returns a CBS News article by `url`, a canonical HTTPS `cbsnews.com/news/<slug>` address. The response has the title, description, publication and update times, authors, section, lead image and the body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical CBS News article URL

### `cbsnews_author`

- **HTTP:** `GET /cbsnews/author`
- **What:** Get a CBS News author profile. Returns one CBS News author's public team-page profile: name, biography, coverage topics, headshot (when the page has one), social links, and their recent articles.
- **Params:** `url` (string, **required**) — Canonical cbsnews.com/team/<slug> author URL

### `cbsnews_headlines`

- **HTTP:** `GET /cbsnews/headlines`
- **What:** Get CBS News section headlines. Returns fresh headlines for one CBS News section. `section` is required and is one of `main`, `us`, `world`, `politics`, `moneywatch`, `health`, `entertainment`, `science`, `technology` or `space`. Each item has a title and URL, and may also carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — CBS News RSS section slug

### `cbsnews_news`

- **HTTP:** `GET /cbsnews/news`
- **What:** Get CBS News top stories. Returns the latest CBS News top stories, with no input needed. Each item has a title and canonical URL, and may also carry a summary, author, publication time and image.
- **Params:** _none_

### `cbsnews_sections`

- **HTTP:** `GET /cbsnews/sections`
- **What:** Get CBS News sections. Lists the ten CBS News sections accepted by `cbsnews-headlines`: `main`, `us`, `world`, `politics`, `moneywatch`, `health`, `entertainment`, `science`, `technology` and `space`. Each has a `slug`, a display `name` and the feed `url`.
- **Params:** _none_

## CBS Sports (5)

### `cbssports_article`

- **HTTP:** `GET /cbssports/article`
- **What:** Get CBS Sports article content. Returns a CBS Sports article by `url`, a canonical `https://www.cbssports.com/<sport>/news/<slug>/` address, including `nfl/draft/news/` and fantasy football news: title, description, publication and update times, authors, lead image and body `paragraphs`. Video, scores, schedule and player pages are rejected. `paywalled` is omitted because the articles are free.
- **Params:** `url` (string, **required**) — Canonical CBS Sports article URL

### `cbssports_author`

- **HTTP:** `GET /cbssports/author`
- **What:** Get a CBS Sports writer profile. Returns a CBS Sports writer's profile, identified by `slug` (such as `david-cobb`) or a `cbssports.com/writers/<slug>/` `url`; exactly one is required and an unknown slug returns not-found. The response has name, title, headshot, bio, X/Twitter link and about 15 recent articles with title, URL and summary. Profile fields the page lacks are omitted.
- **Params:** `slug` (string, optional) — Writer slug, e.g. david-cobb; `url` (string, optional) — Canonical cbssports.com/writers/<slug>/ URL; alternative to slug

### `cbssports_headlines`

- **HTTP:** `GET /cbssports/headlines`
- **What:** Get CBS Sports section headlines. Returns fresh headlines from one CBS Sports per-sport feed. `section` is required and takes one of 21 slugs, such as `nfl`, `college-basketball`, `soccer`, `ufc`, `betting` or `general`. Each item has a title and URL, and may carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — CBS Sports section slug

### `cbssports_news`

- **HTTP:** `GET /cbssports/news`
- **What:** Get CBS Sports top stories. Returns the current CBS Sports headlines across every sport, with no input needed: news stories, analysis columns and picks or predictions articles. Only article links are returned; video, scores, schedule and player pages are filtered out. Items have `title` and `url`, plus `summary`, `published_at` and `author` when provided.
- **Params:** _none_

### `cbssports_sections`

- **HTTP:** `GET /cbssports/sections`
- **What:** Get CBS Sports sections. Lists the 21 CBS Sports per-sport sections accepted by `cbssports-headlines`, from `nfl`, `nba` and `soccer` to `betting`, `prediction` and `general`. Each has a `slug`, a display `name` and the feed `url`. A feed can include a story from a neighbouring sport, and off-season ones such as `olympics` can be weeks or months old.
- **Params:** _none_

## Chicago Tribune (5)

### `chicagotribune_article`

- **HTTP:** `GET /chicagotribune/article`
- **What:** Get Chicago Tribune article content. Returns public Chicago Tribune article metadata and body paragraphs from a canonical article URL. For subscriber-only articles the response carries the free lead-in with paywalled set to true.
- **Params:** `url` (string, **required**) — Canonical Chicago Tribune article URL

### `chicagotribune_author`

- **HTTP:** `GET /chicagotribune/author`
- **What:** Get a Chicago Tribune author profile. Returns one Chicago Tribune author's public profile: name, job title when listed, bio, public email and X/Twitter handle, and their recent articles.
- **Params:** `slug` (string, optional) — Author slug, e.g. olivia-olander; `url` (string, optional) — Canonical chicagotribune.com/author/<slug>/ URL; alternative to slug

### `chicagotribune_headlines`

- **HTTP:** `GET /chicagotribune/headlines`
- **What:** Get Chicago Tribune section headlines. Returns headlines from one Chicago Tribune section page. `section` is required and takes one of 60 slugs, such as `local-news`, `crime-public-safety`, `chicago-bears`, `restaurants-food-drink` or `naperville-sun`. Each story has a title, article URL, publication time, byline, excerpt and image where the card shows them. Most sections give about 10 stories.
- **Params:** `section` (string, **required**) — Chicago Tribune section slug

### `chicagotribune_news`

- **HTTP:** `GET /chicagotribune/news`
- **What:** Get Chicago Tribune top stories. Returns the current Chicago Tribune top stories from its homepage, with no input needed. Each has a title and canonical article URL, plus publication time, byline, excerpt and lead image where the story card shows them.
- **Params:** _none_

### `chicagotribune_sections`

- **HTTP:** `GET /chicagotribune/sections`
- **What:** Get Chicago Tribune sections. Lists the 60 Chicago Tribune sections accepted by `chicagotribune-headlines`, spanning news, suburban papers, opinion, sports teams and arts, such as `crime-public-safety`, `daily-southtown`, `chicago-cubs` and `theater`. Each has a `slug`, display `name` and page `url`. Tag pages and hubs that repeat the homepage are not included.
- **Params:** _none_

## Cleveland.com (1)

### `clevelandcom_news`

- **HTTP:** `GET /clevelandcom/news`
- **What:** Get Cleveland.com top stories. Returns Cleveland.com's 50-item public top-stories RSS feed. Summaries and encoded content are publisher teasers; this endpoint does not claim to return full article text. Editorial section inventory and article pages could not be reliably verified due to upstream DataDome blocking.
- **Params:** _none_

## CNA (5)

### `cna_article`

- **HTTP:** `GET /cna/article`
- **What:** Get CNA article content. Returns a CNA (Channel NewsAsia) article by `url`, a canonical `channelnewsasia.com` address such as `/singapore/<slug>-<id>` or `/commentary/<slug>-<id>`: title, description, publication and update times, section, authors, image and the body `paragraphs`. No paywalled or gated content was found during validation.
- **Params:** `url` (string, **required**) — Canonical CNA article URL

### `cna_author`

- **HTTP:** `GET /cna/author`
- **What:** Get a CNA author profile. Returns a CNA correspondent's or contributor's profile, identified by `slug` (such as `aqil-haziq-mahmud`) or a `channelnewsasia.com/author/<slug>` `url`; exactly one is required. The response has name, job title, bio, email, image and the latest page of bylined articles, each with title, URL and label. External Commentary contributors usually have only a name and articles.
- **Params:** `slug` (string, optional) — Author slug, e.g. aqil-haziq-mahmud; `url` (string, optional) — Canonical channelnewsasia.com/author/<slug> URL; alternative to slug

### `cna_headlines`

- **HTTP:** `GET /cna/headlines`
- **What:** Get CNA section headlines. Returns fresh CNA headlines for one section. `section` is required and is `asia`, `business`, `singapore`, `sport` or `world`. Each item has a title and URL, and may also carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — CNA section slug

### `cna_news`

- **HTTP:** `GET /cna/news`
- **What:** Get CNA top stories. Returns the latest CNA (Channel NewsAsia) top stories, with no input needed. Each item has a title and canonical URL, and may also carry a summary, author, publication time and image.
- **Params:** _none_

### `cna_sections`

- **HTTP:** `GET /cna/sections`
- **What:** Get CNA sections. Lists the five CNA sections accepted by `cna-headlines`: `asia`, `business`, `singapore`, `sport` and `world`. Each has a `slug`, a display `name` and the feed `url`.
- **Params:** _none_

## CNBC (4)

### `cnbc_article`

- **HTTP:** `GET /cnbc/article`
- **What:** CNBC article content. Returns public CNBC article metadata and server-rendered body paragraphs. Provide a canonical dated cnbc.com article URL; account-gated content is not bypassed.
- **Params:** `url` (string, **required**) — Canonical cnbc.com article URL

### `cnbc_author`

- **HTTP:** `GET /cnbc/author`
- **What:** CNBC author profile. Returns one CNBC author's public bio page: name, job title, biography, social links, and their most recent articles. Provide either the author's slug (the last path segment of their cnbc.com bio page) or the full bio page URL.
- **Params:** `slug` (string, optional) — CNBC author slug, e.g. jeff-cox; `url` (string, optional) — Canonical https://www.cnbc.com/<slug>/ author page URL, as an alternative to slug

### `cnbc_categories`

- **HTTP:** `GET /cnbc/categories`
- **What:** CNBC editorial sections. Lists the public CNBC editorial sections accepted by /cnbc/headlines, including market, investing, business, technology, and policy subsections, with each section's slug, display name, and landing-page URL.
- **Params:** _none_

### `cnbc_headlines`

- **HTTP:** `GET /cnbc/headlines`
- **What:** CNBC section headlines. Returns current server-rendered CNBC headlines for one public editorial section, including title, article URL, and card metadata when available. Use /cnbc/categories to discover the supported section slugs.
- **Params:** `section` (string, **required**) — Public CNBC editorial section slug from /cnbc/categories

## CNET (5)

### `cnet_article`

- **HTTP:** `GET /cnet/article`
- **What:** Get CNET article content. Returns public CNET article metadata and body paragraphs from a canonical article URL. CNET articles are freely readable; video-only pages and pages without an article body are reported as upstream errors rather than returned empty.
- **Params:** `url` (string, **required**) — Canonical CNET article URL

### `cnet_author`

- **HTTP:** `GET /cnet/author`
- **What:** Get a CNET author profile. Returns one CNET author's public profile: name, role, biography, areas of expertise, social links, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. scottstein8; `url` (string, optional) — Canonical cnet.com/profiles/<slug> URL, optionally with a /page/<n>/ segment; alternative to slug

### `cnet_headlines`

- **HTTP:** `GET /cnet/headlines`
- **What:** Get CNET section headlines. Returns fresh CNET headlines for one topic. `section` is required and takes a topic slug such as `ai`, `deals`, `smart-home`, `electric-vehicles` or `tv-and-movies`; an invalid value returns a 400 error. Each item has a title and URL, and may also carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — CNET topic slug

### `cnet_news`

- **HTTP:** `GET /cnet/news`
- **What:** Get CNET top stories. Returns the latest CNET top stories, with no input needed. Each item has a title, canonical URL, summary, publication time and author name when CNET provides them.
- **Params:** _none_

### `cnet_sections`

- **HTTP:** `GET /cnet/sections`
- **What:** Get CNET sections. Lists the 51 CNET topics accepted by `cnet-headlines`: top-level and second-level topics with a recently updated feed, plus `ai`, `deals` and `tv-and-movies`. Each has a `slug`, a display `name` and the feed `url`. Deeper sub-topics are not separate sections; `internet` means Home Internet and `security` means Home Security.
- **Params:** _none_

## Collider (5)

### `collider_article`

- **HTTP:** `GET /collider/article`
- **What:** Get Collider article content. Returns one Collider article by its `url`, which must be a single-segment `https://collider.com/<slug>/` address. The response has the title, description, publish and update times, section, authors, lead image and body `paragraphs`. Section hubs and video or author pages are rejected as invalid parameters.
- **Params:** `url` (string, **required**) — Canonical Collider article URL

### `collider_author`

- **HTTP:** `GET /collider/author`
- **What:** Get a Collider author profile. Returns a Collider author profile for a `url` of the form `https://collider.com/author/<slug>/`. The response has the name, title, image, biography, `social_links` (type and URL) and the roughly 20 latest articles on the profile. Paginated author URLs are rejected, so older articles are not available.
- **Params:** `url` (string, **required**) — Canonical Collider author URL

### `collider_headlines`

- **HTTP:** `GET /collider/headlines`
- **What:** Get Collider section headlines. Returns fresh headlines from one public Collider RSS section. Items from video categories have type video and are not readable through the article endpoint.
- **Params:** `section` (string, **required**) — Collider RSS section slug

### `collider_news`

- **HTTP:** `GET /collider/news`
- **What:** Get Collider top stories. Lists the latest Collider stories, about 10 items. Each item has its title, canonical URL, summary, publish time, author names (co-authors are joined with a comma) and lead image. Takes no parameters.
- **Params:** _none_

### `collider_sections`

- **HTTP:** `GET /collider/sections`
- **What:** Get Collider RSS sections. Lists the Collider section slugs that `collider-headlines` accepts, such as `movie-news`, `tv-reviews`, `trailers`, `interviews`, `horror` and `video-games`. Each entry has the `slug`, display `name` and feed `url`. Takes no parameters.
- **Params:** _none_

## CTV News (5)

### `ctvnews_article`

- **HTTP:** `GET /ctvnews/article`
- **What:** Get CTV News article content. Returns public CTV News article metadata and body paragraphs from a canonical story URL (https://www.ctvnews.ca/<section>/article/<slug>/). Video, photo-gallery and live-stream pages are not article pages.
- **Params:** `url` (string, **required**) — Canonical CTV News article URL

### `ctvnews_author`

- **HTTP:** `GET /ctvnews/author`
- **What:** Get a CTV News author profile. Returns a CTV News byline profile from a canonical author URL: name, role, biography, photo, public contact address, and recent stories.
- **Params:** `url` (string, **required**) — Canonical CTV News author URL

### `ctvnews_headlines`

- **HTTP:** `GET /ctvnews/headlines`
- **What:** Get CTV News section headlines. Returns the current stories listed on one public CTV News section page, newest first, with headline, summary, byline, publication time and image.
- **Params:** `section` (string, **required**) — CTV News section slug

### `ctvnews_news`

- **HTTP:** `GET /ctvnews/news`
- **What:** Get CTV News top stories. Returns the newest CTV News stories (about the last 24 hours, newest first) from its public news sitemap, each with headline, publication time and lead image.
- **Params:** _none_

### `ctvnews_sections`

- **HTTP:** `GET /ctvnews/sections`
- **What:** Get CTV News sections. Lists the 27 CTV News sections accepted by `ctvnews-headlines`: 12 national topic sections such as `canada`, `politics` and `sci-tech`, and 15 local newsrooms such as `toronto`, `calgary` and `atlantic`. Video, photo, weather, podcast, sponsored and shopping hubs are not included.
- **Params:** _none_

## The Daily Caller (5)

### `dailycaller_article`

- **HTTP:** `GET /dailycaller/article`
- **What:** Get The Daily Caller article content. Returns public The Daily Caller article metadata and body paragraphs from a canonical article URL. Patriots-only (premium) articles expose only a public teaser and are flagged paywalled.
- **Params:** `url` (string, **required**) — Canonical The Daily Caller article URL

### `dailycaller_author`

- **HTTP:** `GET /dailycaller/author`
- **What:** Get a The Daily Caller author profile. Returns a The Daily Caller author's byline metadata, job title, optional biography, contact links, and newest articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical The Daily Caller author URL

### `dailycaller_headlines`

- **HTTP:** `GET /dailycaller/headlines`
- **What:** Get The Daily Caller section headlines. Returns the newest headlines, about 40, from one Daily Caller section page. `section` is required (`politics`, `world`, `energy`, `opinion`, `patriots` and others); any other value returns a 400. Items have a title, URL, lead image and sometimes a `type` such as `opinion`. Section pages carry no publish time or byline.
- **Params:** `section` (string, **required**) — The Daily Caller section slug

### `dailycaller_news`

- **HTTP:** `GET /dailycaller/news`
- **What:** Get The Daily Caller top stories. Returns about 25 of the newest Daily Caller top stories, mixed across sections. Each item has its title, URL, author, publication time (RFC 3339, UTC) and lead image. It takes no parameters; use the headlines endpoint when you want a single section.
- **Params:** _none_

### `dailycaller_sections`

- **HTTP:** `GET /dailycaller/sections`
- **What:** Get The Daily Caller sections. Lists the 22 Daily Caller section slugs that the headlines endpoint accepts, from `politics` and `world` to `opinion` and `video`, each with its `name` and section page `url`. Sponsored content is not offered. A few sections such as `satire`, `two-sides` and `video` publish rarely, so their newest items can be months old.
- **Params:** _none_

## Daily Express (5)

### `dailyexpress_article`

- **HTTP:** `GET /dailyexpress/article`
- **What:** Get Daily Express article content. Returns one Daily Express article by its canonical article `url`. The response has the title, description, publish and update times, section, authors, lead image, body `paragraphs` and a `paywalled` flag. Subscriber-only or blocked articles return an upstream error instead of partial text.
- **Params:** `url` (string, **required**) — Canonical Daily Express article URL

### `dailyexpress_author`

- **HTTP:** `GET /dailyexpress/author`
- **What:** Get a Daily Express journalist profile. Returns one Daily Express journalist's public profile: name, job title, bio, and their recent articles, from a canonical journalist URL.
- **Params:** `url` (string, **required**) — Canonical Daily Express journalist URL

### `dailyexpress_headlines`

- **HTTP:** `GET /dailyexpress/headlines`
- **What:** Get Daily Express section headlines. Returns the latest Daily Express headlines for one section. `section` is required and takes a slug such as `news`, `royal`, `showbiz-tv`, `formula-1` or `city-business`. Each item has its title, URL, summary, publication time and image.
- **Params:** `section` (string, **required**) — Daily Express section slug

### `dailyexpress_news`

- **HTTP:** `GET /dailyexpress/news`
- **What:** Get Daily Express top stories. Returns the current Daily Express top stories. Each item has its title, URL, summary, publication time and image. Takes no parameters; use `dailyexpress-headlines` to read a single section instead.
- **Params:** _none_

### `dailyexpress_sections`

- **HTTP:** `GET /dailyexpress/sections`
- **What:** Get Daily Express sections. Lists the Daily Express sections that `dailyexpress-headlines` accepts, such as `news`, `uk`, `royal`, `sport` and `personal-finance`. Each entry has a stable `slug`, a display `name` and the section `url`. Takes no parameters.
- **Params:** _none_

## Daily Mail (5)

### `dailymail_article`

- **HTTP:** `GET /dailymail/article`
- **What:** Get Daily Mail article content. Returns one Daily Mail article by its canonical `url`, which must contain an `article-<id>` path segment. The response has the title, description, publish and update times, section, authors, lead image, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Daily Mail article URL

### `dailymail_author`

- **HTTP:** `GET /dailymail/author`
- **What:** Get a Daily Mail author profile. Returns one Daily Mail author's public profile: name, job title, bio, social accounts, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page of articles to return; defaults to 1; `url` (string, **required**) — Canonical dailymail.com/profile-<id>/<slug>.html URL

### `dailymail_headlines`

- **HTTP:** `GET /dailymail/headlines`
- **What:** Get Daily Mail section headlines. Returns the latest Daily Mail headlines for one section. `section` is required and must be one of `home`, `news`, `sport`, `tvshowbiz`, `health`, `femail`, `travel`, `sciencetech`, `money`, `debate`, `us` or `australia`. Each item has its title, URL, summary, publication time and image.
- **Params:** `section` (string, **required**) — Daily Mail RSS section slug

### `dailymail_news`

- **HTTP:** `GET /dailymail/news`
- **What:** Get Daily Mail top stories. Returns the current Daily Mail top stories. Each item has its title, URL, summary, publication time and image. Takes no parameters; use `dailymail-headlines` for a single section.
- **Params:** _none_

### `dailymail_sections`

- **HTTP:** `GET /dailymail/sections`
- **What:** Get Daily Mail RSS sections. Lists the 12 Daily Mail sections accepted by `dailymail-headlines`: `home`, `news`, `sport`, `tvshowbiz`, `health`, `femail`, `travel`, `sciencetech`, `money`, `debate`, `us` and `australia`. Each entry has the `slug`, display `name` and feed `url`.
- **Params:** _none_

## Daily Record (5)

### `dailyrecord_article`

- **HTTP:** `GET /dailyrecord/article`
- **What:** Get Daily Record article content. Returns one Daily Record article by its canonical article `url`. The response has the title, description, publish and update times, section, authors, lead image, body `paragraphs` and a `paywalled` flag. Subscriber-only or blocked articles return an upstream error.
- **Params:** `url` (string, **required**) — Canonical Daily Record article URL

### `dailyrecord_author`

- **HTTP:** `GET /dailyrecord/author`
- **What:** Get a Daily Record author profile. Returns a Daily Record author profile, found by `slug` (for example `paul-hutcheon`) or by a canonical `url`; send exactly one of the two. The response has the name, job title, bio, email, X/Twitter link and recent articles with their label. Contact details the page does not list are simply absent.
- **Params:** `slug` (string, optional) — Author slug, e.g. paul-hutcheon; `url` (string, optional) — Canonical dailyrecord.co.uk/authors/<slug>/ URL; alternative to slug

### `dailyrecord_headlines`

- **HTTP:** `GET /dailyrecord/headlines`
- **What:** Get Daily Record section headlines. Returns the latest Daily Record headlines for one section. `section` is required and must be one of `news`, `scotland`, `uk-world-news`, `sport`, `football`, `showbiz`, `lifestyle`, `money`, `travel` or `in-your-area`. Every item has its title and URL; the `news` section also carries summary, publication time and image.
- **Params:** `section` (string, **required**) — Daily Record section slug

### `dailyrecord_news`

- **HTTP:** `GET /dailyrecord/news`
- **What:** Get Daily Record top stories. Returns the current Daily Record top stories. Each item has its title, URL, summary, publication time and image. Takes no parameters; use `dailyrecord-headlines` for a single section.
- **Params:** _none_

### `dailyrecord_sections`

- **HTTP:** `GET /dailyrecord/sections`
- **What:** Get Daily Record sections. Lists the Daily Record sections accepted by `dailyrecord-headlines`, such as `news`, `scotland`, `uk-world-news`, `football` and `in-your-area`. Each entry has a stable `slug`, a display `name` and the section `url`. Takes no parameters.
- **Params:** _none_

## Daily Star UK (5)

### `dailystaruk_article`

- **HTTP:** `GET /dailystaruk/article`
- **What:** Get Daily Star (UK) article content. Returns public Daily Star (UK) article metadata (including the section) and body paragraphs from a canonical article URL. Photo-gallery and sponsored partner-story URLs are rejected.
- **Params:** `url` (string, **required**) — Canonical Daily Star (UK) article URL

### `dailystaruk_author`

- **HTTP:** `GET /dailystaruk/author`
- **What:** Get a Daily Star (UK) author profile. Returns one Daily Star (UK) author's public profile (name and, when published, job title, bio, email and X/Twitter handle) and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page number of the author's article list (1 to 100); overrides any pageNumber in url; `slug` (string, optional) — Author slug, e.g. edward-easton; `url` (string, optional) — Canonical dailystar.co.uk/authors/<slug>/ URL; alternative to slug

### `dailystaruk_headlines`

- **HTTP:** `GET /dailystaruk/headlines`
- **What:** Get Daily Star (UK) section headlines. Returns fresh headlines from one public Daily Star (UK) section. Photo galleries are omitted because they have no readable article body.
- **Params:** `section` (string, **required**) — Daily Star (UK) section slug

### `dailystaruk_news`

- **HTTP:** `GET /dailystaruk/news`
- **What:** Get Daily Star (UK) top stories. Returns fresh Daily Star (UK) top stories from the public home RSS feed. Photo galleries are omitted because they have no readable article body.
- **Params:** _none_

### `dailystaruk_sections`

- **HTTP:** `GET /dailystaruk/sections`
- **What:** Get Daily Star (UK) sections. Lists the Daily Star (UK) sections accepted by `dailystaruk-headlines`, including nested slugs such as `sport/football`, `news/weird-news` and `tech/gaming`. Each entry has the `slug`, `name` and feed `url`. Feeds were checked on 2026-09-25 and return up to about 25 entries.
- **Params:** _none_

## DailyWire (5)

### `dailywire_article`

- **HTTP:** `GET /dailywire/article`
- **What:** Get Daily Wire article content. Returns public Daily Wire article metadata and body paragraphs from an article URL under any of the site's content-vertical prefixes.
- **Params:** `url` (string, **required**) — Daily Wire article URL

### `dailywire_author`

- **HTTP:** `GET /dailywire/author`
- **What:** Get a Daily Wire author profile. Returns one Daily Wire staff writer or contributor's public profile: name, headshot, social handles when present, biography, and their recent articles.
- **Params:** `slug` (string, optional) — Author slug, e.g. brent-scher; `url` (string, optional) — Canonical dailywire.com/author/<slug> URL; alternative to slug

### `dailywire_headlines`

- **HTTP:** `GET /dailywire/headlines`
- **What:** Get Daily Wire section headlines. Returns current Daily Wire headlines for one content vertical. `section` is required and takes `news`, `opinion`, `dw-opinion`, `analysis`, `news-and-commentary`, `news-and-analysis`, `exclusive`, `entertainment`, `original`, `upstream`, `sports` or `mi-x-dw`. An empty result means the front page does not currently feature that vertical.
- **Params:** `section` (string, **required**) — Daily Wire section slug

### `dailywire_news`

- **HTTP:** `GET /dailywire/news`
- **What:** Get Daily Wire top stories. Returns the current Daily Wire top stories. Each item has its title, URL, summary, publication time, author and image. Takes no parameters; use `dailywire-headlines` to filter by content vertical.
- **Params:** _none_

### `dailywire_sections`

- **HTTP:** `GET /dailywire/sections`
- **What:** Get Daily Wire content-vertical sections. Lists the Daily Wire content verticals that `dailywire-headlines` accepts, such as `news`, `opinion`, `analysis`, `entertainment`, `upstream` and `sports`. Each entry has a `slug`, `name` and `url`. Sampled on 2026-09-24, so the list may not be exhaustive.
- **Params:** _none_

## Dawn (5)

### `dawn_article`

- **HTTP:** `GET /dawn/article`
- **What:** Get Dawn article content. Returns one Dawn article by its canonical `url` in the form `https://www.dawn.com/news/<id>/<slug>`. The response has the title, description, publish and update times, section, authors, lead image and body `paragraphs`. Blocked or malformed pages return an upstream error.
- **Params:** `url` (string, **required**) — Canonical Dawn article URL

### `dawn_author`

- **HTTP:** `GET /dawn/author`
- **What:** Get a Dawn author profile. Returns one Dawn byline's public profile (name and biography, when Dawn publishes one) and their recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical www.dawn.com/authors/<id>/<slug> URL

### `dawn_headlines`

- **HTTP:** `GET /dawn/headlines`
- **What:** Get Dawn section headlines. Returns the latest Dawn headlines for one section. `section` is required and takes a slug such as `pakistan`, `pakistan-sindh`, `world-south-asia`, `business-finance`, `sport-cricket`, `opinion` or `prism`. Each item has its title, URL, summary, publication time and, when the outlet provides one, image.
- **Params:** `section` (string, **required**) — Dawn section slug

### `dawn_news`

- **HTTP:** `GET /dawn/news`
- **What:** Get Dawn top stories. Returns the current top stories from Dawn, the Pakistani newspaper. Each item has its title, URL, summary, publication time and, when the outlet provides one, image. Takes no parameters; use `dawn-headlines` for a single section.
- **Params:** _none_

### `dawn_sections`

- **HTTP:** `GET /dawn/sections`
- **What:** Get Dawn sections. Returns the complete public Dawn section inventory (Pakistan provinces, World, Business, Sport, Opinion, Technology, Newspaper, Magazines, and Prism) accepted by /dawn/headlines.
- **Params:** _none_

## Deadline (5)

### `deadline_article`

- **HTTP:** `GET /deadline/article`
- **What:** Get Deadline article content. Returns public Deadline article metadata (title, author(s), published/updated dates, section, lead image) and body paragraphs from a canonical article URL.
- **Params:** `url` (string, **required**) — Canonical Deadline article URL

### `deadline_author`

- **HTTP:** `GET /deadline/author`
- **What:** Get a Deadline author profile. Returns one Deadline staff writer or contributor's public profile: name, job title, headshot, biography, social/contact links, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page of recent articles to return; defaults to 1; `url` (string, **required**) — Canonical deadline.com/author/<slug> URL

### `deadline_headlines`

- **HTTP:** `GET /deadline/headlines`
- **What:** Get Deadline section headlines. Returns the latest Deadline headlines for one section or vertical. `section` is required and takes one of 48 slugs, for example `film`, `tv`, `box-office`, `awards`, `casting`, `reviews` or `obituaries`. Each item has its title, URL, summary, publication time, author and image.
- **Params:** `section` (string, **required**) — Deadline section slug

### `deadline_news`

- **HTTP:** `GET /deadline/news`
- **What:** Get Deadline top stories. Returns the current Deadline Hollywood top stories from its main feed. Each item has its title, URL, summary, publication time, author and image. Takes no parameters; use `deadline-headlines` for a single section or vertical.
- **Params:** _none_

### `deadline_sections`

- **HTTP:** `GET /deadline/sections`
- **What:** Get Deadline sections. Lists the 48 Deadline sections accepted by `deadline-headlines`: 28 editorial categories such as `news`, `reviews` and `festivals`, and 20 verticals such as `film`, `tv`, `business` and `awards`. Each entry has the `slug`, `name` and feed `url`.
- **Params:** _none_

## DW (5)

### `dw_article`

- **HTTP:** `GET /dw/article`
- **What:** Get DW article content. Returns one Deutsche Welle article by its canonical `url`, either a standard `/en/<slug>/a-<id>` article or a `/en/<slug>/live-<id>` live-blog page. The response has the title, description, publish time, section, authors, lead image and body `paragraphs`. Blocked or malformed pages return an upstream error.
- **Params:** `url` (string, **required**) — Canonical DW article URL

### `dw_author`

- **HTTP:** `GET /dw/author`
- **What:** Get a DW author profile. Returns one Deutsche Welle correspondent's public profile (name, expertise, biography) and their recent articles from a canonical person-profile URL. Many DW breaking-news items are bylined to the "Deutsche Welle" editorial organization rather than a named person; those articles have no person-profile URL to look up.
- **Params:** `url` (string, **required**) — Canonical www.dw.com/en/<name>/person-<id> URL

### `dw_headlines`

- **HTTP:** `GET /dw/headlines`
- **What:** Get DW section headlines. Returns the latest Deutsche Welle headlines for one section. `section` is required and takes one of 18 slugs, such as `africa`, `middle-east`, `germany`, `climate`, `migration`, `human-rights`, `business` or `sports`. Each item has its title and URL, plus an image when the card shows one.
- **Params:** `section` (string, **required**) — DW section slug

### `dw_news`

- **HTTP:** `GET /dw/news`
- **What:** Get DW top stories. Returns the current Deutsche Welle top stories. Each item has its title, URL, summary and publication time. Takes no parameters; use `dw-headlines` for a single region, topic or category.
- **Params:** _none_

### `dw_sections`

- **HTTP:** `GET /dw/sections`
- **What:** Get DW sections. Lists the DW English-edition sections accepted by `dw-headlines`, grouped under the site's three navigation groups: regions, topics and categories. Each entry has a stable `slug`, display `name` and the section `url`. Takes no parameters.
- **Params:** _none_

## Economic Times (5)

### `economictimes_article`

- **HTTP:** `GET /economictimes/article`
- **What:** Get Economic Times article content. Returns public Economic Times article metadata (title, author(s), published/updated dates, section, lead image) and body paragraphs from a canonical article URL. An ETPrime subscription-gated story returns a permission error instead of a truncated or fabricated body.
- **Params:** `url` (string, **required**) — Canonical Economic Times article URL

### `economictimes_author`

- **HTTP:** `GET /economictimes/author`
- **What:** Get an Economic Times author profile. Returns an Economic Times reporter profile for a `url` like `https://economictimes.indiatimes.com/etreporter/author-<name>-<id>.cms`. The response has the name, job title (role and desk in one string), biography, headshot and recent articles with title and URL. Job title, biography and image may be empty; no email field exists.
- **Params:** `url` (string, **required**) — Canonical Economic Times author URL

### `economictimes_headlines`

- **HTTP:** `GET /economictimes/headlines`
- **What:** Get The Economic Times section headlines. Returns the latest Economic Times headlines for one section. `section` is required and takes a slug such as `top-stories`, `markets-stocks`, `mf-mf-news`, `industry-banking-finance`, `jobs-fresher` or `news-india`. Each item has its title, URL, summary, publication time and image.
- **Params:** `section` (string, **required**) — Economic Times section slug

### `economictimes_news`

- **HTTP:** `GET /economictimes/news`
- **What:** Get The Economic Times top stories. Returns the current Economic Times top stories. Each item has its title, URL and publication time, plus a summary for some stories. Takes no parameters; use `economictimes-headlines` for a single section.
- **Params:** _none_

### `economictimes_sections`

- **HTTP:** `GET /economictimes/sections`
- **What:** Get The Economic Times sections. Returns the complete public section inventory accepted by /api/v1/economictimes/headlines: business/markets verticals, industry, tech, wealth, mutual funds, small business, NRI, careers, opinion, astrology, and ETPrime (subscription-gated) sections.
- **Params:** _none_

## Engadget (5)

### `engadget_article`

- **HTTP:** `GET /engadget/article`
- **What:** Get Engadget article content. Returns public Engadget article metadata and body paragraphs from a canonical article URL. Engadget articles are free to read, so the full body is returned.
- **Params:** `url` (string, **required**) — Canonical Engadget article URL

### `engadget_author`

- **HTTP:** `GET /engadget/author`
- **What:** Get an Engadget author profile. Returns one Engadget author's public profile: name, biography, expertise, social links, and the latest stories listed on their page (a single fixed batch; the page has no further pagination).
- **Params:** `slug` (string, optional) — Author slug, e.g. mariella-moon; `url` (string, optional) — Canonical engadget.com/author/<slug> URL; alternative to slug

### `engadget_headlines`

- **HTTP:** `GET /engadget/headlines`
- **What:** Get Engadget section headlines. Returns the latest Engadget headlines for one category. `section` is required and takes one of 48 slugs such as `ai`, `gaming`, `apple`, `laptop-pc-reviews` or `transportation-evs`; other values return an invalid-parameter error. Small categories, such as buying guides, may hold only a few items.
- **Params:** `section` (string, **required**) — Engadget category slug

### `engadget_news`

- **HTTP:** `GET /engadget/news`
- **What:** Get Engadget top stories. Returns the current Engadget technology news. Each item has a title, URL, summary, publish time, author and image when available. Engadget articles are free to read. Takes no parameters; use `engadget-headlines` for a single category.
- **Params:** _none_

### `engadget_sections`

- **HTTP:** `GET /engadget/sections`
- **What:** Get Engadget sections. Lists the 48 Engadget categories accepted by `engadget-headlines`, such as `ai`, `cybersecurity`, `smartphone-reviews`, `space` and `xbox`. Each entry has the `slug`, display `name` and category feed `url`. Categories with an empty feed are not listed.
- **Params:** _none_

## E! News (5)

### `eonline_article`

- **HTTP:** `GET /eonline/article`
- **What:** Get E! News article content. Returns one E! News article by its `url`, in the form `https://www.eonline.com/news/<numeric id>/<slug>`. The response has the title, description, publish time, byline, lead image, body `paragraphs` and `section`, which is the article's first tag. Photo galleries, videos and show pages are rejected; an unknown id returns not-found.
- **Params:** `url` (string, **required**) — Canonical E! News article URL

### `eonline_author`

- **HTTP:** `GET /eonline/author`
- **What:** Get an E! News author page. Returns an E! News writer's `name` and the articles on their author page, about 45 per page, for a `url` like `https://www.eonline.com/authors/natalie-finn` (add `/page/<n>` for older ones). There is no biography or photo. `published_at` is the page's own text, such as `18 minutes ago`, not a timestamp.
- **Params:** `url` (string, **required**) — Canonical E! News author URL

### `eonline_headlines`

- **HTTP:** `GET /eonline/headlines`
- **What:** Get E! News section headlines. Returns up to 30 E! News headlines for one section. `section` is required and must be one of `top_stories`, `tv`, `movies`, `music`, `celebrities`, `couples`, `royals`, `red_carpet`, `influencer`, `style`, `fashion` or `shop`. Each item has its title, URL, summary, publication time, author and image.
- **Params:** `section` (string, **required**) — E! News section slug

### `eonline_news`

- **HTTP:** `GET /eonline/news`
- **What:** Get E! News top stories. Returns up to 30 top stories from the US edition of E! News. Each item has its title, canonical article URL, summary, publication time, byline and thumbnail. Takes no parameters; use `eonline-headlines` for a single section.
- **Params:** _none_

### `eonline_sections`

- **HTTP:** `GET /eonline/sections`
- **What:** Get E! News sections. Lists the 12 E! News sections accepted by `eonline-headlines`, from `top_stories`, `tv` and `movies` to `royals`, `fashion` and `shop`. Each entry has the `slug`, `name` and feed `url`. The list is curated from the main navigation hubs and major tag feeds, not every tag.
- **Params:** _none_

## Euronews (5)

### `euronews_article`

- **HTTP:** `GET /euronews/article`
- **What:** Get Euronews article content. Returns one Euronews English-edition article by its `url`, in the form `https://www.euronews.com/YYYY/MM/DD/<slug>`. The response has the title, description, publish and update times, section, authors, lead image and body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical Euronews article URL

### `euronews_author`

- **HTTP:** `GET /euronews/author`
- **What:** Get a Euronews author profile. Returns a Euronews author profile for a `url` like `https://www.euronews.com/profiles/<id>`. The response has the name, job title, editorial team, `social_links` (usually one X/Twitter link, empty if none) and recent articles. There is no headshot or biography, and `job_title` is repeated as Euronews gives it.
- **Params:** `url` (string, **required**) — Canonical Euronews author profile URL

### `euronews_headlines`

- **HTTP:** `GET /euronews/headlines`
- **What:** Get Euronews section headlines. Returns the latest Euronews English-edition headlines for one section. `section` is required and takes one of 42 slugs, including themes (`business`, `culture`, `earth`, `health`, `next`, `travel`) and their sub-sections such as `business-markets` or `next-space`. Each item has its title and URL; the `news` and `business` sections also carry summary and publication time.
- **Params:** `section` (string, **required**) — Euronews section slug

### `euronews_news`

- **HTTP:** `GET /euronews/news`
- **What:** Get Euronews top stories. Returns the current Euronews English-edition top stories. Each item has its title, URL, summary and publication time. Takes no parameters; use `euronews-headlines` for a single theme or sub-section.
- **Params:** _none_

### `euronews_sections`

- **HTTP:** `GET /euronews/sections`
- **What:** Get Euronews sections. Lists the 42 Euronews English-edition sections accepted by `euronews-headlines`. Top-level themes include `news`, `business`, `culture`, `earth`, `health`, `my-europe`, `next` and `travel`, each with sub-sections such as `news-africa` or `earth-climate`. Each entry has the `slug`, `name` and `url`.
- **Params:** _none_

## Entertainment Weekly (5)

### `ew_article`

- **HTTP:** `GET /ew/article`
- **What:** Get Entertainment Weekly article content. Returns one Entertainment Weekly article by its canonical `url` in the form `ew.com/<slug>-<id>`. The response has the title, description, publish and update times, section, authors, lead image, body `paragraphs` and a `paywalled` flag. Blocked or malformed pages return an upstream error.
- **Params:** `url` (string, **required**) — Canonical Entertainment Weekly article URL

### `ew_author`

- **HTTP:** `GET /ew/author`
- **What:** Get an Entertainment Weekly author profile. Returns one Entertainment Weekly contributor's public profile (name, job title, biography) and their recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical ew.com/author/<slug> or ew.com/<slug>-<id> profile URL

### `ew_headlines`

- **HTTP:** `GET /ew/headlines`
- **What:** Get Entertainment Weekly section headlines. Returns the latest Entertainment Weekly headlines for one section. `section` is required and must be one of `tv`, `movies`, `music`, `what-to-watch`, `binge`, `celebrity`, `awardist`, `books` or `theater`. Each item has its title and URL, plus an image when the card shows one.
- **Params:** `section` (string, **required**) — Entertainment Weekly section slug

### `ew_news`

- **HTTP:** `GET /ew/news`
- **What:** Get Entertainment Weekly top stories. Returns the current Entertainment Weekly top stories. Each item has its title and URL, plus an image when the card shows one. Takes no parameters; use `ew-headlines` for a single section.
- **Params:** _none_

### `ew_sections`

- **HTTP:** `GET /ew/sections`
- **What:** Get Entertainment Weekly sections. Lists the nine Entertainment Weekly primary-navigation sections accepted by `ew-headlines`: `tv`, `movies`, `music`, `what-to-watch`, `binge`, `celebrity`, `awardist`, `books` and `theater`. Each entry has the `slug`, display `name` and section `url`.
- **Params:** _none_

## Fast Company (5)

### `fastcompany_article`

- **HTTP:** `GET /fastcompany/article`
- **What:** Get Fast Company article content. Returns public Fast Company article metadata and body paragraphs from a canonical article URL. It does not bypass authentication or access controls.
- **Params:** `url` (string, **required**) — Canonical Fast Company article URL

### `fastcompany_author`

- **HTTP:** `GET /fastcompany/author`
- **What:** Get a Fast Company contributor profile. Returns a Fast Company contributor's name, biography, and recent articles from a canonical contributor URL. The biography is omitted if the contributor's profile page cannot be loaded. It does not bypass authentication or access controls.
- **Params:** `url` (string, **required**) — Canonical Fast Company contributor URL

### `fastcompany_headlines`

- **HTTP:** `GET /fastcompany/headlines`
- **What:** Get Fast Company section headlines. Returns fresh headlines from one Fast Company section or topic's public RSS feed. section accepts any slug returned by GET /fastcompany/sections (78 values, e.g. "technology" or "artificial-intelligence").
- **Params:** `section` (string, **required**) — Fast Company section slug, from GET /fastcompany/sections

### `fastcompany_news`

- **HTTP:** `GET /fastcompany/news`
- **What:** Get Fast Company top stories. Returns the current Fast Company top stories. Each item has its title, canonical URL, summary, publication time, author and image. Takes no parameters, so there is no section or paging control.
- **Params:** _none_

### `fastcompany_sections`

- **HTTP:** `GET /fastcompany/sections`
- **What:** Get Fast Company sections. Returns the Fast Company section/topic inventory: the site's six primary verticals (Tech, Work Life, News, Design, Leadership, Impact) plus every topic tag accepted by GET /fastcompany/headlines (78 values total, too many to enumerate inline -- see that endpoint for the full, current, live-verified list), each linking to its public RSS feed.
- **Params:** _none_

## Fox News (6)

### `foxnews_article`

- **HTTP:** `GET /foxnews/article`
- **What:** Get Fox News article content. Returns public Fox News article metadata and body paragraphs from a canonical article URL. This does not bypass login, subscription, or other access controls.
- **Params:** `url` (string, **required**) — Canonical Fox News article URL

### `foxnews_author`

- **HTTP:** `GET /foxnews/author`
- **What:** Get Fox News author profile. Returns one Fox News author/personality's public bio page: name, biography, and their most recent articles. Provide either the author's name slug or the full https://www.foxnews.com/person/<letter>/<slug> page URL.
- **Params:** `slug` (string, optional) — Fox News author name slug, e.g. brooke-taylor; `url` (string, optional) — Canonical https://www.foxnews.com/person/<letter>/<slug> author page URL, as an alternative to slug

### `foxnews_headlines`

- **HTTP:** `GET /foxnews/headlines`
- **What:** Get Fox News section headlines. Returns the latest 25 Fox News headlines for one section. `section` is required and must be one of `us`, `world`, `politics`, `science`, `health`, `sports`, `travel`, `tech`, `opinion`, `entertainment`, `media` or `lifestyle`. Each item has its title, URL, summary, publication time and image.
- **Params:** `section` (string, **required**) — Fox News RSS section slug: us, world, politics, science, health, sports, travel, tech, opinion, entertainment, media, or lifestyle

### `foxnews_news`

- **HTTP:** `GET /foxnews/news`
- **What:** Get Fox News top stories. Returns fresh Fox News top stories from the public site-wide RSS feed. The feed is a public headline/body source and does not require credentials.
- **Params:** _none_

### `foxnews_search`

- **HTTP:** `GET /foxnews/search`
- **What:** Search Fox News public content. Searches Fox News. Results may include article, video, or slideshow records; use type to restrict the result kind.
- **Params:** `q` (string, **required**) — Search query; `start` (integer, optional) — 1-based result offset; `type` (string, optional) — Result type

### `foxnews_sections`

- **HTTP:** `GET /foxnews/sections`
- **What:** Get Fox News RSS sections. Returns the exact live-verified Fox News article RSS section slugs accepted by foxnews-headlines. The video-only RSS feed is intentionally excluded.
- **Params:** _none_

## FOX Sports (4)

### `foxsports_article`

- **HTTP:** `GET /foxsports/article`
- **What:** Get FOX Sports article content. Returns public FOX Sports article metadata and body paragraphs from a canonical foxsports.com/stories/<section>/<slug> URL. Public body content stops at the article body container.
- **Params:** `url` (string, **required**) — Canonical FOX Sports story URL

### `foxsports_headlines`

- **HTTP:** `GET /foxsports/headlines`
- **What:** Get FOX Sports section headlines. Returns current FOX Sports headlines for one sport or topic. `section` is required and takes one of 23 slugs such as `top`, `nfl`, `nba`, `college-football`, `ufc`, `golf` or `fifa-world-cup`; others return an invalid-parameter error. Feeds follow FOX Sports' own curation and can include related cross-sport items.
- **Params:** `section` (string, **required**) — FOX Sports section slug

### `foxsports_news`

- **HTTP:** `GET /foxsports/news`
- **What:** Get FOX Sports top stories. Returns current cross-sport stories from FOX Sports' All Headlines feed. Each item has its title and canonical story URL, plus summary, publication time, author and image when FOX Sports supplies them. Takes no parameters.
- **Params:** _none_

### `foxsports_sections`

- **HTTP:** `GET /foxsports/sections`
- **What:** Get FOX Sports news sections. Lists the 23 FOX Sports editorial feeds accepted by `foxsports-headlines`, including `top`, `mlb`, `nfl`, `soccer`, `olympics` and `wwe`. Each entry has the `slug`, `name` and feed `url`. The All Headlines feed is served by `foxsports-news`, not as a section; checked 2026-09-28.
- **Params:** _none_

## France 24 (5)

### `france24_article`

- **HTTP:** `GET /france24/article`
- **What:** Get France 24 article content. Returns public France 24 English-edition article metadata and body paragraphs from a canonical article URL. Live-blog pages are supported and return their chronological update entries as body paragraphs.
- **Params:** `url` (string, **required**) — Canonical France 24 article URL

### `france24_author`

- **HTTP:** `GET /france24/author`
- **What:** Get a France 24 author profile. Returns one France 24 byline's public profile (name, job title, biography) and their recent articles from a canonical author-profile URL. This includes the shared "FRANCE 24" newsroom byline used on many stories, which has no individual biography.
- **Params:** `url` (string, **required**) — Canonical www.france24.com/en/author/<slug>/ URL

### `france24_headlines`

- **HTTP:** `GET /france24/headlines`
- **What:** Get France 24 section headlines. Returns the latest France 24 English-edition headlines for one section. `section` is required and must be one of `africa`, `americas`, `asia-pacific`, `europe`, `france`, `middle-east`, `business-tech`, `culture`, `environment`, `sport`, `live-news` or `tv-shows`. Each item has its title, URL, summary, publication time and author.
- **Params:** `section` (string, **required**) — France 24 section slug

### `france24_news`

- **HTTP:** `GET /france24/news`
- **What:** Get France 24 top stories. Returns the current France 24 English-edition top stories. Each item has its title, URL, summary, publication time and author. Takes no parameters; use `france24-headlines` for a single region or topic.
- **Params:** _none_

### `france24_sections`

- **HTTP:** `GET /france24/sections`
- **What:** Get France 24 sections. Lists the 12 France 24 English-edition sections accepted by `france24-headlines`: six regions, four topics, the `live-news` wire-briefs hub and the `tv-shows` programmes hub. Each entry has the `slug`, display `name` and section `url`.
- **Params:** _none_

## Free Malaysia Today (2)

### `freemalaysiatoday_news`

- **HTTP:** `GET /freemalaysiatoday/news`
- **What:** Get the latest Free Malaysia Today stories. Returns Free Malaysia Today's current public top-stories RSS feed: each story's title, canonical URL, summary, author, publication time, and lead image.
- **Params:** _none_

### `freemalaysiatoday_sections`

- **HTTP:** `GET /freemalaysiatoday/sections`
- **What:** List Free Malaysia Today sections. Lists every live-verified primary editorial navigation section, with its slug, display name, and landing-page URL. This is the live-verified primary editorial navigation taxonomy; media, promotional, and duplicate commercial destinations are excluded.
- **Params:** _none_

## Game Rant (5)

### `gamerant_article`

- **HTTP:** `GET /gamerant/article`
- **What:** Get Game Rant article content. Returns one Game Rant article by its `https://gamerant.com/<slug>/` `url`. The response has the title, description, publish and update times, section, authors, lead image and body `paragraphs`. Section hubs, video pages and author pages are rejected as invalid parameters; `paywalled` is set only if the page declares the article not free.
- **Params:** `url` (string, **required**) — Canonical Game Rant article URL

### `gamerant_author`

- **HTTP:** `GET /gamerant/author`
- **What:** Get a Game Rant author profile. Returns a Game Rant author profile for a `url` of the form `https://gamerant.com/author/<slug>/`. The response has the name, title, image, biography, `social_links` (type and URL) and about 20 latest articles. Paginated author URLs are rejected, so older articles are not available.
- **Params:** `url` (string, **required**) — Canonical Game Rant author URL

### `gamerant_headlines`

- **HTTP:** `GET /gamerant/headlines`
- **What:** Get Game Rant section headlines. Returns fresh headlines from one public Game Rant RSS section. Items from video sections have type video and are not readable through the article endpoint.
- **Params:** `section` (string, **required**) — Game Rant RSS section slug

### `gamerant_news`

- **HTTP:** `GET /gamerant/news`
- **What:** Get Game Rant top stories. Lists the latest Game Rant stories, about 10 items. Each item has its title, canonical URL, summary, publish time, author names (co-authors are joined with a comma) and lead image. Takes no parameters.
- **Params:** _none_

### `gamerant_sections`

- **HTTP:** `GET /gamerant/sections`
- **What:** Get Game Rant RSS sections. Lists the 178 Game Rant section slugs accepted by `gamerant-headlines`, covering platforms (`pc-news`, `ps5-news`, `nintendo-switch-news`), franchises (`fortnite-news`, `pokemon-news`, `fallout-news`), `anime` and `game-reviews`. Each entry has the `slug`, `name` and feed `url`.
- **Params:** _none_

## GamesRadar+ (5)

### `gamesradar_article`

- **HTTP:** `GET /gamesradar/article`
- **What:** Get GamesRadar+ article content. Returns one GamesRadar+ article by its canonical `gamesradar.com` `url`. The response has the title, description, publish and update times, section, authors, lead image and body `paragraphs`. Game and hardware review pages work too, taking the author from the page byline when no article-level author exists.
- **Params:** `url` (string, **required**) — Canonical GamesRadar+ article URL

### `gamesradar_author`

- **HTTP:** `GET /gamesradar/author`
- **What:** Get a GamesRadar+ author profile. Returns a GamesRadar+ author profile, found by `slug` (for example `rosalie-newcombe`) or by `url`; send exactly one. `page` (1-based, default 1) overrides any page in the URL. The response has the name, job title, biography, `social_links`, one page of articles, `page` and `has_next_page`.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. rosalie-newcombe; `url` (string, optional) — Canonical gamesradar.com/author/<slug> URL, optionally with a /page/<n> segment; alternative to slug

### `gamesradar_headlines`

- **HTTP:** `GET /gamesradar/headlines`
- **What:** Get GamesRadar+ section headlines. Returns the latest GamesRadar+ headlines for one section. `section` is required and takes one of 21 slugs such as `games`, `games-reviews`, `hardware-news`, `entertainment-tv`, `lego` or `dungeons-and-dragons`. Each item has its title, URL and `type`, plus publication time, author and image when the section page shows them.
- **Params:** `section` (string, **required**) — GamesRadar+ section slug

### `gamesradar_news`

- **HTTP:** `GET /gamesradar/news`
- **What:** Get GamesRadar+ top stories. Returns the current GamesRadar+ top stories. Each item has its title, URL, summary, publication time, author and image. Takes no parameters; use `gamesradar-headlines` for a single games, hardware or entertainment section.
- **Params:** _none_

### `gamesradar_sections`

- **HTTP:** `GET /gamesradar/sections`
- **What:** Get GamesRadar+ sections. Lists the 21 GamesRadar+ sections accepted by `gamesradar-headlines`, from top-level hubs like `games`, `hardware` and `entertainment` to sub-sections such as `games-guides`, `hardware-reviews` and `entertainment-streaming`. Each entry has the `slug`, `name` and `url`.
- **Params:** _none_

## GB News (5)

### `gbnews_article`

- **HTTP:** `GET /gbnews/article`
- **What:** Get GB News article content. Returns one GB News story by its `gbnews.com` `url` (news, opinion or sport; query strings are ignored). The response has the title, description, publish and update times, section label, authors, lead image and body `paragraphs`, without captions or widgets. `paywalled` is never set. Video, audio, author and hub pages return an error.
- **Params:** `url` (string, **required**) — Canonical GB News story URL

### `gbnews_author`

- **HTTP:** `GET /gbnews/author`
- **What:** Get a GB News author profile. Returns one GB News author's public profile: name, role, biography, image, and their most recent stories (up to 24; older stories are not available).
- **Params:** `slug` (string, optional) — Author slug, e.g. peter-stevens-a; `url` (string, optional) — Canonical gbnews.com/authors/<slug> URL; alternative to slug

### `gbnews_headlines`

- **HTTP:** `GET /gbnews/headlines`
- **What:** Get GB News section headlines. Returns the latest GB News headlines for one section or topic. `section` is required and takes a site path such as `news`, `news/uk/london`, `news/world/ukraine`, `news/us` or `news/migrant-crisis`; the accepted values are listed by `gbnews-sections`. Each item has its title, URL, summary, publication time, author and image.
- **Params:** `section` (string, **required**) — GB News section or topic path

### `gbnews_news`

- **HTTP:** `GET /gbnews/news`
- **What:** Get GB News top stories. Returns the latest 30 GB News top stories. Each item has a title, canonical URL, summary (the story's first paragraph), publication time, author name and lead image, when GB News provides them. Takes no parameters.
- **Params:** _none_

### `gbnews_sections`

- **HTTP:** `GET /gbnews/sections`
- **What:** Get GB News sections. Lists the 390 GB News sections and topics accepted by `gbnews-headlines`. Each entry has a `slug` that is the path on the site, such as `news/uk/scotland` or `news/world/china`, a display `name` and the feed `url`. Takes no parameters.
- **Params:** _none_

## GhanaWeb (9)

### `ghanaweb_archive`

- **HTTP:** `GET /ghanaweb/archive`
- **What:** List GhanaWeb archive article URLs. Returns paginated canonical article URLs from one month sitemap. Discover accepted month values from ghanaweb-archive-months; the service only fetches child sitemap URLs derived from that official index.
- **Params:** `limit` (integer, optional) — Items per page, 1–100 (default 50); `month` (string, **required**) — A YYYYMM value returned by ghanaweb-archive-months; `page` (integer, optional) — Page number (default 1)

### `ghanaweb_archive_months`

- **HTTP:** `GET /ghanaweb/archive/months`
- **What:** Discover GhanaWeb archive months. Lists the `YYYYMM` months currently available in GhanaWeb's article archive, each with the time it was last updated. Use a returned month with the GhanaWeb archive endpoint; the set grows over time. It takes no parameters.
- **Params:** _none_

### `ghanaweb_article`

- **HTTP:** `GET /ghanaweb/article`
- **What:** Get GhanaWeb article content. Returns public article metadata and readable body paragraphs. GhanaWeb's JSON-LD identifies the publisher rather than person authors, so authors are omitted.
- **Params:** `url` (string, **required**) — Canonical GhanaWeb article URL ending in its numeric story ID

### `ghanaweb_headlines`

- **HTTP:** `GET /ghanaweb/headlines`
- **What:** Get GhanaWeb section headlines. Returns the article cards currently listed on one GhanaWeb section. `section` is required and takes one of 15 slugs such as `news`, `sports`, `crime`, `tabloid` or `regional`. Each item has its `title`, `url` and, when the card shows one, `image_url`. Summary, author and publication time are not returned.
- **Params:** `section` (string, **required**) — Section slug from ghanaweb-sections

### `ghanaweb_news`

- **HTTP:** `GET /ghanaweb/news`
- **What:** Get GhanaWeb latest stories. Lists GhanaWeb's current stories across the site, with no parameters. Each item carries its headline as `title`, the canonical article `url` and the `published_at` time. No author, summary or image is returned.
- **Params:** _none_

### `ghanaweb_sections`

- **HTTP:** `GET /ghanaweb/sections`
- **What:** Get GhanaWeb article sections. Lists the 15 article sections GhanaWeb accepts for `ghanaweb-headlines`, from `news` and `sports` to `tabloid`, `lifestyle` and `features`. Each entry has a `slug`, display `name` and section `url`. Video and other non-article areas are left out.
- **Params:** _none_

### `ghanaweb_video`

- **HTTP:** `GET /ghanaweb/video`
- **What:** Get GhanaWeb TV video metadata. Returns metadata for one GhanaWeb TV video by its required numeric `id`: title, page URL, image URL, published and updated times, and the YouTube embed URL. The video file itself is not returned.
- **Params:** `id` (string, **required**) — Numeric GhanaWeb TV video ID

### `ghanaweb_video_sections`

- **HTTP:** `GET /ghanaweb/video-sections`
- **What:** Get GhanaWeb TV video sections. Lists the four GhanaWeb TV video categories accepted by `ghanaweb-videos`: `news`, `sports`, `business` and `entertainment`. Each entry has a `slug`, a display `name` and the category `url` on GhanaWeb. Takes no parameters.
- **Params:** _none_

### `ghanaweb_videos`

- **HTTP:** `GET /ghanaweb/videos`
- **What:** List GhanaWeb TV videos. Returns current public video cards for one GhanaWeb TV category, including metadata and a canonical detail URL. This endpoint does not retrieve video media.
- **Params:** `section` (string, **required**) — Video category from ghanaweb-video-sections

## Gizmodo (5)

### `gizmodo_article`

- **HTTP:** `GET /gizmodo/article`
- **What:** Get Gizmodo article content. Returns public Gizmodo article metadata and body paragraphs from a canonical article URL. Gizmodo articles are free to read, so the full body is returned.
- **Params:** `url` (string, **required**) — Canonical Gizmodo article URL

### `gizmodo_author`

- **HTTP:** `GET /gizmodo/author`
- **What:** Get a Gizmodo author profile. Returns a Gizmodo author's name, job title, biography, headshot, social links, and most recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical Gizmodo author URL

### `gizmodo_headlines`

- **HTTP:** `GET /gizmodo/headlines`
- **What:** Get Gizmodo section headlines. Returns the latest Gizmodo headlines for one section. `section` is required and takes a slug such as `gadgets`, `artificial-intelligence`, `io9`, `science` or `deals`; any other value returns an invalid-params error. Each item has its title, URL, summary, publication time, author and image. Use `gizmodo-sections` to list the slugs.
- **Params:** `section` (string, **required**) — Gizmodo section slug

### `gizmodo_news`

- **HTTP:** `GET /gizmodo/news`
- **What:** Get Gizmodo top stories. Returns Gizmodo's current top stories from the main site-wide listing, with no parameters. Each item has its title, URL, summary, publication time, author and lead image.
- **Params:** _none_

### `gizmodo_sections`

- **HTTP:** `GET /gizmodo/sections`
- **What:** Get Gizmodo sections. Returns the Gizmodo section inventory: its five top-level verticals (Tech, Science, io9, Earther, Reviews), their sub-topics, and Deals, each linking to its public RSS feed. Every slug is accepted by the headlines endpoint.
- **Params:** _none_

## Global News (5)

### `globalnews_article`

- **HTTP:** `GET /globalnews/article`
- **What:** Get Global News article content. Returns one Global News article by `url`, a canonical `globalnews.ca` link of the form `/news/<id>/<slug>/` or `/the-curator/<id>/<slug>/`. The response has the title, description, section, authors, lead image, publish and update times, the body as `paragraphs`, and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Global News article URL

### `globalnews_author`

- **HTTP:** `GET /globalnews/author`
- **What:** Get a Global News author profile. Returns a Global News author profile by `url`, a canonical `https://globalnews.ca/author/<slug>/` link. The response has the author's `name`, `biography`, `image_url` and a list of recent articles. `title`, `image_url` and `biography` appear only if the author page shows them, and each article's `published_at` is relative text such as `2 hours` or `Sep 16`, not a timestamp.
- **Params:** `url` (string, **required**) — Canonical Global News author URL

### `globalnews_headlines`

- **HTTP:** `GET /globalnews/headlines`
- **What:** Get Global News section headlines. Returns recent Global News headlines for one section. `section` is required and takes a slug such as `canada`, `world`, `money`, `us-news`, `the-curator` or a local-station slug like `toronto` or `calgary`. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them.
- **Params:** `section` (string, **required**) — Global News RSS section slug

### `globalnews_news`

- **HTTP:** `GET /globalnews/news`
- **What:** Get Global News top stories. Returns the latest top stories from Global News (globalnews.ca), with no parameters. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them, so it works as a quick check on what the outlet is leading with.
- **Params:** _none_

### `globalnews_sections`

- **HTTP:** `GET /globalnews/sections`
- **What:** Get Global News RSS sections. Returns the public Global News RSS section inventory used by the headlines endpoint, covering topical sections and every regional/city hub with its own feed.
- **Params:** _none_

## GlobeAndMail (5)

### `globeandmail_article`

- **HTTP:** `GET /globeandmail/article`
- **What:** Get a Globe and Mail article's content. Returns one public Globe and Mail article's metadata and full body paragraphs from a canonical article URL. The Globe and Mail runs a metered paywall on most staff-bylined stories; those return a 403 permission error rather than a truncated or fabricated body -- see the endpoint markdown for the exact detection method.
- **Params:** `url` (string, **required**) — Canonical Globe and Mail article URL

### `globeandmail_author`

- **HTTP:** `GET /globeandmail/author`
- **What:** Get a Globe and Mail reporter profile. Returns one Globe and Mail reporter's public profile: name, job title, location, biography, headshot, contact/social links, and their recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical Globe and Mail author URL

### `globeandmail_headlines`

- **HTTP:** `GET /globeandmail/headlines`
- **What:** Get the latest stories in a Globe and Mail section. Returns the current public feed for one Globe and Mail section: each story's title, canonical URL, summary, author, publication time, and lead image. Section must be one of the slugs returned by /globeandmail/sections: `canada`, `world`, `business`, `investing`, `personal-finance`, `politics`, `opinion`, `culture`, `sports`, `life`, `real-estate`, `drive`.
- **Params:** `section` (string, **required**) — Globe and Mail section slug from /globeandmail/sections

### `globeandmail_news`

- **HTTP:** `GET /globeandmail/news`
- **What:** Get the latest Globe and Mail stories. Returns The Globe and Mail's current public top-stories feed: each story's title, canonical URL, summary, author, publication time, and lead image.
- **Params:** _none_

### `globeandmail_sections`

- **HTTP:** `GET /globeandmail/sections`
- **What:** List Globe and Mail sections. Lists every Globe and Mail section accepted by /globeandmail/headlines, with its slug, display name, and landing-page URL. This is the full public, RSS-backed section taxonomy from the site's primary navigation.
- **Params:** _none_

## GMA News (4)

### `gmanews_article`

- **HTTP:** `GET /gmanews/article`
- **What:** Get GMA News article content. Returns public GMA News Online article metadata and body paragraphs from a canonical article URL. GMA News articles are free to read; no content is paywalled.
- **Params:** `url` (string, **required**) — Canonical GMA News article URL

### `gmanews_headlines`

- **HTTP:** `GET /gmanews/headlines`
- **What:** Get GMA News section headlines. Returns up to 15 of the newest GMA News Online stories for one section, newest first. `section` is required and takes one of 44 slugs such as `topstories-world`, `money-economy`, `sports-nba` or `showbiz`. Each item has `title`, `url`, `summary`, `published_at` (UTC) and `image_url`. Quiet sections can return only a few items. An invalid or missing `section` returns 400.
- **Params:** `section` (string, **required**) — GMA News section slug

### `gmanews_news`

- **HTTP:** `GET /gmanews/news`
- **What:** Get GMA News top stories. Returns fresh GMA News Online top stories from the public top-stories RSS feed, with title, URL, summary, publish time, and thumbnail.
- **Params:** _none_

### `gmanews_sections`

- **HTTP:** `GET /gmanews/sections`
- **What:** Get GMA News sections. Lists the 44 GMA News Online sections accepted by `gmanews-headlines`, each with a `slug`, display `name` and `url`. Slugs run from `topstories` and `money` to sub-sections such as `sports-basketball` and `lifestyle-travel`. Video, photo and TV-show sections are excluded. Takes no parameters.
- **Params:** _none_

## GQ (5)

### `gq_article`

- **HTTP:** `GET /gq/article`
- **What:** Get GQ article content. Returns public GQ article metadata and body paragraphs from a canonical story URL. A story GQ marks as subscriber-only returns a 403 permission error instead of partial text.
- **Params:** `url` (string, **required**) — Canonical GQ story URL

### `gq_author`

- **HTTP:** `GET /gq/author`
- **What:** Get a GQ contributor profile. Returns a GQ contributor profile, identified by `slug` (such as `tom-ward`) or by a canonical `url`; provide exactly one. The response has the name, job title, biography, headshot, social links and one page of recent articles. `page` runs from 1 to 100 (default 1) and `has_next_page` signals more. Unknown contributors return 404.
- **Params:** `page` (integer, optional) — 1-based page of the contributor's article list (1-100); `slug` (string, optional) — Contributor slug, e.g. tom-ward; provide slug or url; `url` (string, optional) — Canonical www.gq.com/contributor/<slug> URL; alternative to slug

### `gq_headlines`

- **HTTP:** `GET /gq/headlines`
- **What:** Get GQ section headlines. Returns the story cards currently on one GQ section page. `section` is required and takes one of 11 slugs such as `style`, `grooming`, `watches` or `gqsports`. Each item has its `title`, `url`, `summary`, `author`, `image_url` and a `published_at` date (`YYYY-MM-DD`). Only `/story/` articles are listed, and fields GQ does not show are omitted.
- **Params:** `section` (string, **required**) — GQ section slug

### `gq_news`

- **HTTP:** `GET /gq/news`
- **What:** Get GQ top stories. Returns GQ's current top stories, with no parameters. Each item has its `title`, `url`, `summary`, `author`, `image_url` and `published_at` as an RFC 3339 UTC timestamp. Only `/story/` articles are included; galleries and other content types are skipped.
- **Params:** _none_

### `gq_sections`

- **HTTP:** `GET /gq/sections`
- **What:** Get GQ sections. Lists the 11 GQ sections accepted by `gq-headlines`: `culture`, `entertainment`, `fitness`, `gq-hype`, `gq-recommends`, `gqsports`, `grooming`, `politics`, `style`, `watches` and `wellness`. Each entry has a `slug`, display `name` and section `url`. Pages that list no stories are not included.
- **Params:** _none_

## Gulf News (5)

### `gulfnews_article`

- **HTTP:** `GET /gulfnews/article`
- **What:** Get Gulf News article content. Returns a Gulf News article by `url`, a canonical `gulfnews.com` link whose path ends in the `-1.<id>` suffix. The response has the title, description, section, authors, lead image, publish and update times, and body `paragraphs`. Section and author pages are rejected, and `paywalled` is omitted because sampled articles were freely readable.
- **Params:** `url` (string, **required**) — Canonical Gulf News article URL

### `gulfnews_author`

- **HTTP:** `GET /gulfnews/author`
- **What:** Get a Gulf News author profile. Returns a Gulf News author profile, identified by `slug` (such as `nathaniel-lacsina`) or by a canonical `gulfnews.com/author/<slug>` `url`; provide exactly one. The response has the name, job title, bio and the single page of recent articles on the profile, each with `title`, `url` and sometimes a `summary`. Unknown authors return not found.
- **Params:** `slug` (string, optional) — Author slug, e.g. nathaniel-lacsina; `url` (string, optional) — Canonical gulfnews.com/author/<slug> URL; alternative to slug

### `gulfnews_headlines`

- **HTTP:** `GET /gulfnews/headlines`
- **What:** Get Gulf News section headlines. Returns current Gulf News headlines for one section. `section` is required and takes one of 19 slugs such as `latest-news`, `business`, `uae`, `sport`, `living-in-uae` or `your-money`; other values return an invalid-params error. Each item has a title and canonical article URL.
- **Params:** `section` (string, **required**) — Gulf News section slug

### `gulfnews_news`

- **HTTP:** `GET /gulfnews/news`
- **What:** Get Gulf News top stories. Returns the latest Gulf News stories across all sections, with no parameters. Each item has its title, canonical article URL, publication time and lead image. The listing carries no summary text.
- **Params:** _none_

### `gulfnews_sections`

- **HTTP:** `GET /gulfnews/sections`
- **What:** Get Gulf News sections. Lists the 19 top-level Gulf News sections accepted by `gulfnews-headlines`, such as `latest-news`, `business`, `uae`, `world`, `sport` and `things-to-do`. Each entry has a `slug`, display `name` and section `url`. Sub-sections such as `business/aviation` are not separate values; their stories appear under the parent.
- **Params:** _none_

## Hindustan Times (5)

### `hindustantimes_article`

- **HTTP:** `GET /hindustantimes/article`
- **What:** Get Hindustan Times article content. Returns public Hindustan Times article metadata and body paragraphs from a canonical article URL. A story Hindustan Times marks subscriber-only (chiefly syndicated Wall Street Journal / The Economist partner content) returns a permission error instead of a body.
- **Params:** `url` (string, **required**) — Canonical Hindustan Times article URL

### `hindustantimes_author`

- **HTTP:** `GET /hindustantimes/author`
- **What:** Get a Hindustan Times author profile. Returns a Hindustan Times author's byline metadata, biography, contact/social links, and their most recent articles (the first page only) from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical Hindustan Times author URL

### `hindustantimes_headlines`

- **HTTP:** `GET /hindustantimes/headlines`
- **What:** Get Hindustan Times section headlines. Returns current Hindustan Times headlines for one section. `section` is required and takes one of 24 slugs such as `india-news`, `world-news`, `cricket`, `business`, `htcity` or `editorials`. Each item has its title, URL, summary, author, publication time and image where the site provides them.
- **Params:** `section` (string, **required**) — Hindustan Times section slug

### `hindustantimes_news`

- **HTTP:** `GET /hindustantimes/news`
- **What:** Get Hindustan Times top stories. Returns Hindustan Times' current top stories from its Latest News listing, with no parameters. Each item has its title, URL, summary, author, publication time and image where available.
- **Params:** _none_

### `hindustantimes_sections`

- **HTTP:** `GET /hindustantimes/sections`
- **What:** Get Hindustan Times sections. Lists the 24 Hindustan Times sections accepted by `hindustantimes-headlines`, including `india-news`, `world-news`, `cricket`, `real-estate`, `nri` and `editors-pick`. Each entry has a `slug`, display `name` and section `url`. Takes no parameters.
- **Params:** _none_

## Hollywood Reporter (5)

### `hollywoodreporter_article`

- **HTTP:** `GET /hollywoodreporter/article`
- **What:** Get The Hollywood Reporter article content. Returns public The Hollywood Reporter article metadata (title, author(s), published/updated dates, section, lead image) and body paragraphs from a canonical article URL.
- **Params:** `url` (string, **required**) — Canonical Hollywood Reporter article URL

### `hollywoodreporter_author`

- **HTTP:** `GET /hollywoodreporter/author`
- **What:** Get a Hollywood Reporter author profile. Returns one Hollywood Reporter staff writer or contributor's public profile: name, job title, headshot, biography, social/contact links, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page of recent articles to return; defaults to 1; `url` (string, **required**) — Canonical hollywoodreporter.com/author/<slug> URL

### `hollywoodreporter_headlines`

- **HTTP:** `GET /hollywoodreporter/headlines`
- **What:** Get The Hollywood Reporter section headlines. Returns recent Hollywood Reporter headlines for one section or editorial vertical. `section` is required and takes one of 37 slugs such as `movie-reviews`, `tv-news`, `music-industry-news`, `awards`, `heat-vision` or `thr-esq`. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them.
- **Params:** `section` (string, **required**) — Hollywood Reporter section slug

### `hollywoodreporter_news`

- **HTTP:** `GET /hollywoodreporter/news`
- **What:** Get The Hollywood Reporter top stories. Returns The Hollywood Reporter's current top entertainment-industry stories from its home feed, with no parameters. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them.
- **Params:** _none_

### `hollywoodreporter_sections`

- **HTTP:** `GET /hollywoodreporter/sections`
- **What:** Get The Hollywood Reporter sections. Returns the complete public section inventory accepted by /api/v1/hollywoodreporter/headlines (both The Hollywood Reporter's editorial categories and its named editorial verticals).
- **Params:** _none_

## How-To Geek (1)

### `howtogeek_news`

- **HTTP:** `GET /howtogeek/news`
- **What:** Get How-To Geek top stories. Returns current stories from How-To Geek's public RSS feed. Summaries are publisher teasers, not full article text. This feed-only route does not claim a complete section taxonomy or retrieve article bodies.
- **Params:** _none_

## HuffPost (5)

### `huffpost_article`

- **HTTP:** `GET /huffpost/article`
- **What:** Get HuffPost article content. Returns a HuffPost article by `url`, a canonical `huffpost.com/entry/<slug>_<type>_<id>` link. The response has the title, description, section, authors, lead image, publish and update times, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical HuffPost article URL

### `huffpost_author`

- **HTTP:** `GET /huffpost/author`
- **What:** Get a HuffPost author profile. Returns a HuffPost author or contributor profile by `url`, a canonical `https://www.huffpost.com/author/<slug>` link. The response has the name, recent articles, and, when the profile shows them, `job_title`, `image_url`, `biography` and `social_links` (platform and URL). Outside contributors often lack most of these optional fields.
- **Params:** `url` (string, **required**) — Canonical huffpost.com/author/<slug> URL

### `huffpost_headlines`

- **HTTP:** `GET /huffpost/headlines`
- **What:** Get HuffPost section headlines. Returns current HuffPost headlines for one topic hub. `section` is required and takes a slug that can include a path, such as `news/politics`, `impact/green`, `entertainment/tv`, `life/travel` or `voices/black-voices`. Each item has its title, URL and image. Summary, author and publication time are not returned.
- **Params:** `section` (string, **required**) — HuffPost section slug

### `huffpost_news`

- **HTTP:** `GET /huffpost/news`
- **What:** Get HuffPost top stories. Returns HuffPost's current top stories from its homepage, with no parameters. Each item has its title, URL and image where available. Summary, author and publication time are not returned.
- **Params:** _none_

### `huffpost_sections`

- **HTTP:** `GET /huffpost/sections`
- **What:** Get HuffPost sections. Lists the topic hubs accepted by `huffpost-headlines`, such as `news/politics`, `impact/business`, `life/travel` and `voices/latino-voices`. Each entry has a `slug`, display `name` and hub `url`. Games, Horoscopes, Newsletters and HuffPost's international editions are excluded.
- **Params:** _none_

## IGN (5)

### `ign_article`

- **HTTP:** `GET /ign/article`
- **What:** Get IGN article or review content. Returns public IGN article or review metadata and body paragraphs from a canonical article URL. Only canonical https://www.ign.com/articles/<slug> URLs are accepted; wiki, video, and game/movie/TV hub pages return an invalid-parameter error.
- **Params:** `url` (string, **required**) — Canonical IGN article or review URL

### `ign_author`

- **HTTP:** `GET /ign/author`
- **What:** Get an IGN author profile. Returns an IGN author profile by `url`, a canonical `https://www.ign.com/person/<username>` link. The response has the `username`, name, job title, location, biography, headshot, `social_links` (platform and URL) and the author's recent articles.
- **Params:** `url` (string, **required**) — Canonical www.ign.com/person/<username> URL

### `ign_headlines`

- **HTTP:** `GET /ign/headlines`
- **What:** Get IGN section headlines. Returns current IGN headlines for one section. `section` is required and takes one of `news`, `reviews`, `games`, `movies`, `tv`, `tech`, `nintendo`, `playstation`, `xbox`, `pc`, `mobile` or `comics`. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them.
- **Params:** `section` (string, **required**) — IGN section slug

### `ign_news`

- **HTTP:** `GET /ign/news`
- **What:** Get IGN top stories. Returns IGN's current top stories on gaming and entertainment, with no parameters. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them, covering games, film and TV news in one list.
- **Params:** _none_

### `ign_sections`

- **HTTP:** `GET /ign/sections`
- **What:** Get IGN sections. Lists the 12 IGN sections accepted by `ign-headlines`: `news`, `reviews`, `games`, `movies`, `tv`, `tech`, `nintendo`, `playstation`, `xbox`, `pc`, `mobile` and `comics`. Each entry has a `slug`, display `name` and `url`.
- **Params:** _none_

## The Independent (5)

### `independent_article`

- **HTTP:** `GET /independent/article`
- **What:** Get The Independent article content. Returns one The Independent article by `url`, which must be a canonical HTTPS `independent.co.uk` article link. The response has the title, description, section, authors, publication and update times, lead image URL, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical The Independent article URL

### `independent_author`

- **HTTP:** `GET /independent/author`
- **What:** Get an Independent author profile. Returns one Independent author's profile by `slug` (for example `lizzie-dearden`) or `url`; exactly one is required. The response has name, job title, bio, X/Twitter handle and the author's recent articles with title, URL, section and section URL. It is a single page of articles with no further pagination.
- **Params:** `slug` (string, optional) — Author slug, e.g. lizzie-dearden; `url` (string, optional) — Canonical independent.co.uk/author/<slug> URL; alternative to slug

### `independent_headlines`

- **HTTP:** `GET /independent/headlines`
- **What:** Get The Independent section headlines. Returns the current headlines for one The Independent section. `section` is required and takes one of 17 slugs, such as `news/uk`, `news/world`, `sport`, `voices`, `money` or `bulletin`. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them, and the response echoes the `section`.
- **Params:** `section` (string, **required**) — The Independent RSS section slug

### `independent_news`

- **HTTP:** `GET /independent/news`
- **What:** Get The Independent top stories. Returns the current top stories from The Independent. It takes no parameters. Each item has its title, URL and, where the outlet gives them, a summary, author, publication time, image URL and `type`. Use the headlines endpoint for one section.
- **Params:** _none_

### `independent_sections`

- **HTTP:** `GET /independent/sections`
- **What:** Get The Independent RSS sections. Lists the 17 The Independent section slugs that the headlines endpoint accepts, from `news` and `news/uk` to `life-style`, `voices`, `money` and `bulletin`. Each entry has a `slug`, a display `name` and a `url`.
- **Params:** _none_

## The Indian Express (5)

### `indianexpress_article`

- **HTTP:** `GET /indianexpress/article`
- **What:** Get The Indian Express article content. Returns public The Indian Express article metadata and body paragraphs from a canonical article URL. A story gated behind an Express Premium subscription returns a permission error instead of a truncated or paid body.
- **Params:** `url` (string, **required**) — Canonical The Indian Express article URL

### `indianexpress_author`

- **HTTP:** `GET /indianexpress/author`
- **What:** Get a The Indian Express author profile. Returns a The Indian Express author's profile by `url`, a canonical `indianexpress.com/profile/author/<slug>/` link: name, image URL, biography and recent articles with title, URL, summary and image. `image_url` and `biography` may be missing, and `published_at` is the page's date text such as `Sep 24, 2026 16:36 IST`, not a timestamp.
- **Params:** `url` (string, **required**) — Canonical The Indian Express author URL

### `indianexpress_headlines`

- **HTTP:** `GET /indianexpress/headlines`
- **What:** Get The Indian Express section headlines. Returns the current headlines for one The Indian Express section. `section` is required and takes a slug such as `india`, `explained`, `cities-delhi`, `entertainment-bollywood`, `sports-cricket` or `political-pulse`. Items carry title, URL, summary, author, publication time and image, and the response echoes the `section`.
- **Params:** `section` (string, **required**) — The Indian Express RSS section slug

### `indianexpress_news`

- **HTTP:** `GET /indianexpress/news`
- **What:** Get The Indian Express top stories. Returns the current top stories from The Indian Express. It takes no parameters. Each item has its title, URL and, where the outlet gives them, a summary, author, publication time, image URL and `type`. Use the headlines endpoint to read one section.
- **Params:** _none_

### `indianexpress_sections`

- **HTTP:** `GET /indianexpress/sections`
- **What:** Get The Indian Express RSS sections. Lists the The Indian Express section slugs that the headlines endpoint accepts, including `politics`, `india`, `explained`, `cities-mumbai`, `entertainment-tamil`, `lifestyle-health` and `smart-stocks`. Each entry has a `slug`, a display `name` and a section `url`.
- **Params:** _none_

## India Today (5)

### `indiatoday_article`

- **HTTP:** `GET /indiatoday/article`
- **What:** Get India Today article content. Returns public India Today article metadata and body paragraphs from a canonical story URL. Subscriber-only magazine stories return only the public teaser with paywalled set to true.
- **Params:** `url` (string, **required**) — Canonical India Today story URL

### `indiatoday_author`

- **HTTP:** `GET /indiatoday/author`
- **What:** Get an India Today author profile. Returns an India Today author profile by `url`, a canonical `https://www.indiatoday.in/author/<slug>` link; desk bylines such as `india-today-business-desk` work too. The response has the name, job title, headshot, biography and the first page of recent text stories (typically 20), each with title, URL, section, summary and image. Stories carry no dates.
- **Params:** `url` (string, **required**) — Canonical India Today author URL

### `indiatoday_headlines`

- **HTTP:** `GET /indiatoday/headlines`
- **What:** Get India Today section headlines. Returns the text stories listed on one India Today section page, typically 12 to 60. `section` is required and takes one of 35 slugs such as `top-news`, `cricket`, `markets`, `bollywood` or `fact-check`; other values return 400. Items have title, URL, `type`, summary and image when shown, but no `published_at`.
- **Params:** `section` (string, **required**) — India Today section slug

### `indiatoday_news`

- **HTTP:** `GET /indiatoday/news`
- **What:** Get India Today top stories. Returns fresh India Today top stories from its public RSS feed (text stories only; video and photo items are omitted).
- **Params:** _none_

### `indiatoday_sections`

- **HTTP:** `GET /indiatoday/sections`
- **What:** Get India Today sections. Lists the 35 India Today sections accepted by `indiatoday-headlines`, such as `top-news`, `south-india`, `markets`, `ott`, `elections` and `history-of-it`. Each entry has a `slug`, display `name` and the section page `url`. Takes no parameters.
- **Params:** _none_

## IndieWire (5)

### `indiewire_article`

- **HTTP:** `GET /indiewire/article`
- **What:** Get IndieWire article content. Returns public IndieWire article metadata (title, author(s), published/updated dates, section, lead image) and the body paragraphs an anonymous visitor sees, from a canonical article URL. Paywalled content is never bypassed; a gated story would return only its public portion.
- **Params:** `url` (string, **required**) — Canonical IndieWire article URL

### `indiewire_author`

- **HTTP:** `GET /indiewire/author`
- **What:** Get an IndieWire author profile. Returns one IndieWire staff writer or contributor's public profile: name, headshot, biography, any listed social/contact links, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page of recent articles to return; defaults to 1; `url` (string, **required**) — Canonical indiewire.com/author/<slug> URL

### `indiewire_headlines`

- **HTTP:** `GET /indiewire/headlines`
- **What:** Get IndieWire section headlines. Returns fresh headlines from one public IndieWire section feed. Gallery and list pages are omitted because they are not text articles.
- **Params:** `section` (string, **required**) — IndieWire section slug

### `indiewire_news`

- **HTTP:** `GET /indiewire/news`
- **What:** Get IndieWire top stories. Returns IndieWire's current top stories on independent film, TV and awards, with no parameters. Each item has its title, URL, one-sentence summary, author and publication time. Gallery and list pages are left out because they are not text articles.
- **Params:** _none_

### `indiewire_sections`

- **HTTP:** `GET /indiewire/sections`
- **What:** Get IndieWire sections. Lists IndieWire's 32 editorial categories accepted by `indiewire-headlines`, such as `analysis`, `box-office`, `festivals`, `interviews`, `obituary` and `trailers`. Each entry has a `slug`, display `name` and the category feed `url`. Categories nest under the roots `news`, `features`, `awards` and `criticism`.
- **Params:** _none_

## i (5)

### `inews_article`

- **HTTP:** `GET /inews/article`
- **What:** Get i article content. Returns public i article metadata (headline, description, section, authors, publish/update times, lead image) and body paragraphs from a canonical article URL.
- **Params:** `url` (string, **required**) — Canonical i article URL

### `inews_author`

- **HTTP:** `GET /inews/author`
- **What:** Get an i author profile. Returns an author profile from i (inews.co.uk) by `url`, a canonical `https://inews.co.uk/author/<slug>` link. The response has `name`, `bio`, `image_url`, `same_as` social profiles and up to about 30 recent articles, each with title, URL, summary, section and `published_at`. Paginated or non-author URLs return 400, and an unknown author returns 404.
- **Params:** `url` (string, **required**) — Canonical i author URL

### `inews_headlines`

- **HTTP:** `GET /inews/headlines`
- **What:** Get i section headlines. Returns fresh headlines from one public i section feed. The section must be a slug returned by the sections endpoint.
- **Params:** `section` (string, **required**) — i section slug

### `inews_news`

- **HTTP:** `GET /inews/news`
- **What:** Get i top stories. Returns fresh i (inews.co.uk) top stories from the site's public RSS feed, with summary, author, publish time, and lead image when present.
- **Params:** _none_

### `inews_sections`

- **HTTP:** `GET /inews/sections`
- **What:** Get i sections. Lists the 45 i sections accepted by `inews-headlines`, from `home` and `news` to `football`, `money` and `relationships`. Each entry has a `slug`, display `name` and `url`. `home` is the site-wide listing, and low-volume sections such as `golf` or `comedy` may hold only one or two items.
- **Params:** _none_

## Philippine Daily Inquirer (5)

### `inquirer_article`

- **HTTP:** `GET /inquirer/article`
- **What:** Get Philippine Daily Inquirer article content. Returns public Philippine Daily Inquirer article metadata and body paragraphs from a canonical article URL on any of its ten public news subdomains.
- **Params:** `url` (string, **required**) — Canonical Philippine Daily Inquirer article URL

### `inquirer_author`

- **HTTP:** `GET /inquirer/author`
- **What:** Get a Philippine Daily Inquirer author profile. Returns one Philippine Daily Inquirer byline's public archive page: the contributor's name and their recent articles on that subdomain, from a canonical byline URL. Byline pages are per-subdomain, so an author's articles from a different section require calling this endpoint again with that section's own byline URL.
- **Params:** `page` (integer, optional) — 1-based page number of articles to return; defaults to 1 and overrides any page number already present in url; `url` (string, **required**) — Canonical Philippine Daily Inquirer byline URL

### `inquirer_headlines`

- **HTTP:** `GET /inquirer/headlines`
- **What:** Get Philippine Daily Inquirer section headlines. Returns the latest Philippine Daily Inquirer stories for one section. `section` is required and takes `newsinfo`, `globalnation`, `business`, `sports`, `entertainment`, `lifestyle`, `technology`, `opinion`, `usa` or `cebudailynews`. Each item has its title, URL, summary, publication time, author and lead image.
- **Params:** `section` (string, **required**) — Philippine Daily Inquirer section slug

### `inquirer_news`

- **HTTP:** `GET /inquirer/news`
- **What:** Get Philippine Daily Inquirer top stories. Returns the latest top stories from the Philippine Daily Inquirer's flagship national-news site, newsinfo.inquirer.net. Takes no parameters. Each item has its title, URL, summary, publication time, author and lead image.
- **Params:** _none_

### `inquirer_sections`

- **HTTP:** `GET /inquirer/sections`
- **What:** Get Philippine Daily Inquirer sections. Lists the ten Philippine Daily Inquirer sections that `inquirer-headlines` accepts, from `newsinfo` to `cebudailynews`. Each entry has a `slug`, a display `name` and the section's `url`. Takes no parameters.
- **Params:** _none_

## Investopedia (5)

### `investopedia_article`

- **HTTP:** `GET /investopedia/article`
- **What:** Get Investopedia article content. Returns metadata (title, description, dates, section, authors, image) and body paragraphs for a public Investopedia page that uses the article template: news stories, dictionary terms (/terms/...), explainers and Q&A pages (/articles/..., /ask/answers/..., and similar), and product roundups. Section listing pages and author profiles are rejected with a 400 that names the endpoint to use instead.
- **Params:** `url` (string, **required**) — Canonical Investopedia article, term, or explainer URL

### `investopedia_author`

- **HTTP:** `GET /investopedia/author`
- **What:** Get an Investopedia author or expert profile. Returns an Investopedia writer, editor, reviewer, or expert contributor's public profile (name, job title, summary, photo, credentials such as education, location, and expertise, personal social links, biography, favorite quote) and their recent articles.
- **Params:** `url` (string, **required**) — Canonical Investopedia author URL (/<name>-<id> or /contributors/<id>/)

### `investopedia_headlines`

- **HTTP:** `GET /investopedia/headlines`
- **What:** Get Investopedia section headlines. Returns the current story list from one Investopedia section, with title, URL, byline, and image. section accepts any slug returned by GET /investopedia/sections.
- **Params:** `section` (string, **required**) — Investopedia section slug, from GET /investopedia/sections

### `investopedia_news`

- **HTTP:** `GET /investopedia/news`
- **What:** Get Investopedia latest news. Returns the newest Investopedia news stories (markets, companies, earnings, economy, government, crypto, rates, and personal finance news), with title, URL, byline, and image.
- **Params:** _none_

### `investopedia_sections`

- **HTTP:** `GET /investopedia/sections`
- **What:** Get Investopedia sections. Returns the full Investopedia section inventory (43 news, investing, banking, personal finance, economy, and reviews sections), each with a slug, display name, and public listing URL. Use a returned slug as the section parameter on GET /investopedia/headlines.
- **Params:** _none_

## IOL (5)

### `iol_article`

- **HTTP:** `GET /iol/article`
- **What:** Get IOL article content. Returns an IOL article by `url`, a canonical `iol.co.za` story link. The response has the title, description, section (the deepest in the breadcrumb, such as `Crime and Courts`), authors, lead image, publish and update times, and body `paragraphs`. Section, author, tag and search pages are rejected. `paywalled` is never set.
- **Params:** `url` (string, **required**) — Canonical IOL article URL

### `iol_author`

- **HTTP:** `GET /iol/author`
- **What:** Get an IOL author profile. Returns an IOL author profile, identified by `slug` (such as `xolile-mtembu`) or a canonical `iol.co.za/authors/<slug>/` `url`; provide exactly one. The response has the name, `role` and `image_url` when present, and up to 25 recent articles with title, URL, summary, section and a `published_date` taken from the article URL. Unknown authors return not found.
- **Params:** `slug` (string, optional) — Author slug, e.g. xolile-mtembu; `url` (string, optional) — Canonical iol.co.za/authors/<slug>/ URL; alternative to slug

### `iol_headlines`

- **HTTP:** `GET /iol/headlines`
- **What:** Get IOL section headlines. Returns recent IOL headlines for one section path. `section` is required and takes a value such as `news`, `news/south-africa/gauteng`, `sport/rugby/springboks`, `business/economy` or `entertainment/music`. Each item has its title, URL, summary, publication time and image, plus the author when the outlet names one. Unlisted values are rejected.
- **Params:** `section` (string, **required**) — IOL section path

### `iol_news`

- **HTTP:** `GET /iol/news`
- **What:** Get IOL top stories. Returns the 30 newest stories from IOL (Independent Online, South Africa), with no parameters. Each item has its title, canonical article URL, short summary, publication time, author byline and lead image.
- **Params:** _none_

### `iol_sections`

- **HTTP:** `GET /iol/sections`
- **What:** Get IOL sections. Returns the verified IOL section inventory accepted by the headlines endpoint: news, sport, business, lifestyle, entertainment, technology, motoring, travel and opinion, their sub-sections, provincial news and the sister-title feeds.
- **Params:** _none_

## Irish Independent (5)

### `irishindependent_article`

- **HTTP:** `GET /irishindependent/article`
- **What:** Get Irish Independent article content. Returns public Irish Independent article metadata (headline, description, section, authors, publish/update times, lead image) and body paragraphs from a canonical article URL. Premium articles are served to anonymous readers as a one-paragraph teaser; those are returned with paywalled set to true and only the teaser paragraph.
- **Params:** `url` (string, **required**) — Canonical Irish Independent article URL

### `irishindependent_author`

- **HTTP:** `GET /irishindependent/author`
- **What:** Get an Irish Independent author profile. Returns an Irish Independent author's name, biography, published email and social links, headshot, and their most recent articles (the first page of the profile's article list) from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical Irish Independent author URL

### `irishindependent_headlines`

- **HTTP:** `GET /irishindependent/headlines`
- **What:** Get Irish Independent section headlines. Returns fresh headlines from one public Irish Independent section feed. The section must be a slug returned by the sections endpoint.
- **Params:** `section` (string, **required**) — Irish Independent section slug

### `irishindependent_news`

- **HTTP:** `GET /irishindependent/news`
- **What:** Get Irish Independent top stories. Returns fresh Irish Independent (independent.ie) top stories from the site's public RSS feed, with summary, author, publish time, and lead image when present. Some stories are premium (subscriber) content; open them with the article endpoint to see the paywalled flag.
- **Params:** _none_

### `irishindependent_sections`

- **HTTP:** `GET /irishindependent/sections`
- **What:** Get Irish Independent sections. Returns every Irish Independent section slug accepted by the headlines endpoint (national, regional and county news, sport, business, comment, lifestyle and entertainment), with its display name and public RSS feed URL.
- **Params:** _none_

## Irish Times (5)

### `irishtimes_article`

- **HTTP:** `GET /irishtimes/article`
- **What:** Get Irish Times article content. Returns public Irish Times article metadata and body paragraphs from a canonical article URL. A subscriber-only (premium) article returns a permission error instead of its body; metered articles are returned in full.
- **Params:** `url` (string, **required**) — Canonical Irish Times article URL

### `irishtimes_author`

- **HTTP:** `GET /irishtimes/author`
- **What:** Get an Irish Times author profile. Returns an Irish Times author's name, job title, biography, headshot, contact details, and recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical Irish Times author URL

### `irishtimes_headlines`

- **HTTP:** `GET /irishtimes/headlines`
- **What:** Get Irish Times section headlines. Returns current Irish Times headlines for one section. `section` is required and takes one of 16 slugs such as `ireland`, `politics`, `your-money`, `life-style`, `motors` or `abroad`; other values return 400. Some listed articles are subscriber-only, and `irishtimes-article` returns a permission error for those.
- **Params:** `section` (string, **required**) — Irish Times section slug

### `irishtimes_news`

- **HTTP:** `GET /irishtimes/news`
- **What:** Get Irish Times top stories. Returns up to 100 current Irish Times top stories from its Irish news listing, with no parameters. Each item has its title, URL, summary, author, publication time and image where available.
- **Params:** _none_

### `irishtimes_sections`

- **HTTP:** `GET /irishtimes/sections`
- **What:** Get Irish Times sections. Lists the 16 Irish Times sections accepted by `irishtimes-headlines`: `ireland`, `opinion`, `politics`, `business`, `your-money`, `world`, `sport`, `life-style`, `health`, `technology`, `culture`, `property`, `food`, `motors`, `history` and `abroad`. Each entry has a `slug`, `name` and `url`.
- **Params:** _none_

## Jerusalem Post (6)

### `jerusalempost_article`

- **HTTP:** `GET /jerusalempost/article`
- **What:** Get Jerusalem Post article content. Returns public Jerusalem Post article metadata and free body paragraphs. If isAccessibleForFree is false, paywalled is true and body paragraphs are omitted; paid article text is not represented by feed snippets.
- **Params:** `url` (string, **required**) — Canonical Jerusalem Post article URL

### `jerusalempost_author`

- **HTTP:** `GET /jerusalempost/author`
- **What:** Get Jerusalem Post author profile. Returns a Jerusalem Post author or blogger profile by `url`, a canonical `/author/<slug>` or `/blogger/<slug>` link. The response has the profile `type`, name, `description`, `image_url` and article cards with title, URL, summary and publication time.
- **Params:** `url` (string, **required**) — Canonical Jerusalem Post /author/<slug> or /blogger/<slug> profile URL

### `jerusalempost_authors`

- **HTTP:** `GET /jerusalempost/authors`
- **What:** List Jerusalem Post author profiles. Returns the current author and blogger profile URLs discovered from the site's public Experts sitemap. This dynamic roster is intentionally exposed as a discovery endpoint.
- **Params:** _none_

### `jerusalempost_headlines`

- **HTTP:** `GET /jerusalempost/headlines`
- **What:** Get Jerusalem Post section headlines. Returns current Jerusalem Post stories for one section. `section` is required and takes one of 40 slugs such as `israel-news`, `iran-news`, `middle-east`, `tech-and-startups` or `torah-portion`. Each item has its title, URL, author, publication time and image, plus a summary except on premium items, which have none.
- **Params:** `section` (string, **required**) — Jerusalem Post section slug

### `jerusalempost_news`

- **HTTP:** `GET /jerusalempost/news`
- **What:** Get Jerusalem Post top stories. Returns recent Jerusalem Post front-page stories, with no parameters. Each item has its title, URL, author, publication time and image where available. Premium items keep their title and metadata but have no summary. Use `jerusalempost-article` to read an article and check its paywall flag.
- **Params:** _none_

### `jerusalempost_sections`

- **HTTP:** `GET /jerusalempost/sections`
- **What:** Get Jerusalem Post section inventory. Lists the 40 English-language editorial sections accepted by `jerusalempost-headlines`, such as `world-news`, `israel-politics`, `archaeology` and `jewish-holidays`. Each entry has a `slug`, display `name` and section `url`. Takes no parameters.
- **Params:** _none_

## Khaleej Times (5)

### `khaleejtimes_article`

- **HTTP:** `GET /khaleejtimes/article`
- **What:** Get Khaleej Times article content. Returns public Khaleej Times article metadata and body paragraphs from a canonical article URL. Live-blog pages are accepted and return their timestamped update headlines as paragraphs.
- **Params:** `url` (string, **required**) — Canonical Khaleej Times article URL

### `khaleejtimes_author`

- **HTTP:** `GET /khaleejtimes/author`
- **What:** Get a Khaleej Times author profile. Returns a Khaleej Times author's name, photo, biography, and most recent articles (first page) from a canonical author profile URL.
- **Params:** `url` (string, **required**) — Canonical Khaleej Times author URL

### `khaleejtimes_headlines`

- **HTTP:** `GET /khaleejtimes/headlines`
- **What:** Get Khaleej Times section headlines. Returns current Khaleej Times headlines for one section or sub-section. `section` is required; its slug is the section's URL path with slashes turned into hyphens, so `/business/markets` is `business-markets`. Top-level sections mix their sub-sections' stories. Each item has its title, URL and publication time, plus summary, author and image when the outlet provides them. Call `khaleejtimes-sections` for the slugs.
- **Params:** `section` (string, **required**) — Khaleej Times section slug

### `khaleejtimes_news`

- **HTTP:** `GET /khaleejtimes/news`
- **What:** Get Khaleej Times top stories. Returns fresh Khaleej Times top stories from its public Google News sitemap (the site publishes no RSS feed). Video, partner-content, and section pages are left out.
- **Params:** _none_

### `khaleejtimes_sections`

- **HTTP:** `GET /khaleejtimes/sections`
- **What:** Get Khaleej Times sections. Returns the public Khaleej Times section inventory used by the headlines endpoint. A section slug is its URL path with slashes turned into hyphens (for example business-markets for /business/markets).
- **Params:** _none_

## Kotaku (5)

### `kotaku_article`

- **HTTP:** `GET /kotaku/article`
- **What:** Get Kotaku article content. Returns public Kotaku article metadata and body paragraphs from a canonical article URL. Kotaku articles are free to read, so the full body is returned.
- **Params:** `url` (string, **required**) — Canonical Kotaku article URL

### `kotaku_author`

- **HTTP:** `GET /kotaku/author`
- **What:** Get a Kotaku author profile. Returns a Kotaku author profile by `url`, a canonical `https://kotaku.com/author/<slug>` link. The response has the `name`, `biography`, `image_url`, `social_links` (a `type` label and URL) and recent articles. The article `published_at` is the page's own date text, such as `Published September 23, 2026 at 11:20 am`, not a timestamp.
- **Params:** `url` (string, **required**) — Canonical Kotaku author URL

### `kotaku_headlines`

- **HTTP:** `GET /kotaku/headlines`
- **What:** Get Kotaku section headlines. Returns recent Kotaku headlines for one section. `section` is required and takes one of 17 slugs such as `news`, `reviews`, `games`, `game-tips`, `retro`, `horror` or `deals`. Each item has its title, URL, summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Kotaku section slug

### `kotaku_news`

- **HTTP:** `GET /kotaku/news`
- **What:** Get Kotaku top stories. Returns Kotaku's current top gaming stories, with no parameters. Each item has its title, URL, summary, author, publication time and image where Kotaku provides them. Use `kotaku-headlines` for a single section instead.
- **Params:** _none_

### `kotaku_sections`

- **HTTP:** `GET /kotaku/sections`
- **What:** Get Kotaku sections. Returns the Kotaku section inventory: Entertainment (with its Action, Fantasy, Horror, Sci-Fi, and Superhero sub-topics), Reviews, the Culture umbrella's own sub-topics (News, Retro, Kotaku Game Diary, YouTube, Odds and Ends, Feature, Fine Art), Tips & Guides, Games, and Deals, each linking to its public RSS feed. Every slug is accepted by the headlines endpoint.
- **Params:** _none_

## Mint (5)

### `livemint_article`

- **HTTP:** `GET /livemint/article`
- **What:** Get Mint article content. Returns public Mint article metadata and body paragraphs from a canonical article URL. A story Mint marks "Mint Premium" returns a permission error instead of a body.
- **Params:** `url` (string, **required**) — Canonical Mint article URL

### `livemint_author`

- **HTTP:** `GET /livemint/author`
- **What:** Get a Mint author profile. Returns a Mint author profile from a required `url` in the form `https://www.livemint.com/authors/<slug>`. The response has `name`, `job_title`, `biography`, `image_url` and Twitter, Facebook, LinkedIn and Instagram links, each present only when the profile carries it. It does not list the author's articles.
- **Params:** `url` (string, **required**) — Canonical Mint author URL

### `livemint_headlines`

- **HTTP:** `GET /livemint/headlines`
- **What:** Get Mint section headlines. Returns recent Mint headlines for one section. `section` is required and takes one of 15 slugs, including `companies`, `markets`, `money`, `ai` and `videos`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Mint section slug

### `livemint_news`

- **HTTP:** `GET /livemint/news`
- **What:** Get Mint top stories. Returns the current Mint (livemint.com) top stories, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. For one topic area, use `livemint-headlines` with a `section`.
- **Params:** _none_

### `livemint_sections`

- **HTTP:** `GET /livemint/sections`
- **What:** Get Mint sections. Lists the 15 Mint section slugs accepted by `livemint-headlines`, such as `companies`, `markets`, `money`, `budget` and `videos`. Each entry has its `slug`, display `name` and page `url`.
- **Params:** _none_

## Liverpool Echo (5)

### `liverpoolecho_article`

- **HTTP:** `GET /liverpoolecho/article`
- **What:** Get Liverpool Echo article content. Returns public Liverpool Echo article metadata (including the section) and body paragraphs from a canonical article URL. Photo-gallery URLs are rejected.
- **Params:** `url` (string, **required**) — Canonical Liverpool Echo article URL

### `liverpoolecho_author`

- **HTTP:** `GET /liverpoolecho/author`
- **What:** Get a Liverpool Echo author profile. Returns one Liverpool Echo author's public profile: name, job title, bio, email, X/Twitter handle, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page number of the author's article list (1 to 100); overrides any pageNumber in url; `slug` (string, optional) — Author slug, e.g. wesley-holmes; `url` (string, optional) — Canonical liverpoolecho.co.uk/authors/<slug>/ URL; alternative to slug

### `liverpoolecho_headlines`

- **HTTP:** `GET /liverpoolecho/headlines`
- **What:** Get Liverpool Echo section headlines. Returns fresh headlines from one public Liverpool Echo section. Photo galleries are omitted because they have no readable article body.
- **Params:** `section` (string, **required**) — Liverpool Echo section slug

### `liverpoolecho_news`

- **HTTP:** `GET /liverpoolecho/news`
- **What:** Get Liverpool Echo top stories. Returns fresh Liverpool Echo top stories from the public home RSS feed. Photo galleries are omitted because they have no readable article body.
- **Params:** _none_

### `liverpoolecho_sections`

- **HTTP:** `GET /liverpoolecho/sections`
- **What:** Get Liverpool Echo sections. Lists the Liverpool Echo sections accepted by `liverpoolecho-headlines`, such as `news/liverpool-news`, `sport/football/transfer-news`, `whats-on/theatre-news` and `in-your-area`. Each entry has a `slug`, display `name` and feed `url`. Each listed section had at least one current entry when last checked, and feeds hold up to about 25 entries.
- **Params:** _none_

## Live Science (5)

### `livescience_article`

- **HTTP:** `GET /livescience/article`
- **What:** Get Live Science article content. Returns a Live Science article by `url`, a canonical HTTPS `livescience.com` article link. The response has the title, description, section, authors, lead image, publish and update times, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Live Science article URL

### `livescience_author`

- **HTTP:** `GET /livescience/author`
- **What:** Get a Live Science author profile. Returns one Live Science author's public profile: name, job title, biography, social links, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page number of the author's article list; overrides any page number embedded in url; `slug` (string, optional) — Author slug, e.g. ben-turner; `url` (string, optional) — Canonical livescience.com/author/<slug> URL, optionally with a /page/<n> segment; alternative to slug

### `livescience_headlines`

- **HTTP:** `GET /livescience/headlines`
- **What:** Get Live Science section headlines. Returns current Live Science headlines for one section. `section` is required and takes one of 14 slugs: `animals`, `archaeology`, `chemistry`, `features`, `health`, `human-behavior`, `interviews`, `news`, `opinion`, `physics-mathematics`, `planet-earth`, `products`, `space` or `technology`. Each item has a title and URL, plus author, publication time and image when the section page shows them.
- **Params:** `section` (string, **required**) — Live Science section slug

### `livescience_news`

- **HTTP:** `GET /livescience/news`
- **What:** Get Live Science top stories. Returns Live Science's current top stories across the site, with no parameters. Each item has its title, URL, summary, author, publication time and image where available. Use `livescience-headlines` to narrow to one section.
- **Params:** _none_

### `livescience_sections`

- **HTTP:** `GET /livescience/sections`
- **What:** Get Live Science sections. Lists the 14 top-level Live Science sections accepted by `livescience-headlines`, including `animals`, `archaeology`, `human-behavior`, `physics-mathematics`, `planet-earth` and `space`. Each entry has a `slug`, display `name` and section `url`.
- **Params:** _none_

## MacRumors (5)

### `macrumors_article`

- **HTTP:** `GET /macrumors/article`
- **What:** Get MacRumors article content. Returns a MacRumors article by `url`: a dated news post, or a `/guide/`, `/how-to/` or `/review/` page. The response has the title, description, section, authors, lead image, publish time, `updated_at` and body `paragraphs`. Roundup, author and forum URLs are rejected. Reviews have no `updated_at`, and `paywalled` is omitted.
- **Params:** `url` (string, **required**) — Canonical MacRumors article URL

### `macrumors_author`

- **HTTP:** `GET /macrumors/author`
- **What:** Get a MacRumors author profile. Returns a MacRumors author profile, identified by `slug` (such as `juli-clover`) or a canonical `macrumors.com/author/<slug>` `url`; provide exactly one. The response has the name, `bio`, `image_url` and about 20 recent articles with title, URL, publication time and, when shown, summary and image. Unknown authors return not found.
- **Params:** `slug` (string, optional) — Author slug, e.g. juli-clover; `url` (string, optional) — Canonical macrumors.com/author/<slug> URL; alternative to slug

### `macrumors_headlines`

- **HTTP:** `GET /macrumors/headlines`
- **What:** Get MacRumors section headlines. Returns the newest 20 MacRumors entries for one section. `section` is required and takes `front-page`, `guides`, `how-to` or `reviews`; other values return an invalid-params error. Each item has its title, URL, author, publication time and short summary. Items from `guides`, `how-to` and `reviews` also carry a thumbnail `image_url`.
- **Params:** `section` (string, **required**) — MacRumors section slug

### `macrumors_news`

- **HTTP:** `GET /macrumors/news`
- **What:** Get MacRumors top stories. Returns the latest 20 stories across MacRumors, with no parameters. Each item has its title, canonical article URL, author, publication time and a plain-text summary of about 300 characters. Items carry no lead image.
- **Params:** _none_

### `macrumors_sections`

- **HTTP:** `GET /macrumors/sections`
- **What:** Get MacRumors sections. Lists the four MacRumors sections accepted by `macrumors-headlines`: `front-page` (all stories mixed), `guides`, `how-to` and `reviews`. Each entry has a `slug`, display `name` and `url`. Roundups, the Buyer's Guide and the forums are not sections.
- **Params:** _none_

## MarketWatch (5)

### `marketwatch_article`

- **HTTP:** `GET /marketwatch/article`
- **What:** Get MarketWatch article content. Returns a MarketWatch article by `url`, a canonical HTTPS article link. The response has the title, description, section, authors, lead image, publish and update times, body `paragraphs` and a `paywalled` flag. Subscriber-only or blocked articles return an upstream error, so some URLs may fail.
- **Params:** `url` (string, **required**) — Canonical MarketWatch article URL

### `marketwatch_author`

- **HTTP:** `GET /marketwatch/author`
- **What:** Get a MarketWatch author profile. Returns a MarketWatch author profile, identified by `slug` (such as `hannah-pedone`) or a canonical `marketwatch.com/author/<slug>` `url`; provide exactly one. The response has the name, job title, bio, `works_for` and one page of recent articles with title and URL. The `?mod=` attribution query is removed from article URLs.
- **Params:** `slug` (string, optional) — Author slug, e.g. hannah-pedone; `url` (string, optional) — Canonical marketwatch.com/author/<slug> URL; alternative to slug

### `marketwatch_headlines`

- **HTTP:** `GET /marketwatch/headlines`
- **What:** Get MarketWatch section headlines. Returns current MarketWatch headlines for one section. `section` is required and takes `latest-news`, `markets`, `investing`, `personal-finance`, `economy-politics`, `technology`, `retirement` or `real-estate`. Each item has its title, URL, summary, author, publication time and image where available.
- **Params:** `section` (string, **required**) — MarketWatch section slug

### `marketwatch_news`

- **HTTP:** `GET /marketwatch/news`
- **What:** Get MarketWatch top stories. Returns MarketWatch's current top stories, with no parameters. Each item has its title, URL, summary, author, publication time and image where available. Use `marketwatch-headlines` to read a single section instead.
- **Params:** _none_

### `marketwatch_sections`

- **HTTP:** `GET /marketwatch/sections`
- **What:** Get MarketWatch sections. Lists the eight MarketWatch sections accepted by `marketwatch-headlines`: `latest-news`, `markets`, `investing`, `personal-finance`, `economy-politics`, `technology`, `retirement` and `real-estate`. Each entry has a `slug`, display `name` and section `url`.
- **Params:** _none_

## Mashable (5)

### `mashable_article`

- **HTTP:** `GET /mashable/article`
- **What:** Get Mashable article content. Returns public Mashable article metadata and body paragraphs from a canonical article URL. Mashable articles are free to read, so the full body is returned.
- **Params:** `url` (string, **required**) — Canonical Mashable article URL

### `mashable_author`

- **HTTP:** `GET /mashable/author`
- **What:** Get a Mashable author profile. Returns one Mashable author's public profile (name, job title, biography, image, social links) plus one page of their recent articles. Profile fields are only present on page 1.
- **Params:** `page` (integer, optional) — 1-based page number of the article list; `slug` (string, optional) — Author slug, e.g. amanda-yeo; `url` (string, optional) — Canonical mashable.com/author/<slug> URL; alternative to slug

### `mashable_headlines`

- **HTTP:** `GET /mashable/headlines`
- **What:** Get Mashable section headlines. Returns fresh Mashable headlines from one public category RSS feed. Sponsored partner posts, shopping roundups, reviews, and video pages are not included.
- **Params:** `section` (string, **required**) — Mashable category slug

### `mashable_news`

- **HTTP:** `GET /mashable/news`
- **What:** Get Mashable top stories. Returns fresh Mashable top stories from the public all-stories RSS feed. Mashable articles are free to read; sponsored partner posts, shopping roundups, reviews, and video pages are not included.
- **Params:** _none_

### `mashable_sections`

- **HTTP:** `GET /mashable/sections`
- **What:** Get Mashable sections. Returns the public Mashable category taxonomy accepted by the headlines endpoint. Only categories that publish a working public RSS feed are listed.
- **Params:** _none_

## Mediaite (5)

### `mediaite_article`

- **HTTP:** `GET /mediaite/article`
- **What:** Get Mediaite article content. Returns public Mediaite article metadata and body paragraphs from a canonical article URL. Mediaite One Sheet (premium) pages are flagged paywalled.
- **Params:** `url` (string, **required**) — Canonical Mediaite article URL

### `mediaite_author`

- **HTTP:** `GET /mediaite/author`
- **What:** Get a Mediaite author profile. Returns a Mediaite author profile by `slug` (for example `michael-luciano`) or by a mediaite.com author `url`; supply exactly one. The response has `name`, `bio`, `avatar_url`, `email`, `twitter` and about 10 recent articles, each with `title`, `url` and a short `date` label such as `Sep 24th` (no year or time). Contact fields are omitted when the page shows none.
- **Params:** `slug` (string, optional) — Author slug, e.g. michael-luciano; `url` (string, optional) — Canonical mediaite.com/author/<slug>/ URL; alternative to slug

### `mediaite_headlines`

- **HTTP:** `GET /mediaite/headlines`
- **What:** Get Mediaite section headlines. Returns up to 20 recent Mediaite stories for one category. `section` is required and takes a slug such as `tv`, `politics`, `opinion` or `premium`; any other value returns an invalid-parameter error. Each item has a title, URL and publication time, and may include author, summary and image.
- **Params:** `section` (string, **required**) — Mediaite category slug

### `mediaite_news`

- **HTTP:** `GET /mediaite/news`
- **What:** Get Mediaite top stories. Returns the 20 most recent Mediaite stories across the site, with no parameters. Each item has its title, canonical URL, summary, publication time and author. Use `mediaite-headlines` to read a single category instead.
- **Params:** _none_

### `mediaite_sections`

- **HTTP:** `GET /mediaite/sections`
- **What:** Get Mediaite sections. Lists the 15 Mediaite category slugs accepted as `section` by `mediaite-headlines`, such as `tv`, `politics`, `opinion` and `crime`. Each entry has its `slug`, display `name` and `url`. `premium` is the Mediaite One Sheet newsletter category, and `election-2020` is a legacy category that still publishes occasionally.
- **Params:** _none_

## Medical News Today (5)

### `medicalnewstoday_article`

- **HTTP:** `GET /medicalnewstoday/article`
- **What:** Get a Medical News Today article. Returns public article metadata and body paragraphs. No login or paywall is bypassed. URLs under the robots-disallowed /articles/mnt-* path are rejected.
- **Params:** `url` (string, **required**) — Canonical Medical News Today article URL

### `medicalnewstoday_author`

- **HTTP:** `GET /medicalnewstoday/author`
- **What:** Get a Medical News Today author profile. Returns a Medical News Today author profile by `slug` including its numeric id (for example `peter-brown-1595`) or by the profile `url`; provide one of the two. The response has the author's `name`, a `bio` when one is listed, and recent articles with title and URL, plus summary, date and image where present.
- **Params:** `slug` (string, optional) — Author slug including numeric id, e.g. peter-brown-1595; `url` (string, optional) — Public author profile URL

### `medicalnewstoday_headlines`

- **HTTP:** `GET /medicalnewstoday/headlines`
- **What:** Get Medical News Today section headlines. Returns the dated story cards from the Medical News Today Health News stream. `section` is required and currently accepts only `news`; `medicalnewstoday-sections` shows the accepted value. Each item has a title and URL, with a publication date such as `2026-09-26`, author, summary and image when the card shows them.
- **Params:** `section` (string, **required**) — Medical News Today newsroom section

### `medicalnewstoday_news`

- **HTTP:** `GET /medicalnewstoday/news`
- **What:** Get Medical News Today latest health news. Returns the current article cards from Medical News Today's Health News listing, with no parameters. Each item has a title and URL, plus publication date, author, summary and image when the card shows them. It is the way to read the latest health stories without choosing a section.
- **Params:** _none_

### `medicalnewstoday_sections`

- **HTTP:** `GET /medicalnewstoday/sections`
- **What:** Get Medical News Today newsroom sections. Returns the exact public editorial news-section value accepted by medicalnewstoday-headlines. Health Topics and Health Hubs are educational resources, not newsroom sections.
- **Params:** _none_

## Manchester Evening News (5)

### `men_article`

- **HTTP:** `GET /men/article`
- **What:** Get Manchester Evening News article content. Returns a Manchester Evening News article by `url`, a canonical HTTPS article link. The response has the title, description, section, authors, lead image, publish and update times, body `paragraphs` and a `paywalled` flag. Subscriber-only or blocked articles return an upstream error.
- **Params:** `url` (string, **required**) — Canonical Manchester Evening News article URL

### `men_author`

- **HTTP:** `GET /men/author`
- **What:** Get a Manchester Evening News author profile. Returns a Manchester Evening News author profile, identified by `slug` (such as `lee-swettenham`) or a canonical `manchestereveningnews.co.uk/authors/<slug>/` `url`; provide exactly one. The response has the name, job title, bio, `email`, `twitter` and one page of recent articles with title, URL and label. Contact fields are absent when unlisted.
- **Params:** `slug` (string, optional) — Author slug, e.g. lee-swettenham; `url` (string, optional) — Canonical manchestereveningnews.co.uk/authors/<slug>/ URL; alternative to slug

### `men_headlines`

- **HTTP:** `GET /men/headlines`
- **What:** Get Manchester Evening News section headlines. Returns current Manchester Evening News headlines for one section. `section` is required and takes a slug such as `news`, `news/greater-manchester-news`, `sport/football/transfer-news`, `whats-on/theatre-news` or `trips-and-breaks`. Each item has its title, URL, summary, publication time and image.
- **Params:** `section` (string, **required**) — Manchester Evening News section slug

### `men_news`

- **HTTP:** `GET /men/news`
- **What:** Get Manchester Evening News top stories. Returns the Manchester Evening News' current top stories, with no parameters. Each item has its title, URL, summary, author, publication time and image where available.
- **Params:** _none_

### `men_sections`

- **HTTP:** `GET /men/sections`
- **What:** Get Manchester Evening News sections. Lists the Manchester Evening News sections accepted by `men-headlines`, such as `news`, `news/uk-news`, `sport/football`, `whats-on/music-nightlife-news` and `trips-and-breaks`. Each entry has a stable `slug`, display `name` and section `url`. Takes no parameters.
- **Params:** _none_

## Metro (5)

### `metro_article`

- **HTTP:** `GET /metro/article`
- **What:** Get Metro article content. Returns public Metro article metadata (headline, description, section, authors, publish/update times, lead image) and body paragraphs from a canonical article URL. Metro articles are free to read; live-blog entries are included in the body.
- **Params:** `url` (string, **required**) — Canonical Metro article URL

### `metro_author`

- **HTTP:** `GET /metro/author`
- **What:** Get a Metro author profile. Returns a Metro author's name, job title, biography, topic areas, social links, and most recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical Metro author URL

### `metro_headlines`

- **HTTP:** `GET /metro/headlines`
- **What:** Get Metro section headlines. Returns fresh headlines from one public Metro section feed. The section must be a slug returned by the sections endpoint.
- **Params:** `section` (string, **required**) — Metro section slug

### `metro_news`

- **HTTP:** `GET /metro/news`
- **What:** Get Metro top stories. Returns fresh Metro (metro.co.uk) top stories from the site's public RSS feed, with summary, author, publish time, and lead image when present.
- **Params:** _none_

### `metro_sections`

- **HTTP:** `GET /metro/sections`
- **What:** Get Metro sections. Lists the 42 Metro section slugs accepted by `metro-headlines`, each with its display name and URL. Slugs include `uk`, `football`, `showbiz` and `coronation-street`. `home` is the site-wide stream, the same stories as `metro-news`, and parent sections such as `news` and `sport` aggregate their child sections.
- **Params:** _none_

## Mirror (5)

### `mirror_article`

- **HTTP:** `GET /mirror/article`
- **What:** Get Mirror article content. Returns a Mirror article by its canonical `url`: title, description, section, authors, lead image, publication and update times, a `paywalled` flag and the body `paragraphs`. Only public content is returned; subscriber-only or blocked articles return an upstream error.
- **Params:** `url` (string, **required**) — Canonical Mirror article URL

### `mirror_author`

- **HTTP:** `GET /mirror/author`
- **What:** Get a Mirror author profile. Returns a Mirror author profile by `slug` (for example `neil-shaw`) or by a mirror.co.uk author `url`; supply exactly one. The response has `name`, `job_title`, `bio`, `email`, `twitter` and one page of recent articles with title, URL and label. There is no paging, and unlisted contact details are omitted rather than raising an error.
- **Params:** `slug` (string, optional) — Author slug, e.g. neil-shaw; `url` (string, optional) — Canonical mirror.co.uk/authors/<slug>/ URL; alternative to slug

### `mirror_headlines`

- **HTTP:** `GET /mirror/headlines`
- **What:** Get Mirror section headlines. Returns recent Mirror headlines for one section. `section` is required and takes one of 34 slugs or paths, such as `news/uk-news`, `sport/football`, `3am` or `lifestyle/food-drink`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Mirror section slug

### `mirror_news`

- **HTTP:** `GET /mirror/news`
- **What:** Get Mirror top stories. Returns the current Mirror top stories, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `mirror-headlines` to read a single section.
- **Params:** _none_

### `mirror_sections`

- **HTTP:** `GET /mirror/sections`
- **What:** Get Mirror sections. Lists the Mirror section slugs accepted by `mirror-headlines`. Each entry has a stable `slug`, a display `name` and a section `url`. Slugs can contain a path, such as `news/uk-news` or `sport/football`.
- **Params:** _none_

## MLive (1)

### `mlive_news`

- **HTTP:** `GET /mlive/news`
- **What:** Get MLive top stories. Returns current MLive top stories, including title, canonical URL, brief summary, author, publication time, and image where available. Article pages are not currently available, and category endpoints are deferred.
- **Params:** _none_

## Moneycontrol (5)

### `moneycontrol_article`

- **HTTP:** `GET /moneycontrol/article`
- **What:** Get Moneycontrol article content. Returns public Moneycontrol article metadata and body paragraphs from a canonical article URL. Moneycontrol Pro subscriber stories are refused with a 403 permission error because no free content is available. Live blogs return one paragraph per update.
- **Params:** `url` (string, **required**) — Canonical Moneycontrol article URL

### `moneycontrol_author`

- **HTTP:** `GET /moneycontrol/author`
- **What:** Get a Moneycontrol author profile. Returns a Moneycontrol author's name, job title, biography (when present), social links, and recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical Moneycontrol author URL

### `moneycontrol_headlines`

- **HTTP:** `GET /moneycontrol/headlines`
- **What:** Get Moneycontrol section headlines. Returns the current front page of one Moneycontrol section: 25 or 50 stories, each with `title`, `url`, a short `summary` and `image_url`. `section` is required and takes one of 52 slugs such as `markets`, `ipo` or `cricket`; other values return `400`. Publication time and author are omitted, and only the first page is available.
- **Params:** `section` (string, **required**) — Moneycontrol section slug

### `moneycontrol_news`

- **HTTP:** `GET /moneycontrol/news`
- **What:** Get Moneycontrol latest news. Returns the 50 newest Moneycontrol stories across all sections, newest first, with no parameters. Each item has `title`, `url`, `published_at` (RFC3339 UTC) and `image_url`. Videos, podcasts, photo galleries and sponsored brand-connect posts are left out.
- **Params:** _none_

### `moneycontrol_sections`

- **HTTP:** `GET /moneycontrol/sections`
- **What:** Get Moneycontrol sections. Lists the 52 Moneycontrol news section slugs accepted by `moneycontrol-headlines`, such as `markets`, `economy`, `ipo` and `cricket`. Each entry has its `slug`, display `name` and page `url`. Moneycontrol Pro-only research, video, podcast and photo hubs are not sections.
- **Params:** _none_

## The Motley Fool (5)

### `motleyfool_article`

- **HTTP:** `GET /motleyfool/article`
- **What:** Get a Motley Fool article. Returns one Motley Fool investing article by `url`, which must look like `https://www.fool.com/investing/YYYY/MM/DD/slug/`; only public `/investing/` URLs are accepted. The response has the title, description, section, authors, publication and update times, image URL, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical The Motley Fool investing article URL

### `motleyfool_author`

- **HTTP:** `GET /motleyfool/author`
- **What:** Get a Motley Fool author profile. Returns a Motley Fool author's name, biography when published, image when available and recent investing articles from their author page. `url` is required, for example `https://www.fool.com/author/2104/`. Each article has a title, URL, summary, author, image, `type` and publication time.
- **Params:** `url` (string, **required**) — Canonical The Motley Fool author URL

### `motleyfool_headlines`

- **HTTP:** `GET /motleyfool/headlines`
- **What:** Get The Motley Fool section headlines. Returns the article cards of one Motley Fool investing-news section. `section` is required: `trending-news`, `news`, `market-movers`, `tech-stock-news`, `market-trends`, `crypto-news`, `markets`, `most-active-stocks`, `top-stock-gainers` or `top-stock-losers`. Other values return a 400. Items carry the title, URL and, where present, summary, author and publication time.
- **Params:** `section` (string, **required**) — The Motley Fool section slug

### `motleyfool_news`

- **HTTP:** `GET /motleyfool/news`
- **What:** Get The Motley Fool top investing stories. Returns up to 50 recent Motley Fool investing stories, newest first, each with its title, URL and publication time. Only stories at `/investing/YYYY/MM/DD/slug/` URLs are included. It takes no parameters; use the headlines endpoint for a named section.
- **Params:** _none_

### `motleyfool_sections`

- **HTTP:** `GET /motleyfool/sections`
- **What:** List The Motley Fool news sections. Lists the 10 Motley Fool Stock Market News section slugs that the headlines endpoint accepts, from `trending-news` and `news` to `most-active-stocks`, `top-stock-gainers` and `top-stock-losers`. Each entry has a `slug`, a display `name` (`news` is named Stock News) and a section `url`.
- **Params:** _none_

## Nation Africa (5)

### `nationafrica_article`

- **HTTP:** `GET /nationafrica/article`
- **What:** Get Nation Africa article content. Returns public Nation Africa article metadata and body paragraphs from a canonical article URL. paywalled is true for a Premium story: the publisher serves an anonymous reader only the opening paragraph(s), so paragraphs is a partial teaser and nothing is bypassed. Video, photo, audio, puzzle and cartoon URLs are rejected with a 400.
- **Params:** `url` (string, **required**) — Canonical Nation Africa article URL

### `nationafrica_author`

- **HTTP:** `GET /nationafrica/author`
- **What:** Get a Nation Africa author profile. Returns one Nation Africa author's public profile: name, bio, portrait and the latest stories the profile page itself lists (a handful; the site loads the full list separately and it is not read).
- **Params:** `slug` (string, optional) — Author slug, e.g. richard-munguti-11590; `url` (string, optional) — Canonical nation.africa/kenya/<author-slug> URL; alternative to slug

### `nationafrica_headlines`

- **HTTP:** `GET /nationafrica/headlines`
- **What:** Get Nation Africa section headlines. Returns the current story teasers of one public Nation Africa section page. Subscriber-only stories carry type "premium". Teasers show only a relative age, so published_at is omitted.
- **Params:** `section` (string, **required**) — Nation Africa section slug

### `nationafrica_news`

- **HTTP:** `GET /nationafrica/news`
- **What:** Get Nation Africa top stories. Returns the newest Nation Africa (Daily Nation, Kenya) stories from its public news sitemap: headline, publication time and lead image. If the sitemap returns 404, it falls back to the public News section hub, whose relative timestamps may omit publication time. Video pages are excluded.
- **Params:** _none_

### `nationafrica_sections`

- **HTTP:** `GET /nationafrica/sections`
- **What:** Get Nation Africa sections. Lists the 47 section slugs of Nation Africa's Kenya edition accepted by `nationafrica-headlines`, such as `news`, `politics`, `counties`, `football` and `fact-checks`. Each entry has its `slug`, display `name` and section page `url`. Photo, video, audio, puzzle, newsletter and cartoon pages are not included.
- **Params:** _none_

## National Post (5)

### `nationalpost_article`

- **HTTP:** `GET /nationalpost/article`
- **What:** Get National Post article content. Returns public National Post article metadata and body paragraphs from a canonical article URL. paywalled is true when the publisher marks the story subscriber-only or registration-gated; National Post gates these stories in the reader's browser but still serves the complete text to an anonymous request, so paragraphs is the whole body and nothing is bypassed. Category, tag, author and Sponsored URLs are rejected with a 400.
- **Params:** `url` (string, **required**) — Canonical National Post article URL

### `nationalpost_author`

- **HTTP:** `GET /nationalpost/author`
- **What:** Get a National Post author profile. Returns one National Post author's public profile: name, bio when the author has one, the total number of stories the page attributes to them, and their latest stories (first page).
- **Params:** `slug` (string, optional) — Author slug, e.g. stuckpostmedia-com; `url` (string, optional) — Canonical nationalpost.com/author/<slug>/ URL; alternative to slug

### `nationalpost_headlines`

- **HTTP:** `GET /nationalpost/headlines`
- **What:** Get National Post section headlines. Returns National Post headlines for one section; `section` is required and takes one of 45 slugs such as `canada`, `hockey` or `deals`. The top-level sections `health`, `opinion`, `longreads`, `modern-life`, `travel`, `entertainment`, `shopping-essentials` and `sports` return 10 stories with publication time and byline. Others return up to about 45 without either. Sponsored stories are left out.
- **Params:** `section` (string, **required**) — National Post section slug

### `nationalpost_news`

- **HTTP:** `GET /nationalpost/news`
- **What:** Get National Post top stories. Returns the latest 10 National Post stories across all sections, with no parameters. Each item has a title, canonical article URL, one-line summary, publication time and byline. Use `nationalpost-headlines` to read a single section.
- **Params:** _none_

### `nationalpost_sections`

- **HTTP:** `GET /nationalpost/sections`
- **What:** Get National Post sections. Lists the 45 National Post section slugs accepted by `nationalpost-headlines`, such as `canada`, `opinion`, `hockey` and `gift-guide`, each with its display `name` and category page `url`. Links that leave nationalpost.com (Financial Post, Driving.ca, puzzles, classifieds, e-paper) and the paid Sponsored categories are not included.
- **Params:** _none_

## NBC News (5)

### `nbc_article`

- **HTTP:** `GET /nbc/article`
- **What:** Get NBC News article content. Returns public NBC News article metadata and body paragraphs from a canonical article URL. This does not bypass login, subscription, or other access controls.
- **Params:** `url` (string, **required**) — Canonical www.nbcnews.com article URL

### `nbc_author`

- **HTTP:** `GET /nbc/author`
- **What:** Get an NBC News author profile. Returns an NBC News author's byline metadata (job title, bio, social links) and their recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical NBC News author URL

### `nbc_headlines`

- **HTTP:** `GET /nbc/headlines`
- **What:** Get NBC News section headlines. Returns recent NBC News stories for one section. `section` is required and must be one of `news`, `world`, `us-news`, `politics`, `business`, `science` or `health`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — NBC News RSS section slug: news, world, us-news, politics, business, science, or health

### `nbc_news`

- **HTTP:** `GET /nbc/news`
- **What:** Get NBC News top stories. Returns the current NBC News top stories across the site, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `nbc-headlines` to read one section.
- **Params:** _none_

### `nbc_sections`

- **HTTP:** `GET /nbc/sections`
- **What:** Get NBC News RSS sections. Lists the seven NBC News section slugs accepted by `nbc-headlines`: `news`, `world`, `us-news`, `politics`, `business`, `science` and `health`. Each entry has its `slug`, display `name` and `url`.
- **Params:** _none_

## NDTV (12)

### `ndtv_article`

- **HTTP:** `GET /ndtv/article`
- **What:** Get NDTV article content. Returns public NDTV article metadata and body paragraphs from a canonical article URL. premium is true for NDTV Premium stories; paragraphs are always the text NDTV serves on its public page.
- **Params:** `url` (string, **required**) — Canonical NDTV article URL

### `ndtv_author`

- **HTTP:** `GET /ndtv/author`
- **What:** Get an NDTV author profile. Returns an NDTV author's or news agency's byline profile (name, role, biography, image) and one page of authored news stories from a canonical author URL. Request sequential pages until articles is empty; NDTV does not expose a total count.
- **Params:** `page` (integer, optional) — 1-based authored news story page; request sequentially until articles is empty; `url` (string, **required**) — Canonical NDTV author or agency URL

### `ndtv_headlines`

- **HTTP:** `GET /ndtv/headlines`
- **What:** Get NDTV section headlines. Returns the current story cards from one NDTV section page: title, canonical URL, and, where the section shows them, summary, publication time, byline, and image.
- **Params:** `section` (string, **required**) — NDTV section slug from ndtv-sections

### `ndtv_latest_videos`

- **HTTP:** `GET /ndtv/latest-videos`
- **What:** Get NDTV latest videos. Returns one page from NDTV's separate latest-videos feed. This feed is not a category slug; use page sequentially. Results contain metadata only, with no media bytes or player URLs.
- **Params:** `page` (integer, optional) — 1-based latest-video page

### `ndtv_live_blog`

- **HTTP:** `GET /ndtv/live-blog`
- **What:** Get structured updates from an NDTV live blog. Returns the metadata and ordered updates of an NDTV live blog, given its canonical article `url`. The blog carries title, description, section, authors, image and publish and update times. Each update has its title, URL, body text, timestamps, authors and image when NDTV gives them. A regular article URL is rejected with an error.
- **Params:** `url` (string, **required**) — Canonical NDTV live-blog article URL

### `ndtv_live_blogs`

- **HTTP:** `GET /ndtv/live-blogs`
- **What:** Get NDTV live-blog index. Returns one page of public NDTV live-blog cards. Pages include only www.ndtv.com live blogs; sister-site cards are excluded. NDTV does not expose a total count or continuation marker; request sequential pages until the upstream reports not found.
- **Params:** `page` (integer, optional) — 1-based index page

### `ndtv_news`

- **HTTP:** `GET /ndtv/news`
- **What:** Get NDTV latest stories. Returns the stories NDTV published in roughly the last two days, newest first, from its public news sitemap: title, canonical URL, publication time, keywords, and lead image.
- **Params:** _none_

### `ndtv_search`

- **HTTP:** `GET /ndtv/search`
- **What:** Search NDTV news stories. Returns one page of NDTV's public news topic results (15 story cards per page). Unknown topics return 404. The result page supports no sort or filter parameters.
- **Params:** `page` (integer, optional) — 1-based result page; `query` (string, **required**) — Search terms

### `ndtv_sections`

- **HTTP:** `GET /ndtv/sections`
- **What:** Get NDTV sections. Lists the NDTV section slugs accepted by `ndtv-headlines`, each with its display name and page URL. They cover national and world news (`latest`, `india`, `world`), city and state pages such as `mumbai-news` and `kerala-news`, and topics such as `education` and `food`. `spotlight` is NDTV's Premium hub; video, podcasts and sister sites are excluded.
- **Params:** _none_

### `ndtv_video`

- **HTTP:** `GET /ndtv/video`
- **What:** Get NDTV video metadata. Returns title, description, publication time, duration, and thumbnail metadata from one canonical NDTV video page. It does not fetch or return video media or player URLs.
- **Params:** `url` (string, **required**) — Canonical NDTV video URL

### `ndtv_video_categories`

- **HTTP:** `GET /ndtv/video-categories`
- **What:** Get NDTV video categories. Returns the live-verified NDTV-hosted category slugs accepted by ndtv-videos. Categories hosted on sister domains, Shorts, and unavailable Faith are excluded.
- **Params:** _none_

### `ndtv_videos`

- **HTTP:** `GET /ndtv/videos`
- **What:** Get videos from an NDTV category. Returns one page of metadata cards from a supported NDTV-hosted video category. Use ndtv-video-categories to discover the complete supported category set; request pages sequentially. This returns no media bytes or player URLs.
- **Params:** `category` (string, **required**) — NDTV video category slug from ndtv-video-categories; `page` (integer, optional) — 1-based category result page

## News18 (5)

### `news18_article`

- **HTTP:** `GET /news18/article`
- **What:** Get News18 article content. Returns a News18 article by canonical `url` in the form `/<section>/<slug>-<id>.html`, optionally with a subsection. The response has title, description, authors, lead image, publication and update times, a `paywalled` flag and body `paragraphs`. `section` is the article's own category, so it can be a subsection such as `business/markets` that `news18-sections` does not list.
- **Params:** `url` (string, **required**) — Canonical News18 article URL

### `news18_author`

- **HTTP:** `GET /news18/author`
- **What:** Get a News18 author profile. Returns a News18 author profile from a required `url` in the form `https://www.news18.com/byline/<slug>.html`. The response has `name`, `biography`, `image_url`, `social_links` (whichever of website, X/Twitter, Facebook, Instagram, YouTube and LinkedIn are set) and recent articles with `published_at` in RFC3339 UTC. Wire and staff bylines often have no bio or links.
- **Params:** `url` (string, **required**) — Canonical News18 author URL

### `news18_headlines`

- **HTTP:** `GET /news18/headlines`
- **What:** Get News18 section headlines. Returns recent News18 stories for one section. `section` is required and takes one of 18 slugs, such as `india`, `cricket`, `elections`, `viral` or `breaking-news`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — News18 RSS section slug

### `news18_news`

- **HTTP:** `GET /news18/news`
- **What:** Get News18 top stories. Returns the current News18 top stories, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `news18-headlines` to read one section.
- **Params:** _none_

### `news18_sections`

- **HTTP:** `GET /news18/sections`
- **What:** Get News18 RSS sections. Lists the 18 News18 section slugs accepted by `news18-headlines`, such as `india`, `world`, `cricket`, `explainers` and `education-career`. Each entry has its `slug`, display `name` and `url`.
- **Params:** _none_

## News24 (4)

### `news24_article`

- **HTTP:** `GET /news24/article`
- **What:** Get News24 article content. Returns public News24 article metadata and body paragraphs from a canonical article URL. Subscriber-only articles return the standfirst as the only paragraph with paywalled set to true.
- **Params:** `url` (string, **required**) — Canonical News24 article URL

### `news24_headlines`

- **HTTP:** `GET /news24/headlines`
- **What:** Get News24 section headlines. Returns News24 headlines for one section. `section` is required and takes a path such as `business/markets`, `sport/rugby/springboks` or `politics`, from the 73 listed by `news24-sections`. Each item has a title and URL, and `type` is `subscriber` on cards News24 marks subscriber-only. Summary, author, publication time and image appear when available.
- **Params:** `section` (string, **required**) — News24 section path

### `news24_news`

- **HTTP:** `GET /news24/news`
- **What:** Get News24 top stories. Returns the current News24 top stories, with no parameters. Each item has a title, canonical URL and image. `type` is `subscriber` when News24 marks the story subscriber-only and is omitted for freely readable stories.
- **Params:** _none_

### `news24_sections`

- **HTTP:** `GET /news24/sections`
- **What:** Get News24 sections. Lists the 73 News24 sections accepted by `news24-headlines`. Each entry has a `slug` (the URL path under news24.com, which may contain `/`, as in `sport/rugby/springboks`), a display `name` and a page `url`. Top-level groups include `business`, `life`, `opinions`, `southafrica`, `sport` and `world`.
- **Params:** _none_

## News.com.au (5)

### `newscomau_article`

- **HTTP:** `GET /newscomau/article`
- **What:** Get News.com.au article content. Returns a News.com.au article by canonical `url`, which must be a `www.news.com.au` link ending in `/news-story/<32-character-id>`. The response has title, description, section, authors, lead image, publication and update times, a `paywalled` flag and body `paragraphs`. `authors` is empty for wire or agency pieces with no byline.
- **Params:** `url` (string, **required**) — Canonical News.com.au article URL

### `newscomau_author`

- **HTTP:** `GET /newscomau/author`
- **What:** Get a News.com.au author profile. Returns a News.com.au staff writer's profile (name, job title, headshot, biography, social links) and recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical News.com.au author URL

### `newscomau_headlines`

- **HTTP:** `GET /newscomau/headlines`
- **What:** Get News.com.au section headlines. Returns fresh headlines from one News.com.au section or category listing page. section accepts any slug returned by GET /newscomau/sections (236 values, too many to enumerate inline -- see that endpoint for the full, current list), for example "national" or the nested "national/nsw-act/politics".
- **Params:** `section` (string, **required**) — News.com.au section slug, from GET /newscomau/sections

### `newscomau_news`

- **HTTP:** `GET /newscomau/news`
- **What:** Get News.com.au top stories. Returns the current News.com.au top stories, with no parameters and no section filter. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** _none_

### `newscomau_sections`

- **HTTP:** `GET /newscomau/sections`
- **What:** Get News.com.au sections. Returns the full News.com.au section/category navigation inventory (236 entries as of 2026-09-23), each with a slug, display name, and public listing URL. Use a returned slug as the section parameter on GET /newscomau/headlines.
- **Params:** _none_

## Newsmax (5)

### `newsmax_article`

- **HTTP:** `GET /newsmax/article`
- **What:** Get Newsmax article content. Returns a Newsmax article by canonical `url` in the form `/<section>/<slug>/YYYY/MM/DD/id/<id>`: title, description, section, authors, lead image, publication and update times, and body `paragraphs`. `authors` may be empty for wire or staff-aggregated stories. Paywalled Platinum URLs are not accepted.
- **Params:** `url` (string, **required**) — Canonical Newsmax article URL

### `newsmax_author`

- **HTTP:** `GET /newsmax/author`
- **What:** Get a Newsmax Insiders author profile. Returns a Newsmax Insiders (opinion columnist) profile from a required `url` such as `https://www.newsmax.com/insiders/<slug>/id-<id>/`. The response has `name`, `biography`, `image_url` and recent columns. `biography` is omitted when Newsmax's separate profile page is unavailable, and article `published_at` is date text such as `Sep 23, 2026`.
- **Params:** `url` (string, **required**) — Canonical Newsmax Insiders author URL

### `newsmax_headlines`

- **HTTP:** `GET /newsmax/headlines`
- **What:** Get Newsmax section headlines. Returns recent Newsmax stories for one section. `section` is required and takes one of 20 slugs, such as `newsfront`, `politics`, `health-news`, `finance-news` or `insiders`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Newsmax RSS section slug

### `newsmax_news`

- **HTTP:** `GET /newsmax/news`
- **What:** Get Newsmax top stories. Returns the current Newsmax top stories from the Newsfront section, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `newsmax-headlines` for other sections.
- **Params:** _none_

### `newsmax_sections`

- **HTTP:** `GET /newsmax/sections`
- **What:** Get Newsmax RSS sections. Lists the 20 Newsmax section slugs accepted by `newsmax-headlines`, such as `newsfront`, `scitech`, `street-talk` and `global-talk`. Each entry has its `slug`, display `name` and `url`. `insiders` is the combined opinion section, and `finance-headlines` is the finance section's Headlines listing.
- **Params:** _none_

## Newsweek (5)

### `newsweek_article`

- **HTTP:** `GET /newsweek/article`
- **What:** Get Newsweek article content. Returns a Newsweek article by canonical `url`, which must be a `newsweek.com` link ending in a numeric article id. The response has title, description, section, authors, lead image, publication and update times, a `paywalled` flag and body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical Newsweek article URL

### `newsweek_author`

- **HTTP:** `GET /newsweek/author`
- **What:** Get a Newsweek author profile. Returns a Newsweek author profile by `slug` (for example `jennifer-fink`) or a newsweek.com authors `url`; supply exactly one. `page` selects the 1-based page of recent articles (default 1) and overrides any page in `url`. The response has `name`, `job_title`, `bio`, `email`, `image_url`, articles and `has_next_page`; a page past the end gives an empty `articles` list, not an error.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. jennifer-fink; `url` (string, optional) — Canonical newsweek.com/authors/<slug> URL, optionally with a ?page=<n> query; alternative to slug

### `newsweek_headlines`

- **HTTP:** `GET /newsweek/headlines`
- **What:** Get Newsweek section headlines. Returns recent Newsweek stories for one section. `section` is required and takes one of 21 slugs, such as `politics`, `fact-check`, `better-planet`, `personal-finance` or `my-turn`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Newsweek section slug

### `newsweek_news`

- **HTTP:** `GET /newsweek/news`
- **What:** Get Newsweek top stories. Returns the current Newsweek top stories, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `newsweek-headlines` to read one section.
- **Params:** _none_

### `newsweek_sections`

- **HTTP:** `GET /newsweek/sections`
- **What:** Get Newsweek sections. Lists the 21 Newsweek section slugs accepted by `newsweek-headlines`, such as `news`, `world`, `us`, `fact-check` and `pets`. Each entry has its `slug`, display `name` and section page `url`.
- **Params:** _none_

## The New Yorker (5)

### `newyorker_article`

- **HTTP:** `GET /newyorker/article`
- **What:** Get The New Yorker article content. Returns public The New Yorker article metadata and body paragraphs from a canonical article URL. The New Yorker uses a metered paywall: when a page marks itself as gated, only the publicly served text is returned and is_truncated is true; is_accessible_for_free reports the page's own access flag.
- **Params:** `url` (string, **required**) — Canonical The New Yorker article URL

### `newyorker_author`

- **HTTP:** `GET /newyorker/author`
- **What:** Get a The New Yorker contributor profile. Returns a The New Yorker contributor's name, photo, biography, external profile links, and the first page of their recent articles from a canonical contributor URL.
- **Params:** `url` (string, **required**) — Canonical The New Yorker contributor URL

### `newyorker_headlines`

- **HTTP:** `GET /newyorker/headlines`
- **What:** Get The New Yorker section headlines. Returns fresh headlines from one public The New Yorker section feed. Section must be one of the slugs returned by the sections endpoint.
- **Params:** `section` (string, **required**) — The New Yorker section slug

### `newyorker_news`

- **HTTP:** `GET /newyorker/news`
- **What:** Get The New Yorker top stories. Returns fresh The New Yorker top stories from its public RSS feed: title, canonical URL, summary, author, publication time, lead image, and the department label (for example "News / The Lede").
- **Params:** _none_

### `newyorker_sections`

- **HTTP:** `GET /newyorker/sections`
- **What:** List The New Yorker sections. Lists every The New Yorker section accepted by the headlines endpoint, with slug, display name, and feed URL. This is the complete set of public text-article feeds the publisher serves; cartoon, podcast, video, and puzzle feeds are not included.
- **Params:** _none_

## 9to5Mac (5)

### `ninetofivemac_article`

- **HTTP:** `GET /ninetofivemac/article`
- **What:** Get 9to5Mac article content. Returns a 9to5Mac article by `url`, a canonical `9to5mac.com` address in the form `/YYYY/MM/DD/<slug>/`: title, description, publication and update times, `authors`, `section`, image and the body `paragraphs`. The affiliate FTC disclaimer and embedded-tweet text are left out, and `paywalled` is never set because the articles are free.
- **Params:** `url` (string, **required**) — Canonical 9to5Mac article URL

### `ninetofivemac_author`

- **HTTP:** `GET /ninetofivemac/author`
- **What:** Get a 9to5Mac author profile. Returns a 9to5Mac author profile from `url`, a canonical `https://9to5mac.com/author/<slug>/` address: name, avatar, `biography`, `social_links` and the first page of recent articles. Each social link's `type` comes from the page's icon, and each article's `published_at` is the page's own text, such as `9 hours ago`, not a timestamp.
- **Params:** `url` (string, **required**) — Canonical 9to5Mac author URL

### `ninetofivemac_headlines`

- **HTTP:** `GET /ninetofivemac/headlines`
- **What:** Get 9to5Mac section headlines. Returns the newest posts from one 9to5Mac topic guide, up to 100. `section` is required and takes a guide slug such as `iphone`, `macbook-pro`, `vision-pro` or `how-to`; an unknown or missing value returns an invalid-params error. Smaller guides, such as `apple-watch-se`, return fewer. Items carry title, URL, summary, time and author.
- **Params:** `section` (string, **required**) — 9to5Mac guide slug

### `ninetofivemac_news`

- **HTTP:** `GET /ninetofivemac/news`
- **What:** Get 9to5Mac top stories. Returns the latest 9to5Mac Apple news stories with no input needed. Each item has a title, canonical article URL, summary, publication time, author and image when present. The list can include podcast episode posts, such as Happy Hour and 9to5Mac Daily, alongside news articles.
- **Params:** _none_

### `ninetofivemac_sections`

- **HTTP:** `GET /ninetofivemac/sections`
- **What:** Get 9to5Mac sections. Lists the 35 9to5Mac topic guides that the headlines endpoint accepts as `section`. Each has a `slug` (for example `iphone`, `mac-studio` or `carplay`), a display `name` and the guide's feed `url`.
- **Params:** _none_

## NJ.com (1)

### `njcom_news`

- **HTTP:** `GET /njcom/news`
- **What:** Get NJ.com top stories. Returns current NJ.com top stories, including title, canonical URL, short summary, author, publication time, and image where available. Category discovery, section headlines, and article and author routes are not available.
- **Params:** _none_

## New York Daily News (5)

### `nydailynews_article`

- **HTTP:** `GET /nydailynews/article`
- **What:** Get New York Daily News article content. Returns public New York Daily News article metadata and body paragraphs from a canonical article URL. For subscriber-only articles the response carries the free lead-in with paywalled set to true.
- **Params:** `url` (string, **required**) — Canonical New York Daily News article URL

### `nydailynews_author`

- **HTTP:** `GET /nydailynews/author`
- **What:** Get a New York Daily News author profile. Returns one New York Daily News author's public profile: name, job title, bio, public email and X/Twitter handle, and their recent articles.
- **Params:** `slug` (string, optional) — Author slug, e.g. rocco-parascandola; `url` (string, optional) — Canonical nydailynews.com/author/<slug>/ URL; alternative to slug

### `nydailynews_headlines`

- **HTTP:** `GET /nydailynews/headlines`
- **What:** Get New York Daily News section headlines. Returns New York Daily News headlines for one section, newest first, up to about 100 stories. `section` is required and takes one of 36 slugs such as `crime-public-safety`, `new-york-yankees` or `opinion`; other values return an invalid-params error. Items carry a title and URL, plus publication time, byline, excerpt and lead image where shown. Team pages can list fewer stories out of season.
- **Params:** `section` (string, **required**) — New York Daily News section slug

### `nydailynews_news`

- **HTTP:** `GET /nydailynews/news`
- **What:** Get New York Daily News top stories. Returns the current New York Daily News top stories, with no parameters. Each item has a title and canonical article URL, plus publication time, byline, excerpt and lead image where the story card shows them. Use `nydailynews-headlines` for a single section.
- **Params:** _none_

### `nydailynews_sections`

- **HTTP:** `GET /nydailynews/sections`
- **What:** Get New York Daily News sections. Lists the 36 New York Daily News section slugs accepted by `nydailynews-headlines`, such as `crime-public-safety`, `new-york-mets`, `nfl` and `things-to-do`. Each entry has its `slug` (the last path segment of the section URL), display `name` and `url`. Topic (`/tag/...`) pages and off-site properties are not sections.
- **Params:** _none_

## New York Magazine (5)

### `nymag_article`

- **HTTP:** `GET /nymag/article`
- **What:** Get New York Magazine article content. Returns a New York Magazine article by its canonical `url`: title, description, section, authors, lead image, publication and update times, a `paywalled` flag and the body `paragraphs`. Subscriber-only or blocked articles return an upstream error.
- **Params:** `url` (string, **required**) — Canonical New York Magazine article URL

### `nymag_author`

- **HTTP:** `GET /nymag/author`
- **What:** Get a New York Magazine author profile. Returns a New York Magazine author profile from a required `url` in the form `https://nymag.com/author/<slug>/`. The response has `name`, `job_title` (empty for some contributors), `bio` and recent articles with title, URL, `excerpt` and a `section` label. Each article's `published_at` is the page's date text, such as `Sept. 20, 2026`, not a timestamp.
- **Params:** `url` (string, **required**) — Canonical New York Magazine author URL

### `nymag_headlines`

- **HTTP:** `GET /nymag/headlines`
- **What:** Get New York Magazine section headlines. Returns recent New York Magazine stories for one site section. `section` is required and takes one of nine slugs: `intelligencer`, `thecut`, `vulture`, `grub-street`, `curbed`, `strategist`, `select-all`, `science` or `daily`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — New York Magazine section slug

### `nymag_news`

- **HTTP:** `GET /nymag/news`
- **What:** Get New York Magazine top stories. Returns the current New York Magazine top stories, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `nymag-headlines` to read one of its sections.
- **Params:** _none_

### `nymag_sections`

- **HTTP:** `GET /nymag/sections`
- **What:** Get New York Magazine sections. Lists the New York Magazine section slugs accepted by `nymag-headlines`, such as `intelligencer`, `thecut`, `vulture` and `grub-street`. Each entry has its stable `slug`, display `name` and section `url`.
- **Params:** _none_

## New York Post (5)

### `nypost_article`

- **HTTP:** `GET /nypost/article`
- **What:** Get New York Post article content. Returns a New York Post article by canonical `url` in the form `https://nypost.com/YYYY/MM/DD/<section>/<slug>/`: title, description, section, authors, lead image, publication and update times, a `paywalled` flag and the body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical New York Post article URL

### `nypost_author`

- **HTTP:** `GET /nypost/author`
- **What:** Get a New York Post author profile. Returns a New York Post author profile from a required `url` in the form `https://nypost.com/author/<slug>/`. The response has `name`, `biography`, `image_url`, `social_links` and recent articles. Staff and wire bylines often have no headshot or bio, and each article's `published_at` is the page's date text such as `September 20, 2026 | 10:06pm`.
- **Params:** `url` (string, **required**) — Canonical New York Post author URL

### `nypost_headlines`

- **HTTP:** `GET /nypost/headlines`
- **What:** Get New York Post section headlines. Returns recent New York Post stories for one section. `section` is required and takes one of 54 slugs, such as `us-news`, `metro`, `nfl`, `business`, `real-estate` or `astrology`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — New York Post RSS section slug

### `nypost_news`

- **HTTP:** `GET /nypost/news`
- **What:** Get New York Post top stories. Returns the current New York Post top stories, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `nypost-headlines` to read a single section.
- **Params:** _none_

### `nypost_sections`

- **HTTP:** `GET /nypost/sections`
- **What:** Get New York Post RSS sections. Lists the 54 New York Post section slugs accepted by `nypost-headlines`, such as `us-news`, `politics`, `nfl`, `celebrities` and `mental-health`. Each entry has its `slug`, display `name` and `url`.
- **Params:** _none_

## NZ Herald (5)

### `nzherald_article`

- **HTTP:** `GET /nzherald/article`
- **What:** Get NZ Herald article content. Returns public NZ Herald article metadata and body paragraphs from a canonical article URL. A premium (subscriber-only) article URL returns a permission error instead of a partial or fabricated body.
- **Params:** `url` (string, **required**) — Canonical NZ Herald article URL

### `nzherald_author`

- **HTTP:** `GET /nzherald/author`
- **What:** Get an NZ Herald author profile. Returns an NZ Herald author profile from a required `url` in the form `https://www.nzherald.co.nz/author/<slug>/`. The response has `name`, `job_title`, `location`, `email`, `biography`, `image_url` and recent articles. Each field reflects what the author's page shows, and article `published_at` is RFC3339 where the page gives a machine-readable timestamp.
- **Params:** `url` (string, **required**) — Canonical NZ Herald author URL

### `nzherald_headlines`

- **HTTP:** `GET /nzherald/headlines`
- **What:** Get NZ Herald section headlines. Returns recent NZ Herald headlines for one section. `section` is required and takes a slug listed by `nzherald-sections`, such as `nz`, `business`, `rugby`, `politics` or `world`. Each item has a title and URL. A URL may point at a premium article, which `nzherald-article` rejects with a permission error.
- **Params:** `section` (string, **required**) — NZ Herald section slug

### `nzherald_news`

- **HTTP:** `GET /nzherald/news`
- **What:** Get NZ Herald top stories. Returns the current New Zealand Herald top stories, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `nzherald-headlines` to read one section.
- **Params:** _none_

### `nzherald_sections`

- **HTTP:** `GET /nzherald/sections`
- **What:** Get NZ Herald sections. Lists the NZ Herald section slugs accepted by `nzherald-headlines`, such as `nz`, `business`, `rugby`, `technology` and `world`. Each entry has its `slug`, a display `name` (for example `New Zealand` for `nz`) and a `url`.
- **Params:** _none_

## Page Six (5)

### `pagesix_article`

- **HTTP:** `GET /pagesix/article`
- **What:** Get Page Six article content. Returns a Page Six article by canonical `url` in the form `https://pagesix.com/YYYY/MM/DD/<section>/<slug>/`: title, description, section, authors, lead image, publication and update times, a `paywalled` flag and the body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical Page Six article URL

### `pagesix_author`

- **HTTP:** `GET /pagesix/author`
- **What:** Get a Page Six author profile. Returns a Page Six author profile from a required `url` in the form `https://pagesix.com/author/<slug>/`. The response has `name`, `biography`, `image_url`, `social_links` and recent articles. An RSS feed link is the only social link always present, and each article's `published_at` is the page's date text such as `September 23, 2026 | 8:16pm`.
- **Params:** `url` (string, **required**) — Canonical Page Six author URL

### `pagesix_headlines`

- **HTTP:** `GET /pagesix/headlines`
- **What:** Get Page Six section headlines. Returns recent Page Six stories for one section. `section` is required and takes one of 30 slugs, such as `celebrity-news`, `royal-family`, `taylor-swift` or `new-york-city-society`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Page Six RSS section slug

### `pagesix_news`

- **HTTP:** `GET /pagesix/news`
- **What:** Get Page Six top stories. Returns the current Page Six top stories, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `pagesix-headlines` to read one section.
- **Params:** _none_

### `pagesix_sections`

- **HTTP:** `GET /pagesix/sections`
- **What:** Get Page Six RSS sections. Lists the 30 Page Six section slugs accepted by `pagesix-headlines`, such as `celebrity-news`, `royal-family`, `taylor-swift` and `palm-beach-society`. Each entry has its `slug`, display `name` and `url`.
- **Params:** _none_

## PC Gamer (5)

### `pcgamer_article`

- **HTTP:** `GET /pcgamer/article`
- **What:** Get PC Gamer article content. Returns a PC Gamer article by canonical `pcgamer.com` `url`; review pages work the same way as news articles. The response has title, description, section, authors, lead image, publication and update times, a `paywalled` flag and body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical PC Gamer article URL

### `pcgamer_author`

- **HTTP:** `GET /pcgamer/author`
- **What:** Get a PC Gamer author profile. Returns a PC Gamer author profile by `slug` (for example `harvey-randall`) or a pcgamer.com author `url`; supply exactly one. `page` picks the 1-based page of recent articles (default 1) and overrides a `/page/<n>` segment in `url`. The response has `name`, `job_title`, `biography`, `social_links`, articles, `page` and `has_next_page`.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. harvey-randall; `url` (string, optional) — Canonical pcgamer.com/author/<slug> URL, optionally with a /page/<n> segment; alternative to slug

### `pcgamer_headlines`

- **HTTP:** `GET /pcgamer/headlines`
- **What:** Get PC Gamer section headlines. Returns recent PC Gamer headlines for one section. `section` is required and takes one of eight slugs: `deals`, `games`, `gaming-industry`, `guides`, `hardware`, `movies-tv`, `news` or `software`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — PC Gamer section slug

### `pcgamer_news`

- **HTTP:** `GET /pcgamer/news`
- **What:** Get PC Gamer top stories. Returns the current PC Gamer top stories, with no parameters. Each item has a title and URL, and may include summary, author, publication time and image. Use `pcgamer-headlines` to read one section.
- **Params:** _none_

### `pcgamer_sections`

- **HTTP:** `GET /pcgamer/sections`
- **What:** Get PC Gamer sections. Lists the eight top-level PC Gamer sections accepted by `pcgamer-headlines`: `deals`, `games`, `gaming-industry`, `guides`, `hardware`, `movies-tv`, `news` and `software`. Each entry has its `slug`, display `name` and `url`.
- **Params:** _none_

## PCMag (5)

### `pcmag_article`

- **HTTP:** `GET /pcmag/article`
- **What:** Get PCMag article or review content. Returns a PCMag article or product review by canonical `pcmag.com` `url`, such as `/news/<slug>` or `/reviews/<slug>`. The response has title, description, publication time, section label, authors, lead image and body `paragraphs`. Hub pages, author pages and pages without a readable body return an upstream error.
- **Params:** `url` (string, **required**) — Canonical PCMag article or review URL

### `pcmag_author`

- **HTTP:** `GET /pcmag/author`
- **What:** Get a PCMag author profile. Returns a PCMag author profile by `slug` (for example `michael-kan`) or a pcmag.com authors `url`; supply exactly one. The response has `name`, `role`, `biography`, `image_url`, `expertise` topics linked to category hubs, `social_links` (X, LinkedIn, Bluesky, Threads) as full URLs, and recent articles.
- **Params:** `slug` (string, optional) — Author slug, e.g. michael-kan; `url` (string, optional) — Canonical pcmag.com/authors/<slug> URL; alternative to slug

### `pcmag_headlines`

- **HTTP:** `GET /pcmag/headlines`
- **What:** Get PCMag section headlines. Returns recent PCMag headlines for one product or topic category. `section` is required and takes a category slug such as `ai`, `antivirus`, `cameras`, `crm-software` or `gaming-systems`; `pcmag-sections` lists them. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — PCMag category slug

### `pcmag_news`

- **HTTP:** `GET /pcmag/news`
- **What:** Get PCMag top stories. Returns the current PCMag top stories, with no parameters. Each item has a title, canonical URL, summary, publication time and author name when available. Use `pcmag-headlines` to read one product or topic category.
- **Params:** _none_

### `pcmag_sections`

- **HTTP:** `GET /pcmag/sections`
- **What:** Get PCMag sections. Lists the PCMag product and topic category slugs accepted by `pcmag-headlines`, such as `3d-printers`, `ai`, `antivirus`, `crm-software` and `drones`. Each entry has a `slug`, a display `name` and the category hub `url`.
- **Params:** _none_

## PEOPLE (5)

### `people_article`

- **HTTP:** `GET /people/article`
- **What:** Get PEOPLE article content. Returns a PEOPLE article by canonical `people.com` `url`, such as `https://people.com/example-headline-12345678`. The response has title, description, section, authors, lead image, publication and update times, a `paywalled` flag and body `paragraphs`. `authors` is empty for pieces with no byline.
- **Params:** `url` (string, **required**) — Canonical PEOPLE article URL

### `people_author`

- **HTTP:** `GET /people/author`
- **What:** Get a PEOPLE author profile. Returns a PEOPLE staff writer or contributor's public profile (name, job title, structured intro fields, biography, personal social links) and recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical PEOPLE author URL

### `people_headlines`

- **HTTP:** `GET /people/headlines`
- **What:** Get PEOPLE section headlines. Returns fresh headlines from one PEOPLE section listing page. section accepts any slug returned by GET /people/sections (37 values, too many to enumerate inline -- see that endpoint for the full, current list), for example "celebrity" or "royals".
- **Params:** `section` (string, **required**) — PEOPLE section slug, from GET /people/sections

### `people_news`

- **HTTP:** `GET /people/news`
- **What:** Get PEOPLE top stories. Returns the current PEOPLE celebrity and entertainment top stories, with no parameters and no section filter. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** _none_

### `people_sections`

- **HTTP:** `GET /people/sections`
- **What:** Get PEOPLE sections. Returns the full PEOPLE section/category navigation inventory (37 entries as of 2026-09-24), each with a slug, display name, and public listing URL. Use a returned slug as the section parameter on GET /people/headlines.
- **Params:** _none_

## Philadelphia Inquirer (5)

### `phillyinquirer_article`

- **HTTP:** `GET /phillyinquirer/article`
- **What:** Get Philadelphia Inquirer article content. Returns a Philadelphia Inquirer story by canonical `inquirer.com` `url` ending in `-<yyyymmdd>.html`: title, description, publication and update times, section, authors, lead image and body `paragraphs` in reading order. Captions, teasers and comments are excluded. Associated Press `/wires/` pages, section pages and author pages return `400`.
- **Params:** `url` (string, **required**) — Canonical Philadelphia Inquirer story URL

### `phillyinquirer_author`

- **HTTP:** `GET /phillyinquirer/author`
- **What:** Get a Philadelphia Inquirer author profile. Returns a Philadelphia Inquirer staff author profile by `slug` (for example `gammage_jeff`) or an inquirer.com author `url`; supply exactly one. The response has `name`, `role`, `biography`, `image_url`, public web social links (no email or phone) and the latest 20 stories, with no paging. An unknown slug returns a 404 error.
- **Params:** `slug` (string, optional) — Author slug, e.g. gammage_jeff; `url` (string, optional) — Canonical inquirer.com/author/<slug> URL; alternative to slug

### `phillyinquirer_headlines`

- **HTTP:** `GET /phillyinquirer/headlines`
- **What:** Get Philadelphia Inquirer section headlines. Returns recent Philadelphia Inquirer stories for one section, without Associated Press wire copy. `section` is required and takes one of 24 slugs, such as `news`, `sixers`, `eagles`, `south-jersey` or `real-estate`; invalid values return `400`. Each item has a title and URL, and may include summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Philadelphia Inquirer section slug

### `phillyinquirer_news`

- **HTTP:** `GET /phillyinquirer/news`
- **What:** Get Philadelphia Inquirer top stories. Returns the current Philadelphia Inquirer top stories, with no parameters. Each item has a title, canonical URL, summary, publication time and author name when available. Associated Press wire copy, which makes up much of the source, is excluded.
- **Params:** _none_

### `phillyinquirer_sections`

- **HTTP:** `GET /phillyinquirer/sections`
- **What:** Get Philadelphia Inquirer sections. Lists the 24 Philadelphia Inquirer section slugs accepted by `phillyinquirer-headlines`, such as `news`, `sixers`, `eagles` and `south-jersey`. Each entry has a `slug`, display `name` and `url`. Sub-sections such as `news/philadelphia` are not listed because the `news` section already contains them.
- **Params:** _none_

## Philstar (5)

### `philstar_article`

- **HTTP:** `GET /philstar/article`
- **What:** Get Philstar article content. Returns public Philstar article metadata and body paragraphs from a canonical article URL. Philstar serves full stories to anonymous readers, so no paywall flag is needed.
- **Params:** `url` (string, **required**) — Canonical Philstar article URL

### `philstar_author`

- **HTTP:** `GET /philstar/author`
- **What:** Get a Philstar author archive. Returns one Philstar author's public archive: name, profile photo when set, and the most recent stories on the first page of the archive. Authors are identified by the numeric id in the byline link (philstar.com/authors/<id>/<name>).
- **Params:** `id` (string, optional) — Numeric Philstar author id from a byline link, e.g. 1805259; `url` (string, optional) — Author archive URL, https://www.philstar.com/authors/<id>[/<name>]; alternative to id

### `philstar_headlines`

- **HTTP:** `GET /philstar/headlines`
- **What:** Get Philstar section headlines. Returns the current headlines from the first page of one public Philstar section page (Philstar publishes no crawlable feeds, so this reads the section page itself).
- **Params:** `section` (string, **required**) — Philstar section slug

### `philstar_news`

- **HTTP:** `GET /philstar/news`
- **What:** Get Philstar top stories. Returns the current Philstar (Philippine Star) top stories from the public homepage: the latest, trending and featured stories with summary, byline, thumbnail and the publication date encoded in the story URL.
- **Params:** _none_

### `philstar_sections`

- **HTTP:** `GET /philstar/sections`
- **What:** Get Philstar sections. Returns the public Philstar editorial section inventory: every English, Filipino (Pilipino Star Ngayon, Pang-Masa) and Cebuano (Banat, The Freeman) section page that lists stories.
- **Params:** _none_

## PhoneArena (5)

### `phonearena_article`

- **HTTP:** `GET /phonearena/article`
- **What:** Get PhoneArena article or review content. Returns public PhoneArena news or review metadata and body paragraphs from a canonical article URL. PhoneArena serves pages behind a Cloudflare challenge; when the challenge is not cleared the endpoint returns a 503 error.
- **Params:** `url` (string, **required**) — Canonical PhoneArena article URL

### `phonearena_author`

- **HTTP:** `GET /phonearena/author`
- **What:** Get a PhoneArena author profile. Returns one PhoneArena staff author's public profile: name, role, biography, image, social links and the recent articles listed on the profile page.
- **Params:** `slug` (string, optional) — Author username, e.g. sebastian.f; `url` (string, optional) — Canonical phonearena.com/team/<slug> URL; alternative to slug

### `phonearena_headlines`

- **HTTP:** `GET /phonearena/headlines`
- **What:** Get PhoneArena section headlines. Returns up to 100 newest PhoneArena stories or reviews from one public listing. For news-month and reviews, titles are reconstructed from the hero-image file name and published_at is the listing's last-modified time.
- **Params:** `section` (string, **required**) — PhoneArena listing slug

### `phonearena_news`

- **HTTP:** `GET /phonearena/news`
- **What:** Get PhoneArena top stories. Returns PhoneArena's most recent phone news stories (about the last two days) from its public news sitemap, with exact titles and publication times.
- **Params:** _none_

### `phonearena_sections`

- **HTTP:** `GET /phonearena/sections`
- **What:** Get PhoneArena sections. Lists the three PhoneArena listings that `phonearena-headlines` accepts: `news` (the last two days of news), `news-month` (the newest news of the current calendar month) and `reviews` (the newest reviews, comparisons and hands-on articles of the current year). Each entry has a `slug`, a display `name` and a source `url`.
- **Params:** _none_

## Polygon (5)

### `polygon_article`

- **HTTP:** `GET /polygon/article`
- **What:** Get Polygon article content. Returns a Polygon article by canonical `url` (`https://www.polygon.com/<slug>/`): title, description, section, authors, publication and update times, lead image, body `paragraphs` and a `paywalled` flag. Section, guide and other non-article URLs, such as `/gaming-news/` or `/guides/`, are rejected as an invalid parameter.
- **Params:** `url` (string, **required**) — Canonical Polygon article URL

### `polygon_author`

- **HTTP:** `GET /polygon/author`
- **What:** Get a Polygon author profile. Returns a Polygon author profile by canonical `url` (`https://www.polygon.com/author/<slug>/`): name, `title`, `image_url`, `biography`, social links and the articles in the profile's Latest module. Title, image and biography appear only as the profile shows them. `social_links` holds the author's own accounts, not Polygon's internal follow link.
- **Params:** `url` (string, **required**) — Canonical Polygon author URL

### `polygon_headlines`

- **HTTP:** `GET /polygon/headlines`
- **What:** Get Polygon section headlines. Returns the latest Polygon stories for one section. `section` is required and takes one of 15 slugs, including `gaming-news`, `gaming-reviews`, `movie-tv-reviews`, `anime`, `guides` and `videos`. Each item has its title, URL, summary, publication time, author and image.
- **Params:** `section` (string, **required**) — Polygon RSS section slug

### `polygon_news`

- **HTTP:** `GET /polygon/news`
- **What:** Get Polygon top stories. Returns Polygon's latest top stories across the site, covering games and entertainment. Takes no parameters, and `polygon-headlines` narrows by section instead. Each item has its title, URL, summary, publication time, author and image.
- **Params:** _none_

### `polygon_sections`

- **HTTP:** `GET /polygon/sections`
- **What:** Get Polygon RSS sections. Lists the Polygon sections that `polygon-headlines` accepts, from `gaming-news` and `gaming-reviews` to `guides` and `videos`. Each entry has a `slug`, a display `name` and the section's feed `url`.
- **Params:** _none_

## Popular Mechanics (1)

### `popularmechanics_news`

- **HTTP:** `GET /popularmechanics/news`
- **What:** Get Popular Mechanics top stories. Returns current stories from Popular Mechanics' public all-stories RSS feed. Summaries are publisher teasers, not full article text. This feed-only route does not claim a complete section taxonomy or retrieve article bodies.
- **Params:** _none_

## ProPublica (5)

### `propublica_article`

- **HTTP:** `GET /propublica/article`
- **What:** Get ProPublica article content. Returns a ProPublica article by canonical `url` (`propublica.org/article/<slug>`): title, authors, publication and update dates, the dek as `description`, lead image where available, section, a `paywalled` flag and the body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical ProPublica article URL

### `propublica_author`

- **HTTP:** `GET /propublica/author`
- **What:** Get a ProPublica staff profile. Returns one ProPublica staff/contributor's public profile: name, bio, contact email and social accounts where published, and one page of their recent bylined stories.
- **Params:** `page` (integer, optional) — 1-based page of recent stories to return; defaults to 1; `url` (string, **required**) — Canonical propublica.org/people/<slug> URL

### `propublica_headlines`

- **HTTP:** `GET /propublica/headlines`
- **What:** Get ProPublica topic headlines. Returns the latest ProPublica stories for one topic. `section` is required and takes one of 33 topic slugs, such as `politics`, `health-care`, `immigration`, `courts`, `environment` or `trump-administration`. Each item has its title, URL, publication time and author.
- **Params:** `section` (string, **required**) — ProPublica topic slug

### `propublica_news`

- **HTTP:** `GET /propublica/news`
- **What:** Get ProPublica top stories. Returns the latest ProPublica top stories across topics. Takes no parameters. Each item has its title, URL, summary, publication time and image, plus the author byline, which can name more than one reporter.
- **Params:** _none_

### `propublica_sections`

- **HTTP:** `GET /propublica/sections`
- **What:** Get ProPublica topics. Lists the 33 topics from ProPublica's Browse Topics menu that `propublica-headlines` accepts. Each entry has a stable `slug`, a display `name` and the topic's feed `url`. Takes no parameters.
- **Params:** _none_

## Punch (5)

### `punch_article`

- **HTTP:** `GET /punch/article`
- **What:** Get Punch article content. Returns a Punch article by canonical `url` (`https://punchng.com/<slug>/`): title, description, publication and update times, section, authors, image and the body `paragraphs`. Punch articles are free to read, so `paywalled` is never set. Video-led stories may have only a short text summary.
- **Params:** `url` (string, **required**) — Canonical Punch article URL

### `punch_author`

- **HTTP:** `GET /punch/author`
- **What:** Get a Punch author archive. Returns a Punch author's name and their most recent articles (the first archive page, about 30) from a canonical `url` (`https://punchng.com/author/<slug>/`). `total_pages` is the number of archive pages. Punch author pages have no biography, photo or social links, so none are returned. An unknown author returns not-found.
- **Params:** `url` (string, **required**) — Canonical Punch author URL

### `punch_headlines`

- **HTTP:** `GET /punch/headlines`
- **What:** Get Punch section headlines. Returns the current stories, about 30, from one Punch topic page. `section` is required and takes a topic slug such as `news`, `politics`, `business`, `sports`, `metro-plus` or `top-stories`; any other value is an invalid-parameter error. Each item has a title and article URL, plus summary, publication time and image URL when the page shows them.
- **Params:** `section` (string, **required**) — Punch topic slug

### `punch_news`

- **HTTP:** `GET /punch/news`
- **What:** Get Punch top stories. Returns the latest Punch stories from punchng.com: title, article URL, summary, author and publication time. Takes no parameters. Punch labels its times as UTC but publishes them in West Africa Time (UTC+1), and `published_at` is corrected for that one-hour skew.
- **Params:** _none_

### `punch_sections`

- **HTTP:** `GET /punch/sections`
- **What:** Get Punch sections. Lists the Punch topic slugs that `punch-headlines` accepts, such as `news`, `politics`, `business` and `sports`. Each entry has a `slug`, a display `name` and the topic page `url`. The list covers top-level topics linked from Punch's navigation or active in the 90 days before 2026-09-25.
- **Params:** _none_

## Rappler (5)

### `rappler_article`

- **HTTP:** `GET /rappler/article`
- **What:** Get Rappler article content. Returns public Rappler article metadata and body paragraphs from a canonical article URL. Rappler+ member-tier stories are flagged with paywalled.
- **Params:** `url` (string, **required**) — Canonical Rappler article URL

### `rappler_author`

- **HTTP:** `GET /rappler/author`
- **What:** Get a Rappler author profile. Returns a Rappler author's profile, looked up by `slug` (for example `delfin-dioquino`) or by canonical `url`; exactly one is required. The response has the name, `bio`, `social_links` and the 10 most recent articles, each with title, URL, section and publication time. There is no further paging. `bio` and `social_links` are omitted when empty; an unknown author returns not-found.
- **Params:** `slug` (string, optional) — Author slug, e.g. delfin-dioquino; `url` (string, optional) — Canonical rappler.com/author/<slug>/ URL; alternative to slug

### `rappler_headlines`

- **HTTP:** `GET /rappler/headlines`
- **What:** Get Rappler section headlines. Returns the latest Rappler stories for one section. `section` is required and takes one of the site's category slugs, such as `business`, `nation`, `entertainment`, `fact-check`, `investigative` or `climate-change`. Each item has its title, URL, summary, publication time and author, plus an image when the outlet provides one.
- **Params:** `section` (string, **required**) — Rappler section slug

### `rappler_news`

- **HTTP:** `GET /rappler/news`
- **What:** Get Rappler top stories. Returns the newest Rappler stories across all sections. Takes no parameters. Each item has its title, canonical article URL, a short summary, publication time, author byline and lead image.
- **Params:** _none_

### `rappler_sections`

- **HTTP:** `GET /rappler/sections`
- **What:** Get Rappler sections. Lists the 175 Rappler categories that have a live feed and are accepted by `rappler-headlines`, such as `news-updates`, `business`, `nation`, `fact-check` and `climate-change`. Each entry has a `slug`, a display `name` and the category `url`.
- **Params:** _none_

## Raw Story (5)

### `rawstory_article`

- **HTTP:** `GET /rawstory/article`
- **What:** Get Raw Story article content. Returns a Raw Story article by canonical `url` on `rawstory.com`, for example `https://www.rawstory.com/trump-media-ban-2677933730/`: title, description, publication and update times, section, authors, image and body `paragraphs` (embedded videos excluded). `section` is omitted for slug-only URLs. Hub, tag and author URLs return an invalid-params error; a missing story returns not-found.
- **Params:** `url` (string, **required**) — Canonical Raw Story article URL

### `rawstory_author`

- **HTTP:** `GET /rawstory/author`
- **What:** Get a Raw Story author profile. Returns a Raw Story author's profile, looked up by `slug` (for example `bennitokelty`) or canonical `url`; exactly one is required. The response has the name, `bio`, avatar, social links and the 15 most recent stories, each with title, URL and a `YYYY-MM-DD` date. Older stories are not reachable, and an unknown author returns not-found.
- **Params:** `slug` (string, optional) — Author slug, e.g. bennitokelty; `url` (string, optional) — Canonical rawstory.com/u/<slug> URL; alternative to slug

### `rawstory_headlines`

- **HTTP:** `GET /rawstory/headlines`
- **What:** Get Raw Story section headlines. Returns the latest Raw Story stories, up to 30, for one section hub. `section` is required and takes one of 15 slugs such as `us-news`, `trump-news`, `world`, `commentary` or `supreme-court`. Each item has its title, URL, lead-paragraph summary, publication time, author and image when given. The dormant `presidential-campaign-issues` hub returns 9 stories.
- **Params:** `section` (string, **required**) — Raw Story section slug

### `rawstory_news`

- **HTTP:** `GET /rawstory/news`
- **What:** Get Raw Story top stories. Returns the 30 newest Raw Story stories across all sections. Takes no parameters. Each item has its title, story URL, a lead-paragraph summary capped at 500 characters, publication time, author byline and lead image.
- **Params:** _none_

### `rawstory_sections`

- **HTTP:** `GET /rawstory/sections`
- **What:** Get Raw Story sections. Lists the 15 section and topic hubs that `rawstory-headlines` accepts. Each entry has a `slug`, a display `name` such as `U.S. News` or `Raw Exclusives`, and the hub page `url`. Hubs overlap: `us-news`, `trump-news` and `smartnews` share most recent stories, and `presidential-campaign-issues` is dormant.
- **Params:** _none_

## RNZ (5)

### `rnz_article`

- **HTTP:** `GET /rnz/article`
- **What:** Get RNZ article content. Returns public RNZ news article metadata and body paragraphs from a canonical rnz.co.nz/news/<section>/<id>/<slug> article URL. RNZ has no paywall, so the full body is returned.
- **Params:** `url` (string, **required**) — Canonical RNZ news article URL

### `rnz_author`

- **HTTP:** `GET /rnz/author`
- **What:** Get an RNZ author profile. Returns one RNZ reporter's public profile: name, role, bio, email, X/Twitter handle, photo, total story count, and the first page of their news stories.
- **Params:** `slug` (string, optional) — Author slug, e.g. ellen-o-dwyer; `url` (string, optional) — Canonical rnz.co.nz/authors/<slug> URL; alternative to slug

### `rnz_headlines`

- **HTTP:** `GET /rnz/headlines`
- **What:** Get RNZ section headlines. Returns the latest RNZ (Radio New Zealand) stories for one section. `section` is required and takes one of 19 slugs such as `news`, `national`, `political`, `business`, `pacific`, `te-manu-korihi` or `weather`; others return a 400. Each item has its title, URL, summary and publication time. Smaller sections can carry items from earlier weeks, so check `published_at`.
- **Params:** `section` (string, **required**) — RNZ section slug

### `rnz_news`

- **HTTP:** `GET /rnz/news`
- **What:** Get RNZ top stories. Returns RNZ (Radio New Zealand) top stories from its all-news feed: title, article URL, summary and publication time in UTC. Takes no parameters. Lifestyle guides, audio programme pages and section hubs are left out, and article URLs use RNZ's current section names.
- **Params:** _none_

### `rnz_sections`

- **HTTP:** `GET /rnz/sections`
- **What:** Get RNZ sections. Lists the 19 RNZ news sections that `rnz-headlines` accepts, such as `news`, `national`, `political`, `pacific` and `te-manu-korihi`. Each entry has a `slug`, a display `name` and the section's feed `url`. RNZ's programme-schedule and recipe feeds are not included.
- **Params:** _none_

## Rolling Stone (5)

### `rollingstone_article`

- **HTTP:** `GET /rollingstone/article`
- **What:** Get Rolling Stone article content. Returns a Rolling Stone article by canonical `url`, a `rollingstone.com` address ending in a numeric article id: title, description, section, authors, publication and update times, image, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Rolling Stone article URL

### `rollingstone_author`

- **HTTP:** `GET /rollingstone/author`
- **What:** Get a Rolling Stone author profile. Returns a Rolling Stone author's byline metadata, biography, and recent articles (sourced from the author's own public RSS feed) from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical Rolling Stone author URL

### `rollingstone_headlines`

- **HTTP:** `GET /rollingstone/headlines`
- **What:** Get Rolling Stone section headlines. Returns the latest Rolling Stone stories for one section. `section` is required and takes one of 34 slugs, including `music`, `music-news`, `music-album-reviews`, `politics`, `tv-movie-reviews`, `culture` and `rs-gaming`. Each item has its title, URL, summary, publication time and author.
- **Params:** `section` (string, **required**) — Rolling Stone section slug

### `rollingstone_news`

- **HTTP:** `GET /rollingstone/news`
- **What:** Get Rolling Stone top stories. Returns Rolling Stone's latest top stories across the site. Takes no parameters, and `rollingstone-headlines` narrows by section instead. Each item has its title, URL, summary, publication time and author.
- **Params:** _none_

### `rollingstone_sections`

- **HTTP:** `GET /rollingstone/sections`
- **What:** Get Rolling Stone sections. Returns the public Rolling Stone section inventory: every music, politics, TV & movies, and culture subsection plus the site's standalone verticals (Rolling Stone Pro, product recommendations) and tag hubs, each linking to its public RSS feed.
- **Params:** _none_

## RTÉ News (5)

### `rte_article`

- **HTTP:** `GET /rte/article`
- **What:** Get RTÉ News article content. Returns public RTÉ News article metadata and body paragraphs from a canonical rte.ie/news article URL. RTÉ News articles are free to read; paywalled is omitted.
- **Params:** `url` (string, **required**) — Canonical RTÉ News article URL

### `rte_author`

- **HTTP:** `GET /rte/author`
- **What:** Get an RTÉ News author profile. Returns an RTÉ News author's profile by canonical `url` (`https://www.rte.ie/author/<id>-<slug>/`, the author link on an article byline): name, headshot, `role` and recent articles, each with title, URL, summary, publication time and image. `role` is the job title the page shows, for example Political Correspondent, and is omitted when there is none.
- **Params:** `url` (string, **required**) — Canonical RTÉ author URL

### `rte_headlines`

- **HTTP:** `GET /rte/headlines`
- **What:** Get RTÉ News section headlines. Returns the latest RTÉ News stories for one section. `section` is required and takes one of 29 slugs such as `ireland`, `world`, `politics`, `dublin`, `courts` or `nuacht` (Irish-language); others return a 400. Each item has its title, URL, summary, publication time and image. Small sections like `science` return only a handful of items.
- **Params:** `section` (string, **required**) — RTÉ News section slug

### `rte_news`

- **HTTP:** `GET /rte/news`
- **What:** Get RTÉ News top stories. Returns fresh RTÉ News top stories from its public news feed. Scope is RTÉ News (rte.ie/news) only, not the RTÉ Player, radio, sport or entertainment sections.
- **Params:** _none_

### `rte_sections`

- **HTTP:** `GET /rte/sections`
- **What:** Get RTÉ News sections. Lists the 29 RTÉ News section hubs that `rte-headlines` accepts, such as `ireland`, `politics`, `dublin`, `ukraine` and `investigations-unit`. Each entry has a `slug`, a display `name` and the feed `url`. The list is curated to hubs with their own article feed, so narrower topic pages are not included.
- **Params:** _none_

## Salon (5)

### `salon_article`

- **HTTP:** `GET /salon/article`
- **What:** Get Salon article content. Returns a Salon article by canonical `url` on `www.salon.com` in the `/YYYY/MM/DD/<slug>/` form: title, description, section, authors, publication and update times, image, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Salon article URL

### `salon_author`

- **HTTP:** `GET /salon/author`
- **What:** Get a Salon writer profile. Returns a Salon writer's profile by canonical `url` (`https://www.salon.com/writer/<slug>`): name, `job_title`, `bio`, `image_url`, `same_as` links and a list of articles. Each article carries only a title and URL, with no date or category. Job title, photo and `same_as` appear only when the writer page shows them.
- **Params:** `url` (string, **required**) — Canonical Salon writer URL

### `salon_headlines`

- **HTTP:** `GET /salon/headlines`
- **What:** Get Salon section headlines. Returns the latest Salon stories for one section. `section` is required and takes one of 32 slugs, including `home`, `news-and-politics`, `politics`, `opinion`, `culture`, `science-and-health` and `technology`. Each item has its title, URL, summary, publication time, author and image.
- **Params:** `section` (string, **required**) — Salon RSS section slug

### `salon_news`

- **HTTP:** `GET /salon/news`
- **What:** Get Salon top stories. Returns Salon's latest top stories across the site. Takes no parameters, and `salon-headlines` narrows by section instead. Each item has its title, URL, summary, publication time, author and image.
- **Params:** _none_

### `salon_sections`

- **HTTP:** `GET /salon/sections`
- **What:** Get Salon RSS sections. Lists the 32 Salon sections that `salon-headlines` accepts, from `home` and `news-and-politics` to `working_ahead`. Each entry has a `slug`, a display `name` and the section's feed `url`. The list includes older event slugs such as `oscars_2012` and `sxsw_2013`.
- **Params:** _none_

## SBS News (5)

### `sbsnews_article`

- **HTTP:** `GET /sbsnews/article`
- **What:** Get SBS News article content. Returns public SBS News article metadata and body paragraphs from a canonical article URL, including standard, Insight, and Dateline stories.
- **Params:** `url` (string, **required**) — Canonical SBS News article URL

### `sbsnews_author`

- **HTTP:** `GET /sbsnews/author`
- **What:** Get an SBS News author profile. Returns an SBS News byline collection by canonical `url`, for example `https://www.sbs.com.au/news/collection/jennifer-scherer`: name, headshot, biography and the articles on the requested archive `page` (1-based, default 1), with `has_next_page` for paging. Articles are limited to SBS News article, Insight and Dateline links.
- **Params:** `page` (integer, optional) — 1-based author archive page number; `url` (string, **required**) — Canonical SBS News author collection URL

### `sbsnews_headlines`

- **HTTP:** `GET /sbsnews/headlines`
- **What:** Get SBS News section headlines. Returns current SBS News headlines for one section. `section` is required and takes one of 15 slugs from `sbsnews-sections`, such as `top`, `latest`, `australia`, `world`, `politics`, `indigenous`, `cost-of-living` or `sport`. Every item has its title and URL. The `top`, `latest`, `australia` and `world` sections also include summary, publication time and image.
- **Params:** `section` (string, **required**) — Section slug from sbsnews-sections

### `sbsnews_news`

- **HTTP:** `GET /sbsnews/news`
- **What:** Get SBS News top stories. Returns the current SBS News Top Stories. Takes no parameters. Each item has its title, canonical SBS News article URL and summary, with publication time, author and image when present.
- **Params:** _none_

### `sbsnews_sections`

- **HTTP:** `GET /sbsnews/sections`
- **What:** Get SBS News sections. Lists the SBS News sections that `sbsnews-headlines` accepts: the seven primary navigation sections, the Top Stories feed and featured topic and collection pages. Each entry has a `slug`, a display `name` and a `url`. News Podcasts and video surfaces are not included.
- **Params:** _none_

## ScienceAlert (5)

### `sciencealert_article`

- **HTTP:** `GET /sciencealert/article`
- **What:** Get ScienceAlert article content. Returns a ScienceAlert article by absolute canonical `url`: title, description, section, authors, publication and update times, image, the cleaned body `paragraphs` and a `paywalled` flag. Section pages and author listing URLs are rejected.
- **Params:** `url` (string, **required**) — Canonical ScienceAlert article URL

### `sciencealert_author`

- **HTTP:** `GET /sciencealert/author`
- **What:** Get a ScienceAlert author profile. Returns a ScienceAlert author's profile and one page of articles, from an author listing `url` in the form `https://www.sciencealert.com/<author>/page/<number>`; the first observed page is `/page/0`. The response has the name, `slug`, biography, image, social links, that page's articles, and `page` and `has_next_page` for paging.
- **Params:** `url` (string, **required**) — Canonical ScienceAlert author listing URL, e.g. /michelle-starr/page/0

### `sciencealert_headlines`

- **HTTP:** `GET /sciencealert/headlines`
- **What:** Get ScienceAlert section headlines. Returns the latest ScienceAlert stories for one section. `section` is required and takes `space`, `health`, `environment`, `humans`, `tech`, `nature`, `physics` or `this-week-in-science`; other values are rejected. Each item has its title and URL.
- **Params:** `section` (string, **required**) — Section slug

### `sciencealert_news`

- **HTTP:** `GET /sciencealert/news`
- **What:** Get ScienceAlert top stories. Returns ScienceAlert's latest top stories across the site. Takes no parameters, and `sciencealert-headlines` narrows by section instead. Each item has its title, URL, summary, author and publication time.
- **Params:** _none_

### `sciencealert_sections`

- **HTTP:** `GET /sciencealert/sections`
- **What:** Get ScienceAlert sections. Lists the eight top-level ScienceAlert sections that `sciencealert-headlines` accepts: `space`, `health`, `environment`, `humans`, `tech`, `nature`, `physics` and `this-week-in-science`. Each entry has a `slug`, a display `name` and the section page `url`.
- **Params:** _none_

## SCMP (4)

### `scmp_article`

- **HTTP:** `GET /scmp/article`
- **What:** Get an SCMP article's content. Returns one public South China Morning Post article's metadata and body paragraphs from a canonical article URL. `content_locked` and `paywall_types` are the upstream's own restricted-access signals for that article, reported exactly as the site returns them; the body returned here is the same one the site's own page serves to an anonymous visitor. An article whose page genuinely withholds its body is reported as a restricted-access error instead of a hollow or truncated response.
- **Params:** `url` (string, **required**) — Canonical SCMP article URL

### `scmp_author`

- **HTTP:** `GET /scmp/author`
- **What:** Get an SCMP author/reporter profile. Returns one South China Morning Post author/reporter's public profile -- name, role, biography, areas of expertise, languages, location, headshot, and contact/social links -- plus their recent articles, from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical scmp.com/author/<slug> URL

### `scmp_headlines`

- **HTTP:** `GET /scmp/headlines`
- **What:** Get the latest stories in an SCMP section. Returns the current article listing for one South China Morning Post section: each story's title, canonical URL, summary, byline, publication time, and lead image. Section must be a slug returned by /scmp/sections.
- **Params:** `section` (string, **required**) — Section slug from /scmp/sections

### `scmp_sections`

- **HTTP:** `GET /scmp/sections`
- **What:** List SCMP sections. Lists every South China Morning Post section accepted by /scmp/headlines, with its slug, display name, feed URL, and (for a subsection) its parent section's slug and name. Values: `news`, `business`, `property`, `tech`, `lifestyle`, `culture`, `sport`, `postmag`, `style`, `this-week-in-asia`, `cooking`, `hong-kong`, `china`, `asia`, `world`, `people-culture`, `china-politics`, `china-diplomacy`, `china-economy`, `hong-kong-politics`, `hong-kong-economy`, `hong-kong-health-environment`, `hong-kong-education`, `world-us-canada`, `world-europe`, `world-middle-east`, `world-americas`, `world-africa`, `world-russia-central-asia`, `asia-australasia`, `asia-diplomacy`, `asia-east-asia`, `asia-southeast-asia`, `asia-south-asia`, `business-companies`, `business-investor-relations`, `business-global-economy`, `business-money-wealth`, `opinion-comment`, `opinion-harrys-view`, `opinion-blogs`, `opinion-polls`, `opinion-letters`, `property-hong-kong-china`, `property-international`, `tech-big-tech`, `tech-enterprises`, `tech-innovation`, `tech-leaders-founders`, `tech-science-research`, `lifestyle-fashion-beauty`, `lifestyle-travel-leisure`, `lifestyle-motoring`, `lifestyle-food-drink`, `lifestyle-health-wellness`, `lifestyle-watches`, `culture-books`, `culture-music`, `culture-film-tv`, `culture-arts`, `sport-hong-kong`, `sport-china`, `sport-golf`, `sport-racing`, `sport-rugby`, `sport-football`, `sport-tennis`, `sport-other`, `sport-boxing`, `sport-hong-kong-sevens`, `postmag-culture`, `postmag-travel`, `postmag-food-drink`, `postmag-passions`, `postmag-wellness`, `postmag-design-interiors`, `style-luxury`, `style-fashion`, `style-beauty`, `style-people`, `style-lifestyle`, `this-week-in-asia-politics`, `this-week-in-asia-geopolitics`, `this-week-in-asia-economics`, `this-week-in-asia-society`, `this-week-in-asia-opinion`, `this-week-in-asia-asia-buzz`, `this-week-in-asia-people`.
- **Params:** _none_

## ScreenRant (5)

### `screenrant_article`

- **HTTP:** `GET /screenrant/article`
- **What:** Get ScreenRant article content. Returns a ScreenRant article by canonical `url` of the form `https://screenrant.com/<slug>/`: title, description, section, authors, publication and update times, image and body `paragraphs`. Warning and note callouts and Related cards are left out of `paragraphs`. Section hubs and multi-segment URLs such as `/video/<slug>/` are rejected as invalid.
- **Params:** `url` (string, **required**) — Canonical ScreenRant article URL

### `screenrant_author`

- **HTTP:** `GET /screenrant/author`
- **What:** Get a ScreenRant author profile. Returns a ScreenRant author's profile by canonical `url` (`https://screenrant.com/author/<slug>/`): name, `title`, `biography`, image, social links (such as `x`, `linkedin`, `youtube` or `muckrack`) and about 20 articles from the profile's Latest module. Older pages are not available.
- **Params:** `url` (string, **required**) — Canonical ScreenRant author URL

### `screenrant_headlines`

- **HTTP:** `GET /screenrant/headlines`
- **What:** Get ScreenRant section headlines. Returns about 10 of the most recent ScreenRant items for one section. `section` is required and takes one of 34 slugs such as `movie-news`, `tv-reviews`, `reality-tv`, `comics`, `game-news` or `anime`. Items in `videos`, and some in `interviews` and `movie-trailers`, link to `/video/<slug>/` pages that `screenrant-article` rejects.
- **Params:** `section` (string, **required**) — ScreenRant RSS section slug

### `screenrant_news`

- **HTTP:** `GET /screenrant/news`
- **What:** Get ScreenRant top stories. Returns ScreenRant's main feed of latest stories, about 10 items. Takes no parameters. Each item has its title, URL, summary, publication time, author and image.
- **Params:** _none_

### `screenrant_sections`

- **HTTP:** `GET /screenrant/sections`
- **What:** Get ScreenRant RSS sections. Lists the 34 ScreenRant sections that `screenrant-headlines` accepts, spanning movies, TV, reality TV, comics, gaming, anime, books, interviews and videos. Each entry has a `slug`, a display `name` and the section's feed `url`.
- **Params:** _none_

## Seattle Times (5)

### `seattletimes_article`

- **HTTP:** `GET /seattletimes/article`
- **What:** Get Seattle Times article content. Returns public Seattle Times story metadata and body paragraphs from a canonical story URL. The site's metered paywall is a client-side overlay: anonymous requests receive the full body, which is returned as-is.
- **Params:** `url` (string, **required**) — Canonical Seattle Times story URL

### `seattletimes_author`

- **HTTP:** `GET /seattletimes/author`
- **What:** Get a Seattle Times author profile. Returns one Seattle Times author's public profile: name, bio, newsroom-published email and X/Twitter link when listed, and their most recent stories.
- **Params:** `slug` (string, optional) — Author slug, e.g. mike-lindblom; `url` (string, optional) — Canonical seattletimes.com/author/<slug>/ URL; alternative to slug

### `seattletimes_headlines`

- **HTTP:** `GET /seattletimes/headlines`
- **What:** Get Seattle Times section headlines. Returns about 30 to 35 of the latest Seattle Times stories for one section. `section` is required and takes a section slug such as `seattle-news`, `politics`, `boeing-aerospace`, `mariners`, `seahawks` or `obituaries`. Each item has its title, canonical URL without tracking parameters, summary, publication time and author. Only the newest page is available.
- **Params:** `section` (string, **required**) — Seattle Times section slug

### `seattletimes_news`

- **HTTP:** `GET /seattletimes/news`
- **What:** Get Seattle Times top stories. Returns about 30 of the newest Seattle Times stories across all sections, including Associated Press wire stories. Takes no parameters. Each item has its title, canonical URL without tracking parameters, summary, publication time, author byline and lead image.
- **Params:** _none_

### `seattletimes_sections`

- **HTTP:** `GET /seattletimes/sections`
- **What:** Get Seattle Times sections. Returns the public Seattle Times section inventory: every category in the site's navigation and RSS feed list that publishes a live feed.
- **Params:** _none_

## 7NEWS Australia (5)

### `sevennewsau_article`

- **HTTP:** `GET /sevennewsau/article`
- **What:** Get 7NEWS Australia article content. Returns public 7NEWS article metadata and body paragraphs from a canonical 7news.com.au article URL. 7NEWS articles are free to read; a non-free content tier, if one ever appears, is flagged as paywalled.
- **Params:** `url` (string, **required**) — Canonical 7NEWS article URL

### `sevennewsau_author`

- **HTTP:** `GET /sevennewsau/author`
- **What:** Get a 7NEWS Australia author profile. Returns one 7NEWS journalist's public profile: name, job title, biography, portrait, public social links and the latest stories listed on the profile page.
- **Params:** `slug` (string, optional) — Author slug, e.g. aimee-edwards; `url` (string, optional) — Canonical 7news.com.au/profile/<slug> URL; alternative to slug

### `sevennewsau_headlines`

- **HTTP:** `GET /sevennewsau/headlines`
- **What:** Get 7NEWS Australia section headlines. Returns the 100 most recent 7NEWS Australia stories for one topic. `section` is required and takes a topic slug such as `news-sydney`, `sport-afl` or `business-property`, which is the site path with slashes replaced by hyphens. Each item has its title, URL, summary, publication time, author when credited, and lead image.
- **Params:** `section` (string, **required**) — 7NEWS topic slug (the site path with slashes replaced by hyphens)

### `sevennewsau_news`

- **HTTP:** `GET /sevennewsau/news`
- **What:** Get 7NEWS Australia top stories. Returns the 100 most recent 7NEWS Australia stories across every section, with no input needed. Each item has its title, canonical URL, summary, publication time, lead image, and the author when one is credited. Agency copy is often credited to `Digital Staff`.
- **Params:** _none_

### `sevennewsau_sections`

- **HTTP:** `GET /sevennewsau/sections`
- **What:** Get 7NEWS Australia sections. Returns the public 7NEWS topic feed inventory accepted by the headlines endpoint: national and city news, sport, politics, business, entertainment, lifestyle and more.
- **Params:** _none_

## SFGate (5)

### `sfgate_article`

- **HTTP:** `GET /sfgate/article`
- **What:** Get SFGate article content. Returns public SFGATE article metadata and body paragraphs from a canonical article URL. Article pages are served through proxied browser renderers; the service does not bypass authentication or access controls, and marks paywalled=true when only a teaser is public.
- **Params:** `url` (string, **required**) — Canonical SFGate article URL

### `sfgate_author`

- **HTTP:** `GET /sfgate/author`
- **What:** Get an SFGate author profile. Returns an SFGATE author's name, job title, biography, headshot, public profile links, and recent articles from a canonical author URL. Author pages are served through proxied browser renderers; the service does not bypass authentication or access controls.
- **Params:** `url` (string, **required**) — Canonical SFGate author URL

### `sfgate_headlines`

- **HTTP:** `GET /sfgate/headlines`
- **What:** Get SFGate section headlines. Returns the latest SFGATE stories for one section. `section` is required and takes `top-news`, `bay-area`, `business-technology`, `entertainment`, `celebrity`, `food-dining`, `travel`, `routes`, `top-sports`, `giants`, `49ers` or `warriors`. Feeds hold 12 to 30 items, and the `warriors` feed is quiet in the off-season.
- **Params:** `section` (string, **required**) — SFGate section slug

### `sfgate_news`

- **HTTP:** `GET /sfgate/news`
- **What:** Get SFGate top stories. Returns the latest stories from SFGATE's Top News Stories feed: title, canonical URL, summary, author and publication time in UTC. Takes no parameters. The feed carries no images.
- **Params:** _none_

### `sfgate_sections`

- **HTTP:** `GET /sfgate/sections`
- **What:** Get SFGate sections. Returns the SFGATE feed inventory (Top News, Bay Area, Business and Technology, Entertainment, Celebrity, Food and Dining, Travel, Routes, Top Sports, Giants, 49ers, Warriors), each linking to its public RSS feed.
- **Params:** _none_

## Sky News (7)

### `skynews_article`

- **HTTP:** `GET /skynews/article`
- **What:** Get Sky News article content. Returns a Sky News article by canonical `url` of the form `https://news.sky.com/story/...-<id>`: title, description, section, authors, publication and update times, image, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Sky News article URL

### `skynews_author`

- **HTTP:** `GET /skynews/author`
- **What:** Get a Sky News author profile. Returns a Sky News author's profile by canonical `url` (`https://news.sky.com/author/<name>-<id>`): name, `job_title`, biography paragraphs and recent articles. An `info` list carries whatever else the page shows, as label and value entries with an optional link, such as expertise, location, social handles or email.
- **Params:** `url` (string, **required**) — Canonical Sky News author URL

### `skynews_headlines`

- **HTTP:** `GET /skynews/headlines`
- **What:** Get Sky News section headlines. Returns fresh headlines from one Sky News section, either its official RSS feed or (for the 5 sections with no feed) its public hub page.
- **Params:** `section` (string, **required**) — Sky News section slug

### `skynews_news`

- **HTTP:** `GET /skynews/news`
- **What:** Get Sky News top stories. Returns Sky News's latest top stories across the site. Takes no parameters. Each item has its title, URL, summary, publication time and image. Pass an item's URL to `skynews-article` for its body paragraphs.
- **Params:** _none_

### `skynews_sections`

- **HTTP:** `GET /skynews/sections`
- **What:** Get Sky News sections. Returns the Sky News section inventory: 9 official RSS feeds plus 5 additional site sections with no RSS feed, listed from their public hub page instead.
- **Params:** _none_

### `skynews_video`

- **HTTP:** `GET /skynews/video`
- **What:** Get Sky News video metadata. Returns one Sky News video's public metadata (title, description, thumbnails, duration, embed URL) from a canonical video URL. There is no transcript or article body for a video.
- **Params:** `url` (string, **required**) — Canonical Sky News video URL

### `skynews_videos`

- **HTTP:** `GET /skynews/videos`
- **What:** Get the Sky News videos hub. Lists recent videos from the Sky News videos hub. Takes no parameters. Each item has its title, URL, summary, author, lead image, publication time and type. An item's `url` can be passed to `skynews-video` to get that video's own metadata.
- **Params:** _none_

## Sky Sports (5)

### `skysports_article`

- **HTTP:** `GET /skysports/article`
- **What:** Get a Sky Sports article. Returns a Sky Sports article by `url`, an HTTPS `skysports.com` address with a sport news path such as `/football/news/<id>/<slug>`: title, description, section, authors, publication and update times, image and body `paragraphs`. The returned URL uses `www.skysports.com`, and query strings and fragments are discarded.
- **Params:** `url` (string, **required**) — Canonical Sky Sports article URL

### `skysports_author`

- **HTTP:** `GET /skysports/author`
- **What:** Get a Sky Sports author profile. Returns a Sky Sports author's name, current `job_title`, biography paragraphs and the article links on their profile page, from an author `url` such as `https://www.skysports.com/author/kaveh-solhekol-773`. Each article has a title and URL, with summary, author, publication time and image where present.
- **Params:** `url` (string, **required**) — Canonical Sky Sports author URL

### `skysports_headlines`

- **HTTP:** `GET /skysports/headlines`
- **What:** Get Sky Sports section headlines. Returns the article cards from one Sky Sports section listing page. `section` is required and takes one of 22 slugs such as `football`, `f1`, `cricket`, `rugby-union`, `golf`, `boxing`, `nfl` or `darts`. The site's Show More pagination is not exposed, so only the first listing comes back.
- **Params:** `section` (string, **required**) — Sky Sports section slug

### `skysports_news`

- **HTTP:** `GET /skysports/news`
- **What:** Get Sky Sports top stories. Returns the 20 latest Sky Sports top stories. Takes no parameters. Each item has its title, canonical `www.skysports.com` article URL, summary, publication time and image.
- **Params:** _none_

### `skysports_sections`

- **HTTP:** `GET /skysports/sections`
- **What:** Get Sky Sports sections. Lists the 22 Sky Sports sections that `skysports-headlines` accepts, from `football` and `f1` to `wwe` and `olympics`. Each entry has a `slug`, a display `name` and the section `url`. Winter Sports and Commonwealth Games pages returned 404 in the 2026-09-28 check and are not accepted.
- **Params:** _none_

## Slate (3)

### `slate_article`

- **HTTP:** `GET /slate/article`
- **What:** Slate article content. Returns public Slate article metadata and server-delivered body paragraphs from a canonical dated Slate URL. It does not log in, use account cookies, or bypass a challenge; is_paywalled reports when Slate marks the delivered page as subscription-gated.
- **Params:** `url` (string, **required**) — Canonical HTTPS Slate article URL

### `slate_categories`

- **HTTP:** `GET /slate/categories`
- **What:** Slate public feed sections. Lists the exact Slate section values accepted by slate-headlines. The set includes all, news-and-politics, culture, technology, business, life, and advice; subsection navigation pages are not RSS feeds and are intentionally not accepted by slate-headlines.
- **Params:** _none_

### `slate_headlines`

- **HTTP:** `GET /slate/headlines`
- **What:** Slate section headlines. Returns current Slate article-card metadata from one public RSS feed. section must be one of the values returned by slate-categories.
- **Params:** `section` (string, optional) — Slate feed section

## MIT Sloan Management Review (5)

### `sloanreview_article`

- **HTTP:** `GET /sloanreview/article`
- **What:** Get MIT Sloan Management Review article content. Returns an MIT Sloan Management Review article's metadata and full body paragraphs from an existing public archive.today snapshot. Sloan Review's origin HTML is paywalled/partial; no login, cookies, or subscription credentials are used. Coverage is partial and an article without a verified full snapshot returns 404.
- **Params:** `url` (string, **required**) — Canonical Sloan Review article URL

### `sloanreview_articles`

- **HTTP:** `GET /sloanreview/articles`
- **What:** List MIT Sloan Management Review article URLs. Returns a paginated, sitemap-backed index of all article URLs currently published by MIT Sloan Management Review. Use an item's URL with sloanreview-article to request archive-backed body content; archive availability remains dependent on a public snapshot existing for that article.
- **Params:** `page` (integer, optional) — 1-based page number (default 1); `page_size` (integer, optional) — Items per page, 1-500 (default 100)

### `sloanreview_categories`

- **HTTP:** `GET /sloanreview/categories`
- **What:** Get MIT Sloan Management Review topic taxonomy. Returns the complete public MIT Sloan Management Review topic taxonomy discovered from the site's All Topics page. The returned slugs are the accepted values for sloanreview-topic.
- **Params:** _none_

### `sloanreview_headlines`

- **HTTP:** `GET /sloanreview/headlines`
- **What:** Get MIT Sloan Management Review headlines. Returns the article cards on the MIT Sloan Management Review homepage, including editor picks and tiled feeds, with no parameters. Each item has a `title` and `url` and, when present, `topic`, `authors` and `published_at`. It covers the homepage only; the articles endpoint finds URLs beyond it.
- **Params:** _none_

### `sloanreview_topic`

- **HTTP:** `GET /sloanreview/topic`
- **What:** Get an MIT Sloan Management Review topic archive. Returns article cards from one public Sloan Review topic page. Use sloanreview-categories for the complete accepted slug set; this includes the primary navigation topics and the site's child topic pages.
- **Params:** `topic` (string, **required**) — Sloan Review topic slug returned by sloanreview-categories

## The Sydney Morning Herald (5)

### `smh_article`

- **HTTP:** `GET /smh/article`
- **What:** Get The Sydney Morning Herald article content. Returns one Sydney Morning Herald article's public metadata and the body paragraphs an anonymous visitor's page request is served, from a canonical article URL. The Sydney Morning Herald runs a metered subscription paywall; the response reports it with is_accessible_for_free (the page's own declaration), paywalled (the page marks the story as subscriber content), and is_truncated (the page served a shortened preview, or no body at all, instead of the full story). Paywalls are never bypassed and body text is never fabricated. Video-only pages are rejected with a 400.
- **Params:** `url` (string, **required**) — Canonical The Sydney Morning Herald article URL

### `smh_author`

- **HTTP:** `GET /smh/author`
- **What:** Get a Sydney Morning Herald journalist profile. Returns a Sydney Morning Herald journalist's public profile -- name, short biography, headshot, contact email and social links where published -- plus their recent stories, from a canonical https://www.smh.com.au/by/<name>-<id> URL.
- **Params:** `url` (string, **required**) — Canonical The Sydney Morning Herald journalist URL

### `smh_headlines`

- **HTTP:** `GET /smh/headlines`
- **What:** Get The Sydney Morning Herald section headlines. Returns the current stories for one Sydney Morning Herald section: title, canonical URL, summary, author, publication time, and image where the section lists them. section must be one of the slugs returned by /smh/sections; any other value is rejected with a 400 before The Sydney Morning Herald is contacted.
- **Params:** `section` (string, **required**) — Section slug from /smh/sections

### `smh_news`

- **HTTP:** `GET /smh/news`
- **What:** Get The Sydney Morning Herald top stories. Returns The Sydney Morning Herald's current "Latest News" public RSS feed: each story's title, canonical URL, summary, author, publication time, and lead image.
- **Params:** _none_

### `smh_sections`

- **HTTP:** `GET /smh/sections`
- **What:** Get The Sydney Morning Herald sections. Lists every Sydney Morning Herald section accepted by /smh/headlines (96 sections from the site's own section menu), each with its slug, display name, and public section-front URL.
- **Params:** _none_

## Space (5)

### `space_article`

- **HTTP:** `GET /space/article`
- **What:** Get Space.com article content. Returns a Space.com article by canonical `url` in any of the site's URL shapes, including older `.html` reference pages: title, description, section, authors, publication and update times, image and body `paragraphs`. `/news/live/` pages return only their introductory paragraphs, and membership-gated content returns only its public preview.
- **Params:** `url` (string, **required**) — Canonical Space.com article URL

### `space_author`

- **HTTP:** `GET /space/author`
- **What:** Get a Space.com author profile. Returns a Space.com author's profile, looked up by `slug` (for example `elizabeth-howell`) or canonical `url`; exactly one is required. The response has the name, `job_title`, biography, image and the first batch of recent articles on the author page. That page has no URL-based pagination, so no further articles are available.
- **Params:** `slug` (string, optional) — Author slug, e.g. elizabeth-howell; `url` (string, optional) — Canonical space.com/author/<slug> URL; alternative to slug

### `space_headlines`

- **HTTP:** `GET /space/headlines`
- **What:** Get Space.com section headlines. Returns the latest Space.com stories for one category. `section` is required and takes a slug from `space-sections`, which joins nested category paths with hyphens, such as `astronomy`, `astronomy-solar-system-mars` or `stargazing-meteor-showers`. Each item has its title, URL, summary, author, publication time and image. Other values return a 400.
- **Params:** `section` (string, **required**) — Space.com category slug

### `space_news`

- **HTTP:** `GET /space/news`
- **What:** Get Space.com top stories. Returns the latest Space.com top stories (space, astronomy and skywatching news) from the site's latest-news hub. Takes no parameters. Each item has its title, URL, summary, author, publication time and image.
- **Params:** _none_

### `space_sections`

- **HTTP:** `GET /space/sections`
- **What:** Get Space.com sections. Lists the Space.com categories that `space-headlines` accepts, from `astronomy`, `entertainment`, `science`, `space-exploration`, `stargazing` and `technology` down to their subcategories. Each entry has a `slug`, a display `name` and the category `url`. Slugs join the nested path with hyphens, so `astronomy-solar-system-mars` maps to `/astronomy/solar-system/mars`.
- **Params:** _none_

## Sporting News (5)

### `sportingnews_article`

- **HTTP:** `GET /sportingnews/article`
- **What:** Get Sporting News article content. Returns a Sporting News US article by canonical `url`, such as `https://www.sportingnews.com/us/nfl/dallas-cowboys/news/<slug>/<id>`: title, description, section (the sport or topic in the URL, for example `NFL`), authors, publication and update times, image and body `paragraphs`. Tables, embeds, ad slots and related-story lists are excluded. Non-US editions and hub pages are rejected.
- **Params:** `url` (string, **required**) — Canonical Sporting News US article URL

### `sportingnews_author`

- **HTTP:** `GET /sportingnews/author`
- **What:** Get a Sporting News author profile. Returns a Sporting News US author's profile, looked up by `slug` (for example `anne-erickson`) or canonical `url`; exactly one is required. The response has the name, `bio`, photo, social links and about 20 recent articles, each with title, URL, section, author, publication time and image. There is no pagination, and an unknown author returns not-found.
- **Params:** `slug` (string, optional) — Author slug, e.g. anne-erickson; `url` (string, optional) — Canonical sportingnews.com/us/author/<slug> URL; alternative to slug

### `sportingnews_headlines`

- **HTTP:** `GET /sportingnews/headlines`
- **What:** Get Sporting News section headlines. Returns up to 20 of the newest Sporting News US stories for one sport, league or topic. `section` is required and takes one of 44 slugs such as `nfl`, `nba`, `mlb`, `premier-league`, `formula-1`, `ufc` or `college`. Each item has its title, URL, summary, publication time, author and image. Off-season leagues may return older stories.
- **Params:** `section` (string, **required**) — Sporting News section slug

### `sportingnews_news`

- **HTTP:** `GET /sportingnews/news`
- **What:** Get Sporting News top stories. Returns fresh top stories from the Sporting News US edition public RSS feed. Only the US edition (sportingnews.com/us) is covered.
- **Params:** _none_

### `sportingnews_sections`

- **HTTP:** `GET /sportingnews/sections`
- **What:** Get Sporting News sections. Lists the 44 Sporting News US sport, league and topic feeds that `sportingnews-headlines` accepts. Each entry has a `slug`, a display `name` and the feed `url`. Off-season leagues such as `club-world-cup` and `softball` are listed and may return older items. Team feeds and non-US editions are not covered.
- **Params:** _none_

## Evening Standard (5)

### `standard_article`

- **HTTP:** `GET /standard/article`
- **What:** Get Evening Standard article content. Returns one Evening Standard article by its canonical `standard.co.uk` article `url`. The response has the title, description, publish and update times, section, authors, lead image, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Evening Standard article URL

### `standard_author`

- **HTTP:** `GET /standard/author`
- **What:** Get an Evening Standard author profile. Returns an Evening Standard author profile, found by `slug` (for example `nicholas-cecil`) or by a canonical `url`; send exactly one of the two. The response has the name, job title, bio, X/Twitter link and the author's recent articles with their section. It is one page, with no further pagination.
- **Params:** `slug` (string, optional) — Author slug, e.g. nicholas-cecil; `url` (string, optional) — Canonical standard.co.uk/author/<slug> URL; alternative to slug

### `standard_headlines`

- **HTTP:** `GET /standard/headlines`
- **What:** Get Evening Standard section headlines. Returns the latest Evening Standard headlines for one section. `section` is required and takes a slug such as `news/london`, `news/politics`, `sport/football`, `business/markets`, `culture/theatre` or `homesandproperty/renting`. Each item has its title, URL, summary, publication time, author and image.
- **Params:** `section` (string, **required**) — Evening Standard RSS section slug

### `standard_news`

- **HTTP:** `GET /standard/news`
- **What:** Get Evening Standard top stories. Returns the current Evening Standard top stories. Each item has its title, URL, summary, publication time, author and image. Takes no parameters; use `standard-headlines` for a single section.
- **Params:** _none_

### `standard_sections`

- **HTTP:** `GET /standard/sections`
- **What:** Get Evening Standard RSS sections. Lists the Evening Standard sections accepted by `standard-headlines`, as parent and child slugs such as `news`, `news/london`, `sport/rugby`, `going-out/restaurants` and `homesandproperty/gardening`. Each entry has the `slug`, display `name` and feed `url`.
- **Params:** _none_

## Minnesota Star Tribune (1)

### `startribune_news`

- **HTTP:** `GET /startribune/news`
- **What:** Get Minnesota Star Tribune top stories. Returns the public Star Tribune RSS feed with current story titles and canonical URLs; publisher summaries and publication dates are included when supplied by the feed. Optional bylines and images are returned only when present. Summaries are publisher teasers, not full article text. This feed-only route does not claim a complete section taxonomy or retrieve article bodies; use attribution when republishing feed content.
- **Params:** _none_

## The Straits Times (5)

### `straitstimes_article`

- **HTTP:** `GET /straitstimes/article`
- **What:** Get The Straits Times article content. Returns public The Straits Times article metadata and body paragraphs from a canonical article URL. A subscriber-only article returns only its publicly served teaser paragraphs with paywalled set to true.
- **Params:** `url` (string, **required**) — Canonical The Straits Times article URL

### `straitstimes_author`

- **HTTP:** `GET /straitstimes/author`
- **What:** Get a The Straits Times author profile. Returns a The Straits Times author's profile by `url`, a canonical `straitstimes.com/authors/<slug>` link: name, email when the author's page publishes one, and recent articles with title, URL, summary, author, image, `type` and publication time.
- **Params:** `url` (string, **required**) — Canonical The Straits Times author URL

### `straitstimes_headlines`

- **HTTP:** `GET /straitstimes/headlines`
- **What:** Get The Straits Times section headlines. Returns the current headlines for one The Straits Times section. `section` is required and takes a slug such as `singapore`, `singapore/housing`, `asia/se-asia`, `business/economy`, `sport/formula-one` or `breaking-news`. Items carry the title and URL. Top-level sections such as `singapore` and `business` add summary and publication time; subsection pages such as `singapore/housing` add an image when shown.
- **Params:** `section` (string, **required**) — The Straits Times section slug

### `straitstimes_news`

- **HTTP:** `GET /straitstimes/news`
- **What:** Get The Straits Times top stories. Returns the current top stories from The Straits Times. It takes no parameters. Each item has its title, URL and, where the outlet gives them, a summary, author, publication time, image URL and `type`. Use the headlines endpoint for one section.
- **Params:** _none_

### `straitstimes_sections`

- **HTTP:** `GET /straitstimes/sections`
- **What:** Get The Straits Times sections. Lists The Straits Times section slugs that the headlines endpoint accepts, including nested ones such as `singapore/politics`, `asia/east-asia`, `world/europe`, `life/food`, `business/invest`, `sport/tennis`, `tech` and `breaking-news`. Each entry has a `slug`, display `name` and `url`.
- **Params:** _none_

## Stuff (5)

### `stuff_article`

- **HTTP:** `GET /stuff/article`
- **What:** Get Stuff article content. Returns public Stuff article metadata and body paragraphs from a canonical article URL. A story the publisher marks premium is reported as paywalled, or refused with a permission error when no free text is available.
- **Params:** `url` (string, **required**) — Canonical Stuff article URL

### `stuff_author`

- **HTTP:** `GET /stuff/author`
- **What:** Get a Stuff author profile. Returns a Stuff (New Zealand) author's profile, looked up by `slug` (for example `damien-venuto`) or canonical `url`; exactly one is required. The response has the name, `job_title`, `location`, biography, headshot, `email` and recent stories. Fields show only what the profile has; shared team bylines usually carry just a job title. An unknown author returns not found.
- **Params:** `slug` (string, optional) — Author slug, e.g. damien-venuto; `url` (string, optional) — Canonical stuff.co.nz/authors/<slug> URL; alternative to slug

### `stuff_headlines`

- **HTTP:** `GET /stuff/headlines`
- **What:** Get Stuff section headlines. Returns the latest Stuff (New Zealand) stories for one section. `section` is required and takes one of 31 slugs, including slash-separated regional and sport ones such as `nz-news/auckland` and `sport/rugby`, plus `world-news`, `business`, `politics` and `motoring`. Each item has its title, URL, summary, publication time, author and image.
- **Params:** `section` (string, **required**) — Stuff section slug

### `stuff_news`

- **HTTP:** `GET /stuff/news`
- **What:** Get Stuff top stories. Returns the latest Stuff (New Zealand) top stories from the site-wide feed. Takes no parameters. Each item has its title, URL, summary, publication time, author and image where the feed provides them.
- **Params:** _none_

### `stuff_sections`

- **HTTP:** `GET /stuff/sections`
- **What:** Get Stuff sections. Lists the 31 Stuff sections that `stuff-headlines` accepts, including regional and sport slugs that contain a slash, such as `nz-news/auckland` and `sport/rugby`. Each entry has a `slug`, a display `name` and the section's Atom feed `url`.
- **Params:** _none_

## The Sun (5)

### `sun_article`

- **HTTP:** `GET /sun/article`
- **What:** Get The Sun article content. Returns one The Sun article by `url`, a canonical HTTPS article link. The response has the title, description, section, authors, publication and update times, lead image URL, body `paragraphs` and a `paywalled` flag. Subscriber-only or blocked pages return an error instead.
- **Params:** `url` (string, **required**) — Canonical The Sun article URL

### `sun_author`

- **HTTP:** `GET /sun/author`
- **What:** Get a Sun author profile. Returns a Sun author's profile by `url`, a canonical `thesun.co.uk/author/<slug>/` link: name, job title, bio and recent articles with title, URL, excerpt, category and category URL. `job_title` is often empty because most Sun bylines carry only a name and bio.
- **Params:** `url` (string, **required**) — Canonical The Sun author URL

### `sun_headlines`

- **HTTP:** `GET /sun/headlines`
- **What:** Get The Sun section headlines. Returns the current headlines for one The Sun section. `section` is required and takes one of `news`, `politics`, `royal-family`, `sport`, `showbiz`, `money`, `tech`, `fabulous`, `travel` or `health`. Every item has its title and URL. The `news` section also carries summary, author, publication time and image when the outlet provides them.
- **Params:** `section` (string, **required**) — The Sun section slug

### `sun_news`

- **HTTP:** `GET /sun/news`
- **What:** Get The Sun top stories. Returns the current top stories from The Sun. It takes no parameters. Each item has its title, URL and, where available, a summary, author, publication time, image URL and `type`. Use the headlines endpoint to read one section.
- **Params:** _none_

### `sun_sections`

- **HTTP:** `GET /sun/sections`
- **What:** Get The Sun sections. Lists the The Sun sections that the headlines endpoint accepts, such as `news`, `politics`, `royal-family`, `sport`, `showbiz`, `money`, `tech`, `fabulous`, `travel` and `health`. Each entry has a `slug`, a display `name` and a section `url`.
- **Params:** _none_

## TechCrunch (5)

### `techcrunch_article`

- **HTTP:** `GET /techcrunch/article`
- **What:** Get TechCrunch article content. Returns public TechCrunch article metadata (title, author(s), published/updated dates, dek, section, lead image) and body paragraphs from a canonical article URL.
- **Params:** `url` (string, **required**) — Canonical TechCrunch article URL

### `techcrunch_author`

- **HTTP:** `GET /techcrunch/author`
- **What:** Get a TechCrunch author profile. Returns one TechCrunch staff writer or contributor's public profile: name, job title, headshot, biography, social links, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page of recent articles to return; defaults to 1; `url` (string, **required**) — Canonical techcrunch.com/author/<slug> URL

### `techcrunch_headlines`

- **HTTP:** `GET /techcrunch/headlines`
- **What:** Get TechCrunch category headlines. Returns the latest TechCrunch stories for one category. `section` is required and takes one of 22 slugs such as `artificial-intelligence`, `startups`, `venture`, `security`, `fintech`, `space` or `cryptocurrency`. Each item has its title, URL, summary, publication time and author.
- **Params:** `section` (string, **required**) — TechCrunch category slug

### `techcrunch_news`

- **HTTP:** `GET /techcrunch/news`
- **What:** Get TechCrunch top stories. Returns the latest TechCrunch top stories from its home feed. Takes no parameters. Each item has its title, URL, summary, publication time and author name.
- **Params:** _none_

### `techcrunch_sections`

- **HTTP:** `GET /techcrunch/sections`
- **What:** Get TechCrunch categories. Lists the 22 TechCrunch categories that `techcrunch-headlines` accepts, taken from the site's primary navigation dropdown. Each entry has a stable `slug`, a display `name` and the category's feed `url`. For example, `artificial-intelligence` is named AI.
- **Params:** _none_

## TechRadar (5)

### `techradar_article`

- **HTTP:** `GET /techradar/article`
- **What:** Get TechRadar article content. Returns a TechRadar article by canonical `url` on `techradar.com`: title, description, section, authors, publication and update times, lead image, the body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical TechRadar article URL

### `techradar_author`

- **HTTP:** `GET /techradar/author`
- **What:** Get a TechRadar author profile. Returns a TechRadar author's profile, looked up by `slug` (for example `tom-power`) or canonical `url`, which may end in `/page/<n>`; exactly one is required. `page` (1-based, default 1) overrides any page in `url`. The response has the name, `job_title`, biography, social links, one page of articles and `has_next_page`.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. tom-power; `url` (string, optional) — Canonical techradar.com/author/<slug> URL, optionally with a /page/<n> segment; alternative to slug

### `techradar_headlines`

- **HTTP:** `GET /techradar/headlines`
- **What:** Get TechRadar section headlines. Returns the latest TechRadar stories for one section hub. `section` is required and takes one of 25 slugs such as `computing`, `phones`, `audio`, `gaming`, `deals`, `reviews`, `news` or `vpn`. Each item has its title, URL, summary, publication time, author and image.
- **Params:** `section` (string, **required**) — TechRadar section slug

### `techradar_news`

- **HTTP:** `GET /techradar/news`
- **What:** Get TechRadar top stories. Returns TechRadar's latest top stories across the site. Takes no parameters, and `techradar-headlines` narrows by section instead. Each item has its title, URL, summary, publication time, author and image.
- **Params:** _none_

### `techradar_sections`

- **HTTP:** `GET /techradar/sections`
- **What:** Get TechRadar sections. Lists the 25 top-level TechRadar sections that `techradar-headlines` accepts, such as `computing`, `phones`, `best`, `deals` and `how-to`. Each entry has a `slug`, a display `name` and the section page `url`.
- **Params:** _none_

## The Telegraph (5)

### `telegraph_article`

- **HTTP:** `GET /telegraph/article`
- **What:** Get The Telegraph article content. Returns one The Telegraph article by `url`, a canonical HTTPS article link. The response has the title, description, section, authors, publication and update times, image URL, body `paragraphs` and a `paywalled` flag. Access is intermittent, and subscriber-only or blocked pages return an error.
- **Params:** `url` (string, **required**) — Canonical The Telegraph article URL

### `telegraph_author`

- **HTTP:** `GET /telegraph/author`
- **What:** Get a Telegraph author profile. Returns a Telegraph author's profile by `url`, a canonical `telegraph.co.uk/authors/<letter>/<range>/<name>/` link: name, job title, bio and recent articles with title, URL, excerpt and ISO-8601 `published_at`. `job_title` can be empty for contributors without a masthead credit.
- **Params:** `url` (string, **required**) — Canonical Telegraph author URL

### `telegraph_headlines`

- **HTTP:** `GET /telegraph/headlines`
- **What:** Get The Telegraph section headlines. Returns the current headlines for one The Telegraph section. `section` is required and takes one of `uk-news`, `world-news`, `politics`, `business`, `finance`, `technology`, `sport`, `culture`, `travel`, `lifestyle`, `health`, `science` or `opinion`. Each item has its title and URL.
- **Params:** `section` (string, **required**) — The Telegraph section slug

### `telegraph_news`

- **HTTP:** `GET /telegraph/news`
- **What:** Get The Telegraph top stories. Returns the current top stories from The Telegraph. It takes no parameters. Each item has its title, URL and, where available, a summary, author, publication time, image URL and `type`. It can return an error when The Telegraph declines the request.
- **Params:** _none_

### `telegraph_sections`

- **HTTP:** `GET /telegraph/sections`
- **What:** Get The Telegraph sections. Lists the The Telegraph sections that the headlines endpoint accepts, such as `uk-news`, `world-news`, `politics`, `finance`, `culture` and `opinion`. Each entry has a `slug`, a display `name` and a section `url`.
- **Params:** _none_

## The Age (5)

### `theage_article`

- **HTTP:** `GET /theage/article`
- **What:** Get The Age article content. Returns one The Age article's public metadata and the body paragraphs an anonymous visitor's page request is served, from a canonical article URL. The Age runs a metered subscription paywall; the response reports it with is_accessible_for_free (the page's own declaration), paywalled (the page marks the story as subscriber content), and is_truncated (the page served a shortened preview, or no body at all, instead of the full story). Paywalls are never bypassed and body text is never fabricated. Video-only pages are rejected with a 400.
- **Params:** `url` (string, **required**) — Canonical The Age article URL

### `theage_author`

- **HTTP:** `GET /theage/author`
- **What:** Get an Age journalist profile. Returns an Age journalist's public profile -- name, short biography, headshot, contact email and social links where published -- plus their recent stories, from a canonical https://www.theage.com.au/by/<name>-<id> URL.
- **Params:** `url` (string, **required**) — Canonical The Age journalist URL

### `theage_headlines`

- **HTTP:** `GET /theage/headlines`
- **What:** Get The Age section headlines. Returns the current stories for one The Age section: title, canonical URL, summary, author, publication time, and image where the section lists them. section must be one of the slugs returned by /theage/sections; any other value is rejected with a 400 before The Age is contacted.
- **Params:** `section` (string, **required**) — Section slug from /theage/sections

### `theage_news`

- **HTTP:** `GET /theage/news`
- **What:** Get The Age top stories. Returns The Age's current "Latest News" public RSS feed: each story's title, canonical URL, summary, author, publication time, and lead image.
- **Params:** _none_

### `theage_sections`

- **HTTP:** `GET /theage/sections`
- **What:** Get The Age sections. Lists every The Age section accepted by /theage/headlines (96 sections from the site's own section menu), each with its slug, display name, and public section-front URL.
- **Params:** _none_

## The Atlantic (4)

### `theatlantic_article`

- **HTTP:** `GET /theatlantic/article`
- **What:** Get an Atlantic article's content. Returns one public Atlantic article's metadata and body paragraphs from a canonical article URL. `metered` reflects the site's own soft-paywall flag for that article; the body returned here is the same one the site's own page serves to an anonymous visitor and is never truncated because of it. An article whose page genuinely withholds its body is reported as a restricted-access error instead of a hollow response.
- **Params:** `url` (string, **required**) — Canonical The Atlantic article URL

### `theatlantic_author`

- **HTTP:** `GET /theatlantic/author`
- **What:** Get an Atlantic staff author profile. Returns one Atlantic staff author's public profile -- name, headshot, and biography -- plus their recent articles, from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical theatlantic.com/author/<slug>/ URL

### `theatlantic_headlines`

- **HTTP:** `GET /theatlantic/headlines`
- **What:** Get the latest stories in an Atlantic section. Returns the current front-page article cards for one Atlantic section: each story's title, canonical URL, description, byline, publication time, and lead image. Section must be a slug returned by /theatlantic/sections.
- **Params:** `section` (string, **required**) — Section slug from /theatlantic/sections

### `theatlantic_sections`

- **HTTP:** `GET /theatlantic/sections`
- **What:** List The Atlantic sections. Lists every top-level Atlantic section accepted by /theatlantic/headlines, with its slug, display name, and landing-page URL. Values: `ideas`, `politics`, `economy`, `international`, `national-security`, `technology`, `science`, `health`, `education`, `culture`, `family`, `books`, `photography`.
- **Params:** _none_

## The Daily Beast (5)

### `thedailybeast_article`

- **HTTP:** `GET /thedailybeast/article`
- **What:** Get The Daily Beast article content. Returns one The Daily Beast article by its canonical `url`, either a root-level slug or one under a single content vertical such as `obsessed`. The response has the title, description, section, authors, publication and update times, lead image URL, body `paragraphs` and a `paywalled` flag. Digest or index pages are not articles and return an error.
- **Params:** `url` (string, **required**) — Canonical The Daily Beast article URL

### `thedailybeast_author`

- **HTTP:** `GET /thedailybeast/author`
- **What:** Get a The Daily Beast author profile. Returns one The Daily Beast reporter's public profile: name, job title, biography, headshot, social link, and their recent articles, from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical thedailybeast.com/author/<slug> URL

### `thedailybeast_headlines`

- **HTTP:** `GET /thedailybeast/headlines`
- **What:** Get The Daily Beast section headlines. Returns the current headlines of one The Daily Beast section. `section` is required and takes a slug such as `politics`, `politics/opinion`, `obsessed/reviews`, `scouted/home` or `world/china`. Each item can carry its title, URL, summary, author, publication time, lead image and `type`, and the response echoes the `section`.
- **Params:** `section` (string, **required**) — The Daily Beast section slug

### `thedailybeast_news`

- **HTTP:** `GET /thedailybeast/news`
- **What:** Get The Daily Beast top stories. Returns the current top stories from The Daily Beast. It takes no parameters. Each item has its title, URL, summary, publication time, author and lead image, so it is a quick front-page view; use the headlines endpoint with a `section` slug for one category.
- **Params:** _none_

### `thedailybeast_sections`

- **HTTP:** `GET /thedailybeast/sections`
- **What:** Get The Daily Beast sections. Lists the sections of The Daily Beast that the headlines endpoint accepts, both top-level categories such as `politics` and `world` and child sub-sections such as `politics/opinion` and `world/middle-east`. Each entry has a `slug`, a display `name` and the section `url`.
- **Params:** _none_

## The Hill (5)

### `thehill_article`

- **HTTP:** `GET /thehill/article`
- **What:** Get The Hill article content. Returns one The Hill article by `url`, which must be a canonical HTTPS `thehill.com` article link containing a numeric article id. The response has the title, description, section, authors, publication and update times, lead image URL, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical The Hill article URL

### `thehill_author`

- **HTTP:** `GET /thehill/author`
- **What:** Get a The Hill author profile. Returns a The Hill author's profile by `url`, a canonical `thehill.com/author/<slug>/` link: name, job title, bio, image URL and recent articles with title, URL, category and category URL. `job_title` and `image_url` may be missing, and each article's `published_at` is relative text such as `10 hours ago`, not a timestamp.
- **Params:** `url` (string, **required**) — Canonical The Hill author URL

### `thehill_headlines`

- **HTTP:** `GET /thehill/headlines`
- **What:** Get The Hill section headlines. Returns the current headlines for one The Hill section. `section` is required and takes one of 19 slugs, including `home`, `policy`, `business`, `senate`, `national-security` and `technology`. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them, and the response echoes the `section`.
- **Params:** `section` (string, **required**) — The Hill RSS section slug

### `thehill_news`

- **HTTP:** `GET /thehill/news`
- **What:** Get The Hill top stories. Returns the current top stories from The Hill. It takes no parameters. Each item has its title, URL and, where the outlet gives them, a summary, author, publication time, image URL and `type`. Use the headlines endpoint to read one section instead.
- **Params:** _none_

### `thehill_sections`

- **HTTP:** `GET /thehill/sections`
- **What:** Get The Hill RSS sections. Lists the 19 The Hill section slugs that the headlines endpoint accepts, such as `home`, `policy`, `senate`, `defense` and `technology`. Each entry has the section `slug`, its display `name` and its `url`.
- **Params:** _none_

## The Hindu (5)

### `thehindu_article`

- **HTTP:** `GET /thehindu/article`
- **What:** Get The Hindu article content. Returns public The Hindu article metadata and body paragraphs from a canonical article URL. A story The Hindu marks subscriber-only returns a permission error instead of a body.
- **Params:** `url` (string, **required**) — Canonical The Hindu article URL

### `thehindu_author`

- **HTTP:** `GET /thehindu/author`
- **What:** Get a The Hindu author profile. Returns a The Hindu author's byline metadata, biography, contact/social links, and their most recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical The Hindu author URL

### `thehindu_headlines`

- **HTTP:** `GET /thehindu/headlines`
- **What:** Get The Hindu section headlines. Returns the current headlines for one The Hindu section. `section` is required and takes a slug such as `news-national`, `opinion-editorial`, `business-markets`, `sport-cricket` or `sci-tech-health`. Items carry the title, URL, summary, author, publication time and image, and the response echoes the `section`.
- **Params:** `section` (string, **required**) — The Hindu section slug

### `thehindu_news`

- **HTTP:** `GET /thehindu/news`
- **What:** Get The Hindu top stories. Returns the current stories from The Hindu's Latest News listing. It takes no parameters. Each item has its title, URL and, where available, a summary, author, publication time, image URL and `type`. For a single desk such as cricket or business, use the headlines endpoint.
- **Params:** _none_

### `thehindu_sections`

- **HTTP:** `GET /thehindu/sections`
- **What:** Get The Hindu sections. Lists the The Hindu section slugs that the headlines endpoint accepts, covering news, opinion, business, sport, entertainment, sci-tech, education, life and style, society, books and food, for example `news-national`, `sport-cricket` and `food-recipes`. Each entry has a `slug`, `name` and `url`.
- **Params:** _none_

## TheJournal.ie (5)

### `thejournal_article`

- **HTTP:** `GET /thejournal/article`
- **What:** Get TheJournal.ie article content. Returns public TheJournal.ie article metadata and body paragraphs from a canonical article URL. Stories are served in full to anonymous readers, so paywalled is never set.
- **Params:** `url` (string, **required**) — Canonical TheJournal.ie article URL

### `thejournal_author`

- **HTTP:** `GET /thejournal/author`
- **What:** Get a TheJournal.ie author page. Returns one TheJournal.ie author's public archive page: name, numeric author id, and the most recent articles the first page lists.
- **Params:** `slug` (string, optional) — Author slug, e.g. ottoline-spearman; `url` (string, optional) — Canonical thejournal.ie/author/<slug>/ URL, optionally with the numeric author id; alternative to slug

### `thejournal_headlines`

- **HTTP:** `GET /thejournal/headlines`
- **What:** Get TheJournal.ie section headlines. Returns current headlines from one public TheJournal.ie section listing page, with the story type label, summary and image when the page shows them.
- **Params:** `section` (string, **required**) — TheJournal.ie section slug

### `thejournal_news`

- **HTTP:** `GET /thejournal/news`
- **What:** Get TheJournal.ie top stories. Returns the latest TheJournal.ie stories across all sections. Each item has a title, canonical URL, short summary, publication time (RFC 3339, UTC) and lead image. Items carry no author byline; the article endpoint supplies it. It takes no parameters.
- **Params:** _none_

### `thejournal_sections`

- **HTTP:** `GET /thejournal/sections`
- **What:** Get TheJournal.ie sections. Lists the 22 TheJournal.ie sections that the headlines endpoint accepts, verified 2026-09-25: nine category pages such as `irish`, `politics` and `business`, plus topic pages such as `housing`, `courts`, `ukraine` and `gaza`. Each entry has a `slug`, `name` and listing page `url`. Topic pages outside the site navigation are not served.
- **Params:** _none_

## The Star Malaysia (5)

### `thestarmy_article`

- **HTTP:** `GET /thestarmy/article`
- **What:** Get The Star (Malaysia) article content. Returns public The Star (Malaysia) story metadata and body paragraphs from a canonical story URL. Metered and premium stories return only the public teaser paragraphs the server shows anonymous readers, flagged with paywalled; a story with no readable teaser returns a permission error.
- **Params:** `url` (string, **required**) — Canonical The Star (Malaysia) story URL

### `thestarmy_author`

- **HTTP:** `GET /thestarmy/author`
- **What:** Get a The Star (Malaysia) author page. Returns one The Star (Malaysia) byline's public author page: display name, the public byline email, and their most recent stories.
- **Params:** `name` (string, optional) — Byline name, matched case-insensitively, e.g. Ivan Loh; `url` (string, optional) — Canonical thestar.com.my/authors?q=<name> URL; alternative to name

### `thestarmy_headlines`

- **HTTP:** `GET /thestarmy/headlines`
- **What:** Get The Star (Malaysia) section headlines. Returns the current stories of one The Star (Malaysia) section page, usually 10 and up to 100 on column-style sections. `section` is required, for example `news-nation`, `latest-business`, `sport-badminton` or `latest-food`. Items have a title and URL, and when the page shows them a `type`, summary, byline, image and publication time. Older stories are not paginated.
- **Params:** `section` (string, **required**) — The Star (Malaysia) section slug

### `thestarmy_news`

- **HTTP:** `GET /thestarmy/news`
- **What:** Get The Star (Malaysia) top stories. Returns the current top stories on The Star (Malaysia) home page. It takes no parameters. Each item has a title and canonical URL, plus a short section label in `type`, a summary and a byline when the page shows them. `published_at` is omitted here; the section headlines endpoint carries it.
- **Params:** _none_

### `thestarmy_sections`

- **HTTP:** `GET /thestarmy/sections`
- **What:** Get The Star (Malaysia) sections. Lists the 94 The Star (Malaysia) sections that returned at least one story to an anonymous reader when checked on 2026-09-25, and that the headlines endpoint accepts. Examples are `news-latest`, `latest-nation`, `business-smebiz` and `sport-football`. Each entry has a `slug`, a `name` and the section page `url`.
- **Params:** _none_

## The Verge (5)

### `theverge_article`

- **HTTP:** `GET /theverge/article`
- **What:** Get The Verge article content. Returns one The Verge article by `url`, a canonical HTTPS article link. The response has the title, description, section, authors, publication and update times, lead image URL, body `paragraphs` and a `paywalled` flag. Subscriber-only or blocked pages return an error instead.
- **Params:** `url` (string, **required**) — Canonical The Verge article URL

### `theverge_author`

- **HTTP:** `GET /theverge/author`
- **What:** Get a The Verge author profile. Returns a The Verge author's profile by `url`, a canonical `theverge.com/authors/<slug>` link: name, job title such as Senior Reporter, bio and recent articles. Each article has a title, URL, excerpt, ISO-8601 `published_at` and `category`, the post's primary Verge vertical such as Tech.
- **Params:** `url` (string, **required**) — Canonical The Verge author URL

### `theverge_headlines`

- **HTTP:** `GET /theverge/headlines`
- **What:** Get The Verge section headlines. Returns the current headlines for one The Verge section. `section` is required and takes one of `tech`, `reviews`, `science`, `entertainment`, `ai`, `policy`, `gaming`, `mobile`, `apps` or `features`. Each item has its title, URL, summary, author and publication time.
- **Params:** `section` (string, **required**) — The Verge section slug

### `theverge_news`

- **HTTP:** `GET /theverge/news`
- **What:** Get The Verge top stories. Returns the current top stories from The Verge. It takes no parameters. Each item has its title, URL and, where available, a summary, author, publication time, image URL and `type`. Use the headlines endpoint to read one section.
- **Params:** _none_

### `theverge_sections`

- **HTTP:** `GET /theverge/sections`
- **What:** Get The Verge sections. Lists the The Verge sections that the headlines endpoint accepts: `tech`, `reviews`, `science`, `entertainment`, `ai`, `policy`, `gaming`, `mobile`, `apps` and `features`. Each entry has a `slug`, a display `name` and a section `url`.
- **Params:** _none_

## This Is Money (5)

### `thisismoney_article`

- **HTTP:** `GET /thisismoney/article`
- **What:** Get This Is Money article content. Returns one This Is Money article by `url`, a canonical HTTPS article link. The response has the title, description, section, authors, publication and update times, image URL, body `paragraphs` and a `paywalled` flag. Pages that are subscriber-only or blocked return an error.
- **Params:** `url` (string, **required**) — Canonical This Is Money article URL

### `thisismoney_author`

- **HTTP:** `GET /thisismoney/author`
- **What:** Get a This Is Money author profile. Returns a This Is Money author's profile by `url`, a canonical `thisismoney.co.uk/profile-<id>/<slug>.html` link: name, job title, bio, coverage topic tags such as Money or Bills, and recent articles with title, URL, excerpt and ISO-8601 `published_at`. `job_title` and `coverage` can be empty.
- **Params:** `url` (string, **required**) — Canonical This Is Money author URL

### `thisismoney_headlines`

- **HTTP:** `GET /thisismoney/headlines`
- **What:** Get This Is Money section headlines. Returns the current headlines for one This Is Money section. `section` is required and takes one of `money`, `markets`, `investing`, `savings`, `pensions`, `mortgages`, `property`, `cars`, `travel` or `consumer`. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them.
- **Params:** `section` (string, **required**) — This Is Money section slug

### `thisismoney_news`

- **HTTP:** `GET /thisismoney/news`
- **What:** Get This Is Money top stories. Returns the current top stories from This Is Money. It takes no parameters. Each item has its title, URL and, where available, a summary, author, publication time, image URL and `type`. Use the headlines endpoint to read one section.
- **Params:** _none_

### `thisismoney_sections`

- **HTTP:** `GET /thisismoney/sections`
- **What:** Get This Is Money sections. Lists the This Is Money sections that the headlines endpoint accepts, such as `money`, `markets`, `savings`, `pensions`, `mortgages`, `property` and `cars`. Each entry has a `slug`, a display `name` and a section `url`.
- **Params:** _none_

## TIME (5)

### `time_article`

- **HTTP:** `GET /time/article`
- **What:** Get TIME article content. Returns one TIME article by `url`, which must be a canonical HTTPS dated `time.com` article link. The response has the title, description, section, authors, publication and update times, lead image URL, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical TIME article URL

### `time_author`

- **HTTP:** `GET /time/author`
- **What:** Get a TIME author profile. Returns a TIME author's profile by `url`, a canonical `time.com/author/<slug>/` link: name, job title, bio, image URL, social account links and recent articles with title, URL, excerpt, section, section URL and ISO-8601 `published_at`. Not every author lists a social account.
- **Params:** `url` (string, **required**) — Canonical TIME author URL

### `time_headlines`

- **HTTP:** `GET /time/headlines`
- **What:** Get TIME section headlines. Returns the current headlines for one TIME section. `section` is required and takes one of `news`, `politics`, `world`, `business`, `technology`, `health`, `entertainment`, `sports`, `ideas` or `climate`. Each item has its title and URL.
- **Params:** `section` (string, **required**) — TIME RSS section slug

### `time_news`

- **HTTP:** `GET /time/news`
- **What:** Get TIME top stories. Returns the current top stories from TIME. It takes no parameters. Each item has its title, URL and, where available, a summary, author, publication time, image URL and `type`. Use the headlines endpoint to read one section.
- **Params:** _none_

### `time_sections`

- **HTTP:** `GET /time/sections`
- **What:** Get TIME RSS sections. Lists the 10 TIME section slugs that the headlines endpoint accepts: `news`, `politics`, `world`, `business`, `technology`, `health`, `entertainment`, `sports`, `ideas` and `climate`. Each entry has a `slug`, a display `name` and a `url`.
- **Params:** _none_

## Times of India (5)

### `timesofindia_article`

- **HTTP:** `GET /timesofindia/article`
- **What:** Get The Times of India article content. Returns public Times of India article metadata (title, author(s), published/updated dates, section, lead image) and body paragraphs from a canonical article URL. A story gated behind a subscription returns a permission error instead of a truncated or fabricated body.
- **Params:** `url` (string, **required**) — Canonical Times of India article URL

### `timesofindia_author`

- **HTTP:** `GET /timesofindia/author`
- **What:** Get a Times of India author profile. Returns a Times of India reporter's profile by `url`, a canonical `timesofindia.indiatimes.com/toireporter/author-<name>-<id>.cms` link: name, job title, organization, location, email, biography, headshot and recent articles with title and URL. Fields the profile page does not publish may be empty.
- **Params:** `url` (string, **required**) — Canonical Times of India author URL

### `timesofindia_headlines`

- **HTTP:** `GET /timesofindia/headlines`
- **What:** Get The Times of India section headlines. Returns the current headlines for one Times of India section or city edition. `section` is required, for example `top-stories`, `india`, `world`, `business`, `cricket`, `mumbai`, `delhi` or `bangalore`. Items carry the title and URL, plus summary, author, publication time and image when the outlet provides them.
- **Params:** `section` (string, **required**) — Times of India section slug

### `timesofindia_news`

- **HTTP:** `GET /timesofindia/news`
- **What:** Get The Times of India top stories. Returns the current Times of India top stories. It takes no parameters. Each item has its title, URL, summary, publication time with its UTC offset, author and image URL. Use the headlines endpoint for a section or city edition.
- **Params:** _none_

### `timesofindia_sections`

- **HTTP:** `GET /timesofindia/sections`
- **What:** Get The Times of India sections. Lists the 55 Times of India sections that the headlines endpoint accepts, covering national and international topics such as `india`, `world`, `business` and `cricket`, and India city editions such as `mumbai`, `delhi` and `bangalore`. Each entry has a `slug`, a display `name` and the section feed `url`.
- **Params:** _none_

## Times of Israel (5)

### `timesofisrael_article`

- **HTTP:** `GET /timesofisrael/article`
- **What:** Get Times of Israel article content. Returns public Times of Israel article metadata and body paragraphs from a canonical article URL. Both regular story pages and individual liveblog-update pages (/liveblog_entry/<slug>/) are accepted.
- **Params:** `url` (string, **required**) — Canonical Times of Israel article URL

### `timesofisrael_author`

- **HTTP:** `GET /timesofisrael/author`
- **What:** Get a Times of Israel author profile. Returns a Times of Israel writer's byline metadata, biography, social links, and recent articles from a canonical writer profile URL.
- **Params:** `url` (string, **required**) — Canonical Times of Israel author URL

### `timesofisrael_headlines`

- **HTTP:** `GET /timesofisrael/headlines`
- **What:** Get Times of Israel section headlines. Returns the current headlines for one Times of Israel section. `section` is required and takes one of `israel-and-the-region`, `israel-inside`, `jewish-times`, `real-estate-israel` or `tech-israel`. Each item has its title and URL.
- **Params:** `section` (string, **required**) — Times of Israel section slug

### `timesofisrael_news`

- **HTTP:** `GET /timesofisrael/news`
- **What:** Get Times of Israel top stories. Returns the latest Times of Israel stories. It takes no parameters. Each item has a title, URL and publication time. The list includes both regular story pages and individual liveblog-update pages, so expect some entries to be short updates.
- **Params:** _none_

### `timesofisrael_sections`

- **HTTP:** `GET /timesofisrael/sections`
- **What:** Get Times of Israel sections. Lists the five Times of Israel sections that the headlines endpoint accepts: `israel-and-the-region`, `israel-inside`, `jewish-times`, `real-estate-israel` and `tech-israel`. Each entry has a `slug`, a display `name` and a section `url`.
- **Params:** _none_

## TMZ (5)

### `tmz_article`

- **HTTP:** `GET /tmz/article`
- **What:** Get TMZ article content. Returns one TMZ article by `url`, a canonical HTTPS `tmz.com` link of the form `/<year>/<month>/<day>/<slug>/`. The response has the title, description, section, authors, publication and update times, image URL, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical TMZ article URL

### `tmz_author`

- **HTTP:** `GET /tmz/author`
- **What:** Get a TMZ person profile. Returns a named person's TMZ profile hub: their name and their most recent TMZ coverage, from a canonical person-hub URL or slug. TMZ credits virtually all of its editorial content to a single "TMZ Staff" byline with no individual journalist profile pages, so this endpoint surfaces TMZ's own public per-person coverage hub (used for both celebrities and other newsmakers TMZ covers) as the closest available "profile + recent articles" surface.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Person slug, e.g. dolly-parton; `url` (string, optional) — Canonical tmz.com/people/<slug> URL, optionally with a ?page= query parameter; alternative to slug

### `tmz_headlines`

- **HTTP:** `GET /tmz/headlines`
- **What:** Get TMZ section headlines. Returns the current headlines for one TMZ section. `section` is required and must be `news` or `sports`. Each item has its title, URL and, where available, a summary, author, publication time, image and `type`, and the response echoes the `section`.
- **Params:** `section` (string, **required**) — TMZ section slug

### `tmz_news`

- **HTTP:** `GET /tmz/news`
- **What:** Get TMZ top stories. Returns the current TMZ celebrity news top stories. It takes no parameters. Each item has its title, URL and, where available, an author such as TMZ Staff, a summary, publication time and image URL. Use the headlines endpoint with `sports` for sports stories.
- **Params:** _none_

### `tmz_sections`

- **HTTP:** `GET /tmz/sections`
- **What:** Get TMZ sections. Returns the TMZ section inventory accepted by tmz-headlines: News (the home feed) and Sports. TMZ's public site has no broader stable editorial-category taxonomy beyond its own small main navigation -- see tmz-headlines for details.
- **Params:** _none_

## Tom's Guide (5)

### `tomsguide_article`

- **HTTP:** `GET /tomsguide/article`
- **What:** Get Tom's Guide article content. Returns one Tom's Guide article by `url`, a canonical HTTPS `tomsguide.com` link such as `tomsguide.com/<section>/<slug>`. The response has the title, description, section, authors, publication and update times, image URL, body `paragraphs` and a `paywalled` flag. On some product reviews `authors` may be empty.
- **Params:** `url` (string, **required**) — Canonical Tom's Guide article URL

### `tomsguide_author`

- **HTTP:** `GET /tomsguide/author`
- **What:** Get a Tom's Guide author profile. Returns a Tom's Guide author's name, job title, biography, social links and one page of recent articles. Give exactly one of `slug` or `url`; `page` is 1-based, defaults to 1 and overrides any page in `url`. The response also has `page` and `has_next_page`.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. tom-pritchard; `url` (string, optional) — Canonical tomsguide.com/author/<slug> URL, optionally with a /page/<n> segment; alternative to slug

### `tomsguide_headlines`

- **HTTP:** `GET /tomsguide/headlines`
- **What:** Get Tom's Guide section headlines. Returns the current headlines for one Tom's Guide section. `section` is required and takes one of 22 slugs, such as `ai`, `audio`, `deals`, `how-to`, `news`, `reviews`, `tvs` or `phones`. Each item has its title, URL, summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Tom's Guide section slug

### `tomsguide_news`

- **HTTP:** `GET /tomsguide/news`
- **What:** Get Tom's Guide top stories. Returns the current top stories from Tom's Guide. It takes no parameters. Each item has its title, URL and, where available, a summary, author, publication time, image URL and `type`. Use the headlines endpoint to read one section.
- **Params:** _none_

### `tomsguide_sections`

- **HTTP:** `GET /tomsguide/sections`
- **What:** Get Tom's Guide sections. Lists the 22 top-level Tom's Guide content verticals that the headlines endpoint accepts, such as `ai`, `best-picks`, `how-to`, `mattresses`, `reviews`, `vehicle-tech` and `phones`. Each entry has a `slug`, a display `name` and a `url`.
- **Params:** _none_

## Tom's Hardware (5)

### `tomshardware_article`

- **HTTP:** `GET /tomshardware/article`
- **What:** Get Tom's Hardware article content. Returns one Tom's Hardware article by its canonical `url`, either the current `tomshardware.com/<section>/<subsection>/<slug>` form or the legacy `/reviews/<slug>,<id>.html` form. The response has the title, description, authors, section, published and updated times, lead image, the body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Tom's Hardware article URL

### `tomshardware_author`

- **HTTP:** `GET /tomshardware/author`
- **What:** Get a Tom's Hardware author profile. Returns a Tom's Hardware author profile with name, job title, biography, social links and one page of recent articles. Identify the author with `slug` (such as `christian-eberle`) or an author `url`; `page` (default 1) overrides any page in the URL. `has_next_page` tells you whether more articles exist.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. christian-eberle; `url` (string, optional) — Canonical tomshardware.com/author/<slug> URL, optionally with a /page/<n> segment; alternative to slug

### `tomshardware_headlines`

- **HTTP:** `GET /tomshardware/headlines`
- **What:** Get Tom's Hardware section headlines. Lists the current headlines for one Tom's Hardware section. `section` is required and takes a slug such as `gpus`, `cpus`, `laptops`, `deals`, `reviews` or `news`; use `tomshardware-sections` for the full set. Each item has its title, URL, author, publication time and lead image, plus a summary when the section's listing provides one.
- **Params:** `section` (string, **required**) — Tom's Hardware section slug

### `tomshardware_news`

- **HTTP:** `GET /tomshardware/news`
- **What:** Get Tom's Hardware top stories. Returns the latest Tom's Hardware top stories with no parameters. Each item has its title, URL, summary, author, publication time and lead image. Use the item URLs with `tomshardware-article` to read the body.
- **Params:** _none_

### `tomshardware_sections`

- **HTTP:** `GET /tomshardware/sections`
- **What:** Get Tom's Hardware sections. Lists the 20 Tom's Hardware top-level sections that `tomshardware-headlines` accepts, including `3d-printing`, `cpus`, `gpus`, `monitors`, `news` and `reviews`. Each section carries its `slug`, display `name` and page `url`. Takes no parameters.
- **Params:** _none_

## Toronto Star (5)

### `torontostar_article`

- **HTTP:** `GET /torontostar/article`
- **What:** Get Toronto Star article content. Returns public Toronto Star article metadata and the body paragraphs shown to an anonymous reader from a canonical article URL. The Star meters its articles, so paywalled is true and paragraphs holds only the public teaser (typically the first two paragraphs) whenever the page hides the rest from non-subscribers.
- **Params:** `url` (string, **required**) — Canonical Toronto Star article URL

### `torontostar_author`

- **HTTP:** `GET /torontostar/author`
- **What:** Get a Toronto Star author profile. Returns one Toronto Star author's public profile: name, job title, biography, location and topic focus, avatar, and their recent articles.
- **Params:** `slug` (string, optional) — Author profile slug (thestar.com/users/profile/<slug>); use this or url; `url` (string, optional) — Canonical thestar.com/users/profile/<slug> URL; alternative to slug

### `torontostar_headlines`

- **HTTP:** `GET /torontostar/headlines`
- **What:** Get Toronto Star section headlines. Returns fresh Toronto Star headlines from one public section page, with summary, publish time and image when the page shows them.
- **Params:** `section` (string, **required**) — Toronto Star section path

### `torontostar_news`

- **HTTP:** `GET /torontostar/news`
- **What:** Get Toronto Star top stories. Returns the newest Toronto Star editorial stories (up to 50, newest first) from the public news sitemap. Press-release and sponsored pages are excluded.
- **Params:** _none_

### `torontostar_sections`

- **HTTP:** `GET /torontostar/sections`
- **What:** Get Toronto Star sections. Lists the 69 Toronto Star sections accepted by the headlines endpoint, taken from thestar.com's main navigation. Each has a `slug`, a display `name` and a `url`. Nested sections use slash paths such as `news/gta`, `sports/hockey/pwhl` and `business/technology`. Takes no parameters.
- **Params:** _none_

## Townhall (5)

### `townhall_article`

- **HTTP:** `GET /townhall/article`
- **What:** Get Townhall article content. Returns public Townhall article metadata and body paragraphs from a canonical news or column URL. VIP stories are flagged with paywalled and return only the free lead paragraphs.
- **Params:** `url` (string, **required**) — Canonical Townhall article URL

### `townhall_author`

- **HTTP:** `GET /townhall/author`
- **What:** Get a Townhall author profile. Returns a Townhall author profile by `slug` (such as `amy-curtis`) or by an author `url`; exactly one is required. The response has the name, photo, bio, X profile link and the first page of the author's archive, about 50 stories, each with its section label and a `vip` flag. Unknown authors return a not-found error.
- **Params:** `slug` (string, optional) — Author slug, e.g. amy-curtis; `url` (string, optional) — Canonical townhall.com/author/<slug> URL; alternative to slug

### `townhall_headlines`

- **HTTP:** `GET /townhall/headlines`
- **What:** Get Townhall section headlines. Lists headlines for one Townhall section. `section` is required: `news` and `columnists` return the 20 most recent stories, while the topic sections (such as `congress`, `economy` or `iran`) return up to 30 stories mixing news and columns. Items carry title, URL, image and, when available, author, time and summary.
- **Params:** `section` (string, **required**) — Townhall section slug

### `townhall_news`

- **HTTP:** `GET /townhall/news`
- **What:** Get Townhall top stories. Returns the latest Townhall stories, news and opinion columns mixed, newest first, about 50 items. Each has its title, URL, short summary, publication time, author byline and lead image. Video pages are left out. Takes no parameters.
- **Params:** _none_

### `townhall_sections`

- **HTTP:** `GET /townhall/sections`
- **What:** Get Townhall sections. Returns the public Townhall section inventory: the site-wide news and column feeds plus the editorial topic hubs the site promotes.
- **Params:** _none_

## USA Today (5)

### `usatoday_article`

- **HTTP:** `GET /usatoday/article`
- **What:** Get a USA Today article's content. Returns one normal USA Today article's public metadata and body paragraphs from a canonical article URL. Video, gallery, and other non-article routes are not supported.
- **Params:** `url` (string, **required**) — Canonical USA Today article URL

### `usatoday_author`

- **HTTP:** `GET /usatoday/author`
- **What:** Get a USA Today staff/author profile. Returns one USA Today staff writer's public profile: name, bio, social accounts, and their recent articles, from a canonical staff page URL.
- **Params:** `url` (string, **required**) — Canonical USA Today staff URL

### `usatoday_headlines`

- **HTTP:** `GET /usatoday/headlines`
- **What:** Get USA Today section headlines. Returns the newest USA Today items for one top-level section, up to 100. `section` is required and takes `news`, `sports`, `entertainment`, `life`, `money`, `tech`, `travel`, `opinion`, `cars`, `shopping`, `weather`, `politics` or `grocery`. Each item has its title, URL, published and updated times, and lead image when there is one.
- **Params:** `section` (string, **required**) — Top-level USA Today section

### `usatoday_news`

- **HTTP:** `GET /usatoday/news`
- **What:** Get fresh USA Today headlines. Returns the newest window of USA Today's public news feed: title, canonical URL, publication and update times, and the lead image when USA Today publishes one.
- **Params:** _none_

### `usatoday_sections`

- **HTTP:** `GET /usatoday/sections`
- **What:** List USA Today sections. Lists the 13 top-level USA Today sections accepted by `usatoday-headlines`, from `news` and `sports` to `politics` and `grocery`. Each has a `slug`, a display `name` and a landing-page `url`. Takes no parameters.
- **Params:** _none_

## Us Weekly (5)

### `usmagazine_article`

- **HTTP:** `GET /usmagazine/article`
- **What:** Get Us Weekly article content. Returns one Us Weekly article by its canonical `url`, in the form `/<section>/news/<slug>/`. The response has the title, description, published and updated times, section, authors, lead image and the body `paragraphs`, without sub-headings or embeds. Photo-gallery URLs and non-article pages return a 400 error.
- **Params:** `url` (string, **required**) — Canonical Us Weekly article URL

### `usmagazine_author`

- **HTTP:** `GET /usmagazine/author`
- **What:** Get a Us Weekly author profile. Returns a Us Weekly author's profile from their canonical `url` (`/author/<slug>/`, required): name, biography, contact links and the newest articles, about 20. Staff and desk bylines may have no biography or links. Photo galleries are skipped and `published_at` is not set on the articles.
- **Params:** `url` (string, **required**) — Canonical Us Weekly author URL

### `usmagazine_headlines`

- **HTTP:** `GET /usmagazine/headlines`
- **What:** Get Us Weekly section headlines. Lists recent Us Weekly headlines for one section. `section` is required and takes `celebrity-news`, `entertainment`, `sports`, `shopping`, `crime-news`, `stylish`, `celebrity-moms`, `celebrity-body`, `food`, `reviews`, `reality-tv` or `royal-family`. Returns up to about 20 items, with photo galleries excluded; `reviews` holds only a few.
- **Params:** `section` (string, **required**) — Us Weekly RSS section slug

### `usmagazine_news`

- **HTTP:** `GET /usmagazine/news`
- **What:** Get Us Weekly top stories. Returns the latest Us Weekly top stories with no parameters. Each item has its title and URL, plus summary, publication time, author and image when the outlet provides them. Only article URLs of the form `/<section>/news/<slug>/` appear; photo galleries are left out.
- **Params:** _none_

### `usmagazine_sections`

- **HTTP:** `GET /usmagazine/sections`
- **What:** Get Us Weekly RSS sections. Lists the 12 Us Weekly sections accepted by `usmagazine-headlines`, from `celebrity-news` and `entertainment` to `reality-tv` and `royal-family`. Each entry has a `slug`, display `name` and section feed `url`. Takes no parameters.
- **Params:** _none_

## Vanguard (5)

### `vanguardng_article`

- **HTTP:** `GET /vanguardng/article`
- **What:** Get Vanguard article content. Returns one Vanguard (Nigeria) story by its `url`, a vanguardngr.com link in the `/YYYY/MM/<slug>/` form; section pages and feeds are rejected. The response has the title, description, times, section, authors, lead image and body `paragraphs`. Vanguard has no paywall, so `paywalled` is never set.
- **Params:** `url` (string, **required**) — Canonical Vanguard article URL

### `vanguardng_author`

- **HTTP:** `GET /vanguardng/author`
- **What:** Find recent Vanguard articles by byline. Vanguard publishes no author profile pages, so this returns the recent articles in one public feed (site-wide by default, or one section) credited to a byline, matched on the on-page "By <Name>" line or the site's creator field.
- **Params:** `name` (string, **required**) — Byline to look for (3 to 80 characters), e.g. Chioma Obinna; `section` (string, optional) — Optional section slug to scan instead of the site-wide feed

### `vanguardng_headlines`

- **HTTP:** `GET /vanguardng/headlines`
- **What:** Get Vanguard section headlines. Lists up to 20 recent Vanguard stories from one category. `section` is required and takes one of 42 slugs such as `national-news`, `politics`, `business`, `sports`, `business/energy` or `more/metro`. Items carry title, URL, summary, author and publication time. An unknown section returns an invalid-params error.
- **Params:** `section` (string, **required**) — Vanguard section slug

### `vanguardng_news`

- **HTTP:** `GET /vanguardng/news`
- **What:** Get Vanguard top stories. Returns the latest 20 Vanguard (Nigeria) stories with no parameters. Each has a title, URL, summary, publication time and image where available. `author` is the site's account name, often a desk account such as `Nwafor`; use `vanguardng-article` for the on-page byline.
- **Params:** _none_

### `vanguardng_sections`

- **HTTP:** `GET /vanguardng/sections`
- **What:** Get Vanguard sections. Lists the 42 Vanguard sections accepted by `vanguardng-headlines`. Each has a `slug` (nested categories contain a `/`, as in `business/energy`), a display `name` and a feed `url`. `national-news` is the site's News category and `promoted` is sponsored content. Takes no parameters.
- **Params:** _none_

## Vanity Fair (5)

### `vanityfair_article`

- **HTTP:** `GET /vanityfair/article`
- **What:** Get Vanity Fair article content. Returns public Vanity Fair article metadata and body paragraphs from a canonical article URL. A story Vanity Fair marks as subscriber-only in its own page metadata is reported as a permission error instead of a partial or fabricated body.
- **Params:** `url` (string, **required**) — Canonical Vanity Fair article URL

### `vanityfair_author`

- **HTTP:** `GET /vanityfair/author`
- **What:** Get a Vanity Fair contributor profile. Returns a Vanity Fair contributor profile from their canonical `url` (`www.vanityfair.com/contributor/<slug>`, required). The response has the name, job title when present, biography, headshot, social links and recent articles with title, URL and publication time.
- **Params:** `url` (string, **required**) — Canonical Vanity Fair contributor URL

### `vanityfair_headlines`

- **HTTP:** `GET /vanityfair/headlines`
- **What:** Get Vanity Fair section headlines. Lists the current headlines for one Vanity Fair section. `section` is required and takes `hollywood`, `movies`, `television`, `award-season`, `what-is-cinema`, `culture`, `politics`, `business`, `style`, `beauty`, `fashion` or `royals`. Each item has its title and URL.
- **Params:** `section` (string, **required**) — Vanity Fair section slug

### `vanityfair_news`

- **HTTP:** `GET /vanityfair/news`
- **What:** Get Vanity Fair top stories. Returns the latest Vanity Fair top stories and takes no parameters. Each item has its title, canonical URL, summary, author, publication time and lead image.
- **Params:** _none_

### `vanityfair_sections`

- **HTTP:** `GET /vanityfair/sections`
- **What:** Get Vanity Fair sections. Returns the Vanity Fair section inventory: Hollywood (plus its Movies, Television, and Award Season sub-verticals), Arts & Culture, Politics, Business, and Style (plus its Beauty, Fashion, and Royals sub-verticals), each linking to its public listing page.
- **Params:** _none_

## Variety (5)

### `variety_article`

- **HTTP:** `GET /variety/article`
- **What:** Get Variety article content. Returns one Variety article by its canonical `variety.com` `url`, in the form `/<year>/<vertical>/<subcategory>/<slug>-<id>/`. The response has the title, description, authors, section, published and updated times, lead image, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Variety article URL

### `variety_author`

- **HTTP:** `GET /variety/author`
- **What:** Get a Variety author profile. Returns a Variety author profile with name, biography, photo, social links and one page of recent articles. Give either `slug` (such as `ellise-shafer`) or an author `url`, which may include a `/page/<n>/` segment; `page` (default 1) overrides it. `has_next_page` shows whether another page exists.
- **Params:** `page` (integer, optional) — 1-based page number; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. ellise-shafer; `url` (string, optional) — Canonical variety.com/author/<slug> URL, optionally with a /page/<n>/ segment; alternative to slug

### `variety_headlines`

- **HTTP:** `GET /variety/headlines`
- **What:** Get Variety section headlines. Lists fresh Variety headlines for one vertical. `section` is required and takes a slug such as `film`, `music`, `tv`, `biz`, `awards`, `gaming`, `global`, `legit` or `vip`; `variety-sections` lists all 24. Each item has its title and URL, plus summary, author, publication time and image when the outlet provides them.
- **Params:** `section` (string, **required**) — Variety vertical slug

### `variety_news`

- **HTTP:** `GET /variety/news`
- **What:** Get Variety top stories. Returns the latest Variety top stories with no parameters. Each item has its title, URL, summary, author, publication time and image. Item URLs can be passed to `variety-article` for the body.
- **Params:** _none_

### `variety_sections`

- **HTTP:** `GET /variety/sections`
- **What:** Get Variety sections. Lists the 24 Variety verticals accepted by `variety-headlines`, such as `film`, `tv`, `music`, `biz`, `awards`, `legit` and `voices`. Each has a `slug`, a display `name` and a `url`. Takes no parameters.
- **Params:** _none_

## VICE (5)

### `vice_article`

- **HTTP:** `GET /vice/article`
- **What:** Get VICE article content. Returns one VICE article by its canonical `url`, in the form `www.vice.com/en/article/<slug>`. The response has the title, description, authors, section, published and updated times, lead image and body `paragraphs`, plus a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical VICE article URL

### `vice_author`

- **HTTP:** `GET /vice/author`
- **What:** Get a VICE contributor profile. Returns a VICE contributor profile from their canonical `url` (`www.vice.com/en/contributor/<slug>`, required). The response has the name and headshot when present, the biography paragraphs and recent articles with title, URL, summary, author, publication time and image.
- **Params:** `url` (string, **required**) — Canonical VICE contributor URL

### `vice_headlines`

- **HTTP:** `GET /vice/headlines`
- **What:** Get VICE section headlines. Returns fresh headlines from one VICE section, either its public RSS feed (News, Life, Tech, Music) or its public listing page for the remaining sections.
- **Params:** `section` (string, **required**) — VICE section slug

### `vice_news`

- **HTTP:** `GET /vice/news`
- **What:** Get VICE top stories. Returns the latest VICE stories with no parameters. Each item has its title and URL, plus summary, author, publication time and lead image when the outlet provides them. Pass an item URL to `vice-article` to read the story.
- **Params:** _none_

### `vice_sections`

- **HTTP:** `GET /vice/sections`
- **What:** Get VICE sections. Returns the VICE section inventory: the site's own 12 curated sections (News, Life, Tech, Music, and others), each linking to its public listing page.
- **Params:** _none_

## Vox (5)

### `vox_article`

- **HTTP:** `GET /vox/article`
- **What:** Get Vox article content. Returns one Vox article by its canonical `url`: title, description, authors, section, published and updated times, lead image and the body `paragraphs`. Only public content is returned; a subscriber-only or blocked article comes back as an upstream error rather than a partial body.
- **Params:** `url` (string, **required**) — Canonical Vox article URL

### `vox_author`

- **HTTP:** `GET /vox/author`
- **What:** Get a Vox author profile. Returns a Vox author profile from their canonical `url` (`www.vox.com/authors/<slug>`, required). The response has the name, `job_title` from the masthead (such as Senior Politics Correspondent), `bio` and recent articles, each with title, URL, excerpt, category and an ISO-8601 `published_at`.
- **Params:** `url` (string, **required**) — Canonical Vox author URL

### `vox_headlines`

- **HTTP:** `GET /vox/headlines`
- **What:** Get Vox section headlines. Lists the current Vox headlines for one section. `section` is required and takes `politics`, `culture`, `policy`, `world`, `money`, `technology`, `science-and-health`, `climate`, `future-perfect` or `explainers`. Each item has its title, URL, summary, author and publication time.
- **Params:** `section` (string, **required**) — Vox section slug

### `vox_news`

- **HTTP:** `GET /vox/news`
- **What:** Get Vox top stories. Returns the latest Vox top stories with no parameters. Each item has its title, URL, summary, author and publication time. Item URLs can be passed to `vox-article` for the body.
- **Params:** _none_

### `vox_sections`

- **HTTP:** `GET /vox/sections`
- **What:** Get Vox sections. Lists the Vox editorial sections accepted by `vox-headlines`, each with a stable `slug`, a display `name` and the section `url`. Use the slugs as the `section` value. Takes no parameters.
- **Params:** _none_

## WalesOnline (5)

### `walesonline_article`

- **HTTP:** `GET /walesonline/article`
- **What:** Get WalesOnline article content. Returns public WalesOnline article metadata (including the section) and body paragraphs from a canonical article URL, including live blogs. Photo-gallery URLs are rejected.
- **Params:** `url` (string, **required**) — Canonical WalesOnline article URL

### `walesonline_author`

- **HTTP:** `GET /walesonline/author`
- **What:** Get a WalesOnline author profile. Returns one WalesOnline author's public profile (name, plus job title, bio, email and X/Twitter handle when the author lists them) and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page number of the author's article list (1 to 100); overrides any pageNumber in url; `slug` (string, optional) — Author slug, e.g. rahaf-ali; `url` (string, optional) — Canonical walesonline.co.uk/authors/<slug>/ URL; alternative to slug

### `walesonline_headlines`

- **HTTP:** `GET /walesonline/headlines`
- **What:** Get WalesOnline section headlines. Lists recent WalesOnline headlines for one section, up to about 25 items. `section` is required and takes a slug such as `news/wales-news`, `news/politics`, `sport/rugby`, `sport/football` or `whats-on`; `walesonline-sections` lists all 37. Photo galleries are omitted, and an invalid value returns a 400 error.
- **Params:** `section` (string, **required**) — WalesOnline section slug

### `walesonline_news`

- **HTTP:** `GET /walesonline/news`
- **What:** Get WalesOnline top stories. Returns fresh WalesOnline top stories from the public home RSS feed. Photo galleries are omitted because they have no readable article body.
- **Params:** _none_

### `walesonline_sections`

- **HTTP:** `GET /walesonline/sections`
- **What:** Get WalesOnline sections. Lists the 37 WalesOnline sections accepted by `walesonline-headlines`, with nested slugs such as `news/wales-news`, `sport/rugby` and `whats-on/food-drink-news`. Each has a `slug`, a display `name` and a feed `url`. Takes no parameters.
- **Params:** _none_

## WIRED (5)

### `wired_article`

- **HTTP:** `GET /wired/article`
- **What:** Get a WIRED article's content. Returns one public WIRED article's metadata and full body paragraphs from a canonical article URL. WIRED marks some stories subscriber-only in the page's own metadata; those return a 403 permission error rather than a truncated or fabricated body -- see the endpoint markdown for the exact detection method.
- **Params:** `url` (string, **required**) — Canonical WIRED article URL

### `wired_author`

- **HTTP:** `GET /wired/author`
- **What:** Get a WIRED contributor profile. Returns one WIRED contributor's public profile: name, job title, biography, headshot, social links, and their recent articles from a canonical author URL.
- **Params:** `url` (string, **required**) — Canonical WIRED author URL

### `wired_headlines`

- **HTTP:** `GET /wired/headlines`
- **What:** Get the latest stories in a WIRED section. Returns the current public RSS feed for one WIRED section: each story's title, canonical URL, summary, author, publication time, and lead image. Section must be one of the slugs returned by /wired/sections: `business`, `culture`, `gear`, `politics`, `science`, `security`.
- **Params:** `section` (string, **required**) — WIRED section slug from /wired/sections

### `wired_news`

- **HTTP:** `GET /wired/news`
- **What:** Get the latest WIRED stories. Returns WIRED's current top stories with no parameters. Each item has its title, canonical URL, summary, author, publication time and lead image, plus a type label for the item.
- **Params:** _none_

### `wired_sections`

- **HTTP:** `GET /wired/sections`
- **What:** List WIRED sections. Lists every WIRED section accepted by /wired/headlines, with its slug, display name, and landing-page URL. This is the full public, RSS-backed section taxonomy -- see the endpoint markdown for the one primary-nav link (Big Story) that is excluded and why.
- **Params:** _none_

## Wall Street Journal (2)

### `wsj_article`

- **HTTP:** `GET /wsj/article`
- **What:** Get a Wall Street Journal article's content. Returns one Wall Street Journal article's title, byline, publication time, word count, and body paragraphs, recovered from a public web-archive snapshot of the article. WSJ serves only the first paragraphs of premium articles at the origin, so an article is returned only when a full-text archive snapshot exists; an article without one returns 404.
- **Params:** `url` (string, **required**) — Canonical WSJ article URL

### `wsj_author`

- **HTTP:** `GET /wsj/author`
- **What:** Get a Wall Street Journal author's profile and recent articles. Returns one Wall Street Journal author's profile (name, job title, bio, and social links when available) and the recent articles listed on their author page, read directly from the live page. The author page sits behind the same access wall as article pages, so a nonexistent author slug returns 404.
- **Params:** `slug` (string, optional) — WSJ author slug; `url` (string, optional) — Canonical https://www.wsj.com/news/author/<slug> URL, as an alternative to slug

## XDA (5)

### `xda_article`

- **HTTP:** `GET /xda/article`
- **What:** Get XDA article content. Returns one XDA article by its `url`, which must be a `www.xda-developers.com/<slug>/` link; section hubs, author pages and the bare `xda-developers.com` host are rejected. The response has the title, description, times, section, authors, lead image and body `paragraphs`. `paywalled` is set to `true` only if the page declares the article not free.
- **Params:** `url` (string, **required**) — Canonical XDA article URL

### `xda_author`

- **HTTP:** `GET /xda/author`
- **What:** Get an XDA author profile. Returns an XDA author profile from their `https://www.xda-developers.com/author/<slug>/` `url` (required; paginated author URLs are rejected). The response has the name, title, biography, image, social links and the profile's latest articles, about 20, with no older pages.
- **Params:** `url` (string, **required**) — Canonical XDA author URL

### `xda_headlines`

- **HTTP:** `GET /xda/headlines`
- **What:** Get XDA section headlines. Lists 10 recent XDA items for one section. `section` is required and takes a slug such as `news`, `reviews`, `buying-guides`, `gpu`, `laptops`, `windows`, `linux-hub` or `ai-tools`; `xda-sections` lists them all. Dormant sections such as `editorials` or `beats` return old items. Other values are rejected.
- **Params:** `section` (string, **required**) — XDA RSS section slug

### `xda_news`

- **HTTP:** `GET /xda/news`
- **What:** Get XDA top stories. Returns about 10 of the latest XDA top stories with no parameters. Each item has its title, canonical URL, summary, publication time, author names (co-authors joined with a comma) and lead image.
- **Params:** _none_

### `xda_sections`

- **HTTP:** `GET /xda/sections`
- **What:** Get XDA RSS sections. Lists the XDA sections accepted by `xda-headlines`, including `news`, `reviews`, `buying-guides`, `gpu`, `laptops`, `gaming-handhelds`, `windows`, `linux-hub` and `ai-tools`. Each has a `slug`, a display `name` and a feed `url`. Takes no parameters.
- **Params:** _none_

## ZDNet (5)

### `zdnet_article`

- **HTTP:** `GET /zdnet/article`
- **What:** Get ZDNet article or review content. Returns one ZDNet article, review or how-to by its canonical `zdnet.com` `url`. The response has the title, description, published and updated times, section labels, authors, lead image and body `paragraphs`. Video, topic and author pages are not supported and return an error instead of an empty article.
- **Params:** `url` (string, **required**) — Canonical ZDNet article URL

### `zdnet_author`

- **HTTP:** `GET /zdnet/author`
- **What:** Get a ZDNet author profile. Returns one ZDNet author's public profile: name, role, biography, education, areas of expertise, join date, article count, and one page of their recent articles.
- **Params:** `page` (integer, optional) — 1-based page number of the author's article list; overrides any page number in url; `slug` (string, optional) — Author slug, e.g. abeaty; `url` (string, optional) — Canonical zdnet.com/meet-the-team/<slug> URL; alternative to slug

### `zdnet_headlines`

- **HTTP:** `GET /zdnet/headlines`
- **What:** Get ZDNet section headlines. Lists fresh ZDNet headlines for one topic or content type. `section` is required and takes a slug such as `artificial-intelligence`, `security`, `smartphones`, `vpn`, `how-to` or `news`; `zdnet-sections` lists all of them. Video pages are dropped, and an invalid value returns a 400 error.
- **Params:** `section` (string, **required**) — ZDNet topic or content-type slug

### `zdnet_news`

- **HTTP:** `GET /zdnet/news`
- **What:** Get ZDNet top stories. Returns the latest ZDNet top stories with no parameters. Each item has its title, canonical URL, summary, publication time and author name when available. Video pages are not included.
- **Params:** _none_

### `zdnet_sections`

- **HTTP:** `GET /zdnet/sections`
- **What:** Get ZDNet sections. Lists the ZDNet topic and content-type sections accepted by `zdnet-headlines`, such as `artificial-intelligence`, `security`, `smartphones`, `vpn`, `how-to` and `deals`. Each has a `slug`, a display `name` and a feed `url`. Takes no parameters.
- **Params:** _none_

## Android Police (5)

### `androidpolice_article`

- **HTTP:** `GET /androidpolice/article`
- **What:** Get Android Police article content. Returns an Android Police article by `url`, a canonical address with a flat, single-slug path. The response has the title, authors, section, description, publication and update times, image and the readable body `paragraphs`.
- **Params:** `url` (string, **required**) — Canonical Android Police article URL

### `androidpolice_author`

- **HTTP:** `GET /androidpolice/author`
- **What:** Get an Android Police author profile. Returns a public author's byline metadata, biography, social links, and recent articles from a canonical author URL. Only the first page is covered.
- **Params:** `url` (string, **required**) — Canonical Android Police author URL

### `androidpolice_headlines`

- **HTTP:** `GET /androidpolice/headlines`
- **What:** Get Android Police section headlines. Returns recent Android Police headlines for one of 18 sections. `section` is required and takes a slug such as `news`, `phones`, `smart-home`, `ai-machine-learning` or `deals`. Each item has a title and URL, and may also carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Android Police section slug

### `androidpolice_news`

- **HTTP:** `GET /androidpolice/news`
- **What:** Get Android Police top stories. Returns the current Android Police top stories across the site, with no input needed. Each item has a title and URL, and may also carry the author, publication time, summary and image.
- **Params:** _none_

### `androidpolice_sections`

- **HTTP:** `GET /androidpolice/sections`
- **What:** Get Android Police sections. Lists the 18 feed-backed sections in Android Police's primary navigation, from `news`, `phones` and `tablets` to `deals`, `videos` and `awards`. Each entry has a `slug`, a display `name` and the feed `url`, and the slugs are accepted by `androidpolice-headlines`.
- **Params:** _none_

## Benzinga (5)

### `benzinga_article`

- **HTTP:** `GET /benzinga/article`
- **What:** Get a Benzinga article. Returns a Benzinga article by `url`, a canonical dated editorial article URL: title, description, publication and update times, section, authors, image and the body `paragraphs`. Paid products, profiles, press releases, SEC pages and partner content are not accepted.
- **Params:** `url` (string, **required**) — Canonical dated Benzinga editorial article URL

### `benzinga_headlines`

- **HTTP:** `GET /benzinga/headlines`
- **What:** Get Benzinga section headlines. Returns current Benzinga story cards for one section. `section` is required and is `latest`, `technology-stocks`, `politics` or `health-care`. Each item has a title and URL, and may also carry a summary, author, publication time and image.
- **Params:** `section` (string, **required**) — Benzinga editorial section slug

### `benzinga_news`

- **HTTP:** `GET /benzinga/news`
- **What:** Get Benzinga top stories. Returns the current Benzinga stories, with no input needed. Each item has a title, URL and a `summary` that is the publisher's short teaser rather than article text, and may also carry the author, publication time and image.
- **Params:** _none_

### `benzinga_search`

- **HTTP:** `GET /benzinga/search`
- **What:** Search Benzinga article suggestions. Returns up to five public news-article suggestions from Benzinga's anonymous search typeahead. Ticker-only suggestions are omitted; this is not a paginated archive search.
- **Params:** `q` (string, **required**) — Search text (2 to 100 characters)

### `benzinga_sections`

- **HTTP:** `GET /benzinga/sections`
- **What:** List Benzinga news sections. Lists the four Benzinga editorial sections accepted by `benzinga-headlines`: `latest` (named Breaking News), `technology-stocks`, `politics` and `health-care`. Each has a `slug`, a display `name` and the section's page `url`.
- **Params:** _none_

## Brisbane Times (5)

### `brisbanetimes_article`

- **HTTP:** `GET /brisbanetimes/article`
- **What:** Get Brisbane Times article content. Returns one Brisbane Times article's metadata and the exact body paragraphs served by one anonymous page request, with the publisher's is_accessible_for_free, paywalled, and is_truncated flags. No paywall is bypassed or hidden content fetched.
- **Params:** `url` (string, **required**) — Canonical Brisbane Times article URL

### `brisbanetimes_author`

- **HTTP:** `GET /brisbanetimes/author`
- **What:** Get a Brisbane Times journalist profile. Returns a Brisbane Times journalist profile from `url`, a canonical `https://www.brisbanetimes.com.au/by/<name>-<id>` address: name, biography, headshot, email, social links and recent story cards with title, URL, summary and image. Fields appear only when the profile shows them; the sampled profile returned 10 stories.
- **Params:** `url` (string, **required**) — Canonical Brisbane Times journalist URL

### `brisbanetimes_headlines`

- **HTTP:** `GET /brisbanetimes/headlines`
- **What:** Get Brisbane Times section or topic headlines. Returns current story cards from one observed Brisbane Times server-rendered section or populated topic page. `section` must be one of the exact slugs from `/brisbanetimes/sections`; unsupported and unresolved linkless paths are rejected before an upstream request. Off-brand story links on Traveller are omitted.
- **Params:** `section` (string, **required**) — Section or topic slug from /brisbanetimes/sections

### `brisbanetimes_news`

- **HTTP:** `GET /brisbanetimes/news`
- **What:** Get Brisbane Times top stories. Returns Brisbane Times's current public Latest News RSS feed: story title, canonical URL, summary, author, publication time, and lead image.
- **Params:** _none_

### `brisbanetimes_sections`

- **HTTP:** `GET /brisbanetimes/sections`
- **What:** Get Brisbane Times editorial sections. Lists the 104 accepted Brisbane Times editorial surfaces (95 article-bearing section pages and nine populated topic hubs), each with its exact path slug, menu label, and requested Brisbane Times URL. Three linkless surfaces with no explicit empty-state marker are excluded.
- **Params:** _none_

## The Denver Post (5)

### `denverpost_article`

- **HTTP:** `GET /denverpost/article`
- **What:** Get a Denver Post article. Returns article metadata and paragraphs present on the public page. Subscriber-only pages may expose only an anonymous preview; this service does not bypass access controls.
- **Params:** `url` (string, **required**) — Canonical Denver Post article URL

### `denverpost_author`

- **HTTP:** `GET /denverpost/author`
- **What:** Get a Denver Post author archive. Returns a Denver Post author's profile and the articles on the first page of their archive. Give exactly one of `slug` (for example `aldo-svaldi`) or `url` (a denverpost.com/author/<slug>/ link). The profile has name, job title, bio, email and Twitter handle where the page shows them; each article has a title, URL, summary and publication time.
- **Params:** `slug` (string, optional) — Author slug, e.g. aldo-svaldi; `url` (string, optional) — Canonical denverpost.com/author/<slug>/ URL; alternative to slug

### `denverpost_headlines`

- **HTTP:** `GET /denverpost/headlines`
- **What:** Get Denver Post section headlines. Returns current headlines for one Denver Post section or topic archive. `section` is required and must be a slug from the sections endpoint, such as `business`, `denver-broncos`, `colorado` or `weather`; an invalid value returns an invalid-params error. Items carry title and URL, plus summary, author, publication time and image when the card shows them. Cards without a dated Denver Post article URL are skipped.
- **Params:** `section` (string, **required**) — Section or topic slug returned by denverpost-sections

### `denverpost_news`

- **HTTP:** `GET /denverpost/news`
- **What:** Get Denver Post top stories. Returns the article cards on the Denver Post homepage, about 91 when last checked, though the count varies as the site updates. Each item has a title and URL and can carry a summary, author, publication time, image and `type`. It takes no parameters.
- **Params:** _none_

### `denverpost_sections`

- **HTTP:** `GET /denverpost/sections`
- **What:** Get Denver Post section and topic inventory. Lists the Denver Post slugs that the headlines endpoint accepts: 56 editorial sections and 19 topic archives, checked on 2026-09-30. Examples are `colorado`, `denver-broncos`, `economy` and `hiking`. Each entry has a `slug`, `name` and `url`. Branded content and cartoons are left out.
- **Params:** _none_

## The Express Tribune (5)

### `expresstribune_article`

- **HTTP:** `GET /expresstribune/article`
- **What:** Get The Express Tribune article content. Returns one Express Tribune story by `url`, which must be a canonical `tribune.com.pk/story/<id>/<slug>` link. The response has the title, description, section, authors, publication and update times, lead image URL, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Express Tribune story URL

### `expresstribune_author`

- **HTTP:** `GET /expresstribune/author`
- **What:** Get an Express Tribune author's public archive. Returns one page of story cards from a canonical public author archive. Page is 1-based; the publisher's Next link indicates another page.
- **Params:** `page` (integer, optional) — 1-based page number; `url` (string, **required**) — Canonical author archive URL

### `expresstribune_headlines`

- **HTTP:** `GET /expresstribune/headlines`
- **What:** Get The Express Tribune section headlines. Returns headlines from one public RSS section. Some directory feeds are historical or infrequently updated; their publisher timestamps are preserved.
- **Params:** `section` (string, **required**) — The Express Tribune section slug

### `expresstribune_news`

- **HTTP:** `GET /expresstribune/news`
- **What:** Get The Express Tribune top stories. Returns current top stories from The Express Tribune's public RSS feed. Feed dates and publisher teasers are returned as published.
- **Params:** _none_

### `expresstribune_sections`

- **HTTP:** `GET /expresstribune/sections`
- **What:** Get The Express Tribune sections. Returns every usable feed section listed in the publisher's RSS directory. talko is omitted because its official endpoint currently returns an empty response.
- **Params:** _none_

## Houston Chronicle (5)

### `houston_chronicle_article`

- **HTTP:** `GET /houston-chronicle/article`
- **What:** Get Houston Chronicle article content. Returns public Houston Chronicle article metadata and the body available in the anonymous response. Premium stories are flagged from the publisher's content-tier and JSON-LD markers; the service does not authenticate or bypass access controls.
- **Params:** `url` (string, **required**) — Canonical Houston Chronicle article URL

### `houston_chronicle_author`

- **HTTP:** `GET /houston-chronicle/author`
- **What:** Get a Houston Chronicle author profile. Returns a Houston Chronicle author profile by `url`, a canonical `houstonchronicle.com/author/<slug>/` link. The response has the `name`, `job_title`, `biography`, `image_url`, social profile links in `same_as`, and recent article cards with title, URL and summary.
- **Params:** `url` (string, **required**) — Canonical Houston Chronicle author URL

### `houston_chronicle_headlines`

- **HTTP:** `GET /houston-chronicle/headlines`
- **What:** Get Houston Chronicle section headlines. Returns current public headlines from a verified Houston Chronicle editorial section. Pages that return Hearst's Client Challenge are retried through configured rendering backends; the service does not solve or bypass access controls.
- **Params:** `section` (string, **required**) — Houston Chronicle public section slug

### `houston_chronicle_news`

- **HTTP:** `GET /houston-chronicle/news`
- **What:** Get Houston Chronicle top stories. Returns current public Houston Chronicle homepage stories. Publisher premium markers are preserved on article responses.
- **Params:** _none_

### `houston_chronicle_sections`

- **HTTP:** `GET /houston-chronicle/sections`
- **What:** Get Houston Chronicle sections. Returns every live-verified public editorial section accepted by the Houston Chronicle headlines endpoint. Newsletter, games, audio-only, external marketplace and interactive project/tool links are excluded.
- **Params:** _none_

## The Japan Times (5)

### `japantimes_article`

- **HTTP:** `GET /japantimes/article`
- **What:** Get a The Japan Times article. Returns public article metadata. If the page marks its body as blurred for anonymous visitors, paywalled is true and hidden subscriber text is omitted.
- **Params:** `url` (string, **required**) — Canonical HTTPS The Japan Times article URL

### `japantimes_author`

- **HTTP:** `GET /japantimes/author`
- **What:** Get a The Japan Times author profile. Returns a The Japan Times author's name and the article cards linked from their profile page. `url` is required and must be a canonical HTTPS profile link in the form `/author/<numeric-id>/<slug>/`. Each article has a title, URL, summary, author, image, `type` and publication time. Paginated `/page/<n>/` URLs are not followed.
- **Params:** `url` (string, **required**) — Canonical HTTPS /author/<numeric-id>/<slug>/ profile URL

### `japantimes_headlines`

- **HTTP:** `GET /japantimes/headlines`
- **What:** Get The Japan Times section headlines. Returns public article cards from one canonical section page. This site's section pages are HTML; only the top stories surface has a verified RSS feed.
- **Params:** `section` (string, **required**) — Canonical section slug from japantimes-sections

### `japantimes_news`

- **HTTP:** `GET /japantimes/news`
- **What:** Get The Japan Times top stories. Returns the current top stories from The Japan Times. It takes no parameters. Each item has its title, URL, publication time and a short publisher-written teaser in `summary`, not the article text, plus the author and image when the outlet provides them.
- **Params:** _none_

### `japantimes_sections`

- **HTTP:** `GET /japantimes/sections`
- **What:** Get The Japan Times sections. Lists the 60 sections linked from The Japan Times main navigation, which the headlines endpoint accepts, for example `news-japan`, `business-markets`, `sports-sumo`, `culture-film` and `community-voices`. Each entry has a `slug`, a display `name` and a section `url`.
- **Params:** _none_

## MakeUseOf (5)

### `makeuseof_article`

- **HTTP:** `GET /makeuseof/article`
- **What:** Get MakeUseOf article content. Returns a MakeUseOf article by `url`, a canonical HTTPS article link. The response has the title, description, section, authors, lead image, publish and update times, the article body as `paragraphs`, and a `paywalled` flag. Section, author, tag, utility and video pages are not article URLs.
- **Params:** `url` (string, **required**) — Canonical MakeUseOf article URL

### `makeuseof_author`

- **HTTP:** `GET /makeuseof/author`
- **What:** Get a MakeUseOf author profile. Returns an author's public byline metadata, biography, social links, and recent stories from a canonical author URL. Only the first page is covered.
- **Params:** `url` (string, **required**) — Canonical MakeUseOf author URL

### `makeuseof_headlines`

- **HTTP:** `GET /makeuseof/headlines`
- **What:** Get MakeUseOf section headlines. Returns current MakeUseOf headlines for one category. `section` is required and takes one of 14 slugs such as `windows`, `linux`, `google-android`, `security`, `smart-home` or `news`; tag archives are not accepted. Each item has its title, URL, summary, author, publication time and image.
- **Params:** `section` (string, **required**) — MakeUseOf section slug

### `makeuseof_news`

- **HTTP:** `GET /makeuseof/news`
- **What:** Get MakeUseOf top stories. Returns MakeUseOf's current top stories, with no parameters. Each item has its title, canonical article URL, short summary, publication time, and author and image when available.
- **Params:** _none_

### `makeuseof_sections`

- **HTTP:** `GET /makeuseof/sections`
- **What:** Get MakeUseOf RSS sections. Lists the 14 MakeUseOf sections accepted by `makeuseof-headlines`, including `windows`, `linux`, `apple`, `networking`, `productivity`, `streaming` and `news`. Each entry has a `slug`, display `name` and `url`. Open-ended tag archives are not sections.
- **Params:** _none_

## The National (5)

### `national_article`

- **HTTP:** `GET /national/article`
- **What:** Get The National article content. Returns article metadata and the body served to an anonymous visitor for one canonical The National story URL. The endpoint does not bypass subscriber or access gates and reports paywalled when the page marks content as restricted.
- **Params:** `url` (string, **required**) — Canonical thenationalnews.com article URL

### `national_author`

- **HTTP:** `GET /national/author`
- **What:** Get a The National author profile. Returns one public author topic page, its name, optional author image and the latest article cards listed on that page.
- **Params:** `slug` (string, optional) — The National author slug, e.g. cody-combs; `url` (string, optional) — Canonical thenationalnews.com/topics/Author/<slug> URL; alternative to slug

### `national_headlines`

- **HTTP:** `GET /national/headlines`
- **What:** Get The National section headlines. Returns current The National stories for a category. Pass one of the editorial section slugs from national_sections. A valid category with no current stories returns an empty items list.
- **Params:** `section` (string, **required**) — The National editorial section slug

### `national_news`

- **HTTP:** `GET /national/news`
- **What:** Get The National top stories. Returns current The National UAE stories.
- **Params:** _none_

### `national_sections`

- **HTTP:** `GET /national/sections`
- **What:** Get The National sections. Returns all 57 editorial categories in The National's section taxonomy that are accepted by national_headlines. Podcast, newsletter, puzzle, partner and promotional surfaces are excluded.
- **Params:** _none_

## 9to5Google (5)

### `ninetofivegoogle_article`

- **HTTP:** `GET /ninetofivegoogle/article`
- **What:** Get a 9to5Google article. Returns public 9to5Google article metadata and readable body paragraphs from a canonical dated article URL. Audio-first podcast archive slugs are excluded from the sections list; podcast episodes that appear in the main feed can still be read when their page exposes metadata and paragraphs.
- **Params:** `url` (string, **required**) — Canonical 9to5Google article URL

### `ninetofivegoogle_author`

- **HTTP:** `GET /ninetofivegoogle/author`
- **What:** Get a 9to5Google author profile. Returns a 9to5Google author profile from `url`, a canonical `https://9to5google.com/author/<slug>/` address. The response has the author's `name`, avatar, `biography`, `social_links` and the first page of recent articles, each with title, URL, summary and image. Social-link types and dates are as the author's page shows them.
- **Params:** `url` (string, **required**) — Canonical 9to5Google author URL

### `ninetofivegoogle_headlines`

- **HTTP:** `GET /ninetofivegoogle/headlines`
- **What:** Get 9to5Google section headlines. Returns recent 9to5Google headlines for one guide or editorial archive. `section` is required and takes a slug such as `gemini`, `google-pixel-9` or `wear-os`; an unknown or missing value returns an invalid-params error. There are 58 guide feeds and five editorial archives, and some hold fewer than 100 entries.
- **Params:** `section` (string, **required**) — Slug returned by ninetofivegoogle_sections

### `ninetofivegoogle_news`

- **HTTP:** `GET /ninetofivegoogle/news`
- **What:** Get 9to5Google top stories. Returns recent 9to5Google stories with no input needed. Each item has a title, canonical URL, summary, publication time and author. Cross-network links are filtered out, so returned items use canonical 9to5Google story URLs.
- **Params:** _none_

### `ninetofivegoogle_sections`

- **HTTP:** `GET /ninetofivegoogle/sections`
- **What:** Discover 9to5Google sections. Returns the 58 topic guides linked by the current first-party Guides directory and five separately navigable editorial feeds. Use each slug with the headlines endpoint.
- **Params:** _none_

## TheBlaze (5)

### `theblaze_article`

- **HTTP:** `GET /theblaze/article`
- **What:** Get a Blaze Media article. Returns one TheBlaze (Blaze Media) article by `url`, a canonical HTTPS editorial or show-story link on `theblaze.com`; non-editorial paths and off-site URLs are rejected. The response has the title, description, section, authors, publication and update times, image URL, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical theblaze.com article URL

### `theblaze_author`

- **HTTP:** `GET /theblaze/author`
- **What:** Get a Blaze Media contributor profile. Returns a public /u/<slug> profile and up to 30 recent article feed items. Provide exactly one of slug or canonical profile URL.
- **Params:** `slug` (string, optional) — TheBlaze author username; `url` (string, optional) — Canonical HTTPS theblaze.com/u/<slug> profile URL

### `theblaze_headlines`

- **HTTP:** `GET /theblaze/headlines`
- **What:** Get Blaze Media section headlines. Returns up to 30 recent stories from one TheBlaze (Blaze Media) section. `section` is required, case-sensitive and must match exactly, for example `news`, `columns/opinion`, `lifestyle/men`, `tech` or a show such as `shows/relatable`. Other values are rejected. Items have a title and URL, plus summary, author, publication time and image when the outlet provides them.
- **Params:** `section` (string, **required**) — Exact Blaze Media section slug

### `theblaze_news`

- **HTTP:** `GET /theblaze/news`
- **What:** Get Blaze Media top stories. Returns the latest site-wide stories from TheBlaze (Blaze Media), up to 30 items, covering news and opinion. Each item has a headline, canonical URL, publication time, byline, summary and image URL when published. It takes no parameters.
- **Params:** _none_

### `theblaze_sections`

- **HTTP:** `GET /theblaze/sections`
- **What:** List Blaze Media sections. Returns all verified article-bearing editorial and show sections accepted by the headlines endpoint. The contributors collection is included; the off-site Profile feed is excluded.
- **Params:** _none_

## The Next Web (5)

### `thenextweb_article`

- **HTTP:** `GET /thenextweb/article`
- **What:** Get The Next Web article content. Returns one The Next Web article by `url`, which must be a canonical HTTPS `thenextweb.com/news/<slug>` link; off-site URLs and non-article paths are rejected. The response has the title, description, section, authors, publication and update times, image URL, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical thenextweb.com article URL

### `thenextweb_author`

- **HTTP:** `GET /thenextweb/author`
- **What:** Get a The Next Web author profile. Returns a The Next Web author's name, image URL and the story cards on their archive page. Give `slug` or a canonical `thenextweb.com/author/<slug>` `url`; `slug` is required when `url` is omitted. Each article has a title, URL, summary, author, image, `type` and publication time.
- **Params:** `slug` (string, optional) — Author slug from the public author sitemap or an article byline; `url` (string, optional) — Canonical thenextweb.com/author/<slug> URL; alternative to slug

### `thenextweb_headlines`

- **HTTP:** `GET /thenextweb/headlines`
- **What:** Get The Next Web section headlines. Returns the story cards of one The Next Web editorial section. `section` is required and must be one of `deep-tech`, `sustainability`, `ecosystems`, `data-security`, `fintech-ecommerce`, `future-of-work`, `startups-technology`, `investors-funding`, `government-policy` or `corporates-innovation`; other values return a 400.
- **Params:** `section` (string, **required**) — Editorial section slug returned by thenextweb_sections

### `thenextweb_news`

- **HTTP:** `GET /thenextweb/news`
- **What:** Get The Next Web top stories. Returns the current top stories from The Next Web. It takes no parameters. Each item has the publisher's title, canonical URL, summary, publication time and author, plus the image URL when one is present.
- **Params:** _none_

### `thenextweb_sections`

- **HTTP:** `GET /thenextweb/sections`
- **What:** Get The Next Web sections. Returns the ten editorial sections in The Next Web's current homepage navigation. Topic/tag archives, media, events and promotional categories are excluded.
- **Params:** _none_

## Wccftech (5)

### `wccftech_article`

- **HTTP:** `GET /wccftech/article`
- **What:** Get a Wccftech article. Returns one Wccftech article by its canonical `url` on `wccftech.com` or `www.wccftech.com`, covering news, reviews, how-tos, roundups and best-of pages. The response has the title, description, authors, section, times, lead image and body `paragraphs` where the site serves them, plus a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Wccftech article URL

### `wccftech_author`

- **HTTP:** `GET /wccftech/author`
- **What:** Get a Wccftech author profile. Returns a Wccftech author profile with name, role, bio, photo and recent article cards (title, URL, summary, image, publication time). Identify the author with `slug` (such as `sarfraz`) or a canonical `/author/<slug>/` `url`; one of the two is required.
- **Params:** `slug` (string, optional) — Wccftech author slug, e.g. sarfraz; `url` (string, optional) — Canonical Wccftech author page URL

### `wccftech_headlines`

- **HTTP:** `GET /wccftech/headlines`
- **What:** Get Wccftech section headlines. Returns current articles from one Wccftech topic, category, or editorial archive. Pass a slug from wccftech-sections, such as topic:hardware, category:news, or archive:videos.
- **Params:** `section` (string, **required**) — Wccftech section slug returned by /wccftech/sections

### `wccftech_news`

- **HTTP:** `GET /wccftech/news`
- **What:** Get current Wccftech news. Returns current top stories from Wccftech's public RSS feed, including title, canonical URL, summary, byline, publication time, and image when available.
- **Params:** _none_

### `wccftech_sections`

- **HTTP:** `GET /wccftech/sections`
- **What:** Discover Wccftech sections. Lists all non-empty public category and topic sections, plus the Reviews, Videos, How To, and Roundups archives. Use a returned slug with wccftech-headlines.
- **Params:** _none_

## Yardbarker (5)

### `yardbarker_article`

- **HTTP:** `GET /yardbarker/article`
- **What:** Get a Yardbarker article. Extracts metadata and the publicly served text paragraphs from a canonical Yardbarker story URL. Quiz, account, player, and non-article URLs are rejected.
- **Params:** `url` (string, **required**) — Canonical Yardbarker story URL

### `yardbarker_author`

- **HTTP:** `GET /yardbarker/author`
- **What:** Get a Yardbarker author profile. Returns a Yardbarker author profile from a canonical author `url` of the form `https://www.yardbarker.com/authors/<slug>/<id>` (required). The response has the name, profile image when provided and linked recent stories. Biography text and pagination are not available.
- **Params:** `url` (string, **required**) — Canonical Yardbarker author URL

### `yardbarker_headlines`

- **HTTP:** `GET /yardbarker/headlines`
- **What:** Get headlines for a Yardbarker section. Lists recent Yardbarker headlines with short summaries for one section. `section` is required and takes a typed slug from `yardbarker-sections`, such as `sport_1`, `team_18`, `school_506` or `topic_16979`. Items have title, URL, summary, author, time and image. Unknown slugs return a 400 error.
- **Params:** `section` (string, **required**) — Section slug returned by /yardbarker/sections

### `yardbarker_news`

- **HTTP:** `GET /yardbarker/news`
- **What:** Get Yardbarker top stories. Returns recent Yardbarker story metadata and short summaries from its public homepage. Use /yardbarker/sections to discover the supported sports, team, school, and topic sections.
- **Params:** _none_

### `yardbarker_sections`

- **HTTP:** `GET /yardbarker/sections`
- **What:** List Yardbarker sections. Lists the 589 Yardbarker sections as a dated snapshot: 88 sports hubs, 278 team pages, 150 school pages and 73 topics. Each has a typed `slug` (such as `sport_1` or `team_18`), a display `name` and a hub `url`. Use the slug as `section` in `yardbarker-headlines`. Takes no parameters.
- **Params:** _none_

## Daily Kos (4)

### `dailykos_article`

- **HTTP:** `GET /dailykos/article`
- **What:** Get a Daily Kos staff article. Returns metadata and text paragraphs from a canonical staff-authored Daily Kos /news/ story. Community stories and photographer-owned images are not included.
- **Params:** `url` (string, **required**) — Canonical Daily Kos staff /news/ article URL

### `dailykos_headlines`

- **HTTP:** `GET /dailykos/headlines`
- **What:** Get Daily Kos category headlines. Returns the current stories for one Daily Kos category. `section` is required and takes one of 24 slugs such as `news/elections`, `news/courts`, `cartoon` or `announcements`; any other value returns a 400. Some categories can be empty, which comes back as an empty `items` list.
- **Params:** `section` (string, **required**) — Daily Kos category slug

### `dailykos_news`

- **HTTP:** `GET /dailykos/news`
- **What:** Get Daily Kos top stories. Returns the current staff-written Daily Kos stories, about 10 items, each with title, URL, summary, publication time and author. Community stories and image URLs are left out because the site licenses them separately. Takes no parameters.
- **Params:** _none_

### `dailykos_sections`

- **HTTP:** `GET /dailykos/sections`
- **What:** List Daily Kos categories. Lists the 24 Daily Kos categories accepted by `dailykos-headlines`, including nested slugs such as `news/elections` and `news/whitehouse`. Each entry has the `slug`, display `name` and category `url`. Dynamic tag archives are not part of this set.
- **Params:** _none_

## Daily Maverick (4)

### `dailymaverick_article`

- **HTTP:** `GET /dailymaverick/article`
- **What:** Get a Daily Maverick article. Extracts the public article metadata and body paragraphs Daily Maverick serves to an anonymous visitor. The paywalled flag is set only when the page exposes the publisher's access-control marker.
- **Params:** `url` (string, **required**) — Canonical Daily Maverick article or opinionista URL

### `dailymaverick_headlines`

- **HTTP:** `GET /dailymaverick/headlines`
- **What:** Get headlines from one Daily Maverick section. Returns up to 21 current story cards for one Daily Maverick category. `section` is required and takes one of 51 slugs such as `maverick-news`, `business-maverick`, `opinionistas`, `politics` or `sport`. Each item has its title, URL and type, plus summary, publication time, author and image when the outlet provides them.
- **Params:** `section` (string, **required**) — Daily Maverick category slug

### `dailymaverick_news`

- **HTTP:** `GET /dailymaverick/news`
- **What:** Get current Daily Maverick stories. Lists recent Daily Maverick articles and opinionista pieces from a rolling set of the newest entries. Each item has its title, URL, `type`, publication time and, when available, summary, author and image. Videos, cartoons and other non-article pages are excluded.
- **Params:** _none_

### `dailymaverick_sections`

- **HTTP:** `GET /dailymaverick/sections`
- **What:** List Daily Maverick sections. Lists the 51 article-bearing Daily Maverick categories accepted by `dailymaverick-headlines`, such as `africa`, `maverick-citizen`, `op-eds` and `sci-tech`. Each entry has the `slug`, `name` and category `url`. Empty, media-only and other non-story categories are omitted; checked 2026-09-28.
- **Params:** _none_

## Malay Mail (4)

### `malaymail_article`

- **HTTP:** `GET /malaymail/article`
- **What:** Get a Malay Mail article. Returns a Malay Mail article by `url`, an absolute canonical link in the dated form `/news/<section>/<year>/<month>/<day>/<slug>/<id>`. The response has the title, description, section, authors, lead image, publish and update times, body `paragraphs` and a `paywalled` flag.
- **Params:** `url` (string, **required**) — Canonical Malay Mail article URL

### `malaymail_headlines`

- **HTTP:** `GET /malaymail/headlines`
- **What:** Get Malay Mail section headlines. Returns current Malay Mail headline cards for one News section. `section` is required and takes one of `malaysia`, `singapore`, `money`, `world`, `life`, `eat-drink`, `showbiz`, `opinion`, `sports`, `tech-gadgets` or `what-you-think`. Each item has its title and URL; no summary, author, time or image is returned.
- **Params:** `section` (string, **required**) — Malay Mail News section slug

### `malaymail_news`

- **HTTP:** `GET /malaymail/news`
- **What:** Get Malay Mail top stories. Returns up to 50 current stories from Malay Mail's public all-stories RSS feed. Summaries are publisher teasers, not full article text. Use the sections, headlines, and article routes for verified public archives and story pages.
- **Params:** _none_

### `malaymail_sections`

- **HTTP:** `GET /malaymail/sections`
- **What:** Get Malay Mail sections. Lists the 11 Malay Mail News sections accepted by `malaymail-headlines`, from `malaysia` and `singapore` to `eat-drink`, `tech-gadgets` and `what-you-think`. Each entry has a `slug`, display `name` and section `url`. Takes no parameters.
- **Params:** _none_

## Phys.org (4)

### `physorg_article`

- **HTTP:** `GET /physorg/article`
- **What:** Get a Phys.org article. Returns public Phys.org article metadata and readable body paragraphs from a canonical dated news URL. The service tries proxied HTTP first and uses the production browser fleet when the article edge challenges HTTP. Billing is 2 credits for an HTTP-profile success and 10 credits when browser rendering is required. No author-profile route was verified.
- **Params:** `url` (string, **required**) — Canonical Phys.org article URL

### `physorg_headlines`

- **HTTP:** `GET /physorg/headlines`
- **What:** Get Phys.org section headlines. Returns current stories from one Phys.org feed. The accepted values are the seven Topics menu feeds plus the Breaking and Editorials feeds. Search and tag feeds are not included.
- **Params:** `section` (string, **required**) — Phys.org RSS feed slug from physorg-sections

### `physorg_news`

- **HTTP:** `GET /physorg/news`
- **What:** Get Phys.org top stories. Returns current stories from Phys.org's public all-stories RSS feed. Summaries are publisher-provided teasers. Use physorg-sections to discover the topic and editorial RSS feeds accepted by physorg-headlines.
- **Params:** _none_

### `physorg_sections`

- **HTTP:** `GET /physorg/sections`
- **What:** List Phys.org RSS sections. Lists the seven topic feeds in Phys.org's Topics menu and its two additional public Breaking and Editorials feeds. Every returned slug is accepted by physorg-headlines. Search and tag feeds are not included.
- **Params:** _none_

## TimesLIVE (4)

### `timeslive_article`

- **HTTP:** `GET /timeslive/article`
- **What:** Get TimesLIVE article content. Returns article metadata and body paragraphs for a canonical TimesLIVE editorial article URL. Some stories may have a publisher access gate; paywalled is set when the page's first-party access flags indicate restricted content.
- **Params:** `url` (string, **required**) — Canonical TimesLIVE article URL

### `timeslive_headlines`

- **HTTP:** `GET /timeslive/headlines`
- **What:** Get TimesLIVE section headlines. Returns current TimesLIVE stories for a section. Pass a slug from timeslive_sections; results are the first 15 items in the live section order.
- **Params:** `section` (string, **required**) — TimesLIVE editorial section slug

### `timeslive_news`

- **HTTP:** `GET /timeslive/news`
- **What:** Get TimesLIVE top stories. Returns current TimesLIVE stories, including section-specific headlines. Article access can vary by story.
- **Params:** _none_

### `timeslive_sections`

- **HTTP:** `GET /timeslive/sections`
- **What:** Get TimesLIVE sections. Returns the complete public editorial navigation set accepted by the TimesLIVE headlines endpoint. External Sunday Times, partner, podcast, account, and link-only surfaces are excluded.
- **Params:** _none_
