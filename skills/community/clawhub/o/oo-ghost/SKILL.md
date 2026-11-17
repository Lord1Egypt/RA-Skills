---
name: oo-ghost
description: "Ghost (ghost.org). Use this skill for ANY Ghost request — searching and reading data. Whenever a task involves Ghost, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Ghost"
  author: "OOMOL"
  version: "1.0.5"
  services: ["ghost"]
  icon: "https://static.oomol.com/logo/third-party/ghost.png"
---

# Ghost

Operate **Ghost** through your OOMOL-connected account. This skill calls the `ghost` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Ghost. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ghost" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ghost" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_author` — Get one public Ghost author by ID or slug.
- `get_page` — Get one published Ghost page by ID or slug.
- `get_post` — Get one published Ghost post by ID or slug.
- `get_tag` — Get one public Ghost tag by ID or slug.
- `list_authors` — List public authors from the connected Ghost site.
- `list_pages` — List published pages from the connected Ghost site.
- `list_posts` — List published posts from the connected Ghost site.
- `list_tags` — List public tags from the connected Ghost site.
- `read_settings` — Read public settings for the connected Ghost site.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Ghost state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Ghost is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/ghost
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Ghost homepage: https://ghost.org
- API documentation: https://ghost.org/docs/content-api/
