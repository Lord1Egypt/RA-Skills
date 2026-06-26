---
name: "health-assistant"
description: "🌟 Your personal Garmin & AI health coach. Analyze sleep and biometric data daily for actionable functional medicine insights."
author: "Susan"
version: "0.1.0"
tags: ["health", "wearable", "sleep analysis", "Garmin", "AI coach"]
intents:
  - "generate health report"
  - "reset configuration"
cron:
  - name: "daily-health-report"
    schedule: "0 8 * * *"
    command: "python src/main.py --daily-report --quiet"
---

# 🦞 Health Assistant
**Make your wearable data speak for you.**

A personalized health coach powered by Garmin data and NotebookLM. 
It automatically syncs your daily steps, sleep, HRV, and body battery, aligns with your personal wellness goals (e.g., improve sleep, manage stress, weight loss), and delivers a highly actionable, medical-grade daily briefing.

## Interfaces

### Trigger Daily Report
**Command**: `python src/main.py --daily-report`
**Description**: Usually triggered by a scheduled task (Cron/Heartbeat) every morning.

### Interactive Setup
**Intent**: `configure_health_assistant`
**Description**: Guides the user to set up health concerns and bind devices.
**Workflow**:
1. Welcome and ask for primary wellness goals (A-F).
2. Select device (1. Garmin).
3. Provide account information.
4. Confirm daily report delivery time.
5. Complete configuration and enable daily briefings.

## Dependencies
- **Garmin API**: Requires Garmin account authorization (stored locally & safely using `garth`).
- **NotebookLM CLI**: `notebooklm-py` and `playwright` must be installed with active Google authentication.
- **OpenClaw Message Plugin**: Used to push reports to Telegram/Discord/WeChat/Feishu.
