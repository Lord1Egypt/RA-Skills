---
name: google-analytics-reporting
description: Run GA4 reports, inspect properties, list audiences and data streams, and analyze traffic and conversion data via the Google Analytics Data API. Use this skill when users want to list account summaries and properties, run standard or realtime GA4 reports with chosen dimensions and metrics, inspect available fields and compatibility, list audiences, data streams and key events, compare traffic and campaign performance, or create key events after confirmation.
---

# Google Analytics

![Google Analytics](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-analytics.svg)

Access Google Analytics via the GA4 Data API with OAuth authentication. Run GA4 reports, inspect properties, list audiences and data streams, and analyze traffic and conversion data.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-analytics-reporting) for hosted connection flows and credentials so you do not need to configure Google Analytics API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Analytics |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Analytics |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  GA4 Data API    │
│   (User Chat)   │     │   (OAuth)    │     │   (REST)         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Google Analytics                   │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ GA4      │
   │  File    │           │ Auth     │           │ Reports  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Analytics again."

## Quick Start

```bash
# List accessible accounts and properties
clawlink_call_tool --tool "google_analytics_list_account_summaries" --params '{}'

# Run a basic GA4 report
clawlink_call_tool --tool "google_analytics_run_report" --params '{"property": "properties/123456789", "dimensions": [{"name": "country"}, {"name": "deviceCategory"}], "metrics": [{"name": "sessions"}, {"name": "totalRevenue"}]}'

# Run a realtime report
clawlink_call_tool --tool "google_analytics_run_realtime_report" --params '{"property": "properties/123456789", "dimensions": [{"name": "country"}], "metrics": [{"name": "activeUsers"}]}'
```

## Authentication

All Google Analytics tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every GA4 API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-analytics and connect Google Analytics.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-analytics` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-analytics
```

**Response:** Returns the live tool catalog for Google Analytics.

### Reconnect

If Google Analytics tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-analytics
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-analytics`

## Security & Permissions

- Access is scoped to GA4 properties accessible to the connected Google account.
- **All write operations require explicit user confirmation.** Before executing any key event creation or property update, confirm the intended effect with the user.
- Reports and analytics queries are read-only and do not modify account data.

## Tool Reference

### Account & Property Discovery

| Tool | Description | Mode |
|------|-------------|------|
| `google_analytics_list_account_summaries` | List all accessible accounts and properties | Read |
| `google_analytics_list_accounts_v1_beta` | List all Google Analytics accounts | Read |
| `google_analytics_list_properties_filtered` | List GA4 properties with filtering | Read |
| `google_analytics_get_property` | Get GA4 property details | Read |
| `google_analytics_get_account` | Get account details | Read |

### Reporting

| Tool | Description | Mode |
|------|-------------|------|
| `google_analytics_run_report` | Run a customized GA4 data report | Read |
| `google_analytics_run_realtime_report` | Run a realtime report (last 30-60 min) | Read |
| `google_analytics_run_pivot_report` | Run a pivot table report | Read |
| `google_analytics_run_funnel_report` | Run a funnel analysis report | Read |
| `google_analytics_batch_run_reports` | Run multiple reports in one batch | Read |
| `google_analytics_check_compatibility` | Check dimension/metric compatibility | Read |

### Metadata & Configuration

| Tool | Description | Mode |
|------|-------------|------|
| `google_analytics_get_metadata` | Get available dimensions, metrics, comparisons | Read |
| `google_analytics_get_property_quotas_snapshot` | Get API quota usage for a property | Read |
| `google_analytics_get_data_retention_settings` | Get data retention configuration | Read |
| `google_analytics_get_attribution_settings` | Get attribution model settings | Read |
| `google_analytics_get_google_signals_settings` | Get Google Signals configuration | Read |

### Audiences & Data Streams

| Tool | Description | Mode |
|------|-------------|------|
| `google_analytics_list_audiences` | List configured audiences | Read |
| `google_analytics_get_audience` | Get audience configuration details | Read |
| `google_analytics_list_data_streams` | List data streams for a property | Read |
| `google_analytics_list_key_events` | List key events (conversions) | Read |
| `google_analytics_get_key_event` | Get key event details | Read |

### Audience Lists

| Tool | Description | Mode |
|------|-------------|------|
| `google_analytics_create_audience_list` | Create an audience list snapshot | Write |
| `google_analytics_create_recurring_audience_list` | Create a recurring audience list | Write |
| `google_analytics_list_audience_lists` | List all audience lists | Read |
| `google_analytics_query_audience_list` | Query audience list results | Read |

### Custom Definitions

| Tool | Description | Mode |
|------|-------------|------|
| `google_analytics_list_custom_dimensions` | List custom dimensions | Read |
| `google_analytics_create_custom_dimension` | Create a custom dimension | Write |
| `google_analytics_list_custom_metrics` | List custom metrics | Read |
| `google_analytics_create_custom_metric` | Create a custom metric | Write |

### Property Management

| Tool | Description | Mode |
|------|-------------|------|
| `google_analytics_update_property` | Update property settings | Write |
| `google_analytics_create_rollup_property` | Create a roll-up property | Write |

## Code Examples

### Run a basic traffic report

```bash
clawlink_call_tool --tool "google_analytics_run_report" \
  --params '{
    "property": "properties/123456789",
    "dimensions": [{"name": "date"}, {"name": "country"}, {"name": "deviceCategory"}],
    "metrics": [{"name": "sessions"}, {"name": "totalUsers"}, {"name": "bounceRate"}],
    "dateRanges": [{"startDate": "30daysAgo", "endDate": "today"}]
  }'
