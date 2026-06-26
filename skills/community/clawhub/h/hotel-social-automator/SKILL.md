---
name: media.hotelmind
description: Generate, review, and publish social media content through MCP with AgentAuth and workspace token authentication.
---

# media.hotelmind

Calls MCP tools to generate, review, and publish social media content.

---

## Prerequisites

### Required Environment

| Dependency | Purpose | Required |
|------------|---------|----------|
| `mcporter` CLI | Invoke MCP server tools | **Yes** |
| `curl` | Download images from URLs | **Yes** |
| `feishu-send` at `/usr/local/bin/feishu-send` | Send Feishu notifications | No (only if Feishu notifications needed) |
| Write access to `/root/.openclaw/workspace/` | Store temporary images | **Yes** |

**Note**: If `feishu-send` is not available, the skill will still function but cannot send notifications via Feishu.

### Required Configuration

This skill requires dual-token MCP authentication:

- `Authorization: Bearer hp_sk_*`
- `X-Agent-User-Key: uk_*`

Users must:

1. Sign in to AgentAuth and copy a `uk_*`
2. Sign in to HotelPost and create or copy a workspace `hp_sk_*`
3. Put both tokens into the installed agent's MCP configuration

Full user onboarding guide:
- `references/user-onboarding.md`

MCP server must be configured in your agent's MCP settings:

```json
{
  "mcpServers": {
    "hotelpost": {
      "type": "streamable-http",
      "url": "https://mcp.example.com/api/mcp",
      "headers": {
        "Authorization": "Bearer <API_KEY>",
        "X-Agent-User-Key": "<AGENTAUTH_USER_KEY>"
      }
    }
  }
}
```

**Required credentials:**
- **API Key**: Obtain from HotelPost Web admin panel → Settings → API Keys. Format: `hp_sk_xxxxxxxx`
- **AgentAuth User Key**: Obtain from AgentAuth Dashboard after user login. Format: `uk_xxxxxxxx`
- MCP now requires both tokens together: workspace `hp_sk_*` plus user `uk_*`

### Credit System

Content generation consumes credits:
- Each draft generation (up to 4 candidates) costs 40 credits
- Each regeneration costs 10 credits

If credit quota is exceeded, the tool returns `AIQuotaExceededError`. Ensure sufficient credits before generating content. Credits can be managed in the HotelPost Web admin panel.

### Multi-Tenant Isolation

This skill uses the HotelPost API key to resolve the target workspace and uses `X-Agent-User-Key` to verify the calling user. Both are required, and all operations remain scoped to the workspace bound to the `hp_sk_*` key.

---

## Tool Invocation

**Must use mcporter to call MCP server tools** — do NOT use exec/curl!

Correct usage:
```
mcporter call hotelpost.<tool_name> <parameters>
```

Examples:
- `mcporter call hotelpost.list_scenarios` — List marketing scenarios
- `mcporter call hotelpost.generate_content scenarioId=scenario_demo_001` — Generate content
- `mcporter call hotelpost.get_drafts draftId=draft_demo_001` — Get draft details

**Forbidden: using exec/curl to access MCP API directly. Must use mcporter!**

## MCP Server Configuration

MCP server name is `hotelpost`. Server URL and both auth headers must be configured as described above.

For full user-side setup, token acquisition, and troubleshooting:
- `references/user-onboarding.md`

## When to Activate

- User asks to generate social media posts or publish content
- User asks to browse or select marketing scenarios
- User asks to manage, view, or modify drafts
- User asks to check publishing status or post list
- User mentions HotelPost, hotel marketing, or social media publishing
- User asks to schedule posts
- Keywords: hotel, social media, post, publish, draft, marketing scenario, Instagram, X, Facebook, LinkedIn

## Core Flow

```
list_scenarios → generate_content → get_drafts (polling) → [regenerate_draft] → publish_post / schedule_post
```

## Step-by-Step

