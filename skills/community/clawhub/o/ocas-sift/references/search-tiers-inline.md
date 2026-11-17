# Sift — Search Tier Selection

All configured search sources fire in parallel. Results are deduplicated by URL and content hash.

- **Internal knowledge** — LLM knowledge, conversation context, Chronicle if available. Always runs first as a pre-check.
- **Free web search (parallel fan-out)** — all of the following fire simultaneously:
  - **N2 MCP** (`n2_web_search`) — SearXNG-backed, 70+ engines, no API key required. Registered during `sift.init`. Also provides `n2_news_search` for recency-focused queries.
  - **Brave Search API** — structured web results. See `references/search_tiers.md` for provider configuration and API keys.
  - **SearXNG** — self-hosted instance. See `references/search_tiers.md` for provider configuration and API keys. **Deduplication gate:** if self-hosted SearXNG responds, skip the N2 MCP call — both are SearXNG-backed and results would duplicate.
  - **Platform search** — agent-reach on Twitter/X (via Mirror Rotator → Search Bridge), Reddit, LinkedIn, GitHub, etc.
- **Semantic research** — Exa, Tavily. Deep research only. Quota-limited (~50 calls/day combined). Runs when standard web search is insufficient.

For detailed tier-by-tier workflow, API curl examples, and cloud environment fallbacks, read `references/research-workflow.md`.

Read `references/search_tiers.md` for provider details.


```bash
# Primary — web_search tool (SearXNG plugin, no CAPTCHA)
# Just call web_search directly; it routes to SearXNG automatically.
# For raw access (e.g., from scripts):
curl -s "http://localhost:8888/search?q=QUERY&format=json" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for r in d.get('results',[])[:10]:
    print(r['title']); print(r['url']); print(r['content'][:200]); print()
"

# Fallback — CSAPI (route through Reach for quota management)
reach.csapi_check
reach.csapi_increment  # after each CSAPI query
```
