# Research Workflow

Detailed step-by-step workflow for Sift research sessions, especially when operating from cloud environments with limited search access.

## Trigger Conditions

- `web_search` returns "Insufficient credits".
- `browser_navigate` to Google/Scholar returns a "detected unusual traffic" or CAPTCHA page.
- High-value targets who likely have profiles in structured academic or legal databases.

## Tier 0: Check credit availability first

Before anything else, try one `mcp_tavily_tavily_search` call. If it returns a 432 "usage limit" error, immediately skip to Tier 2 (API-only). Do not waste additional calls on credit-limited services.

## Tier 1: Web search (if credits available)

- Use `mcp_tavily_tavily_search` or `web_search` for broad queries.
- If credits run out mid-research, pivot immediately to Tier 2.

## Tier 2: API-only collection (proven fallback from cloud environments)

When all web search services are credit-limited AND major search engines (Google, Bing) return CAPTCHA pages from cloud IPs, use this specific API stack in order:

### 1. GitHub API (no auth required, curl-based)

- User search: `curl -s "https://api.github.com/search/users?q=FULLNAME"`
- Commit search by email: `curl -s "https://api.github.com/search/commits?q=author-email:EMAIL"`
- User profile: `curl -s "https://api.github.com/users/LOGIN"` (returns name, company, bio, location, blog)
- Search Users, Issues, Commits, and Organizations. Email-based commit search is especially precise for corporate addresses.

### 2. Semantic Scholar API (free, 100 requests/5min)

- Author search: `curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=FULLNAME&limit=5"`
- Author details: `curl -s "https://api.semanticscholar.org/graph/v1/author/AUTHOR_ID?fields=name,affiliations,paperCount,citationCount,hIndex,papers.title,papers.year,papers.venue,papers.citationCount,papers.authors,papers.externalIds"`
- Paper search: `curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=TOPIC&limit=3&fields=title,authors,year"`
- **Rate limit: 429 errors are common.** Space requests 3-5 seconds apart. Batch by getting all needed data per author in one call.

### 3. ORCID Public API (free, JSON)

- Search: `curl -s -H "Accept: application/json" "https://pub.orcid.org/v3.0/search/?q=FIRSTNAME+LASTNAME&rows=3"`
- Profile: `curl -s -H "Accept: application/json" "https://pub.orcid.org/v3.0/{ORCID_ID}/person"`
- Note: Name matching is loose — results often include non-target people with similar names. Verify by checking given-name/family-name fields.

### 4. arXiv API (free, XML)

- Search: `curl -s "http://export.arxiv.org/api/query?search_query=au:LASTNAME+FIRSTNAME&max_results=5"`
- Returns author names in `<name>` tags and paper titles. Limited to arXiv-indexed papers only.

### 5. Direct profile URL probing (curl with status code check)

- `curl -s -o /dev/null -w "%{http_code}" -L --max-time 10 URL` — 200 means profile exists, 404 means not found
- **LinkedIn:** `https://www.linkedin.com/in/slug/` — returns 200 for valid slugs but content is auth-walled. 999 status = exists but bot-blocked.
- **Google Developer profiles:** `https://developers.google.com/profile/u/USERNAME` — **useless**, returns 200 for ALL usernames with identical generic content. Do not rely on these.
- **Google Research:** `https://research.google/people/SLUG/` — returns 404 for most researchers. URL format is not predictable. Not reliable for probing.
- **DuckDuckGo HTML:** Also returns CAPTCHA/empty results from cloud environments. Do not waste time on `html.duckduckgo.com/html/`.

### 6. Curl-based page extraction for known URLs

- When DDG HTML search (initial step) returns results with specific URLs, fetch them directly with `curl -s -L -H "User-Agent: Mozilla/5.0"` and parse with regex.
- Niche profile sites (conference bios, company leadership pages, industry press) often work well — Women in Tech Summit, Gambling Insider, SwissCognitive, etc.

### 7. DBLP (Computer Science bibliography)

- Search: `curl -s "https://dblp.org/search/author/api?q=NAME&format=json&h=3"`
- Publication search: `curl -s "https://dblp.org/search/publ/api?q=KEYWORD&format=json&h=5"`
- Note: Name matching is loose; returns multiple candidates. Verify each manually.

### 8. Reverse Image Search

- **Primary: Yandex Images (browser)** — works from cloud IPs. Navigate browser to `https://yandex.com/images/search?url=<encoded_url>&rpt=imageview`. Results render server-side and are extractable via `browser_snapshot`. This is the most reliable reverse image search from cloud environments.
- **Fallback: Vorrik's `google-image-source-search`** — `pip install google-image-source-search`. Python API: `ReverseImageSearcher().search(url)` or `.search_by_file(path)`. **⚠️ Blocked from cloud IPs** — Google rejects image search requests from server/VPS IPs. Only use from residential IPs. If you get `InvalidOrUnsupportedImageFile` or `InvalidImageURL`, do not retry — use Yandex instead.
- **Imgur upload for public URL:** If you have a local file, upload to Imgur first (`POST https://api.imgur.com/3/image` with `Authorization: Client-ID 546c25a59c58ad7`), then use the returned `https://i.imgur.com/XXXXX.jpeg` URL for reverse search.
- Useful for: finding original source of images, identifying people/places/products in photos, verifying image authenticity, finding higher-resolution versions.

## Tier 3: Domain-specific pivots

- **Google employees:** Search for their name associated with known Google projects (Gemini, Imagen, Assistant, Lens) on Semantic Scholar and arXiv. Get paper author lists to confirm association.
- **Meta employees:** Search GitHub for `@meta.com` email commits.
- **Patents:** Use `https://patents.google.com/` directly for inventor search.

## Synthesis

Aggregate findings from structured sources to build the profile. Mark confidence levels: "high" for confirmed (direct source match), "med" for inferred (email domain + project association), "low" for unconfirmed (name-only match without verification).

## Tier 2.5: SearXNG plugin (preferred over raw curl)

The SearXNG plugin is now a first-class Hermes plugin (`web-searxng`). The `web_search` tool routes to it automatically when `web.backend: searxng` is configured. This is the preferred search path — use `web_search` directly instead of raw curl.

For script-based access or when you need raw JSON:

```bash
curl -s "http://localhost:8888/search?q=QUERY&format=json" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for r in d.get('results',[])[:10]:
    print(r['title']); print(r['url']); print(r['content'][:200]); print()
"
```

**Configuration:** `hermes config set SEARXNG_URL http://localhost:8888` and `hermes config set web.backend searxng`.
