---
name: jubjub
description: Publish content across TikTok, Instagram, YouTube, Facebook, LinkedIn, Vimeo, Vimeo OTT, and Mux. Manage team workflows, collaborate with your team, and track verified publish history.
version: 1.2.0
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      env:
        - JUBJUB_API_KEY
    primaryEnv: JUBJUB_API_KEY
---

# JubJub

## 1. OVERVIEW

JubJub is a content publishing and team collaboration platform for creators. Upload video content, collaborate with team members through threaded messaging and notifications, and publish across multiple platforms — TikTok, Instagram, YouTube, Facebook, LinkedIn, Vimeo, Vimeo OTT, and Mux — from a single workflow. Every publish creates a verified on-chain record on Base, giving creators immutable proof of ownership and publish history.

Supported platforms: TikTok, Instagram, YouTube, LinkedIn, Facebook, Vimeo, Vimeo OTT, Mux. JubJub does not currently support X/Twitter.

## 2. CONFIRMATION REQUIRED

Several JubJub actions are high-impact, public, destructive, or financial. Before invoking any of the following tools, the agent MUST surface the planned action to the user — including target platforms, visibility, schedule, account, and any cost — and wait for explicit confirmation. Do not chain these actions inside multi-step workflows without a confirmation step.

**Public publishing** (fans out to external platforms, hard to fully undo):
- `launches_create`, `launches_retry`, `launches_reschedule`

**Destructive** (permanent or hard to reverse):
- `contents_delete`, `workspaces_delete`, `teams_delete`, `launches_cancel`, `credentials_delete`, `teams_members_remove`, `communication_delete`

**External-facing** (sends email or creates shareable links):
- `teams_invite`, `workspaces_invite_link_create`

**Financial / on-chain** (mints tokens, transfers value, or charges credits):
- `catalogue_proposals_accept`, `catalogue_proposals_reject`, `team_splits_set`, `workspace_splits_set`, `register_content_for_revenue`, `generate_platform_key`

For each invocation, confirm: (a) the exact target (platform, account, workspace, content), (b) visibility and schedule where relevant, (c) any associated cost or credit consumption. The user's approval applies to a single invocation only — re-confirm on each call.

## 3. AUTHENTICATION

- **Get your key:** jubjubapp.com → Profile → Agents → Create New Agent
- **Header:** `X-JubJub-Agent-Key: jjagent_YOUR_KEY`
- **Base URL:** `https://api.jubjubapp.com`

## 4. PRICING

JubJub uses two unrelated pricing models. Which one applies depends entirely on who is calling.

### 4.1 Humans — SaaS subscription (AUD via Stripe)

For humans signed in at studio.jubjubapp.com. All plans include unlimited multi-platform publishing, on-chain records, and unmetered access to every tool. Plans differ in workspace permanence, storage, and collaboration features. Human users never pay per-action USDC fees regardless of plan.

| Plan    | Monthly (AUD) | Annual (AUD/mo) | Workspace TTL | Collections |
|---------|---------------|------------------|---------------|-------------|
| Free    | $0            | $0               | 7 days        | No          |
| Creator | $39           | $31 (20% off)    | Permanent     | Yes         |
| Studio  | $199          | $159 (20% off)   | Permanent     | Yes         |

Sign up: studio.jubjubapp.com/auth?tab=signup
Creator: studio.jubjubapp.com/checkout?plan=creator
Studio: studio.jubjubapp.com/checkout?plan=studio

### 4.2 Agents — per-action (USDC via x402 or MPP)

For autonomous agents calling the MCP server without a human session. Each priced tool charges a small USDC fee on invocation. Creator AND Studio subscribers are both exempt — pass a session credential and pay nothing per call.

| Tool                          | Cost (USDC) | Rails                      |
|-------------------------------|-------------|----------------------------|
| contents_create               | $0.25       | x402, MPP, HTTP            |
| launches_create               | $0.25       | x402, MPP, HTTP            |
| get_publish_recommendations   | $0.002      | x402, MPP, HTTP            |
| get_content_analytics         | $0.005      | x402, MPP, HTTP            |
| get_platform_comparison       | $0.005      | x402, MPP, HTTP            |
| get_content_ownership         | $0.005      | x402, MPP, HTTP            |
| get_content_revenue           | $0.005      | x402, MPP, HTTP            |
| get_creator_intelligence      | $0.005      | x402, MPP (MCP rail only)  |

