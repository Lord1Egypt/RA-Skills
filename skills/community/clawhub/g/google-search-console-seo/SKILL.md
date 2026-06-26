---
name: google-search-console-seo
description: Google Search Console API integration with managed OAuth. Query search performance analytics, inspect URL indexing status, review sitemaps, and manage verified site properties. Use this skill when users want to monitor SEO performance or troubleshoot indexing issues.
---

# Google Search Console

![Google Search Console](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-search-console.png)

Access Google Search Console via the Search Console API with managed OAuth authentication. Query search performance, inspect indexing status, review sitemaps, and manage verified sites.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-search-console-seo) for hosted connection flows and credentials so you do not need to configure Google Search Console API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Search Console |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Search Console |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Google Search  │
│   (User Chat)   │     │   (OAuth)    │     │   Console API    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect GSC       │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Search  │
   │  File    │           │ Auth     │           │  Console │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Search Console again."

## Quick Start

```bash
# List verified sites
clawlink_call_tool --tool "google_search_console_list_sites" --params '{}'

# Query search analytics
clawlink_call_tool --tool "google_search_console_search_analytics_query" --params '{"site_url": "https://example.com/", "start_date": "2024-01-01", "end_date": "2024-01-31"}'

# Inspect a URL
clawlink_call_tool --tool "google_search_console_inspect_url" --params '{"site_url": "https://example.com/", "inspection_url": "https://example.com/page/"}'
```

## Authentication

All Google Search Console tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Search Console API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-search-console and connect Google Search Console.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-search-console` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-search-console
```

**Response:** Returns the live tool catalog for Google Search Console.

### Reconnect

If Google Search Console tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-search-console
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-search-console`

## Security & Permissions

- Access is scoped to sites verified in the connected Google Search Console account.
- **All write operations require explicit user confirmation.** Before executing any site addition, removal, or sitemap submission, confirm the target and intended effect with the user.
- Destructive actions (delete site) are marked as high-impact and must be confirmed.

## Tool Reference

### Site Management

| Tool | Description | Mode |
|------|-------------|------|
| `google_search_console_list_sites` | List all verified sites (URL-prefix and domain properties) owned by the user | Read |
| `google_search_console_get_site` | Get details and permission level for a specific site | Read |
| `google_search_console_add_site` | Register a new site property in Search Console | Write |
| `google_search_console_delete_site` | Remove a site from Search Console tracking | Write |

### Search Analytics

| Tool | Description | Mode |
|------|-------------|------|
| `google_search_console_search_analytics_query` | Query clicks, impressions, CTR, and position metrics | Read |

### URL Inspection

| Tool | Description | Mode |
|------|-------------|------|
| `google_search_console_inspect_url` | Inspect a specific URL for indexing status and issues | Read |

### Sitemap Management

| Tool | Description | Mode |
|------|-------------|------|
| `google_search_console_list_sitemaps` | List all sitemaps submitted for a site | Read |
| `google_search_console_get_sitemap` | Get sitemap metadata (submitted/indexed counts, errors, timestamps) | Read |
| `google_search_console_submit_sitemap` | Submit or resubmit a sitemap for a verified property | Write |

## Code Examples

### List verified sites

```bash
clawlink_call_tool --tool "google_search_console_list_sites" \
  --params '{}'
```

### Query search analytics for a date range

```bash
clawlink_call_tool --tool "google_search_console_search_analytics_query" \
  --params '{
    "site_url": "https://example.com/",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "dimensions": ["query", "page"]
  }'
```

### Query analytics filtered by country

```bash
clawlink_call_tool --tool "google_search_console_search_analytics_query" \
  --params '{
    "site_url": "https://example.com/",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "dimensions": ["country"],
    "row_limit": 50
  }'
```

### Inspect a URL for indexing issues

```bash
clawlink_call_tool --tool "google_search_console_inspect_url" \
  --params '{
    "site_url": "https://example.com/",
    "inspection_url": "https://example.com/important-page/"
  }'
```

### Submit a sitemap

```bash
clawlink_call_tool --tool "google_search_console_submit_sitemap" \
  --params '{
    "site_url": "https://example.com/",
    "feedpath": "/sitemap.xml"
  }'
```

### Add a new site

```bash
clawlink_call_tool --tool "google_search_console_add_site" \
  --params '{
    "site_url": "https://newsite.example.com/"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Search Console is connected.
2. Call `clawlink_list_tools --integration google-search-console` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-search-console`.
5. If no Google Search Console tools appear, direct the user to https://claw-link.dev/dashboard?add=google-search-console.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → query → inspect → call                        │
│                                                             │
│  Example: List sites → Query analytics → Show results       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview → User approves            │
│           → Execute sitemap submission                      │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer listing sites, querying analytics, and inspecting URLs before writes.
4. For sitemap submissions, site additions or removals, or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- The `site_url` parameter must exactly match the property as returned by `list_sites` — include protocol, subdomain, and trailing slash where applicable.
- `search_analytics_query` only returns URLs with at least one impression; missing rows do not confirm non-indexing.
- Position is an impression-weighted average rank across all queries.
- Sitemap metadata (`errors`, `warnings`, `submitted`, `indexed`) may be returned as strings — cast to integers before comparisons.
- Results may reflect cached data lagging real changes by several days.
- High-volume inspect_url usage can trigger 429 quota errors — limit to priority URLs.
- Numeric fields in sitemap responses can lag several days after submission.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-search-console`. |
| Missing connection | Google Search Console is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-search-console. |
| `NOT_VERIFIED` | Site is not verified in Search Console. Complete verification first. |
| `FORBIDDEN` | No permission level for the requested site. |
| `INVALID_ARGUMENT` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
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

1. Ensure the integration slug is exactly `google-search-console`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Search Console API Overview](https://developers.google.com/webmaster-tools/search-console-api-original)
- [Search Analytics Reference](https://developers.google.com/webmaster-tools/search-console-api-original/v3/searchanalytics)
- [Sites Reference](https://developers.google.com/webmaster-tools/search-console-api-original/v3/sites)
- [Sitemaps Reference](https://developers.google.com/webmaster-tools/search-console-api-original/v3/sitemaps)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-search-console-seo
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-search-console-seo)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)