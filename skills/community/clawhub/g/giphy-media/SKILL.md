---
name: giphy-media
description: Search GIFs, stickers, emojis, trending media, and upload assets to GIPHY via the GIPHY API. Use this skill when users want to search for GIFs and stickers, browse trending content, translate phrases into matching media, fetch specific media by ID, or upload GIF or video assets after confirmation.
---

# GIPHY

![GIPHY](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/giphy.svg)

Access GIPHY via the GIPHY API with API key authentication. Search GIFs, stickers, emojis, trending media, and upload assets.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=giphy-media) for hosted connection flows and credentials so you do not need to configure GIPHY API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect GIPHY |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect GIPHY |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   GIPHY API      │
│   (User Chat)   │     │   (OAuth)    │     │   (REST)         │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect GIPHY     │                       │
         │                       │  4. Secure Token      │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ GIPHY    │
   │  File    │           │ Auth     │           │ Search   │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for GIPHY again."

## Quick Start

```bash
# Search GIFs
clawlink_call_tool --tool "giphy_search_gifs" --params '{"query": "laughing"}'

# Get trending GIFs
clawlink_call_tool --tool "giphy_trending_gifs" --params '{}'

# Translate phrase to GIF
clawlink_call_tool --tool "giphy_translate" --params '{"phrase": "thumbs up"}'
```

## Authentication

All GIPHY tool calls are authenticated automatically by ClawLink using the user's connected GIPHY account.

**No API key is required in chat.** ClawLink stores credentials securely and injects them into every GIPHY API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=giphy and connect GIPHY.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `giphy` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration giphy
```

**Response:** Returns the live tool catalog for GIPHY.

### Reconnect

If GIPHY tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=giphy
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration giphy`

## Security & Permissions

- Access is scoped to GIPHY content searchable and uploadable by the connected account.
- **All write operations require explicit user confirmation.** Before executing any create or upload, confirm the target resource and intended effect with the user.
- Uploading copyrighted material may violate GIPHY terms of service.

## Tool Reference

### Search & Discovery

| Tool | Description | Mode |
|------|-------------|------|
| `giphy_search_gifs` | Search for GIFs by keyword or phrase | Read |
| `giphy_search_stickers` | Search for stickers by keyword or phrase | Read |
| `giphy_search_emoji` | Search for emoji media by keyword | Read |
| `giphy_search_channels` | Search for GIPHY channels | Read |
| `giphy_search_tags` | Search for trending tags | Read |

### Trending

| Tool | Description | Mode |
|------|-------------|------|
| `giphy_trending_gifs` | Get trending GIFs | Read |
| `giphy_trending_stickers` | Get trending stickers | Read |
| `giphy_trending_searches` | Get trending search terms | Read |

### Translate

| Tool | Description | Mode |
|------|-------------|------|
| `giphy_translate` | Translate a phrase into a matching GIF or sticker | Read |

### Media Retrieval

| Tool | Description | Mode |
|------|-------------|------|
| `giphy_get_gif_by_id` | Fetch a specific GIF by its GIPHY ID | Read |
| `giphy_get_sticker_by_id` | Fetch a specific sticker by its GIPHY ID | Read |

### Upload

| Tool | Description | Mode |
|------|-------------|------|
| `giphy_upload_gif` | Upload a GIF or video asset to GIPHY | Write |

## Code Examples

### Search for reaction GIFs

```bash
clawlink_call_tool --tool "giphy_search_gifs" \
  --params '{
    "query": "thumbs up",
    "limit": 10,
    "rating": "pg-13"
  }'
```

### Get trending stickers

```bash
clawlink_call_tool --tool "giphy_trending_stickers" \
  --params '{
    "limit": 20
  }'
```

### Translate a phrase to a GIF

```bash
clawlink_call_tool --tool "giphy_translate" \
  --params '{
    "phrase": "facepalm",
    "rating": "pg-13"
  }'
```

### Get a specific GIF by ID

```bash
clawlink_call_tool --tool "giphy_get_gif_by_id" \
  --params '{
    "gif_id": "abc123xyz"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm GIPHY is connected.
2. Call `clawlink_list_tools --integration giphy` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `giphy`.
5. If no GIPHY tools appear, direct the user to https://claw-link.dev/dashboard?add=giphy.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  search → trending → translate → get by ID                  │
│                                                             │
│  Example: Search GIFs → Display results → User picks        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → upload                      │
│                                                             │
│  Example: Preview upload → User confirms → Execute upload   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer search, trending, and content lookup flows before uploads.
4. For uploads or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- GIPHY content is organized into GIFs, stickers, and emoji categories — use the appropriate tool for each type.
- Content ratings (`g`, `pg`, `pg-13`, `r`) filter content appropriateness. Match the rating to your use case.
- Uploaded media becomes part of the GIPHY library and may be searchable by other users.
- Trending content updates regularly; results may vary between calls.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration giphy`. |
| Missing connection | GIPHY is not connected. Direct the user to https://claw-link.dev/dashboard?add=giphy. |
| `404 Not Found` | GIF or sticker ID does not exist. Verify the ID. |
| Write rejected | User did not confirm an upload action. Always confirm before uploading. |

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

1. Ensure the integration slug is exactly `giphy`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [GIPHY API Documentation](https://developers.giphy.com/docs/api/)
- [GIPHY Developers](https://developers.giphy.com/)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=giphy-media)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Related Skills

- [Slack](https://clawhub.ai/hith3sh/slack) — For posting GIFs in channels
- [Discord](https://clawhub.ai/hith3sh/discord) — For sharing media in servers

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=giphy-media)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)