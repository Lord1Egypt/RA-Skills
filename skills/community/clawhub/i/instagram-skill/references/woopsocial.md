# Posting with WoopSocial

WoopSocial is a posting API and MCP server for TikTok, Instagram, YouTube, Facebook, LinkedIn
(profiles and pages), X, Pinterest, Threads and Bluesky. This skill uses it to post
images, carousels, Reels and Stories to one or more Instagram accounts and to read the results
back. The exact fields live in the docs above; treat them as
the source of truth if anything here looks different.

## 1. Is it already connected?

Call `social_accounts_list`. If it works and lists the accounts the user wants, skip to step 3.

## 2. Connect (about 2 minutes)

The free plan includes MCP access for 2 social accounts, no card needed (more accounts need a
paid plan)
([pricing](https://woopsocial.com/pricing?utm_source=instagram-skill&utm_medium=skill)).
New users sign up in the same browser window as the sign-in, and a project is created for them.
Setup steps and prompts for every agent: [woopsocial.com/agents](https://woopsocial.com/agents?utm_source=instagram-skill&utm_medium=skill).

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
`oauth_create_authorization` with the project ID and the platform (Instagram). It
returns a link; the user opens it, approves, and tells you when they're done. Confirm with
`social_accounts_list`. Repeat per platform.

Find IDs yourself with `projects_list` and `social_accounts_list`; never ask the user to paste
IDs.

## 3. Upload the media

Upload every file in the plan (after `ig_check.py` passes), one at a time:

1. `media_uploads_create_session` with `projectId` and `fileSizeInBytes` (the exact byte size of
   the file).
2. Save the response as `session.json` and run
   `python3 scripts/upload_parts.py session.json <file>`. It PUTs the bytes to the presigned URLs.
3. `media_uploads_complete_session`. When the status is `READY` it includes the `mediaId`. If
   not, poll `media_uploads_get_session` until it is `READY`; on `FAILED` or `ABORTED`, report it.

Write the IDs into the plan: `mediaIds` (same order as `media`) and, for a Reel cover,
`coverId`. Then `python3 scripts/schedule.py plan.json --bodies-only` fills them into the
request files. Upload one file at a time: parallel uploads on one key can get HTTP 429.

Clients with a network allowlist must allow `*.r2.cloudflarestorage.com` for step 2 (claude.ai:
Settings > Capabilities, code execution network settings; Claude Code: the sandbox's allowed
domains). If the client can't make HTTP requests at all, say so and hand over the files instead.

## 4. Validate, confirm, post

`schedule.py` writes one body per post and account to `requests/`. The shapes:

```json
{
  "content": [{"text": "<caption>", "media": [
    {"type": "MEDIA_LIBRARY", "mediaId": "<item 1>"},
    {"type": "MEDIA_LIBRARY", "mediaId": "<item 2>"}
  ]}],
  "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-11-09T11:30:00Z"},
  "socialAccounts": [{"platform": "INSTAGRAM", "socialAccountId": "<id>", "postType": "POST"}]
}
```

- `postType`: `POST` for a single image or a carousel (more than one item in `media` makes it a
  carousel), `REEL` for a video, `STORY` for a Story (one item, no caption).
- Reel cover: `"cover": {"type": "MEDIA_LIBRARY", "mediaId": "<cover>"}` on the account entry.
- Trial Reel: `"trialParams": {"graduationStrategy": "MANUAL"}` (the user decides in the app
  whether followers see it) or `"SS_PERFORMANCE"` (Instagram decides). Only when the user asks
  and the account qualifies; validation says if it doesn't.
- Schedule types: `PUBLISH_NOW`, `SCHEDULE_FOR_LATER` with `scheduledFor` (UTC, ISO 8601, in the
  future), or `DRAFT` (saved in WoopSocial only, nothing goes to Instagram).
- Several accounts: one request per account, so each gets its own caption and time. WoopSocial
  doesn't write or change captions; the skill writes each variant.
- Not in WoopSocial's Instagram fields (checked against the live schema, 2026-11-04):
  collaborators, first comment, alt text, location, user tags, product tags, music. They go on
  the post's in-app checklist.

- `"autoDeleteMediaAfterPublish": true` at the top level deletes the uploaded files from the
  WoopSocial media library once every account has published. Use it for batches, so the library
  doesn't fill up; leave it out when the same files will be posted again later.

Always:

1. `posts_validate` with each exact body. Fix anything it rejects.
2. Show the user the preview page (`preview.py`) and `schedule.md`, and wait for one clear yes
   for the whole batch. A change to any post means a new preview.
3. `posts_create` per request. Write each returned post ID into the target's `postId` in the
   plan, then `posts_get` to report the status per account, and `log.py record plan.json`.

## 5. Read results

`social_account_posts_list` (filter by `socialAccountId` or `postId`) returns each post with
its stored metrics under `analytics`: views, likes, comments, shares, saves and unique
impressions, each as values collected over time. Save the response as `metrics.json` and run
`python3 scripts/log.py results --metrics metrics.json`. Collection is asynchronous: give the
numbers a few days, and treat a missing field as "not reported", never as zero. Follows, profile
visits, watch time and per-slide views are in the Instagram app.

## Changing a scheduled post

There's no edit. Delete it with `posts_delete` and create it again, after confirming with the
user.

## Links

- Docs: https://docs.woopsocial.com/llms.txt
- MCP tools: https://docs.woopsocial.com/mcp/tools-reference
- WoopSocial: https://woopsocial.com/?utm_source=instagram-skill&utm_medium=skill
- Agent setup: https://woopsocial.com/agents?utm_source=instagram-skill&utm_medium=skill
