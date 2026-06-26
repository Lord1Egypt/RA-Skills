---
name: monday
description: Interact directly with the monday.com GraphQL API — no third-party gateway required. Read and create boards, items, columns, updates, and users. Use when asked to check tasks, add items, update statuses, query boards, or do anything with a user's monday.com workspace.
homepage: https://github.com/mondaycom/monday-graphql-api
metadata:
  {
    "openclaw":
      {
        "emoji": "📋",
        "requires": { "env": ["MONDAY_API_TOKEN"], "optionalEnv": ["MONDAY_API_ENDPOINT", "PLATFORM_API"] },
        "primaryEnv": "MONDAY_API_TOKEN",
      },
  }
---

# monday.com

GraphQL API skill via the official `@mondaydotcomorg/api` client.

## Setup

1. **Install dependencies** — `node_modules` is not included in the published skill. After installing, run:
   ```bash
   npm install --prefix ~/.agents/skills/monday/scripts
   ```

2. **API token** — set `MONDAY_API_TOKEN` in your environment, or store it in `openclaw.json` under `skills.entries.monday.apiKey` and add `"primaryEnv": "MONDAY_API_TOKEN"` to your agent config so OpenClaw injects it automatically.

   Optional env vars (endpoint overrides, rarely needed):
   - `MONDAY_API_ENDPOINT` — override the API base URL
   - `PLATFORM_API` — JSON secret map containing `PLATFORM_API_ENDPOINT` (monday.com platform apps only)

## Running queries

All API calls go through `scripts/monday.js`:

```bash
node ~/.agents/skills/monday/scripts/monday.js query '<graphql>' [--variables '<json>'] [--version '2026-01']
```

- Prints JSON to stdout on success.
- Prints `{ "error": "...", "graphqlErrors": [...] }` to stderr and exits non-zero on failure.
- Default API version: `2026-01`.

### Example — who am I?
```bash
node ~/.agents/skills/monday/scripts/monday.js query '{ me { id name email } }'
```

### Example — list boards
```bash
node ~/.agents/skills/monday/scripts/monday.js query '{ boards(limit: 20) { id name description } }'
```

### Example — items on a board (paginated)
```bash
node ~/.agents/skills/monday/scripts/monday.js query '
  query($id: [ID!]) {
    boards(ids: $id) {
      items_page(limit: 50) {
        cursor
        items { id name state column_values { id text } }
      }
    }
  }
' --variables '{"id": ["BOARD_ID"]}'
```

### Example — create an item
```bash
node ~/.agents/skills/monday/scripts/monday.js query '
  mutation($board: ID!, $name: String!) {
    create_item(board_id: $board, item_name: $name) { id name }
  }
' --variables '{"board": "BOARD_ID", "name": "New task"}'
```

## Key API rules

- Use `items_page` (not `items`) for fetching items from a board — it is paginated and performant.
- Use `next_items_page(cursor: $cursor)` to fetch subsequent pages.
- Use `users(limit: 50, page: N)` for paginating users.
- Request only the fields you actually need.
- Board IDs and item IDs are strings in variables (`ID!` type).

## LLM context rules

Official monday.com guidance files are in `references/`:

- `references/graphql-api-best-practices.md` — pagination patterns and correct query structure
- `references/api-client-best-practices.md` — client setup, error handling, env var usage
- `references/backend-usage-rules.md` — Node.js mutation/query examples with full error handling
- `references/frontend-usage-rules.md` — browser/React examples (reference only; this skill is server-side)

When writing a new or unfamiliar query, read the relevant rules file first.
