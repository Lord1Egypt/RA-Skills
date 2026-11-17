# Scenario Cards

Use these scenario cards to translate natural-language Reddit requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

posts, comments, sub-comments, users, trophies, active communities, subreddits, rules, settings, channels, feeds, search results, typeahead suggestions, and trending searches

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| Post details, batch post details, comments, and sub-comment traversal | `reddit-post-comment-rules.md` | /reddit/ |
| Subreddit info, rules, settings, channels, feeds, highlights, and mute status | `reddit-community-rules.md` | /reddit/ |
| Dynamic search, typeahead, trending searches, home/popular/news/games feeds, and user activity | `reddit-discovery-rules.md` | /reddit/ |

## 1. Inspect posts and discussion threads

- User intent: Retrieve post details and comment trees for one or more Reddit posts.
- Primary entity: post / comment / sub-comment
- Ask for: post ID(s), optional comment context, comment depth, and whether batch retrieval is appropriate.
- Default workflow: Use single or batch post detail depending on count; use post comments for top-level discussion and sub-comment replies only when a comment node exposes more cursor context.
- Reference module: `reddit-post-comment-rules.md`
- Endpoint shortlist:
  - [Fetch Single Reddit Post Details](https://docs.keyapi.ai/en/reddit/fetch_post_details.md) - Get single post details by post ID, optionally including the context of a specific comment
  - [Fetch Reddit Post Details in Batch (Max 5)](https://docs.keyapi.ai/en/reddit/fetch_post_details_batch.md) - Batch get post details by a list of post IDs, supports up to 5 posts per batch, optionally including the context of a specific comment
  - [Fetch Reddit Post Details in Large Batch (Max 30)](https://docs.keyapi.ai/en/reddit/fetch_post_details_batch_large.md) - Batch get post details by a large list of post IDs, supports up to 30 posts per batch, optionally including the context of a specific comment
  - [Fetch Reddit APP Post Comments](https://docs.keyapi.ai/en/reddit/fetch_post_comments.md) - Get comments under a specified post on Reddit APP
  - [Fetch Reddit APP Comment Replies (Sub-comments)](https://docs.keyapi.ai/en/reddit/fetch_comment_replies.md) - Get replies (second-level comments / sub-comments) under a specified comment on Reddit APP When a comment node has a more.cursor field, use this API to fetch the sub-comments of that comment

## 2. Analyze a user profile and activity

- User intent: Understand a Reddit user's profile, posts, comments, trophies, and active communities.
- Primary entity: user
- Ask for: username, activity surfaces, page depth, and whether active subreddit context is needed.
- Default workflow: Fetch profile first, then posts/comments/trophies/active subreddits based on the report sections requested.
- Reference module: `reddit-discovery-rules.md`
- Endpoint shortlist:
  - [Fetch Reddit APP User Profile](https://docs.keyapi.ai/en/reddit/fetch_user_profile.md) - Get detailed profile information for a specified user on Reddit APP
  - [Fetch User Posts](https://docs.keyapi.ai/en/reddit/fetch_user_posts.md) - Get the list of posts published by a specified user
  - [Fetch User Comments](https://docs.keyapi.ai/en/reddit/fetch_user_comments.md) - Get the list of comments posted by a specified user
  - [Fetch User Public Trophies](https://docs.keyapi.ai/en/reddit/fetch_user_trophies.md) - Get the list of public trophies/achievements for a specified Reddit user
  - [Fetch User's Active Subreddits](https://docs.keyapi.ai/en/reddit/fetch_user_active_subreddits.md) - Get the list of most active Reddit communities for a specified user

## 3. Analyze a subreddit community

- User intent: Inspect a subreddit profile, rules, settings, post channels, highlights, and feed content.
- Primary entity: subreddit / community
- Ask for: subreddit name, sections needed, feed depth, and whether mute status matters.
- Default workflow: Use subreddit info for baseline, then rules/style/settings/channels for governance context and feed/highlights for content context.
- Reference module: `reddit-community-rules.md`
- Endpoint shortlist:
  - [Fetch Reddit APP Subreddit Info](https://docs.keyapi.ai/en/reddit/fetch_subreddit_info.md)
  - [Fetch Reddit APP Subreddit Rules and Style Info](https://docs.keyapi.ai/en/reddit/fetch_subreddit_style.md) - Get rules and style information for a specified subreddit on Reddit APP
  - [Fetch Reddit APP Subreddit Settings](https://docs.keyapi.ai/en/reddit/fetch_subreddit_settings.md) - Get settings information for a specified subreddit on Reddit APP, including posting rules, user flair settings, moderation settings, and other configuration
  - [Fetch Reddit APP Subreddit Post Channels](https://docs.keyapi.ai/en/reddit/fetch_subreddit_post_channels.md) - Get post channel information for a specified subreddit on Reddit APP
  - [Fetch Reddit APP Subreddit Feed](https://docs.keyapi.ai/en/reddit/fetch_subreddit_feed.md) - Get the feed content stream for a specified subreddit, showing the post list for that subreddit
  - [Fetch Reddit APP Community Highlights](https://docs.keyapi.ai/en/reddit/fetch_community_highlights.md) - Get featured highlight content for a specified community on Reddit APP, including popular posts and important announcements
  - [Check if Subreddit is Muted](https://docs.keyapi.ai/en/reddit/check_subreddit_muted.md) - Check if a specified Reddit subreddit is muted by the current user

## 4. Discover topics, communities, and trends

- User intent: Search Reddit for posts, communities, comments, media, users, or trending topics.
- Primary entity: search result / trend
- Ask for: keyword, search target type when relevant, result depth, and whether typeahead/trending should seed the search.
- Default workflow: Use dynamic search for explicit search intent; use typeahead for query expansion and trending searches for current topic discovery.
- Reference module: `reddit-discovery-rules.md`
- Endpoint shortlist:
  - [Fetch Reddit APP Dynamic Search Results](https://docs.keyapi.ai/en/reddit/fetch_dynamic_search.md) - Perform dynamic search on Reddit APP, supporting search for posts, communities, comments, media, and users
  - [Fetch Reddit APP Search Typeahead Suggestions](https://docs.keyapi.ai/en/reddit/fetch_search_typeahead.md) - Get search typeahead suggestions from the Reddit APP search box, including recommended subreddits, users, and search terms
  - [Fetch Reddit APP Trending Searches](https://docs.keyapi.ai/en/reddit/fetch_trending_searches.md) - Get current trending search topics and content on Reddit APP, no parameters required

## 5. Monitor feed surfaces

- User intent: Inspect popular, home, news, or games feeds for current Reddit content.
- Primary entity: feed
- Ask for: feed type, page depth, and whether posts should be expanded with details/comments.
- Default workflow: Fetch the target feed first, then enrich selected posts only if the user asks for deeper analysis.
- Reference module: `reddit-discovery-rules.md`
- Endpoint shortlist:
  - [Fetch Reddit APP Popular Feed](https://docs.keyapi.ai/en/reddit/fetch_popular_feed.md) - Get Reddit APP popular/trending recommended content, showing the most popular posts across the site
  - [Fetch Reddit APP Home Feed](https://docs.keyapi.ai/en/reddit/fetch_home_feed.md) - Get Reddit APP home feed recommended content
  - [Fetch Reddit APP News Feed](https://docs.keyapi.ai/en/reddit/fetch_news_feed.md) - Get Reddit APP news feed recommended content, showing the latest news and current events discussions
  - [Fetch Reddit APP Games Feed](https://docs.keyapi.ai/en/reddit/fetch_games_feed.md) - Get Reddit APP gaming-related recommended content, showing popular posts from gaming communities
  - [Fetch Single Reddit Post Details](https://docs.keyapi.ai/en/reddit/fetch_post_details.md) - Get single post details by post ID, optionally including the context of a specific comment

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
