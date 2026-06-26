---
name: hostinger-hosting
description: Hostinger API integration via managed credentials. Inspect domains, DNS records, VPS instances, websites, subscriptions, and hosting account data. Use this skill when users want to manage their Hostinger hosting account or query account information.
---

# Hostinger

![Hostinger](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/hostinger.svg)

Access Hostinger via the Hostinger API with managed credentials. Inspect domains, DNS records, VPS instances, websites, subscriptions, and hosting account details.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=hostinger-hosting) for hosted connection flows and credentials so you do not need to configure Hostinger API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Hostinger |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Hostinger |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│    Hostinger     │
│   (User Chat)   │     │   (OAuth)    │     │   (API v1)       │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Hostinger  │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │ Hostinger │
   │  File    │           │ Auth     │           │   API    │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Hostinger again."

## Quick Start

```bash
# List domains
clawlink_call_tool --tool "hostinger_list_domains" --params '{}'

# Get DNS records
clawlink_call_tool --tool "hostinger_get_dns_records" --params '{"domain": "example.com"}'

# List VPS instances
clawlink_call_tool --tool "hostinger_list_vps" --params '{}'
```

## Authentication

All Hostinger tool calls are authenticated automatically by ClawLink using the user's connected Hostinger account.

**No API key is required in chat.** ClawLink stores the credentials securely and injects them into every Hostinger API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=hostinger and connect Hostinger.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `hostinger` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration hostinger
```

**Response:** Returns the live tool catalog for Hostinger.

### Reconnect

If Hostinger tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=hostinger
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration hostinger`

## Security & Permissions

- Access is scoped to the Hostinger account and resources configured in the connection.
- **All write operations require explicit user confirmation.** Before executing any DNS change, hosting configuration, or domain update, confirm the target and intended effect with the user.
- Destructive actions (delete DNS record, cancel subscription) are marked as high-impact and must be confirmed.

## Tool Reference

### Domain Management

| Tool | Description | Mode |
|------|-------------|------|
| `hostinger_list_domains` | List all domains in the account | Read |
| `hostinger_get_domain` | Get details for a specific domain | Read |
| `hostinger_check_domain_availability` | Check if a domain name is available for registration | Read |
| `hostinger_get_domain_dnssec` | Get DNSSEC configuration for a domain | Read |
| `hostinger_get_domain_ownership_status` | Get domain ownership verification status | Read |

### DNS Management

| Tool | Description | Mode |
|------|-------------|------|
| `hostinger_list_dns_records` | List all DNS records for a domain | Read |
| `hostinger_get_dns_records` | Get DNS records for a domain | Read |
| `hostinger_create_dns_record` | Create a new DNS record | Write |
| `hostinger_update_dns_record` | Update an existing DNS record | Write |
| `hostinger_delete_dns_record` | Delete a DNS record | Write |
| `hostinger_list_dns_snapshots` | List DNS snapshots for a domain | Read |
| `hostinger_restore_dns_snapshot` | Restore DNS from a snapshot | Write |

### DNS Zone & Forwarding

| Tool | Description | Mode |
|------|-------------|------|
| `hostinger_get_dns_zone` | Get the full DNS zone for a domain | Read |
| `hostinger_create_dns_zone` | Create a new DNS zone | Write |
| `hostinger_delete_dns_zone` | Delete a DNS zone | Write |
| `hostinger_list_domain_forwardings` | List forwarding rules for a domain | Read |
| `hostinger_create_domain_forwarding` | Create a domain forwarding rule | Write |
| `hostinger_delete_domain_forwarding` | Delete a domain forwarding rule | Write |

### Website Management

| Tool | Description | Mode |
|------|-------------|------|
| `hostinger_list_websites` | List all websites on the account | Read |
| `hostinger_get_website` | Get details for a specific website | Read |
| `hostinger_website_stats` | Get traffic and resource usage stats | Read |
| `hostinger_list_ssl_certificates` | List SSL certificates for a website | Read |
| `hostinger_install_ssl` | Install an SSL certificate on a website | Write |