Payment rails:
- **x402** — USDC on Base. Credential passed at `_meta["x402-payment"]`.
- **MPP** — USDC on Tempo. Credential passed at `_meta["org.paymentauth/credential"]`.

All MCP-served priced tools surface both rails via the JSON-RPC -32042 challenge. The HTTP `/v2/paid/{tool}` surface is x402-only and live for every priced tool except `get_creator_intelligence` (HTTP route currently disabled pending an upstream fix).

To bypass per-action pricing entirely, subscribe to Creator or Studio: studio.jubjubapp.com/profile/subscription

## 5. TOOLS

### Workspaces (6 tools)

| Tool | Description |
|------|-------------|
| `workspaces_create` | Create a new workspace. Required: `name`. Optional: `description`. |
| `workspaces_list` | List workspaces for the current user. Optional filters: `team_id`, `role`, `limit`, `offset`. |
| `workspaces_get` | Get workspace details. Required: `workspace_id`. |
| `workspaces_update` | Update workspace name or description. Required: `workspace_id`. Optional: `name`, `description`. |
| `workspaces_delete` | Delete a workspace. Required: `workspace_id`. Destructive. |
| `workspaces_invite_link_create` | Generate a shareable invite link for a workspace — recipients can view content without an account and are prompted to sign up free to comment or approve. |

### Content (5 tools)

| Tool | Description |
|------|-------------|
| `contents_create` | Create a content item. Required: `workspace_id`, `title`, `video_id`. Optional: `description`, `thumbnail_id`, `tags`, `language`, `is_made_for_kids`. **Payment required** for agent callers without an active subscription ($0.25 USDC). Pass x402 credential at `_meta["x402-payment"]` or MPP credential at `_meta["org.paymentauth/credential"]`. Returns `_payment` with `payment_verified`, `protocol`, `payment_id` on success. Subscribe to avoid per-action charges: studio.jubjubapp.com/profile/subscription |
| `contents_list` | List content in a workspace. Required: `workspace_id`. Optional: `status`, `limit`, `offset`. |
| `contents_get` | Get content details. Required: `content_id`. |
| `contents_update` | Update content fields. Required: `content_id`. Optional: `title`, `description`, `tags`, `video_id`, `thumbnail_id`, `language`, `is_made_for_kids`. |
| `contents_delete` | Delete content and associated resources. Required: `content_id`. Optional: `force` (bool). Destructive. |

### Platform Configs (3 tools)

| Tool | Description |
|------|-------------|
| `platform_configs_create` | Create a platform configuration linking content to a credential. Required: `content_id`, `platform` (tiktok/instagram/youtube/facebook/linkedin/vimeo/vimeo_ott/mux), `credential_id`. Optional: `settings`, `visibility`/`privacy`. Mux defaults: playback_policy=public, mp4_support=standard. |
| `platform_configs_list` | List platform configs for a content item. Optional: `content_id`. |
| `platform_configs_update` | Update platform config settings. Required: `config_id`. Optional: `settings`. |

### Launches (5 tools)

| Tool | Description |
|------|-------------|
| `launches_create` | Create a launch to publish or schedule content. Required: `content_id`, `platform_config_ids` (array). Optional: `scheduled_for` (ISO 8601 with timezone offset). **Payment required** for agent callers without an active subscription ($0.25 USDC). Pass x402 credential at `_meta["x402-payment"]` or MPP credential at `_meta["org.paymentauth/credential"]`. Returns `_payment` with `payment_verified`, `protocol`, `payment_id` and `_ownership` with on-chain proof details (transaction hash available in Vault once the onchain worker confirms). Subscribe to avoid per-action charges: studio.jubjubapp.com/profile/subscription |
| `launches_get` | Get launch details including per-platform status. Required: `launch_id`. |
| `launches_list` | List launches. Required: `workspace_id`. Optional: `limit`, `offset`. |
| `launches_cancel` | Cancel a scheduled launch. Required: `launch_id`. Destructive. |
| `launches_retry` | Retry a failed launch. Required: `launch_id`. Optional: `data` (object). |

