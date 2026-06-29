---
name: open-crawl
version: 1.0.0
description: "Look up live Amazon product and search-results data — title, price, rating, BSR, reviews, rankings — and get it back as clean structured JSON. Runs through Claw School's hosted data API with your own CLAW_KEY; no third-party scraping account to set up. Use only when the user explicitly asks to look up Amazon product or search-results data, or to fetch a specific public web page they have named. The target URL and the returned page content are sent to Claw School's hosted API for processing, so it must not be used for private, internal-network, logged-in, or otherwise sensitive pages."
---

# open-crawl

Fetches live Amazon data through Claw School's hosted data API and returns it as
structured JSON, so you don't have to parse HTML yourself. It can also fetch a
specific public web page (returned as raw HTML).

**When to use it.** Only when the user has *explicitly* asked you to look up
current Amazon product or search data — e.g. "check the price and rating of this
Amazon listing", "show me the top results for this Amazon search" — or to fetch a
specific public page they named. This is **not** a background crawler and must
not be invoked on URLs the user did not ask you to look up.

## Privacy & safe use

> ⚠️ Every URL you submit **and the page content returned** is sent to Claw
> School's hosted data API (which uses an upstream scraping provider) for
> processing. Treat it like any external API:
>
> - Submit **public** URLs only.
> - **Never** submit internal/private-network addresses (`localhost`, `10.x`,
>   `192.168.x`, `*.internal`, …), logged-in/authenticated pages, pre-signed
>   links, or URLs containing secrets, tokens, or personal data.
> - Keep your `CLAW_KEY` confidential — it authenticates your account and is sent
>   only to the Claw School API, never to the target site.
>
> The API also rejects internal/private targets server-side, but you should never
> rely on that — don't send them in the first place.

## Authentication

This skill authenticates with a `CLAW_KEY` issued by
[claw-school.com](https://claw-school.com). It is provisioned automatically during
package install (the `/redeem` step configures it for you) — you don't need to
create or edit any files. The key is sent only to the Claw School API, as a
standard `Authorization: Bearer` credential.

## How to call it

Use your normal web-request capability to make an HTTPS request — no shell or
command-line tools are involved.

- **Method:** `POST`
- **Endpoint:** `{CLAW_API_BASE}/api/scrape` — the API base URL is provisioned
  together with your key.
- **Headers:**
  - `Authorization: Bearer <your CLAW_KEY>`
  - `Content-Type: application/json`
- **Body (JSON):**

```json
{
  "url": "https://www.amazon.com/dp/B07DN8ZJRL",
  "mode": "scraper"
}
```

### Body fields

| Field | Required | Description |
|---|---|---|
| `url` | yes | The public page to look up |
| `mode` | no | `"scraper"` — JS-rendered, the default; use for Amazon. `"proxy"` — fast raw HTTP for static pages. |
| `country` | no | Two-letter country code for geo-targeting, e.g. `"US"`, `"JP"` |
| `js_snippet` | no | JavaScript to run after page load (scraper mode only) |

> The `Authorization: Bearer` header is preferred. For backward compatibility the
> key may also be passed as a `claw_key` field in the JSON body.

## Response format

**Amazon product page (PDP)** — structured fields extracted automatically:

```json
{
  "url": "https://www.amazon.com/dp/B07DN8ZJRL",
  "status": 200,
  "parsed": {
    "asin": "B07DN8ZJRL",
    "title": "Echo Dot (3rd Gen)",
    "price": "$29.99",
    "rating": "4.7 out of 5 stars",
    "review_count": "847,231 ratings",
    "bought_past_month": "10K+ bought in past month",
    "bsr": ["#1 in Smart Speakers"],
    "badges": ["Amazon's Choice"],
    "bullet_points": ["..."],
    "reviews": [{ "author": "...", "rating": "5.0", "title": "...", "body": "..." }]
  },
  "body": null,
  "error": null
}
```

**Amazon search page (SERP)** — ranked results with pricing:

```json
{
  "url": "https://www.amazon.com/s?k=iphone+case",
  "status": 200,
  "parsed": {
    "keyword": "iphone case",
    "result_count": 48,
    "results": [
      {
        "position": "1",
        "asin": "B0XXXXX",
        "title": "...",
        "price": "$12.99",
        "rating": "4.7 out of 5 stars",
        "review_count": "23,456 ratings",
        "bought_past_month": "5K+ bought in past month",
        "sponsored": false,
        "ac_badge": "Amazon's Choice"
      }
    ]
  },
  "body": null,
  "error": null
}
```

> **Note:** If `parsed` fields are sparse (parse quality low), the response
> includes `body` with raw HTML as a fallback so you can extract data yourself.

**Any other public URL** — raw HTML in `body`:

```json
{ "url": "https://example.com", "status": 200, "parsed": null, "body": "<html>...</html>", "error": null }
```

## Error handling

The API returns a structured error `code`. Map it to a clear message for your
owner rather than surfacing a raw HTTP error:

| code | meaning | what to tell the user |
|---|---|---|
| `KEY_MISSING` | No credential supplied | Internal config issue — re-run the install/redeem step |
| `KEY_NOT_FOUND` | CLAW_KEY is invalid | The key is invalid; check claw-school.com |
| `KEY_NOT_ACTIVATED` | Key not yet activated | Finish activation at claw-school.com |
| `KEY_BLOCKED` | Key suspended/revoked | Contact Claw School support |
| `QUOTA_EXCEEDED` | Plan quota used up | Relay the `action.message` (renew at claw-school.com) |
| `URL_NOT_ALLOWED` | Target is internal/private/non-public | Relay the `action.message`; ask for a public URL |
| `UPSTREAM_TIMEOUT` | Target site slow | Retry once |

Responses may include an `action` object (e.g. `{"type": "notify_user", "message": "…"}`);
when present, relay that message to your owner verbatim.

## Get a CLAW_KEY

Visit [claw-school.com](https://claw-school.com) to get access. Each key is tied
to one agent and is configured for you during install.
