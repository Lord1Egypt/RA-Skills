---
name: google-analytics-mcp
description: "Query Google Analytics 4 data — reports, funnels, realtime, property details — via the GA MCP server. Uses per-workspace service account credentials; no Gemini required."
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - uvx
        - mcporter
---

# Google Analytics

Query GA4 properties using the [Google Analytics MCP server](https://github.com/googleanalytics/google-analytics-mcp) via MCPorter. Each workspace supplies its own service account credentials — no shared or global auth.

## Prerequisites

- `uvx` (from `uv`) — runs `analytics-mcp` ephemerally, no install needed
- `mcporter` — `npm i -g mcporter`
- Service account JSON with GA read access in the workspace (see Setup)

## Per-workspace credentials

Each workspace stores its own credentials:

```
{workspace}/
  credentials/
    ga-service-account.json   ← Google service account key file
    ga-config.json            ← optional: default project/property
```

`ga-config.json` shape (optional):
```json
{
  "projectId": "my-gcp-project",
  "defaultProperty": "properties/123456789"
}
```

If `ga-config.json` is absent, pass `property` explicitly in every query.

## Workflow

1. **Locate credentials** — read `{workspace}/credentials/ga-service-account.json` (fail clearly if missing).
2. **Load config** — read `{workspace}/credentials/ga-config.json` if present; extract `projectId` and `defaultProperty`.
3. **Run query** via the helper script or direct mcporter call:

```bash
bash {skill_dir}/scripts/ga.sh <workspace> <tool> [args...]
```

Or directly:
```bash
CREDS="{workspace}/credentials/ga-service-account.json"
PROJECT_ID="$(cat {workspace}/credentials/ga-config.json | python3 -c 'import json,sys; print(json.load(sys.stdin).get("projectId",""))')"

mcporter call \
  --stdio uvx \
  --stdio-arg analytics-mcp \
  --env "GOOGLE_APPLICATION_CREDENTIALS=$CREDS" \
  --env "GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
  "analytics-mcp.<tool>" \
  [key=value ...]
```

## Available tools

| Tool | Purpose |
|------|---------|
| `get_account_summaries` | List all GA accounts + properties the SA has access to |
| `get_property_details` | Details for a specific property |
| `run_report` | Standard GA4 data report (dimensions, metrics, date ranges) |
| `run_funnel_report` | Funnel analysis |
| `run_realtime_report` | Realtime data |
| `get_custom_dimensions_and_metrics` | Custom dimensions/metrics for a property |
| `list_google_ads_links` | Google Ads links for a property |

## Common queries

**List all accessible properties:**
```bash
mcporter call --stdio uvx --stdio-arg analytics-mcp \
  --env "GOOGLE_APPLICATION_CREDENTIALS=$CREDS" \
  analytics-mcp.get_account_summaries
```

**Run a report (sessions last 30 days):**
```bash
mcporter call --stdio uvx --stdio-arg analytics-mcp \
  --env "GOOGLE_APPLICATION_CREDENTIALS=$CREDS" \
  --env "GOOGLE_CLOUD_PROJECT=$PROJECT_ID" \
  analytics-mcp.run_report \
  property=properties/123456789 \
  'dimensions=[{"name":"date"}]' \
  'metrics=[{"name":"sessions"}]' \
  'dateRanges=[{"startDate":"30daysAgo","endDate":"today"}]'
```

## Setup (one-time per workspace)

See `references/setup.md` for full instructions. Short version:

1. Create a GCP service account
2. Enable **Google Analytics Admin API** and **Google Analytics Data API**
3. Download the JSON key → save to `{workspace}/credentials/ga-service-account.json`
4. In GA4: Admin → Property Access Management → add the service account email as Viewer
5. Test: `bash {skill_dir}/scripts/ga.sh {workspace} get_account_summaries`

## Error notes

- `PERMISSION_DENIED` — SA email not added to GA property access
- `credentials not found` — check `ga-service-account.json` path
- `API not enabled` — enable Admin + Data APIs in GCP console
