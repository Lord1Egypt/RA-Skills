---
name: oo-notion
description: "Notion (notion.so). Use this skill for ANY Notion request — reading, creating, updating, and deleting data. Whenever a task involves Notion, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Notion"
  author: "OOMOL"
  version: "1.0.1"
  services: ["notion"]
  icon: "https://static.oomol.com/logo/third-party/Notion.svg"
---

# Notion

Operate **Notion** through your OOMOL-connected account. This skill calls the `notion` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Notion. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "notion" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "notion" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `append_block` — Append a single paragraph block to a Notion page. This is a simplified compatibility helper over `append_block_children`. [write]
- `append_block_children` — Append raw Notion child blocks to an existing parent block, using the official block-children append API. [write]
- `create_data_source` — Create a Notion data source under a parent database with a properties schema. [write]
- `create_database` — Create a Notion database container under a parent page or workspace, optionally with an initial data source. [write]
- `create_page` — Create a Notion page under a parent page, data source, or workspace-level private area. Use parentId + title for a simple child page under an existing page. Use parent with an official Notion parent payload for advanced cases: { page_id: "..." }, { data_source_id: "..." }, or { workspace: true } for OAuth public integrations. When parent is provided, do not use the top-level title field; provide the page title through properties.title instead. Internal integration secrets usually cannot create workspace-level private pages and should use a parent page or data source. [write]
- `delete_block` — Archive a Notion block through the official delete endpoint. [destructive]
- `get_page` — Get a Notion page together with its first-level child blocks. This is a repo-level aggregate helper over page retrieval plus block-children listing.
- `list_block_children` — List the direct child blocks under a Notion block with pagination. [write]
- `list_data_source_templates` — List templates available on a Notion data source.
- `list_users` — List users in the Notion workspace with pagination.
- `move_page` — Move a Notion page under another page or under a data source through the official page move API. [write]
- `query_data_source` — Query a Notion data source with filters, sorts, pagination, and optional property filtering.
- `retrieve_block` — Retrieve a Notion block by block ID. [write]
- `retrieve_data_source` — Retrieve a Notion data source by data source ID.
- `retrieve_database` — Retrieve a Notion database's metadata and schema by database ID.
- `retrieve_page` — Retrieve a Notion page's properties and metadata by page ID. This does not include child block content.
- `retrieve_page_markdown` — Retrieve a Notion page or block subtree rendered as enhanced Markdown through the official page markdown API.
- `retrieve_page_property` — Retrieve a specific property item from a Notion page by page ID and property ID. Title, rich_text, relation, and people properties return the paginated list response with type property_item.
- `retrieve_user` — Retrieve a Notion user by user ID.
- `search` — Search Notion pages and data sources with optional filter, sort, and pagination controls.
- `update_block` — Update a Notion block using raw block fields, including block-type payloads and optional trash state. [write]
- `update_data_source` — Update a Notion data source's title, icon, properties schema, parent, or trash status. [write]
- `update_database` — Update a Notion database container's parent, title, description, icon, cover, inline display, trash status, or locked state. [write]
- `update_page` — Update a Notion page's properties, title, icon, cover, trash status, or locked state. [write]
- `update_page_markdown` — Update a Notion page's content as enhanced Markdown through the official page markdown API. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Notion state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Notion is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=notion
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Notion homepage: https://www.notion.so
