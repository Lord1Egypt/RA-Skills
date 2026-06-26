---
name: oo-pushover
description: "Pushover (pushover.net). Use this skill for ANY Pushover request — reading, creating, updating, and deleting data. Whenever a task involves Pushover, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pushover"
  author: "OOMOL"
  version: "1.0.1"
  services: ["pushover"]
  icon: "https://static.oomol.com/logo/third-party/Pushover.svg"
---

# Pushover

Operate **Pushover** through your OOMOL-connected account. This skill calls the `pushover` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pushover. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pushover" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pushover" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `ack_delete_messages_up_to_id` — Acknowledge and delete all Open Client messages up to the provided message identifier. [destructive]
- `add_group_user` — Add an existing Pushover user to a delivery group. [write]
- `add_team_user` — Add a user to a Pushover for Teams organization using the Team API token. [write]
- `assign_license` — Assign one prepaid Pushover license credit to a user by key or email address. [write]
- `cancel_receipt_retries` — Cancel further retries for one emergency receipt before it expires. [write]
- `cancel_retries_by_tag` — Cancel retries for all active emergency receipts that share the provided tag. [write]
- `check_license_credits` — Get the number of prepaid Pushover license credits remaining on the application.
- `client_login` — Authenticate an Open Client user with email, password, and optional two-factor code.
- `create_group` — Create a new Pushover delivery group. [write]
- `disable_group_user` — Temporarily disable deliveries to a user, or one of the user's devices, inside a delivery group. [write]
- `enable_group_user` — Re-enable deliveries to a previously disabled user, or one of the user's devices, inside a delivery group. [write]
- `fetch_client_messages` — Download pending Open Client messages for a registered device.
- `get_app_icon_image` — Download a Pushover application icon PNG by icon identifier and return its binary content as base64.
- `get_app_limits` — Get the current monthly message limit, remaining messages, and reset time for the connected Pushover application.
- `get_app_token` — Return the application API token resolved from the action input or the connected credential.
- `get_group` — Get the name and membership of a Pushover delivery group.
- `get_receipt_status` — Get the status of an emergency notification receipt, including acknowledgment, callback, and expiry details.
- `get_team_api_token` — Return the Team API token resolved from the action input or the connected credential metadata.
- `list_groups` — List the delivery groups owned by the connected Pushover application account.
- `listen_client_websocket` — Open a temporary Open Client WebSocket session, login with the provided device and secret, and collect realtime events until timeout or close.
- `register_client_device` — Register an Open Client desktop device using a user session secret. [write]
- `remove_group_user` — Remove a user, or one of the user's devices, from a delivery group. [destructive]
- `remove_team_user` — Remove a user from a Pushover for Teams organization without deleting the user's Pushover account. [destructive]
- `rename_group` — Rename an existing Pushover delivery group. [write]
- `send_message` — Send a Pushover notification to a user or delivery group, with optional emergency settings, URL metadata, and image attachment. [write]
- `store_team_api_token` — Validate a Pushover Team API token for later use. Persist the token through the provider connection extra field when needed.
- `subscription_flow` — Validate and echo a Pushover subscription code collected through the web subscription flow.
- `update_glances` — Update Pushover Glances widget data for a user without creating a push notification. [write]
- `validate_user_or_group` — Validate that a Pushover user or delivery group key can receive notifications, optionally restricted to one device.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pushover state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pushover is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=pushover
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Pushover homepage: https://pushover.net
