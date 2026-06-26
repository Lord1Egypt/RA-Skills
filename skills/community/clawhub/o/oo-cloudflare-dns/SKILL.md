---
name: oo-cloudflare-dns
description: "Cloudflare DNS (cloudflare.com). Use this skill for ANY Cloudflare DNS request — reading, creating, updating, and deleting data. Whenever a task involves Cloudflare DNS, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Cloudflare DNS"
  author: "OOMOL"
  version: "1.0.3"
  services: ["cloudflare_dns"]
  icon: "https://static.oomol.com/logo/third-party/Cloudflare.svg"
---

# Cloudflare DNS

Operate **Cloudflare DNS** through your OOMOL-connected account. This skill calls the `cloudflare_dns` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Cloudflare DNS. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "cloudflare_dns" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "cloudflare_dns" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_dns_record` — Create a DNS record inside a Cloudflare zone. [write]
- `delete_dns_record` — Delete one DNS record from a Cloudflare zone. [destructive]
- `get_dns_record` — Get one DNS record from a Cloudflare zone.
- `get_zone` — Get one Cloudflare zone by zone ID.
- `list_accounts` — List Cloudflare accounts visible to the current credential.
- `list_dns_records` — List DNS records inside one Cloudflare zone.
- `list_zones` — List the Cloudflare zones visible to the current API token.
- `update_dns_record` — Patch one DNS record inside a Cloudflare zone. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Cloudflare DNS state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Cloudflare DNS is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key, OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=cloudflare_dns
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Cloudflare DNS homepage: https://www.cloudflare.com
