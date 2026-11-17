# Scenario Cards

Use these scenario cards to translate natural-language Facebook requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

public profiles, pages, profile IDs, profile posts, Reels, photos, public groups, group IDs, group posts, and future events

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| Public profile/page ID resolution and baseline detail | `facebook-profile-rules.md` | /facebook/ |
| Public profile/page posts, Reels, and photos | `facebook-profile-content-rules.md` | /facebook/ |
| Public group details, posts, and future events | `facebook-group-rules.md` | /facebook/ |

## 1. Resolve and inspect public profiles or pages

- User intent: Get reliable profile/page details from a URL or ID before collecting posts or media.
- Primary entity: profile / page
- Ask for: profile or page URL, profile ID if known, and whether follow-on content is needed.
- Default workflow: Resolve identity first, then retrieve URL or ID detail; route media/content sections to the profile content module.
- Reference module: `facebook-profile-rules.md`
- Endpoint shortlist:
  - [Get profile id](https://docs.keyapi.ai/en/facebook/profile_profile_id.md) - Get user ID from profile URL
  - [Profile details by url](https://docs.keyapi.ai/en/facebook/profile_details_url.md) - Get profile details via Facebook profile URL
  - [Profiles details by id](https://docs.keyapi.ai/en/facebook/profile_details_id.md) - Get profile details by ID, used in conjunction with get_profile_id (profile_details_by_url as an alternative)

## 2. Collect profile/page posts and media

- User intent: Analyze recent public posts, Reels, or photos for a profile/page.
- Primary entity: profile content
- Ask for: profile/page identifier, content type, page depth, and topic/time focus if supported.
- Default workflow: Use posts, Reels, or photos according to the requested surface; resolve profile/page first if identity is ambiguous.
- Reference module: `facebook-profile-content-rules.md`
- Endpoint shortlist:
  - [Profile posts](https://docs.keyapi.ai/en/facebook/profile_posts.md) - Get public Facebook profile posts.
  - [Profile Reels](https://docs.keyapi.ai/en/facebook/profile_reels.md) - Get a public Facebook page's reels.
  - [Profiles photos](https://docs.keyapi.ai/en/facebook/profile_photos.md) - Get a public Facebook page's photos.

## 3. Analyze public groups

- User intent: Inspect a public group baseline, posts, and upcoming events.
- Primary entity: group
- Ask for: group URL or ID, desired post depth, and whether future events are needed.
- Default workflow: Resolve group ID, fetch group detail, then posts and future events only when requested.
- Reference module: `facebook-group-rules.md`
- Endpoint shortlist:
  - [Get group id](https://docs.keyapi.ai/en/facebook/group_id.md) - Get a public Facebook group ID.
  - [Get group details](https://docs.keyapi.ai/en/facebook/group_details.md) - Get a public Facebook groups details.
  - [Get group posts](https://docs.keyapi.ai/en/facebook/group_posts.md) - Get a public Facebook groups posts.
  - [Get group future events](https://docs.keyapi.ai/en/facebook/group_future_events.md) - Get a public Facebook group future events.

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
