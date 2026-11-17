---
name: keyapi-tiktok
description: Analyze TikTok creators, TikTok Shop commerce, content, live streams, trends, ads, products, shops, categories, videos, hashtags, music, comments, and audience signals through the KeyAPI REST API using live official docs. Use for influencer discovery, product and seller research, video intelligence, live commerce, trend monitoring, and multi-endpoint reports.
---

# TikTok KeyAPI Skill

Turn natural-language TikTok requests into documentation-guided KeyAPI REST workflows. Start from the user's business goal, map it to the closest scenario, verify the current endpoint contract in the latest KeyAPI docs, then execute the request with a helper script when available or with direct REST when it is not.

## Execution Contract

- Use KeyAPI REST API execution for live data lookup, ranking, analysis, search, comparison, and reporting.
- Treat `https://docs.keyapi.ai/llms.txt` and linked endpoint pages as the source of truth for method, `/v1/...` path, parameters, enums, pagination, request body, and response shape.
- Do not use platform web pages or manual browsing as a substitute for API data.
- Keep credentials local. Never print or restate `KEYAPI_TOKEN`.
- If official docs conflict with this skill, follow the official docs.

## Workflow

1. Apply `references/global-rules.md` as the base execution contract.
2. Check auth with `node scripts/configure-keyapi-auth.mjs --status` when script execution is available and setup state is unknown; treat `authStatus: "available"` as ready and `authStatus: "unavailable"` as missing credentials.
3. If `authStatus` is `unavailable`, stop live execution, load `references/setup-and-auth.md`, and tell the user the exact setup command: `node scripts/configure-keyapi-auth.mjs`. Do not only say "set KEYAPI_TOKEN".
4. Identify the user's goal, entity, scope, metric, pagination depth, and desired output.
5. Use `references/scenarios.md` to map the request to a TikTok scenario.
6. Use `references/routing-policy.md` to choose search/list, detail, resolver, ranking/trend, related-entity, or composed workflow patterns.
7. Apply `references/tiktok-rules.md` for TikTok-specific identifiers, pagination, and reporting rules.
8. Load the relevant scenario module before endpoint selection:
   - `references/tiktok-influencer-rules.md` for TikTok Influencer workflows.
   - `references/tiktok-shop-rules.md` for TikTok Shop product, shop, seller, category, review, and commerce workflows.
   - `references/tiktok-content-rules.md` for video, comments, hashtags, music, live, captions, downloads, and content search workflows.
   - `references/tiktok-intelligence-rules.md` for trend, insight, ad, keyword, top product, hashtag, music, and viral intelligence workflows.
9. Resolve current docs with `node scripts/search-keyapi-docs.mjs --query "<semantic entity action>" --resolve` when the helper script is available; otherwise open `https://docs.keyapi.ai/llms.txt` and the selected endpoint page directly. Build the query from the inferred scenario/API concept, not by copying vague or translated user wording literally.
10. Use the resolver output or opened docs page to extract the current OpenAPI method, `/v1/...` path, required query/body parameters, examples, and response contract before any live API call. Never infer API paths from docs URLs, scenario names, endpoint titles, remembered routes, or a previous 404.
11. Ask only for missing high-value inputs that cannot be safely defaulted.
12. Prefer `node scripts/keyapi-api.mjs` for live REST calls when script execution is available. Use the host's HTTP client only when scripts are unavailable or the helper cannot express the documented request.
13. Check HTTP status and KeyAPI response envelope. `code = 0` means success; non-zero `code` is an API-level failure.
14. Return the result in user-facing analytical language, separating observed API facts from inference.

## Interaction Rules

- Do not start by listing raw endpoints or dumping all parameters. First identify the user's business goal, choose the closest scenario, collect only missing high-value inputs, resolve the current docs, then execute.
- Prefer scenario names and user-facing workflows over endpoint names for non-technical users. Use raw endpoint names only after the route is chosen or when the user asks for integration details.
- Treat endpoint selection as semantic routing first: infer the platform data surface and action from the user's goal, then use docs search to verify the current endpoint.
- If multiple endpoints could solve the task, choose the one with the least user input burden and strongest documented filtering.
- If the user's request is vague, offer 2 to 4 concrete scenario options instead of asking an open-ended question.
- If a request needs a broad report or many adjacent calls, confirm the sections and maximum scope before execution.
- If credentials are missing, pause live execution and route to setup; do not fall back to platform websites or unauthenticated browsing for API data.

## Scenario Selection

Read `references/scenarios.md` to choose the best scenario card. If no exact scenario fits, use the nearest scenario with explicit assumptions or fall back to advanced mode that exposes filters gradually. Treat the official docs index as the endpoint source of truth, not the scenario card.

## Input Model

Compress parameter-heavy APIs into these decision fields:

- Goal: search, detail, enrichment, ranking, comparison, monitoring, or report
- Entity: the TikTok object being searched, analyzed, compared, ranked, or monitored
- Scope: country/region, category, keyword, creator/product/shop/video/hashtag/music/live identifier, and date window
- Metric or sort: GMV, sales, views, likes, comments, shares, engagement rate, follower growth, ranking position
- Pagination depth: one page, top N, until enough evidence, or all available within the user's approved scope
- Output format: concise answer, table, raw JSON, or structured report

## Scenario Families

