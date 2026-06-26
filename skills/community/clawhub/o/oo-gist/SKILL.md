---
name: oo-gist
description: "Gist (gist.github.com). Use this skill for ANY Gist request — reading, creating, updating, and deleting data. Whenever a task involves Gist, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Gist"
  author: "OOMOL"
  version: "1.0.1"
  services: ["gist"]
  icon: "https://static.oomol.com/logo/third-party/github.png"
---

# Gist

Operate **Gist** through your OOMOL-connected account. This skill calls the `gist` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Gist. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gist" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gist" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_gist_starred` — Check whether the authenticated GitHub user has starred a gist.
- `create_gist` — Create a new GitHub gist. [write]
- `create_gist_comment` — Create a comment on a GitHub gist. [write]
- `delete_gist` — Delete a GitHub gist. [destructive]
- `delete_gist_comment` — Delete a GitHub gist comment. [destructive]
- `fork_gist` — Fork a GitHub gist.
- `get_gist` — Get a GitHub gist by id.
- `get_gist_comment` — Get a GitHub gist comment by id. [write]
- `get_gist_revision` — Get a specific revision of a GitHub gist.
- `list_gist_comments` — List comments for a GitHub gist.
- `list_gist_commits` — List commit history for a GitHub gist.
- `list_gist_forks` — List forks for a GitHub gist.
- `list_my_gists` — List gists visible to the authenticated GitHub user.
- `list_public_gists` — List recent public GitHub gists.
- `list_starred_gists` — List gists starred by the authenticated GitHub user.
- `list_user_gists` — List public gists for a GitHub user.
- `star_gist` — Star a GitHub gist. [write]
- `unstar_gist` — Unstar a GitHub gist. [write]
- `update_gist` — Update a GitHub gist description or files. [write]
- `update_gist_comment` — Update a GitHub gist comment. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Gist state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Gist is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=gist
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Gist homepage: https://gist.github.com
