---
name: oo-anchor-browser
description: "Anchor Browser (anchorbrowser.io). Use this skill for ANY Anchor Browser request — reading, creating, and updating data. Whenever a task involves Anchor Browser, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Anchor Browser"
  author: "OOMOL"
  version: "1.0.0"
  services: ["anchor_browser"]
  icon: "https://static.oomol.com/logo/third-party/anchor_browser.svg"
---

# Anchor Browser

Operate **Anchor Browser** through your OOMOL-connected account. This skill calls the `anchor_browser` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Anchor Browser. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "anchor_browser" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "anchor_browser" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_billing_info` — Retrieve Anchor Browser project billing balance, usage, tier, and browser limits.
- `get_project_metadata` — Retrieve lightweight Anchor Browser project metadata by project ID.
- `start_browser_session` — Start an Anchor Browser session and return its CDP and live-view connection URLs. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Anchor Browser state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Anchor Browser is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=anchor_browser
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Anchor Browser homepage: https://anchorbrowser.io
