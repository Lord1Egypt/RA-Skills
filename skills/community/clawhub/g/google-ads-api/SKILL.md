---
name: google-ads
description: |
  Google Ads API integration with managed OAuth. Query campaigns, ad groups, keywords, and performance metrics with GAQL. Use this skill when users want to interact with Google Ads data. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Google Ads

Access the Google Ads API with managed OAuth authentication. Query campaigns, ad groups, keywords, and performance metrics using GAQL.

## Quick Start

**CLI:**

```bash
maton google-ads query -c 1234567890 --resource campaign --fields 'campaign.id, campaign.status'
```

```bash
maton google-ads query -c 1234567890 --gaql 'SELECT campaign.id, campaign.status FROM campaign'
```

```bash
maton api '/google-ads/v24/customers/1234567890/googleAds:search' -f query='SELECT campaign.id, campaign.status FROM campaign'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'SELECT campaign.id, campaign.name, campaign.status FROM campaign'}).encode()
req = urllib.request.Request('https://api.maton.ai/google-ads/v24/customers/1234567890/googleAds:search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://api.maton.ai/google-ads/{native-api-path}
```

Maton proxies requests to `googleads.googleapis.com` and automatically injects OAuth and developer tokens.

## Installation

**NPM:**
```bash
npm install -g @maton-ai/cli
```

**Homebrew:**
```bash
brew install maton-ai/cli/maton
```

## Authentication

**CLI:**

```bash
maton login                          # Opens browser for API key
maton login --interactive            # Skip browser, paste API key directly
maton whoami                         # Show current auth state
```

**Manual:**

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key
4. Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## Connection Management

Manage your Google Ads OAuth connections at `https://api.maton.ai`.

### List Connections

**CLI:**

```bash
maton connection list google-ads --status ACTIVE
```