```

### Run a realtime report

```bash
clawlink_call_tool --tool "google_analytics_run_realtime_report" \
  --params '{
    "property": "properties/123456789",
    "dimensions": [{"name": "country"}, {"name": "city"}],
    "metrics": [{"name": "activeUsers"}]
  }'
```

### List key events

```bash
clawlink_call_tool --tool "google_analytics_list_key_events" \
  --params '{
    "property": "properties/123456789"
  }'
```

### Check dimension/metric compatibility

```bash
clawlink_call_tool --tool "google_analytics_check_compatibility" \
  --params '{
    "property": "properties/123456789",
    "dimensions": [{"name": "userAgeBracket"}, {"name": "sessionCampaignName"}],
    "metrics": [{"name": "sessions"}]
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Analytics is connected.
2. Call `clawlink_list_tools --integration google-analytics` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-analytics`.
5. If no Google Analytics tools appear, direct the user to https://claw-link.dev/dashboard?add=google-analytics.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → run_report → check_compatibility              │
│                                                             │
│  Example: List properties → Run report → Show results       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → create/update               │
│                                                             │
│  Example: Preview key event creation → User confirms        │
│           → Execute create                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer listing accounts, properties, metadata, compatibility, and read-only reports before writes.
4. For key event creation, property updates, or anything marked as requiring confirmation, call `clawlink_preview_tool` first, then confirm with the user.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- GA4 property IDs use format `properties/123456789` in API calls.
- Dimension and metric names in GAQL use camelCase (e.g., `date`, `sessionCampaignName`, `totalUsers`).
- GA4 Data API has strict dimension/metric compatibility rules. Not all combinations are valid. Use `check_compatibility` to validate before running complex reports.
- Realtime data covers the last 30-60 minutes and may not be available for all custom dimensions.
- Key events (conversions) are read-only via API — creation and deletion require the Google Analytics UI.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-analytics`. |
| Missing connection | Google Analytics is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-analytics. |
| `400 INVALID_ARGUMENT` | Incompatible dimension/metric combination. Use `check_compatibility` to validate. |
| `403 Forbidden` | Insufficient OAuth scopes or permissions. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `google-analytics`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [GA4 Data API Documentation](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [GA4 Dimensions & Metrics](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema)
- [GA4 Realtime API](https://developers.google.com/analytics/devguides/reporting/realtime/v1)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-analytics-reporting)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-analytics-reporting)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)