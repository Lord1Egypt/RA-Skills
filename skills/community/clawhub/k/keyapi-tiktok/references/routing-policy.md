# Routing Policy

Use this file to choose the right TikTok endpoint family and, when necessary, compose multiple endpoints into one answer. Lowest-level rules for docs resolution, Analytics versus realtime data source choice, pagination, response handling, and auth live in `global-rules.md`.

## Default Decision Order

First translate the user's natural-language request into the closest platform data surface and API action. Use `search-keyapi-docs.mjs` to verify current docs after that semantic route is chosen; do not let literal keyword ranking decide the route by itself.

1. Prefer one precise realtime endpoint when the user needs current details, current search results, live status, comments, downloads, image search, or direct lookup.
2. Prefer one Analytics/EchoTik endpoint when the user wants broad discovery, ranking, historical comparison, GMV, sales, creator/product/shop benchmarking, or trend analysis.
3. Prefer a resolver first when the user provides a URL, handle, keyword, category name, image, or ambiguous identifier but the target endpoint needs a canonical ID.
4. Prefer a composed workflow when the user asks for an explanation, comparison, report, or related-entity analysis that one endpoint cannot answer.

For explicit search intent:

1. use the dedicated realtime search endpoint for current entity lookup, unless the user asks for Analytics/EchoTik metrics
2. use the dedicated Analytics list/ranking/search endpoint when the user asks for historical, commerce, or ranking metrics
3. use general Analytics search only as a fallback or cross-entity discovery path

## Required Mode Clarification

Ask the user to choose realtime/current data or Analytics/EchoTik data when both variants exist and the request is ambiguous for these workflows:

- creator detail or creator video list
- product detail, product list, or product reviews
- shop product list or shop report
- video detail, video list, or video trend analysis
- search workflows where the user may mean current public results or analytics-enriched commerce results

Do not ask when the user's wording already makes the mode clear. Words such as current, latest, live, comments, download, image search, and active usually imply realtime. Words such as ranking, historical, GMV, sales, trend, benchmark, top, growth, and performance analysis usually imply Analytics/EchoTik.

## Composition Patterns

### Find creators for a product

- Step 1: resolve or search the product.
- Step 2: fetch product-related creators from Analytics/EchoTik data.
- Step 3: optionally enrich shortlisted creators with creator detail, videos, products, or trend endpoints.

### Explain why a product is selling

- Step 1: fetch product detail in the requested mode.
- Step 2: fetch Analytics/EchoTik trend and review signals when historical performance matters.
- Step 3: fetch related creators, videos, and livestreams when the user asks for traffic sources.

### Explain why a video performed well

- Step 1: fetch realtime or Analytics video detail according to the user's mode choice.
- Step 2: use realtime 14-day interaction trend for recent movement, or Analytics/EchoTik trends for historical snapshots.
- Step 3: fetch comment keywords, comments, captions, and linked products only when they support the explanation.

### Explore hashtag or music opportunities

- Step 1: search the hashtag or music keyword if only text is known.
- Step 2: fetch associated videos or trend detail.
- Step 3: enrich selected videos or creators only when the user asks for examples or execution ideas.

### Evaluate a shop

- Step 1: use shop list/ranking for discovery, or shop detail when a seller is known.
- Step 2: fetch shop products, trends, creators, videos, or livestreams according to the report sections.
- Step 3: use realtime shop products for current catalog and Analytics/EchoTik shop products for performance history.

## Report Policy

- If the user asks for a comprehensive report, confirm the sections before calling every adjacent endpoint family.
- Typical creator report sections: detail, trend, videos, products, followers/following, region, milestones, livestream history, and ranking context.
- Typical product report sections: detail, trend, reviews, related creators, related videos, related livestreams, category/ranking context, and realtime product state.
- Typical shop report sections: detail, trend, products, creators, videos, livestreams, ranking context, and realtime catalog.
- Typical video report sections: detail, interaction trend, comments, comment keywords, captions, linked products, creator context, and download URL when requested.

## UX Policy

- Do not expose endpoint names first to non-technical users. Think in terms of business goals and entity families, then map to endpoints.
- When docs search is needed, query with the inferred API concept and action, then verify the selected page before execution.
- Ask only for missing high-value inputs that cannot be safely defaulted from the scenario.
- Prefer API-side filtering from the current docs over client-side filtering.
- If params are uncertain, resolve the docs page and use one minimal documented request instead of guessing hidden enums.
- If tools are available, execute the chosen API instead of only describing what would be called.
- Never answer a data question by pointing the user to TikTok, TikTok Shop, or EchoTik web pages.

## API Questions

If the user asks technical API questions such as which endpoint to use, what Analytics means, why a parameter is required, or how auth works, answer directly from the docs and this policy. Execute live calls only when the user wants data back.
