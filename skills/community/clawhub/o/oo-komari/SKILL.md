---
name: oo-komari
description: "Komari (github.com). Use this skill for ANY Komari request — reading, creating, updating, and deleting data. Whenever a task involves Komari, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Komari"
  author: "OOMOL"
  version: "1.0.5"
  services: ["komari"]
  icon: "https://static.oomol.com/logo/third-party/komari.png"
---

# Komari

Operate **Komari** through your OOMOL-connected account. This skill calls the `komari` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Komari. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "komari" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "komari" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_client` — Create a Komari client. The response contains its enrollment token. [write]
- `add_load_notification` — Create a load notification rule. [write]
- `add_ping_task` — Create a ping task. [write]
- `batch_delete_clipboard` — Delete multiple clipboard entries. [destructive]
- `cancel_metric_migration` — Cancel the active metric-store migration. [destructive]
- `clear_all_records` — Permanently delete all load and ping records. [destructive]
- `clear_records` — Permanently delete all load records. [destructive]
- `create_clipboard` — Create a clipboard entry. [write]
- `delete_all_sessions` — Revoke all login sessions. [destructive]
- `delete_clipboard` — Delete a clipboard entry. [destructive]
- `delete_load_notification` — Delete load notification rules. [destructive]
- `delete_ping_tasks` — Delete ping tasks and their records. [destructive]
- `delete_session` — Revoke one login session using the stable identifier returned by list_sessions. [destructive]
- `disable_offline_notifications` — Disable offline notifications for clients. [destructive]
- `disable_traffic_report_notifications` — Disable traffic reports for clients. [destructive]
- `edit_client` — Update client fields. This changes Komari configuration. [write]
- `edit_load_notification` — Replace load notification rule fields. [write]
- `edit_offline_notifications` — Replace offline notification rule fields. [write]
- `edit_ping_tasks` — Replace ping task fields. [write]
- `edit_settings` — Update arbitrary Komari settings; invalid database settings can disrupt service. [destructive]
- `edit_traffic_report_notifications` — Replace traffic-report rule fields. [write]
- `enable_offline_notifications` — Enable offline notifications for clients. [write]
- `enable_traffic_report_notifications` — Enable traffic reports for clients. [write]
- `execute_command` — DANGEROUS: execute a shell command on selected clients. Komari API keys bypass interactive 2FA for this sensitive RPC. [destructive]
- `get_client` — Get one client without returning its enrollment token.
- `get_client_task_result` — Get one client's result for an execution task.
- `get_client_token` — Get a client enrollment token. Treat the response as a secret.
- `get_clipboard` — Get one clipboard entry.
- `get_current_user` — Get the current Komari user or guest identity.
- `get_database_size` — Inspect main and monitoring database storage.
- `get_execution_task` — Get one remote execution task and its results.
- `get_load_history` — Get persisted resource metrics for a node.
- `get_message_sender_provider` — Get one message-sender configuration or list available templates. The result may contain secrets.
- `get_metric_migration_status` — Get metric-store migration progress.
- `get_oidc_provider` — Get one OIDC configuration or list templates. The result may contain client secrets.
- `get_ping_history` — Get ping records by node, task, or both.
- `get_ping_metric_stats` — Get aggregate latency, loss, percentile, and standard-deviation statistics.
- `get_public_settings` — Get settings that Komari exposes to its public frontend.
- `get_recent_metrics` — Get the short in-memory window of recent reports for a node.
- `get_settings` — Get all Komari settings. The result can contain secrets and database DSNs.
- `get_terminal_settings` — Get xterm.js terminal appearance settings.
- `get_version` — Get the Komari server version and build hash.
- `list_audit_logs` — List paged audit logs.
- `list_client_execution_tasks` — List execution tasks assigned to a client.
- `list_clients` — List all clients without returning enrollment tokens.
- `list_clipboard` — List clipboard entries.
- `list_execution_tasks` — List remote execution tasks and their results, which may contain command output.
- `list_load_notifications` — List load notification rules.
- `list_metric_definitions` — List all metric definitions and retention policies.
- `list_nodes` — List visible Komari nodes without client tokens or private address fields.
- `list_offline_notifications` — List offline notification rules.
- `list_ping_tasks` — List all ping tasks including targets.
- `list_public_metric_definitions` — List public metric definitions and retention policies.
- `list_public_ping_tasks` — List ping tasks using the public response shape.
- `list_sessions` — List login sessions using stable identifiers while redacting session tokens and IP addresses.
- `list_task_results` — List all client results for an execution task.
- `list_traffic_report_notifications` — List traffic-report rules.
- `order_clients` — Set client display weights using a UUID-to-weight map. [write]
- `order_ping_tasks` — Set ping-task weights using an ID-to-weight map. [write]
- `query_metrics` — Query metric time-series points with filters, aggregation, and downsampling.
- `record_visitor_event` — Record a bounded visitor audit event in Komari. [write]
- `remove_client` — Permanently delete a client and its runtime state. [destructive]
- `set_message_sender_provider` — Save and possibly reload a message-sender provider configuration. [write]
- `set_oidc_provider` — Save and possibly reload an OIDC provider configuration. [write]
- `set_terminal_settings` — Update xterm.js terminal appearance settings, including optional custom CSS. [write]
- `start_metric_migration` — Start migrating metrics from a source store into the current store. [write]
- `test_geoip` — Test Komari GeoIP lookup.
- `test_message_sender` — Send a test notification through the active message sender. [write]
- `update_clipboard` — Update a clipboard entry. [write]
- `update_metric_definition` — Change a metric retention policy; zero deletes stored data for that metric. [write]
- `vacuum_database` — Run database maintenance and reclaim storage space. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Komari state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Komari is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/komari
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Komari homepage: https://github.com/komari-monitor/komari
- API documentation: https://komari-document.pages.dev/en/dev/api
