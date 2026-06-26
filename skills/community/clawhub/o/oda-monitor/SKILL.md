---
name: oda-monitor
description: >
  Monitors websites, APIs, and cron jobs (watchdogs) using Watch.dog.
  Use it when the user asks to "check the status of my monitors", 
  "check uptime", "review watchdogs", or "create a website monitor".
  IMPORTANT: Deleting monitors and watchdogs requires explicit prior confirmation from the user.
  When the user provides their credentials (WATCHDOG_API_KEY, WATCHDOG_API_URL) or modifies them, 
  you MUST automatically execute the `list_monitors` tool as a silent test to verify the connection, 
  and then inform them if it was successful by showing a summary of what the skill can do.
version: "1.0.0"
author: Oda Monitor Team
clawhub: true
metadata:
  openclaw:
    emoji: "🐕"
    requires:
      bins: ["node"]
mcp:
  transport: stdio
  command: node
  args: ["{baseDir}/index.js"]
  env:
    WATCHDOG_API_KEY: ""
    WATCHDOG_API_URL: "https://api.watch.dog/api/mcp_server.php"
---

# Watch.dog Uptime – OpenClaw Skill

## What does this skill do?

Connects your AI agent with the **Watch.dog** platform to:

- 🔭 **Actively monitor** websites, APIs, IPs, and ports (HTTP, Keyword, Ping)
- 🫀 **Watch scheduled tasks** (cron jobs, backups, scripts) through Passive Watchdogs (Heartbeats)
- 📊 **Check the status** of your infrastructure in real-time
  - Monitor statuses are interpreted as follows:
    - `null`: Pending
    - `0`: Down (Offline)
    - `1`: Up (Online)
    - `2`: New (New/Created)
- 🗑️ **Manage resources** (Pause, Resume, Delete)
- 🌐 **Public Status Pages** (Tracker Pages)

## When to activate this skill

Use it when the user:

- Wants to create a monitor for a URL, website, API, or server
- Asks about the status, historical uptime, or availability of their services
- Needs to configure a watchdog for a scheduled task or cron job
- Asks for a summary of their monitored infrastructure
- Wants to pause, resume, or delete monitors or watchdogs from their account
- Requests to configure their public status page (Tracker Page)

## Required Configuration

Create a `.env` file in this folder with:

```env
WATCHDOG_API_KEY="sk_live_your_key_here"
WATCHDOG_API_URL="api_url_here" | "https://api.watch.dog/api/mcp_server.php"
```

> If you don't have an API Key, create one in your dashboard at [watch.dog](https://watch.dog).

### Clarification about Intervals

- When creating monitors (`create_monitor`) or watchdogs (`create_watchdog`), if the user specifies a time (e.g. "every 5 minutes"), **always pass the exact value in seconds** (e.g. 300).
- Be aware the remote API may auto-correct the interval if the user's plan does not support such high frequencies, so report the returned interval accurately.

## Available Tools

| Tool                         | Description                                         |
| ---------------------------- | --------------------------------------------------- |
| `list_monitors`              | Lists all active monitors                           |
| `create_monitor`             | Creates an Active Monitor (HTTP, Keyword, Ping)     |
| `get_monitor_status`         | Status and recent events of a specific monitor      |
| `pause_monitor`              | Temporarily pauses an Active Monitor                |
| `resume_monitor`             | Resumes a previously paused Active Monitor          |
| `delete_monitor`             | Deletes an Active Monitor (Requires Confirmation)   |
| `get_monitor_uptime_history` | Uptime/Availability matrix of a monitor             |
| `update_tracker_page`        | Configures the Public Status Page (`/monitors/...`) |
| `list_watchdogs`             | Lists all Passive Watchdogs/Heartbeats              |
| `create_watchdog`            | Creates a Passive Watchdog for a cron job           |
| `get_watchdog_status`        | Health status of the last ping of a watchdog        |
| `delete_watchdog`            | Deletes a Passive Watchdog (Requires Confirmation)  |

## Installation

```bash
cd oda-monitor
npm install
```
