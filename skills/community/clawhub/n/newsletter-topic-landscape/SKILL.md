---
name: newsletter-topic-landscape
description: Compare editorial topics and coverage across Substack newsletters through Crawlora publication discovery and bounded public post samples. Use for a newsletter landscape, publication positioning map, coverage-gap brief, or topic-focused reading shortlist without inferring readership.
---

# Newsletter topic landscape

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound pages and calls by the requested scope and credit budget.
Preserve source IDs, URLs, retrieval times, and source dates where supplied.

Map what a chosen set of newsletters publishes about a topic. Define topic and
synonyms, date window, language, publication scope, and balanced per-publication
sample budget. Use a supplied publication set first; search and category results
are discovery samples rather than a complete newsletter universe.

## Resolve publications and sample their editorial work

1. Use site-wide `substack_search` for candidate posts/publications or discover
   categories before browsing. Category `paid`/`free` scopes differ; do not pass
   a category ID to a route that expects a publication ID. Search/category pages
   are zero-based; publication archives use `offset`/`limit`.
2. Resolve each publication's subdomain/custom domain and numeric publication ID.
   Use detail and contributors to distinguish publication identity from writer
   identity. Recommendations are attributed publication links, not proof of
   commercial affiliation or endorsement of every story.
3. Sample each publication archive with `sort=new` for comparable recent coverage,
   or an explicit topical search. `top`/`community` ordering samples popular
   posts, not chronology; do not call those representative recent coverage.
   Preserve selection rules, returned dates, offsets, and the stopping reason.
4. Site-wide search supplies metadata, not article bodies. Fetch selected posts
   using the discovered publication and post slug. Treat public previews and
   paywalled articles as partial evidence. If only a title is available, label
   the coding basis as title-only and lower claim specificity.

```sh
scripts/crawlora.sh /substack/search query="climate adaptation" page=0
scripts/crawlora.sh /substack/categories
# Use discovered publication/slug values, for example:
# scripts/crawlora.sh /substack/publication/posts publication="$PUBLICATION" sort=new limit=10 offset=0
# scripts/crawlora.sh /substack/post publication="$PUBLICATION" slug="$POST_SLUG"
```

## Code topics and distinguish editorial positioning

Create a shared topic rubric, preserving unexpected topics and uncertain labels.
A post may receive multiple labels; label counts can therefore exceed unique
posts. Deduplicate by canonical post URL/ID within each publication, and retain
cross-publication reposts as related content. Compare topic shares only with
visible denominators, equal sampling rules, and unavailable-body counts.
Separate frequency of publication, article length/depth, framing, and engagement
observations. Likes/comments and leaderboard positions do not establish reader
numbers, paid subscribers, revenue, influence, or audience demographics.

Return a publication-by-topic matrix, sampled-post evidence with dates/URLs and
coding basis, notable editorial differences, a reading shortlist, and observed
coverage gaps. An unobserved topic is a gap in the sample, not proof a publication
never covers it or proof of market demand for a new newsletter. Do not subscribe,
contact writers, or create a recurring coverage monitor unless requested.
