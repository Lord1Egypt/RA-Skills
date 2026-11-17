---
name: mobile-agent
description: >-
    Control a real phone from OpenClaw via a local MCP relay. Use when the user asks to
    operate a phone (open apps, tap, input, take screenshots), run an AI automation task
    on a connected Android/iPhone device, check the current phone screen or device info,
    or query/abort a running phone agent task. WARNING: This skill can modify device state
    and perform actions on behalf of the user — see the Safety Notice section before use.
version: 1.0.0
metadata:
    openclaw:
        requires:
            bins:
                - node
        envVars:
            - name: PHONE_AGENT_WS_PORT
              required: false
              description: WebSocket relay port between the MCP server and the browser page (default 7788).
        emoji: "📱"
---

# Phone Agent Skill

Bridges the Mobile AI Agent running in the browser via a local MCP Server, allowing OpenClaw to remotely control a real phone — no extra code needed, just describe the task in natural language.

## ⚠️ Safety Notice — Read Before Use

**This skill performs real actions on a physical device.** The Agent can open apps, tap UI elements, type text, send messages, change settings, and execute multi-step automation workflows — all of which may irreversibly alter device state or have real-world consequences.

### Potential Impacts

| Action Category | Examples | Risk Level |
|----------------|----------|------------|
| **Messaging** | Send WeChat / SMS / Email on your behalf | 🔴 High — recipients will receive the message |
| **Purchases & Payments** | Place orders, confirm payments in apps | 🔴 High — may incur financial charges |
| **Settings Changes** | Toggle Wi-Fi, Bluetooth, system preferences | 🟡 Medium — device behavior will change |
| **App Data** | Delete contacts, clear cache, remove files | 🟡 Medium — data loss may be irreversible |
| **Navigation** | Open apps, search, browse content | 🟢 Low — read-only in nature |

### User Consent Requirements

1. **Explicit confirmation**: Before executing any task that may send messages, trigger purchases, or modify critical settings, the Agent **must** confirm the intended action with the user and wait for explicit approval.
2. **Clear task scope**: Users should describe tasks precisely. Vague commands (e.g. "clean up my phone") may lead to unintended operations.
3. **Supervision recommended**: For first-time use or high-risk operations, stay present and observe the Agent's execution in real time via the screen mirror.
4. **Abort capability**: Call `abort_task` at any time to immediately stop the Agent if it begins an unintended action.

### Best Practices for AI Agents Calling This Skill

- **Always ask the user for confirmation** before calling `run_agent_task` with goals that involve sending messages, making purchases, deleting data, or changing system settings.
- **Prefer read-only operations first**: Use `take_screenshot` and `get_device_status` to inspect the current state before executing write operations.
- **Never auto-retry failed tasks** that involve financial transactions or irreversible actions without re-confirming with the user.

## When to Use This Skill

- The user asks to operate a real phone (open apps, tap, input, swipe)
- The user asks to view the current phone screen (screenshot)
- The user asks to query device information (model, OS version)
- The user asks to run a multi-step AI automation task on the phone
- The user asks to query/abort a running Agent task

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                        External AI Agent                             │
│              (OpenClaw / Qoder / Claude Desktop / Chrome AI)         │
└───────────┬──────────────────────────────────────────┬───────────────┘
            │ Channel A: stdio JSON-RPC 2.0            │ Channel B: document
            ▼                                          │   .modelContext
┌───────────────────────────────┐                      │   .callTool()
│  mcp-server/dist/server.js    │                      ▼
│  (Node.js McpServer)          │      ┌───────────────────────────────┐
│  6 Tools registered on stdio  │      │   Chrome WebMCP Runtime       │
└───────────┬───────────────────┘      │   (#enable-webmcp-testing)    │
            │ WebSocket                └───────────────┬───────────────┘
            │ ws://localhost:7788                      │ execute()
            ▼                                          ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    Browser Page (Mobile AI Use)                      │
│   McpRelayClient (Channel A)    WebMcpService (Channel B)            │
│                └────────────┬────────────┘                           │
│                             ▼  McpServiceContext (shared)            │
│            Plan-and-Resolve Agent / ReAct Agent                      │
└─────────────────────────────┬────────────────────────────────────────┘
                              │  Web ADB
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                       Android / iOS Device                           │
└──────────────────────────────────────────────────────────────────────┘
```

## Installation/Setup

### 1. Start the Local MCP Server

```bash
cd <project-root>/mcp-server
npm install      # Install dependencies on first run
npm run build    # Compile TypeScript
npm start        # Start the server (listens on stdio + WebSocket :7788)
```

### 2. Open the Mobile AI Agent Page

Navigate to https://mobile-ai-use.xyz/mobileAi — the **Relay** indicator in the top-right corner of the page header turning green indicates a successful connection.

### 3. Connect the Phone

Connect an Android device via USB; the page should display "Connected".

### 4. Configure OpenClaw (add to `openclaw.json`)

```json5
{
  mcp: {
    servers: {
      "phone-agent": {
        command: "node",
        // Replace <PROJECT_ROOT> with the actual absolute path
        args: ["<PROJECT_ROOT>/mcp-server/dist/server.js"],
        env: {
          // Optional: change the WebSocket port (default 7788)
          PHONE_AGENT_WS_PORT: "7788"
        }
      }
    }
  }
}
```

You can also configure via CLI:

```bash
openclaw mcp set phone-agent --command node --args "<PROJECT_ROOT>/mcp-server/dist/server.js"
```

## Usage

Simply describe the task in natural language — no coding required:

> Open WeChat, find the conversation with Zhang San, and send a "Hello" message

> Take a screenshot to see what's currently on the phone screen

> Open phone Settings and check the system version information

> Abort the currently running task

> What was the result of the most recent Agent task

## Tool Reference

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `run_agent_task` | ⚠️ **Write** — Run a multi-step AI automation task on the phone (may modify device state) | `goal` (required), `timeoutMs` (default 1200s) |
| `abort_task` | Abort the currently running task | — |
| `take_screenshot` | Read — Capture the phone screen, returns a PNG image | — |
| `get_device_status` | Read — Query device model, OS version, and other info | — |
| `get_task_result` | Read — Query detailed task results by taskId | `taskId` (required), `includeSteps` (default true) |
| `get_latest_task` | Read — Get the result of the most recent task | — |

## Full Call Chain

```
OpenClaw Agent
    │ stdio JSON-RPC 2.0
    ▼
mcp-server/dist/server.js  (Node.js MCP Server)
    │ WebSocket ws://localhost:7788
    ▼
Browser Page AiChatPanel (McpRelayClient)
    │ McpServiceContext
    ▼
PlanResolveAgent / ReAct Agent
    │ Web ADB
    ▼
Phone
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Relay indicator is red | Confirm `npm start` is running in the mcp-server directory |
| Tool call times out | An Agent task is still running — wait or call `abort_task` |
| Phone not responding | Check the ADB connection; the page should show the device as "Connected" |
| Port 7788 is occupied | Set `PHONE_AGENT_WS_PORT=7789` and update the MCP configuration accordingly |
