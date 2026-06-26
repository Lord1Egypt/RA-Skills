---
name: pinterest-search
description: Search Pinterest for images and pins using keyword queries. Use this skill whenever the user wants to find Pinterest content, images, pins, or visual inspiration by keyword. Triggers on requests like "search Pinterest for X", "find Pinterest images of Y", "get Pinterest results for Z", or any request to look up visual content on Pinterest — even if the user doesn't say "skill".
env:
  - PINTEREST_COOKIE: "Optional: Pinterest cookie string for authenticated search. Empty string for non-authenticated search."
  - T2P_PROXY: "Optional: Proxy URL (e.g., http://127.0.0.1:7890 or socks5://127.0.0.1:1080). If not set, no proxy will be used."
  - T2P_IMAGE_DIR: "Optional: Custom directory for downloaded images (used with --download flag). Default: Windows: %LOCALAPPDATA%/trend2product/images, Linux/macOS: ~/.cache/trend2product/images"
---

# Pinterest Search Skill

Search Pinterest for pins matching a keyword query and return structured JSON results.

## Inputs

| Parameter       | Type | Description |
|-----------------|---|---|
| `query`         | string | Search keywords (e.g. `"minimalist bedroom"`) |
| `numResults`    | number | Number of results to return (default: 10) |
| `cookie`        | string | Pinterest cookie string (optional). **Overrides** `PINTEREST_COOKIE` env var. |
| `proxy`         | string | Proxy URL (e.g. `http://127.0.0.1:7890`). **Overrides** `T2P_PROXY` env var. |
| `--page`        | number | Number of pages to fetch (default: 1). Each page returns ~10 results. |
| `--incremental` | flag   | Only output new results that haven't been cached before |
| `--download`    | flag   | Download images after search using @t2p/image-cache |
| `--output`      | string | Custom output directory for results (default: `results/`) |

## Output Format

Returns a JSON array of pin objects. Results are automatically saved to `results/<query>_<timestamp>_<count>.json`.

```json
[
  {
    "id": "123456789",
    "title": "Minimalist Bedroom Ideas",
    "grid_title": "Clean & Simple Bedroom",
    "description": "A beautifully minimal bedroom with neutral tones.",
    "url": "https://i.pinimg.com/736x/ab/cd/ef/abcdef.jpg",
    "height": 1102,
    "width": 736,
    "link": "https://www.pinterest.com/pin/123456789/",
    "domain": "apartmenttherapy.com",
    "pinner": {
      "username": "someuser",
      "full_name": "Some User"
    }
  }
]
```

## Execution

### Prerequisites

Install [Bun](https://bun.sh) runtime:

```bash
curl -fsSL https://bun.sh/install | bash
```

Install dependencies:

```bash
cd scripts && bun install
```

### Run Scripts

Use the script at `scripts/pinterest_search.ts`. All TypeScript files must be run with **Bun**:

```bash
bun run scripts/pinterest_search.ts
```

### Configuration Tool

Use `scripts/configure.ts` to generate environment variable commands and manage cache:

```bash
# Generate cookie setting command (copy and run the output)
bun run scripts/configure.ts cookie "_auth=xxx;_pinterest_sess=yyy"

# Generate proxy setting command (copy and run the output)
bun run scripts/configure.ts proxy "http://127.0.0.1:7890"

# List cache files
bun run scripts/configure.ts listcache

# Clear cache for specific keyword
bun run scripts/configure.ts clearcache "keyword"

# Clear all cache
bun run scripts/configure.ts clearcache --all
```

**Note:** Cookie and Proxy are only read from environment variables, not from files. Use `--page` parameter to fetch multiple pages of results.

## Usage Notes

- **Runtime**: All TypeScript files must be run with `bun run`
- **Cookie Optional**: Cookie is optional for search requests. Use `configure.ts cookie` to set, or set `PINTEREST_COOKIE` environment variable
- **Proxy Support**: Use `configure.ts proxy` to set, or set `T2P_PROXY` environment variable
- **Pagination**: Use `--page N` to fetch N pages of results. Each page returns approximately 18 results.
- **Results Saved**: Search results are automatically saved to `results/<query>_<timestamp>_<count>.json`
- **Cache & Deduplication**: Search results are automatically cached to `resultscache/<query>_cache.md`. Each Pinterest ID is stored on a separate line for deduplication
- **Incremental Mode**: Use `--incremental` flag to only output results that haven't been seen before
- **Download Mode**: Use `--download` flag to automatically download images after search. Images are cached using `@t2p/image-cache`
- **Image Directory**: Use `T2P_IMAGE_DIR` environment variable to customize where downloaded images are stored (default: `images/`)
- **Cache Management**: Use `configure.ts listcache` to view caches, `configure.ts clearcache` to clear

## Example

All commands use `bun run`:

```bash
# Search for "minimalist bedroom" (non-authenticated, no proxy)
bun run scripts/pinterest_search.ts "minimalist bedroom"

# Set cookie for authenticated search
bun run scripts/configure.ts cookie "your-cookie-string"
bun run scripts/pinterest_search.ts "minimalist bedroom"

# Set proxy
bun run scripts/configure.ts proxy "http://127.0.0.1:7890"
bun run scripts/pinterest_search.ts "minimalist bedroom"

# Incremental search - only output new results not in cache
bun run scripts/pinterest_search.ts "minimalist bedroom" --incremental

# Download images after search
bun run scripts/pinterest_search.ts "minimalist bedroom" --download

# Download images to custom directory (using environment variable)
export T2P_IMAGE_DIR="/path/to/custom/images"
bun run scripts/pinterest_search.ts "minimalist bedroom" --download

# Combined: incremental search with download
bun run scripts/pinterest_search.ts "minimalist bedroom" --incremental --download

# Specify custom output directory
bun run scripts/pinterest_search.ts "minimalist bedroom" --output /path/to/custom/results

# List all cache files
bun run scripts/configure.ts listcache

# Clear cache for specific keyword
bun run scripts/configure.ts clearcache "minimalist bedroom"

# Clear all cache
bun run scripts/configure.ts clearcache --all
```

## Error Handling

| Situation | What to do |
|---|---|
| HTTP 4xx/5xx | Report the status code; Pinterest may be rate-limiting or cookie is invalid |
| Non-JSON response | Cookie may be invalid or expired; try refreshing your Pinterest cookie |
| Empty results | Try broader keywords or check spelling |
| Missing image URL | The pin may be a video pin; `url` will be empty |
