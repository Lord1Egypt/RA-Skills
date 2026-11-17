# Posts

> Safety: the API key posts to real accounts. Use a dedicated key, never echo it, and confirm with the user before any publish, schedule, cancel or delete. Do all four only through the `postnext` helper: its preview and `--confirm` step is that confirmation, and a raw request skips it.

A post is a `providers` map. The helper builds it for you; this page documents the shape so you can read posts back and understand helper errors. Each key is a **bare provider name** and each value is one channel's entry.

## Request shape (CreatePostRequest)

```jsonc
{
  "providers": {
    "twitter": {                              // BARE name. NOT "twitter:@handle".
      "channelName": "@yourbrand",            // the real connected handle (from GET /connections)
      "providerId":  "tw_9f3a1c20e5",         // connection.providerId (NOT uniqueId)
      "content": { "text": "We shipped v2.",
                   "media": [{ "url": "https://cdn.postnext.io/assets/hero.png", "type": "IMAGE" }],
                   "hashtags": ["launch"] },
      "firstComment": "..."                   // instagram + linkedin ONLY; ignored elsewhere
    }
  },
  "title": "Launch",                          // optional, internal label
  "tags": ["launch"]                          // optional
}
```

`providerId` and `channelName` come from `GET /api/connections` (see `channels.md`). Resolve them by matching `provider` + `channelName`. A wrong/missing `providerId` makes the publish worker reject the row silently.

## How to send it

| Goal | Helper command |
|------|----------------|
| Publish immediately | `./postnext post --provider P --text "..." [--media FILE or URL]` |
| Schedule | `./postnext schedule --provider P --text "..." --at <future ISO8601>` |
| Cancel a scheduled post (back to draft) | `./postnext cancel <postId>` |
| Delete a post from PostNext | `./postnext delete <groupId>` (does not delete an already-published post from the platform) |

> Safety: every command in this table changes the user's account. Each one first prints a preview and sends nothing (exit code 3). Show the user that preview, wait for their explicit yes, then run the identical command again with `--confirm <code>` from the preview. Never send these requests with raw curl or another HTTP client.

Saving a draft, and publishing or scheduling an existing post by id, are not covered by this skill. Use the PostNext web app for those.

`userId` and `teamId` are derived from the key - never send them.

Note: fetching a deleted or non-existent post (`GET /api/posts/{id}`) returns HTTP 500 with `message: "Post group not found"`, not 404 (see `errors.md`).

## Single post vs thread

`content` is either an object (single post) or an array (thread).

**Single** (`LegacyPostContent`):
```jsonc
{ "text": "...", "media": [{ "url": "<asset.url>", "type": "IMAGE|VIDEO|GIF" }],
  "hashtags": ["a"], "instagramPostType": "feed|post|story|reel" }
```

**Thread** (array, `twitter` and `threads` ONLY):
```jsonc
[ { "order": 1, "text": "1/", "media": [] },
  { "order": 2, "text": "2/" } ]
```
`order` must be exactly 1..N with no gaps. Sending an array to any other provider silently keeps only element `[0]`.

Attach media by URL (`content.media[].url` or the legacy `content.mediaUrls[]`). `assetIds` is never dereferenced - a post with only `assetIds` has no media.

## Per-provider rules enforced at create time

| Provider | Rules |
|----------|-------|
| instagram | text or media required; caption <= 2200; <= 30 hashtags; `firstComment` <= 2200; `instagramPostType` in feed/post/story/reel |
| bluesky | text or image; <= 300 graphemes; <= 4 images; **no video** |
| linkedin | **no video** (422 UNSUPPORTED_MEDIA_FOR_PLATFORM); IMAGE + GIF ok; `firstComment` <= 1250 |
| twitter | text required; no char limit enforced at create; polls 2-4 options |
| threads, tiktok | no create-time content validator |
| youtube | publish path via this route is UNVERIFIED - test before relying on it |

## Scheduling

`scheduledAt` must be a future ISO8601 datetime (past or now is a 400). `timezone` only affects recurrence and display; it never shifts the fire time.

**Idempotency:** every confirmed `schedule` creates a new scheduled post, so running it twice publishes twice. Before scheduling again, run `./postnext posts SCHEDULED` and check the post is not already queued. The helper refuses past times, and its `--confirm` code covers one exact operation, but it does not detect an existing post with the same content.

## Examples

```bash
# publish now: the first run prints a preview and sends nothing
./postnext post --provider twitter --channel @brand --text "hi" --media ./x.png
# only after the user approves that exact preview
./postnext post --provider twitter --channel @brand --text "hi" --media ./x.png --confirm <code from the preview>

# schedule, cancel and delete preview the same way
./postnext schedule --provider twitter --text "hi" --at 2026-12-01T14:00:00Z
./postnext cancel <postId>
./postnext delete <groupId>
```

Reads are safe with raw curl when the helper cannot run:

```bash
# list posts (optionally by status)
curl -sS "https://api-app.postnext.io/api/posts?status=SCHEDULED" -H "x-api-key: $POSTNEXT_API_KEY"

# per-channel publish outcomes
curl -sS https://api-app.postnext.io/api/posts/results -H "x-api-key: $POSTNEXT_API_KEY"
```
