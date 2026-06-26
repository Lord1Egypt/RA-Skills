---
name: monday-for-agents
description: "Set up a monday.com account for an OpenClaw agent and work with monday.com boards, items, and updates via the GraphQL API or MCP server. Use when: creating a monday.com workspace for a PA, connecting the PA to monday.com, querying boards and items, creating or updating items, or troubleshooting monday.com API access. Covers GraphQL cookbook, column types, and MCP configuration. Works with any LLM model."
metadata:
  {
    "openclaw":
      {
        "emoji": "📋",
        "requires":
          {
            "env": ["MONDAY_API_TOKEN"],
          },
      },
  }
---

# monday.com for Agents

One skill for everything monday.com: account setup, daily operations, GraphQL API, MCP server, and troubleshooting.

## Minimum Model
Any model for routine operations. Use a medium model for debugging GraphQL errors.

---

## Section 1 — Setup

### Option A: Manual Account Creation

Each PA needs its own account — do not use the owner's.

1. Go to [monday.com/agents-signup](https://monday.com/agents-signup).
2. Use the agent email (e.g. `agent@agentdomain.com`).
3. Owner invites the PA via Admin → Users → Invite.

### Get an API Token

1. Log into monday.com as the agent.
2. Click avatar → **Developers** → **My Access Tokens** → **Copy**.
3. Set the token as an environment variable via OpenClaw's config (preferred) or your system's secret manager.
   ❌ Do **not** write the token to a plaintext file or add it to shell startup files.
   ❌ Do **not** commit tokens to version control.

**Recommended: OpenClaw env config**
Add `MONDAY_API_TOKEN` to your OpenClaw agent environment via the Ocana dashboard or `openclaw.json` `env` block — never hardcode it in scripts.

**For local dev only (not production):**
```bash
export MONDAY_API_TOKEN="TOKEN_HERE"  # current shell only, not persisted
```

### Setup Checklist

```
[ ] PA has a monday.com account (agent email, not owner's)
[ ] MONDAY_API_TOKEN set in OpenClaw agent environment (not a plaintext file)
[ ] Workspace access confirmed
[ ] Verified with: monday_query '{"query": "{ me { id name } }"}'
[ ] If using MCP: server added to config and tested
```

---

## Section 2 — Operations

### API Basics

Monday.com uses a single **GraphQL endpoint**:

```
https://api.monday.com/v2    (preferred)
https://api.monday.com/graphql  (also works)
```

#### Reusable Helper

```bash
MONDAY_API_URL="https://api.monday.com/v2"

# MONDAY_API_TOKEN must be set in the agent's environment (not read from file)
if [ -z "$MONDAY_API_TOKEN" ]; then
  echo "ERROR: MONDAY_API_TOKEN is not set. Configure it in your OpenClaw agent environment." >&2
  exit 1
fi

monday_query() {
  RESPONSE=$(curl -s -X POST "$MONDAY_API_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: $MONDAY_API_TOKEN" \
    -H "API-Version: 2024-10" \
    -d "$1")

  if echo "$RESPONSE" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d.get('errors'):
    print('API ERROR:', d['errors'])
    sys.exit(1)
" 2>/dev/null; then
    echo "$RESPONSE"
  else
    echo "API ERROR: $RESPONSE" >&2
    return 1
  fi
}
```

### Common Operations

```bash
# List boards
monday_query '{"query": "{ boards(limit: 25) { id name description state } }"}'

# Get items from a board
monday_query '{"query": "{ boards(ids: [BOARD_ID]) { items_page(limit: 50) { cursor items { id name group { id title } column_values { id title text type } } } } }"}'

# Create an item
monday_query '{
  "query": "mutation ($board: ID!, $name: String!) { create_item(board_id: $board, item_name: $name) { id } }",
  "variables": {"board": "BOARD_ID", "name": "New Task"}
}'

# Update a status column
monday_query '{
  "query": "mutation ($board: ID!, $item: ID!, $col: String!, $val: JSON!) { change_column_value(board_id: $board, item_id: $item, column_id: $col, value: $val) { id } }",
  "variables": {
    "board": "BOARD_ID",
    "item": "ITEM_ID",
    "col": "status",
    "val": "{\"label\": \"Done\"}"
  }
}'

# Add a comment to an item
monday_query '{
  "query": "mutation ($item: ID!, $body: String!) { create_update(item_id: $item, body: $body) { id } }",
  "variables": {"item": "ITEM_ID", "body": "Update text here"}
}'

# List columns in a board
monday_query '{"query": "{ boards(ids: [BOARD_ID]) { columns { id title type } } }"}'

# Query subitems
monday_query '{"query": "{ items(ids: [ITEM_ID]) { subitems { id name column_values { id text } } } }"}'

# Get current user
monday_query '{"query": "{ me { id name email account { id name } } }"}'
```

### Pagination for Large Boards

```bash
# First page — also returns a cursor
monday_query '{"query": "{ boards(ids: [BOARD_ID]) { items_page(limit: 100) { cursor items { id name } } } }"}'

# Next page — pass the cursor value from the previous response
monday_query '{"query": "{ next_items_page(limit: 100, cursor: \"CURSOR_VALUE\") { cursor items { id name } } }"}'
```

### Check Before Creating (Avoid Duplicates)

```bash
RESULT=$(monday_query '{"query": "{ items_by_multiple_column_values(board_id: BOARD_ID, column_id: \"name\", column_values: [\"Item Name\"]) { id name } }"}')

COUNT=$(echo "$RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(len(d.get('data', {}).get('items_by_multiple_column_values', [])))
")

if [ "$COUNT" -eq 0 ]; then
  echo "Item not found — creating"
else
  echo "Item already exists — skipping"
fi
```

### Batch Update Multiple Items

```bash
for ITEM_ID in 123456 789012 345678; do
  monday_query "{
    \"query\": \"mutation { change_column_value(board_id: BOARD_ID, item_id: $ITEM_ID, column_id: \\\"status\\\", value: \\\"{\\\\\\\"label\\\\\\\": \\\\\\\"In Progress\\\\\\\"}\\\") { id } }\"
  }"
  sleep 0.2  # Respect rate limits
done
```

### Rate Limits

Monday.com uses **complexity-based** rate limiting (not simple request counting). Response headers include `x-ratelimit-remaining-complexity`. Keep queries focused, use pagination, and add `sleep 0.2` between batch calls.

---

## Section 3 — MCP Server (Recommended for Daily Use)

The MCP server lets you work with boards using natural language tools — no manual GraphQL needed.

### Option A: Hosted MCP

Add to `~/.openclaw/openclaw.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "monday-mcp": {
      "url": "https://mcp.monday.com/mcp"
    }
  }
}
```

No local install needed. Uses OAuth.

Test: `mcporter call monday-mcp list_boards`

### Option B: Local MCP (npx)

```json
{
  "mcpServers": {
    "monday-api-mcp": {
      "command": "npx",
      "args": ["@mondaydotcomorg/monday-api-mcp@latest"],
      "env": {
        "MONDAY_API_TOKEN": "your_token_here"
      }
    }
  }
}
```

Speed tip: `npm install -g @mondaydotcomorg/monday-api-mcp` then use `"command": "monday-api-mcp"`.

---

## Section 4 — Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| 401 Unauthorized | Token invalid or expired | Regenerate in Developer settings, update file |
| 403 Forbidden | No board access | Ask owner to share the board with the PA account |
| "Column not found" | Wrong column ID | Run list columns query first |
| "Complexity budget exhausted" | Query too heavy | Use pagination with `limit: 50` |
| Empty response | Network or JSON issue | `echo $RESPONSE \| python3 -m json.tool` |
| Rate limit (429) | Too many requests | Add `sleep 0.2` between calls in loops |

---

## Core Operating Rules

Follow these rules every time, without exception:

1. **Create → API. Operate → MCP.**
   - New workspace / board / column: use API (curl + GraphQL)
   - Daily read/update/create items: use MCP (mcporter)

2. **Never guess IDs.**
   - Before any mutation: run `mcporter call monday.list_workspaces` or `get_board_info` first
   - Store all IDs in TOOLS.md immediately after creation

3. **One workspace per context.**
   - Family ≠ Work ≠ PA Network
   - Never mix contexts in the same workspace

4. **Before any mutation: verify.**
   - Run `mcporter call monday.get_board_info boardId=X` to confirm column IDs
   - Wrong column ID = silent failure or data corruption

5. **IDs in TOOLS.md, not memory.**
   - After creating any resource: `echo "board-name: $ID" >> TOOLS.md`
   - Before using an ID: `grep "board-name" TOOLS.md`

6. **Do NOT create or update board items without explicit instruction from owner.**
   - Always confirm board ID before mutations
   - Never print or log the API token

---

## Cost Tips

- **Cheap:** MCP handles natural language → API translation. Prefer it over raw GraphQL.
- **Expensive:** Fetching all items from large boards without pagination. Always use `limit:`.
- **Small model OK:** Routine ops (list, create, update) work with any model.
- **Use medium model for:** Debugging GraphQL errors or constructing complex queries.

---

## References

- Column value JSON formats: see `references/column-types.md` in this skill directory
- Full GraphQL cookbook: see `references/graphql-operations.md` in this skill directory
- monday.com GraphQL API: https://developer.monday.com/api-reference
- MCP server docs: https://mcp.monday.com