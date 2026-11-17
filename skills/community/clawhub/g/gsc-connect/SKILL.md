---
name: gsc-connect
description: Connect OpenClaw or another MCP-compatible agent to Google Search Console and retrieve official read-only properties, performance, sitemap, and URL inspection data. Use for clicks, impressions, CTR, average position, queries, pages, countries, devices, dates, and indexing investigations.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - openclaw
    homepage: https://yusihk.com/en/gsc-connect-codex-plugin-google-search-console/
    emoji: "📊"
---

# GSC Connect

Connect the agent to Google Search Console through YUSIHK's public, read-only MCP service. Retrieve remote data only through Google's official Search Console APIs.

## Requirements

- A Google account that already has access to at least one Search Console property.
- An MCP client that supports Streamable HTTP and OAuth.
- MCP endpoint: [`https://gsc.yusihk.com/mcp`](https://gsc.yusihk.com/mcp)
- English documentation: [`https://gsc.yusihk.com/docs`](https://gsc.yusihk.com/docs)
- Traditional Chinese documentation: [`https://gsc.yusihk.com/zh-hant/docs`](https://gsc.yusihk.com/zh-hant/docs)
- YUSIHK product guide: [`https://yusihk.com/en/gsc-connect-codex-plugin-google-search-console/`](https://yusihk.com/en/gsc-connect-codex-plugin-google-search-console/)

The service requests read-only Search Console access. Never ask the user for a Google password, OAuth client secret, access token, refresh token, cookie, or authorization code.

## Configure OpenClaw

Use a current OpenClaw release with outbound Streamable HTTP MCP and OAuth client support.

Check whether the server already exists:

```bash
openclaw mcp show google-search-console --json
```

For a new connection, save the remote MCP server:

```bash
openclaw mcp add google-search-console \
  --url https://gsc.yusihk.com/mcp \
  --transport streamable-http \
  --auth oauth
```

Run the OAuth connection and verify the tools:

```bash
openclaw mcp login google-search-console
openclaw mcp doctor google-search-console --probe
openclaw mcp reload
```

If the installed OpenClaw release does not yet provide `mcp add`, `mcp login`, or `mcp doctor`, save the equivalent server definition with the legacy-compatible command:

```bash
openclaw mcp set google-search-console '{"url":"https://gsc.yusihk.com/mcp","transport":"streamable-http","auth":"oauth"}'
```

Then restart OpenClaw and complete OAuth from the MCP settings screen. Upgrade OpenClaw if the installed release cannot authorize remote HTTP MCP servers.

If the client asks for connection fields, use:

| Field | Value |
| --- | --- |
| Name | `google-search-console` |
| Server URL | `https://gsc.yusihk.com/mcp` |
| Transport | `streamable-http` |
| Authentication | OAuth |
| Bearer token | Leave empty |
| Custom headers | Leave empty |
| OAuth client ID and secret | Leave empty; use server discovery |

The OpenClaw Control UI can also manage this connection at **Settings → MCP**. After changing the connection, reload MCP or restart the task/runtime that owns the MCP client.

## Configure Codex or another compatible client

In Codex CLI, add and authorize the same server:

```bash
codex mcp add google-search-console --url https://gsc.yusihk.com/mcp
codex mcp login google-search-console
```

In a graphical client, add a remote MCP server with the fields in the table above. Do not paste a Google password or manually created token into the MCP configuration.

## Detect available tools

Look for the following tool names. OpenClaw may prefix them with the server name, for example `google-search-console__gsc_list_sites`.

- `gsc_list_sites`
- `gsc_site_overview`
- `gsc_query_search_analytics`
- `gsc_list_sitemaps`
- `gsc_inspect_url`

If the tools are absent:

1. Run `openclaw mcp status --verbose`.
2. Run `openclaw mcp doctor google-search-console --probe`.
3. If authorization is required, run `openclaw mcp login google-search-console` once and complete the newest authorization flow.
4. Reload MCP and start a new task if the current task does not refresh its tool list.
5. Do not claim that live GSC data was accessed until the connector exposes the tools.

On older OpenClaw releases that do not have `status` or `doctor`, use `openclaw mcp show google-search-console` to confirm the saved definition, then restart OpenClaw and inspect the MCP settings screen.

## Select a property first

1. Call `gsc_list_sites` after authorization.
2. Show every exact `siteUrl` and its permission level.
3. Ask the user to select a property before any property-specific query unless they already supplied one.
4. Preserve Google's exact property identifier. Do not convert `sc-domain:example.com` into an HTTPS URL.
5. Prefer a `sc-domain:` property when the user requests whole-domain coverage; use the requested URL-prefix property when scope must stay limited.

## Query workflow

### Site overview

Use `gsc_site_overview` for a quick review. Always provide an explicit start date and end date. Summarize totals and leading queries, pages, countries, and devices without treating the result as a complete query log.

### Search performance

Use `gsc_query_search_analytics` for custom reports involving:

- clicks, impressions, CTR, and average position;
- query, page, date, country, and device dimensions;
- explicit date ranges and supported filters;
- comparable period analysis.

Preserve the exact property identifier returned by `gsc_list_sites`. Treat CTR as a decimal fraction unless formatting it as a percentage. Treat average position as an aggregate metric, not a fixed rank for every user.

### Sitemaps

Use `gsc_list_sitemaps` to read submitted sitemap processing status and errors. Do not submit, delete, or modify a sitemap.

### URL inspection

Use `gsc_inspect_url` to read Google's known indexed version of a URL. Clearly state that this is not a live URL test and does not request indexing or force a recrawl.

## Interpretation rules

- Mention `dataState` when fresh or incomplete data is included.
- Search Analytics can return top rows and enforce row limits; never claim that it returns every possible query.
- Compare equivalent date lengths, search types, countries, devices, and filters.
- Present seasonality, site changes, device mix, branded-query shifts, and indexing signals as possible explanations rather than proven causes.
- Separate API observations from SEO recommendations.
- Keep every action read-only. Never submit or delete properties or sitemaps, request indexing, transfer ownership, or change Search Console settings.

## Output format

Return:

1. Property, date range, search type, and filters used.
2. Key metrics and notable changes.
3. Queries or pages that deserve attention.
4. Data limitations and uncertainty.
5. Prioritized content, technical, and measurement checks.

## Troubleshooting

### Authorization request expired

Start one fresh login attempt and use only the newest authorization page. Do not click the connection control repeatedly while it is loading.

### Authorization succeeded but tools are missing

Run `openclaw mcp doctor google-search-console --probe`, reload MCP, and start a new task so tool discovery can refresh.

### A property is missing

Confirm that the authorized Google account already has access to the property in Search Console. Then call `gsc_list_sites` again and use the exact property identifier it returns.

### The endpoint is unavailable

Check [`https://gsc.yusihk.com/docs`](https://gsc.yusihk.com/docs) and retry the MCP probe. For support, email [`services@yusihk.com`](mailto:services@yusihk.com) without sending passwords, tokens, or private Search Console exports.

## Example requests

- “列出我可以访问的所有 GSC 网站，让我选择一个。”
- “检查这个网站最近 28 天表现，并列出热门查询和页面。”
- “按日期和设备获取点击、展示、CTR 和平均排名。”
- “找出展示较高但点击率偏低的页面。”
- “检查这个 URL 在 Google 已知索引中的状态。”
