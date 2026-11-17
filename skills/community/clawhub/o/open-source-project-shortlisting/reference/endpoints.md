# open-source-project-shortlisting — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**6 endpoints across 2 platform group(s).**

## GitHub (5)

### `github_repo`

- **HTTP:** `GET /github/repo/{owner}/{repo}`
- **What:** Retrieve a GitHub repository. Returns the public details of one GitHub repository, identified by the required `owner` and `repo`. Fields include the full name, description, main language, topics, stars, forks, watchers, open issues, license, default branch and last push time.
- **Params:** `owner` (string, **required**) — Repository owner (user or org login); `repo` (string, **required**) — Repository name

### `github_repo_contributors`

- **HTTP:** `GET /github/repo/{owner}/{repo}/contributors`
- **What:** List a repository's contributors. Lists the contributors to a GitHub repository, identified by the required `owner` and `repo`, ordered by number of contributions. Page with `page` and `per_page` (max 100). Each contributor has their login, id, contribution count, profile URL and account type.
- **Params:** `owner` (string, **required**) — Repository owner (user or org login); `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `repo` (string, **required**) — Repository name

### `github_repo_languages`

- **HTTP:** `GET /github/repo/{owner}/{repo}/languages`
- **What:** Retrieve a repository's language breakdown. Returns the languages detected in a GitHub repository, identified by the required `owner` and `repo`, as language and byte-count pairs sorted by bytes, largest first.
- **Params:** `owner` (string, **required**) — Repository owner (user or org login); `repo` (string, **required**) — Repository name

### `github_repo_releases`

- **HTTP:** `GET /github/repo/{owner}/{repo}/releases`
- **What:** List a repository's releases. Lists the published releases of a GitHub repository, identified by the required `owner` and `repo`. Page with `page` and `per_page` (max 100). Each release has its tag name, title, URL, prerelease flag, publication time and author.
- **Params:** `owner` (string, **required**) — Repository owner (user or org login); `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `repo` (string, **required**) — Repository name

### `github_search_repositories`

- **HTTP:** `GET /github/search/repositories`
- **What:** Search public GitHub repositories. Searches public GitHub repositories with the required GitHub search query `q`. Order with `sort` (`stars`, `forks`, `help-wanted-issues` or `updated`) and `order`, and page with `page` and `per_page` (max 100). The response has `total_count` and items with full name, owner, description, language, stars, forks, topics and license.
- **Params:** `order` (string, optional) — Sort order; `page` (integer, optional) — Page number; `per_page` (integer, optional) — Results per page (max 100); `q` (string, **required**) — GitHub repository search query; `sort` (string, optional) — Sort field

## Web (1)

### `web_scrape`

- **HTTP:** `POST /web/scrape`
- **What:** Scrape a URL into markdown, HTML, links or metadata. Fetches a single public URL and returns clean content in the requested formats (markdown, html, raw_html, links, metadata). The request body IS the ScrapeOption object itself — e.g. {"url": "https://example.com"} — do not wrap it in an extra key. With render=auto the request starts as a fast HTTP fetch and escalates to a real browser when the page is blocked or rendered with JavaScript. only_main_content (default true) strips navigation, headers, footers and other boilerplate before conversion. Only public pages are supported; respect each site's terms of use and robots directives. A handful of popular sites (Amazon, Reddit, Yelp, LinkedIn, and others) already have a dedicated, more reliable endpoint elsewhere in this API — a failed scrape against one of them names it. A Reddit URL that maps onto a dedicated Reddit endpoint (listings, search, comment threads, user and domain pages) is answered by that endpoint instead, and its response is returned as-is in data with an X-Routed-To header; send dedicated=false to always get the scraped page.
- **Params:** `scrapeOption` (object, **required**) — Scrape options
- **REST body:** Send the value of the MCP argument `scrapeOption` directly as the JSON body; do not wrap it in a `scrapeOption` property.
