# Miremo Skill for OpenClaw

Access your [Miremo](https://miremoapp.com) notes, documents, supertags, and knowledge graph directly from OpenClaw via MCP.

## Prerequisites

This skill requires the Miremo MCP server to be connected in OpenClaw. Complete the following setup first.

---

## Step 1: Generate a Miremo API Key

1. Open the Miremo app → **Settings → Preferences**
2. Find the **API Key** section and click **New API Key**
3. Enter a name (e.g. `OpenClaw`) and confirm
4. **Copy the key immediately** (format: `sk-miremo-xxxx`) — it won't be shown again

---

## Step 2: Add the MCP Server to OpenClaw

Edit `~/.openclaw/openclaw.json` and add under `mcp.servers`:

```json
{
  "mcp": {
    "servers": {
      "miremo": {
        "type": "http",
        "url": "https://api.miremoapp.com/mcp/v1/mcp",
        "headers": {
          "Authorization": "Bearer sk-miremo-YOUR_KEY_HERE"
        }
      }
    }
  }
}
```

> For local development, use `http://localhost:8000/mcp/v1/mcp` as the URL.

---

## Step 3: Install This Skill

```bash
openclaw skills install miremo
```

Start a new OpenClaw session and the Miremo tools will be available.

---

## Available Tools

| Tool | Description |
|---|---|
| `search_memos` | Semantic / full-text / hybrid search across memos |
| `list_memos` | Paginated list of memos |
| `create_memo` | Create a new memo |
| `list_supertags` | List / search topic supertags |
| `list_documents` | List uploaded documents |
| `global_search` | Cross-type search (memos + docs + supertags) |
| `get_entity_graph` | Get 1-hop knowledge graph for an entity |
| `list_entities` | List AI-extracted knowledge graph entities |
| `list_workspaces` | List all workspaces accessible to the current user |
| `get_current_workspace` | Get effective workspace resolution (`explicit` / `default`) |

Workspace resolution rules:
- If `workspace_id` is provided in tool arguments, the operation runs in that workspace.
- If `workspace_id` is omitted, the operation runs only in the user's default workspace.

---

## Security Notes

- Treat your API Key like a password — never commit it to version control
- Revoke unused keys anytime in Miremo settings
- Create separate keys for different clients for independent management
