---
name: jpeng-web-scraper
description: "Web scraping skill with JavaScript rendering support. Extract data from websites using CSS selectors, XPath, or AI-powered extraction."
version: "1.0.0"
author: "jpeng"
tags: ["web", "scraping", "extraction", "crawler", "playwright"]
---

# Web Scraper

Extract data from websites with support for dynamic content.

## When to Use

- User wants to scrape data from a website
- Extract structured data from HTML
- Handle JavaScript-rendered pages
- Crawl multiple pages

## Features

- **Static pages**: Fast HTML parsing
- **Dynamic pages**: Playwright/Puppeteer rendering
- **Selectors**: CSS, XPath, regex
- **AI extraction**: Auto-detect data patterns

## Usage

### Simple scrape

```bash
python3 scripts/scrape.py \
  --url "https://example.com/products" \
  --selector ".product-name" \
  --output ./products.json
```

### With JavaScript rendering

```bash
python3 scripts/scrape.py \
  --url "https://spa-example.com/data" \
  --render \
  --wait 2000 \
  --selector ".data-item"
```

### Extract multiple fields

```bash
python3 scripts/scrape.py \
  --url "https://example.com/listings" \
  --fields '{
    "title": "h1.title",
    "price": ".price",
    "description": ".desc"
  }'
```

### Crawl multiple pages

```bash
python3 scripts/scrape.py \
  --url "https://example.com/page/1" \
  --crawl 'a[href*="/page/"]' \
  --max-pages 10 \
  --selector ".item"
```

### AI-powered extraction

```bash
python3 scripts/scrape.py \
  --url "https://example.com/article" \
  --ai-extract "Extract the title, author, and publication date"
```

## Output

```json
{
  "success": true,
  "url": "https://example.com/products",
  "items": [
    {"name": "Product 1", "price": "$99"},
    {"name": "Product 2", "price": "$149"}
  ],
  "scraped_at": "2024-01-15T10:30:00Z"
}
```

## Rate Limiting

- Default delay: 1 second between requests
- Respects robots.txt
- Customizable user agent
