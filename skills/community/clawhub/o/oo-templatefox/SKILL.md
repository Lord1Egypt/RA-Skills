---
name: oo-templatefox
description: "TemplateFox (templatefox.com). Use this skill for ANY TemplateFox request — reading, creating, and updating data. Whenever a task involves TemplateFox, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TemplateFox"
  author: "OOMOL"
  version: "1.0.4"
  services: ["templatefox"]
  icon: "https://static.oomol.com/logo/third-party/templatefox.png"
---

# TemplateFox

Operate **TemplateFox** through your OOMOL-connected account. This skill calls the `templatefox` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TemplateFox. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "templatefox" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "templatefox" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_image` — Generate an image from a TemplateFox image template and return a signed download URL. [write]
- `create_pdf` — Generate a PDF from a TemplateFox template and return a signed download URL. [write]
- `extract_pdf_pages` — Extract selected pages from a PDF URL with TemplateFox and return a signed download URL.
- `get_account` — Get TemplateFox account information including remaining credits.
- `get_template_fields` — Get dynamic field definitions for a TemplateFox template.
- `list_templates` — List TemplateFox templates visible to the API key.
- `merge_pdfs` — Merge multiple PDF URLs with TemplateFox and return a signed download URL for the result. [write]
- `rotate_pdf` — Rotate all pages or selected pages in a PDF URL with TemplateFox and return a signed download URL.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TemplateFox state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TemplateFox is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/templatefox
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- TemplateFox homepage: https://templatefox.com
- API documentation: https://templatefox.com/docs/api-reference
