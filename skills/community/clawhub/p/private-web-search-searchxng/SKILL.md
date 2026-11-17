---
name: private-web-search-searchxng
slug: private-web-search-searchxng
version: 1.3.2
description: |
  Self-hosted private web search using SearXNG. Use when privacy is important, external search APIs are blocked or paid, or you need search without tracking.
triggers:
  - private search
  - searxng
  - self hosted search
  - privacy search
  - search without tracking
metadata:
  openclaw:
    requires:
      bins: ["docker", "curl", "jq"]
      env: []
---

# Private Web Search (SearXNG)

Privacy-respecting, self-hosted metasearch engine for AI agents.

## Quick Setup

```bash
# If container exists but stopped:
docker start searxng

# Or fresh start:
docker run -d --name searxng -p 8080:8080 -e BASE_URL=http://localhost:8080/ --restart unless-stopped searxng/searxng

# Enable JSON API (only needed once)
docker exec searxng sed -i 's/  formats:/  formats:\n    - json/' /etc/searxng/settings.yml
docker restart searxng

# Verify
curl -s "http://localhost:8080/search?q=test&format=json&engines=bing&num_results=1" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Results: {d.get('number_of_results',0)}\")"

## Usage

### Basic Search

```bash
curl -sL "http://localhost:8080/search?q=YOUR_QUERY&format=json" | jq '.results[:10]'
```

### Using the Helper Script

```bash
./scripts/search.sh "openclaw ai" 5
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| SEARXNG_PORT | 8080 | Container port |
| SEARXNG_HOST | localhost | Server host |
| BASE_URL | http://localhost:8080 | Public URL |

## Working Engines (Tested June 2026)

**85 engines enabled** by default, but most major engines are blocked or rate-limited:

| Engine | Status | Results | Notes |
|--------|--------|---------|-------|
| Bing | Working | 10-30 | Most reliable, 282K+ total |
| GitHub | Working | 30 | Package/repo search |
| Stack Overflow | Working | 10 | Q&A search |
| Wikipedia | Sometimes | 1 | Varies by query |
| Google | Blocked | 0 | CAPTCHA, "access denied" |
| DuckDuckGo | Blocked | 0 | Rate limited |
| Startpage | Blocked | 0 | CAPTCHA |
| Qwant | Blocked | 0 | Rate limited |

### Multi-Engine Queries (Recommended)

Combine multiple working engines for best results:

```bash
# Get combined results from Bing + GitHub + Stack Overflow
curl -s "http://localhost:8080/search?q=python&format=json&engines=bing,github,stackoverflow&num_results=10"
```

This returns 40+ results with diverse sources (web, code, Q&A).

### Why Most Engines Fail

- **Google/DuckDuckGo**: Detect automated traffic, return CAPTCHA/403 errors
- **Public instances**: Get IP-banned quickly due to high volume
- **Self-hosted**: Slightly better but still rate-limited
- **Bing**: Most permissive, works reliably

**Note:** Engine status changes frequently. Test with `&num_results=5` to verify before heavy use.

## Management

```bash
docker start searxng   # Start
docker stop searxng    # Stop
docker logs searxng    # View logs
docker rm searxng -f   # Remove
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results | Check `docker logs searxng` |
| 403 Forbidden | Enable JSON format (step 2) |
| Connection refused | Run `docker start searxng` |
| "container name already in use" | Container stopped, run `docker start searxng` |
| Most engines return 0 | Engine rate-limiting — use Bing |
