# How to Find a Competitor's Facebook Page ID

The Page ID is more reliable than keyword search — it targets exactly one brand's ads.

## Method 1: From the Ad Library URL

1. Go to https://www.facebook.com/ads/library/
2. Search for the brand name
3. Click on their page name in the results
4. Look at the URL: `?view_all_page_id=434174436675167` ← that number is the page ID

## Method 2: From the Facebook Page itself

1. Go to the brand's Facebook Page (e.g., facebook.com/Nike)
2. Right-click → View Page Source
3. Search for `"pageID"` or look for a 15-digit number near the page name

## Method 3: Via Graph API (if you have a token)

```python
import requests

def find_page_id(brand_name: str, access_token: str) -> list[dict]:
    """Search for a brand's Facebook page and get its ID."""
    response = requests.get(
        "https://graph.facebook.com/v23.0/pages/search",
        params={
            "q": brand_name,
            "fields": "id,name,fan_count,category",
            "access_token": access_token,
        }
    )
    data = response.json()
    return data.get("data", [])

# Usage:
results = find_page_id("Nike", access_token="YOUR_TOKEN")
for page in results[:5]:
    print(f"{page['name']} — ID: {page['id']} — Followers: {page.get('fan_count', 'N/A')}")
```

## Method 4: Playwright automation

```python
async def find_page_id_playwright(brand_name: str) -> str:
    """Find page ID by navigating to Ad Library and extracting from URL."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"https://www.facebook.com/ads/library/?q={brand_name}&search_type=page")
        await page.wait_for_timeout(3000)
        
        # Click the first page result
        first_result = await page.query_selector('a[href*="view_all_page_id"]')
        if first_result:
            href = await first_result.get_attribute("href")
            import re
            match = re.search(r'view_all_page_id=(\d+)', href)
            if match:
                await browser.close()
                return match.group(1)
        
        await browser.close()
        return None
```

## Common Brand Page IDs (for quick testing)

| Brand | Page ID |
|-------|---------|
| Apple | 434174436675167 |
| Nike | 15087023444 |
| Amazon | 164885266835 |
| Coca-Cola | 40796308305 |
| McDonald's | 25953702998 |

> Always verify IDs — pages can change. Use the lookup methods above for competitors.
