# Lightpanda Scraper — ClawHub Skill

Fast headless browser web scraping using [Lightpanda](https://github.com/nicholasgasior/lightpanda-browser). 0.5s page loads, 90x faster than Chromium.

## Features

- **Blazing fast** — 0.5s per page vs 45s for Playwright/Chromium
- **Lightweight** — ~100MB binary, ~50MB memory usage
- **No dependencies** — Single binary, no Node.js/Python browser libs needed
- **OSINT-ready** — Link extraction, markdown dumps, JS evaluation
- **Proxy support** — HTTP and SOCKS5 (Tor compatible)
- **CDP server mode** — Programmatic access via Chrome DevTools Protocol
- **MCP integration** — Use as an MCP server for AI agent workflows

## Install

```bash
clawhub install lightpanda-scraper
```

## Usage

```bash
# Basic scrape
python3 scripts/lp-scrape.py https://target.com

# Extract links
python3 scripts/lp-scrape.py https://target.com --links

# Save output
python3 scripts/lp-scrape.py https://target.com --output page.md
```

See SKILL.md for full documentation.
