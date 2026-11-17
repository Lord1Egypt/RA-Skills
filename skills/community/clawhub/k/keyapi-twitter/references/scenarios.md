# Scenario Cards

Use these scenario cards to translate natural-language Twitter/X requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

tweets, threads, replies, retweets, profiles, timelines, media, followers, following, communities, lists, trends, jobs, Spaces, affiliates, and live status

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| Tweet detail, thread, replies, retweets, search, trends, and media/content analysis | `twitter-content-rules.md` | /twitter/ |
| Profile detail, timelines, media, followers, following, affiliates, and follow checks | `twitter-profile-social-rules.md` | /twitter/ |
| Communities, lists, jobs, Spaces, and adjacent network surfaces | `twitter-community-rules.md` | /twitter/ |

## 1. Analyze tweets, threads, replies, and retweets

- User intent: Inspect a tweet, reconstruct a thread, collect replies, or check retweet status.
- Primary entity: tweet / thread / reply / retweet
- Ask for: tweet ID or URL, whether thread/replies/retweets are needed, and page depth.
- Default workflow: Fetch tweet info first, then thread or replies; use retweets and check-retweet only when the user asks for reposting/social proof.
- Reference module: `twitter-content-rules.md`
- Endpoint shortlist:
  - [Tweet info](https://docs.keyapi.ai/en/twitter/tweet.md)
  - [Tweet thread](https://docs.keyapi.ai/en/twitter/tweet_thread.md)
  - [Latest replies](https://docs.keyapi.ai/en/twitter/latest_replies.md)
  - [Retweets](https://docs.keyapi.ai/en/twitter/retweets.md)
  - [Check Retweet](https://docs.keyapi.ai/en/twitter/checkretweet.md)

## 2. Inspect profiles and timelines

- User intent: Analyze a user profile, timeline, media posts, live status, or profile metadata.
- Primary entity: profile / timeline / media
- Ask for: handle or rest ID, content surface, page depth, and whether profile resolution is needed.
- Default workflow: Resolve profile by handle/rest ID as needed, then call timeline/media/live/about endpoints according to requested sections.
- Reference module: `twitter-profile-social-rules.md`
- Endpoint shortlist:
  - [User info](https://docs.keyapi.ai/en/twitter/screenname.md)
  - [About profile](https://docs.keyapi.ai/en/twitter/about.md)
  - [Profiles By RestIds](https://docs.keyapi.ai/en/twitter/screennames.md)
  - [User timeline](https://docs.keyapi.ai/en/twitter/timeline.md)
  - [User's Media](https://docs.keyapi.ai/en/twitter/usermedia.md)
  - [User live](https://docs.keyapi.ai/en/twitter/broadcast.md)
  - [Inspiration Posts](https://docs.keyapi.ai/en/twitter/top_posts.md)

## 3. Map social graph and relationship context

- User intent: Collect followers, following, affiliates, or check whether one account follows another.
- Primary entity: social graph
- Ask for: source profile, target profile for follow checks, direction, page depth, and whether discovered profiles need enrichment.
- Default workflow: Use followers/following for graph collection, check-follow for a specific relationship, and affiliates when the user asks for affiliated accounts.
- Reference module: `twitter-profile-social-rules.md`
- Endpoint shortlist:
  - [Followers](https://docs.keyapi.ai/en/twitter/followers.md)
  - [Following](https://docs.keyapi.ai/en/twitter/following.md)
  - [Check follow](https://docs.keyapi.ai/en/twitter/checkfollow.md)
  - [Affilates](https://docs.keyapi.ai/en/twitter/affilates.md)
  - [Profiles By RestIds](https://docs.keyapi.ai/en/twitter/screennames.md)

## 4. Search and trend monitoring

- User intent: Search posts or inspect current trends for a market or topic.
- Primary entity: search result / trend
- Ask for: query, result mode, location/market when documented, and page depth.
- Default workflow: Use search for explicit queries and trends for current topic discovery; enrich selected tweets or profiles only when needed.
- Reference module: `twitter-content-rules.md`
- Endpoint shortlist:
  - [Search](https://docs.keyapi.ai/en/twitter/search.md)
  - [Trends](https://docs.keyapi.ai/en/twitter/trends.md)
  - [Tweet info](https://docs.keyapi.ai/en/twitter/tweet.md)
  - [User info](https://docs.keyapi.ai/en/twitter/screenname.md)

## 5. Analyze communities and lists

- User intent: Search communities, inspect community details/members/posts, or analyze list timelines/members/followers.
- Primary entity: community / list
- Ask for: community/list identifier, target section, top versus latest preference, and page depth.
- Default workflow: Use community search/info first, then members or posts; use list endpoints for list timeline and membership analysis.
- Reference module: `twitter-community-rules.md`
- Endpoint shortlist:
  - [Communities Search](https://docs.keyapi.ai/en/twitter/search_communities.md)
  - [Community Info](https://docs.keyapi.ai/en/twitter/community_info.md)
  - [Community Members](https://docs.keyapi.ai/en/twitter/community_members.md)
  - [Comunity Posts](https://docs.keyapi.ai/en/twitter/community_timeline.md)
  - [Communities Posts Search Top](https://docs.keyapi.ai/en/twitter/search_communities_top.md)
  - [Communities Posts Search Latest](https://docs.keyapi.ai/en/twitter/search_communities_latest.md)
  - [List timeline](https://docs.keyapi.ai/en/twitter/listtimeline.md)
  - [List members](https://docs.keyapi.ai/en/twitter/list_members.md)
  - [List followers](https://docs.keyapi.ai/en/twitter/list_followers.md)

## 6. Inspect jobs and Spaces

- User intent: Search jobs or retrieve Spaces information connected to Twitter/X activity.
- Primary entity: job / Space
- Ask for: job query or Space identifier, location/filter details when documented, and result depth.
- Default workflow: Use jobs search for hiring queries and Spaces info for a known Space; combine with profile detail only if the user asks for account context.
- Reference module: `twitter-community-rules.md`
- Endpoint shortlist:
  - [Jobs Search](https://docs.keyapi.ai/en/twitter/jobs.md)
  - [Spaces info](https://docs.keyapi.ai/en/twitter/spaces.md)
  - [User info](https://docs.keyapi.ai/en/twitter/screenname.md)

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
