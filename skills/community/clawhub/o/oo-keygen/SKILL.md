---
name: oo-keygen
description: "Keygen (keygen.sh). Use this skill for ANY Keygen request — reading, creating, updating, and deleting data. Whenever a task involves Keygen, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Keygen"
  author: "OOMOL"
  version: "1.0.1"
  services: ["keygen"]
  icon: "https://static.oomol.com/logo/third-party/keygen.svg"
---

# Keygen

Operate **Keygen** through your OOMOL-connected account. This skill calls the `keygen` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Keygen. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "keygen" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "keygen" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `activate_machine` — Activate a machine in the connected Keygen account. [write]
- `attach_license_entitlements` — Attach entitlements to a Keygen license.
- `attach_license_users` — Attach users to a Keygen license.
- `attach_policy_entitlements` — Attach entitlements to a Keygen policy.
- `ban_user` — Ban a Keygen user from authenticating. [destructive]
- `change_license_group` — Change the group assigned to a Keygen license.
- `change_license_owner` — Change the owner user for a Keygen license.
- `change_license_policy` — Move a Keygen license to another policy.
- `change_machine_group` — Change the group assigned to a Keygen machine.
- `change_machine_owner` — Change the owner user for a Keygen machine.
- `change_user_group` — Move a Keygen user to another group.
- `check_in_license` — Check in a Keygen license for policies that require periodic license check-ins.
- `create_component` — Create a machine component in the connected Keygen account. [write]
- `create_entitlement` — Create an entitlement in the connected Keygen account. [write]
- `create_group` — Create a group in the connected Keygen account. [write]
- `create_license` — Create a license in the connected Keygen account. [write]
- `create_policy` — Create a license policy in the connected Keygen account. [write]
- `create_process` — Create a tracked process in the connected Keygen account. [write]
- `create_product` — Create a product in the connected Keygen account. [write]
- `create_user` — Create a user in the connected Keygen account. [write]
- `deactivate_machine` — Deactivate a machine from the connected Keygen account. [destructive]
- `decrement_license_usage` — Decrement metered usage for a Keygen license.
- `delete_component` — Delete a machine component from the connected Keygen account. [destructive]
- `delete_entitlement` — Delete an entitlement from the connected Keygen account. [destructive]
- `delete_group` — Delete a group from the connected Keygen account. [destructive]
- `delete_license` — Delete a license from the connected Keygen account. [destructive]
- `delete_policy` — Delete a license policy from the connected Keygen account. [destructive]
- `delete_process` — Delete a tracked process from the connected Keygen account. [destructive]
- `delete_product` — Delete a product from the connected Keygen account. [destructive]
- `delete_user` — Delete a user from the connected Keygen account. [destructive]
- `detach_license_entitlements` — Detach entitlements from a Keygen license.
- `detach_license_users` — Detach users from a Keygen license.
- `detach_policy_entitlements` — Detach entitlements from a Keygen policy.
- `increment_license_usage` — Increment metered usage for a Keygen license.
- `list_components` — List machine components in the connected Keygen account.
- `list_entitlements` — List entitlements in the connected Keygen account.
- `list_groups` — List groups in the connected Keygen account.
- `list_license_entitlements` — List entitlements attached to a Keygen license.
- `list_license_users` — List users attached to a Keygen license.
- `list_licenses` — List licenses in the connected Keygen account.
- `list_machines` — List activated machines in the connected Keygen account.
- `list_policies` — List license policies in the connected Keygen account.
- `list_policy_entitlements` — List entitlements attached to a Keygen policy.
- `list_processes` — List tracked processes in the connected Keygen account.
- `list_products` — List products in the connected Keygen account.
- `list_users` — List users in the connected Keygen account.
- `ping_machine` — Ping a Keygen machine heartbeat.
- `ping_process` — Ping a Keygen process heartbeat.
- `reinstate_license` — Reinstate a suspended Keygen license.
- `renew_license` — Renew a Keygen license according to its policy.
- `reset_license_usage` — Reset metered usage for a Keygen license. [destructive]
- `reset_machine_heartbeat` — Reset a Keygen machine heartbeat. [destructive]
- `retrieve_component` — Retrieve one machine component from the connected Keygen account.
- `retrieve_entitlement` — Retrieve one entitlement from the connected Keygen account.
- `retrieve_group` — Retrieve one group from the connected Keygen account.
- `retrieve_license` — Retrieve one license from the connected Keygen account.
- `retrieve_machine` — Retrieve one activated machine from the connected Keygen account.
- `retrieve_policy` — Retrieve one license policy from the connected Keygen account.
- `retrieve_process` — Retrieve one tracked process from the connected Keygen account.
- `retrieve_product` — Retrieve one product from the connected Keygen account.
- `retrieve_user` — Retrieve one user from the connected Keygen account.
- `revoke_license` — Revoke a Keygen license through the official revoke action. [destructive]
- `suspend_license` — Suspend a Keygen license so it can no longer authenticate with the API.
- `unban_user` — Unban a Keygen user so they can authenticate again.
- `update_component` — Update a machine component in the connected Keygen account. [write]
- `update_entitlement` — Update an entitlement in the connected Keygen account. [write]
- `update_group` — Update a group in the connected Keygen account. [write]
- `update_license` — Update a license in the connected Keygen account. [write]
- `update_machine` — Update an activated machine in the connected Keygen account. [write]
- `update_policy` — Update a license policy in the connected Keygen account. [write]
- `update_process` — Update a tracked process in the connected Keygen account. [write]
- `update_product` — Update a product in the connected Keygen account. [write]
- `update_user` — Update a user in the connected Keygen account. [write]
- `validate_license_by_id` — Validate a Keygen license by its resource ID and optional validation scope.
- `validate_license_key` — Validate a Keygen license key and optional validation scope.
- `whoami` — Fetch the Keygen profile associated with the connected API token.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Keygen state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Keygen is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=keygen
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Keygen homepage: https://keygen.sh