### Analytics & Intelligence (8 tools)

| Tool | Description |
|---|---|
| get_publish_recommendations | Get personalised data-driven recommendations for a video before publishing, based on the creator's historical performance. Required: content_id. **$0.002 USDC for agent callers without an active subscription.** Pass x402 credential at `_meta["x402-payment"]` or MPP credential at `_meta["org.paymentauth/credential"]`. |
| get_content_analytics | Retrieve performance analytics for a piece of content across all platforms it was published to. Required: content_id. **$0.005 USDC for agent callers without an active subscription.** |
| refresh_content_analytics | Trigger a fresh analytics fetch right now for a piece of content, pulling latest stats from all connected platforms. Required: content_id. Free. |
| get_platform_comparison | Compare performance of a piece of content across every platform it was published to. Required: content_id. **$0.005 USDC for agent callers without an active subscription.** |
| get_portfolio_analytics | Retrieve aggregated performance analytics across all content a user has published. Free. |
| get_content_ownership | Get on-chain ownership details for a piece of content — token holders, percentages, contract addresses. Required: content_id. **$0.005 USDC for agent callers without an active subscription.** |
| get_content_revenue | Get streaming revenue stats for a content item directly from the smart contract. Required: content_id. **$0.005 USDC for agent callers without an active subscription.** |
| get_creator_intelligence | Retrieve the full content intelligence profile for a creator — personalised patterns derived from their channel history. Required: profile_id. **$0.005 USDC for agent callers without an active subscription. MCP rail only — HTTP route disabled pending upstream fix.** |

### Wallet & Holdings (3 tools)

| Tool | Description |
|---|---|
| get_my_tokens | List all content where the current user holds ownership tokens — full token portfolio with percentages and contract addresses. Free. |
| get_my_claimable | Total claimable USDC balance across all content the user holds tokens for, broken down by content. Reads live from smart contracts on Base. Free. |
| get_wallet_balance | Current user's total spendable USDC balance — smart wallet balance plus pending claimable. Free. |

### Teams (14 tools)

| Tool | Description |
|------|-------------|
| `teams_create` | Create a new team. Required: `name`. Optional: `description`. |
| `teams_list` | List teams for the current user. |
| `teams_get` | Get team details. Required: `team_id`. |
| `teams_update` | Update team name, description, or avatar. Required: `team_id`. Optional: `name`, `description`, `avatar_url`. |
| `teams_delete` | Delete a team. Required: `team_id`. Destructive. |
| `teams_transfer` | Transfer team ownership. Required: `team_id`, `new_owner_profile_id`. Destructive. |
| `teams_members_list` | List team members. Required: `team_id`. |
| `teams_members_update` | Update a member's role. Required: `team_id`, `member_profile_id`, `role`. Optional: `custom_permissions`. |
| `teams_members_remove` | Remove a member from a team. Required: `team_id`, `member_profile_id`. Destructive. |
| `teams_leave` | Leave a team. Required: `team_id`. Destructive. |
| `teams_permissions` | Get your permissions for a team. Required: `team_id`. |
| `teams_stats` | Get team statistics. Required: `team_id`. |
| `teams_search` | Search teams by name. Required: `query`. |
| `teams_activity` | Get recent team activity. Required: `team_id`. |

### Team Invites (6 tools)

| Tool | Description |
|------|-------------|
| `teams_invite` | Invite someone to a team by email. Required: `team_id`, `invitee_email`, `role`. Optional: `custom_permissions`. |
| `teams_invites_list` | List invitations for a team. Required: `team_id`. Optional: `status`. |
| `teams_invites_cancel` | Cancel a pending invite. Required: `team_id`, `invite_id`. Destructive. |
| `teams_invites_pending` | List pending invites for the current user. |
| `teams_invites_accept` | Accept a team invitation. Required: `invite_id`. |
| `teams_invites_reject` | Reject a team invitation. Required: `invite_id`. |

