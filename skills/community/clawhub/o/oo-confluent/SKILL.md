---
name: oo-confluent
description: "Confluent (confluent.io). Use this skill for ANY Confluent request — reading, creating, updating, and deleting data. Whenever a task involves Confluent, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Confluent"
  author: "OOMOL"
  version: "1.0.4"
  services: ["confluent"]
  icon: "https://static.oomol.com/logo/third-party/confluent.svg"
---

# Confluent

Operate **Confluent** through your OOMOL-connected account. This skill calls the `confluent` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Confluent. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "confluent" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "confluent" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_environment` — Create a Confluent Cloud environment. [write]
- `delete_environment` — Delete a Confluent Cloud environment by ID. [destructive]
- `get_environment` — Retrieve one Confluent Cloud environment by ID.
- `get_kafka_cluster` — Retrieve one Kafka cluster in a Confluent Cloud environment.
- `get_organization` — Retrieve one Confluent Cloud organization by ID.
- `list_environments` — List Confluent Cloud environments visible to the connected Cloud API key.
- `list_kafka_clusters` — List Kafka clusters in a Confluent Cloud environment.
- `list_organizations` — List Confluent Cloud organizations visible to the connected Cloud API key.
- `update_environment` — Update the display name or Stream Governance package of an environment. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Confluent state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Confluent is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/confluent
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Confluent homepage: https://www.confluent.io
- API documentation: https://docs.confluent.io/cloud/current/api-docs/cloud-overview.html
