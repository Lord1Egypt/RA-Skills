---
name: oo-pdfcraft
description: "PDFCraft (pdfcraft.ai). Use this skill for ANY PDFCraft request — reading, creating, updating, and deleting data. Whenever a task involves PDFCraft, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PDFCraft"
  author: "OOMOL"
  version: "1.0.0"
  services: ["pdfcraft"]
  icon: "https://static.oomol.com/logo/third-party/pdfcraft.png"
---

# PDFCraft

Operate **PDFCraft** through your OOMOL-connected account. This skill calls the `pdfcraft` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

PDFCraft needs no account connection. Assume the oo CLI is installed and signed in. **Do not run `oo auth login` proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pdfcraft" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pdfcraft" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a PDFCraft MCP tool using its live schema from list_tools. Results preserve the upstream data envelope. For file conversion, prefer submit_transform to handle uploading a public file URL. get_download_urls defaults to complete output; request limited output only explicitly. [destructive]
- `get_transform` — Get a PDFCraft task and its progress or failure recovery guidance. When succeeded, call get_download_urls through call_tool and save the result before it expires.
- `list_tools` — Discover PDFCraft tools and their live schemas for conversion, translation, balance, estimates, task recovery and downloads. Call get_capabilities through call_tool before the first conversion.
- `submit_transform` — Download a public PDF or EPUB URL, create a PDFCraft task, upload the bytes and launch conversion or translation. Uses OOMOL credits. Returns immediately after launch; use get_transform to check completion, then call get_download_urls for a download link. Connector accepts files up to 100 MiB. On failure after creation, retain the UUID from the error and resume that task instead of creating another. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PDFCraft state — confirm the exact payload and effect with the user before running.**
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

- PDFCraft homepage: https://pdfcraft.ai
- API documentation: https://pdfcraft.ai/zh-CN/docs/getting-started/mcp
