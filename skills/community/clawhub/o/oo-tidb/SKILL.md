---
name: oo-tidb
description: "TiDB Cloud (pingcap.com). Use this skill for ANY TiDB Cloud request — reading, creating, and updating data. Whenever a task involves TiDB Cloud, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "TiDB Cloud"
  author: "OOMOL"
  version: "1.0.1"
  services: ["tidb"]
  icon: "https://static.oomol.com/logo/third-party/tidb.svg"
---

# TiDB Cloud

Operate **TiDB Cloud** through your OOMOL-connected account. This skill calls the `tidb` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected TiDB Cloud. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tidb" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tidb" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_api_key` — Fetch one TiDB Cloud API key by access key.
- `get_branch` — Fetch one TiDB Cloud Starter or Essential branch by branch ID.
- `get_cluster` — Fetch one TiDB Cloud Starter, Essential, or Dedicated cluster by ID.
- `get_export` — Fetch one TiDB Cloud Starter or Essential export task.
- `get_import` — Fetch one TiDB Cloud Starter, Essential, or Dedicated import task. [write]
- `get_node_spec` — Fetch one TiDB Cloud Dedicated node spec by region, component type, and key.
- `get_region` — Fetch one TiDB Cloud Dedicated region by region ID.
- `list_api_keys` — List TiDB Cloud API keys visible to the connected organization API key.
- `list_audit_logs` — List TiDB Cloud console audit logs for security and change tracking.
- `list_branches` — List TiDB Cloud Starter or Essential branches for a cluster.
- `list_clusters` — List TiDB Cloud Starter, Essential, or Dedicated clusters.
- `list_exports` — List TiDB Cloud Starter or Essential export tasks.
- `list_imports` — List TiDB Cloud Starter, Essential, or Dedicated import tasks.
- `list_node_specs` — List TiDB Cloud Dedicated node specs available in a region.
- `list_regions` — List TiDB Cloud regions available to the connected organization API key.
- `show_cloud_providers` — List cloud providers available for TiDB Cloud Dedicated clusters.
- `show_node_quota` — List TiDB Cloud Dedicated node quotas for the organization.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change TiDB Cloud state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — TiDB Cloud is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=tidb
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- TiDB Cloud homepage: https://www.pingcap.com/tidb/cloud/
