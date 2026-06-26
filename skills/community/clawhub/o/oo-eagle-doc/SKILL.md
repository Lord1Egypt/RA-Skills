---
name: oo-eagle-doc
description: "Eagle Doc (eagle-doc.com). Use this skill for ANY Eagle Doc request — searching and reading data. Whenever a task involves Eagle Doc, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Eagle Doc"
  author: "OOMOL"
  version: "1.0.1"
  services: ["eagle_doc"]
  icon: "https://static.oomol.com/logo/third-party/eagle_doc.png"
---

# Eagle Doc

Operate **Eagle Doc** through your OOMOL-connected account. This skill calls the `eagle_doc` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Eagle Doc. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "eagle_doc" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "eagle_doc" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_current_usage` — Fetch the current billing-month usage counters for the connected Eagle Doc API key.
- `get_quota` — Fetch the overall Eagle Doc management quota summary tied to the connected API key.
- `list_monthly_usage` — List Eagle Doc monthly usage history together with pricing metadata for each month returned.
- `list_usage_logs` — List recent Eagle Doc request log rows with processed page counts and timestamps.
- `process_finance_document` — Upload one invoice, receipt, or PDF to Eagle Doc Finance OCR and return the structured extraction result.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Eagle Doc state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Eagle Doc is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=eagle_doc
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Eagle Doc homepage: https://www.eagle-doc.com/en/products/eagle-doc-apis/
