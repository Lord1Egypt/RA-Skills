---
name: lightpanda-scraper
description: Fast headless browser web scraping using Lightpanda (0.5s page loads, 90x faster than Chromium). Perfect for OSINT recon, link extraction, and content scraping. No GPU or heavy dependencies needed.
homepage: https://github.com/nicholasgasior/lightpanda-browser
metadata: {"openclaw":{"emoji":"🐼","requires":{"bins":["python3"]},"install":[{"id":"lightpanda","kind":"manual","label":"Install Lightpanda binary","commands":["curl -L https://github.com/nicholasgasior/lightpanda-browser/releases/latest/download/lightpanda-linux-x86_64 -o ~/.local/bin/lightpanda","chmod +x ~/.local/bin/lightpanda"]}]}}
---

# Lightpanda Scraper — Fast Headless Browser for OSINT

Blazing fast web scraping using Lightpanda, a Zig-based headless browser. **0.5s per page** vs 45s for Chromium/Playwright. Perfect for OSINT recon, link extraction, and content scraping.

## Prerequisites

Install Lightpanda binary:
```bash
mkdir -p ~/.local/bin
curl -L https://github.com/nicholasgasior/lightpanda-browser/releases/latest/download/lightpanda-linux-x86_64 -o ~/.local/bin/lightpanda
chmod +x ~/.local/bin/lightpanda
```

## Quick Start

```bash
# Dump page as markdown
python3 {baseDir}/scripts/lp-scrape.py https://target.com

# Extract all links
python3 {baseDir}/scripts/lp-scrape.py https://target.com --links

# Get raw HTML
python3 {baseDir}/scripts/lp-scrape.py https://target.com --html
```

## Options

- `--links` — Extract and categorize all links from the page
- `--html` — Dump raw HTML instead of markdown
- `--frames` — Include iframe content
- `--js "code"` — Evaluate JavaScript on the page
- `--output FILE` — Save output to file
- `--wait MODE` — Wait condition: `networkidle` (default), `load`, `domcontentloaded`
- `--strip TYPES` — Comma-separated resource types to strip: `js`, `css`, `images`
- `--proxy URL` — Use proxy (e.g., `socks5://127.0.0.1:9050` for Tor)
- `--timeout SECS` — Request timeout (default: 30)
- `--serve --port PORT` — Start CDP server mode
- `--mcp` — Start as MCP server (stdio)

## Use Cases

### OSINT Recon
```bash
# Quick page dump for analysis
python3 {baseDir}/scripts/lp-scrape.py https://target.com > recon.md

# Extract all endpoints from a site
python3 {baseDir}/scripts/lp-scrape.py https://target.com --links | grep -i api

# Crawl with Tor
python3 {baseDir}/scripts/lp-scrape.py https://target.com --proxy socks5://127.0.0.1:9050
```

### Bug Bounty Recon
```bash
# Fast subdomain content grab
for sub in api admin dev staging; do
  python3 {baseDir}/scripts/lp-scrape.py https://$sub.target.com --links 2>/dev/null
done
```

### Content Extraction
```bash
# Save clean markdown
python3 {baseDir}/scripts/lp-scrape.py https://article.com --output article.md

# JavaScript evaluation
python3 {baseDir}/scripts/lp-scrape.py https://app.com --js "document.querySelectorAll('a').length"
```

### CDP Server Mode
```bash
# Start server for programmatic access
python3 {baseDir}/scripts/lp-scrape.py --serve --port 9222
# Then connect with any CDP client
```

## Speed Comparison

| Tool | Page Load | Memory | Binary Size |
|------|-----------|--------|-------------|
| **Lightpanda** | ~0.5s | ~50MB | ~100MB |
| Chromium/Playwright | ~45s | ~500MB | ~300MB |
| curl/wget | ~0.3s | ~5MB | N/A |

Lightpanda gives you Playwright-like page rendering at near-curl speeds. The catch: no complex JS interactions (use Playwright for those).

## Notes

- Lightpanda is in active development; some complex SPAs may not render perfectly
- For authenticated sessions or complex JS interactions, use Playwright instead
- Binary is ~100MB Zig-compiled native code, runs on Linux x86_64
- Supports HTTP/SOCKS5 proxies for Tor or VPN routing
