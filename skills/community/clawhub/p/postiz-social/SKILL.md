---
name: postiz-social
description: Manage social publishing, scheduled posts, and content workflows in Postiz via the Postiz API. Use this skill when users want to create, schedule, or manage social media posts, review publishing queues, and coordinate content workflows via Postiz.
---

# Postiz Social Publishing

![Postiz Social Publishing](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/postiz.png)

Access Postiz's social publishing platform via the Postiz API. Manage social publishing, scheduled posts, and content workflows across connected social accounts.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=postiz-social) for hosted connection flows and credentials so you do not need to configure Postiz API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Postiz |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Postiz |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Postiz API │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │  3. Connect Postiz    │                       │
          │                      │  4. Secure Token      │
          │                      │  5. Proxy Requests    │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │  Postiz │
    │  File    │           │ Auth     │           │ Platform │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Postiz again."

## Quick Start

```bash
# List scheduled posts
clawlink_call_tool --tool "postiz_list_posts" --params '{"status": "scheduled"}'

# Get post details
clawlink_call_tool --tool "postiz_get_post" --params '{"post_id": "POST_ID"}'

# List workspaces
clawlink_call_tool --tool "postiz_list_workspaces" --params '{}'
```

## Authentication

All Postiz tool calls are authenticated automatically by ClawLink using the user's connected Postiz account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Postiz API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=postiz and connect Postiz.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `postiz` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration postiz
```

**Response:** Returns the live tool catalog for Postiz.

### Reconnect

If Postiz tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=postiz
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration postiz`

## Security& Permissions

- Access is scoped to posts, workspaces, and content workflows within the connected Postiz account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Publishing, editing, or deleting posts affects live social accounts — confirm carefully.
- Destructive actions must be confirmed.

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Postiz is connected.
2. Call `clawlink_list_tools --integration postiz` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `postiz`.
5. If no Postiz tools appear, direct the user to https://claw-link.dev/dashboard?add=postiz.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List scheduled posts → Get details → Show queue  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves │
│           → Execute update                                 │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Code Examples

### List scheduled posts

```bash
clawlink_call_tool --tool "postiz_list_posts" \
  --params '{
    "workspace_id": "WORKSPACE_ID",
    "status": "scheduled",
    "limit": 50
  }'
```

### Create a post

```bash
clawlink_call_tool --tool "postiz_create_post" \
  --params '{
    "workspace_id": "WORKSPACE_ID",
    "content": "Excited to announce our new product launch!",
    "social_account_ids": ["ACCOUNT_ID"],
    "scheduled_at": "2024-07-20T10:00:00Z"
  }'
```

### Get post analytics

```bash
clawlink_call_tool --tool "postiz_get_post_analytics" \
  --params '{
    "post_id": "POST_ID"
  }'
```

### Update a scheduled post

```bash
clawlink_call_tool --tool "postiz_update_post" \
  --params '{
    "post_id": "POST_ID",
    "content": "Updated announcement with new details!"
  }'
```

## Notes

- Postiz API has rate limits. Use exponential backoff when encountering 429 errors.
- Workspace IDs and post IDs are strings — verify IDs before passing to operations.
- Scheduling posts requires specifying a future `scheduled_at` timestamp in ISO 8601 format.
- Social account IDs must be from the same workspace as the post operation.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration postiz`. |
| Missing connection | Postiz is not connected. Direct the user to https://claw-link.dev/dashboard?add=postiz. |
| `not_found` | Post, workspace, or account does not exist. Check the ID. |
| `validation_error` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Rate limited | Too many requests. Wait and retry with exponential backoff. |
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

1. Ensure the integration slug is exactly `postiz`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Postiz](https://postiz.com/)
- [Postiz API Documentation](https://docs.postiz.com/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=postiz-social
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Postiz](https://clawhub.ai/hith3sh/postiz-social) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=postiz-social)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
