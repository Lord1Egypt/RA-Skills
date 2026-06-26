---
name: kibana-observability
description: Manage Elastic Kibana for observability and security operations. Query data views, manage alerting rules and detection engine rules, handle Fleet agent policies, manage cases, and interact with the Elastic Security solution.
---

# Kibana

![Kibana](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/kibana.svg?v=2)

Manage Elastic Kibana for observability, security, and infrastructure monitoring. Query data views, manage alerting rules, handle detection engine rules, manage Fleet agent policies, and work with cases and security alerts.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=kibana-observability) for hosted connection flows and credentials so you do not need to configure Kibana API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Kibana |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│  Kibana REST API │
│   (User Chat)   │     │   (OAuth)    │     │   (v8.x)        │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin  │                       │
         │  2. Pair Device   │                       │
         │  3. Connect Kibana │                      │
         │                   │  4. Secure Token      │
         │                   │  5. Proxy Requests    │
         │                   │                       │
         ▼                   ▼                       ▼
   ┌──────────┐      ┌──────────┐           ┌──────────┐
   │  SKILL   │      │ Dashboard│           │  Kibana  │
   │  File    │      │ Auth     │           │ Stack   │
   └──────────┘      └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Kibana again."

## Quick Start

```bash
# List data views
clawlink_call_tool --tool "kibana_get_data_views" --params '{}'

# Get alert types
clawlink_call_tool --tool "kibana_get_alert_types" --params '{}'

# List cases
clawlink_call_tool --tool "kibana_get_cases" --params '{}'
```

## Authentication

All Kibana tool calls are authenticated automatically by ClawLink using the user's connected Kibana instance.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Kibana API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=kibana and connect Kibana (requires an active Kibana instance).
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `kibana` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration kibana
```

**Response:** Returns the live tool catalog for Kibana.

### Reconnect

If Kibana tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=kibana
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration kibana`

## Security & Permissions

- Access is scoped to the connected Kibana instance only.
- **All write operations require explicit user confirmation.** Before executing any alerting, case, or Fleet action, confirm the target resource and intended effect with the user.
- Destructive actions (delete rule, delete saved object, delete connector) are marked as high-impact and must be confirmed.
- Fleet agent policy changes affect deployed agents — confirm before executing.
- Detection engine rule changes affect security monitoring — confirm before executing.

## Tool Reference

### Data Views

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_get_data_views` | List all data views (index patterns) available in Kibana | Read |

### Alerting

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_get_alert_types` | Get available rule types with license requirements and configuration options | Read |
| `kibana_get_alerting_rules` | List alerting rules with pagination and filtering | Read |
| `kibana_delete_alerting_rules` | Delete an alerting rule by ID | Write |

### Actions & Connectors

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_get_action_types` | Get available connector types (Slack, Email, Webhook, ServiceNow, etc.) | Read |
| `kibana_get_connectors` | List all configured connectors | Read |
| `kibana_delete_connectors` | Delete a connector by ID | Write |

### Cases

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_get_cases` | List cases with optional filtering by status, assignee, or severity | Read |

### Saved Objects

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_delete_saved_objects` | Delete a saved object (visualization or dashboard) by ID | Write |

### Security Detection Engine

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_get_detection_engine_rules_find` | List detection engine rules with KQL filtering and sorting | Read |

### Alerts

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_find_alerts` | Find and aggregate detection alerts with optional query filtering | Read |

### Endpoint Exceptions

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_get_endpoint_list_items` | List Elastic Endpoint exception list items with filtering | Read |

### Entity Store

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_get_entity_store_engines` | Get entity store engine configurations and status | Read |
| `kibana_get_entity_store_entities_list` | List entity records (users, hosts, services) with paging and filtering | Read |
| `kibana_get_entity_store_status` | Get Entity Store status and configured engines | Read |

### Fleet

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_get_fleet_agent_policies` | List Fleet agent policies with filtering and enrollment counts | Read |
| `kibana_get_fleet_agents_available_versions` | Get available Elastic Agent versions | Read |
| `kibana_get_fleet_agents_setup_status` | Check Fleet setup readiness and missing requirements | Read |
| `kibana_get_fleet_check_permissions` | Verify user permissions for Fleet API operations | Read |
| `kibana_get_fleet_enrollment_api_keys` | List enrollment API keys for agent authentication | Read |
| `kibana_get_fleet_enrollment_api_key` | Get details of a specific enrollment API key by ID | Read |
| `kibana_delete_fleet_output` | Delete a Fleet output configuration by ID | Write |
| `kibana_delete_fleet_proxy` | Delete a Fleet proxy configuration by ID | Write |

