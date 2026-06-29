---
name: oo-dns-filter
description: "DNSFilter (dnsfilter.com). Use this skill for ANY DNSFilter request — searching and reading data. Whenever a task involves DNSFilter, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "DNSFilter"
  author: "OOMOL"
  version: "1.0.1"
  services: ["dns_filter"]
  icon: "https://static.oomol.com/logo/third-party/dns_filter.webp"
---

# DNSFilter

Operate **DNSFilter** through your OOMOL-connected account. This skill calls the `dns_filter` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected DNSFilter. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "dns_filter" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "dns_filter" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_category` — Get one DNSFilter domain category by ID.
- `get_current_user` — Get the DNSFilter user associated with the API key.
- `get_my_ip` — Get the public IP address observed by DNSFilter for the current request.
- `list_application_categories` — List DNSFilter application categories with optional pagination.
- `list_applications` — List DNSFilter applications with optional category filtering and pagination.
- `list_categories` — List DNSFilter domain categories with optional pagination.
- `list_ip_addresses` — List DNSFilter IP address records with optional search and pagination.
- `list_networks` — List DNSFilter networks with optional search and policy assignment filters.
- `list_policies` — List DNSFilter policies with optional organization and global-policy filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change DNSFilter state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — DNSFilter is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=dns_filter
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- DNSFilter homepage: https://www.dnsfilter.com
