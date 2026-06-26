---
name: image-search
description: >
  Visual image search using Google Lens via SerpAPI. Identify objects, landmarks, products,
  plants, animals, artwork, logos, or any visual entity from an image. Returns visual matches,
  entity identification, product info with prices, and related content.
  Use when: (1) user sends an image and asks "what is this?", (2) user wants to find similar
  images or products, (3) user wants to identify a landmark/plant/animal/product from a photo,
  (4) user needs to verify image origin or find higher resolution versions, (5) user asks to
  find where to buy something shown in an image. Requires SERPAPI_KEY env var.
metadata: {"openclaw": {"requires": {"env": ["SERPAPI_KEY"]}, "primaryEnv": "SERPAPI_KEY", "emoji": "🔍"}}
---

# Image Search (Google Lens)

Identify anything from an image using Google Lens via SerpAPI.

## Setup

Requires `SERPAPI_KEY` environment variable. Get a key at https://serpapi.com/ (100 free searches/month).

No pip dependencies needed — uses only Python stdlib (`urllib`, `json`, `base64`).

## Usage

### From CLI / Agent (exec tool)

```bash
# Search by image URL
python3 {baseDir}/scripts/lens_search.py "https://example.com/photo.jpg"

# Search by local file (auto-uploads to get a URL)
python3 {baseDir}/scripts/lens_search.py /path/to/image.png

# Refine with text query (e.g., find red version of a product)
python3 {baseDir}/scripts/lens_search.py "https://example.com/bag.jpg" --query "red"

# Product search (returns prices)
python3 {baseDir}/scripts/lens_search.py "https://example.com/sneakers.jpg" --type products

# Find exact matches (where this image appears online)
python3 {baseDir}/scripts/lens_search.py "https://example.com/photo.jpg" --type exact_matches

# Raw JSON output for programmatic use
python3 {baseDir}/scripts/lens_search.py "https://example.com/photo.jpg" --json

# Localized results (e.g., Japanese products with ¥ prices)
python3 {baseDir}/scripts/lens_search.py "https://example.com/laptop.jpg" --type products --country jp
```

## Search Types

| Type | Use Case | Returns |
|------|----------|---------|
| `all` (default) | General identification | Entity name + visual matches + text |
| `visual_matches` | Find similar images | Visually similar results with sources |
| `exact_matches` | Find image origin | Pages containing this exact image |
| `products` | Shopping / price lookup | Products with prices and buy links |
| `about_this_image` | Image provenance | Metadata about the image's origin |

## Output Format

The script outputs structured markdown:

```
## Identified Entity
- **Danny DeVito** — [link](https://...)

## Visual Matches (top 5)
- **Danny DeVito — Wikipedia** (Wikipedia) ✅ exact match
  https://en.wikipedia.org/wiki/Danny_DeVito
- ...
```

Use `--json` for raw SerpAPI response when you need thumbnails, image dimensions, or other metadata.

## Agent Decision Guide

When a user sends an image:

1. **Already identified by vision model?** If the main model confidently recognizes the entity, skip reverse search.
2. **Uncertain identification?** Run `lens_search.py` to verify. Compare model's guess with Lens results.
3. **Need details beyond identification?** First identify with Lens, then `web_search` for deeper info.
4. **Shopping intent?** Use `--type products` to get prices and buy links directly.
5. **Local file from user?** The script handles local files by auto-uploading to get a searchable URL.

## Combining with Other Tools

Typical multi-tool workflow:

```
1. User sends image → "What building is this?"
2. reverse_image_search → identifies "Cologne Cathedral"
3. web_search("Cologne Cathedral history architecture") → detailed info
4. Compose answer combining visual match + web knowledge
```

## Limitations

- SerpAPI free tier: 100 searches/month. Paid plans from $50/month.
- Local file upload uses freeimage.host (free) or imgbb (needs IMGBB_API_KEY).
- Google Lens results vary by region; use `--country` for localized results.
- Some niche/long-tail entities may not return useful visual matches.
