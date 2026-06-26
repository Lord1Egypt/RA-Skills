---
name: pagerduty-incidents
description: Manage PagerDuty incidents, services, schedules, escalation policies, users, and on-call data via the PagerDuty REST API. Use this skill when users want to create, acknowledge, or resolve incidents, manage on-call schedules, and review service health via PagerDuty.
---

# PagerDuty Incidents

![PagerDuty Incidents](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/pagerduty.svg?v=2)

Access PagerDuty's incident management platform via the PagerDuty REST API. Manage incidents, services, schedules, escalation policies, users, and on-call data.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pagerduty-incidents) for hosted connection flows and credentials so you do not need to configure PagerDuty API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect PagerDuty |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect PagerDuty |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ PagerDuty REST   │
│   (User Chat)   │     │   (API Key)  │     │      API         │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │  3. Connect PagerDuty│                       │
          │                      │  4. Secure Proxy      │
          │                      │  5. API Requests      │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │ PagerDuty│
    │  File    │           │ Auth     │           │ Platform │
    └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for PagerDuty again."

## Quick Start

```bash
# List recent incidents
clawlink_call_tool --tool "pagerduty_list_incidents" --params '{"status": "triggered", "limit": 25}'

# Get incident details
clawlink_call_tool --tool "pagerduty_get_incident" --params '{"incident_id": "INCIDENT_ID"}'

# List services
clawlink_call_tool --tool "pagerduty_list_services" --params '{}'
```

## Authentication

All PagerDuty tool calls are authenticated automatically by ClawLink using the user's PagerDuty account.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every PagerDuty API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=pagerduty and connect PagerDuty.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `pagerduty` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration pagerduty
```

**Response:** Returns the live tool catalog for PagerDuty.

### Reconnect

If PagerDuty tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=pagerduty
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration pagerduty`

## Security& Permissions

- Access is scoped to incidents, services, schedules, and data within the connected PagerDuty account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete service, remove user) must be confirmed.
- Incident reassignment, escalation changes, and schedule modifications affect real on-call workflows — confirm carefully.

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm PagerDuty is connected.
2. Call `clawlink_list_tools --integration pagerduty` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `pagerduty`.
5. If no PagerDuty tools appear, direct the user to https://claw-link.dev/dashboard?add=pagerduty.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List incidents → Get details → Show status      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call           │
│                                                             │
│  Example: Describe tool → Preview changes → User approves   │
│           → Execute update                                  │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Code Examples

### List incidents

```bash
clawlink_call_tool --tool "pagerduty_list_incidents" \
  --params '{
    "statuses": ["triggered", "acknowledged"],
    "limit": 50,
    "sort_by": "created_at",
    "order": "desc"
  }'
```

### Create an incident

```bash
clawlink_call_tool --tool "pagerduty_create_incident" \
  --params '{
    "title": "High CPU usage on prod-server-01",
    "service_id": "SERVICE_ID",
    " urgency": "high",
    "incident_key": "cpu-prod-server-01",
    "body": {
      "type": "incident_body",
      "details": "CPU usage exceeded 90% for 5 minutes"
    }
  }'
```

### Acknowledge an incident

```bash
clawlink_call_tool --tool "pagerduty_acknowledge_incident" \
  --params '{
    "incident_id": "INCIDENT_ID"
  }'
```

### Get on-call schedule

```bash
clawlink_call_tool --tool "pagerduty_get_on_call" \
  --params '{
    "escalation_policy_ids": ["ESCALATION_POLICY_ID"]
  }'
```

## Notes

- PagerDuty API has rate limits. Use exponential backoff when encountering 429 errors.
- Incident IDs and service IDs are strings — verify IDs before passing to write operations.
- Status transitions (triggered → acknowledged → resolved) follow strict rules — not all transitions are valid from all states.
- On-call queries require escalation policy IDs — list escalation policies first if needed.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration pagerduty`. |
| Missing connection | PagerDuty is not connected. Direct the user to https://claw-link.dev/dashboard?add=pagerduty. |
| `not_found` | Incident, service, or user does not exist. Check the ID. |
| `invalid_state_transition` | Status transition is not allowed from current state. |
| `validation_error` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Rate limited | Too many requests. Wait and retry with exponential backoff. |
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

1. Ensure the integration slug is exactly `pagerduty`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [PagerDuty REST API Reference](https://developer.pagerduty.com/api-reference/)
- [Incidents API](https://developer.pagerduty.com/api-reference/rZMyfN/incidents/)
- [Services API](https://developer.pagerduty.com/api-reference/R4FyWD/services/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pagerduty-incidents
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [PagerDuty](https://clawhub.ai/hith3sh/pagerduty-incidents) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=pagerduty-incidents)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
