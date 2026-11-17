# Global Rules

These rules are the lowest-level execution contract for every Amazon KeyAPI REST workflow. Every scenario, routing path, and endpoint choice must comply with them.

## API-Only Policy

- Use KeyAPI REST API execution for live lookup, ranking, analysis, search, comparison, and reporting.
- Do not browse, inspect, scrape, or navigate Amazon web pages as a substitute for API data.
- Platform web pages may only be referenced when the user explicitly asks about public URLs, UI context, or non-API browsing.

## Source Of Truth

- Documentation index: `https://docs.keyapi.ai/llms.txt`
- Platform docs family: `https://docs.keyapi.ai/en/amazon/`
- API base URL: `https://api.keyapi.ai`
- Authentication: `Authorization: Bearer $KEYAPI_TOKEN`
- Before any live API request, resolve or read the current docs page for the selected endpoint and extract method, `/v1/...` path, required parameters, request body shape, pagination, and response contract.
- Never infer API paths from docs URLs, scenario names, endpoint titles, remembered routes, or a previous 404.
- If this skill conflicts with the official docs page, follow the official docs page.

## REST Execution

- Prefer skill-local scripts under `scripts/` for execution: auth status, docs resolution, then live request.
- Use the host HTTP client only when scripts are unavailable or the helper cannot express the documented request.
- For query values with spaces or shell-sensitive characters, prefer repeated `--query-param key=value` or `--param key=value`; use `--query-file` for structured query objects.
- For large request bodies, file uploads, or image/base64 payloads, prefer `--body-file` or `--image-file` instead of inline shell JSON.

## Parameter Discipline

- Include required parameters exactly as documented.
- Do not send empty optional parameters.
- Confirm enum values, date windows, sorting values, locale/market fields, and pagination fields from the endpoint docs.
- Resolve ambiguous identifiers first through the documented search, conversion, resolver, or detail endpoint.
- Prefer API-side filtering over client-side filtering when the endpoint supports it.

## Response Handling

- Check HTTP status first.
- Then check the KeyAPI response envelope when present:
  - `code = 0`: success
  - non-zero `code`: API-level error; report the `message` and adjust inputs if appropriate
- If auth is missing or a request returns `401`, load `references/setup-and-auth.md` and give the exact setup command `node scripts/configure-keyapi-auth.mjs`.
- For `402` or quota messages, explain that the request needs available credits or plan access.
- For `429`, reduce request rate or wait before retrying.
- For `500`, retry once for idempotent requests before reporting failure.

## Pagination And Scope

- Use the pagination shape documented for the exact endpoint.
- Numeric pagination may use `page`, `page_num`, `page_size`, `limit`, `offset`, or similar fields.
- Cursor pagination must use the cursor returned by the previous response.
- Stop when the requested top N or evidence target is satisfied, the response has no items, `has_more` is false, or no next cursor exists.
- Ask before broad crawling, large fan-out enrichment, or report workflows that require many adjacent endpoints.

## Output Handling

- `scripts/keyapi-api.mjs` sends each request to the live API by default. Repeating the same request with the same parameters calls the API again.
- The helper does not create local response files unless `--output-file` is supplied.
- Large responses may return a stdout preview to keep agent output manageable.
- Use `--output-file path.json` when complete fields are needed for extraction, sorting, aggregation, validation, or downstream analysis. The saved file is the full helper result JSON, and the API payload is usually under `data.data`.
- For agent-internal analysis, write `--output-file` to a temporary path, such as the OS temp directory or a workspace `.tmp-keyapi-*.json` file. Do not present internal temporary files as user deliverables. Clean them up when practical, or briefly mention them in the final answer if they remain.
- If the user asks to save results, export JSON, or provide a file, treat `--output-file` as an intentional user-facing output artifact and choose a clear file path.
- When `savedTo` is present, read that file for deeper analysis instead of repeating the request unless fresh data is required.

## Reporting

- Return findings in the user's language and business context, not raw endpoint language.
- Name the endpoint family or data surface when it affects interpretation.
- For multi-endpoint workflows, separate observed API facts from inference.