```bash
maton api -X GET /connections -f app=google-ads -f status=ACTIVE
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections?app=google-ads&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

**CLI:**

```bash
maton connection create google-ads
```

```bash
maton api /connections -f app=google-ads
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-ads'}).encode()
req = urllib.request.Request('https://api.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

**CLI:**

```bash
maton connection view {connection_id}
```

```bash
maton api /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "{connection_id}",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-ads",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

**CLI:**

```bash
maton connection delete {connection_id}
```

```bash
maton api -X DELETE /connections/{connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Google Ads connections, specify which one to use:

**CLI:**

```bash
maton google-ads campaign list -c 1234567890 --connection {connection_id}
```

```bash
maton api /google-ads/v24/customers/1234567890/googleAds:search --connection {connection_id}
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'SELECT campaign.id, campaign.name FROM campaign'}).encode()
req = urllib.request.Request('https://api.maton.ai/google-ads/v24/customers/1234567890/googleAds:search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '{connection_id}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If you have multiple connections, always specify the connection to ensure requests go to the intended account.

## Security & Permissions

- Access is scoped to campaigns, ad groups, ads, keywords, and reporting within the connected Google Ads account.
- **All write operations require explicit user approval.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.

## API Reference

### List Accessible Customers

```bash
GET /google-ads/v24/customers:listAccessibleCustomers
```

Example:

```bash
maton google-ads account list
```

### Search (GAQL Query)

```bash
POST /google-ads/v24/customers/{customerId}/googleAds:search
Content-Type: application/json

{
  "query": "SELECT campaign.id, campaign.name, campaign.status FROM campaign ORDER BY campaign.id"
}
```

Example:

```bash
maton google-ads query -c 1234567890 --resource campaign --fields 'campaign.id, campaign.name, campaign.status' --order-by 'campaign.id'
```

### List Keywords

```bash
POST /google-ads/v24/customers/{customerId}/googleAds:search
Content-Type: application/json

{
  "query": "SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, metrics.impressions, metrics.clicks, metrics.cost_micros FROM keyword_view WHERE segments.date DURING LAST_30_DAYS ORDER BY metrics.impressions DESC"
}
```

Example:

```bash
maton google-ads keyword list -c 1234567890 --date-range LAST_7_DAYS -L 25 --campaign-id 99999
```

Note: This command requests metrics, so it cannot be run against a manager (MCC) account directly. Run it against the client customer ID under the manager, optionally with `--login-customer-id`. See [Manager (MCC) Account Access](#manager-mcc-account-access).

### Search Stream (for large results)

```bash
POST /google-ads/v24/customers/{customerId}/googleAds:searchStream
Content-Type: application/json

{
  "query": "SELECT campaign.id, campaign.name FROM campaign"
}
```

Example:

```bash
maton google-ads query-stream -c 1234567890 --resource campaign --fields 'campaign.id, campaign.name'
```

## Common GAQL Queries

### List Campaigns

```sql
SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type
FROM campaign
WHERE campaign.status != 'REMOVED'
ORDER BY campaign.name
```

### Campaign Performance

```sql
SELECT campaign.id, campaign.name, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.impressions DESC
```

### List Ad Groups

```sql
SELECT ad_group.id, ad_group.name, ad_group.status, campaign.id, campaign.name
FROM ad_group
WHERE ad_group.status != 'REMOVED'
```

### List Keywords with Performance

```sql
SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.impressions, metrics.clicks, metrics.cost_micros
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
LIMIT 50
```

### Search Term Report

```sql
SELECT search_term_view.search_term, campaign.name, ad_group.name, metrics.impressions, metrics.clicks, metrics.conversions
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.clicks DESC
```

### Account-level Performance

```sql
SELECT customer.descriptive_name, segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM customer
WHERE segments.date DURING LAST_7_DAYS
```

## Manager (MCC) Account Access

When accessing a customer account through a Google Ads manager (MCC) account, pass the manager's customer ID via `--login-customer-id` (CLI) or the `login-customer-id` header (direct API). The customer ID in the path is still the client account being queried.

**CLI:**

```bash
# List campaigns in client account 1234567890 via manager 9876543210
maton google-ads campaign list -c 1234567890 --login-customer-id 9876543210
```

```bash
maton api '/google-ads/v24/customers/1234567890/googleAds:search' -H 'login-customer-id: 9876543210' -f query='SELECT campaign.id, campaign.name FROM campaign'
```

**Python:**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'query': 'SELECT campaign.id, campaign.name FROM campaign'}).encode()
req = urllib.request.Request('https://api.maton.ai/google-ads/v24/customers/1234567890/googleAds:search', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('login-customer-id', '9876543210')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Pagination

Google Ads uses token-based pagination. The CLI automatically paginates with '--paginate'.

Example:

```bash
maton google-ads campaign list -c 1234567890 --paginate
```

## Code Examples

### CLI

```bash
# List accessible customer accounts
maton google-ads account list

# Filter with jq
maton google-ads campaign list -c 1234567890 --json --jq '.results[] | {id: .campaign.id, name: .campaign.name}'

# Extract specific fields
maton google-ads campaign list -c 1234567890 --json --jq '.results[].campaign.name'
```

### JavaScript

```javascript
// Get customer IDs
const customers = await fetch(
  'https://api.maton.ai/google-ads/v24/customers:listAccessibleCustomers',
  { headers: { 'Authorization': `Bearer ${process.env.MATON_API_KEY}` } }
).then(r => r.json());

// Query campaigns
const campaigns = await fetch(
  `https://api.maton.ai/google-ads/v24/customers/${customerId}/googleAds:search`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      query: 'SELECT campaign.id, campaign.name FROM campaign'
    })
  }
).then(r => r.json());
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# Query campaigns
response = requests.post(
    f'https://api.maton.ai/google-ads/v24/customers/{customer_id}/googleAds:search',
    headers=headers,
    json={'query': 'SELECT campaign.id, campaign.name FROM campaign'}
)
```

## Notes

- Use `listAccessibleCustomers` first to get customer IDs
- Customer IDs are 10-digit numbers (remove dashes)
- Monetary values are in micros (divide by 1,000,000)
- Date ranges: `LAST_7_DAYS`, `LAST_30_DAYS`, `THIS_MONTH`
- Status values: `ENABLED`, `PAUSED`, `REMOVED`
- For accounts accessed through a Google Ads manager (MCC), pass the manager's customer ID with `--login-customer-id` (or the `login-customer-id` header). See [Manager (MCC) Account Access](#manager-mcc-account-access).
- IMPORTANT: When using curl commands, use `curl -g` when URLs contain brackets (`fields[]`, `sort[]`, `records[]`) to disable glob parsing
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments. You may get "Invalid API key" errors when piping.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Google Ads connection |
| 401 | Invalid or missing Maton API key |
| 429 | Rate limited (10 req/sec per account) |
| 4xx/5xx | Passthrough error from Google Ads API |

### Troubleshooting: API Key Issues

**CLI:**

1. Check your auth state:

```bash
maton whoami
```

2. Verify the API key is valid by listing connections:

```bash
maton connection list
```

**Manual:**

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://api.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `google-ads`. For example:

- Correct: `https://api.maton.ai/google-ads/v24/customers:listAccessibleCustomers`
- Incorrect: `https://api.maton.ai/v24/customers:listAccessibleCustomers`

## Resources

- [Google Ads API Overview](https://developers.google.com/google-ads/api/docs/start)
- [GAQL Reference](https://developers.google.com/google-ads/api/docs/query/overview)
- [GAQL Grammer](https://developers.google.com/google-ads/api/docs/query/grammar)
- [GAQL Cookbook](https://developers.google.com/google-ads/api/docs/query/cookbook)
- [GAQL Fields Reference](https://developers.google.com/google-ads/api/fields/v24/overview)
- [Metrics Reference](https://developers.google.com/google-ads/api/fields/v24/metrics)
- [Search](https://developers.google.com/google-ads/api/reference/rpc/v24/GoogleAdsService/Search)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