### Team Workspaces (3 tools)

| Tool | Description |
|------|-------------|
| `teams_workspaces_link` | Link an existing workspace to a team. Required: `team_id`, `workspace_id`. |
| `teams_workspaces_unlink` | Unlink a workspace from a team. Required: `team_id`, `workspace_id`. Destructive. |
| `teams_workspaces_list` | List workspaces linked to a team. Required: `team_id`. |

### Communication (6 tools)

| Tool | Description |
|------|-------------|
| `communication_create` | Send a message in a scope (team, workspace, content, media, or collection). Required: `scope_type`, `scope_id`, `body`. Optional: `parent_message_id`, `thread_root_id`, `message_type`, `decision_type`, `mentions`, `metadata`. |
| `communication_list` | List messages by scope. Required: `scope_type`, `scope_id`. Optional: `limit`, `cursor`, `thread_root_id`. |
| `communication_get` | Get a single message by ID. Required: `message_id`. Useful for fetching messages referenced in notifications without knowing the scope. |
| `communication_edit` | Edit a message. Required: `message_id`. Optional: `body`, `mentions`, `metadata`. |
| `communication_delete` | Soft-delete a message. Required: `message_id`. Destructive. |
| `communication_resolve` | Resolve a decision message (approve/reject/withdraw). Required: `message_id`, `decision_status`. Optional: `resolution`. |

### Notifications (2 tools)

| Tool | Description |
|------|-------------|
| `notifications_list` | List notifications for the current user. Optional: `cursor`, `limit`, `unread_only`. |
| `notifications_mark_read` | Mark a notification as read. Required: `notification_id`. |

### Credentials (4 tools)

| Tool | Description |
|------|-------------|
| `credentials_list` | List all connected platform credentials. Optional: `platform` filter. |
| `credentials_list_by_platform` | List credentials grouped by platform. Returns all platforms with their connected accounts. |
| `credentials_connect` | Start OAuth flow to connect a platform account. Required: `platform` (tiktok/instagram/youtube/facebook/linkedin/vimeo). Returns an auth URL the user must open in their browser. |
| `credentials_connect_token` | Connect a token-based platform (Mux or Vimeo OTT) using API credentials. Required: `platform` (mux or vimeo_ott), `token_id`, `token_secret`. Optional: `nickname`. |

### Profiles (3 tools)

| Tool | Description |
|------|-------------|
| `profiles_search` | Look up a user profile by email. Required: `email`. Returns profile_id for use in team and member operations. |
| `profiles_get` | Get a user profile by ID. Required: `profile_id`. |
| `profiles_batch` | Batch get multiple profiles. Required: `ids` (array or comma-separated string, max 50). |

### Media & Uploads (5 tools)

| Tool | Description |
|------|-------------|
| `media_ingest_url` | Ingest media from a public URL (server-side fetch). Required: `url`, `workspace_id`. Optional: `filename`. |
| `upload_sessions_create_link` | Create a browser upload link. Required: `workspace_id`. Returns a URL the user must open to upload files. |
| `upload_sessions_get` | Get upload session status and groupings. Required: `upload_session_id`, `token`. Poll until status reaches `groupings_inferred`. |
| `upload_sessions_infer_groupings` | Trigger grouping inference on an upload session. Required: `upload_session_id`, `token`. |
| `upload_sessions_confirm_groupings` | Confirm inferred groupings. Required: `upload_session_id`, `token`, `groupings`. |

### Collections (3 tools)

| Tool | Description |
|------|-------------|
| `collections_create` | Create a collection in a workspace. Required: `workspace_id`, `name`. Optional: `description`. |
| `collections_list` | List collections in a workspace. Required: `workspace_id`. |
| `collections_get` | Get collection details. Required: `collection_id`. |

### System (1 tool)

| Tool | Description |
|------|-------------|
| `mcp_version` | Returns the MCP server version. No parameters. Use to verify connectivity. |

## 6. KEY CONCEPTS

