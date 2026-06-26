---
name: oo-alt-text-ai
description: "AltText.ai (alttext.ai). Use this skill for ANY AltText.ai request — reading, creating, updating, and deleting data. Whenever a task involves AltText.ai, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "AltText.ai"
  author: "OOMOL"
  version: "1.0.2"
  services: ["alt_text_ai"]
  icon: "https://static.oomol.com/logo/third-party/alt_text_ai.svg"
---

# AltText.ai

Operate **AltText.ai** through your OOMOL-connected account. This skill calls the `alt_text_ai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected AltText.ai. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "alt_text_ai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "alt_text_ai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_image` — Add a publicly accessible image URL to AltText.ai and generate alt text. [write]
- `delete_image` — Delete an image from the AltText.ai library by asset ID. [destructive]
- `get_account` — Retrieve AltText.ai account settings and usage details for the API key.
- `get_image` — Retrieve a single AltText.ai image record by asset ID.
- `list_images` — List image records in the AltText.ai library with optional URL filtering.
- `scrape_page` — Scrape a web page or raw HTML document and queue discovered images for alt text generation.
- `search_images` — Search the AltText.ai image library by URL, asset ID, or alt text content.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change AltText.ai state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — AltText.ai is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=alt_text_ai
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- AltText.ai homepage: https://alttext.ai