### VPS Management

| Tool | Description | Mode |
|------|-------------|------|
| `hostinger_list_vps` | List all VPS instances | Read |
| `hostinger_get_vps` | Get details for a specific VPS | Read |
| `hostinger_get_vps_stats` | Get resource usage stats for a VPS | Read |
| `hostinger_list_vps_templates` | List available VPS OS templates | Read |
| `hostinger_list_vps_backups` | List backups for a VPS | Read |
| `hostinger_list_vps_snapshots` | List snapshots for a VPS | Read |
| `hostinger_get_vps_snapshot` | Get a specific VPS snapshot | Read |
| `hostinger_create_vps_snapshot` | Create a new VPS snapshot | Write |
| `hostinger_delete_vps_snapshot` | Delete a VPS snapshot | Write |
| `hostinger_list_vps_ssh_keys` | List SSH keys configured for VPS | Read |
| `hostinger_reboot_vps` | Reboot a VPS instance | Write |
| `hostinger_start_vps` | Start a stopped VPS instance | Write |
| `hostinger_stop_vps` | Stop a running VPS instance | Write |

### Account & Billing

| Tool | Description | Mode |
|------|-------------|------|
| `hostinger_list_subscriptions` | List all subscriptions on the account | Read |
| `hostinger_get_subscription` | Get details for a specific subscription | Read |
| `hostinger_list_orders` | List orders and invoices | Read |
| `hostinger_get_order` | Get details for a specific order | Read |
| `hostinger_get_account_info` | Get account information and settings | Read |

### WHOIS & Data

| Tool | Description | Mode |
|------|-------------|------|
| `hostinger_get_whois` | Get WHOIS information for a domain | Read |
| `hostinger_list_data_centers` | List available data center locations | Read |

## Code Examples

### List all domains

```bash
clawlink_call_tool --tool "hostinger_list_domains" \
  --params '{}'
```

### Get DNS records

```bash
clawlink_call_tool --tool "hostinger_get_dns_records" \
  --params '{
    "domain": "example.com"
  }'
```

### Create a DNS record

```bash
clawlink_call_tool --tool "hostinger_create_dns_record" \
  --params '{
    "domain": "example.com",
    "type": "A",
    "name": "www",
    "content": "192.0.2.1",
    "ttl": 3600
  }'
```

### List VPS instances

```bash
clawlink_call_tool --tool "hostinger_list_vps" \
  --params '{}'
```

### List subscriptions

```bash
clawlink_call_tool --tool "hostinger_list_subscriptions" \
  --params '{}'
```

### Check domain availability

```bash
clawlink_call_tool --tool "hostinger_check_domain_availability" \
  --params '{
    "domain": "newdomain.com"
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Hostinger is connected.
2. Call `clawlink_list_tools --integration hostinger` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `hostinger`.
5. If no Hostinger tools appear, direct the user to https://claw-link.dev/dashboard?add=hostinger.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → check → call                                  │
│                                                             │
│  Example: List domains → Get DNS records → Show results   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview → User approves            │
│           → Execute DNS change                               │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer domain, DNS, VPS, and subscription reads before any configuration change.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- DNS changes can take time to propagate across the internet.
- VPS operations (start, stop, reboot) may take a few minutes to complete.
- Domain ownership status is verified through the registrar.
- DNS snapshots allow point-in-time recovery of DNS configuration.
- Subscription renewal dates and billing information can be retrieved for planning purposes.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration hostinger`. |
| Missing connection | Hostinger is not connected. Direct the user to https://claw-link.dev/dashboard?add=hostinger. |
| `RESOURCE_NOT_FOUND` | Domain, VPS, or other resource does not exist. Check the identifier. |
| `INVALID_ARGUMENT` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `hostinger`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Hostinger API Documentation](https://developers.hostinger.com/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=hostinger-hosting
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=hostinger-hosting)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)