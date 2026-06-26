---
name: obsidian-search
description: "Semantic search for Obsidian notes using AI vector embeddings. Find notes by meaning, discover connections, filter by tags/dates/folders, and retrieve full content. Use when the user says 'search my notes', 'find in Obsidian', 'what did I write about', 'related notes', 'Obsidian search', or wants AI-powered knowledge retrieval from their Obsidian vault."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔍"
    homepage: https://obsidian.10xboost.org/
---

# Obsidian Search

AI-powered semantic search for your Obsidian notes — find notes by meaning, not just keywords. Powered by [Obvec](https://obsidian.10xboost.org).

## Security & Data Handling

- **MCP link is a credential**: Your MCP Server URL (`https://rag.10xboost.org/mcp?token=xxxxx`) contains an embedded authentication token. Treat it like a password — do not share it publicly.
- **Token scope**: The token grants **read-only** access. It can search, list, retrieve note content, and analyze connections. It cannot modify, delete, or create notes in your Obsidian vault.
- **Token lifetime**: Tokens are valid for 30 days. After expiry, you will need to get a new MCP link from [obsidian.10xboost.org](https://obsidian.10xboost.org). You can also regenerate the token at any time in Settings, which invalidates any previously shared links.
- **Where the token is stored**: The token is generated server-side by Obvec. When you paste the MCP link into a Claude Connector or MCP client config, that client stores the link locally on your device. Revoking or regenerating the token server-side invalidates all copies.
- **Your note data**: To provide semantic search, your Obsidian note content is uploaded to the Obvec server and stored as text and vector embeddings. This means **your note content is stored on a third-party server** (Obvec, hosted on Google Cloud). Notes are isolated per user and are not shared with other users or used for model training. You can delete your indexed data at any time from your account dashboard.
- **No additional credentials**: No separate API keys, environment variables, or secrets are needed beyond the MCP link.


## Prerequisites

1. **Sign up** at [obsidian.10xboost.org](https://obsidian.10xboost.org) with Google
2. **Connect your Obsidian vault** — follow the setup guide to sync your notes
3. **Get your MCP link**: Go to **Settings** → copy your MCP Server URL
4. **Add to Claude**: Paste the MCP link as a Connector — no install, no API key needed

## Available Tools (4)

| Tool | Description |
|------|-------------|
| `search_notes` | Semantic search — find notes by meaning with similarity scoring, tag/date filters |
| `list_notes` | Browse notes by folder, tags, date range, with sorting options |
| `get_note` | Retrieve full content of a specific note by path or search term |
| `analyze_connections` | Discover related notes through AI-powered similarity analysis |

## Workflow

### Step 1: Understand the User's Intent

| User Request | Tool to Use |
|-------------|------------|
| "Find notes about X" | `search_notes` |
| "What did I write about X?" | `search_notes` |
| "Show my recent notes" | `list_notes` with `sortBy: "modifiedAt"` |
| "Notes in folder X" | `list_notes` with `pathPrefix` |
| "Open note X" | `get_note` |
| "What's related to X?" | `analyze_connections` |

### Step 2: Search Notes

#### Semantic Search
```
search_notes(
  query: "machine learning project ideas",
  limit: 10,
  minScore: 0.7
)
```

#### With Filters
```
search_notes(
  query: "meeting notes",
  tags: ["work", "project-x"],
  sortBy: "modifiedAt",
  limit: 20
)
```

### Step 3: Retrieve Full Content

```
get_note(path: "Projects/AI Research.md")
```
or search by term:
```
get_note(searchTerm: "quarterly review")
```

### Step 4: Discover Connections

```
analyze_connections(
  reference: "Projects/AI Research.md",
  limit: 10,
  minScore: 0.6
)
```

Returns notes most semantically similar to the reference — great for finding related ideas, building knowledge graphs, or discovering forgotten notes.

### Step 5: Present Results

- **Search results**: Show titles, relevance scores, and brief excerpts
- **Note content**: Display the full markdown content
- **Connections**: Present as a ranked list with similarity scores and note titles


## Error Handling

| Error | Solution |
|-------|----------|
| No results found | Try a broader query or lower `minScore` |
| Note not found | Use `list_notes` to find the correct path |
| Token expired | Get a new MCP link from [obsidian.10xboost.org](https://obsidian.10xboost.org) Settings (tokens last 30 days) |
