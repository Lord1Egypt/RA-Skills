# SearXNG Search Skill for Clawdbot

Privacy-respecting web search using your local SearXNG instance. This version is **zero-dependency**, requiring only a standard Python 3 installation.

## Prerequisites

**This skill requires a running SearXNG instance.**

If you don't have SearXNG set up yet:

1. **Docker (easiest)**:

   ```bash
   docker run -d -p 8080:8080 searxng/searxng
   ```

2. **Manual installation**: Follow the [official guide](https://docs.searxng.org/admin/installation.html)

3. **Public instances**: Use any public SearXNG instance (less private)

## Features

- 🔒 **Privacy-focused**: All queries go through your local SearXNG instance.
- 🛠️ **Zero Dependencies**: Uses only Python built-in libraries (`urllib`, `json`, `ssl`).
- 🌐 **Multi-engine**: Aggregates results from Google, Bing, DuckDuckGo, and more.
- 📰 **Multiple Categories**: Supports Web, IT, Science, News, and Images.
- 📄 **Clean Output**: Plain-text formatting optimized for AI/LLM readability.
- 🚀 **Fast JSON Mode**: Direct programmatic access for scripts.

## Quick Start

### Basic Search

```
Search "python asyncio tutorial"
```

### Advanced Usage

```
Search "climate change" with 20 results
Search "cute cats" in images category
Search "breaking news" in news category from last day
```

## Configuration

**You must configure your SearXNG instance URL before using this skill.**

### Set Your SearXNG Instance

Configure the SearXNG instance URL using the configuration file:

**Configuration file** (`searxng.ini`):

```ini
[searxng]
url = http://your-searxng-instance.com:port
```

Note: If the configuration file does not exist or is missing required settings, the script will automatically create a default configuration file and prompt you to modify it.

## Direct CLI Usage

You can also use the skill directly from the command line:

```bash
# Basic search
python3 scripts/searxng.py search "query"

# More results (Top 20)
python3 scripts/searxng.py search "query" -n 20

# Category search
python3 scripts/searxng.py search "query" --category it

# JSON output
python3 scripts/searxng.py search "query" --format json

# Time-filtered news
python3 scripts/searxng.py search "AI news" --category news --time-range day
```

## Available Categories

- `general` - General web search (default)
- `images` - Image search
- `videos` - Video search
- `news` - News articles
- `map` - Maps and locations
- `music` - Music and audio
- `files` - File downloads
- `it` - IT and programming
- `science` - Scientific papers and resources

## Time Ranges

Filter results by recency:

- `day` - Last 24 hours
- `week` - Last 7 days
- `month` - Last 30 days
- `year` - Last year

## Examples

### Web Search

```bash
python3 ~/.openclaw/workspace/skills/searxng/scripts/searxng.py search "rust programming language"
```

### Image Search

```bash
python3 ~/.openclaw/workspace/skills/searxng/scripts/searxng.py search "sunset photography" --category images -n 10
```

### Recent News

```bash
python3 ~/.openclaw/workspace/skills/searxng/scripts/searxng.py search "tech news" --category news --time-range day
```

### JSON Output for Scripts

```bash
python3 ~/.openclaw/workspace/skills/searxng/scripts/searxng.py search "python tips" --format json | jq '.results[0]'
```

## SSL/TLS and Security

This skill is designed for local environments:

- **Self-signed Certificates**: The script automatically bypasses SSL verification (`ssl.CERT_NONE`) to ensure compatibility with local HTTPS instances.
- **No External Calls**: Aside from your SearXNG instance, no data is sent to third-party APIs.

## Troubleshooting

### Connection Issues

If you get connection errors:

1. **Check your SearXNG instance is running:**

   ```bash
   # Use your configured URL from searxng.ini
   curl -k http://your-searxng-instance.com:port
   ```

2. **Verify the URL in your searxng.ini config file**

3. **Check SSL certificate issues**

### No Results

If searches return no results:

1. Check your SearXNG instance configuration
2. Ensure search engines are enabled in SearXNG settings
3. Try different search categories

## Privacy Benefits

- **No tracking**: All searches go through your local instance
- **No data collection**: Results are aggregated locally
- **Engine diversity**: Combines results from multiple search providers
- **Full control**: You manage the SearXNG instance

## About SearXNG

SearXNG is a free, open-source metasearch engine that respects your privacy. It aggregates results from multiple search engines while not storing your search data.

Learn more: https://docs.searxng.org/

## License

This skill is part of the Clawdbot ecosystem and follows the same license terms.