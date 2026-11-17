# instagram-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**5 endpoints across 1 platform group(s).**

## Instagram (5)

### `instagram_comments`

- **HTTP:** `GET /instagram/post/comments`
- **What:** Retrieve paginated Instagram comments. Returns top-level comments for a public Instagram post or Reel. `reply_count` is included when the logged-out source exposes it; reply bodies are not available on this anonymous surface. Pass `paging_info.max_id` back as `max_id` for the next comment page.
- **Params:** `max_id` (string, optional) — Opaque cursor from the previous response's paging_info.max_id; `url` (string, **required**) — Public Instagram post or Reel URL

### `instagram_post`

- **HTTP:** `GET /instagram/post/{id}/{post_id}`
- **What:** Retrieve a specific Instagram post by URL shortcode. Returns media details for an Instagram URL shortcode. Use media.code from the reels response or shortcode from a public post URL; numeric media IDs are rejected.
- **Params:** `id` (string, **required**) — Instagram user ID retained for route compatibility; ownership is not verified; `post_id` (string, **required**) — Instagram URL shortcode (media.code), not a numeric media ID

### `instagram_profile`

- **HTTP:** `GET /instagram/profile/{username}`
- **What:** Retrieve an Instagram user profile by username. Returns the public profile of an Instagram account by `username`. The response has the user id, full name, biography, bio links, external URL, category, follower, following and post counts, verified and private flags, location, profile picture, recent posts with captions and like counts, and related profiles.
- **Params:** `username` (string, **required**) — Instagram username

### `instagram_reels`

- **HTTP:** `GET /instagram/reels/{id}`
- **What:** Retrieve Instagram Reels for a user. Returns up to 12 public Reels via anonymous proxied HTTP for the numeric Instagram user ID. Supports opaque `max_id` pagination. Captions, timestamps and original image dimensions are omitted when the public source does not expose them.
- **Params:** `id` (string, **required**) — Numeric Instagram user ID (not a username); `max_id` (string, optional) — Pagination cursor for fetching the next page of Reels

### `instagram_user_posts`

- **HTTP:** `GET /instagram/user/{username}/posts`
- **What:** Retrieve paginated Instagram user posts. Returns public posts and Reels from the logged-out Posts tab for an Instagram username. Each item exposes the fields available in Instagram's public grid; source-omitted metrics and dimensions are not inferred. Pass `paging_info.max_id` back as `max_id` for the next page.
- **Params:** `max_id` (string, optional) — Opaque cursor from the previous response's paging_info.max_id; `username` (string, **required**) — Instagram username, optionally prefixed with @
