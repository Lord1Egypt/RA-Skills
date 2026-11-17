---
name: oo-zerotier
description: "ZeroTier (zerotier.com). Use this skill for ANY ZeroTier request — reading, creating, updating, and deleting data. Whenever a task involves ZeroTier, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ZeroTier"
  author: "OOMOL"
  version: "1.0.2"
  services: ["zerotier"]
  icon: "https://static.oomol.com/logo/third-party/zerotier.svg"
---

# ZeroTier

Operate **ZeroTier** through your OOMOL-connected account. This skill calls the `zerotier` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ZeroTier. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "zerotier" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "zerotier" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `accept_invitation` — v1 only: accept an organization invitation. [write]
- `add_iam` — v2 only: add roles for a principal on an org, network group, or network. [write]
- `add_members` — v2 only: add multiple members to a network in one call. [write]
- `add_user_token` — v1 only: register an API token for a user. The caller supplies the token value (get_random_token generates one); it cannot be retrieved after it is set. [write]
- `authorize_member` — Authorize one member on a ZeroTier network. [write]
- `authorize_members` — v2 only: authorize multiple members on a network in one call. [write]
- `check_permissions` — v2 only: check whether the authenticated principal holds permissions on resources.
- `create_api_key` — v2 only: create an API key for a service account. The secret is returned only once. [write]
- `create_invitation` — v1 only: send an organization invitation to an email address. [write]
- `create_network` — Create a ZeroTier network. For v1 sends {config, description} and rejects networkGroupId; for v2 sends {name, description, config} and requires networkGroupId (the group the network is created under) and name. [write]
- `create_network_group` — v2 only: create a network group inside an organization. [write]
- `create_service_account` — v2 only: create a service account in an organization. [write]
- `create_webhook` — v2 only: create a webhook for an organization. [write]
- `deauthorize_member` — Revoke authorization for one member on a ZeroTier network. [destructive]
- `deauthorize_members` — v2 only: de-authorize multiple members on a network in one call. [destructive]
- `decline_invitation` — v1 only: decline or cancel an organization invitation. [destructive]
- `delete_api_key` — v2 only: delete an API key. [destructive]
- `delete_current_user` — v2 only: permanently delete the authenticated user account. [destructive]
- `delete_member` — Remove a member from a ZeroTier network. [destructive]
- `delete_network` — Permanently delete a ZeroTier network and all its members. [destructive]
- `delete_network_group` — v2 only: permanently delete a network group. Upstream also deletes all networks in the group. [destructive]
- `delete_service_account` — v2 only: permanently delete a service account and all of its API keys. [destructive]
- `delete_user` — v1 only: permanently delete a ZeroTier user account by ID. Upstream also deletes every network the user owns; this cannot be undone. [destructive]
- `delete_user_token` — v1 only: delete one of a user's API tokens by name. [destructive]
- `delete_webhook` — v2 only: delete a webhook. [destructive]
- `delete_webhook_secret` — v2 only: revoke an overlap (previous) webhook secret by ID before its grace window ends. The active primary secret cannot be deleted (upstream returns 400); rotate first. [destructive]
- `get_api_key` — v2 only: get one API key's metadata by ID.
- `get_flow_rules` — v2 only (beta): get a network's flow rules.
- `get_iam` — v2 only: list IAM role assignments on an org, network group, or network.
- `get_invitation` — v1 only: get one organization invitation by ID.
- `get_member` — Get one member of a ZeroTier network, including authorization and IP assignment state.
- `get_network` — Get one ZeroTier network by ID, including its config (v1 responses also include member counts).
- `get_network_group` — v2 only: get one network group by ID.
- `get_org` — Get a ZeroTier organization. For v1, returns the current user's org when orgId is omitted, or /org/{orgId}. For v2, uses orgId or falls back to the connection's orgId; one of them is required.
- `get_org_iam_tree` — v2 only: get the IAM tree of an organization (groups, networks, principals, roles).
- `get_org_subscription` — v2 only: get an organization's subscription plan and entitlements.
- `get_random_token` — v1 only: get a server-generated random token value.
- `get_service_account` — v2 only: get one service account by ID, including its API keys.
- `get_status` — v1 only: get ZeroTier Legacy Central status, including the authenticated user, version, and uptime.
- `get_user` — v1 only: get a ZeroTier user by ID.
- `get_webhook` — v2 only: get one webhook by ID.
- `invite_users` — v2 only: invite email addresses to an organization. [write]
- `list_invitations` — v1 only: list organization invitations for the current user.
- `list_members` — List all members (devices) joined to a ZeroTier network.
- `list_network_group_networks` — v2 only: list networks inside one network group.
- `list_network_groups` — v2 only: list network groups, optionally filtered by organization.
- `list_networks` — List ZeroTier networks visible to the configured token. Works on both API versions; orgId, stats, and permissionCheck are v2 only and rejected on v1, which always lists every network the token can access.
- `list_org_members` — v1 only: list user members of an organization.
- `list_orgs` — v2 only: list organizations the service account can access.
- `list_service_accounts` — v2 only: list service accounts in an organization.
- `list_webhooks` — v2 only: list webhooks in an organization.
- `reject_member` — v2 only: reject one member on a network. [destructive]
- `reject_members` — v2 only: reject multiple members on a network in one call. [destructive]
- `remove_iam` — v2 only: remove roles from a principal on an org, network group, or network. [destructive]
- `remove_members` — v2 only: remove multiple members from a network in one call. [destructive]
- `replace_iam` — v2 only: replace all IAM assignments on an org, network group, or network. Existing assignments missing from the list are removed, so an empty list strips every role. [destructive]
- `rotate_webhook_secret` — v2 only: rotate a webhook's signing secret. [destructive]
- `search_principals` — v2 only: search org users by email term.
- `set_network_user_permissions` — v1 only: replace a user's permission set on a network. The call sets all four flags, so omitted flags are sent as false. [destructive]
- `update_api_key` — v2 only: update an API key's description. [write]
- `update_current_user` — v2 only: update the authenticated user's profile. [write]
- `update_flow_rules` — v2 only (beta): update a network's flow rules (custom rule source or isolation config). [destructive]
- `update_member` — Update a network member. v1 fields: name, description, authorized, activeBridge, noAutoAssignIps, ipAssignments. v2 fields: name, description, activeBridge, noAutoAssignIps, ipv4Assignments, ipv6Assignments. Fields from the other API version are rejected; on v2 change authorization with authorize_member or deauthorize_member. [destructive]
- `update_network` — Update a ZeroTier network's name, description, and/or configuration fields. [destructive]
- `update_network_group` — v2 only: rename or re-describe a network group. [write]
- `update_service_account` — v2 only: update a service account's name or description. [write]
- `update_user` — v1 only: update a user's profile fields. [write]
- `update_webhook` — v2 only: update a webhook's URL, event list, or description. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ZeroTier state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ZeroTier is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/zerotier
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- ZeroTier homepage: https://www.zerotier.com
- API documentation: https://docs.zerotier.com/api/
