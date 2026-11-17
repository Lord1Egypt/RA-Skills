---
name: jubjub
description: Media ownership and payment infrastructure over MCP. Publish a video to TikTok, Instagram, YouTube, Facebook, LinkedIn, Vimeo, Vimeo OTT, Mux and Farcaster in one launch, get an on-chain ownership record when it goes out, and search or buy media metadata per use over x402 or MPP.
version: 1.3.0
metadata:
  clawdbot:
    emoji: "🎬"
    requires:
      env:
        - JUBJUB_API_KEY
    primaryEnv: JUBJUB_API_KEY
---

# JubJub

## 1. Overview

JubJub is media ownership and payment infrastructure. One launch publishes a piece to every platform it is set up for. When the piece goes out, JubJub writes its ownership record on Base, and payment for it routes to every rights holder.

Agents reach all of it over one MCP server:

```
https://api.jubjubapp.com/v2/mcp
```

What an agent can do through this skill:

- Publish a video to TikTok, Instagram, YouTube, Facebook, LinkedIn, Vimeo, Vimeo OTT, Mux and Farcaster from one launch, now or on a schedule. X is not supported.
- Read each destination's result, and send a failed destination again.
- Read the ownership record of a piece and who holds it.
- Search the JubJub media catalogue for free, then buy a piece's metadata or the piece itself per use.
- Track analytics per piece and across a whole catalogue.
- Run a team: workspaces, versions, reviewers and approvals, comments, share links.

## 2. Confirmation required

Several JubJub actions are public, destructive or financial. Before calling any tool below, the agent MUST show the user the planned action (target platforms, account, visibility, schedule, and whether the call moves money) and wait for an explicit yes. Do not chain these inside a multi-step workflow without a confirmation step.

**Public publishing** (goes out to outside platforms and is hard to fully undo):
- `launches_create`, `launches_retry`, `launches_reschedule`

**Destructive** (permanent or hard to reverse):
- `contents_delete`, `media_delete`, `workspaces_delete`, `workspaces_transfer`, `teams_delete`, `teams_transfer`, `teams_members_remove`, `launches_cancel`, `credentials_delete`, `platform_configs_delete`, `communication_delete`, `notifications_delete`, `agents_delete`, `contents_share_link_revoke`

**External-facing** (sends email or creates a link anyone can open):
- `teams_invite`, `workspaces_invite_link_create`, `contents_share_link_create`, `teams_connect_email_send`

**Financial and on-chain** (spends, routes money, or changes who owns what):
- `purchase_metadata`, `purchase_content`, `cards_mint`, `cards_top_up`, `catalogue_proposals_accept`, `catalogue_proposals_reject`, `team_splits_set`, `workspace_splits_set`, `workspace_ownership_opt_out`, `workspace_ownership_opt_in`, `register_content_for_revenue`, `generate_platform_key`, `meta_ads_select`, `meta_ads_request_activation`

For each call, confirm (a) the exact target (platform, account, workspace, content), (b) visibility and schedule where they apply, and (c) whether the call spends or routes money. One yes covers one call only. Ask again for the next one.

## 3. Connect

- **MCP endpoint:** `https://api.jubjubapp.com/v2/mcp` (streamable HTTP).
- **Agent key:** jubjubapp.com, then Profile, Agents, Create new agent. The key starts with `jjagent_`. Send it as the header `X-JubJub-Agent-Key: jjagent_YOUR_KEY`.
- **OAuth:** an MCP client that supports OAuth can add the endpoint with no key and sign in when asked.
- **No account yet:** a person signs up free at https://studio.jubjubapp.com/auth. An agent with its own wallet can create an account itself, free, with `get_wallet_signin_nonce` then `create_jubjub_account_with_wallet`.

On connect the server lists a core set of tools. Every other tool is still there: `jubjub_find_tools` lists the areas and returns any tool's schema, and `jubjub_call_tool` calls any tool by name.

## 4. How payment works