- **Workspace** — Container for content, media, and collaboration. Created unlinked; link to a team via `teams_workspaces_link`.
- **Content item** — A single publishable piece. One content item maps to one publishing event. Requires a `video_id` from an uploaded file.
- **Platform config** — Links a content item to a platform credential with platform-specific settings. Create one per platform, all on the same content item.
- **Launch** — The publish event. Takes a `content_id` and `platform_config_ids`. Can be immediate or scheduled via `scheduled_for`.
- **On-chain record** — Every launch creates a verified record on Base blockchain for proof of ownership.

## 7. COMMON WORKFLOWS

**Publish a video:**
1. `workspaces_create`
2. `upload_sessions_create_link`
3. User uploads
4. Poll `upload_sessions_get`
5. `contents_create` with `video_id` from groupings
6. `platform_configs_create` per platform
7. **Confirm with the user before publishing.** Surface the target platforms, visibility, schedule, and account to the user. Wait for explicit approval before invoking `launches_create`.
8. `launches_create`

**Invite a team member:**
1. `teams_invite` with their email → they accept via `teams_invites_accept`

**Connect a platform (OAuth — TikTok, Instagram, YouTube, Facebook, LinkedIn, Vimeo):**
1. `credentials_connect` → user opens auth URL in browser → poll `credentials_list` to confirm

**Connect a platform (API token — Mux, Vimeo OTT):**
1. `credentials_connect_token` with platform, token_id, token_secret → connection confirmed immediately

## 8. EXAMPLE PROMPTS

1. "Publish my latest video to TikTok and Instagram at 3pm EST tomorrow."
2. "Create a new workspace called 'March Campaign' for my marketing team."
3. "Send a message to the Spring Launch workspace saying the video is ready for review."
4. "What's the status of my last launch?"
5. "Schedule this video to YouTube and LinkedIn for next Monday at 9am PST."
6. "Add jamie@example.com to my content team as an editor."
7. "Check my unread notifications."
8. "List all my workspaces."
9. "Connect my TikTok account."
10. "Show me all pending team invitations."

## 9. ON-CHAIN ECONOMICS

These flows are separate from sections 4.1 and 4.2 — neither humans nor agents pay these directly.

**Treasury-paid gas.** JubJub pays all on-chain gas from the operator wallet — contract deploys, token mints, wallet registrations, publish-ledger writes (recordLaunch), streaming session create/settle/close, and recovery worker retries. Users and agents never pay gas.

**Immutable 97/3 revenue split.** Streaming revenue is split inside JubJubPaymentRouter on-chain: 97% to the content's rights holders (routed through the content contract and catalogue to token holders), 3% to JubJub treasury. This is enforced in the smart contract and cannot be turned off, renegotiated, or set per content.

**Viewer-paid streaming.** Viewers watching monetised playback pay $0.005 USDC per minute, capped at $2.00 per session, settled to chain every 60 seconds. This is the viewer's spend, not the agent's or the creator's. USDC flows: viewer → Router → content contract → catalogue → token holders, with the 3% treasury slice diverted along the way.

The agent must never initiate any on-chain operation without surfacing the relevant context to the user. The smart contract may execute autonomously once triggered, so user confirmation must happen before invocation, not after.

## 10. NOTES

- The `video_id` field in `contents_create` comes from upload session groupings (`video_media_id`) or `media_ingest_url`.
- `scheduled_for` must include a timezone offset (e.g., `2026-03-15T15:00:00-05:00`). Naive datetimes default to UTC.
- Upload sessions produce a browser URL — the user must open it to upload. The agent polls `upload_sessions_get` until groupings are ready.
- `credentials_connect` returns an auth URL — the user must complete OAuth in their browser. The agent polls `credentials_list` to confirm connection.
- Team roles: OWNER > ADMIN > MANAGER > EDITOR > PUBLISHER > VIEWER.
- Workspaces are always created unlinked. Use `teams_workspaces_link` to associate a workspace with a team.
- Profile tools (`profiles_search`, `profiles_get`, `profiles_batch`) resolve human-readable emails to `profile_id` values needed by team and member operations.
- Free plan workspaces expire after 7 days. Upgrade to Creator or Studio for permanent workspaces.
