---
name: pinterest-scraper
description: Scrape Pinterest search results and collect pins with image URLs, descriptions, and direct links using infinite scroll. Use when you want to collect visual inspiration, trend data, or product imagery from Pinterest for research, datasets, or content planning.
metadata: {"requires": ["python3", "crawlee", "playwright"], "env": [], "tags": ["pinterest", "social-media", "scraper", "images", "visual-research"]}
---

# Pinterest Search Scraper

Scrapes pins from Pinterest search results using Crawlee's PlaywrightCrawler with infinite scroll support. Collects pin URLs, image URLs, and descriptions without requiring login.

## Requirements

```bash
pip install crawlee[playwright]
playwright install chromium
```

## Usage

```bash
python pinterest_scraper.py "search query"
python pinterest_scraper.py "minimalist home decor" 30
python pinterest_scraper.py "brutalist architecture" 100
```

Arguments:
- `query` (required): Search term (use quotes for multi-word queries)
- `max_pins` (optional): Maximum pins to collect, default 30

## What It Returns

Each pin object contains:

| Field | Description |
|-------|-------------|
| `id` | Pinterest pin ID |
| `url` | Full Pinterest pin URL (`https://www.pinterest.com/pin/<id>/`) |
| `image_url` | Highest-resolution image URL from srcset |
| `description` | Image alt text / pin description |

## Output

Saved to `./storage/pinterest/<safe_query>.json`:

```json
[
  {
    "id": "123456789",
    "url": "https://www.pinterest.com/pin/123456789/",
    "image_url": "https://i.pinimg.com/736x/ab/cd/ef/...",
    "description": "Minimalist living room with white walls"
  },
  ...
]
```

## How It Works

The scraper uses Crawlee's `PlaywrightCrawler` to:

1. Navigate to the Pinterest search URL: `https://www.pinterest.com/search/pins/?q=<encoded_query>`
2. Wait for pin elements to appear (`[data-test-id="pin"]` or `a[href*="/pin/"]`)
3. Iteratively scroll to the bottom to trigger infinite load
4. Extract pins after each scroll via `page.evaluate()` JavaScript injection
5. Deduplicate by pin ID and collect until `max_pins` is reached or scrolling stalls

The JavaScript extractor resolves `srcset` attributes to select the highest-resolution image available:

```python
async def _extract_pins(self, page) -> None:
    """Extract pin data from the current page state."""
    # Runs JS in the browser context to walk the DOM and extract pin data
    # Handles multiple Pinterest DOM structures (data-test-id variants)
    # Resolves srcset to get highest resolution image
    ...
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_pins` | 30 | Maximum pins to collect |
| `headless` | `True` | Run browser headlessly (set `False` for debugging) |
| `max_scroll_attempts` | 10 | Stop after N consecutive scrolls with no new pins |
| `scroll_delay` | 1.5s | Wait between scrolls for content to load |

To run in headed mode for debugging:
```python
scraper = PinterestScraper(max_pins=10, headless=False)
```

## Integrating Into a Pipeline

```python
import asyncio
from pinterest_scraper import PinterestScraper

async def collect_inspiration(query: str, limit: int = 50) -> list[dict]:
    scraper = PinterestScraper(max_pins=limit, headless=True)
    pins = await scraper.scrape_search(query)
    return pins

pins = asyncio.run(collect_inspiration("editorial fashion photography", 50))
```

## Troubleshooting

**No pins found**: Pinterest occasionally changes its DOM structure. Try setting `headless=False` to inspect visually. The scraper attempts two selector strategies (`[data-test-id="pin"]` and `a[href*="/pin/"]`).

**Fewer pins than expected**: Pinterest's infinite scroll depends on scroll velocity and network speed. Increase `max_scroll_attempts` in `scrape_search()` or add a longer `asyncio.sleep()` after each scroll.

**Playwright install error**: Run `playwright install chromium` to download the browser binary. If behind a corporate proxy, set `PLAYWRIGHT_BROWSERS_PATH` to a writable directory.

**Rate limiting / CAPTCHA**: Pinterest may show a CAPTCHA after many rapid requests. Add delays between scraper runs or rotate residential IPs.

## Rate Limiting Guidelines

- Wait 5+ seconds between search queries when running multiple
- Avoid scraping more than 300-500 pins per hour from a single IP
- Pinterest does not require login for search, but aggressive scraping triggers bot detection

## Use Cases

- **Visual trend research**: Collect images around a topic to identify visual patterns
- **Dataset creation**: Build image datasets for computer vision or aesthetic scoring models
- **Content planning**: Find top-performing visuals in a niche to guide creative direction
- **Competitive research**: Scrape brand-related queries to see what imagery dominates a category
- **Mood board generation**: Automate collection of reference images for design projects
