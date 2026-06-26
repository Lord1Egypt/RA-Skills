---
name: instagram-posts
description: Manage Instagram Business and Creator accounts via the Instagram Graph API. Publish posts and carousels, retrieve media and insights, moderate comments, send DMs, and manage story content. Use this skill when users want to manage Instagram content, analyze engagement, or automate social media workflows.
---

# Instagram

![Instagram](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/instagram.svg)

Manage an Instagram Business or Creator account via the Instagram Graph API. Publish posts and carousels, retrieve media and insights, moderate comments, send direct messages, and monitor story content.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=instagram-posts) for hosted connection flows and credentials so you do not need to configure Instagram API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Instagram |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | ![Connect](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/instagram.gif) |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Instagram |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Instagram Graph  │
│   (User Chat)   │     │   (OAuth)    │     │   (API v22)     │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin  │                       │
         │  2. Pair Device   │                       │
         │  3. Connect IG    │                       │
         │                   │  4. Secure Token      │
         │                   │  5. Proxy Requests    │
         │                   │                       │
         ▼                   ▼                       ▼
   ┌──────────┐      ┌──────────┐           ┌──────────┐
   │  SKILL   │      │ Dashboard│           │ Instagram│
   │  File    │      │ Auth     │           │ Business │
   └──────────┘      └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Instagram again."

## Quick Start

```bash
# Get your Instagram account info
clawlink_call_tool --tool "instagram_get_user_info" --params '{}'

# List recent media posts
clawlink_call_tool --tool "instagram_get_ig_user_media" --params '{}'

# Get insights on a specific post
clawlink_call_tool --tool "instagram_get_ig_media_insights" --params '{"media_id": "MEDIA_ID"}'
```

## Authentication

All Instagram tool calls are authenticated automatically by ClawLink using the user's connected Instagram Business or Creator account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Instagram Graph API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=instagram and connect Instagram (requires a Business or Creator account).
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `instagram` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration instagram
```

**Response:** Returns the live tool catalog for Instagram.

### Reconnect

If Instagram tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=instagram
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration instagram`

## Security & Permissions

- Access is scoped to the connected Instagram Business or Creator account only.
- A Business or Creator account is required — personal Instagram accounts are not supported by the Instagram Graph API.
- **All write operations require explicit user confirmation.** Before executing any publish, comment, or DM action, confirm the target resource and intended effect with the user.
- Destructive actions (delete comment, delete message) are marked as high-impact and must be confirmed.
- Content publishing is rate-limited by Instagram (25 posts per 24-hour window per account).

## Tool Reference

### Media Retrieval & Publishing

| Tool | Description | Mode |
|------|-------------|------|
| `instagram_get_ig_user_media` | List all media (posts, photos, videos, reels, carousels) published by the account | Read |
| `instagram_get_ig_media` | Get details for a specific published media item including engagement metrics | Read |
| `instagram_get_ig_media_children` | Get individual media items from a carousel/album post | Read |
| `instagram_post_ig_user_media` | Create a media container for publishing (first step of two-step publish) | Write |
| `instagram_post_ig_user_media_publish` | Publish a media container to the account (auto-waits for processing) | Write |
| `instagram_create_carousel_container` | Create a draft carousel post with 2–10 images/videos | Write |

### Insights & Analytics

| Tool | Description | Mode |
|------|-------------|------|
| `instagram_get_user_insights` | Get account-level insights (profile views, reach, follower count) | Read |
| `instagram_get_ig_media_insights` | Get per-media performance metrics (views, likes, comments, saves, shares) | Read |
| `instagram_get_user_info` | Get profile details and statistics for the Business/Creator account | Read |
| `instagram_get_ig_user_content_publishing_limit` | Check remaining publish quota before posting | Read |

### Comments & Replies

| Tool | Description | Mode |
|------|-------------|------|
| `instagram_get_ig_media_comments` | List comments on a specific post with cursor-based pagination | Read |
| `instagram_get_ig_comment_replies` | Get replies to a specific comment | Read |
| `instagram_post_ig_media_comments` | Post a comment on a media item (300 chars max, 4 hashtags, 1 URL) | Write |
| `instagram_post_ig_comment_replies` | Reply to an existing comment (300 chars max) | Write |
| `instagram_delete_comment` | Delete a comment (only comments your account created) | Write |

### Stories & Live

| Tool | Description | Mode |
|------|-------------|------|
| `instagram_get_ig_user_stories` | List active stories within the 24-hour story window | Read |
| `instagram_get_ig_user_live_media` | Get live media during an active broadcast | Read |

