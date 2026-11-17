---
name: oo-paperform
description: "Paperform (paperform.co). Use this skill for ANY Paperform request — searching and reading data. Whenever a task involves Paperform, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Paperform"
  author: "OOMOL"
  version: "1.0.5"
  services: ["paperform"]
  icon: "https://static.oomol.com/logo/third-party/paperform.png"
---

# Paperform

Operate **Paperform** through your OOMOL-connected account. This skill calls the `paperform` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Paperform. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "paperform" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "paperform" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_form` — Get a Paperform form by slug, custom slug, or ID.
- `get_form_coupon` — Get a Paperform coupon by form and coupon code.
- `get_form_field` — Get a Paperform form field by field key.
- `get_form_partial_submission` — Get a Paperform partial submission by form and partial submission ID.
- `get_form_product` — Get a Paperform product by form and SKU.
- `get_form_submission` — Get a Paperform submission by form and submission ID.
- `get_partial_submission` — Get a Paperform partial submission by partial submission ID.
- `get_submission` — Get a Paperform submission by submission ID.
- `list_form_coupons` — List coupons for a Paperform form.
- `list_form_fields` — List fields for a Paperform form.
- `list_form_partial_submissions` — List partial submissions for a Paperform form.
- `list_form_products` — List products for a Paperform form.
- `list_form_submissions` — List submissions for a Paperform form.
- `list_forms` — List Paperform forms accessible to the authorized user.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Paperform state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Paperform is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/paperform
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Paperform homepage: https://paperform.co
- API documentation: https://paperform.readme.io/reference/getting-started-1