### Fleet EPM (Elastic Package Manager)

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_get_fleet_epm_categories` | Get available package categories with counts | Read |
| `kibana_get_fleet_epm_packages` | List available Fleet integration packages | Read |
| `kibana_get_fleet_epm_packages_installed` | List installed Fleet packages | Read |
| `kibana_get_fleet_epm_package_details` | Get detailed package information including data streams and assets | Read |
| `kibana_get_fleet_epm_package_stats` | Get usage statistics for a specific Fleet package | Read |
| `kibana_get_fleet_epm_package_file` | Get a specific file from an EPM package (manifest, README, changelog) | Read |
| `kibana_get_fleet_epm_data_streams` | List available data streams with filtering | Read |

### Lists

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_delete_list` | Delete a list by ID | Write |

### Osquery

| Tool | Description | Mode |
|------|-------------|------|
| `kibana_delete_osquery_saved_queries` | Delete an Osquery saved query by saved object ID | Write |

## Code Examples

### List data views

```bash
clawlink_call_tool --tool "kibana_get_data_views" \
  --params '{}'
```

### Get alert types

```bash
clawlink_call_tool --tool "kibana_get_alert_types" \
  --params '{}'
```

### List cases

```bash
clawlink_call_tool --tool "kibana_get_cases" \
  --params '{}'
```

### Get detection engine rules

```bash
clawlink_call_tool --tool "kibana_get_detection_engine_rules_find" \
  --params '{"page": 1, "per_page": 25}'
```

### Get Fleet agent policies

```bash
clawlink_call_tool --tool "kibana_get_fleet_agent_policies" \
  --params '{}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Kibana is connected.
2. Call `clawlink_list_tools --integration kibana` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `kibana`.
5. If no Kibana tools appear, direct the user to https://claw-link.dev/dashboard?add=kibana.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                     │
│                                                             │
│  Example: List data views → Get index fields → Query data  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call          │
│                                                             │
│  Example: Preview rule delete → User approves → Execute     │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Alert types include Elasticsearch query alerts, index threshold alerts, machine learning anomaly detection, and security detection rules.
- Connector types (action types) include Slack, Email, Webhook, ServiceNow, and more — each with different license requirements.
- Fleet agent policies define configuration for groups of Elastic Agents including which integrations are enabled.
- Entity store aggregates and manages entity data (users, hosts, services) from various sources.
- Endpoint exception list contains security exceptions applied to Elastic Endpoint agents.
- Osquery saved queries require the saved_object_id (UUID format), not the custom id field.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration kibana`. |
| Missing connection | Kibana is not connected. Direct the user to https://claw-link.dev/dashboard?add=kibana. |
| Permission error | The authenticated user lacks permission for this operation. Check Kibana roles. |
| Fleet not ready | Fleet is not properly configured. Check setup status first. |
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

### Troubleshooting: Fleet Not Ready

1. Check Fleet setup status:
   ```bash
   clawlink_call_tool --tool "kibana_get_fleet_agents_setup_status" --params '{}'
   ```
2. Review missing prerequisites and address them before managing agents or policies.
3. Verify Elasticsearch connection and license status.

## Resources

- [Kibana Documentation](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Elastic Fleet Documentation](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html)
- [Elastic Security Solution](https://www.elastic.co/security)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=kibana-observability
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [New Relic Observability](https://clawhub.ai/hith3sh/new-relic-observability) — For New Relic monitoring and alerting
- [Make Automation](https://clawhub.ai/hith3sh/make-automation) — For Make.com workflow automation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=kibana-observability)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)