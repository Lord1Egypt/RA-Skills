# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube, Facebook, LinkedIn
(profiles and pages), X, Pinterest, Threads and Bluesky. This skill uses it to schedule
image and video pins to one or more Pinterest accounts and to read the results back. Pins go out
through WoopSocial's approved Pinterest app, so they are public from the first day; you don't need
a Pinterest developer app, trial access or an app review of your own. The exact fields live in WoopSocial's API docs and MCP schema (`schema_describe`); treat them as
the source of truth if anything here looks different.

## 1. Is it already connected?

Call `social_accounts_list`. If it works and lists the accounts the user wants, skip to step 3.

## 2. Connect (about 2 minutes)

The free plan includes MCP access for 2 social accounts, no card needed (more accounts need a
paid plan)
([pricing](https://woopsocial.com/pricing?utm_source=pinterest-skill&utm_medium=skill)).
New users sign up in the same browser window as the sign-in, and a project is created for them.
Setup steps and prompts for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=pinterest-skill&utm_medium=skill). What its Pinterest MCP does: [woopsocial.com/social-media-mcp/pinterest-mcp](https://woopsocial.com/social-media-mcp/pinterest-mcp?utm_source=pinterest-skill&utm_medium=skill).

Give the user only the path for the agent you're running in:

| Agent | How to connect |
|---|---|
| Claude (claude.ai, Desktop, Cowork) | Add WoopSocial from the [Claude directory](https://claude.ai/directory/woopsocial), click Connect and sign in |
| Cursor | Install from [cursor.directory](https://cursor.directory/plugins/woopsocial-social-media-scheduler) and sign in |
| Claude Code | `claude mcp add --transport http woopsocial "https://api.woopsocial.com/mcp"`, then restart with `claude --continue` (keeps the conversation), `/mcp`, select woopsocial, Authenticate |
| Codex | `codex mcp add woopsocial --url https://api.woopsocial.com/mcp`, then `codex mcp login woopsocial`, then start a new session (`codex resume --last` keeps this one) |
| OpenClaw | Install the [WoopSocial skill on ClawHub](https://clawhub.ai/woopsocial/skills/social-media-scheduler), or add the MCP URL to the agent's MCP config |
| Agents without sign-in support | Create an API key at [app.woopsocial.com/api-access](https://app.woopsocial.com/api-access) and use `https://api.woopsocial.com/mcp?api_key=YOUR_API_KEY` |

The API key is a password: never paste it into shared chats or commit it.

**Connect the social accounts from the chat.** Once WoopSocial is connected, call
`oauth_create_authorization` with the project ID and the platform (PINTEREST). It
returns a link; the user opens it, approves, and tells you when they're done. Confirm with
`social_accounts_list`. Repeat per platform.

Find IDs yourself with `projects_list` and `social_accounts_list`; never ask the user to paste
IDs.

## 3. Read the boards

`social_accounts_get_platform_inputs` per Pinterest account returns `boards`: each board's `id` and
`name`. Put them in the plan's `accounts.<name>.boards` as name to id, so `pin_check.py` can check
each pin's board and `schedule.py` can fill `pinterestBoardId`. New boards are made in Pinterest
itself; read the list again afterwards.

## 4. Upload the media

Upload every file (after `pin_check.py` passes), one at a time:

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact byte size).
2. Save the response as `session.json` and run `python3 <skill>/scripts/upload_parts.py session.json <file>`.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`; if not,
   poll `media_uploads_get_session`; on `FAILED` or `ABORTED`, report it.

Write each ID into its pin's `mediaIds`, then
`python3 <skill>/scripts/schedule.py plan.json --bodies-only`. Upload one file at a time: parallel uploads
on one key can get HTTP 429. Clients with a network allowlist must allow
`*.r2.cloudflarestorage.com`.

## 5. Validate, confirm, schedule

`schedule.py` writes one body per pin to `requests/`:

```json
{
  "content": [{"text": "<description>", "media": [{"type": "MEDIA_LIBRARY", "mediaId": "<image or video>"}]}],
  "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-11-17T01:30:00Z"},
  "socialAccounts": [{
    "platform": "PINTEREST", "socialAccountId": "<id>",
    "pinterestBoardId": "<board id>",
    "title": "<title, up to 100 characters>",
    "link": "https://example.com/the-page"
  }]
}
```

- `content[0].text` is the pin's description; `title` and `link` sit on the Pinterest target.
- One image or one video per pin.
- `"autoDeleteMediaAfterPublish": true` at the top level deletes the uploaded file from the
  WoopSocial media library once the pin is published.
- Not in WoopSocial's Pinterest fields today: alt text, board sections, a video cover image, the
  AI disclosure. Alt text is pasted in Pinterest after publishing (`schedule.md` lists it: Edit Pin, alt text); the
  video's first frame is its cover; AI use goes in the description.

Always:

1. `posts_validate` with each exact body. Fix anything it rejects.
2. Then show the user `preview/index.html` and `schedule.md`. Wait for one clear yes for the
   batch. A change means new requests, a new validation and a new preview.
3. `posts_create` per request; write each post ID into the pin's `postId`; `posts_get` for the
   status (write `"status": "FAILED"` on the pin if it failed). Report failures in plain words
   (board not found, image too large, link rejected).
4. `python3 <skill>/scripts/log.py record plan.json`.

Optional: `retryPolicy` (`maxRetries`, `delaySeconds`) makes WoopSocial retry a failed delivery.

## 6. Read results

`social_account_posts_list` (filter by `socialAccountId` or `postId`) returns each post with the
numbers WoopSocial has collected for it under `analytics` (each metric's latest value with its
date). Save the response as `metrics.json` and run
`python3 <skill>/scripts/log.py results --plan plan.json --metrics metrics.json` from day 30. Anything Pinterest Analytics
shows that isn't there (pin clicks, outbound clicks) goes in a CSV (`--csv`).

## Changing a scheduled pin

Not live yet: there's no edit, so delete it with `posts_delete` and create it again, after
confirming with the user. Already live: edit it in Pinterest; never delete and re-post it (that is
the same picture to the same page again).

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=pinterest-skill&utm_medium=skill
- WoopSocial Pinterest MCP: https://woopsocial.com/social-media-mcp/pinterest-mcp?utm_source=pinterest-skill&utm_medium=skill
- Agent setup: https://woopsocial.com/agents?utm_source=pinterest-skill&utm_medium=skill
