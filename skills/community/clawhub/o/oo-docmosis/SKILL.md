---
name: oo-docmosis
description: "Docmosis (docmosis.com). Use this skill for ANY Docmosis request — searching and reading data. Whenever a task involves Docmosis, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Docmosis"
  author: "OOMOL"
  version: "1.0.1"
  services: ["docmosis"]
  icon: "https://static.oomol.com/logo/third-party/docmosis.png"
---

# Docmosis

Operate **Docmosis** through your OOMOL-connected account. This skill calls the `docmosis` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Docmosis. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "docmosis" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "docmosis" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_environment_ready` — Check whether the selected Docmosis environment is currently ready to service render requests.
- `get_environment_summary` — Get Docmosis environment plan, quota, and readiness information for the selected processing location.
- `get_template_details` — Get the stored metadata for one uploaded Docmosis template without downloading the template file.
- `get_template_structure` — Get the Docmosis template structure tree that describes fields, repeats, conditions, and other data references.
- `list_templates` — List Docmosis templates available in the selected processing location with optional folder and paging controls.
- `render_document` — Render one Docmosis template with JSON data and return JSON-safe delivery metadata or an explicit base64 result file.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Docmosis state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Docmosis is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=docmosis
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Docmosis homepage: https://www.docmosis.com
