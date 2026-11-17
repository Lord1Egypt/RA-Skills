---
name: oo-esa
description: "esa (esa.io). Use this skill for ANY esa request — reading, creating, updating, and deleting data. Whenever a task involves esa, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "esa"
  author: "OOMOL"
  version: "1.0.6"
  services: ["esa"]
  icon: "https://static.oomol.com/logo/third-party/esa.svg"
---

# esa

Operate **esa** through your OOMOL-connected account. This skill calls the `esa` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected esa. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "esa" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "esa" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `append_post` — Append Markdown content to an esa post without first fetching its current body. [write]
- `archive_post` — Archive an esa post by moving it to the Archived category. [destructive]
- `create_comment` — Create a Markdown comment on an existing esa post. [write]
- `create_post` — Create a new esa post with optional Markdown body, tags, category, WIP state, and revision message. [write]
- `delete_comment` — Permanently delete an esa comment by ID. [destructive]
- `duplicate_post` — Duplicate an esa post into a new WIP post in the same or another accessible team. [write]
- `get_all_category_paths` — List esa category paths with pagination and optional path filters.
- `get_attachment` — Get an esa attachment as a local transit file when possible, otherwise return its downloadable URL.
- `get_categories` — Get an esa category, its child categories, and optional posts or parents.
- `get_comment` — Get one esa comment by ID, optionally including its stargazers.
- `get_markdown_syntax_help` — Get esa's official Markdown-syntax documentation post.
- `get_post` — Get one esa post by number. The body is truncated by default to keep agent context bounded.
- `get_post_backlinks` — List posts that link to a specific esa post.
- `get_post_comments` — List comments on an esa post with pagination.
- `get_post_summary_prompt` — Build the summary prompt for an esa post. The caller supplies the returned prompt to its model.
- `get_search_options_help` — Get esa's official search-syntax documentation post.
- `get_team_comments` — List comments in an esa team with pagination.
- `get_team_members` — List members of an esa team with their roles and profiles.
- `get_team_stats` — Get member, post, comment, star, watch, and activity statistics for an esa team.
- `get_team_tags` — List tags used by posts in an esa team with their counts.
- `get_teams` — List esa teams available to the authenticated user.
- `get_top_categories` — Get all top-level esa categories for a team.
- `list_recent_posts` — List recently updated esa posts. This is the action equivalent of the esa_recent_posts MCP resource.
- `prepend_post` — Prepend Markdown content to an esa post without first fetching its current body. [write]
- `rollback_post_revision` — Restore an esa post to a selected revision and create a new revision from it. [write]
- `search_help` — Search esa's official documentation team with esa query syntax.
- `search_posts` — Search posts in an esa team with esa query syntax and pagination.
- `ship_post` — Mark an esa post as shipped without changing other fields. [write]
- `update_comment` — Update an existing esa comment. [write]
- `update_post` — Update selected fields of an existing esa post. Use append_post or prepend_post to add Markdown without fetching the body. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change esa state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — esa is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/esa
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- esa homepage: https://esa.io
- API documentation: https://docs.esa.io/posts/102
