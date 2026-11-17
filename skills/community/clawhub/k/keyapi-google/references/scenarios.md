# Scenario Cards

Use these scenario cards to translate natural-language Google requests into a small, stable set of inputs. They are routing hints only; the exact method, `/v1/...` path, parameters, body shape, pagination, and response contract must come from `https://docs.keyapi.ai/llms.txt` and the linked endpoint page before execution.

Do not start by listing raw endpoints. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute through `scripts/keyapi-api.mjs` when available.

## Core Entities

queries, SERP results, images, Lens inputs, videos, news, shopping results, places, maps, reviews, scholar results, patents, autocomplete suggestions, and webpages

## Scenario Modules

| User intent | Reference module | Docs path family |
|---|---|---|
| Web search and query expansion | `google-search-rules.md` | /google/ |
| Selected webpage extraction | `google-webpage-rules.md` | /google/ |
| Images, Lens, and video results | `google-visual-rules.md` | /google/ |
| Local places, maps, and reviews | `google-local-rules.md` | /google/ |
| News, shopping, scholar, and patents | `google-vertical-rules.md` | /google/ |

## 1. Run web research

- User intent: Find web sources and expand/refine queries.
- Primary entity: query / SERP
- Ask for: query, country/language/location, freshness or result constraints, and whether extraction is needed.
- Default workflow: Use autocomplete only when helpful, then web search; extract selected pages if the user needs source content.
- Reference module: `google-search-rules.md`
- Endpoint shortlist:
  - [autocomplete](https://docs.keyapi.ai/en/google/autocomplete.md)
  - [search](https://docs.keyapi.ai/en/google/search.md) - Search

## 2. Extract selected webpages

- User intent: Analyze a URL or selected search result page.
- Primary entity: webpage
- Ask for: URL and desired extraction/summary goal.
- Default workflow: Use webpage extraction directly for user-provided URLs or after a search/vertical result is selected.
- Reference module: `google-webpage-rules.md`
- Endpoint shortlist:
  - [Webpage](https://docs.keyapi.ai/en/google/webpage.md)

## 3. Find visual or video results

- User intent: Search images/videos or visually similar results from an image.
- Primary entity: image / Lens / video
- Ask for: text query or image URL, market/language, and result depth.
- Default workflow: Use images/videos for text queries and Lens for image input; extract selected pages only if needed.
- Reference module: `google-visual-rules.md`
- Endpoint shortlist:
  - [images](https://docs.keyapi.ai/en/google/images.md)
  - [Image Search(Lens)](https://docs.keyapi.ai/en/google/lens.md) - Image Search
  - [videos](https://docs.keyapi.ai/en/google/videos.md)

## 4. Analyze local places and reviews

- User intent: Find local businesses, map results, or reputation evidence.
- Primary entity: place / map / review
- Ask for: business/category query, location, language, and review depth.
- Default workflow: Use places/maps for discovery, then reviews for selected targets.
- Reference module: `google-local-rules.md`
- Endpoint shortlist:
  - [places](https://docs.keyapi.ai/en/google/places.md)
  - [maps](https://docs.keyapi.ai/en/google/maps.md)
  - [reviews](https://docs.keyapi.ai/en/google/reviews.md)

## 5. Use specialized Google verticals

- User intent: Research news, shopping results, academic literature, or patents.
- Primary entity: vertical result
- Ask for: query, vertical, market/language, time/filter constraints, and output depth.
- Default workflow: Choose the vertical endpoint that matches the requested surface; extract selected pages when deeper content is needed.
- Reference module: `google-vertical-rules.md`
- Endpoint shortlist:
  - [news](https://docs.keyapi.ai/en/google/news.md)
  - [shopping](https://docs.keyapi.ai/en/google/shopping.md)
  - [scholar](https://docs.keyapi.ai/en/google/scholar.md)
  - [patents](https://docs.keyapi.ai/en/google/patents.md)

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
