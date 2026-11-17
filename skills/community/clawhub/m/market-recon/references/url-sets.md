# Proven URL Sets for GitHub Recon

All URLs verified working on 2026-09-02 via `web_fetch` (HTTP 200).

## Trending pages (HTML, use extractMode markdown)

- https://github.com/trending
- https://github.com/trending?since=weekly
- https://github.com/trending/python?since=weekly
- https://github.com/trending/typescript?since=weekly
- https://github.com/trending/javascript?since=weekly
- Chinese-community signal: https://github.com/trending?spoken_language_code=zh&since=daily

Velocity labels ("stars today / this week") appear per row — capture them, they are the freshest signal.

## Search API (JSON, use extractMode text, maxChars ≤ 20000)

Unauthenticated limit ≈ 10 req/min, 60 req/h per IP. Batch ≤ 5 parallel. CJK terms must be percent-encoded UTF-8.

### Chinese keywords

- AI 赚钱: `https://api.github.com/search/repositories?q=AI%20%E8%B5%9A%E9%92%B1&sort=stars&order=desc&per_page=10`
- AI 副业: `https://api.github.com/search/repositories?q=AI%20%E5%89%AF%E4%B8%9A&sort=stars&order=desc&per_page=10`
- AI 变现: `https://api.github.com/search/repositories?q=AI%20%E5%8F%98%E7%8E%B0&sort=stars&order=desc&per_page=10`
- Fresh Chinese: `https://api.github.com/search/repositories?q=AI%20%E8%B5%9A%E9%92%B1%20created:%3E2026-01-01&sort=stars&order=desc&per_page=10`

### English keywords

- `https://api.github.com/search/repositories?q=ai%20side%20hustle&sort=stars&order=desc&per_page=10`
- `https://api.github.com/search/repositories?q=make%20money%20with%20ai&sort=stars&order=desc&per_page=10`
- `https://api.github.com/search/repositories?q=ai%20income&sort=stars&order=desc&per_page=10` (large: ~3.6k repos)
- `https://api.github.com/search/repositories?q=passive%20income%20ai&sort=stars&order=desc&per_page=10`
- Fresh: `https://api.github.com/search/repositories?q=ai%20money%20created:%3E2026-03-01&sort=stars&order=desc&per_page=10`

### Verticals

- n8n automation: `https://api.github.com/search/repositories?q=n8n%20workflow%20ai&sort=stars&order=desc&per_page=10`
- Fresh agents: `https://api.github.com/search/repositories?q=ai%20agent%20created:%3E2026-04-01&sort=stars&order=desc&per_page=15`
- Faceless video: `https://api.github.com/search/repositories?q=faceless%20video&sort=stars&order=desc&per_page=10`
- Fresh trading bots: `https://api.github.com/search/repositories?q=ai%20trading%20bot%20created:%3E2026-01-01&sort=stars&order=desc&per_page=10`
- SaaS boilerplates: `https://api.github.com/search/repositories?q=ai%20saas%20boilerplate&sort=stars&order=desc&per_page=10`
- Topic page: `https://github.com/topics/ai-agents?o=desc&s=stars`

### Single-repo metadata

`https://api.github.com/repos/{owner}/{repo}` — use when a search result was truncated before `stargazers_count`; never guess the number.

## Gotchas learned the hard way

- Search API JSON per repo ≈ 6–7KB; `per_page=10` always truncates at 20k chars. Top 1–2 items survive; fetch single-repo metadata for anything else that matters.
- Truncated fetch output spills to a temp log file — do not read it when files are off-limits; re-fetch the specific repo endpoint instead.
- Total `total_count` of a query is itself a signal (e.g. ~300k repos for fresh `ai agent` = flood; ~500 for `faceless video` = niche). Quote it.
- If spawning subagents, embed the constraint block verbatim in every task and ask each to state rate-limit events; their `sessions_history` is the salvage path (step 4).
