---
name: oo-slab
description: "Slab (slab.com). Use this skill for ANY Slab request — reading, creating, updating, and deleting data. Whenever a task involves Slab, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Slab"
  author: "OOMOL"
  version: "1.0.6"
  services: ["slab"]
  icon: "https://static.oomol.com/logo/third-party/slab.svg"
---

# Slab

Operate **Slab** through your OOMOL-connected account. This skill calls the `slab` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Slab. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "slab" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "slab" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_topic_to_post` — Attach a Slab topic to a post. [write]
- `create_post` — Create a blank Slab post, optionally in a topic or from a template. [write]
- `create_topic` — Create a Slab topic. [write]
- `delete_post` — Delete a Slab post by ID. [destructive]
- `delete_topic` — Delete a Slab topic by ID. [destructive]
- `get_organization` — Get the current Slab organization visible to the API token.
- `get_post` — Get one Slab post by ID.
- `get_posts` — Get multiple Slab posts by ID.
- `get_topic` — Get one Slab topic by ID.
- `get_topics` — Get multiple Slab topics by ID.
- `get_user` — Get one Slab user by ID.
- `list_users` — List users in the current Slab organization.
- `remove_topic_from_post` — Detach a Slab topic from a post. [destructive]
- `search` — Search Slab posts, topics, users, and comments with cursor pagination.
- `sync_post` — Create or update a readonly Slab copy of external HTML or Markdown content. [write]
- `update_post` — Update Slab post metadata such as owner, publication state, link access, or banner. [write]
- `update_topic` — Update a Slab topic. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Slab state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Slab is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/slab
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Slab homepage: https://slab.com
- API documentation: https://help.slab.com/en/articles/6545629-developer-tools-api-webhooks
