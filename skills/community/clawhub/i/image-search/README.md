# 🔍 image-search

Visual image search powered by Google Lens via [SerpAPI](https://serpapi.com/). Identify anything from a photo — landmarks, plants, animals, products, artwork, logos, people, or any visual entity.

**Zero dependencies.** Python stdlib only.

## Quick Start

```bash
export SERPAPI_KEY="your_key_here"  # Get one at https://serpapi.com/ (100 free/month)

# Identify an object
python3 scripts/lens_search.py "https://upload.wikimedia.org/wikipedia/commons/thumb/Cologne_Cathedral.jpg"

# Search a local file
python3 scripts/lens_search.py ./mystery_plant.jpg

# Find products with prices
python3 scripts/lens_search.py ./sneakers.jpg --type products

# Localized results (e.g., Japanese market)
python3 scripts/lens_search.py ./laptop.jpg --type products --country jp --lang ja

# Raw JSON output
python3 scripts/lens_search.py ./photo.jpg --json
```

## Search Types

| Type | What it does | Example use case |
|------|-------------|-----------------|
| `all` (default) | Entity identification + visual matches | "What is this?" |
| `visual_matches` | Find visually similar images | Find the source of an image |
| `exact_matches` | Find pages containing this exact image | Trace image origin |
| `products` | Shopping results with prices | "Where can I buy this?" |
| `about_this_image` | Image provenance metadata | Fact-checking |

## CLI Options

```
usage: lens_search.py [-h] [--query QUERY] [--type TYPE] [--limit N]
                      [--lang LANG] [--country COUNTRY] [--json]
                      [--api-key KEY] image

positional arguments:
  image                 Image URL or local file path

options:
  --query, -q           Text query to refine search (e.g., "red version")
  --type, -t            Search type: all|visual_matches|exact_matches|products|about_this_image
  --limit, -n           Max results to show (default: 5)
  --lang                Language code (default: en). Supports: en, zh-CN, ja, ko, fr, de, ...
  --country             Country code for localized results (e.g., us, jp, cn)
  --json                Output raw JSON instead of formatted markdown
  --api-key             SerpAPI key (default: reads SERPAPI_KEY env var)
```

## Output Example

```markdown
## Identified Entity
- **Cologne Cathedral** — [link](https://en.wikipedia.org/wiki/Cologne_Cathedral)

## Visual Matches (top 3)
- **Cologne Cathedral — Wikipedia** (Wikipedia) ✅ exact match
  🔗 https://en.wikipedia.org/wiki/Cologne_Cathedral
  🖼️ https://upload.wikimedia.org/...
- **Kölner Dom | Official Guide** (koelner-dom.de)
  🔗 https://www.koelner-dom.de/
```

## Local File Upload

When you pass a local file path, the script auto-uploads it to get a searchable URL:

1. **freeimage.host** — free, no API key needed (default)
2. **imgbb.com** — set `IMGBB_API_KEY` env var as fallback

Max file size: 32MB.

## As an OpenClaw Skill

This repo is also an [OpenClaw](https://github.com/openclaw/openclaw) agent skill. Drop it into your skills directory:

```bash
# Manual install
cp -r image-search ~/.openclaw/workspace/skills/

# Or via ClawHub (when published)
clawhub install image-search
```

The agent will automatically use it when users send images asking "what is this?".

## Use as a Python Library

```python
from scripts.lens_search import google_lens_search, format_results

results = google_lens_search(
    image_url="https://example.com/photo.jpg",
    search_type="visual_matches",
    hl="en",
)
print(format_results(results, limit=3))
```

## Requirements

- Python 3.10+
- SerpAPI key ([free tier](https://serpapi.com/): 100 searches/month, paid from $50/month)
- No pip install needed

## License

MIT
