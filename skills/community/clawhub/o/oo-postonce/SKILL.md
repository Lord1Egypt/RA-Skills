---
name: oo-postonce
description: "PostOnce (postonce.to). Use this skill for ANY PostOnce request — reading, creating, updating, and deleting data. Whenever a task involves PostOnce, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PostOnce"
  author: "OOMOL"
  version: "1.0.0"
  services: ["postonce"]
  icon: "https://static.oomol.com/logo/third-party/postonce.svg"
---

# PostOnce

Operate **PostOnce** through your OOMOL-connected account. This skill calls the `postonce` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected PostOnce. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "postonce" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "postonce" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_post` — Cancel a scheduled or still-pending PostOnce post. Copies already published on social networks are not removed. [destructive]
- `create_post` — Publish a post to one or more connected accounts now, or schedule it with publish_at. Text, media URLs and per-account overrides go in one request. [write]
- `get_post` — Get one PostOnce post with its status and the delivery state and published URL on each account.
- `get_post_analytics` — Get current views, likes, comments, shares and saves for each published copy of a PostOnce post on TikTok, Instagram, YouTube and Facebook.
- `list_accounts` — List the social accounts connected to PostOnce, with each account's ID, network, status and media rules. Use the IDs as create_post targets.
- `list_posts` — List PostOnce posts newest first, including scheduled posts and posts published by workflows, with each account's delivery state.
- `retry_post_target` — Retry one failed account of a PostOnce post without publishing again to the accounts that already succeeded. [write]
- `update_post` — Change a scheduled PostOnce post before it publishes: its text, media, publish time, reference or targets. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PostOnce state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — PostOnce is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/postonce
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- PostOnce homepage: https://postonce.to
- API documentation: https://docs.postonce.to/api-reference/create-post
