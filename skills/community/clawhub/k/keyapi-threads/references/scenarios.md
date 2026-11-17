# Scenario Cards

Use these scenario cards to translate natural-language Threads requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

users, user IDs, profiles, posts, replies, reposts, comments, top content, recent content, and profile search results

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| Profile search and user information | `threads-profile-rules.md` | /threads/ |
| User posts, replies, reposts, post detail, and comments | `threads-content-rules.md` | /threads/ |
| Top and recent content search | `threads-search-rules.md` | /threads/ |

## 1. Find and inspect profiles

- User intent: Search Threads profiles and retrieve user information.
- Primary entity: user / profile
- Ask for: profile keyword, username, or user ID; page depth; and whether activity is needed.
- Default workflow: Use profile search for discovery, then user info or user info by ID for selected profiles.
- Reference module: `threads-profile-rules.md`
- Endpoint shortlist:
  - [Search profiles](https://docs.keyapi.ai/en/threads/search_profiles.md) - Search Threads user profiles
  - [Get user info](https://docs.keyapi.ai/en/threads/fetch_user_info.md) - Get Threads user information
  - [Get user info by ID](https://docs.keyapi.ai/en/threads/fetch_user_info_by_id.md) - Get Threads user information by user ID

## 2. Audit user activity and posts

- User intent: Collect user posts, replies, reposts, or post comments.
- Primary entity: user content / post / comment
- Ask for: user identifier or post URL/shortcode, content surfaces, and page/comment depth.
- Default workflow: Fetch user info first if needed, then posts/replies/reposts; use post detail/comments for selected posts.
- Reference module: `threads-content-rules.md`
- Endpoint shortlist:
  - [Get user posts](https://docs.keyapi.ai/en/threads/fetch_user_posts.md) - Get the list of posts by a Threads user
  - [Get user replies](https://docs.keyapi.ai/en/threads/fetch_user_replies.md) - Get the list of replies by a Threads user
  - [Get user reposts](https://docs.keyapi.ai/en/threads/fetch_user_reposts.md) - Get the list of reposts by a Threads user
  - [Get Post Detail](https://docs.keyapi.ai/en/threads/fetch_post_detail.md) - Get Threads post details (supports shortcode and full URL)
  - [Get post comments](https://docs.keyapi.ai/en/threads/fetch_post_comments.md) - Get the list of comments for a Threads post

## 3. Search top or recent content

- User intent: Find Threads content around a keyword using top or recent ordering.
- Primary entity: content search result
- Ask for: keyword, top versus recent preference, and result depth.
- Default workflow: Use top content for high-visibility posts and recent content for freshness; enrich selected posts through content rules.
- Reference module: `threads-search-rules.md`
- Endpoint shortlist:
  - [Search top content](https://docs.keyapi.ai/en/threads/search_top.md) - Search Threads top content
  - [Search recent content](https://docs.keyapi.ai/en/threads/search_recent.md) - Search Threads recent content

## Docs Search Strategy

1. Map the user's natural-language request to the closest scenario and API concept, then search `llms.txt` for the platform slug plus that semantic entity/action. Do not rely on literal keyword matching when the user wording is vague, translated, or business-oriented.
2. Prefer the narrowest endpoint whose title and description match the requested workflow.
3. Resolve the selected endpoint page before any live call; never infer method or path from this file.
4. Compose multiple endpoints only when the user asks for a report, comparison, enrichment, or explanation that one endpoint cannot answer.
5. API calls are live by default. Repeating the same parameters calls the API again. Large payloads may return a stdout preview; when complete fields are needed for analysis, rerun the same documented request with `--output-file <temp-or-workspace-.tmp-keyapi-file>.json` and read the API payload from `data.data`. Use a user-facing output path only when the user asks to save or export results.

## User Input Compression

- Goal: search, detail, enrichment, ranking, comparison, monitoring, or report
- Entity: the object being searched, analyzed, compared, ranked, or monitored
- Scope: market, country, language, category, keyword, identifier, date window, and page depth
- Sort or metric: freshness, relevance, growth, engagement, rating, sales, price, audience, or other documented metric
- Pagination depth: one page, top N, until enough evidence, or all available within the user's approved scope
- Output format: concise answer, table, raw JSON, or structured report
