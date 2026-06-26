# Sift Search Tiers

## Tier 1 — Internal Knowledge
Sources: LLM knowledge, current conversation context, Chronicle (if available).
Use for: very fast answers that do not require external search.
Cost: zero.

## Tier 2 — Free Web Search
Providers (priority order): Brave Search API, SearXNG instance, DuckDuckGo.
Use for: standard research queries.
Cost: free.
Fallback: if the primary provider fails or is slow, fall back to the next in priority order.

## Tier 3 — Semantic Research
Providers: Exa, Tavily.
Use only when: deep research is required, sources are sparse, or semantic retrieval materially improves accuracy.
Cost: quota-limited. Monitor daily usage via heartbeat.
Quota field: `quota.tier3_daily_limit` in config.

## Escalation Criteria
- Start at Tier 2 for all external queries
- Escalate to Tier 3 only if: Tier 2 returned <3 useful results AND the query is classified as `research` mode AND Tier 3 quota is not exhausted
- Never escalate for `quick_answer` mode queries

## Provider Telemetry
Record per-session: provider, latency_ms, results_returned, results_used. Mentor may analyze these for optimization.
