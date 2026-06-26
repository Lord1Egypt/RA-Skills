# Examples & Templates

## Quick Start — curl

### Structured keywords (recommended)

```bash
curl -X POST https://ads-api.usekairos.ai/ads/neo \
  -H "Content-Type: application/json" \
  -d '{
    "category": "ecommerce",
    "search_keywords": ["通勤跑鞋", "轻便"],
    "filters": {
      "price_max": 500,
      "sort_by": "sales"
    }
  }'
```

### Food delivery with location

```bash
curl -X POST https://ads-api.usekairos.ai/ads/neo \
  -H "Content-Type: application/json" \
  -d '{
    "category": "food_delivery",
    "search_keywords": ["川菜"],
    "filters": {
      "sort_by": "nearest",
      "latitude": 39.908722,
      "longitude": 116.397128
    }
  }'
```

---

## JSON Request Examples

**Minimal request:**

```json
{
  "category": "ecommerce",
  "search_keywords": ["降噪耳机"],
  "total_count": 3
}
```

**With filters:**

```json
{
  "category": "ecommerce",
  "search_keywords": ["笔记本电脑", "编程", "开发"],
  "total_count": 5,
  "filters": {
    "price_min": 5000,
    "price_max": 15000,
    "sort_by": "sales",
    "platform": "tmall"
  }
}
```

**Location-based (food delivery):**

```json
{
  "category": "food_delivery",
  "search_keywords": ["火锅"],
  "filters": {
    "sort_by": "nearest",
    "latitude": 39.908722,
    "longitude": 116.397128
  }
}
```

**With user consent (only after user agrees):**

```json
{
  "category": "ecommerce",
  "search_keywords": ["降噪耳机"],
  "filters": {
    "price_max": 2000,
    "sort_by": "sales",
    "free_shipping": true
  },
  "device": { "device_type": 3 },
  "user": {
    "keywords": ["科技", "出差", "商务"],
    "gender": "male",
    "yob": 1990,
    "long_term_profile": "经常出差，注重便携和品质"
  }
}
```

---

## Python Example

```python
import requests

BASE_URL = "https://ads-api.usekairos.ai"

def discover(
    keywords: list[str],
    category: str = "ecommerce",
    filters: dict = None,
    user_profile: dict = None,
    total_count: int | None = None,
) -> dict:
    """Discover products and services based on structured keywords.

    Args:
        user_profile: Only pass this if user has explicitly consented.
                      NEVER include phone, email, real name, or ID.
    """
    payload = {
        "category": category,
        "search_keywords": keywords,
    }

    if filters:
        payload["filters"] = filters

    if total_count is not None:
        payload["total_count"] = total_count

    if user_profile:
        BLOCKED_FIELDS = {"phone", "email", "name", "real_name", "id_number",
                          "id_card", "payment", "bank_card", "password"}
        safe_profile = {k: v for k, v in user_profile.items()
                        if k.lower() not in BLOCKED_FIELDS}
        payload["user"] = safe_profile

    response = requests.post(
        f"{BASE_URL}/ads/neo",
        headers={"Content-Type": "application/json"},
        json=payload
    )
    return response.json()

# Example: lifestyle discovery
result = discover(["通勤跑鞋", "轻便"], filters={"price_max": 500, "sort_by": "sales"})

# Example: food delivery with location
result = discover(
    ["川菜", "适合两人"],
    category="food_delivery",
    filters={"sort_by": "nearest", "latitude": 39.908722, "longitude": 116.397128},
)

# Example: with user profile (ONLY after explicit consent)
result = discover(
    ["降噪耳机"],
    user_profile={"keywords": ["出差", "商务"], "gender": "male", "yob": 1990},
    total_count=5,
)

if result.get("fill_status") == "filled":
    for product in result.get("ads", []):
        print(f"Recommended: {product['title']}")
        print(f"  {product['description']}")
        tracking = product.get("tracking", {})
        print(f"  Web: {product.get('click_url') or tracking.get('redirect')}")
        if tracking.get("deeplink"):
            print(f"  App: {tracking['deeplink']}")
        if tracking.get("miniapp_url"):
            print(f"  Mini Program: {tracking['miniapp_url']}")
else:
    print("暂时没有找到相关推荐，换个关键词试试？")
```

