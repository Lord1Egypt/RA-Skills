---
name: agent-sdk
description: 'Build autonomous AI features using the Polsia Agent API only; never call model providers directly for product AI.'
---

# Agent SDK

Build AI agents that work autonomously for end users. Use the Polsia API proxy for ALL AI features — never call model providers directly.

## Key Rules
- NEVER call anthropic.messages.create() or openai.chat.completions.create() for AI features
- ONLY use POLSIA_API_URL with POLSIA_API_KEY
- Use runAgent() for autonomous tasks needing real-time data or tools
- Use chat() for simple prompt-response patterns

## Available MCPs
gmail, github, slack, google_calendar, google_sheets

## Auto-Mounted Tools (no config needed)
- save_data({ type, data }) — stores to agent_data table
- send_email({ to, subject, body }) — sends from {slug}@polsia.app
