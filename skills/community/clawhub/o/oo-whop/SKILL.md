---
name: oo-whop
description: "Whop (whop.com). Use this skill for ANY Whop request — searching and reading data. Whenever a task involves Whop, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Whop"
  author: "OOMOL"
  version: "1.0.5"
  services: ["whop"]
  icon: "https://static.oomol.com/logo/third-party/whop.svg"
---

# Whop

Operate **Whop** through your OOMOL-connected account. This skill calls the `whop` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Whop. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "whop" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "whop" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_authorized_user` — Retrieve a Whop authorized user by ID.
- `get_company` — Retrieve a Whop company by ID or route slug.
- `get_membership` — Retrieve a Whop membership by membership ID or license key.
- `get_product` — Retrieve a Whop product by ID.
- `list_authorized_users` — List authorized Whop team members with optional company, user, role, date, and cursor filters.
- `list_companies` — List Whop companies accessible to the credential, optionally filtering connected accounts by parent company.
- `list_memberships` — List Whop memberships for a company with optional product, plan, user, status, and cursor filters.
- `list_products` — List Whop products belonging to a company with optional visibility, type, sort, and cursor filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Whop state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Whop is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/whop
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Whop homepage: https://whop.com
- API documentation: https://docs.whop.com/developer/api/getting-started