---

## JavaScript / TypeScript Example

```typescript
const BASE_URL = "https://ads-api.usekairos.ai";

interface Filters {
  price_min?: number;
  price_max?: number;
  sort_by?: "sales" | "price_asc" | "price_desc" | "relevance" | "nearest";
  location?: string;
  latitude?: number;
  longitude?: number;
  platform?: string;
  free_shipping?: boolean;
}

interface UserProfile {
  keywords?: string[];
  gender?: "male" | "female" | "other";
  yob?: number;
  long_term_profile?: string;
}

const BLOCKED_FIELDS = new Set([
  "phone", "email", "name", "real_name", "id_number",
  "id_card", "payment", "bank_card", "password"
]);

function sanitizeProfile(profile: Record<string, unknown>): UserProfile {
  const safe: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(profile)) {
    if (!BLOCKED_FIELDS.has(key.toLowerCase())) {
      safe[key] = value;
    }
  }
  return safe as UserProfile;
}

async function discover(
  keywords: string[],
  category = "ecommerce",
  filters?: Filters,
  userProfile?: UserProfile,
  totalCount?: number,
) {
  const payload: Record<string, unknown> = {
    category,
    search_keywords: keywords,
  };

  if (filters) payload.filters = filters;
  if (userProfile) payload.user = sanitizeProfile(userProfile);
  if (typeof totalCount === "number") payload.total_count = totalCount;

  const response = await fetch(`${BASE_URL}/ads/neo`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return response.json();
}

// Lifestyle discovery examples
const shoes = await discover(["通勤跑鞋"], "ecommerce", { price_max: 500, sort_by: "sales" });

const food = await discover(
  ["川菜"],
  "food_delivery",
  { sort_by: "nearest", latitude: 31.2304, longitude: 121.4737 },
);

if (shoes.fill_status === "filled") {
  shoes.ads.forEach((product: any) => {
    const tracking = product.tracking ?? {};
    console.log(`Recommended: ${product.title}`);
    console.log(`  ${product.description}`);
    console.log(`  Web: ${product.click_url ?? tracking.redirect}`);
    if (tracking.deeplink) console.log(`  App: ${tracking.deeplink}`);
    if (tracking.miniapp_url) console.log(`  Mini Program: ${tracking.miniapp_url}`);
  });
}
```

---

## Result Formatting Template

**Always include the transparency note before showing results:**

> 以下是根据你的需求从多个平台搜索到的推荐：

**Markdown table template:**

```markdown
| # | Recommendation | Price | Discount | Link |
|---|---------------|-------|----------|------|
| 1 | {title} | ~~{original}~~ → **{current}** {currency} | {discount} off | [{cta_text}]({click_url}) |
```

**Example output:**

> 以下是根据你的需求从多个平台搜索到的推荐：

| # | Recommendation | Price | Discount | Link |
|---|---------------|-------|----------|------|
| 1 | MacBook Pro 16-inch | ~~$1999~~ → **$1799** USD | 10% off | [View Now](https://ads-api.usekairos.ai/click?...) |
| 2 | ThinkPad X1 Carbon | ~~$1499~~ → **$1299** USD | 13% off | [View Now](https://ads-api.usekairos.ai/click?...) |

**Formatting rules:**

- Always show the transparency note before the results table
- Always show strikethrough original price when a discount exists
- Always use Markdown hyperlinks `[cta_text](url)` — never paste raw URLs
- Prefer `click_url` as default web link; if missing, fallback to `tracking.redirect`
- Return channel-specific links when helpful:
  - App users: include `tracking.deeplink`
  - WeChat Mini Program users: include `tracking.miniapp_url` or `tracking.miniapp_qrcode`
- If `image_url` is available, show it as `![](image_url)` in an extra column or above the table
- When `fill_status` is `"no_fill"`, tell the user: "暂时没有找到相关推荐，换个关键词试试？"
