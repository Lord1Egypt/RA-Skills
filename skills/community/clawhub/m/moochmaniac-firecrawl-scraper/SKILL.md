---
name: firecrawl-scraper
description: Web scraping, crawling, and search via Firecrawl API. Converts web pages to clean markdown/JSON optimized for AI consumption. Use when you need to extract content from websites, crawl entire sites, or search and scrape web results. Handles JavaScript-heavy sites, dynamic content, and provides structured output. 96% web coverage including modern SPAs.
---

# Firecrawl Scraper

Professional web scraping powered by Firecrawl API. Converts websites to clean, AI-ready markdown or structured JSON.

## When to Use

- Extract content from web pages for analysis
- Scrape documentation sites or knowledge bases
- Crawl entire websites systematically
- Search the web and get scraped content
- Parse JavaScript-heavy or dynamic sites
- Convert HTML to clean markdown for LLM processing
- Competitive research or content aggregation

## Quick Start

**Scrape a single page:**
```bash
python3 scripts/scrape.py https://example.com
```

**Crawl a website:**
```bash
python3 scripts/scrape.py --crawl https://docs.example.com --depth 2 --limit 10
```

**Search and scrape:**
```bash
python3 scripts/scrape.py --search "AI agent frameworks" --limit 5
```

**Check crawl status:**
```bash
python3 scripts/scrape.py --crawl-status abc123
```

## Commands

### Scrape (Single Page)

Extract content from a single URL:

```bash
python3 scripts/scrape.py <url> [options]
```

**Options:**
- `--formats markdown,html,screenshot` — Output formats (default: markdown)
- `--full` — Include full page (no main content extraction)
- `--json` — Output raw JSON response

**Examples:**
```bash
# Basic scrape
python3 scripts/scrape.py https://docs.example.com

# Get HTML and markdown
python3 scripts/scrape.py https://site.com --formats markdown,html

# Full page (no content filtering)
python3 scripts/scrape.py https://site.com --full

# JSON output
python3 scripts/scrape.py https://site.com --json
```

### Crawl (Entire Website)

Systematically crawl and scrape multiple pages:

```bash
python3 scripts/scrape.py --crawl <url> [options]
```

**Options:**
- `--depth N` — Maximum crawl depth (default: 2)
- `--limit N` — Maximum pages to crawl (default: 10)
- `--json` — Output raw JSON response

**Examples:**
```bash
# Basic crawl
python3 scripts/scrape.py --crawl https://docs.site.com

# Deep crawl with limit
python3 scripts/scrape.py --crawl https://blog.com --depth 3 --limit 50

# Shallow crawl
python3 scripts/scrape.py --crawl https://site.com --depth 1 --limit 5
```

**Note:** Crawl returns a job ID. Use `--crawl-status` to check progress and retrieve results.

### Search (Web Search + Scrape)

Search the web and get scraped content from results:

```bash
python3 scripts/scrape.py --search <query> [options]
```

**Options:**
- `--limit N` — Number of results (default: 5)
- `--json` — Output raw JSON response

**Examples:**
```bash
# Search and scrape
python3 scripts/scrape.py --search "WordPress security best practices"

# More results
python3 scripts/scrape.py --search "AI agents 2026" --limit 10

# JSON output
python3 scripts/scrape.py --search "casino bonuses" --json
```

### Crawl Status

Check status of a crawl job:

```bash
python3 scripts/scrape.py --crawl-status <job-id>
```

Returns JSON with:
- Status: `scraping`, `completed`, `failed`
- Progress: Pages scraped
- Data: Scraped content (when completed)
- Credits used

## Output Formats

**Markdown** (default): Clean, LLM-ready text with preserved structure
- Headings, links, lists, code blocks maintained
- No HTML noise or styling artifacts
- Perfect for RAG, summarization, analysis

**HTML**: Full HTML source (useful for parsing specific elements)

**Screenshot**: Base64-encoded PNG of rendered page

**JSON**: Structured data extraction (custom schemas supported)

## Features

**Smart Content Extraction:**
- Automatically identifies main content
- Removes navigation, ads, footers
- Preserves document structure

**JavaScript Support:**
- Handles SPAs (React, Vue, Angular)
- Waits for dynamic content to load
- 96% web coverage

**Anti-Bot Handling:**
- Proxy management built-in
- Rate limiting handled automatically
- CAPTCHA avoidance

**Caching:**
- Smart caching reduces credits
- Configurable cache behavior

## API Key Setup

The script looks for the Firecrawl API key in:
1. `workspace/secrets/firecrawl_api_key` (OpenClaw workspace)
2. `secrets/firecrawl_api_key` (relative to current directory)
3. `FIRECRAWL_API_KEY` environment variable

Current key is stored at: `workspace/secrets/firecrawl_api_key`

## Credits & Pricing

- **Scrape**: 1 credit per page
- **Crawl**: 1 credit per page crawled
- **Search**: 1 credit per result scraped
- **Screenshot**: +1 credit
- **Advanced features**: May use additional credits

Free tier: 500 credits  
Paid plans: Starting at $16/month (3,000 credits)

## Use Cases

**Documentation Extraction:**
```bash
python3 scripts/scrape.py --crawl https://docs.framework.com --depth 2 --limit 50
```

**Competitive Research:**
```bash
python3 scripts/scrape.py --search "top casino affiliate sites" --limit 10
```

**Content Migration:**
```bash
python3 scripts/scrape.py https://old-site.com/page1 --formats markdown
```

**News Monitoring:**
```bash
python3 scripts/scrape.py --search "WordPress security updates" --limit 5
```

**Blog Scraping:**
```bash
python3 scripts/scrape.py --crawl https://blog.site.com --depth 1 --limit 20
```

## Tips

- Start with low `--limit` values to test
- Use `--depth 1` for blog homepages (gets all posts)
- `--depth 2-3` for documentation sites
- `--search` is faster than manual crawling for research
- Check `--crawl-status` regularly for long crawls
- Use `--json` for programmatic processing
- Markdown format is best for LLM consumption

## Comparison to Other Tools

**vs web_fetch tool:**
- Firecrawl: Better JS support, cleaner output, handles complex sites
- web_fetch: Faster, simpler, no API credits needed
- Use Firecrawl for: Modern sites, heavy JS, need high-quality markdown
- Use web_fetch for: Simple pages, quick checks, no credit usage

**vs browser tool:**
- Firecrawl: Optimized for scraping, structured output, no browser management
- browser: Full control, visual interaction, debugging
- Use Firecrawl for: Content extraction at scale
- Use browser for: Interactive tasks, testing, visual verification