- Publishing, analytics, ownership reads, team work and catalogue search cost an agent nothing.
- Agents pay per use only to unlock a piece from the catalogue: `purchase_metadata` for its structured metadata, `purchase_content` for the full piece. Each has a fixed price, set by JubJub and quoted by the server in its payment challenge before anything is charged.
- Two payment rails: x402 (USDC on Base) and MPP (USDC on Tempo). Pass an x402 credential at `_meta["x402-payment"]` or an MPP credential at `_meta["org.paymentauth/credential"]`. A call without one gets the challenge back, with both rails, so the agent can show the user what it will pay before paying.
- Every account can turn agent discovery and purchase off. With it off, that account's work does not appear in agent search and cannot be bought by agents. The switch is in account settings, or `profiles_update` with `ai_agent_discovery` set to false.
- People never pay to use JubJub. JubJub earns a small fee on settled revenue, when money moves.

Never quote a price from memory. Read it from the payment challenge the server returns.

## 5. Tools

Names below are as the server registers them today. Call `jubjub_find_tools` for each tool's full schema.

### Start and discovery

| Tool | What it does |
|------|-------------|
| `welcome` | A short orientation and what to try first. |
| `mcp_version` | Server version and recent changes. Use it to check the connection. |
| `get_signup_url` | The sign-up link to give a person with no account. |
| `get_wallet_signin_nonce`, `create_jubjub_account_with_wallet` | An agent signs in with its wallet and creates its own account, free. |

### Catalogue and purchase

| Tool | What it does |
|------|-------------|
| `media_search` | Search the catalogue. Free. |
| `jubjub_catalogue_manifest` | What the catalogue holds and how to buy from it. Free. |
| `purchase_metadata` | Unlock one piece's structured metadata. Paid per use over x402 or MPP. Confirm first. |
| `purchase_content` | Unlock one piece in full. Paid per use over x402 or MPP. Confirm first. |
| `content_playback_get` | How to play a piece, and whether playback is paid. |

### Workspaces and content

| Tool | What it does |
|------|-------------|
| `workspaces_create`, `workspaces_list`, `workspaces_get`, `workspaces_update` | Create and manage workspaces. |
| `workspaces_archive`, `workspaces_unarchive` | Archive a workspace and bring it back. |
| `contents_create`, `contents_list`, `contents_get`, `contents_update` | Create and manage content items. `contents_create` needs a `video_id` from an upload. |
| `contents_versions_list`, `contents_versions_add`, `contents_versions_make_current`, `contents_versions_review` | Versions of a piece, and a reviewer's approval or change request. |
| `contents_share_link_create`, `contents_share_link_get` | One link that plays one piece, no sign-in. Confirm before creating. |
| `upload_sessions_create_link`, `upload_sessions_get` | A browser upload link for the user, then its status. |
| `media_ingest_url` | Bring in media from a public URL. |

### Publishing

| Tool | What it does |
|------|-------------|
| `credentials_list`, `credentials_connect`, `credentials_connect_token` | See connected accounts; connect a platform by OAuth, or Mux and Vimeo OTT by token. |
| `connect_farcaster` | Connect Farcaster. |
| `platform_configs_create`, `platform_configs_list`, `platform_configs_update` | One config per destination, all on the same content item. |
| `platform_configs_get_schemas`, `platform_configs_get_requirements` | What each platform's config accepts and needs. |
| `launches_validate` | Check a launch before it goes out. |
| `launches_create` | Publish now, or at `scheduled_for`. Confirm first. |
| `launches_get`, `launches_list` | Each destination's result. |
| `launches_retry`, `launches_reschedule`, `launches_cancel` | Send a failed destination again, move a scheduled launch, or cancel it. Confirm first. |

### Ownership, analytics and money

