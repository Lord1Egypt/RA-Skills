---
name: oo-leina
description: "Leina (leina.ai). Use this skill for ANY Leina request — reading, creating, and updating data. Whenever a task involves Leina, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Leina"
  author: "OOMOL"
  version: "1.0.2"
  services: ["leina"]
  icon: "https://static.oomol.com/logo/third-party/leina.png"
---

# Leina

Operate **Leina** through your OOMOL-connected account. This skill calls the `leina` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Leina needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "leina" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "leina" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `list_bots` — List Leina robots and their runtime status in the current OOMOL team. Bound platforms do not guarantee a configured Home recipient.
- `send_notification` — Send text without invoking a model. Supply the opaque subscription returned by flow_notification_subscribe to deliver to that conversation; never expose the credential or derive a recipient yourself. Omit subscription to use the robot's configured Home channels. Retry uncertain delivery within one hour using the same Idempotency-Key and unchanged input. Subscription delivery deduplication survives Hermes restarts; Home deduplication does not. Delivered is not a read receipt. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Leina state — confirm the exact payload and effect with the user before running.**
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

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Leina homepage: https://leina.ai
