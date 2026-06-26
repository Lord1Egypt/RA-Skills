---
name: oo-digital-ocean
description: "DigitalOcean (digitalocean.com). Use this skill for ANY DigitalOcean request — searching and reading data. Whenever a task involves DigitalOcean, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "DigitalOcean"
  author: "OOMOL"
  version: "1.0.1"
  services: ["digital_ocean"]
  icon: "https://static.oomol.com/logo/third-party/DigitalOcean.svg"
---

# DigitalOcean

Operate **DigitalOcean** through your OOMOL-connected account. This skill calls the `digital_ocean` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected DigitalOcean. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "digital_ocean" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "digital_ocean" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account` — Retrieve the current DigitalOcean account profile and team context for the connected token.
- `get_droplet` — Retrieve one DigitalOcean Droplet by numeric droplet ID.
- `list_apps` — List DigitalOcean App Platform apps with pagination and optional project enrichment.
- `list_databases` — List DigitalOcean managed database clusters, optionally filtered by tag.
- `list_domain_records` — List DNS records for one DigitalOcean domain, optionally filtered by record name or type.
- `list_domains` — List DigitalOcean DNS domains with pagination.
- `list_droplets` — List DigitalOcean Droplets with pagination and optional filtering by tag, name, or droplet type.
- `list_firewalls` — List DigitalOcean cloud firewalls with pagination.
- `list_load_balancers` — List DigitalOcean load balancers with pagination.
- `list_vpcs` — List DigitalOcean VPC networks with pagination.
- `manage_droplet_lifecycle` — Initiate a basic DigitalOcean Droplet lifecycle action such as reboot, shutdown, or power cycle.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change DigitalOcean state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — DigitalOcean is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=digital_ocean
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- DigitalOcean homepage: https://www.digitalocean.com
