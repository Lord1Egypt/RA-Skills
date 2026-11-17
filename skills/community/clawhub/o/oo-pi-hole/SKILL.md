---
name: oo-pi-hole
description: "Pi-hole (pi-hole.net). Use this skill for ANY Pi-hole request — reading, creating, updating, and deleting data. Whenever a task involves Pi-hole, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pi-hole"
  author: "OOMOL"
  version: "1.0.5"
  services: ["pi_hole"]
  icon: "https://static.oomol.com/logo/third-party/pi_hole.svg"
---

# Pi-hole

Operate **Pi-hole** through your OOMOL-connected account. This skill calls the `pi_hole` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pi-hole. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pi_hole" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pi_hole" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_domain` — Add one or more allow or deny domain entries to Pi-hole, either exact or as regular expressions. [write]
- `add_list` — Add one or more allowlist or blocklist entries (addresses) to Pi-hole. [write]
- `batch_delete_clients` — Delete multiple Pi-hole client entries in one request. Reports deleted=false when none of the clients exist. [destructive]
- `batch_delete_domains` — Delete multiple Pi-hole domain entries in one request. Reports deleted=false when none of the entries exist. [destructive]
- `batch_delete_groups` — Delete multiple Pi-hole groups by name in one request. Reports deleted=false when none of the groups exist. [destructive]
- `batch_delete_lists` — Delete multiple Pi-hole allowlist or blocklist entries in one request. Reports deleted=false when none of the entries exist. [destructive]
- `create_client` — Register one or more Pi-hole clients identified by IP address, MAC address, hostname, or interface. [write]
- `create_group` — Create one or more Pi-hole groups, optionally with a comment and enabled state. [write]
- `delete_client` — Delete one Pi-hole client entry by identifier. [destructive]
- `delete_domain` — Delete one Pi-hole allow or deny domain entry. [destructive]
- `delete_group` — Delete one Pi-hole group by name. [destructive]
- `delete_list` — Delete one Pi-hole allowlist or blocklist entry by address. [destructive]
- `export_backup` — Create a complete Pi-hole teleporter backup archive (teleporter.zip) with all settings, lists, and clients.
- `flush_dns_logs` — Flush the Pi-hole DNS query log. [destructive]
- `get_config` — Fetch the current Pi-hole configuration, such as DNS settings, privacy level, and API settings.
- `get_dhcp_leases` — Fetch the currently active DHCP leases assigned by the Pi-hole DHCP server.
- `get_dns_blocking_status` — Fetch whether Pi-hole DNS blocking is currently enabled, disabled, failed, or unknown.
- `get_history` — Fetch the Pi-hole activity graph data: query totals over time with cached, blocked, and forwarded splits.
- `get_network_devices` — Fetch the devices seen on the local network by Pi-hole.
- `get_overview` — Fetch the Pi-hole activity overview: total and blocked queries, blocked query percentage, unique clients and domains, and the blocking and gravity list status.
- `get_queries` — Query the Pi-hole DNS log with optional filters. By default returns the most recent queries; each response exposes a cursor for the next chunk.
- `get_query_types` — Fetch the number of queries of each DNS query type that Pi-hole has seen.
- `get_recent_blocked` — Fetch the domains most recently blocked by Pi-hole.
- `get_top_clients` — Fetch the clients that have queried Pi-hole the most, optionally limited to blocked ones.
- `get_top_domains` — Fetch the domains Pi-hole has handled the most, optionally limited to blocked ones.
- `get_upstreams` — Fetch metrics about Pi-hole's DNS upstream destinations, including response times.
- `import_backup` — Restore a Pi-hole teleporter backup archive (a previously exported teleporter.zip) to this instance. [destructive]
- `list_clients` — List all Pi-hole clients and their group memberships.
- `list_domains` — List the individual Pi-hole domain entries, optionally restricted to one type or kind.
- `list_groups` — List all Pi-hole groups and their memberships.
- `list_lists` — List the Pi-hole allowlists and blocklists (subscription lists).
- `restart_dns` — Restart Pi-hole's DNS server and reload its DNS configuration. [write]
- `run_gravity` — Run the Pi-hole gravity update to refresh the blocklists. The instance streams the gravity log; the action reports a best-effort status from the log plus the tail of the stream. [write]
- `search_domain` — Search whether a domain appears in Pi-hole's allowlists, blocklists, or gravity lists, to understand why it is blocked or allowed.
- `set_dns_blocking` — Enable or disable Pi-hole DNS blocking, optionally for a limited time after which the opposite mode is restored automatically. [destructive]
- `update_client` — Update one Pi-hole client's comment or group memberships. [destructive]
- `update_config` — Change part of the Pi-hole configuration, for example DNS upstreams, the privacy level, or API settings. The provided fields are merged into the current configuration. [destructive]
- `update_domain` — Update one Pi-hole domain entry: change its comment, enabled state, or group memberships. [destructive]
- `update_group` — Update one Pi-hole group: rename it, or change its comment or enabled state. [destructive]
- `update_list` — Update one Pi-hole list: change its comment, enabled state, or group memberships. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pi-hole state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pi-hole is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/pi_hole
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Pi-hole homepage: https://pi-hole.net
- API documentation: https://docs.pi-hole.net/api/
