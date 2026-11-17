---
name: oo-saas-custom-domains
description: "SaaS Custom Domains (saascustomdomains.com). Use this skill for ANY SaaS Custom Domains request — reading, creating, updating, and deleting data. Whenever a task involves SaaS Custom Domains, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SaaS Custom Domains"
  author: "OOMOL"
  version: "1.0.5"
  services: ["saas_custom_domains"]
  icon: "https://static.oomol.com/logo/third-party/saas_custom_domains.svg"
---

# SaaS Custom Domains

Operate **SaaS Custom Domains** through your OOMOL-connected account. This skill calls the `saas_custom_domains` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SaaS Custom Domains. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "saas_custom_domains" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "saas_custom_domains" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_custom_domain` — Create a custom domain for a SaaS Custom Domains upstream. [write]
- `create_upstream` — Create an upstream for a SaaS Custom Domains account. [write]
- `delete_custom_domain` — Delete one SaaS Custom Domains custom domain. [destructive]
- `delete_upstream` — Delete one SaaS Custom Domains upstream and its custom domains. [destructive]
- `get_custom_domain` — Retrieve one SaaS Custom Domains custom domain by UUID.
- `get_upstream` — Retrieve one SaaS Custom Domains upstream by UUID.
- `list_accounts` — List SaaS Custom Domains accounts available to the API token.
- `list_custom_domains` — List custom domains for a SaaS Custom Domains upstream.
- `list_upstreams` — List upstreams for a SaaS Custom Domains account.
- `purge_custom_domain_http_cache` — Initiate an HTTP cache purge for one SaaS Custom Domains custom domain. [destructive]
- `verify_custom_domain_dns_records` — Trigger DNS record verification for one SaaS Custom Domains custom domain. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SaaS Custom Domains state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SaaS Custom Domains is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/saas_custom_domains
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SaaS Custom Domains homepage: https://saascustomdomains.com
- API documentation: https://docs.saascustomdomains.com/authentication
