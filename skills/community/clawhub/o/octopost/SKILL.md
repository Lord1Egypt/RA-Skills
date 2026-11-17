---
name: octopost
description: Post, schedule, queue and thread posts to X (Twitter) through Octopost, with a human approval queue (Threads after Meta approval; Bluesky, LinkedIn and Mastodon in testing). Use when the user says "post this to X", "tweet this", "post on Twitter", "cross-post this", "share this launch", "announce the release", "schedule a tweet for tomorrow at 9", "queue these posts", "post this as a thread", "turn this into a thread and post it", "put this up for approval", "approve the queued post", "what's in my post queue", "reschedule that post", "cancel the scheduled post", "retry the failed post", or "post a changelog update". For drafting copy the user hasn't asked to publish, write it in chat and call Octopost only once they want it posted. Octopost doesn't send DMs, reply to mentions or report analytics.
---

# Octopost: post to X from your agent

Octopost publishes one post (or a thread) to every connected network, handles each network's character limits and thread format, and can hold posts for human approval. It needs an Octopost account (plans from $29/month, 7 days for $1 at https://octopost.ink/pricing) and an API key from https://octopost.ink/dashboard/api-keys.

## Setup (once)

Preferred: the MCP server, so the tools show up natively.

```bash
claude mcp add octopost --transport http https://octopost.ink/mcp --header "Authorization: Bearer $OCTOPOST_API_KEY"
```

Cursor, Codex, Gemini CLI and Windsurf configs: https://octopost.ink/docs/mcp.md

Without MCP, call the REST API at `https://octopost.ink/api` with `Authorization: Bearer $OCTOPOST_API_KEY` (reference: https://octopost.ink/docs/agents.md).

## How to post well

1. **Check what is connected first.** MCP: `list_accounts`. REST: `GET /api/accounts`. Only target networks that are connected.
2. **Ask before publishing on the user's behalf** unless they already said "post it". When unsure, use the approval queue: MCP `queue_post` with `needs_approval: true`. The user approves in the dashboard or with `approve_queued_post`.
3. **Fit the shortest network.** X allows 280 characters, Bluesky 300, Threads 500, Mastodon usually 500, LinkedIn 3,000. For a post going everywhere, stay under 280 or write a thread.
4. **Threads:** pass segments (MCP `create_post`/`queue_post` with `segments`, REST `segments: [{ "content": "..." }]`). X, Bluesky, Threads and Mastodon get native threads; LinkedIn gets the joined text.
5. **Links:** X down-ranks link posts, and on Octopost an X post with a link uses 13 of the plan's monthly X units (a plain post uses 1). Put the link in the last segment of a thread, or leave X out for link-heavy posts.
6. **Timing:** `schedule_post` for a specific time (ISO 8601 with timezone), `queue_post` to let the user's queue pick the next slot (interval and active hours are in `get_queue_status`).
7. **After posting,** report the post URLs returned per network. If a network failed, show its error and offer `retry_failed`.

## MCP tools

`list_accounts`, `create_post`, `schedule_post`, `queue_post`, `approve_queued_post`, `get_queue_status`, `update_queue_settings`, `list_posts`, `get_post`, `update_post`, `reschedule_post`, `cancel_scheduled`, `delete_post`, `retry_failed`, `list_presets`, `get_guide`.

Call `get_guide` for per-network rules before an unusual post (polls, media, content warnings on Mastodon).

## Examples

- "Announce v2.0 everywhere": `list_accounts`, draft under 280 chars, show it, then `create_post` to all connected networks.
- "Queue these five tips for next week, I want to check them first": five `queue_post` calls with `needs_approval: true`.
- "Thread this blog post on Bluesky and Mastodon tomorrow at 9am ET": split into segments under 300 graphemes, `schedule_post` with `segments` and `scheduled_for`.
