---
name: oo-higgsfield-ai
description: "Higgsfield AI (higgsfield.ai). Use this skill for ANY Higgsfield AI request — reading, creating, updating, and deleting data. Whenever a task involves Higgsfield AI, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Higgsfield AI"
  author: "OOMOL"
  version: "1.0.5"
  services: ["higgsfield_ai"]
  icon: "https://static.oomol.com/logo/third-party/higgsfield_ai.png"
---

# Higgsfield AI

Operate **Higgsfield AI** through your OOMOL-connected account. This skill calls the `higgsfield_ai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Higgsfield AI. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "higgsfield_ai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "higgsfield_ai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_request` — Cancel a queued Higgsfield generation request. [destructive]
- `get_request_status` — Retrieve the current status and outputs for a Higgsfield generation request.
- `submit_image_generation` — Submit a Higgsfield text-to-image generation request. [write]
- `submit_video_generation` — Submit a Higgsfield image-to-video generation request. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Higgsfield AI state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Higgsfield AI is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/higgsfield_ai
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Higgsfield AI homepage: https://higgsfield.ai/
- API documentation: https://docs.higgsfield.ai/docs/how-to/introduction
