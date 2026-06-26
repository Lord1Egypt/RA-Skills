---
name: openclaw_interaction_bridge
description: "Bridge OpenClaw agent interactions to any external program! The Snarling demo, for example, shows what the agent is doing and lets you approve or reject actions with physical A/B buttons and send notifications with a feedback loop for attunement."
type: code-plugin
envVars:
  - OPENCLAW_APPROVAL_SECRET
metadata:
  openclaw:
    emoji: "🟥"
---

# OpenClaw Interaction Bridge 🟥

> Agent state on a screen. Approvals on a button. Notifications that learn. No keyboard required.

A plugin that bridges OpenClaw agent activity to any external program! [Snarling](https://github.com/snarflakes/snarling) for example — a Raspberry Pi + DisplayHAT Mini companion that shows what the agent is doing and lets you approve or reject actions with physical A/B buttons and lets agents send notifications with a feedback loop for attunement!

## What It Does

### State Display

The plugin hooks into OpenClaw events and POSTs state updates to Snarling's display server:

| Agent Activity | Snarling Shows | Trigger |
|---|---|---|
| Using tools | `processing` | `before_tool_call` |
| Generating response | `communicating` | `before_agent_reply` |
| 30s idle | `sleeping` | Auto-timeout |

Duplicates are suppressed — only state *changes* are sent. After 30 seconds of no activity, the display automatically goes to sleep.

### Physical Approvals — `request_user_approval`

The plugin registers a `request_user_approval` tool that routes yes/no decisions to Snarling's physical A/B buttons. **Use this tool whenever you need a human decision before proceeding with an action.**

#### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `action` | string | Yes | Short verb phrase, max **24 chars** (e.g., `delete_file`, `send_email`, `publish_skill`). Shown on the display header line. |
| `message` | string | Yes | Brief explanation, max **60 chars** ideal, **80 chars** hard limit. Shown as 2 lines of ~29 chars each on the physical display. Keep it concise — long text gets truncated. (e.g., `Delete /tmp/old-logs? Cannot undo.`) |

#### When to Use

- **Before destructive actions**: deleting files, dropping databases, overwriting configs
- **Before external actions**: sending emails, posting to social, making API calls that change state
- **Before irreversible operations**: publishing packages, deploying to production, transferring funds
- **When uncertain**: if you're not sure the user would want you to proceed, ask first

#### When NOT to Use

- Reading files, checking status, browsing — these are safe internal actions
- When the answer is obvious and the user explicitly asked you to do it
- In group chats or shared channels (the approval goes to a single physical device)

#### How It Works

1. You call `request_user_approval({ action, message })`
2. Plugin creates a TaskFlow and sets it to waiting
3. Snarling displays the request on screen with an A/B button prompt
4. Human presses **A** (approve) or **B** (reject)
5. Snarling forwards the decision to the plugin's `/approval-callback` route
6. Plugin resumes the TaskFlow and returns the result

The tool **blocks** until a response comes back. Only one approval at a time — if another is in progress, the call returns an error message instead of blocking.

#### Return Values

- `✅ APPROVED` — proceed with the action
- `❌ REJECTED` — do not proceed; respect the user's decision
- `⏰ Timed out` — no response within 30 minutes; treat as rejected
- `⚠️ Approval request blocked` — another approval is already waiting; finish that one first

#### Example

```
request_user_approval({
  action: "delete_file",
  message: "Delete old-config.yaml? 90d old, cannot undo."
})
```

**Bad example** (too long, gets truncated on display):
```
request_user_approval({
  action: "delete_important_configuration_file",  // too long for header
  message: "Delete /home/pi/old-config.yaml? This file has not been modified in 90 days and contains important settings."  // way too long
})
```

### Notifications — `send_notification`

The plugin registers a `send_notification` tool that sends informational alerts to the Snarling display. Unlike approvals, notifications don't require a decision — they're for things the agent wants you to know about.

#### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `message` | string | Yes | The notification text, max **60 chars** ideal. Shown across 2-3 rotating banners on the display. |
| `priority` | string | No | `high`, `normal` (default), or `low`. Controls LED color, status boxes, and timeout behavior. |
| `duration` | number | No | Display duration in seconds. Default `0` = use priority-based timeout (high/normal: no timeout; low: 300s auto-dismiss). |

#### Priority Behavior

| Priority | LED Color | Status Boxes | Timeout | Behavior |
|---|---|---|---|---|
| `high` | Warm orange | 5/5 filled | None | Stays until you interact |
| `normal` | Yellow | 3/5 filled | None | Stays until you interact |
| `low` | Soft yellow | 1/5 filled | 300s | Auto-dismisses, sends `timed_out` feedback |

#### How It Works

1. Agent calls `send_notification({ message, priority })`
2. Plugin POSTs to Snarling's `/approval/alert` endpoint with `type: "notification"`
3. Snarling shows a subtle visual alert — the creature's face changes, LED pulses, status boxes fill
4. **No text is shown until you press A** — the notification stays as a subtle presence
5. Press **A** to reveal the notification text, **B** to dismiss without reading
6. Snarling sends feedback back to the agent: `revealed`, `dismissed`, or `timed_out` with `time_to_reveal_sec`

#### Notification Feedback Loop

Every notification gets a feedback callback:

```json
{
  "notification_id": "notify-1234567890-abc",
  "revealed": true,
  "time_to_reveal_sec": 42.5,
  "dismissed": false,
  "timed_out": false,
  "present": true
}
```

`time_to_reveal_sec` measures total time from when the notification was **sent** to when you interacted — including any queue time behind other notifications. This enables **notification attunement**: the agent learns what kinds of messages you respond to and when.

Feedback is sent **once per notification** — on reveal (A press), dismiss (B press), or timeout. Post-reveal dismiss does not send a second callback.

## Setup

### Prerequisites

- Raspberry Pi with DisplayHAT Mini
- [Snarling](https://github.com/snarflakes/snarling) running (display server on port 5000)
- OpenClaw gateway >= 2026.3.24-beta.2

### Install

```bash
# Clone to your OpenClaw extensions directory
git clone https://github.com/snarflakes/openclaw-interaction-bridge.git \
  ~/.openclaw/extensions/openclaw-interaction-bridge

# Install dependencies
cd ~/.openclaw/extensions/openclaw-interaction-bridge
npm install

# Restart OpenClaw
openclaw gateway restart
```

### Custom Targets

To point at something other than the default Snarling ports (e.g., a Tauri app, mobile web view), edit the constants at the top of `index.ts`:

```typescript
const SNARLING_URL = "http://localhost:5000/state";              // → your state endpoint
const CALLBACK_BASE_URL = "http://localhost:18789";              // → your callback base URL
```

For the approval secret (used to authenticate callback requests), set the `OPENCLAW_APPROVAL_SECRET` environment variable. If not set, a random secret is generated on each startup. When using a custom target, ensure the `secret` is included in the request body for callbacks.

No config file needed yet — when there are multiple adapters, a config-driven system will make sense. For now, editing the source is simpler and more honest.

## Architecture

```
┌─────────────┐     HTTP POST      ┌──────────────┐   button press    ┌──────────────┐
│  OpenClaw    │ ────────────────── │  Snarling     │ ───────────────► │  OpenClaw    │
│  (plugin)    │   /state (5000)   │  Display      │  webhook + WS    │  Gateway     │
│              │ ────────────────── │  + Buttons    │  wake           │              │
│              │   /approval/alert  │               │                  │              │
│              │ ────────────────── │               │ ───────────────► │              │
│              │   /approval/alert  │               │  /approval-cb    │              │
│              │   (type: notify)   │               │ ───────────────► │              │
│              │                    │               │  /notification-cb│              │
└─────────────┘                    └──────────────┘                  └──────────────┘
```

- **State updates**: Plugin → Snarling `/state` (agent activity)
- **Approvals**: Plugin → Snarling `/approval/alert` → Human presses A/B → Snarling → Gateway `/approval-callback`
- **Notifications**: Plugin → Snarling `/approval/alert` (type: notify) → Human interacts → Snarling → Gateway `/notification-callback`
- **Wake**: Snarling sends WebSocket RPC wake to bypass gateway `requests-in-flight` check

## Troubleshooting

- **Display not updating**: Check that Snarling's state server is running on port 5000 (`curl -s http://localhost:5000/health`)
- **Approvals not working**: Verify Snarling is running and the callback route is accessible on port 18789
- **Notifications not showing**: Check that the plugin can reach Snarling on port 5000
- **Notification feedback not received**: Verify the gateway callback route on port 18789 is accessible; check gateway logs for `/notification-callback` hits
- **Stuck approval lock**: Wait 30 minutes for the stale timeout, or restart the gateway
- **Plugin not loading**: Check `openclaw gateway restart` logs for errors; verify `npm install` completed; clear jiti cache with `rm -f /tmp/jiti/openclaw-interaction-bridge-*.cjs`

## Install from ClawHub

```bash
openclaw plugins install clawhub:@snarflakes/openclaw-interaction-bridge
```