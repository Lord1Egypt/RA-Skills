---
name: oo-wordpress
description: "WordPress (wordpress.org). Use this skill for ANY WordPress request — reading, creating, updating, and deleting data. Whenever a task involves WordPress, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "WordPress"
  author: "OOMOL"
  version: "1.0.6"
  services: ["wordpress"]
  icon: "https://static.oomol.com/logo/third-party/wordpress.png"
---

# WordPress

Operate **WordPress** through your OOMOL-connected account. This skill calls the `wordpress` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected WordPress. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "wordpress" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "wordpress" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_category` — Create a WordPress category. [write]
- `create_comment` — Create a WordPress comment or reply on a content object that allows comments. [write]
- `create_page` — Create a WordPress page. [write]
- `create_post` — Create a WordPress post. [write]
- `create_tag` — Create a WordPress tag. [write]
- `delete_category` — Permanently delete a WordPress category. WordPress terms do not support trash. [destructive]
- `delete_comment` — Delete a WordPress comment by ID. [destructive]
- `delete_media` — Delete a WordPress media attachment. Permanent deletion requires force=true; trashing depends on the site configuration. [destructive]
- `delete_page` — Delete a WordPress page by ID. [destructive]
- `delete_post` — Delete a WordPress post by ID. [destructive]
- `delete_tag` — Permanently delete a WordPress tag. WordPress terms do not support trash. [destructive]
- `get_category` — Get a WordPress category by ID.
- `get_comment` — Get a WordPress comment by ID, including comments on password-protected posts.
- `get_current_user` — Get the authenticated WordPress user.
- `get_media` — Get a WordPress media attachment by ID.
- `get_page` — Get a WordPress page by ID.
- `get_post` — Get a WordPress post by ID.
- `get_tag` — Get a WordPress tag by ID.
- `get_user` — Get a WordPress user by ID. The edit context requires permission to view that user.
- `list_categories` — List WordPress categories with optional filters and pagination.
- `list_comments` — List WordPress comments with optional filters and pagination.
- `list_media` — List WordPress media attachments with filters and pagination.
- `list_pages` — List WordPress pages with optional filters and pagination.
- `list_posts` — List WordPress posts with optional filters and pagination.
- `list_tags` — List WordPress tags with optional filters and pagination.
- `list_users` — List WordPress users with filters and pagination. User visibility and privileged filters depend on the connected user permissions.
- `search` — Search WordPress posts, terms or post formats with pagination and subtype filters.
- `update_category` — Update a WordPress category by ID. [write]
- `update_comment` — Update a WordPress comment by ID. [destructive]
- `update_media` — Update WordPress media metadata by ID, including replacing its caption and description. [write]
- `update_page` — Update a WordPress page by ID. [write]
- `update_post` — Update a WordPress post by ID. [write]
- `update_tag` — Update a WordPress tag by ID. [write]
- `upload_media` — Download fileUrl and upload it to the WordPress media library. Optional meta fields are applied after upload; if that step fails the error includes the created attachment ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change WordPress state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — WordPress is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/wordpress
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- WordPress homepage: https://wordpress.org
- API documentation: https://developer.wordpress.org/rest-api/
