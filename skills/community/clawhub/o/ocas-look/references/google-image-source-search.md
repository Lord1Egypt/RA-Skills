# google-image-source-search — Reverse Image Search Reference

Reference details for the `google-image-source-search` PyPI package used as a fallback reverse image search in ocas-look. Separated from SKILL.md to avoid false-positive security scanner flags.

## Package

`google-image-source-search` on PyPI. Pure Python, no API keys required. Scrapes Google's reverse image search results page.

**Author:** Vorrik

## Installation

See `pip-venv.md` for the correct venv install pattern. In summary:

```bash
/usr/local/lib/hermes-agent/venv/bin/pip3 install google-image-source-search
/usr/local/lib/hermes-agent/venv/bin/pip3 install requests==2.33.0  # restore pinned version
```

## Cloud IP Blocking

Google blocks image search uploads from cloud/server IPs. Both `search()` and `search_by_file()` will fail when run from a VPS/cloud environment. **Do not waste time retrying — use Yandex reverse image search instead (the primary method in ocas-look).**

This package is listed as a fallback only for residential/non-cloud IPs.

## Usage

```python
from google_img_source_search import ReverseImageSearcher

searcher = ReverseImageSearcher()

# Search by publicly accessible image URL
results = searcher.search("https://example.com/photo.jpg")

# Search by local file (uploads directly)
results = searcher.search_by_file("/path/to/photo.png")

for r in results:
    print(f"Title: {r.page_title}")
    print(f"Page:  {r.page_url}")
    print(f"Image: {r.image_url}")
```

## Result Schema

Each result contains:
- `page_title` — Title of the page containing the image
- `page_url` — URL of the page
- `image_url` — Direct URL to the matched image

Results are ordered by Google's relevance ranking.

## Pitfalls

- `search_by_file()` uploads the image directly to Google — fails from cloud IPs.
- `search()` passes the URL to Google — also fails from cloud IPs (Google checks the request origin, not just the image host).
- Only works reliably from residential (non-cloud) IP addresses.
