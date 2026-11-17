# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube, Facebook, LinkedIn
(profiles and pages), X, Pinterest, Threads and Bluesky. This skill uses it to post the
carousel and to read the results back. The exact fields live in the docs above; treat them as
the source of truth if anything here looks different.

## 1. Is it already connected?

Call `social_accounts_list`. If it works and lists the accounts the user wants, skip to step 3.

## 2. Connect (about 2 minutes)

The free plan includes MCP access for 2 social accounts, no card needed (more accounts need a
paid plan)
([pricing](https://woopsocial.com/pricing?utm_source=instagram-carousel-skill&utm_medium=skill)).
New users sign up in the same browser window as the sign-in, and a project is created for them.
Setup steps and prompts for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=instagram-carousel-skill&utm_medium=skill).

Give the user only the path for the agent you're running in:

| Agent | How to connect |
|---|---|
| Claude (claude.ai, Desktop, Cowork) | Add WoopSocial from the [Claude directory](https://claude.ai/directory/woopsocial), click Connect and sign in |
| Cursor | Install from [cursor.directory](https://cursor.directory/plugins/woopsocial-social-media-scheduler) and sign in |
| Claude Code | `claude mcp add --transport http woopsocial "https://api.woopsocial.com/mcp"`, then `/mcp`, select woopsocial, Authenticate |
| Codex | `codex mcp add woopsocial --url https://api.woopsocial.com/mcp`, then `codex mcp login woopsocial` |
| OpenClaw | Install the [WoopSocial skill on ClawHub](https://clawhub.ai/woopsocial/skills/social-media-scheduler), or add the MCP URL to the agent's MCP config |
| Agents without sign-in support | Create an API key at [app.woopsocial.com/api-access](https://app.woopsocial.com/api-access) and use `https://api.woopsocial.com/mcp?api_key=YOUR_API_KEY` |

The API key is a password: never paste it into shared chats or commit it.

**Connect the social accounts from the chat.** Once WoopSocial is connected, call
`oauth_create_authorization` with the project ID and the platform (Instagram). It
returns a link; the user opens it, approves, and tells you when they're done. Confirm with
`social_accounts_list`. Repeat per platform.

Find IDs yourself with `projects_list` and `social_accounts_list`; never ask the user to paste
IDs.

## 3. Upload the slides

Each slide is uploaded through an upload session:

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact size,
   listed in `carousel/manifest.json`).
2. Save the response as `session.json` and run
   `python3 scripts/upload_parts.py session.json carousel/slide-01.jpg`.
   It PUTs the bytes to the presigned URLs.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`. If
   not, poll `media_uploads_get_session` until it is `READY`; on `FAILED` or `ABORTED`, report it.

Keep the media IDs in slide order. Clients with a network allowlist must allow
`*.r2.cloudflarestorage.com` for step 2 (claude.ai: Settings > Capabilities, code execution
network settings; Claude Code: the sandbox's allowed domains). If the client can't make HTTP
requests at all, tell the user the upload isn't possible from this client and hand over the
files instead.

## 4. Validate, confirm, post

Instagram carousel:

```json
{
  "content": [{"text": "<caption>", "media": [
    {"type": "MEDIA_LIBRARY", "mediaId": "<slide 1>"},
    {"type": "MEDIA_LIBRARY", "mediaId": "<slide 2>"}
  ]}],
  "schedule": {"type": "PUBLISH_NOW"},
  "socialAccounts": [{
    "platform": "INSTAGRAM", "socialAccountId": "<id>", "postType": "POST"
  }]
}
```

- More than one image in `media` makes it a carousel. Keep the slide order.
- Instagram allows up to 20 slides; if `posts_validate` refuses a long carousel, tell the user
  plainly and cut it.
- Schedule types: `PUBLISH_NOW`, `SCHEDULE_FOR_LATER` with `scheduledFor` (UTC, ISO 8601, in the
  future), or `DRAFT`, which saves the post in WoopSocial only and sends nothing to Instagram.
- Several accounts can share one post only with identical content. Different covers or variants
  per account are separate posts (or a per-account `contentOverride`).

Always:

1. Run `posts_validate` with the exact body. Fix anything it rejects.
2. Show the user the contact sheet, caption, account and time with timezone. Wait for a clear yes.
3. `posts_create`, then `posts_get` to report what happened per account.

After it's live, tell the user what WoopSocial doesn't set yet, so they can add it in the
Instagram app: alt text per slide ("..." > Edit > Edit alt text, text in `manifest.json`),
collaborators, music.

## 5. Read results

`social_account_posts_list` returns each post with its latest stored lifetime metrics: for
Instagram these can include views, likes, comments, saves, shares and unique impressions.
Collection is asynchronous: report the collection date with each number, and treat a missing
field as "not reported", never as zero. Per-slide numbers, profile visits and follows from a
post are in the Instagram app, not in WoopSocial.

## Changing a scheduled post

There's no edit. Delete it with `posts_delete` and create it again, after confirming with the
user.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=instagram-carousel-skill&utm_medium=skill
- Agent setup: https://woopsocial.com/agents?utm_source=instagram-carousel-skill&utm_medium=skill