### Conversations & Messaging

| Tool | Description | Mode |
|------|-------------|------|
| `instagram_list_all_conversations` | List all Instagram DM conversations | Read |
| `instagram_get_conversation` | Get details of a specific DM conversation | Read |
| `instagram_list_all_messages` | List messages in a specific DM thread | Read |
| `instagram_send_text_message` | Send a text DM (requires prior conversation thread) | Write |
| `instagram_send_image` | Send an image via DM | Write |
| `instagram_mark_seen` | Mark messages as read in a DM thread | Write |
| `instagram_get_page_conversations` | Get conversations for the connected Page | Read |

### Messaging Configuration

| Tool | Description | Mode |
|------|-------------|------|
| `instagram_get_messenger_profile` | Get ice breakers and messaging settings | Read |
| `instagram_update_messenger_profile` | Configure ice breakers for the Instagram inbox | Write |
| `instagram_delete_messenger_profile` | Remove messaging configuration | Write |

### Mentions & Tags

| Tool | Description | Mode |
|------|-------------|------|
| `instagram_get_ig_user_tags` | Get media where your account was tagged by others | Read |
| `instagram_post_ig_user_mentions` | Reply to a mention of your account | Write |

## Code Examples

### Get account info and insights

```bash
clawlink_call_tool --tool "instagram_get_user_info" \
  --params '{}'
```

### List recent posts with insights

```bash
clawlink_call_tool --tool "instagram_get_ig_user_media" \
  --params '{}'
```

### Get insights for a specific post

```bash
clawlink_call_tool --tool "instagram_get_ig_media_insights" \
  --params '{"media_id": "MEDIA_ID"}'
```

### Post a comment

```bash
clawlink_call_tool --tool "instagram_post_ig_media_comments" \
  --params '{"media_id": "MEDIA_ID", "text": "Great post! Thanks for sharing."}'
```

### Send a DM

```bash
clawlink_call_tool --tool "instagram_send_text_message" \
  --params '{"message": "Hi! Thanks for reaching out.", "conversation_id": "CONVERSATION_ID"}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Instagram is connected.
2. Call `clawlink_list_tools --integration instagram` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `instagram`.
5. If no Instagram tools appear, direct the user to https://claw-link.dev/dashboard?add=instagram.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List media → Get insights → Show results          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Preview comment → User approves → Execute         │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Only **Business** or **Creator** Instagram accounts are supported — personal accounts return permission errors.
- Content publishing is limited to 25 API-published posts per 24-hour moving window per account.
- Media container `creation_id`s expire in under 24 hours — publish promptly after creating a container.
- Comments are limited to 300 characters, 4 hashtags, and 1 URL.
- DMs can only be sent in existing conversation threads — new threads cannot be initiated via the API.
- Insights data is only available for posts published within the last 2 years and requires at least 1,000 followers.
- Instagram IDs in API responses use the format `1784140xxxxx` (not numeric strings).

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration instagram`. |
| Missing connection | Instagram is not connected. Direct the user to https://claw-link.dev/dashboard?add=instagram. |
| Permission error | The account is a personal Instagram profile, not a Business/Creator account. |
| ` OAuthException` | Instagram OAuth token is invalid or expired. Reconnect Instagram. |
| Rate limit exceeded | Publishing quota used. Wait or reduce publish frequency. |
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

### Troubleshooting: Permission Errors

1. Confirm the Instagram account is a **Business** or **Creator** account, not personal.
2. Verify the account is connected at https://claw-link.dev/dashboard?add=instagram.
3. For messaging tools, ensure the Instagram account has the **Instagram Messaging** permission scope.

## Resources

- [Instagram Graph API Overview](https://developers.facebook.com/docs/instagram-api)
- [Instagram Media Publishing API](https://developers.facebook.com/docs/instagram-api/reference/ig-media)
- [Instagram Insights API](https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights)
- [Instagram Messaging API](https://developers.facebook.com/docs/instagram-api/reference/ig-user/conversations)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=instagram-posts
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [LinkedIn Social](https://clawhub.ai/hith3sh/linkedin-social) — For LinkedIn page and post management
- [Twitter](https://clawhub.ai/hith3sh/twitter) — For Twitter/X post management and analytics
- [Facebook Pages](https://clawhub.ai/hith3sh/facebook-pages) — For Facebook Page management

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=instagram-posts)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
