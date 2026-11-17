# private-web-search-searchxng

> Self-hosted private web search using SearXNG — privacy-respecting metasearch for AI agents, no tracking, no paid APIs.

[![AI Agent Skill](https://img.shields.io/badge/AI%20Agent-Skill-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.3.2-green)]()
[![Bash](https://img.shields.io/badge/Shell-Bash-yellow)]()

Run your own SearXNG instance and get JSON search results from Bing, GitHub, Stack Overflow and more — without leaking queries to commercial search/tracking APIs.

## Install

### Via pipeline (GitHub → npx skills)

```bash
npx skills add adelpro/private-web-search-searchxng
```

### Manual

```bash
cp -r private-web-search-searchxng ~/.hermes/skills/
```

## Setup (SearXNG container)

```bash
# Start (or restart a stopped container)
docker start searxng

# Or fresh start
docker run -d --name searxng -p 8080:8080 -e BASE_URL=http://localhost:8080/ --restart unless-stopped searxng/searxng

# Enable JSON API (only needed once)
docker exec searxng sed -i 's/  formats:/  formats:\n    - json/' /etc/searxng/settings.yml
docker restart searxng
```

## Usage

```bash
# Recommended: combined engines (Bing + GitHub + Stack Overflow)
curl -s "http://localhost:8080/search?q=python&format=json&engines=bing,github,stackoverflow&num_results=10"

# Helper script
./scripts/search.sh "your query" 5
```

### Environment variables

- `SEARXNG_PORT` (8080) — container port
- `SEARXNG_HOST` (localhost) — server host
- `SEARXNG_FORMAT` (json) — response format

SearXNG enables 85 engines by default but most are rate-limited/blocked. Bing is the most reliable; Google, DuckDuckGo and Startpage are typically blocked (CAPTCHA/403). Engine status changes often — test with `num_results=5` before heavy use.

## Requirements

- Node.js 18+ (helper script uses curl + jq)
- Docker (for the SearXNG container)
- curl, jq

## Related Skills

- **web-search** — General web search
- **search-cluster** — Aggregated Google/Wikipedia/Reddit search

## Credits

SearXNG is a free, privacy-respecting metasearch engine. No OpenClaw branding implied — this is a generic agent skill.
