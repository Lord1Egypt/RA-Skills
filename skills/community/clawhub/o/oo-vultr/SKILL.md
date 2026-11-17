---
name: oo-vultr
description: "Vultr (vultr.com). Use this skill for ANY Vultr request — reading, creating, updating, and deleting data. Whenever a task involves Vultr, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Vultr"
  author: "OOMOL"
  version: "1.0.5"
  services: ["vultr"]
  icon: "https://static.oomol.com/logo/third-party/vultr.svg"
---

# Vultr

Operate **Vultr** through your OOMOL-connected account. This skill calls the `vultr` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Vultr. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "vultr" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "vultr" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_instance` — Create a Vultr VPS instance from an OS, ISO, snapshot, application, or application image. [write]
- `delete_instance` — Permanently delete a Vultr VPS instance. [destructive]
- `get_account` — Retrieve the connected Vultr account profile, ACL permissions, balance, and billing summary.
- `get_instance` — Retrieve one Vultr VPS instance by ID.
- `list_domain_records` — List DNS records for one domain in the connected Vultr account.
- `list_domains` — List DNS domains in the connected Vultr account.
- `list_firewall_groups` — List firewall groups in the connected Vultr account.
- `list_instances` — List Vultr VPS instances with cursor pagination and common filters.
- `list_operating_systems` — List operating system images available for Vultr instance deployment.
- `list_plans` — List Vultr VPS plans with plan-type and Windows compatibility filters.
- `list_regions` — List Vultr deployment regions and the features available in each region.
- `list_snapshots` — List snapshots in the connected Vultr account.
- `manage_instance_power` — Start, reboot, or halt a Vultr VPS instance. [write]
- `update_instance` — Update common settings on a Vultr VPS instance without reinstalling it. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Vultr state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Vultr is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/vultr
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Vultr homepage: https://www.vultr.com/
- API documentation: https://www.vultr.com/api/
