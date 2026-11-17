# SearXNG Engine Diagnostics

When SearXNG returns results but coverage seems poor, verify which engines are actually contributing before concluding a topic is unfindable.

## Check engine health

```bash
curl -s "$SEARXNG_URL/search?q=test&format=json" \
  | jq '{contributing: ([.results[].engines[]] | unique), failing: [.unresponsive_engines[][0]]}'
```

A short `contributing` list means search is degraded at the engine layer — rephrasing the query will not help. Go to primary sources (`references/primary_source_research.md`).

A degraded engine layer is easy to miss because the service still answers HTTP 200 with plausible-looking results.

## N2 MCP

N2 MCP (`n2_web_search`) is SearXNG-backed, no API key required. Registered during `sift.init`. Also provides `n2_news_search` for recency-focused queries. SearXNG aggregates many engines, but only a handful answer from a datacenter IP — the rest are CAPTCHA'd or rate-limited — so treat one call as a narrow sample rather than coverage of the web.
