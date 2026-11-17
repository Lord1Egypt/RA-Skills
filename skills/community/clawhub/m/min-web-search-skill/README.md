# min-web-search-skill

**No API key. No Docker. No dependencies. Just search.**

## The Problem

AI agents all have a `web_search` tool — but it rarely works out of the box:

- **API keys are a hassle.** Brave, Tavily, Exa — each requires signing up, getting a key, and configuring it.
- **Network restrictions.** If you're in China, Brave and Google are blocked. Even with a key, the connection times out.
- **Heavy alternatives.** SearXNG requires Docker. Browser automation needs Chromium + Playwright.

Meanwhile, **Bing's RSS endpoint** (`www.bing.com/search?q=...&format=rss`) is:
- Free, no API key needed
- Accessible from mainland China
- Returns clean XML with titles, URLs, and snippets

## Implementations

| Script | Platform | Dependencies |
|---|---|---|
| `scripts/search.py` | Any OS with Python 3.8+ | Python stdlib only |
| `scripts/search.sh` | Linux, macOS, Alpine, WSL | curl/wget + sed + grep |
| `scripts/search.ps1` | Windows 10+ | PowerShell (built-in) |

**Recommended:** Use `search.py` when Python is available. Fall back to `search.sh` or `search.ps1` when it isn't.

## Usage

```bash
# Python (recommended)
python3 scripts/search.py "how to install docker"
python3 scripts/search.py "rust tutorial" --max 3
python3 scripts/search.py "openai api" --json

# Shell (when Python unavailable)
./scripts/search.sh "how to install docker"
./scripts/search.sh "rust tutorial" --max 3

# PowerShell (Windows)
.\scripts\search.ps1 "windows service" -Json
```

## Output

Human-readable by default:
```
1. How to Install Docker on Ubuntu 22.04
   https://www.digitalocean.com/community/tutorials/...
   Step 1: Update your existing list of packages...
```

JSON mode (`--json`):
```json
{
  "success": true,
  "query": "how to install docker",
  "results": [
    {"title": "...", "url": "...", "snippet": "..."}
  ]
}
```

## Limitations

- Bing China (`www.bing.com`) — results may bias toward Chinese content
- RSS returns max ~10 results, no pagination
- `grep -oP` in the shell version requires GNU grep

## License

MIT