| Tool | What it does |
|------|-------------|
| `get_content_ownership` | The on-chain ownership record of a piece and its holders. |
| `get_content_revenue` | Revenue recorded for a piece. |
| `get_content_analytics`, `get_platform_comparison`, `refresh_content_analytics` | One piece's numbers, by platform. |
| `get_portfolio_analytics` | Numbers across everything published. |
| `catalogue_get` | The account's catalogue. |
| `get_wallet_balance`, `get_my_claimable`, `get_my_tokens` | Balance, what can be claimed, and holdings. |
| `cards_contract_info`, `cards_mint_quote`, `cards_mint`, `cards_top_up`, `cards_get`, `cards_list` | A prepaid card on Base for paid viewing. Confirm before minting or topping up. |

### Teams and collaboration

| Tool | What it does |
|------|-------------|
| `teams_create`, `teams_list`, `teams_get`, `teams_update`, `teams_members_list`, `teams_members_update` | Create and run a team. |
| `teams_invite`, `teams_invites_list`, `teams_invites_pending`, `teams_invites_accept`, `teams_invites_reject` | Invitations. `teams_invite` sends an email: confirm first. |
| `teams_workspaces_link`, `teams_workspaces_list` | Put a workspace under a team. |
| `communication_create`, `communication_list`, `communication_get`, `communication_resolve` | Comments and decisions on a team, workspace or piece. |
| `approvals_get_pending`, `approvals_decide` | Approvals waiting on the user. |
| `notifications_list`, `notifications_mark_read` | Notifications. |

## 6. Key ideas

- **Workspace.** Holds content, media and conversation. Created on its own; link it to a team with `teams_workspaces_link`.
- **Content item.** One piece to publish. It needs a `video_id` from an upload.
- **Platform config.** Ties a content item to one connected account, with that platform's settings.
- **Launch.** The publish. Takes a `content_id` and a list of `platform_config_ids`, now or at `scheduled_for`.
- **Ownership record.** Written on Base when a piece goes out, never at upload.

## 7. Common workflows

**Publish a video:**
1. `workspaces_create`
2. `upload_sessions_create_link`, and the user uploads in the browser
3. Poll `upload_sessions_get` until the upload is grouped
4. `contents_create` with the `video_id` from the grouping
5. `platform_configs_create`, once per destination
6. `launches_validate`
7. **Confirm with the user:** platforms, accounts, visibility and schedule. Wait for a yes.
8. `launches_create`, then `launches_get` for each destination's result

**Find and buy a piece's metadata:**
1. `media_search` (free)
2. Call `purchase_metadata` with no credential to get the payment challenge
3. **Confirm with the user:** the piece and the price the challenge quotes. Wait for a yes.
4. Call `purchase_metadata` again with the x402 or MPP credential

**Connect a platform:**
1. OAuth platforms: `credentials_connect`, the user opens the link, then poll `credentials_list`
2. Mux or Vimeo OTT: `credentials_connect_token` with the token id and secret

**Invite a team member:**
1. **Confirm the email address with the user**, then `teams_invite`. They accept with `teams_invites_accept`.

## 8. Example prompts

1. "Publish my latest video to TikTok and Instagram at 3pm tomorrow."
2. "Schedule this video to YouTube and LinkedIn for Monday at 9am."
3. "What happened with my last launch? Retry anything that failed."
4. "Who holds the ownership record for this video?"
5. "How did my videos do this month across every platform?"
6. "Find 3 clips about street food in the JubJub catalogue."
7. "Add jamie@example.com to my content team as an editor."
8. "Turn off agent purchase on my account."

## 9. Notes

- `scheduled_for` needs a timezone offset, for example `2026-12-01T15:00:00+11:00`. A time with no offset is read as UTC.
- Uploads and OAuth both happen in the user's browser. The agent gives the link and polls for the result.
- People are named only by display name, avatar and handle, or by an opaque `member_ref`. No tool returns another person's email or profile id. Member, split, transfer and mention tools take `member_ref`.
- Team roles, highest first: owner, admin, manager, editor, publisher, viewer.
- If a tool seems missing, call `mcp_version`, then `jubjub_find_tools` with its name. If it is still missing, reconnect the MCP server.
