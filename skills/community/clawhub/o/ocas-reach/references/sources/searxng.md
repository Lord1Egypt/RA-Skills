# SearXNG

Open-source metasearch engine running locally. Aggregates results from Google, Brave, DuckDuckGo, Startpage, and 70+ other engines. No API key required.

## Configuration

SearXNG runs as a local service. Set the URL via env var:

```bash
SEARXNG_URL=http://localhost:8888
```

Default base_url in sources.yml is `http://localhost:8888`. Override with `SEARXNG_URL` if running on a different host/port.

## Actions

### `search`
General web search.

```bash
python3 scripts/reach.py query searxng search '{"query": "AAPL earnings Q2 2026", "language": "en", "limit": 10}'
```

Params:
- `query` (string, required) — Search terms
- `language` (string, default: "en") — Language code
- `categories` (string, optional) — Comma-separated: general, news, social media, images, videos, map, files, it, science
- `time_range` (string, optional) — day, week, month, year
- `limit` (int, default: 10) — Max results

### `search_social`
Search social media sources (Reddit, Twitter/X, etc.) via SearXNG's social media category.

```bash
python3 scripts/reach.py query searxng search_social '{"query": "AAPL site:reddit.com", "time_range": "week", "limit": 20}'
```

Params: Same as `search`, but targets social media category by default.

## Use cases

- **Open web search** — General web content when you need more than Wikipedia
- **Social signals** — Search Reddit, Twitter/X, Stocktwits for ticker mentions and sentiment
- **News aggregation** — Search across multiple news engines simultaneously
- **Sentiment research** — Find discussions about companies, products, or topics

## Integration with Rally

Rally uses SearXNG for `social_heat` signal computation:
1. Search `site:reddit.com/r/wallstreetbets {ticker}` for Reddit mentions
2. Search `site:stocktwits.com {ticker}` for Stocktwits mentions
3. Count mentions over time windows (48h vs 30-day baseline)
4. Compute velocity score as social_heat

## Pitfalls

- **Local instance required** — SearXNG must be running locally. If unreachable, the source returns a connection error.
- **Engine availability** — Some search engines may be blocked or return no results depending on the server's IP and configuration.
- **Rate limits** — No published cap, but throttle to <5/sec to avoid overwhelming the instance.
- **Social media coverage** — Social media engines in SearXNG may have limited coverage compared to direct API access. For dedicated Reddit access, use the `reddit` source.
