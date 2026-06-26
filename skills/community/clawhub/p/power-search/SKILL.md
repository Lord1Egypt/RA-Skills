---
name: power-search
description: Self-hosted research tool combining Brave Search API + Browserless content fetching. Search the web with optional full-page content extraction and HTML parsing.
version: 2.0.0
author: Kaito
license: MIT
metadata:
  requires:
    - docker
    - node
    - npm
  binaries:
    - search
keywords:
  - search
  - research
  - brave
  - browserless
  - web-scraping
  - cli
  - telegram
---

# Power Search

Self-hosted web research tool combining Brave Search API and Browserless for content fetching. Search quickly, fetch full content optionally, extract structured data from HTML.

## Features

- **Fast search:** Brave Search API (10 results in <1s)
- **Content fetching:** Browserless headless browser for full-page extraction
- **HTML parsing:** Extract clean text from web pages
- **CLI interface:** Simple command-line tool
- **Telegram integration:** Ready for OpenClaw routing
- **Offline-capable:** Local Browserless, no cloud dependencies

## Installation

```bash
clawhub install power-search
```

Or manually:
```bash
git clone https://github.com/yourusername/power-search.git
cd power-search
npm install
```

## Setup

### 1. Docker & Browserless

```bash
# Install Docker
sudo apt-get install docker.io docker-compose

# Start Browserless container
docker run -d --name browserless --restart unless-stopped \
  -p 3000:3000 browserless/chrome:latest
```

### 2. Brave Search API Key

Get a free key from [search.brave.com](https://api.search.brave.com/res/v1/):
- 100 free queries/day
- Set environment variable: `export BRAVE_API_KEY=your_key_here`

### 3. Configuration (Optional)

Create `.env` in the skill directory:
```bash
BRAVE_API_KEY=your_key_here
BROWSERLESS_HOST=http://localhost
BROWSERLESS_PORT=3000
```

## Usage

### Search Only

```bash
search "nodejs frameworks"
search "machine learning" --limit 20
```

### Search + Fetch Content

```bash
search "nodejs express" --fetch
search "rust web frameworks" --fetch --limit 5
```

### Verbose Mode

```bash
search "web scraping" --fetch --verbose
```

### Options

- `--fetch` — Fetch full content from top results
- `--limit N` — Number of results (default: 10, max: 20)
- `--timeout MS` — Timeout in milliseconds (default: 10000)
- `--verbose` — Show detailed logging

## Output

### Search Results
```
=== Search Results for "nodejs frameworks" ===

[1] The 5 Most Popular Node.js Web Frameworks in 2025 - DEV Community
    https://dev.to/leapcell/the-5-most-popular-nodejs-web-frameworks-in-2025-12po
    Nest.js is a framework known for building scalable and efficient Node.js...

[2] Express - Node.js web application framework
    https://expressjs.com/
    Fast, unopinionated, minimalist web framework for Node.js...

...
```

### With Content Fetch
```
📄 Content from "nodejs express"

[1] Express - Node.js web application framework
    URL: https://expressjs.com/
    Content:
    Express - Node.js web application framework Getting started...
```

## API (Programmatic Usage)

```javascript
const BraveSearch = require('./scripts/brave-search');
const Browserless = require('./scripts/browserless');

const brave = new BraveSearch('your_api_key');
const results = await brave.search('nodejs', 10);

const browserless = new Browserless('http://localhost', 3000);
const content = await browserless.fetchContent('https://example.com');
```

## Telegram Integration

Power Search is OpenClaw-ready. Once registered:

```
/search artemis 2
/search machine learning --fetch --limit 5
```

Results post directly to Telegram with formatted output.

## Architecture

```
search/
├── scripts/
│   ├── search.js              # Main CLI entry point
│   ├── search-runner.js       # JSON output runner
│   ├── telegram-handler.js    # Telegram command handler
│   ├── brave-search.js        # Brave API wrapper
│   └── browserless.js         # Browserless wrapper
├── package.json
├── SKILL.md                   # This file
└── openclaw.json              # OpenClaw manifest
```

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Search | <1s | Brave API is very fast |
| Fetch | 2-10s | Depends on page complexity |
| Extract | <500ms | HTML parsing + text cleanup |

## Limitations

- Some sites block headless browsers (Cloudflare, etc.)
- JavaScript-heavy sites may not render full content
- Brave Search free tier: 100 queries/day
- HTML extraction is basic (good for text, may miss complex layouts)

## Troubleshooting

### Browserless not running
```bash
docker ps | grep browserless
docker start browserless
docker logs browserless
```

### Rate limit exceeded
Wait 24 hours or upgrade to Brave's paid plan.

### Slow results
- Reduce `--limit` to fetch fewer results
- Increase timeout: `--timeout 30000`
- Check Docker memory: `docker stats browserless`

## Future Enhancements

- AI summaries (Claude/GPT integration)
- Research chains (auto follow-ups)
- Result caching
- Advanced exports (PDF, HTML with styling)
- Saved searches & monitoring

## License

MIT

## Author

Kaito - Digital Assistant
