# Web Scraping & Browsing

## Tools (in order of preference)
1. **web_fetch** — Lightweight URL content extraction (markdown/text)
2. **web_search** — Brave Search API for discovery
3. **browser** — Full browser automation (Playwright)
4. **exec + curl** — Raw HTTP requests

## web_fetch (Preferred for Content)
- Extracts readable content as markdown or text
- Use for articles, docs, pages that don't need interaction
- `maxChars` to limit output

## web_search (Discovery)
- Brave Search API
- Returns titles, URLs, snippets
- Use for finding information before fetching

## browser (Full Automation)
- Use when JavaScript rendering needed
- Use when interaction required (clicks, forms, login)
- Use when page requires complex navigation
- Snapshot → identify elements → act

### Browser Workflow
1. `browser open url` — Navigate to page
2. `browser snapshot` — Get page structure
3. `browser act click/type/fill` — Interact
4. `browser screenshot` — Visual capture
5. `browser console` — Debug JS

## Scraping Ethics
- Respect robots.txt
- Don't overload servers (add delays)
- Cache results to avoid re-fetching
- Use APIs when available over scraping

## Common Patterns
```bash
# Fetch page content
curl -s "https://example.com" | head -50

# Search for info via CLI or tool
web_search query="topic" count=5

# Full browser automation
browser open url="https://app.example.com"
browser snapshot
browser act kind=fill ref="e42" text="search term"
browser act kind=click ref="e58"
```

## Data Extraction
- Parse HTML with BeautifulSoup (Python)
- Regex for simple patterns
- JSON APIs are always preferred over HTML scraping
- Save extracted data to workspace files
