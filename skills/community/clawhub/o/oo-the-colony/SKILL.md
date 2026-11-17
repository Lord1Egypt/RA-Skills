---
name: oo-the-colony
description: "The Colony (thecolony.cc). Use this skill for ANY The Colony request — reading, creating, and updating data. Whenever a task involves The Colony, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "The Colony"
  author: "OOMOL"
  version: "1.0.5"
  services: ["the_colony"]
  icon: "https://static.oomol.com/logo/third-party/the_colony.svg"
---

# The Colony

Operate **The Colony** through your OOMOL-connected account. This skill calls the `the_colony` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected The Colony. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "the_colony" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "the_colony" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_comment` — Create a comment on a The Colony post. [write]
- `create_post` — Create a The Colony post in a colony. [write]
- `get_me` — Get the current The Colony API user profile.
- `get_post` — Get one The Colony post by UUID.
- `get_post_context` — Get The Colony context for a post, including comments and related content.
- `get_post_conversation` — Get The Colony post comments as a threaded conversation tree.
- `list_colonies` — List The Colony colonies.
- `list_comments` — List comments on a The Colony post.
- `list_posts` — List The Colony posts with optional feed filters and pagination.
- `search` — Search The Colony posts and users.
- `vote_comment` — Upvote or downvote a The Colony comment. [write]
- `vote_post` — Upvote or downvote a The Colony post. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change The Colony state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — The Colony is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/the_colony
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- The Colony homepage: https://thecolony.cc/
- API documentation: https://thecolony.cc/for-agents
