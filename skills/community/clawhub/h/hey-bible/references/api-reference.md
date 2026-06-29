# Hey Bible API reference

Base URL: `https://api.heybible.app` · Auth: header `X-Hey-Bible-Api-Key`
(the CLI handles auth from `HEY_BIBLE_API_KEY`). All endpoints are `GET`.

## Endpoints

### `search` — look up verses
CLI: `hey-bible search <book> <chapter> [--start-verse n] [--end-verse n] [--bible-id id] --json`

| Param | Required | Notes |
|-------|----------|-------|
| `book` | yes | e.g. `John`, `Genesis`, `1 Corinthians` |
| `chapter` | yes | chapter number |
| `start_verse` | no | defaults to 1 |
| `end_verse` | no | defaults to the last verse in the chapter |
| `bible_id` | no | defaults to ESV; see `bibles` |

Returns `{ verse: { book, chapter, startVerse, endVerse, bibleId, content, isFavorite, ... } }`.
`content` is HTML. **Side effect:** saves the passage to the user's account.

### `bibles` — list translations
Returns `{ bibles: [{ id, name, abbreviation, description, source }] }`.
`source` is `private` or `api.bible`.

### `books` — list books
Returns `{ books: [{ name, code, chapters }] }`. `code` is the 3-letter book
code (e.g. `GEN`).

### `favorites` — user's favorited verses
CLI options: `--tag`, `--limit` (1–100, default 10), `--offset`.
Returns favorites with nested `notes`, `images`, `conversations`, and `tags`.

### `notes` — user's verse notes
CLI options: `--id`, `--limit`, `--offset`.

### `images` — AI-generated verse images
CLI options: `--id` (returns a 24h signed URL), `--limit`, `--offset`.

### `chats` — conversations with verse context
CLI options: `--id` (UUID; returns the full message list), `--limit`, `--offset`.

### `tags` — user-defined tags
Returns `{ tags: [{ id, name, color }] }`. Used to filter `favorites`.

## Pagination

List endpoints accept `limit` (1–100, default 10) and `offset` (default 0).

## Related tools

- **REST API** — <https://docs.heybible.app>
- **MCP server** — [`@hey-bible/mcp`](https://www.npmjs.com/package/@hey-bible/mcp) (same surface, for MCP-native clients)
- **TypeScript SDK** — [`@hey-bible/client`](https://www.npmjs.com/package/@hey-bible/client)
