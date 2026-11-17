# pinterest-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**8 endpoints across 1 platform group(s).**

## Pinterest (8)

### `pinterest_board`

- **HTTP:** `GET /pinterest/board/{username}/{slug}`
- **What:** Get a Pinterest board's detail. Returns a Pinterest board's metadata (name, description, cover image, pin/follower counts, owner) plus a page of pins from that board. Public data sourced from Pinterest's own board pages.
- **Params:** `slug` (string, **required**) — Board URL slug, from the board's own /{username}/{slug}/ URL; `username` (string, **required**) — Pinterest username that owns the board

### `pinterest_categories`

- **HTTP:** `GET /pinterest/categories`
- **What:** Get Pinterest's "Ideas" category list. Returns Pinterest's top-level "Ideas" category taxonomy (e.g. "Animals", "Home Decor", "Food And Drink"). Each entry's id is usable directly with GET /pinterest/ideas/{id}. Public data sourced from Pinterest's own ideas.pinterest.com-style category hub.
- **Params:** _none_

### `pinterest_idea`

- **HTTP:** `GET /pinterest/ideas/{id}`
- **What:** Get a Pinterest "Ideas" category's detail feed. Returns one "Ideas" category's metadata (name, description, follower count) plus a page of pins from that category's feed. Public data sourced from Pinterest's own ideas category pages.
- **Params:** `id` (string, **required**) — Pinterest ideas category id. See GET /pinterest/categories for the full list.

### `pinterest_pin`

- **HTTP:** `GET /pinterest/pin/{id}`
- **What:** Get a Pinterest pin's full detail. Returns a single Pinterest pin's full detail: title, description, image, board, pinner, comment count, save count, and creation time. Public data sourced from Pinterest's own pin pages.
- **Params:** `id` (string, **required**) — Pinterest pin id

### `pinterest_search`

- **HTTP:** `GET /pinterest/search`
- **What:** Search Pinterest pins. Returns public Pinterest pins matching a text query: title, description, image, board, and pinner for each result. Public data sourced from Pinterest's own web search.
- **Params:** `query` (string, **required**) — Search text

### `pinterest_user`

- **HTTP:** `GET /pinterest/user/{username}`
- **What:** Get a Pinterest user's public profile. Returns a Pinterest user's public profile: display name, bio, website, avatar, and follower/following/pin/board counts. Public data sourced from Pinterest's own profile pages.
- **Params:** `username` (string, **required**) — Pinterest username

### `pinterest_user_boards`

- **HTTP:** `GET /pinterest/user/{username}/boards`
- **What:** Get a Pinterest user's boards. Returns a page of a Pinterest user's own boards: name, description, cover image, and pin/follower counts for each. Public data sourced from Pinterest's own profile pages.
- **Params:** `username` (string, **required**) — Pinterest username

### `pinterest_user_pins`

- **HTTP:** `GET /pinterest/user/{username}/pins`
- **What:** Get a Pinterest user's own pins. Returns a page of a Pinterest user's own pins: title, description, image, board, and pinner for each. Public data sourced from Pinterest's own profile pages.
- **Params:** `username` (string, **required**) — Pinterest username
