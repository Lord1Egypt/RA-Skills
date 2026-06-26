# Amazon Product Scraping Reference

## Overview

Amazon does not provide a public product API for third parties. Product data must be extracted via web scraping or the Product Advertising API (PA-API, requires Amazon Associates enrollment).

## Method 1: Web Scraping

### Target URLs

Product detail pages follow this pattern:

```
https://www.amazon.com/dp/{ASIN}
https://www.amazon.com/gp/product/{ASIN}
```

ASIN (Amazon Standard Identification Number) is a 10-character alphanumeric identifier.

### Key DOM Elements

| Data | Selector | Notes |
|------|----------|-------|
| Title | `#productTitle` | Product name |
| Price | `.a-price-whole` + `.a-price-fraction` | Current price |
| List Price | `.basisPrice .a-price .a-offscreen` | Original price for comparison |
| Images | `#imgTagWrapperId img`, `.a-dynamic-image` | Thumbnail URLs; replace `_AC_US40_` with `_AC_SL1500_` for high-res |
| Bullet points | `#feature-bullets ul li span` | Key product features |
| Description | `#productDescription` | Full description (may be absent) |
| A+ Content | `#aplus` | Rich brand content (HTML) |
| Variants | `#twister` form | Color/size options |
| Category | `#wayfinding-breadcrumbs_feature_div` | Breadcrumb path |
| Rating | `#acrPopover` | Average star rating |
| Review count | `#acrCustomerReviewText` | Number of reviews |

### Scraping Code

```python
import requests
from bs4 import BeautifulSoup
import time
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def scrape_amazon_product(url):
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    title_el = soup.find("span", id="productTitle")
    title = title_el.get_text(strip=True) if title_el else ""

    # Price extraction (handles various formats)
    price = 0.0
    price_whole = soup.find("span", class_="a-price-whole")
    price_frac = soup.find("span", class_="a-price-fraction")
    if price_whole:
        whole = price_whole.get_text(strip=True).replace(",", "").rstrip(".")
        frac = price_frac.get_text(strip=True) if price_frac else "00"
        price = float(f"{whole}.{frac}")

    # High-resolution images
    images = []
    for img in soup.find_all("img", class_="a-dynamic-image"):
        src = img.get("src", "")
        if src:
            hi_res = re.sub(r"_AC_US\d+_", "_AC_SL1500_", src)
            images.append(hi_res)

    # Bullet points as description
    bullets = soup.find("div", id="feature-bullets")
    description = ""
    if bullets:
        items = bullets.find_all("span", class_="a-list-item")
        description = "\n".join(
            "• " + item.get_text(strip=True) for item in items
            if item.get_text(strip=True)
        )

    # Full description
    desc_el = soup.find("div", id="productDescription")
    if desc_el:
        full_desc = desc_el.get_text(strip=True)
        if full_desc:
            description += "\n\n" + full_desc

    # Category breadcrumbs
    breadcrumbs = soup.find("div", id="wayfinding-breadcrumbs_feature_div")
    category = ""
    if breadcrumbs:
        crumbs = breadcrumbs.find_all("a")
        category = " > ".join(c.get_text(strip=True) for c in crumbs)

    return {
        "title": title,
        "price": price,
        "images": images,
        "description": description,
        "category": category,
    }

def scrape_multiple(urls, delay=3):
    """Scrape multiple products with polite delay."""
    results = []
    for url in urls:
        try:
            product = scrape_amazon_product(url)
            results.append(product)
        except Exception as e:
            results.append({"error": str(e), "url": url})
        time.sleep(delay)
    return results
```

### Image URL Transforms

Amazon uses URL suffixes to control image size:

| Suffix | Size | Use |
|--------|------|-----|
| `_AC_US40_` | 40px | Thumbnail |
| `_AC_SL200_` | 200px | Small |
| `_AC_SL500_` | 500px | Medium |
| `_AC_SL1500_` | 1500px | High-res (recommended) |

Replace the suffix in `src` to get the desired resolution.

## Method 2: Product Advertising API (PA-API)

Requires an Amazon Associates account. Provides structured JSON responses.

```
GET https://webservices.amazon.com/paapi5/getitems
```

PA-API fields map more cleanly but requires enrollment and has rate limits.

## Important Guidelines

- **robots.txt**: Respect Amazon's crawling rules
- **Rate limits**: Use delays of 3-5 seconds between requests to avoid blocks
- **IP rotation**: Amazon blocks aggressive scraping; use residential proxies if needed
- **Dynamic content**: Some data loads via JavaScript — a headless browser (Playwright/Selenium) may be needed for variant details
- **Legal**: Scraping is for personal product migration only; do not redistribute Amazon's content
- **Price editing**: Always review and adjust prices for your store context
- **Image downloading**: Download images locally and include in the import ZIP rather than hotlinking

## Amazon → Mobazha Field Mapping

| Amazon Field | Mobazha Field | Notes |
|--------------|---------------|-------|
| Product title | `title` | Direct copy |
| Bullet points + description | `description` | Combine; strip HTML |
| Current price | `price` | Verify and adjust |
| Product images | `images[]` | Download high-res; include in ZIP |
| Color/size variants | `variants[]` | Map to Mobazha variant options |
| Category breadcrumbs | `tags[]` | Extract relevant tags |
| Condition | `condition` | Usually `NEW` |
| — | `contractType` | `PHYSICAL_GOOD` for tangible items |
| — | `pricingCurrency` | Set to your store's currency |