1. **Select Scenario** — Call `list_scenarios`, display available scenarios, let user choose
2. **Generate Content** — Call `generate_content(scenarioId, language)`, submit async generation task
3. **Poll Drafts** — Call `get_drafts(scenarioId)`, wait for status to change from GENERATING to ACTIVE (usually 15-30 seconds)
4. **View/Modify** — Call `get_drafts(draftId)` to view full content and images; use `regenerate_draft(draftId, feedback)` to modify
5. **Publish** — Call `list_connections` first to confirm available accounts, then call `publish_post` or `schedule_post`
6. **Check Status** — Call `get_post_status(draftId)` to confirm publishing result

## Tool Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `list_scenarios` | List marketing scenarios | none |
| `generate_content` | Generate draft based on scenario | `scenarioId`, `language?` |
| `get_drafts` | Query draft status/details | `scenarioId` or `draftId` |
| `regenerate_draft` | Regenerate with feedback, supports language/platform | `draftId`, `feedback?`, `language?`, `platform?` |
| `list_connections` | List bound social media accounts | none |
| `publish_post` | Publish immediately | `draftId`, `connectionIds[]` |
| `schedule_post` | Schedule for later | `draftId`, `connectionIds[]`, `scheduledAt` |
| `list_posts` | List posts | `status?`, `page?`, `pageSize?` |
| `get_post_status` | Get publishing status | `postId` or `draftId` |

### regenerate_draft Language Options
- `zh` — Chinese (default)
- `en` — English
- `th` — Thai
- `ms` — Malay
- `ja` — Japanese

### regenerate_draft Platform Options
- `x` — X (Twitter)
- `facebook` — Facebook
- `instagram` — Instagram
- `linkedin` — LinkedIn

### list_posts Status Options
- `SCHEDULED` — Scheduled posts
- `PUBLISHING` — Currently publishing
- `PUBLISHED` — Successfully published
- `PARTIAL_SUCCESS` — Partially succeeded
- `FAILED` — Failed

## Important Rules

### Information Display
- **Do NOT expose internal info to users**: Cards should NOT contain draft IDs, internal numbers, etc. Only show content and images the user needs to see.

### Performance Optimization
- **Image URL optimization**: The first `get_drafts(scenarioId)` response includes image URLs in the draft list. **Do NOT call `get_drafts(draftId)` again** to fetch URLs — use the URLs directly from the first call to save time.
- **Parallel processing**:
  - Download images in parallel with `&` (`curl -o "1.png" url1 & curl -o "2.png" url2 & wait`)
  - Send multiple images in parallel (with rate limiting, 3-5 at a time recommended)
  - Avoid serial operations; parallelize whenever possible

### Send Order
- **Send content first, wait, then send images**. Do not send all content at once followed by images — users cannot correlate them.

### General Rules
- Must select a scenario before generating. Do NOT skip `list_scenarios`.
- Generation is async. After `generate_content` returns, you MUST poll `get_drafts` at 10-15 second intervals, up to 3 times.
- Drafts include image assets. No need for users to provide images.
- Before publishing, must confirm account by calling `list_connections` to get connectionId.
- If user says "post to Instagram", find INSTAGRAM platform ID from connections.
- `language` defaults to `zh` (Chinese). Pass `en` when user requests English.
- If user is not satisfied with draft, use `regenerate_draft` with feedback.
- `regenerate_draft` supports specifying `language` (zh/en/th/ms/ja) and `platform` (x/facebook/instagram/linkedin). If not specified, regenerates for all platforms.

### Image Handling
1. Ensure `/root/.openclaw/workspace/` directory exists before downloading
2. Download images with random filenames like `hotelpost_xxx.png`
   - **Do NOT save to /tmp/** — some platforms don't support it
3. **Image URLs must include full signature parameters!** Truncated URLs will be inaccessible.
4. Clean up temporary files after sending.

### Workspace Directory
Before downloading images, ensure the workspace directory exists:
```bash
mkdir -p /root/.openclaw/workspace/
```

## Platform Publishing

After publishing, send notifications via the appropriate IM platform. See the platform-specific guide in `references/`:

- `feishu-guide.md` — Feishu platform sending guide (card/image format, ID selection rules)

**Note**: Feishu notification is optional. The skill functions without it, but users won't receive push notifications.

## Conversation Examples

See `references/conversation-examples.md`

## Error Handling

See `references/error-handling.md`
