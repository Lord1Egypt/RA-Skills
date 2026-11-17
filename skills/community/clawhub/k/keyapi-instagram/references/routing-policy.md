# Routing Policy

Use this file to choose the right Instagram endpoint family and, when necessary, compose multiple endpoints into one answer. Lowest-level execution rules live in `global-rules.md`.

## Default Decision Order

First translate the user's natural-language request into the closest platform data surface and API action. Use `search-keyapi-docs.mjs` to verify current docs after that semantic route is chosen; do not let literal keyword ranking decide the route by itself.

1. If the user provides an exact identifier or URL, start with the narrowest detail, resolver, conversion, or content endpoint.
2. If the user provides a keyword, broad topic, category, or discovery goal, start with the relevant search/list endpoint.
3. If the user asks for top, best, trending, ranking, growth, demand, or monitoring, prefer a ranking, trend, feed, vertical-search, or list endpoint when the docs provide one.
4. If the user asks why something performed well or asks for evidence, combine detail with comments/reviews/replies/related entities only as needed.
5. If a comprehensive report would require many adjacent calls, confirm sections and maximum scope before execution.

## Module Loading

- Use `references/scenarios.md` to select the scenario card.
- Load only the smallest relevant module file from `references/` for the selected scenario.
- If a request spans modules, load the additional module only when it adds a necessary endpoint family or rule.
- Treat module files as routing guidance; final method/path/parameters still come from the current official docs page.

## Endpoint Selection

- Prefer one precise endpoint over a broad endpoint plus manual filtering.
- When docs search is needed, query with the inferred API concept and action, then verify the selected page before execution.
- Prefer documented API filters over client-side filtering.
- Resolve identifiers before detail, comments, related-entity, or enrichment calls.
- Search/list first, then enrich shortlisted results with detail endpoints.
- For comparison, normalize target entities, metrics, markets, date windows, and page depth before comparing.

## User Interaction

- Do not expose raw endpoint names first for non-technical users; translate intent into a workflow.
- Ask only for missing high-value inputs that cannot be safely defaulted.
- If the request is vague, offer 2 to 4 concrete scenario options.
- If the user asks for API integration details, answer with method, path, auth, required params, and a minimal helper-script example after resolving the docs.

## Stop Conditions

Stop collecting pages, enriching entities, or adding related endpoints when:

- the user's requested top N or scope is satisfied
- no next page/cursor exists
- `has_more` is false
- extra calls would add low-value noise
- the user has not approved a broad report workflow
