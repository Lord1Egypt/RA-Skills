# Search Surfaces

Endpoint details, query strategies, and response parsing for each discovery surface.

## 1. MCP Registry

Official registry for Model Context Protocol servers.

### Endpoint

```
GET https://registry.modelcontextprotocol.io/v0/servers?search={query}&limit={limit}
```

No authentication required. Rate limit: reasonable (no published cap; back off on 429).

### Query strategy

- Use 1-4 word capability keywords, not full sentences
- Try the primary term first, then broaden: `"calendar"` before `"schedule management"`
- If zero results, try synonyms or related terms

### Response parsing

JSON array of server objects. Extract:
- `name` -- server name
- `description` -- capability summary
- `url` or `homepage` -- source URL
- `npm_package` or `pypi_package` -- install target
- `license` -- license type
- `version` -- latest version

### Trust signals

- Official servers (maintained by modelcontextprotocol org) are highest trust
- Check `verified` or `official` flags if present
- GitHub star count from linked repo

### Resource ID format

`mcp:{server-id}` (e.g., `mcp:io.github.anthropics/mcp-server-git`)

---

## 2. ClawHub

Platform skill registry with vector search.

### Endpoint

```
GET https://clawhub.ai/api/v1/skills?search={query}&limit={limit}
```

No authentication required for search. Vector search (embedding-based, not keyword).

Rate limits can occur. Retry on failure (usually succeeds on 2nd or 3rd attempt).

### Fallback: web search

If the API is unavailable or returns errors, fall back to:
```
web_search: clawhub.ai {capability} skill
```
Then fetch the skill page directly and parse metadata from the page.

### Supplementary: h4gen FTS index

A third-party full-text search index covering 240,000+ skills (broader than ClawHub alone):
```
GET https://skillsearch-api.hagen-hoferichter.workers.dev/search?q={query}
```
No auth required. Note: queries are sent to a publisher-controlled endpoint. Do not include secrets or PII in queries. Use as a supplement when ClawHub's vector search returns few results.

### Query strategy

- Use natural language descriptions: `"manage calendar events and scheduling"`
- Vector search handles semantic matching, so be descriptive
- Filter results: skip skills flagged as "suspicious" by platform security scan

### Response parsing

JSON array of skill objects. Extract:
- `slug` -- unique identifier
- `name` -- display name
- `description` -- capability summary
- `version` -- latest version
- `downloads` -- install count (treat with skepticism per known manipulation vulnerabilities)
- `stars` -- community signal
- `license` -- license type
- `securityScan` -- Platform security scan and VirusTotal results

### Trust signals

- platform security scan result (Benign / Suspicious / Malicious)
- VirusTotal scan result
- Author account age and other published skills
- Do NOT rely on download count alone as primary trust signal

### Resource ID format

`skill:{slug}` (e.g., `skill:tavily-web-search`)

---

## 2.5. Skills.sh (Vercel)

Separate skill index from ClawHub. Different catalog, different install commands.

### Endpoint

```bash
npx skills find {capability keywords}
npx skills add {owner/repo@skill}    # install
```

No API endpoint exposed. CLI only via npx.

### Query strategy

- Use the same queries as ClawHub but expect different results
- Skills.sh indexes GitHub repos directly (from `vercel-labs/skills`)
- Results include the package source and install string -- keep these attached to every recommendation

### Trust signals

- Package source visibility (GitHub repo link)
- Same red/green flags as ClawHub skills

### Critical rule

ClawHub and Skills.sh install commands are NOT interchangeable. A `clawhub install` slug will fail on a Skills.sh-only skill and vice versa. Always pair the source registry with the install command.

---

## 3. GitHub

Broad search across repositories for skills, MCPs, and API wrappers.

### Endpoint

```
web_search: github.com {capability} MCP server
web_search: github.com {capability} agentskills.io skill
web_search: github.com {capability} free API
```

Use web search tool, not GitHub API (no auth token assumed).

### GitHub Code Search technique (from Agnxi)

Search for SKILL.md files directly to find skills not yet published to ClawHub:
```
web_search: github.com filename:SKILL.md {capability keywords}
```
This surfaces skills in personal repos, forks, and unpublished packages that ClawHub's registry doesn't index. Agnxi.com uses this technique (via GitHub Code Search API with auth) to build its directory of 5000+ skills.

### Query strategy

- Search for MCP servers first (highest value): `github.com {term} MCP server`
- Then skills: `github.com {term} agentskills.io skill SKILL.md`
- Then API wrappers: `github.com {term} API client free`
- Add `language:python` or `language:typescript` if the user has a runtime preference

### Response parsing

From search results, extract:
- Repository name and URL
- Description from search snippet
- Star count (visible in search results)
- Last update date
- License (if visible)

