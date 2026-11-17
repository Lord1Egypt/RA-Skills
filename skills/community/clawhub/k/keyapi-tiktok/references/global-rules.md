# Global Rules

These rules are the lowest-level execution contract for TikTok KeyAPI REST workflows. Every scenario, routing path, and endpoint choice must comply with them.

## Source Of Truth

- Documentation index: `https://docs.keyapi.ai/llms.txt`
- API base URL: `https://api.keyapi.ai`
- Authentication: `Authorization: Bearer $KEYAPI_TOKEN`
- Before any live API request, resolve or read the current docs page for the selected endpoint and decide the final method, `/v1/...` path, required parameters, body shape, and pagination from that page.
- Never infer API paths from docs URLs, scenario names, endpoint titles, remembered routes, or 404 responses.
- If this skill text conflicts with the official docs, follow the official docs.

## Data Source Type

- In KeyAPI TikTok docs, endpoint titles containing `Analytics` and docs paths ending in `-analytics` represent EchoTik analytics data. Treat them as offline or enriched analytics datasets, not realtime public-state lookups.
- Analytics/EchoTik endpoints are appropriate for historical trends, ranking, broad discovery, commerce metrics, GMV, sales, creator/product/shop benchmarking, and multi-dimensional filters.
- Endpoints without `Analytics` are realtime/current interfaces. Treat them as the default for current profile/detail/search/comment/live/download/image-search requests.
- If both Analytics and non-Analytics variants exist and the user has not specified freshness versus historical depth, ask a short mode question before execution.
- If an Analytics/EchoTik lookup returns `code = 0` with empty data for a specific entity, do not immediately conclude the entity does not exist. When a realtime variant exists, offer or use the realtime endpoint according to the user's freshness need.

## REST Execution

- Use the documented method, path, query parameters, and JSON body from the current docs page.
- Do not execute a live REST call until the current docs page or resolver output has produced the endpoint method and `/v1/...` path.
- Prefer the skill-local helper scripts under `scripts/` for local execution; the current KeyAPI docs remain the API source of truth.
- Use the host's available HTTP client only when helper scripts are unavailable or cannot express the documented request.
- Do not use gateway tool schemas or remembered MCP tool definitions as the source of truth.
- Do not navigate TikTok, TikTok Shop, or EchoTik web pages as a fallback for API data.

## Parameter Discipline

- Include required parameters exactly as documented.
- Do not send empty optional parameters.
- Confirm enum values, date windows, sort values, country/region codes, and pagination fields from the endpoint docs.
- When identifiers are ambiguous, resolve them first through the documented resolver/search/detail endpoint.
- For category-sensitive Analytics calls, resolve category levels through the documented primary, secondary, and tertiary category endpoints before using category IDs.

## Response Handling

- Check HTTP status first.
- Then check KeyAPI response envelope when present:
  - `code = 0`: success
  - non-zero `code`: API-level error; report the `message` and adjust inputs if appropriate
- For missing credentials or `401`, load `references/setup-and-auth.md` and give the exact setup command `node scripts/configure-keyapi-auth.mjs`; also mention `node scripts/configure-keyapi-auth.mjs --status` and continue only when it reports `authStatus: "available"`.
- For `402` or quota messages, explain that the request needs available credits or plan access.
- For `429`, wait or reduce request rate.
- For `500`, retry once for idempotent requests before reporting failure.

## Output Handling

- `scripts/keyapi-api.mjs` sends each request to the live API by default. Repeating the same request with the same parameters calls the API again.
- The helper does not create local response files unless `--output-file` is supplied.
- Large responses may return a stdout preview to keep agent output manageable.
- Use `--output-file path.json` when complete fields are needed for extraction, sorting, aggregation, validation, or downstream analysis. The saved file is the full helper result JSON, and the API payload is usually under `data.data`.
- For agent-internal analysis, write `--output-file` to a temporary path, such as the OS temp directory or a workspace `.tmp-keyapi-*.json` file. Do not present internal temporary files as user deliverables. Clean them up when practical, or briefly mention them in the final answer if they remain.
- If the user asks to save results, export JSON, or provide a file, treat `--output-file` as an intentional user-facing output artifact and choose a clear file path.
- When `savedTo` is present, read that file for deeper analysis instead of repeating the request unless fresh data is required.

## Reporting

- Summarize the answer in the user's language.
- State whether the workflow used Analytics/EchoTik data, realtime data, or both when that affects freshness or interpretation.
- For multi-endpoint workflows, separate observed API facts from analytical inference.
