---
name: oo-pdfmonkey
description: "PDFMonkey (pdfmonkey.io). Use this skill for ANY PDFMonkey request — reading, creating, and updating data. Whenever a task involves PDFMonkey, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PDFMonkey"
  author: "OOMOL"
  version: "1.0.1"
  services: ["pdfmonkey"]
  icon: "https://static.oomol.com/logo/third-party/pdfmonkey.svg"
---

# PDFMonkey

Operate **PDFMonkey** through your OOMOL-connected account. This skill calls the `pdfmonkey` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected PDFMonkey. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pdfmonkey" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pdfmonkey" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_document` — Create a PDFMonkey document and optionally queue generation immediately by setting status to pending. [write]
- `get_current_user` — Get the current PDFMonkey account resolved by the provided API key.
- `get_document` — Get one full PDFMonkey document including its payload and generation logs.
- `get_document_card` — Get one PDFMonkey document card for lightweight status polling without the full payload.
- `get_document_template` — Get one full PDFMonkey document template including draft and published fields.
- `list_document_cards` — List PDFMonkey document cards with optional filters for template, status, workspace, update time, and search text.
- `list_document_template_cards` — List PDFMonkey document template cards for one workspace with optional folder, page, and sort filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PDFMonkey state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — PDFMonkey is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=pdfmonkey
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- PDFMonkey homepage: https://pdfmonkey.io
