---
name: oo-paradym
description: "Paradym (paradym.id). Use this skill for ANY Paradym request — reading, creating, and updating data. Whenever a task involves Paradym, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Paradym"
  author: "OOMOL"
  version: "1.0.5"
  services: ["paradym"]
  icon: "https://static.oomol.com/logo/third-party/paradym.png"
---

# Paradym

Operate **Paradym** through your OOMOL-connected account. This skill calls the `paradym` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Paradym. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "paradym" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "paradym" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_openid4vc_credential_offer` — Create an OpenID4VC credential offer using one or more SD-JWT VC or mDoc credential templates. [write]
- `create_openid4vc_verification_request` — Create an OpenID4VC verification request for a Paradym presentation template. [write]
- `get_openid4vc_issuance_session` — Retrieve one OpenID4VC issuance session by ID.
- `get_openid4vc_verification_session` — Retrieve one OpenID4VC verification session by ID.
- `list_issued_credentials` — List issued credential metadata for a Paradym project.
- `list_mdoc_credential_templates` — List mDoc credential templates for a Paradym project with optional filters.
- `list_openid4vc_issuance_sessions` — List OpenID4VC issuance sessions for a Paradym project with optional status, ID, cursor, and sort filters.
- `list_openid4vc_verification_sessions` — List OpenID4VC verification sessions for a Paradym project with optional status, template, ID, cursor, and sort filters.
- `list_presentation_templates` — List Paradym presentation templates for a project with optional ID, name, cursor, and sort filters.
- `list_projects` — List Paradym projects accessible to the connected API key.
- `list_sd_jwt_vc_credential_templates` — List SD-JWT VC credential templates for a Paradym project with optional filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Paradym state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Paradym is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/paradym
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Paradym homepage: https://paradym.id
- API documentation: https://paradym.id/reference