For promising results, fetch the README via `web_fetch` to get:
- Installation instructions
- Whether an API key is required
- Rate limits or pricing tier

### Trust signals

- Star count (>100 is meaningful; >1000 is strong)
- Recent activity (last commit within 6 months)
- License present and permissive
- README quality and completeness

### Resource ID format

`gh:{owner}/{repo}` (e.g., `gh:anthropics/mcp-server-git`)

---

## 4. Public API Directories

Catalogs of free and open APIs.

### Sources

Search these in order:

1. **public-apis GitHub list**
   ```
   web_fetch: https://raw.githubusercontent.com/public-apis/public-apis/master/README.md
   ```
   Grep for the capability keyword in the fetched markdown. This is a curated list with auth requirements, HTTPS support, and CORS noted per entry.

2. **Free API lists via web search**
   ```
   web_search: free {capability} API no key required 2025 2026
   ```

3. **RapidAPI free tier**
   ```
   web_search: rapidapi free {capability} API
   ```

### Query strategy

- Lead with the specific data type or action: `"weather data"` not `"weather"`
- Add `"free"` and `"no API key"` to prioritize zero-cost options
- Cross-reference with the public-apis list for curated quality

### Response parsing

For each API found, extract:
- Name and documentation URL
- Auth requirement (none / API key / OAuth)
- Rate limits (requests per day/month)
- HTTPS support
- Response format (JSON / XML / other)

### Trust signals

- Listed in public-apis curated repo (high trust)
- Official documentation site exists
- HTTPS enforced
- Stable (>1 year old, still responding)

### Resource ID format

`api:{name-slug}` (e.g., `api:open-meteo`)

---

## 5. PulseMCP Directory (supplementary)

Community-maintained MCP server directory with 11,000+ entries.

### Endpoint

```
web_search: pulsemcp.com {capability}
```

Then `web_fetch` the relevant category or search results page.

### Query strategy

- Use as a supplement to the official MCP Registry, not a replacement
- Useful for finding niche or very new MCP servers not yet in the official registry

### Trust signals

- Classification field: `official` > `reference` > `community`
- Estimated weekly visitors (higher = more validated)
- Release date (older = more stable)

### Resource ID format

`pmcp:{server-name}` (e.g., `pmcp:sequential-thinking`)

---

## 6. Curated Directories (supplementary)

When primary surfaces don't yield strong results, try these curated lists:

- `https://clawskills.sh` -- curated, filtered subset of ClawHub with category navigation
- `https://github.com/VoltAgent/awesome-agent-skills` -- 5,200+ skills, filtered and categorized
- `https://github.com/punkpeye/awesome-mcp-servers` -- curated MCP server list

Search via `web_fetch` of the raw README and grep for capability keywords.

---

## 7. Agnxi.com (supplementary)

Curated directory of AI agent tools, MCP servers, and skills.

### Endpoint

Sitemap crawl (always current, no API key):
```
web_fetch: https://agnxi.com/sitemap.xml
```
Parse the XML for `<loc>` elements and filter URLs containing capability keywords. This is how the `doanbactam/agnxi-search-skill` works internally.

Alternatively:
```
web_search: site:agnxi.com {capability keywords}
```

### Query strategy

- Use broad category terms: "browser automation", "pdf parsing", "postgres mcp"
- If specific terms yield nothing, broaden: "PDF" instead of "PyPDF2"
- Returns direct URLs to tool pages

### Trust signals

- Curated directory (not user-submitted)
- Cross-reference results with GitHub repos for star counts and activity

### Resource ID format

`agnxi:{tool-name}` (e.g., `agnxi:browser-use`)

---

## Pre-search: mcporter check

Before searching for MCP servers externally, check what's already connected:

```bash
mcporter list                         # list configured servers
mcporter list <server> --schema       # inspect available tools on a server
```

If mcporter is not installed: `npx -y mcporter` as fallback.

If an existing server already provides the needed capability, report it immediately without searching further.

---

## Rate limiting and error handling

- If any surface returns a rate limit error (429), back off and note in results: "Surface temporarily unavailable, results may be incomplete."
- If a surface is completely unreachable, skip it and note which surfaces were searched.
- Never block the entire search on one surface's failure. Return partial results.
- Log all surface errors to `decisions.jsonl`.

## Cache key generation

Cache key = lowercase, sorted, deduplicated keywords from the query + surface filter.

Example: `multipass.search "calendar event scheduling" --surface mcps` -> cache key: `calendar|event|mcps|scheduling`

Cache hit: if a matching key exists in `search_cache.jsonl` with `timestamp` < 7 days old, return cached results with a note: "Results from cache ({N} days old). Run with --refresh to search again."
