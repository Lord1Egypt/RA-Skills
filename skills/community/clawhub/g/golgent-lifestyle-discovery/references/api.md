# API Reference

## Endpoint

**POST** `https://ads-api.usekairos.ai/ads/neo`

Intelligently search and recommend quality products and services based on structured intent. **Supports anonymous access — no API Key needed.**

---

## Request Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `category` | string | No | Scene category for data source routing. Omit to query all sources |
| `search_keywords` | string[] | No* | 1–3 structured Chinese keywords extracted by the Agent. **Highest priority** |
| `filters` | object | No | Structured filtering conditions |
| `filters.price_min` | number | No | Minimum price (CNY) |
| `filters.price_max` | number | No | Maximum price (CNY) |
| `filters.sort_by` | string | No | Sort: `sales`, `price_asc`, `price_desc`, `relevance`, `nearest` |
| `filters.location` | string | No | Location (city name for general use; detailed address for food delivery if coordinates unavailable) |
| `filters.latitude` | number | No | User latitude (required for `food_delivery`; optional for others) |
| `filters.longitude` | number | No | User longitude (required for `food_delivery`; optional for others) |
| `filters.platform` | string | No | Platform filter: `tmall`, `taobao` |
| `filters.free_shipping` | bool | No | Only show free-shipping items |
| `total_count` | number | No | Number of results to return per category (default: `2`) |
| `intent` | object | No* | *(Deprecated)* Legacy intent info — use `search_keywords` instead |
| `intent.user_intent` | string | No* | User need description (fallback when `search_keywords` not provided) |
| `intent.keywords` | string[] | No | Keywords (fallback when `search_keywords` not provided) |
| `intent.intent_type` | string | No | Intent type (chat, text_to_image, search, etc.) |
| `intent.image_url` | string | No | Related image URL (for image-related intents) |
| `user` | object | No | User preference info (**requires explicit user consent — see privacy.md**) |
| `user.keywords` | string[] | No | User interest tags |
| `user.gender` | string | No | Gender (male, female, other) |
| `user.yob` | int | No | Year of birth |
| `user.long_term_profile` | string | No | User preference description |
| `site` | object | No | Page context |
| `site.page` | string | No | Current page URL |
| `device` | object | No | Device information |
| `device.device_type` | int | No | Device type (1=Android, 2=iOS, 3=Mac, 4=Windows, 5=Other) |

> **Keyword priority:** `search_keywords` > `intent.keywords` > `intent.user_intent`. At least one must be provided.

---

## Response Schema

**Successful response (recommendations found):**

```json
{
  "request_id": "01HQXYZ...",
  "fill_status": "filled",
  "fill_type": "product",
  "ppid": "unique_session_id",
  "ads": [
    {
      "ad_id": "12345",
      "title": "MacBook Pro 16-inch",
      "description": "Best choice for programmers, M3 Pro chip, 18-hour battery life",
      "cta_text": "View Now",
      "image_url": "https://cdn.example.com/macbook.jpg",
      "click_url": "https://ads-api.usekairos.ai/click?...",
      "tracking": {
        "redirect": "https://s.click.meituan.com/...",
        "deeplink": "meituanwaimai://...",
        "miniapp_url": "pages/food/detail?...",
        "miniapp_qrcode": "https://qr.meituan.com/..."
      },
      "price": {
        "original": "1999",
        "current": "1799",
        "currency": "USD",
        "discount": "10%"
      }
    }
  ]
}
```

**No recommendations:**

```json
{
  "request_id": "01HQXYZ...",
  "fill_status": "no_fill",
  "ads": []
}
```

### Response Fields

| Field | Description |
|-------|-------------|
| `fill_status` | `"filled"` = results found; `"no_fill"` = no results |
| `ads[].title` | Product/service title |
| `ads[].description` | Short description |
| `ads[].cta_text` | Call-to-action text |
| `ads[].image_url` | Product image URL |
| `ads[].click_url` | Primary web link (preferred for display) |
| `ads[].tracking.redirect` | Fallback web link |
| `ads[].tracking.deeplink` | Native app deep link |
| `ads[].tracking.miniapp_url` | WeChat Mini Program path |
| `ads[].tracking.miniapp_qrcode` | Mini Program QR code URL |
| `ads[].price.original` | Original price |
| `ads[].price.current` | Discounted price |
| `ads[].price.discount` | Discount percentage |

---

## Best Practices

### Use Structured Keywords, Not Raw Sentences

Extract keywords before calling — don't pass raw user sentences:

- ❌ `"intent": { "user_intent": "我想买一双防水的冬季登山鞋，预算500左右" }`
- ✅ `"search_keywords": ["登山鞋", "防水", "冬季"], "filters": { "price_max": 500 }`

### Record Impressions When Displaying

When showing products, call impression URLs to help optimize recommendations:

```python
for url in product.get("impression_urls", []):
    requests.get(url)
```

### Use Click URLs

Always use `click_url` for links. If `tracking` links are present, select by user channel:

- Web/H5: `click_url` (or fallback `tracking.redirect`)
- Native app: `tracking.deeplink`
- WeChat Mini Program: `tracking.miniapp_url` / `tracking.miniapp_qrcode`

### Handle No Recommendations Gracefully

```python
if result.get("fill_status") == "no_fill":
    print("暂时没有找到相关推荐，换个关键词试试？")
```

---

## Error Handling

| HTTP Status | Meaning | Solution |
|-------------|---------|----------|
| 400 | Bad Request | Check request body format, ensure `search_keywords` or `intent.user_intent` is provided |
| 401 | Invalid Token | Provided `Authorization` header but token is invalid. Omit the header for anonymous access |
| 404 | Not Found | Check URL path |
| 429 | Too Many Requests | Reduce request frequency, use exponential backoff |
| 500 | Server Error | Use exponential backoff retry |

Error response example:

```json
{
  "error": "Either search_keywords or intent.user_intent must be provided"
}
```

---

## Rate Limits

- Authenticated users: 100 requests/second per API Key
- Anonymous users: 100 requests/second per IP
- When receiving 429 response, use exponential backoff retry

---

## Legacy Format (Deprecated)

The `intent` object format is still supported but deprecated. Prefer `search_keywords` for all new integrations.

```json
{
  "intent": {
    "user_intent": "I need a laptop for programming",
    "keywords": ["笔记本电脑"]
  }
}
```

---

## Contact

- Email: support@usekairos.ai
- Documentation: https://docs.usekairos.ai
