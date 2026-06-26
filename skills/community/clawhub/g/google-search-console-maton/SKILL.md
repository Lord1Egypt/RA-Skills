# SKILL.md

## Google Search Console (cURL Version)

Access the Google Search Console API with managed OAuth authentication using **cURL**. Query search analytics, manage sitemaps, and monitor site performance.

---

## Quick Start

### List Sites

```bash
curl -s \
  -H "Authorization: Bearer $MATON_API_KEY" \
  https://gateway.maton.ai/google-search-console/webmasters/v3/sites | jq
```

---

## Base URL

```
https://gateway.maton.ai/google-search-console/{native-api-path}
```

Replace `{native-api-path}` with the actual Google Search Console API endpoint path.
The gateway proxies requests to `www.googleapis.com` and automatically injects your OAuth token.

---

## Authentication

All requests require the Maton API key:

```bash
-H "Authorization: Bearer $MATON_API_KEY"
```

### Environment Variable

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

---

## Getting Your API Key

1. Sign in or create an account at https://maton.ai
2. Go to https://maton.ai/settings
3. Copy your API key

---

## Connection Management

Manage connections at:

```
https://ctrl.maton.ai
```

---

### List Connections

```bash
curl -s \
  -H "Authorization: Bearer $MATON_API_KEY" \
  "https://ctrl.maton.ai/connections?app=google-search-console&status=ACTIVE" | jq
```

---

### Create Connection

```bash
curl -s -X POST \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"app":"google-search-console"}' \
  https://ctrl.maton.ai/connections | jq
```

---

### Get Connection

```bash
curl -s \
  -H "Authorization: Bearer $MATON_API_KEY" \
  https://ctrl.maton.ai/connections/{connection_id} | jq
```

#### Response Example

```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-search-console",
    "metadata": {}
  }
}
```

Open the `url` in a browser to complete OAuth authorization.

---

### Delete Connection

```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $MATON_API_KEY" \
  https://ctrl.maton.ai/connections/{connection_id} | jq
```

---

## Specifying Connection

If multiple connections exist:

```bash
curl -s \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Maton-Connection: 21fd90f9-5935-43cd-b6c8-bde9d915ca80" \
  https://gateway.maton.ai/google-search-console/webmasters/v3/sites | jq
```

If omitted, the default (oldest active) connection is used.

---

## API Reference

### Sites

```bash
# List sites
GET /google-search-console/webmasters/v3/sites

# Get a specific site
GET /google-search-console/webmasters/v3/sites/{siteUrl}
```

> ⚠️ Site URL must be URL-encoded
> Example: `https%3A%2F%2Fexample.com%2F`

---

### Search Analytics

```bash
curl -s -X POST \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  https://gateway.maton.ai/google-search-console/webmasters/v3/sites/{siteUrl}/searchAnalytics/query \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-01-31",
    "dimensions": ["query"],
    "rowLimit": 100
  }' | jq
```

---

### Sitemaps

```bash
# List sitemaps
curl -s \
  -H "Authorization: Bearer $MATON_API_KEY" \
  https://gateway.maton.ai/google-search-console/webmasters/v3/sites/{siteUrl}/sitemaps | jq

# Submit sitemap
curl -s -X PUT \
  -H "Authorization: Bearer $MATON_API_KEY" \
  https://gateway.maton.ai/google-search-console/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}

# Delete sitemap
curl -s -X DELETE \
  -H "Authorization: Bearer $MATON_API_KEY" \
  https://gateway.maton.ai/google-search-console/webmasters/v3/sites/{siteUrl}/sitemaps/{feedpath}
```

---

## Search Analytics Examples

### Top Queries

```json
{
  "startDate": "2024-01-01",
  "endDate": "2024-01-31",
  "dimensions": ["query"],
  "rowLimit": 25
}
```

### Top Pages

```json
{
  "dimensions": ["page"]
}
```

### Device Breakdown

```json
{
  "dimensions": ["device"]
}
```

### Daily Performance

```json
{
  "dimensions": ["date"]
}
```

### Filtered Query

```json
{
  "dimensionFilterGroups": [{
    "filters": [{
      "dimension": "query",
      "operator": "contains",
      "expression": "keyword"
    }]
  }]
}
```

---

## Dimensions

* `query` – Search query
* `page` – Page URL
* `country` – Country code
* `device` – DESKTOP, MOBILE, TABLET
* `date` – Date

---

## Metrics (Auto Returned)

* `clicks`
* `impressions`
* `ctr`
* `position`

---

## Notes

* Site URLs must be URL-encoded
* Date range limited to 16 months
* Max 25,000 rows per request
* Use `startRow` for pagination
* Data delay: 2–3 days

---

## Important cURL Notes

* Use `-g` if URL contains brackets:

```bash
curl -g "https://example.com?fields[]=..."
```

* When piping to `jq`, environment variables may not expand correctly in some shells.

---

## Error Handling

| Status  | Meaning                           |
| ------- | --------------------------------- |
| 400     | Missing Search Console connection |
| 401     | Invalid/missing API key           |
| 429     | Rate limited (10 req/sec)         |
| 4xx/5xx | Upstream API error                |

---

## Troubleshooting API Key

### Check variable

```bash
echo $MATON_API_KEY
```

### Verify key

```bash
curl -s \
  -H "Authorization: Bearer $MATON_API_KEY" \
  https://ctrl.maton.ai/connections | jq
```

---

## Example: Full Query Flow

```bash
SITE_URL=$(python3 -c "import urllib.parse; print(urllib.parse.quote('https://example.com', safe=''))")

curl -s -X POST \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  "https://gateway.maton.ai/google-search-console/webmasters/v3/sites/$SITE_URL/searchAnalytics/query" \
  -d '{
    "startDate": "2024-01-01",
    "endDate": "2024-01-31",
    "dimensions": ["query"],
    "rowLimit": 25
  }' | jq
```

---
