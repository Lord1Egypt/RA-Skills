---
name: oo-tailscale
description: "Tailscale (tailscale.com). Use this skill for ANY Tailscale request — reading, creating, updating, and deleting data. Whenever a task involves Tailscale, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Tailscale"
  author: "OOMOL"
  version: "1.0.5"
  services: ["tailscale"]
  icon: "https://static.oomol.com/logo/third-party/tailscale.png"
---

# Tailscale

Operate **Tailscale** through your OOMOL-connected account. This skill calls the `tailscale` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Tailscale. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tailscale" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tailscale" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `approve_user` — Approve a pending Tailscale user for the tailnet. [write]
- `batch_update_device_posture_attributes` — Set or remove custom posture attributes across multiple Tailscale devices. [destructive]
- `create_key` — Create an auth key, OAuth client credential, or federated trust credential and return its secret. [write]
- `create_oauth_app` — Create a Tailscale OAuth application and return its client secret. [write]
- `create_posture_integration` — Create a device posture integration using its external provider credentials. [write]
- `create_webhook` — Create a webhook endpoint and return its signing secret. [write]
- `delete_device` — Permanently delete a device from its Tailscale tailnet. [destructive]
- `delete_device_invite` — Delete a Tailscale device share invite. [destructive]
- `delete_device_posture_attribute` — Permanently remove one custom posture attribute from a Tailscale device. [destructive]
- `delete_key` — Permanently revoke and delete a Tailscale trust credential or key. [destructive]
- `delete_oauth_app` — Permanently delete a Tailscale OAuth application and revoke its access. [destructive]
- `delete_posture_integration` — Delete a device posture integration. [destructive]
- `delete_service` — Permanently delete a named Tailscale Service. [destructive]
- `delete_user` — Permanently delete a Tailscale user from the tailnet. [destructive]
- `delete_webhook` — Permanently delete a Tailscale webhook endpoint. [destructive]
- `disable_log_streaming` — Disable and remove the destination configuration for a Tailscale log stream. [destructive]
- `expire_device_key` — Immediately expire a device key and require the device to authenticate again. [write]
- `get_aws_external_id` — Create or retrieve the AWS external ID used by Tailscale log streaming. [write]
- `get_contacts` — Get the account, support, and security contacts for the tailnet.
- `get_device` — Get one Tailscale device by its preferred node ID or legacy device ID.
- `get_device_invite` — Get one Tailscale device share invite.
- `get_device_posture_attributes` — Get the posture attributes currently reported for a Tailscale device.
- `get_dns_configuration` — Get the complete DNS configuration for the tailnet.
- `get_dns_preferences` — Get the tailnet DNS preferences, including MagicDNS state.
- `get_key` — Get metadata for a Tailscale trust credential or key.
- `get_log_streaming_configuration` — Get the potentially sensitive destination configuration for a Tailscale log stream.
- `get_log_streaming_status` — Get the current publishing status for configuration or network log streaming.
- `get_oauth_app` — Get a Tailscale OAuth application by app ID.
- `get_policy_file` — Get the current Tailscale policy file as JSON, optionally with validation details.
- `get_posture_integration` — Get one device posture integration by ID.
- `get_service` — Get a Tailscale Service by name.
- `get_service_device_approval` — Get whether a Service is approved on a specific device.
- `get_split_dns` — Get the split DNS nameserver mapping for the tailnet.
- `get_tailnet_settings` — Get the tailnet feature, logging, networking, and policy settings visible to the OAuth client.
- `get_user` — Get a Tailscale user by user ID.
- `get_webhook` — Get a Tailscale webhook endpoint by ID.
- `list_configuration_audit_logs` — List configuration audit logs for an RFC 3339 time window, with optional filters.
- `list_device_invites` — List all share invites for a Tailscale device.
- `list_device_routes` — List the subnet routes advertised and enabled for a Tailscale device.
- `list_devices` — List all devices in the configured Tailscale tailnet.
- `list_dns_nameservers` — List the global DNS nameservers configured for the tailnet.
- `list_dns_search_paths` — List the DNS search paths configured for the tailnet.
- `list_keys` — List trust credentials and keys visible to the OAuth client.
- `list_network_flow_logs` — List network flow logs for an RFC 3339 time window.
- `list_oauth_apps` — List OAuth applications configured for the tailnet.
- `list_posture_integrations` — List the device posture integrations configured for the tailnet.
- `list_service_hosts` — List devices currently hosting a named Tailscale Service.
- `list_services` — List the Services configured in the tailnet.
- `list_users` — List tailnet users with optional user-type and role filters.
- `list_webhooks` — List webhook endpoints configured for the tailnet.
- `preview_policy_rule_matches` — Preview which rules in a proposed policy match a user or IP address and port without saving it.
- `resend_contact_verification_email` — Resend the verification email for a tailnet contact. [write]
- `restore_user` — Restore a suspended Tailscale user. [write]
- `rotate_webhook_secret` — Rotate a webhook signing secret and return the new secret once.
- `set_device_authorized` — Authorize or deauthorize a Tailscale device. [destructive]
- `set_device_ip` — Set the Tailscale IPv4 address for a device. [write]
- `set_device_key_expiry` — Enable or disable key expiry for a Tailscale device. [destructive]
- `set_device_name` — Set a Tailscale device name, or reset it from the OS hostname with an empty name. [destructive]
- `set_device_posture_attribute` — Set one custom posture attribute on a Tailscale device. [destructive]
- `set_device_routes` — Replace the enabled subnet routes for a Tailscale device. [destructive]
- `set_device_tags` — Replace all ACL tags assigned to a Tailscale device. [destructive]
- `set_dns_configuration` — Replace the entire tailnet DNS configuration, including nameservers, split DNS, search paths, and preferences. [destructive]
- `set_dns_nameservers` — Replace the global DNS nameservers configured for the tailnet. [destructive]
- `set_dns_preferences` — Enable or disable MagicDNS for the tailnet. [destructive]
- `set_dns_search_paths` — Replace the DNS search paths configured for the tailnet. [destructive]
- `set_log_streaming_configuration` — Create or replace a Tailscale log streaming destination configuration. [destructive]
- `set_policy_file` — Replace the Tailscale policy file after its embedded tests pass. [destructive]
- `set_split_dns` — Replace the entire tailnet split DNS configuration. [destructive]
- `suspend_user` — Suspend a Tailscale user and their access to the tailnet. [destructive]
- `test_webhook` — Send a test event to a Tailscale webhook endpoint. [write]
- `update_contact` — Change the account, support, or security contact email for the tailnet. [write]
- `update_key` — Replace the mutable configuration of an OAuth or federated Tailscale trust credential. [destructive]
- `update_oauth_app` — Replace the configuration of a Tailscale OAuth application. [destructive]
- `update_posture_integration` — Update a device posture integration and optionally replace its client secret. [destructive]
- `update_service` — Create or replace a named Tailscale Service definition. [destructive]
- `update_service_device_approval` — Approve or revoke approval for a Service on a device. [destructive]
- `update_split_dns` — Merge domain-to-resolver entries into the tailnet split DNS configuration. [destructive]
- `update_tailnet_settings` — Update reversible feature, logging, networking, or policy-link settings for the tailnet. [destructive]
- `update_user_role` — Change a Tailscale user's administrative role. [write]
- `update_webhook` — Replace the subscribed events for a Tailscale webhook endpoint. [destructive]
- `validate_aws_external_id` — Validate an AWS IAM role trust policy against a Tailscale external ID.
- `validate_policy_file` — Validate a proposed policy file or run ACL tests without changing the tailnet policy.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Tailscale state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Tailscale is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/tailscale
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Tailscale homepage: https://tailscale.com
- API documentation: https://tailscale.com/docs/reference/tailscale-api
