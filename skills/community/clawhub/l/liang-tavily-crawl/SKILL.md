---
name: tavily-crawl
description: Crawl any website and save pages as local markdown files. Ideal for downloading documentation, knowledge bases, or web content for offline access or analysis.
homepage: https://tavily.com
metadata: {"openclaw":{"emoji":"🕷️","requires":{"bins":["node"],"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---

# Tavily Crawl

Crawl websites to extract content from multiple pages. Ideal for documentation, knowledge bases, and site-wide content extraction.

## Authentication

Get your API key at https://tavily.com and add to your OpenClaw config:

```json
{
  "skills": {
    "entries": {
      "tavily-crawl": {
        "enabled": true,
        "apiKey": "tvly-YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Or set in environment variable:
```bash
export TAVILY_API_KEY="tvly-YOUR_API_KEY_HERE"
```

## Quick Start

### Using the Script

```bash
node {baseDir}/scripts/crawl.mjs "https://docs.example.com"
node {baseDir}/scripts/crawl.mjs "https://docs.example.com" --output ./docs
node {baseDir}/scripts/crawl.mjs "https://example.com" --depth 2 --limit 50
```

### Examples

```bash
# Basic crawl
node {baseDir}/scripts/crawl.mjs "https://docs.example.com"

# Deeper crawl with limits
node {baseDir}/scripts/crawl.mjs "https://docs.example.com" --depth 2 --limit 50

# Save to files
node {baseDir}/scripts/crawl.mjs "https://docs.example.com" --depth 2 --output ./docs

# Focused crawl with path filters
node {baseDir}/scripts/crawl.mjs "https://example.com" --depth 2 \
  --select "/docs/.*" --exclude "/blog/.*"

# With semantic instructions
node {baseDir}/scripts/crawl.mjs "https://docs.example.com" \
  --instructions "Find API documentation" --chunks 3
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--depth <n>` | Crawl depth (1-5) | 1 |
| `--breadth <n>` | Links per page | 20 |
| `--limit <n>` | Total pages cap | 50 |
| `--output <dir>` | Save pages to directory | - |
| `--instructions <text>` | Natural language guidance | - |
| `--chunks <n>` | Chunks per page (1-5, requires instructions) | - |
| `--depth-mode <mode>` | Extract depth: `basic` or `advanced` | `basic` |
| `--select <pattern>` | Regex pattern to include | - |
| `--exclude <pattern>` | Regex pattern to exclude | - |
| `--timeout <sec>` | Max wait time (10-150 seconds) | 150 |
| `--json` | Output raw JSON | false |

## Depth vs Performance

| Depth | Typical Pages | Time |
|-------|---------------|------|
| 1 | 10-50 | Seconds |
| 2 | 50-500 | Minutes |
| 3 | 500-5000 | Many minutes |

**Start with `--depth 1`** and increase only if needed.

## Crawl for Context vs Data Collection

**For agentic use (feeding results into context):** Always use `--instructions` + `--chunks`. This returns only relevant chunks instead of full pages, preventing context window explosion.

**For data collection (saving to files):** Omit `--chunks` to get full page content.

## Tips

- **Always use `--chunks` for agentic workflows** - prevents context explosion when feeding results to LLMs
- **Omit `--chunks` only for data collection** - when saving full pages to files
- **Start conservative** (`--depth 1`, `--limit 20`) and scale up
- **Use path patterns** to focus on relevant sections
- **Always set a `--limit`** to prevent runaway crawls