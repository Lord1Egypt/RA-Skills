---
name: mcm-agent
slug: mcm-agent
version: 1.0.0
homepage: https://clawsafe.vip
description: Help users manage cross-device AI memory. When user explicitly asks to save or recall information, sync it to their cloud memory account. Categorizes saved content into personality, preferences, chat history, and long-term memory. User must configure their API key and explicitly consent before any sync happens. Supports Claude Code, Windsurf, Cursor, Codex, OpenClaw, Hermes Agent, Cline and all major AI agents. Free 200 entries. MCM, memory, agent memory, cloud memory, sync, 记忆同步, 跨设备记忆, 云端记忆, AI记忆, 智能记忆, 对话同步, 长期记忆, 跨平台同步, 记忆管家, AI对话记录, 角色记忆, 偏好记忆, 记忆云
triggers:
  - memory
  - mcm
  - agent memory
  - cloud memory
  - memory sync
  - 记忆
  - 同步
  - 云端记忆
user-invocable: false
---

# MCM Agent — My Cloud Memory

Help users manage their AI memory across devices. All syncing requires explicit user consent.

## Getting Started

1. **Install**: Search "mcm-agent" in skill store, or copy to `~/.claude/skills/mcm-agent/`
2. **Account**: User signs up at https://clawsafe.vip to get their API Key
3. **Configure**: User provides their API Key to enable the service
4. The service will only sync when the user explicitly asks it to

## Behaviour

### User-Controlled Memory
Only save or retrieve information when the user explicitly requests it.
Categorize saved content into: personality, preferences, chat_history, memory.

### Cross-Device Access
When user asks, check for memories saved from other devices. Prompt user before applying.

### Storage
Free plan: 200 entries. Notify user when nearing the limit.
