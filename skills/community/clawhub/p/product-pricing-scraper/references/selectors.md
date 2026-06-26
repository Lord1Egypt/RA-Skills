# Site-Specific Selectors

Reference for CSS selectors used by product-pricing-scraper.

## Amazon

| Field | Selector |
|-------|----------|
| Title | `#productTitle` |
| Price | `.a-price .a-offscreen` |
| Original Price | `.a-text-price .a-offscreen` |
| Rating | `#acrPopover .a-icon-alt` |
| Review Count | `#acrCustomerReviewText` |
| Stock | `#availability span` |

## eBay

| Field | Selector |
|-------|----------|
| Title | `.x-item-title__mainTitle` |
| Price | `.x-price-primary .notranslate` |
| Shipping | `.x-shipping-primary .notranslate` |
| Rating | `.x-seller-info .ux-icon-text__text` |

## Walmart

| Field | Selector |
|-------|----------|
| Title | `[data-automation-id="product-title"]` |
| Price | `[data-automation-id="product-price"] .price-characteristic` |
| Original Price | `[data-automation-id="product-price"] .price-comparison` |
| Rating | `[data-automation-id="product-rating"] .visually-hidden` |
| Stock | `[data-automation-id="product-offer"]` |

## Generic Fallback

When site is unrecognized, use heuristics:
- Price: `[itemprop="price"]`, `.price`, `[class*="price"]`
- Title: `[itemprop="name"]`, `h1`, `.product-title`
- Rating: `[itemprop="ratingValue"]`, `.rating`

## Notes

- Selectors break frequently; always validate with a snapshot before bulk scraping.
- For JS-rendered sites, use browser tool with `snapshot` to inspect live DOM.