- TikTok Influencer: creator discovery, profile detail, followers/following, videos, products, live history, region, milestones, trend, and rankings.
- TikTok Shop: products, shops, categories, reviews, rankings, product creators, videos, livestreams, image search, and seller analysis.
- TikTok Content: videos, comments, replies, captions, downloads, hashtags, music, live streams, covers, and general content search.
- TikTok Intelligence: trending videos, hashtags, music, ad insights, keyword insights, top products, and market intelligence.

## KeyAPI-Specific Usage

- Prefer API-side filters from the current docs over client-side filtering.
- If multiple endpoints could solve the task, choose the one with the least user input burden and strongest documented filtering.
- For broad reports, confirm the requested sections before launching a multi-endpoint workflow.
- For TikTok reporting, distinguish creator, product, shop, category, video, hashtag, music, live, ad, and trend signals.
- Use the scenario-specific reference module as the endpoint shortlist, then verify the final method/path/params in the live docs page.
- If the user asks about integration details, answer with method, path, auth, required params, and a minimal request example from the current docs.

## Onboarding Rule

When the user has not set up credentials yet, proactively provide the setup script command. Do not answer only with "configure KEYAPI_TOKEN".

When `authStatus` is `unavailable`:

- explain that KeyAPI uses Bearer token authentication with `KEYAPI_TOKEN`
- point them to the KeyAPI dashboard and auth docs
- require local setup with `node scripts/configure-keyapi-auth.mjs` when script execution is available
- also mention `node scripts/configure-keyapi-auth.mjs --status` for checking whether authentication is available
- explain that setup writes credentials into shell environment variables
- explain that `--status` reports `available` or `unavailable`; continue live requests when it reports `available`
- continue live requests only after setup is complete

## Script Contract

This skill includes helper scripts under `scripts/` for reliable local execution:

- `scripts/configure-keyapi-auth.mjs`
- `scripts/search-keyapi-docs.mjs`
- `scripts/keyapi-api.mjs`

Run script commands from this skill directory. If the host agent uses a different current working directory, resolve `scripts/...` relative to this `SKILL.md`. For large JSON bodies, especially base64 image payloads, prefer `--body-file` or `--image-file` instead of inline `--body`. `keyapi-api.mjs` always sends live API requests; repeating identical requests calls the API again. The helper does not create local response files unless `--output-file` is supplied. Large responses may return a stdout preview; when complete fields are needed for extraction, sorting, aggregation, or validation, use `--output-file` to save the full helper result and read the API payload from `data.data`. For agent-internal analysis, write to a temporary path such as the OS temp directory or a workspace `.tmp-keyapi-*.json` file; do not present that temporary file as a user deliverable, and clean it up when practical or briefly mention it in the final answer. When the user asks to save results, export JSON, or provide a file, treat `--output-file` as an intentional user-facing output file. Use `--stdout full` only when the user explicitly needs raw JSON in stdout. For query strings, prefer repeated `--query-param key=value` or `--param key=value`; use `--query-file query.json` or `--query` only when structured array/object query values are needed. Query sources merge in this order: `--query`, `--query-file`, then repeated query params, with later values overriding earlier ones; empty query-param values are not sent.

Prefer them in this order when script execution is available:

1. auth status
2. docs resolution before live REST calls
3. live REST call

If script execution is unavailable in the host agent, or if the helper cannot express the documented request, do not fail the task. Use the same documented REST method, path, headers, query, and body with the host's available HTTP client.

## Script Examples

Resolve current docs for this platform:

```bash
node scripts/search-keyapi-docs.mjs --query "<entity action>" --resolve
```

Execute a documented GET endpoint:

```bash
node scripts/keyapi-api.mjs --path /v1/tiktok/... --query-param example=value
```

Execute query parameters from a JSON file:

```bash
node scripts/keyapi-api.mjs --path /v1/tiktok/... --query-file query.json
```

Preview a large response without saving:

```bash
node scripts/keyapi-api.mjs --path /v1/tiktok/... --query-param example=value --stdout preview
```

Write a complete response to a temporary file for internal analysis:

```bash
node scripts/keyapi-api.mjs --path /v1/tiktok/... --query-param example=value --output-file .tmp-keyapi-tiktok-response.json
```

Save or export a complete response for the user:

```bash
node scripts/keyapi-api.mjs --path /v1/tiktok/... --query-param example=value --output-file response.json
```

Execute a documented POST endpoint:

```bash
node scripts/keyapi-api.mjs --path /v1/tiktok/... --method POST --body '{"example":"value"}'
```

Execute a documented POST endpoint with a large JSON body:

```bash
node scripts/keyapi-api.mjs --path /v1/tiktok/... --method POST --body-file request.json
```

Execute an image JSON endpoint from a local file:

```bash
node scripts/keyapi-api.mjs --path /v1/tiktok/realtime/product/photo-search --method POST --query-param region=US --query-param "sk=blue lounge set" --image-file ./image.jpg --image-field image_base64
```

## References

- `references/global-rules.md`
- `references/scenarios.md`
- `references/routing-policy.md`
- `references/tiktok-rules.md`
- `references/tiktok-search-rules.md`
- `references/tiktok-product-rules.md`
- `references/tiktok-seller-rules.md`
- `references/tiktok-influencer-rules.md`
- `references/tiktok-video-rules.md`
- `references/tiktok-live-rules.md`
- `references/tiktok-intelligence-rules.md`
- `references/tiktok-content-rules.md`
- `references/tiktok-shop-rules.md`
- `references/setup-and-auth.md`
