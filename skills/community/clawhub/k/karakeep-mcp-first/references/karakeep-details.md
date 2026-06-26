# Karakeep Details

Load this reference only when you need Karakeep search syntax, detailed organization guidance, or fallback examples.

## Core Concepts

### Bookmarks

- Bookmarks can be links, text, or media.
- Links save URLs; Karakeep fetches metadata, screenshots, and archived page content.
- Text bookmarks are useful for quick notes, research snippets, and lightweight todos.
- Media bookmarks store uploaded images or PDFs.
- Favorites mark important items for quick access.
- Archiving hides items from the homepage while keeping them searchable.
- Notes and highlights add personal context.

### Lists

- Manual lists are curated collections organized by project or topic.
- Smart lists are auto-updating collections powered by search queries, such as `#ai -is:archived`.
- Use lists when membership itself matters, such as a project reading list, source library, or publish queue.

### Tags

Tags are lightweight labels for any bookmark. Multiple tags can apply to one bookmark, and tags travel with bookmarks across lists. Karakeep can auto-generate AI tags when inference is configured.

When assigning tags:

- Reuse existing tag names when possible.
- Avoid near-duplicates such as `ai-tools`, `aitools`, and `ai tool`.
- Prefer singular/plural consistency within the user's existing library.
- Attach/detach tags through MCP when the tag is known.

## Search Query Language

Karakeep supports full-text search, boolean logic, qualifiers, and date/age filters.

### Basic Syntax

- Spaces between conditions act as implicit AND.
- Use `and` / `or` for explicit boolean logic.
- Prefix a qualifier with `-` or `!` to negate it, such as `-is:archived`.
- Use parentheses for grouping.
- Any text not part of a qualifier is treated as full-text search.

### Qualifiers

| Qualifier | Description | Example |
|-----------|-------------|---------|
| `is:fav` | Favorited bookmarks | `is:fav` |
| `is:archived` | Archived bookmarks | `-is:archived` |
| `is:tagged` | Bookmarks with one or more tags | `is:tagged` |
| `is:inlist` | Bookmarks in one or more lists | `is:inlist` |
| `is:link` | Link bookmarks | `is:link` |
| `is:text` | Text/note bookmarks | `is:text` |
| `is:media` | Media bookmarks | `is:media` |
| `is:broken` | Bookmarks with failed crawls or non-2xx status codes | `is:broken` |
| `url:<value>` | Match URL substring | `url:github.com` |
| `title:<value>` | Match title substring | `title:"my title"` |
| `#<tag>` or `tag:<tag>` | Match bookmarks with a tag | `#important`, `tag:"work in progress"` |
| `list:<name>` | Match bookmarks in a list | `list:reading`, `list:"to review"` |
| `after:<date>` | Created on or after date | `after:2024-01-01` |
| `before:<date>` | Created on or before date | `before:2024-12-31` |
| `age:<time-range>` | Filter by creation age | `age:<1d`, `age:>2w`, `age:<6m` |
| `feed:<name>` | Bookmarks imported from an RSS feed | `feed:Hackernews` |
| `source:<value>` | Match capture source | `source:rss`, `-source:web` |

### Examples

```text
# Favorited bookmarks from 2024 tagged "important"
is:fav after:2024-01-01 before:2024-12-31 #important

# Archived bookmarks in "reading" list or tagged "work"
is:archived and (list:reading or #work)

# Untagged or unorganized bookmarks
-is:tagged or -is:inlist

# Recent bookmarks from the last week
age:<1w

# Full-text search combined with qualifiers
machine learning is:fav -is:archived
```

## MCP Workflows

### Add a Bookmark

1. Search first if the URL/topic may already exist.
2. Create the bookmark with MCP.
3. Attach relevant known tags with MCP.
4. Add it to a list with MCP only if list membership is useful.
5. Do not verify with CLI unless there is a clear reason.

### Search and Retrieve

1. Use `search-bookmarks` with a precise query.
2. Use `get-bookmark` for metadata or `get-bookmark-content` when the saved page text matters.
3. Prefer one focused search over several broad noisy searches.

### Organize Existing Bookmarks

1. Search for candidates.
2. Deduplicate by URL/title/content.
3. Attach/detach tags with MCP.
4. Create lists with MCP when needed.
5. Add or remove bookmarks from lists with MCP.
6. Confirm before destructive cleanup.

## Highlight Workflow

1. Use MCP to create, search, or get the bookmark.
2. Use MCP `get-bookmark-content` to fetch the saved content.
3. Identify the exact text span worth highlighting.
4. Check for existing similar highlights when practical.
5. If highlighting is warranted, use the Karakeep API `POST /api/v1/highlights` because MCP does not currently expose highlight creation.
6. Include `bookmarkId`, `startOffset`, `endOffset`, `text`, `note`, and a conservative color such as `yellow`.
7. Explain that API fallback was used because highlight creation is not available through MCP.
8. Verify with API or CLI only when needed.

## CLI Fallback

Use the CLI only for fallback/debug/bulk/raw-verification work. When using it, say why MCP was not used.

### Authentication

The CLI requires an API key and server address. Prefer existing configured auth when available. Avoid printing API keys.

```bash
export KARAKEEP_API_KEY="your-api-key"
export KARAKEEP_SERVER_ADDR="https://your-karakeep.example.com"
```

or:

```bash
karakeep --api-key <key> --server-addr <addr> <command>
```

### Useful Fallback Commands

```bash
# Verify authentication or server state
karakeep whoami --json

# Raw JSON search verification
karakeep bookmarks search "is:fav #work" --json
karakeep bookmarks search "rust" --limit 10 --sort-order relevance --json

# Get details or content when MCP is unavailable
karakeep bookmarks get <bookmark-id> --json
karakeep bookmarks get <bookmark-id> --include-content --json

# Bulk or administrative flows
karakeep dump --help
karakeep migrate --help
karakeep wipe --help
```

Do not use CLI-first bookmark/list/tag examples for normal work when MCP is available. Use the MCP tools instead.
