---
name: posterly
description: >-
  Use posterly MCP to schedule and publish social posts across connected
  platforms (Instagram, TikTok, LinkedIn, YouTube, X, Facebook, Threads,
  Pinterest, Google Business Profile, and others). Use when the user wants
  to list accounts, draft or validate a post, schedule or publish, or
  manage social publishing through hosted MCP rather than a dashboard.
metadata:
  openclaw:
    requires:
      env:
        - POSTERLY_API_KEY
    primaryEnv: POSTERLY_API_KEY
  clawdbot:
    emoji: "📣"
    requires:
      bins: []
      env:
        - POSTERLY_API_KEY
        - POSTERLY_URL
---

# posterly

Agent skill for the posterly hosted MCP. Prefer MCP tools over inventing REST or CLI calls. Live tool schemas are the source of truth.

Use this skill when the user wants to schedule or publish social posts, list connected accounts, or validate a draft before it goes live.

## When to use hosted MCP

Use hosted MCP when the runtime can call MCP tools (Claude Code plugin, Cursor, or any MCP client).

- Docs: https://www.poster.ly/mcp
- Endpoint: `POST https://www.poster.ly/api/mcp`
- `GET https://www.poster.ly/api/mcp` returns server info without auth

Do not invent a second product surface, UI, Autopilot, or a live Claude Connectors listing. If MCP tools are missing, point the user at the MCP docs rather than pasting a long REST map.

Local stdio is optional: `npx -y posterly-mcp-server@0.50.4` with `POSTERLY_API_KEY` in the environment. Claude Code plugins that ship this package can load MCP from `.mcp.json` using plugin `userConfig.api_key`.

## Auth

API and MCP access need a paid posterly plan with API access. Starter + API is available from $10/month; check current pricing on the signup page.

- Environment: `POSTERLY_API_KEY` (starts with `pst_live_`)
- Claude plugin: `userConfig.api_key`, injected as `POSTERLY_API_KEY`
- Header: `Authorization: Bearer <POSTERLY_API_KEY>`

If the key is missing, send the user to https://www.poster.ly/mcp or https://www.poster.ly/agents/signup. Do not collect card numbers, posterly passwords, or social passwords. Do not invent a signup flow.

Never start signup if `whoami` already works. Never ask the user to paste a key they already have.

## Safe publish loop

Follow this loop for almost every publishing task. Confirm with the human before any write.

1. **whoami**
   Confirm the key, workspace, and scopes. Call this at the start of a session.

2. **List accounts**
   Call `list_accounts`. If the user named a brand or client, resolve it with brand tools first, then use the social account IDs.

3. **Draft and validate**
   Draft caption, media, account, and `scheduled_at`. Call `validate_post` with the complete payload. Fix errors before you ask for a live create.

4. **Schedule or publish with confirmation**
   Show account, platform, caption, schedule (or publish now), media, and workspace. Wait for an explicit yes. Then call `create_post` with the same payload and `confirm: true`.

Omitting `scheduled_at` publishes immediately. Never infer consent from an earlier standing instruction.

## Writes that need a human yes

Confirm the exact target before:

- Immediate publish (no `scheduled_at`)
- `create_post` / `create_posts_batch`
- Delete post, post group, comment, or disconnect
- Review replies, DMs, hide or unhide comments
- Spending AI credits
- Billing or API-key changes

Do not pass `confirm: true` until the user has approved that action.

## Useful read tools

Prefer MCP names. Do not dump raw JSON unless the user is debugging.

- `whoami`, `list_accounts`, `list_brands`, `list_platforms`, `get_platform_schema`
- `validate_post`, `list_posts`, `get_post`, `get_post_missing`
- `find_available_slot`, `list_media`, `list_activity`
- Analytics tools when the user asks how content performed

For media, use the MCP upload tools the runtime already has. Chat paperclips do not reach hosted MCP. If the user must upload a laptop file, use `create_media_drop` and send them the drop URL.

## After create

Tell the user the post was created, share any dashboard link the tool returned, and offer the next natural step. Inspect failed posts before retrying. Do not republish reconnect, re-upload, or edit-and-retry failures until the user has done that work.

## Fallback

If MCP is unavailable and the user has a shell, `npx -y @posterly/cli@0.1.5` uses the same key. Prefer MCP when tools are present.

## Links

- MCP: https://www.poster.ly/mcp
- Hosted MCP: https://www.poster.ly/api/mcp
- Agents signup: https://www.poster.ly/agents/signup

## Claude directory scope

Claude directory installs set `POSTERLY_DIRECTORY_PROFILE=claude` and use `https://www.poster.ly/api/mcp?profile=claude` for hosted connections. In this profile, AI image, video, and audio generation, billing mutations, and legacy tool aliases are unavailable. Do not switch profiles or use CLI or REST fallbacks for excluded operations. Use canonical live tool schemas and their view or action selectors. Other clients retain the standard catalog.
