---
name: hotnews
description: |
  CLI tool to fetch trending news and hot topics from 8 sources across Chinese platforms and GitHub. Returns structured news items with titles, URLs, and metadata.

  USE FOR:
  - Fetching trending/hot news from Chinese and international platforms
  - Monitoring hot topics across social media, tech, finance, and news sites
  - Getting structured news data as JSON for further processing
  - Listing available news sources

  Requires npm install.
allowed-tools:
  - Bash(hotnews *)
  - Bash(npx hotnews *)
---

# hotnews CLI

Fetch trending news and hot topics from 8 sources. Returns news items with title, URL, hot metric, and rank.

Run `hotnews --help` for usage details.

## Workflow

Follow this pattern:

1. **List** - Don't know what sources are available? List them first.
2. **Fetch** - Know the source? Fetch news directly.
3. **JSON** - Need structured data? Add `--json` for machine-readable output.

| Need | Command | When |
|---|---|---|
| See all sources | `hotnews list` | Don't know source names |
| Get news | `hotnews <source>` | Know the source, want readable output |
| Get news as JSON | `hotnews <source> --json` | Need structured data for processing |
| Control item count | `hotnews <source> --limit N` | Want specific number of results (1-50, default 10) |

## Commands

### list

List all available sources.

```bash
hotnews list
```

### Fetch a source

```bash
hotnews baidu
hotnews baidu --json
hotnews weibo --limit 5
hotnews douyin -l 15 --json
```

### Options

| Flag | Short | Description |
|---|---|---|
| `--json` | | Output as JSON |
| `--limit N` | `-l N` | Number of items to return (default: 10, max: 50) |

Output fields (JSON mode):
- `title` - News headline
- `url` - Link to the article
- `hot` - Popularity metric, e.g. "871 stars today", "5.3k" (optional)
- `rank` - Position in the ranking (1-based)

## Sources

8 source endpoints:

| Platform | ID | Description |
|---|---|---|
| Baidu | `baidu` | Baidu real-time search trends |
| Weibo | `weibo` | Weibo real-time trending topics |
| Douyin | `douyin` | Douyin real-time trending |
| Hupu | `hupu` | Hupu street hot posts |
| 36Kr | `kr36` | 36Kr tech news flashes |
| Zhihu | `zhihu` | Zhihu trending questions |
| Juejin | `juejin` | Juejin developer community hot articles |
| GitHub | `github` | GitHub trending open source projects today |

## Source Selection Guide

| Category | Recommended Sources |
|---|---|
| General News | `baidu`, `weibo`, `toutiao` |
| Social/Trending | `weibo`, `douyin`, `zhihu` |
| Tech/Developer | `juejin`, `github`, `kr36` |
| Sports/Lifestyle | `hupu` |

## Working with Results

```bash
hotnews baidu --json | jq '.[].title'
hotnews baidu --json --limit 5
hotnews weibo --json | jq '.[] | "\(.rank). \(.title) \(.hot // "")"'
hotnews github --json | jq '.[] | "\(.title) - \(.hot)"'
```
