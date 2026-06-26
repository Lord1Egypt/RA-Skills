---
name: jackett
description: Search torrent indexers with Jackett. Use when the user asks to "search torrents", "search with Jackett", "find releases", "search indexers", "list Jackett indexers", "check Jackett capabilities", "search movie/tv/music/book releases", or mentions Jackett/Torznab-based torrent search.
---

# Jackett Torznab API

Search configured torrent indexers via Jackett's Torznab API.

## Setup

Config (default): `~/.openclaw/credentials/jackett/config.json`

```json
{
  "url": "http://localhost:9117",
  "apiKey": "your-jackett-api-key"
}
```

## Quick Reference

### List Indexers

```bash
# All configured and available indexers
./scripts/jackett-api.sh indexers

# Only configured indexers
./scripts/jackett-api.sh indexers --configured true
```

### Search Releases

```bash
# Search across all configured indexers
./scripts/jackett-api.sh search "ubuntu 24.04"

# Search a specific indexer
./scripts/jackett-api.sh search "dune 2024" --indexer nyaasi

# Increase the output window when needed
./scripts/jackett-api.sh search "dune 2024" --indexer nyaasi --limit 50 --offset 0

# Search with a Jackett filter indexer
./scripts/jackett-api.sh search "openwrt" --indexer "tag:public,lang:en"

# Keep raw XML instead of parsed JSON
./scripts/jackett-api.sh search "foundation s02" --raw
```

### Typed Searches

```bash
./scripts/jackett-api.sh tvsearch --query "The Last of Us" --season 1 --ep 2
./scripts/jackett-api.sh movie --query "Dune Part Two" --year 2024
./scripts/jackett-api.sh music --artist "Daft Punk" --album "Discovery"
./scripts/jackett-api.sh book --title "The Pragmatic Programmer"
```

### Capabilities

```bash
# Inspect search capabilities for an indexer
./scripts/jackett-api.sh caps --indexer nyaasi

# Inspect the aggregate "all" indexer
./scripts/jackett-api.sh caps
```

## Safe Output Defaults

Parsed searches default to `--limit 20` to avoid overwhelming the terminal on very large result sets.

- Increase the window with `--limit N`
- Page forward with `--offset N`
- Prefer `--indexer`, `--cat`, or typed searches such as `tvsearch` and `movie` before raising the limit
- Use `--raw` only when the original XML is required, because it can be much larger than parsed JSON

## Search Rules

When searching for releases, normalize the query before calling Jackett:

- Prefer the English title instead of localized titles
- Prefer scene-style format keywords instead of natural-language descriptions
- Keep the query compact; start with title + year/edition + core format terms, then broaden only if needed

Examples:
- `Avatar` -> `avatar`
- `Avatar: The Way of Water` -> `avatar the way of water`
- `Dolby Vision` -> `dv`
- `Dolby Atmos` -> `atmos`
- `UHD Blu-ray remux` -> `uhd bluray remux`
- `Subtitles included` usually should not be required in the first query unless the indexer is known to tag it consistently

Recommended search pattern:
- Start with `english-title + important format keywords`
- Add year when the title is ambiguous
- Add one codec/source token at a time, such as `2160p`, `web-dl`, `bluray`, `remux`, `x265`, `dv`, `hdr`, `atmos`
- If there are no results, remove lower-priority format tokens before changing the title

## Response Format

Parsed search results are emitted as JSON with a top-level `meta` object and `results` array.

`meta` includes:
- `total`, `offset`, `limit`, `returned`, `truncated`

Each result object includes fields such as:
- `title`, `guid`, `size`, `publish_date`
- `link`, `details`, `download_url`
- `seeders`, `peers`, `grabs`
- `indexer`, `category`
- `imdb`, `tmdb`, `tvdb`

Use `--raw` to keep Jackett's original XML response.
