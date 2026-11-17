---
name: oo-energy-performance-certificates
description: "Energy Performance Certificates (get-energy-performance-data.communities.gov.uk). Use this skill for ANY Energy Performance Certificates request — searching and reading data. Whenever a task involves Energy Performance Certificates, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Energy Performance Certificates"
  author: "OOMOL"
  version: "1.0.4"
  services: ["energy_performance_certificates"]
  icon: "https://static.oomol.com/logo/third-party/energy_performance_certificates.svg"
---

# Energy Performance Certificates

Operate **Energy Performance Certificates** through your OOMOL-connected account. This skill calls the `energy_performance_certificates` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Energy Performance Certificates. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "energy_performance_certificates" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "energy_performance_certificates" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_certificate` — Get full details for one Energy Performance Certificate or Display Energy Certificate by certificate number.
- `search_display_certificates` — Search display Energy Performance Certificates for public buildings with supported query filters.
- `search_domestic_certificates` — Search domestic Energy Performance Certificates with supported query filters.
- `search_non_domestic_certificates` — Search non-domestic Energy Performance Certificates with supported query filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Energy Performance Certificates state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Energy Performance Certificates is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/energy_performance_certificates
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Energy Performance Certificates homepage: https://get-energy-performance-data.communities.gov.uk
- API documentation: https://get-energy-performance-data.communities.gov.uk/api-technical-documentation
