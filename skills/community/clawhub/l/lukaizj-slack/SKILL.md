---
name: Slack Integration
description: Slack integration - Send messages, manage channels, and automate Slack workflows
homepage: https://github.com/lukaizj/slack-integration-skill
tags:
  - productivity
  - integration
  - slack
  - messaging
requires:
  env:
    - SLACK_BOT_TOKEN
files:
  - slack.py
---

# Slack Integration

Slack integration skill for OpenClaw. Send messages, manage channels, and automate Slack workflows.

## Setup

1. Create a Slack app at https://api.slack.com/apps
2. Get Bot User OAuth Token
3. Add required scopes: channels:read, chat:write, groups:read
4. Configure SLACK_BOT_TOKEN environment variable