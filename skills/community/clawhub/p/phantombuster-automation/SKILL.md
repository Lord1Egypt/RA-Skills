---
name: phantombuster-automation
description: Inspect PhantomBuster agents, automations, launches, and workflow data via the PhantomBuster API. Use this skill when users want to monitor automation runs, review output data, and manage PhantomBuster workflows via the PhantomBuster API.
---

# PhantomBuster Automation

![PhantomBuster Automation](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/phantombuster.svg)

Access PhantomBuster's automation platform via the PhantomBuster API. Inspect agents, automations, launches, and workflow data. Trigger or update automations after confirmation.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=phantombuster-automation) for hosted connection flows and credentials so you do not need to configure PhantomBuster API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect PhantomBuster |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect PhantomBuster |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ PhantomBuster    │
│   (User Not Chat)   │     │   (API Key)  │     │     API          │
└─────────────────┘     └──────────────┘     └──────────────────┘
          │                       │                       │
          │  1. Install Plugin   │                       │
          │  2. Pair Device      │                       │
          │3. Connect PhantomBuster│ │
          │                      │  4. Secure Proxy      │
          │                      │  5. API Requests      │
          │                      │                       │
          ▼                      ▼                       ▼
    ┌──────────┐           ┌──────────┐           ┌──────────┐
    │  SKILL   │           │ Dashboard│           │PhantomBstr│
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

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for PhantomBuster again."

## Quick Start

```bash
# List agents
clawlink_call_tool --tool "phantombuster_list_agents" --params '{}'

# Get agent details
clawlink_call_tool --tool "phantombuster_get_agent" --params '{"agent_id": "AGENT_ID"}'

# List launches
clawlink_call_tool --tool "phantombuster_list_launches" --params '{"agent_id": "AGENT_ID"}'
```

## Authentication

All PhantomBuster tool calls are authenticated automatically by ClawLink using the user's PhantomBuster account.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every PhantomBuster API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=phantombuster and connect PhantomBuster.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `phantombuster` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration phantombuster
```

**Response:** Returns the live tool catalog for PhantomBuster.

### Reconnect

If PhantomBuster tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=phantombuster
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration phantombuster`

## Security& Permissions

- Access is scoped to agents, automations, and data within the connected PhantomBuster account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Triggering automations affects third-party systems and may consume rate limits — confirm carefully.
- Destructive actions must be confirmed.

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm PhantomBuster is connected.
2. Call `clawlink_list_tools --integration phantombuster` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `phantombuster`.
5. If no PhantomBuster tools appear, direct the user to https://claw-link.dev/dashboard?add=phantombuster.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List agents → Get details → Show status          │
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

### List agents

```bash
clawlink_call_tool --tool "phantombuster_list_agents" \
  --params '{
    "limit": 20
  }'
```

### Get agent details

```bash
clawlink_call_tool --tool "phantombuster_get_agent" \
  --params '{
    "agent_id": "AGENT_ID"
  }'
```

### List launches for an agent

```bash
clawlink_call_tool --tool "phantombuster_list_launches" \
  --params '{
    "agent_id": "AGENT_ID",
    "status": "finished"
  }'
```

### Get launch output

```bash
clawlink_call_tool --tool "phantombuster_get_launch_output" \
  --params '{
    "launch_id": "LAUNCH_ID"
  }'
```

## Notes

- PhantomBuster API has rate limits. Use exponential backoff when encountering 429 errors.
- Agent IDs and launch IDs are strings — verify IDs before passing to operations.
- Launching automations may affect third-party system rate limits — confirm before triggering.
- Output data from launches may be large — consider pagination or filtering.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration phantombuster`. |
| Missing connection | PhantomBuster is not connected. Direct the user to https://claw-link.dev/dashboard?add=phantombuster. |
| `not_found` | Agent, launch, or resource does not exist. Check the ID. |
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

1. Ensure the integration slug is exactly `phantombuster`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [PhantomBuster API Documentation](https://hub.phantombuster.com/reference)
- [PhantomBuster](https://phantombuster.com/)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=phantombuster-automation
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [PhantomBuster](https://clawhub.ai/hith3sh/phantombuster-automation) — For this skill's native documentation

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=phantombuster-automation)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
