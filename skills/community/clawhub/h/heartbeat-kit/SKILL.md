---
name: "HeartbeatKit — Plug-and-Play Agent Heartbeat Configs"
description: "Pre-built HEARTBEAT.md templates for common agent tasks: email checking, calendar monitoring, weather alerts, system health, news digests. Drop in and go."
author: "@TheShadowRose"
version: "1.0.0"
tags: ["heartbeat", "automation", "monitoring", "templates", "scheduling", "agent-ops"]
license: "MIT"
---

# HeartbeatKit — Plug-and-Play Agent Heartbeat Configs

Pre-built HEARTBEAT.md templates for the most common agent monitoring tasks. Pick a template, drop it in your workspace, customize the variables, done.

## What's Included

| Template | What It Does |
|----------|-------------|
| `email-check.md` | Check unread emails, surface urgent ones |
| `calendar-watch.md` | Upcoming events in next 24-48h, prep reminders |
| `weather-brief.md` | Local weather + "should I bring an umbrella?" |
| `system-health.md` | Disk, memory, CPU, service status |
| `news-digest.md` | Headlines from configured topics |
| `social-monitor.md` | Check mentions/notifications across platforms |
| `project-status.md` | Git status, open PRs, build status |
| `combined-lite.md` | Email + calendar + weather in one check |
| `combined-full.md` | Everything above, rotated across heartbeats |

## Usage

1. Copy your chosen template to your workspace as `HEARTBEAT.md`
2. Edit the variables at the top (email account, location, repos, etc.)
3. Your agent picks it up on next heartbeat

See README.md for full documentation and customization guide.
