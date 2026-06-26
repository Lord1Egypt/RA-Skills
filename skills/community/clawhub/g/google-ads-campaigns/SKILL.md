---
name: google-ads-campaigns
description: Inspect Google Ads accounts and campaigns, run GAQL reports, and coordinate campaign or audience changes with confirmation via the Google Ads API. Use this skill when users want to list accessible customers, inspect campaigns by ID or name, run GAQL query reports for performance analysis, review customer lists, or create/update campaign, ad group, or audience configurations after confirmation.
---

# Google Ads

![Google Ads](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-ads.svg)

Access Google Ads via the Google Ads API with OAuth authentication. Inspect accounts and campaigns, run GAQL reports, and coordinate campaign or audience changes.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-ads-campaigns) for hosted connection flows and credentials so you do not need to configure Google Ads API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Ads |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Ads |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Google Ads API  │
│   (User Chat)   │     │   (OAuth)    │     │   (REST/GAQL)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Google Ads                        │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Google   │
   │  File    │           │ Auth     │           │ Ads      │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Ads again."

## Quick Start

```bash
# List accessible customers
clawlink_call_tool --tool "google_ads_list_accessible_customers" --params '{}'

# Get campaign details
clawlink_call_tool --tool "google_ads_get_campaign" --params '{"customer_id": "123-456-7890", "campaign_id": 123456789}'

# Run a GAQL report
clawlink_call_tool --tool "google_ads_search" --params '{"customer_id": "123-456-7890", "query": "SELECT campaign.id, campaign.name, metrics.impressions FROM campaign WHERE segments.date DURING LAST_7_DAYS"}'
```

## Authentication

All Google Ads tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Ads API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-ads and connect Google Ads.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-ads` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-ads
```

**Response:** Returns the live tool catalog for Google Ads.

### Reconnect

If Google Ads tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-ads
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-ads`

## Security & Permissions

- Access is scoped to Google Ads accounts accessible to the connected Google account.
- **All write operations require explicit user confirmation.** Before executing any campaign, ad group, or audience changes, confirm the intended effect with the user.
- Destructive actions (pausing campaigns, removing audiences) are marked as high-impact and must be confirmed.
- GAQL queries are read-only and do not modify account data.

## Tool Reference

### Account & Customer Management

| Tool | Description | Mode |
|------|-------------|------|
| `google_ads_list_accessible_customers` | List all customer accounts accessible to the user | Read |
| `google_ads_get_customer` | Get customer account details | Read |

### Campaigns

| Tool | Description | Mode |
|------|-------------|------|
| `google_ads_list_campaigns` | List campaigns for a customer | Read |
| `google_ads_get_campaign` | Get campaign details by ID | Read |
| `google_ads_create_campaign` | Create a new campaign | Write |
| `google_ads_update_campaign` | Update campaign settings | Write |

### Ad Groups

| Tool | Description | Mode |
|------|-------------|------|
| `google_ads_list_ad_groups` | List ad groups in a campaign | Read |
| `google_ads_get_ad_group` | Get ad group details | Read |
| `google_ads_create_ad_group` | Create a new ad group | Write |

### Audiences & Customer Lists

| Tool | Description | Mode |
|------|-------------|------|
| `google_ads_list_audiences` | List audiences for a customer | Read |
| `google_ads_list_customer_lists` | List customer match lists | Read |
| `google_ads_create_customer_list` | Create a new customer list | Write |
| `google_ads_add_customer_list_members` | Add members to a customer list | Write |

### Reporting

| Tool | Description | Mode |
|------|-------------|------|
| `google_ads_search` | Run a GAQL query and return results | Read |
| `google_ads_get_campaign_budget` | Get campaign budget details | Read |

## Code Examples

### List campaigns

```bash
clawlink_call_tool --tool "google_ads_list_campaigns" \
  --params '{
    "customer_id": "123-456-7890"
  }'
```

### Run a GAQL report

```bash
clawlink_call_tool --tool "google_ads_search" \
  --params '{
    "customer_id": "123-456-7890",
    "query": "SELECT campaign.id, campaign.name, campaign.status, metrics.impressions, metrics.clicks, metrics.cost_micros FROM campaign WHERE segments.date DURING LAST_30_DAYS"
  }'
```

### Create a customer list

```bash
clawlink_call_tool --tool "google_ads_create_customer_list" \
  --params '{
    "customer_id": "123-456-7890",
    "name": "High Value Customers",
    "description": "List of high-value customer emails for remarketing"
  }'
```

### Update campaign status

```bash
clawlink_call_tool --tool "google_ads_update_campaign" \
  --params '{
    "customer_id": "123-456-7890",
    "campaign_id": 123456789,
    "status": "PAUSED"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Ads is connected.
2. Call `clawlink_list_tools --integration google-ads` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-ads`.
5. If no Google Ads tools appear, direct the user to https://claw-link.dev/dashboard?add=google-ads.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search (GAQL) → call                          │
│                                                             │
│  Example: List campaigns → Get campaign → Run GAQL report   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → create/update               │
│                                                             │
│  Example: Preview campaign change → User confirms           │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer account inspection, campaign reads, and GAQL queries before writes.
4. For campaign, ad group, or audience changes, call `clawlink_preview_tool` first, then confirm with the user.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Customer IDs use format `123-456-7890` (hyphen-separated, not dashes in the API).
- GAQL queries must use valid Google Ads field names and resources. Invalid queries return 400 errors.
- Campaign and ad group IDs are unique within a customer account but may conflict across accounts.
- Some features require Google Ads API permissions granted during OAuth consent.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-ads`. |
| Missing connection | Google Ads is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-ads. |
| `404 Not Found` | Campaign, ad group, or customer ID does not exist. |
| `400 Bad Request` | Invalid GAQL query syntax or invalid parameter values. |
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

1. Ensure the integration slug is exactly `google-ads`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Ads API Documentation](https://developers.google.com/google-ads/api/docs/start)
- [Google Ads API Reference](https://developers.google.com/google-ads/api/reference/rpc)
- [GAQL Query Builder](https://developers.google.com/google-ads/api/docs/query/overview)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-ads-campaigns)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-ads-campaigns)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)