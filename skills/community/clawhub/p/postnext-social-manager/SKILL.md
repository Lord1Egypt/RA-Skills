---
name: postnext-social-manager
description: Manage social media through PostNext - schedule, publish, and analyze posts across Twitter/X, Instagram, LinkedIn, Threads, YouTube, TikTok, and Bluesky via the PostNext public API. Use when the user wants to compose, schedule, or publish social posts, upload media for posts, check what is queued, cancel a scheduled post or delete a post from PostNext, read social analytics (engagement, best time to post, audience growth) or refresh them with an analytics sync, and has a PostNext account and API key. Publishing, scheduling, cancelling, deleting, uploading and analytics sync always preview first and need the user's approval.
allowed-tools: Bash(./postnext:*), Bash(jq:*), Read
metadata:
  requires:
    bins: [bash, curl, jq]
    env: [POSTNEXT_API_KEY]
---

# PostNext Social Manager

Drive a PostNext account programmatically: connect channels, upload media, compose and schedule or publish posts across platforms, and read analytics. Wraps the PostNext public REST API with an API key.

## Setup

1. The user creates an API key at https://postnext.io/account/api-keys (shown only once).
2. Export it: `export POSTNEXT_API_KEY=<key>`
3. Base URL is `https://api-app.postnext.io`. Auth header on every request: `x-api-key: $POSTNEXT_API_KEY`.

Two ways to use this skill:
- **Helper (required for anything that changes the account):** the bundled `postnext` script (needs `curl` + `jq`). It handles the fiddly, error-prone parts for you and asks for the user's approval before any change. Run `./postnext help`.
- **Raw curl (reads only):** where the helper cannot run, `references/` has curl recipes for reading channels, posts and analytics. Publishing, scheduling, cancelling, deleting, uploading and analytics sync always go through the helper, so its preview and `--confirm` step always runs.

## The core loop

1. **Connect** (one-time, done by the user in the PostNext web app - there is no API to connect a channel). Confirm what is connected: `postnext channels`.
2. **Upload media** if the post has an image or video: `postnext upload ./clip.mp4` prints an asset URL (or pass the file straight to `--media` in step 3).
3. **Compose + publish now** or **schedule**:
   - `postnext post --provider twitter --text "..." --media ./a.png`
   - `postnext schedule --provider instagram --text "..." --media ./a.jpg --at 2026-07-25T14:00:00Z`

   Every command that changes the account (`post`, `schedule`, `cancel`, `delete`, `upload`, `analytics sync`) first prints a **preview and sends nothing** (exit code 3). Show the preview to the user. Only after they approve it, run the identical command again with `--confirm <code>` from the preview. The code covers that exact operation: if the text, media, time or target changes, preview again and get a fresh approval.
4. **Measure**: `postnext analytics overview`, `postnext analytics best-time twitter`, `postnext results`.

## Safety

- The API key acts on the user's real social accounts. Use a dedicated key, and never paste it into posts, logs or URLs.
- Confirm with the user before any publish, schedule, cancel, delete, upload or analytics sync. The helper enforces this: without the `--confirm` code from its own preview it sends nothing. Never pass a code the user has not approved, and never reuse one for a changed operation.
- `delete` removes the post from PostNext only. It does not remove an already-published post from the platform.
- Never publish, schedule, cancel, delete, upload or run an analytics sync with raw curl or another HTTP client. That skips the preview and the user's approval.
- The helper only talks to `https://api-app.postnext.io`. Do not point raw curl recipes at any other host with the key.

## Four traps this skill exists to prevent

The PostNext API has four behaviors that silently produce broken posts. The `postnext` helper handles all four, one more reason to send posts only through it (details in `references/posts.md` and `references/media.md`).

1. **Key posts by the bare provider name** (`twitter`), never `twitter:@handle`. A colon key is rejected at publish. Select the account with the entry's `providerId` + `channelName`.
2. **Attach media by its URL**, never by `assetId`. A post that carries only `assetIds` publishes with no media and no error. Put the uploaded `asset.url` into `content.media`.
3. **`providerId` is the connection's `providerId`** (the platform-native account id from `GET /api/connections`), not `uniqueId`. A wrong or missing `providerId` fails at the publish worker silently.
4. **Only twitter and threads thread.** An array of posts sent to any other provider is silently reduced to the first item.

## When to read which reference

| Task | Read |
|------|------|
| Build a post, threads, per-provider rules, char limits | `references/posts.md` |
| Upload an image or video, size routing | `references/media.md` |
| List or check connected channels, resolve `providerId` | `references/channels.md` |
| Read analytics, best time to post, sync | `references/analytics.md` |
| Response envelope shapes, error codes, rate limits | `references/errors.md` |

## Known limitations

- No channel connect over the API (browser-only in PostNext).
- Account changes need a shell: publishing, scheduling, cancelling, deleting, uploading and analytics sync run only through the bundled helper.
- Saving drafts, publishing or scheduling an existing post by id, and uploading a remote URL into the media library are not covered (use the PostNext web app). A public media URL can go straight to `--media` on `post` or `schedule`.
- No team switching: the key operates on its account's default team.
- One entry per provider per request (no multi-account-per-provider in a single post).
- Analytics and per-post metrics require PUBLISHED posts.
- Not supported by this skill: WordPress/blog posts, brand-profile edits, team management (use the PostNext MCP or web app).
