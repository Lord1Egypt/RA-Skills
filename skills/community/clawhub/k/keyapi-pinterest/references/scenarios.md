# Scenario Cards

Use these scenario cards to translate natural-language Pinterest requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

users, profiles, boards, pins, followers, and following relationships

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| User search and profile information | `pinterest-profile-rules.md` | /pinterest/ |
| Boards and pins | `pinterest-content-rules.md` | /pinterest/ |
| Followers and following | `pinterest-network-rules.md` | /pinterest/ |

## 1. Find and inspect Pinterest users

- User intent: Search users and retrieve profile information.
- Primary entity: user / profile
- Ask for: keyword or username, page depth, and whether boards/pins/social graph should be included.
- Default workflow: Search users for discovery, then get user information for selected accounts.
- Reference module: `pinterest-profile-rules.md`
- Endpoint shortlist:
  - [Search Users](https://docs.keyapi.ai/en/pinterest/search.md) - Search Users
  - [Get user information](https://docs.keyapi.ai/en/pinterest/information.md) - Get user information

## 2. Audit boards and pins

- User intent: Understand what a Pinterest account curates or publishes.
- Primary entity: board / pin
- Ask for: username or user identifier, boards versus pins, and page depth.
- Default workflow: Resolve user first, then retrieve boards and pins according to the requested surface.
- Reference module: `pinterest-content-rules.md`
- Endpoint shortlist:
  - [Get boards](https://docs.keyapi.ai/en/pinterest/boards.md) - Get a user's boards
  - [Get pins](https://docs.keyapi.ai/en/pinterest/pins.md) - Get Pinterest pin

## 3. Map follower and following context

- User intent: Inspect who follows a user or who the user follows.
- Primary entity: followers / following
- Ask for: user identifier, direction, page depth, and enrichment scope.
- Default workflow: Use followers or following based on direction; enrich only selected related users unless broad traversal is approved.
- Reference module: `pinterest-network-rules.md`
- Endpoint shortlist:
  - [Get followers detail](https://docs.keyapi.ai/en/pinterest/followers.md) - Get followers detail
  - [Get following detail](https://docs.keyapi.ai/en/pinterest/followings.md) - Get following detail

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
