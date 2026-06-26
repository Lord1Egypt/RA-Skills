---
name: oo-v2ex
description: "V2EX (v2ex.com). Use this skill for ANY V2EX request — reading, creating, updating, and deleting data. Whenever a task involves V2EX, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "V2EX"
  author: "OOMOL"
  version: "1.0.1"
  services: ["v2ex"]
  icon: "https://static.oomol.com/logo/third-party/v2ex.png"
---

# V2EX

Operate **V2EX** through your OOMOL-connected account. This skill calls the `v2ex` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected V2EX. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "v2ex" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "v2ex" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `boost_topic` — Boost one of the authenticated member's V2EX topics to the homepage.
- `create_token` — Create a new V2EX Personal Access Token from an existing token. [write]
- `delete_notification` — Delete one V2EX notification by its numeric identifier. [destructive]
- `get_current_member` — Fetch the authenticated V2EX member profile.
- `get_current_token` — Fetch metadata for the V2EX Personal Access Token used by this connection.
- `get_node` — Fetch a V2EX node by node name.
- `get_topic` — Fetch a V2EX topic by numeric identifier.
- `list_hot_topics` — Fetch public hot topics from the V2EX legacy JSON API. Responses may be served from V2EX or CDN cache.
- `list_latest_topics` — Fetch public latest topics from the V2EX legacy JSON API. Responses may be served from V2EX or CDN cache.
- `list_node_topics` — Fetch topics from a V2EX node.
- `list_notifications` — Fetch the latest V2EX notifications for the authenticated member.
- `list_topic_replies` — Fetch replies for a V2EX topic.
- `set_topic_sticky` — Set one of the authenticated member's V2EX topics as sticky. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change V2EX state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — V2EX is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=v2ex
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- V2EX homepage: https://www.v2ex.com
