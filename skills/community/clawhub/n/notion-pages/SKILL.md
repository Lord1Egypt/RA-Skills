---
name: notion-workspace
description: Search pages and databases, update content, and manage Notion workspace data from chat. Use this skill when users want to read, create, or modify Notion pages, query databases, manage sections, or automate Notion workflows via the Notion API.
---

# Notion Assistant

Access Notion via the Notion API with OAuth authentication. Search pages and databases, read and update content, manage sections, and coordinate workspace workflows.

This skill uses [ClawLink](https://claw-link.dev) for hosted connection flows and credentials so you do not need to configure Notion API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Notion |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Notion |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│    Notion API    │
│   (User Chat)   │     │   (OAuth)    │     │ │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin │                       │
          │  2. Pair Device      │                       │
          │  3. Connect Notion    │                       │
          │                      │  4. Secure Token      │
          │                      │  5. Proxy Requests │
          │                      │                       │
          ▼ ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │  Notion  │
    │  File    │           │ Auth     │           │ Workspace│
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Notion again."

## Quick Start

```bash
# List databases in the workspace
clawlink_call_tool --tool "notion_list_databases" --params '{}'

# Search for pages by title
clawlink_call_tool --tool "notion_search" --params '{"query": "project notes"}'

# Get page content
clawlink_call_tool --tool "notion_get_page" --params '{"page_id": "PAGE_ID"}'
```

## Authentication

All Notion tool calls are authenticated automatically by ClawLink using the user's connected Notion account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Notion API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=notion and connect Notion.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `notion` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration notion
```

**Response:** Returns the live tool catalog for Notion.

### Reconnect

If Notion tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=notion
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration notion`

## Security& Permissions

- Access is scoped to pages, databases, and content within the connected Notion workspace.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete page, remove database entry) must be confirmed.

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Notion is connected.
2. Call `clawlink_list_tools --integration notion` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `notion`.
5. If no Notion tools appear, direct the user to https://claw-link.dev/dashboard?add=notion.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: Search pages → Read content → Show results        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Code Examples

### Search pages

```bash
clawlink_call_tool --tool "notion_search" \
  --params '{
    "query": "meeting notes",
    "filter": {
      "property": "object",
      "value": "page"
    }
  }'
```

### Query a database

```bash
clawlink_call_tool --tool "notion_query_database" \
  --params '{
    "database_id": "DATABASE_ID",
    "filter": {
      "property": "Status",
      "select": {
        "equals": "In Progress"
      }
    },
    "sorts": [
      {
        "property": "Last edited time",
        "direction": "descending"
      }
    ]
  }'
```

### Create a page

```bash
clawlink_call_tool --tool "notion_create_page" \
  --params '{
    "parent": {
      "database_id": "DATABASE_ID"
    },
    "properties": {
      "Name": {
        "title": [
          {
            "text": {
              "content": "New Project Page"
            }
          }
        ]
      }
    },
    "children": [
      {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
          "rich_text": [
            {
              "text": {
                "content": "Overview"
              }
            }
          ]
        }
      }
    ]
  }'
```

## Notes

- Notion API has rate limits. Use exponential backoff when encountering 429 errors.
- Page and database IDs are UUIDs (e.g., `abc123-def456-...`). Use the full ID, not the human-readable page URL slug.
- Block content updates require the full block structure in the request body.
- Archived pages can be retrieved but may require specific filter conditions.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration notion`. |
| Missing connection | Notion is not connected. Direct the user to https://claw-link.dev/dashboard?add=notion. |
| `object_not_found` | Page or database does not exist. Check the ID or search for the resource first. |
| `validation_error` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| `conflict_error` | Resource was modified concurrently. Retry or re-fetch the latest state. |
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

1. Ensure the integration slug is exactly `notion`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Notion API Documentation](https://developers.notion.com/)
- [Notion Integration Guide](https://www.notion.so/help/guides)
- ClawLink: https://claw-link.dev
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Docs](https://clawhub.ai/hith3sh/google-docs-documents) — For Google Workspace document operations
- [Notion](https://clawhub.ai/hith3sh/notion-workspace) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
