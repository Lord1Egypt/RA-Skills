# Scenario Cards

Use these scenario cards to translate natural-language Instagram requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

users, usernames, user IDs, posts, Reels, Stories, Highlights, followers, following, comments, likes, hashtags, music, explore sections, places, cities, locations, and reposts

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| User discovery, profile detail, related profiles, followers, and following | `instagram-user-rules.md` | /instagram/ |
| Posts, Reels, Stories, Highlights, comments, likes, tagged posts, reposts, and media ID conversion | `instagram-content-rules.md` | /instagram/ |
| General search, hashtags, places, locations, music, Explore sections, and Reels discovery | `instagram-discovery-rules.md` | /instagram/ |

## 1. Find and qualify users

- User intent: Search for users, retrieve profile details, and find related or similar profiles.
- Primary entity: user / profile
- Ask for: username, user ID, or keyword; whether related/similar profiles are needed; and page depth for discovery.
- Default workflow: Search users or general search for discovery, then fetch user info; use related/similar users to expand a shortlist.
- Reference module: `instagram-user-rules.md`
- Endpoint shortlist:
  - [Search users](https://docs.keyapi.ai/en/instagram/search_users.md) - Instagram user search endpoint, returns matching user accounts.
  - [General search](https://docs.keyapi.ai/en/instagram/general_search.md) - Perform a general Instagram search by keyword. Supports paginated retrieval.
  - [Get user info](https://docs.keyapi.ai/en/instagram/fetch_user_info.md) - Get detailed information about an Instagram user. Supports querying by username or user ID.
  - [Get user info by user ID](https://docs.keyapi.ai/en/instagram/user_id_to_username.md) - Get user information by Instagram user ID. Useful for converting a user ID to a username or retrieving detailed user data.
  - [Get related profiles](https://docs.keyapi.ai/en/instagram/fetch_related_profiles.md) - Get a list of users similar to or related to a specified user.
  - [Get similar users](https://docs.keyapi.ai/en/instagram/fetch_similar_users.md) - Get a list of users similar to a specified user, based on Instagram recommendation algorithms.

## 2. Audit a user's content portfolio

- User intent: Collect posts, Reels, Stories, Highlights, tagged posts, or reposts for a user.
- Primary entity: user content
- Ask for: username or user ID, content surfaces, page depth, and whether active Stories or archived Highlights matter.
- Default workflow: Fetch user info first if identity is uncertain, then collect only the requested content surfaces; use highlight list before highlight stories.
- Reference module: `instagram-content-rules.md`
- Endpoint shortlist:
  - [Get user posts](https://docs.keyapi.ai/en/instagram/fetch_user_posts.md) - Get a list of all posts by an Instagram user. Supports paginated retrieval.
  - [Get user reels](https://docs.keyapi.ai/en/instagram/fetch_user_reels.md) - Get a list of Reels (short videos) posted by an Instagram user. Supports paginated retrieval.
  - [Get user stories](https://docs.keyapi.ai/en/instagram/fetch_user_stories.md) - Get an Instagram user's currently active stories (Stories). Stories expire after 24 hours.
  - [Get user highlights](https://docs.keyapi.ai/en/instagram/fetch_user_highlights.md) - Get a list of an Instagram user's highlights (Highlights). Highlights are curated story archives pinned by the user.
  - [Get highlight stories](https://docs.keyapi.ai/en/instagram/fetch_highlight_stories.md) - Get all stories in a specified highlight. Requires obtaining the highlight ID via fetch_user_highlights first.
  - [Get user tagged posts](https://docs.keyapi.ai/en/instagram/fetch_user_tagged_posts.md) - Get a list of posts in which a specified user has been tagged. Supports paginated retrieval.
  - [Get user reposts list](https://docs.keyapi.ai/en/instagram/fetch_user_reposts.md) - Get a list of a user's reposts/shares. Supports pagination.

## 3. Analyze a post or discussion thread

- User intent: Inspect one post, its comments, replies, likes, or convert between shortcode and media ID.
- Primary entity: post / comment / like
- Ask for: post URL, shortcode, media ID, comment ID if replies are requested, and requested comment/like depth.
- Default workflow: Convert IDs only when necessary, fetch post info, then collect comments, replies, or likes according to the user analysis goal.
- Reference module: `instagram-content-rules.md`
- Endpoint shortlist:
  - [Get post info](https://docs.keyapi.ai/en/instagram/fetch_post_info.md) - Get detailed information about an Instagram post. Supports shortcode or post URL.
  - [Convert shortcode to media ID](https://docs.keyapi.ai/en/instagram/shortcode_to_media_id.md) - Convert the shortcode of an Instagram post to a media ID. The shortcode is the unique identifier in the post URL, e.g., DRhvwVLAHAG in instagram.com/p/DRhvwVLAHAG/
  - [Convert media ID to shortcode](https://docs.keyapi.ai/en/instagram/media_id_to_shortcode.md) - Convert the media ID of an Instagram post to a shortcode. The shortcode is used to construct the post URL: instagram.com/p/{shortcode}/
  - [Get post comments](https://docs.keyapi.ai/en/instagram/fetch_post_comments.md) - Get a list of comments on a post. Supports both top-level comments and nested replies. Supports paginated retrieval.
  - [Get comment replies](https://docs.keyapi.ai/en/instagram/fetch_comment_replies.md) - Get a list of replies to a comment. Requires obtaining the comment ID via fetch_post_comments first. Supports paginated retrieval.
  - [Get post likes](https://docs.keyapi.ai/en/instagram/fetch_post_likes.md) - Get a list of users who liked a post. Supports paginated retrieval.

## 4. Explore hashtags, locations, and Explore sections

- User intent: Find topical or place-based content and browse Instagram discovery surfaces.
- Primary entity: hashtag / place / section
- Ask for: hashtag, place keyword, coordinates, country/city, section ID, and page depth.
- Default workflow: Resolve the target surface first, then fetch posts by hashtag, place, or section; use country/city and coordinate search for location-specific workflows.
- Reference module: `instagram-discovery-rules.md`
- Endpoint shortlist:
  - [Search hashtags](https://docs.keyapi.ai/en/instagram/search_hashtags.md) - Instagram hashtag search endpoint, returns matching hashtag results.
  - [Get posts by hashtag](https://docs.keyapi.ai/en/instagram/fetch_hashtag_posts.md) - Get a list of posts under a specified hashtag.
  - [Get explore page sections](https://docs.keyapi.ai/en/instagram/fetch_explore_sections.md) - Get the categorized sections available on the Instagram explore page.
  - [Get posts by section](https://docs.keyapi.ai/en/instagram/fetch_section_posts.md) - Get a list of posts under a specific section on the explore page.
  - [Search places](https://docs.keyapi.ai/en/instagram/search_places.md) - Instagram places search endpoint, returns matching location results.
  - [Search locations by coordinates](https://docs.keyapi.ai/en/instagram/search_by_coordinates.md) - Search nearby Instagram locations using GPS coordinates.
  - [Get cities by country](https://docs.keyapi.ai/en/instagram/fetch_cities.md) - Get a list of cities/regions for a specified country.

## 5. Research Reels and music trends

- User intent: Search Reels or music, then inspect posts using a specific audio track.
- Primary entity: Reel / music
- Ask for: keyword, music/audio identifier if known, page depth, and whether user/profile enrichment is needed.
- Default workflow: Use Reels search for video discovery, music search for audio discovery, and posts-using-music to inspect adoption examples.
- Reference module: `instagram-discovery-rules.md`
- Endpoint shortlist:
  - [Search reels](https://docs.keyapi.ai/en/instagram/search_reels.md) - Search Instagram Reels (short videos) by keyword. Supports paginated retrieval.
  - [Search music](https://docs.keyapi.ai/en/instagram/search_music.md) - Search for music available on Instagram by keyword.
  - [Get posts using specific music](https://docs.keyapi.ai/en/instagram/fetch_music_posts.md) - Get a list of posts/Reels that use a specified song or audio track.
  - [Get post info](https://docs.keyapi.ai/en/instagram/fetch_post_info.md) - Get detailed information about an Instagram post. Supports shortcode or post URL.

## 6. Map social graph context

- User intent: Collect followers or following for a user to understand audience or relationship context.
- Primary entity: followers / following
- Ask for: username or user ID, direction, page depth, and whether discovered users need profile enrichment.
- Default workflow: Fetch user info first, then followers or following; enrich only a small shortlist unless the user approves a broader crawl.
- Reference module: `instagram-user-rules.md`
- Endpoint shortlist:
  - [Get user info](https://docs.keyapi.ai/en/instagram/fetch_user_info.md) - Get detailed information about an Instagram user. Supports querying by username or user ID.
  - [Get user followers](https://docs.keyapi.ai/en/instagram/fetch_user_followers.md) - Get a list of an Instagram user's followers. Supports paginated retrieval.
  - [Get user following](https://docs.keyapi.ai/en/instagram/fetch_user_following.md) - Get a list of users that an Instagram user is following. Supports paginated retrieval.

## Docs Search Strategy

1. Map the user's natural-language request to the closest scenario and API concept, then search `llms.txt` for the platform slug plus that semantic entity/action. Do not rely on literal keyword matching when the user wording is vague, translated, or business-oriented.
2. Prefer the narrowest endpoint whose title and description match the requested workflow.
3. Resolve the selected endpoint page before any live call; never infer method or path from this file.
4. Compose multiple endpoints only when the user asks for a report, comparison, enrichment, or explanation that one endpoint cannot answer.
5. API calls are live by default. Repeating the same parameters calls the API again. Large payloads may return a stdout preview; when complete fields are needed for analysis, rerun the same documented request with `--output-file <temp-or-workspace-.tmp-keyapi-file>.json` and read the API payload from `data.data`. Use a user-facing output path only when the user asks to save or export results.

## User Input Compression

Compress parameter-heavy tasks into:

- Goal: search, detail, enrichment, ranking, comparison, monitoring, or report
- Entity: the object being searched, analyzed, compared, ranked, or monitored
- Scope: market, country, language, category, keyword, identifier, date window, and page depth
- Sort or metric: freshness, relevance, growth, engagement, rating, sales, price, audience, or other documented metric
- Pagination depth: one page, top N, until enough evidence, or all available within the user's approved scope
- Output format: concise answer, table, raw JSON, or structured report
