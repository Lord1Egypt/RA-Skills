---
name: minimax-team-rules
description: Shared MiniMax / MMX CLI operating rules for XiaoMei, DaLong, YuanQi, and the main coordinator. Trigger this skill whenever the task involves MiniMax, minimax, mmx, mmx-cli, Token Plan, quota, quota interpretation, speech-hd, music-2.6, music-cover, lyrics_generation, image-01, coding-plan-vlm, coding-plan-search, MiniMax capability mapping, OpenClaw↔MiniMax tool mapping, or agent-specific delivery/routing rules. Also trigger when the user asks to standardize, document, roll out, align, fix once-for-all, or sync configuration /规范 /工作流 /多 agent rules across multiple agents or files.
---
tags:
  - minimax
  - team
  - multi-agent
compatibility: openclaw
license: MIT


# MiniMax Team Rules

Use this skill whenever the work touches any of these topics:
- MiniMax capability selection or mapping
- `mmx` / `mmx-cli` install, auth, status, quota, or diagnostics
- Token Plan model availability or remaining quota
- OpenClaw tool ↔ MiniMax native CLI mapping
- quota interpretation / model usage explanation
- multi-agent routing, producer-direct delivery, or “谁来发给阿辉”
- configuration / standards / multi-agent workflow changes that should land consistently across multiple layers

## Core Rule
For **configuration / standards / multi-agent workflow** changes, do **one-pass rollout** by default:
1. verify the fact,
2. update the shared source of truth,
3. update affected local guidance or references,
4. record the learning if a misunderstanding or correction occurred.

Do not stop at a partial fix when the issue clearly affects multiple layers.
Do not make the user push for each missing layer one by one.

## Required Execution Pattern
When this skill triggers, default to this checklist:
1. Identify all affected layers (shared docs, local agent guidance, memory, learnings).
2. Update the **shared source of truth first**.
3. Convert repeated local rule blocks into **references to the shared source**, keeping only role-specific additions locally.
4. Keep all four roles aligned: 小美 / 大龙 / 元气 / 小语.
5. When explaining quota, use the documented house interpretation from the reference file. Do not guess from field names alone.
6. When finalizing, give the user the outcome, not internal rollout noise.

## Shared Source of Truth
Read this reference when you need the concrete rules:
- `references/agent-rules.md`

## Operating Defaults
- Prefer OpenClaw first-class tools for normal user work.
- Use `mmx` when you need MiniMax-native verification, auth/quota diagnostics, or a capability not directly exposed the way you need.
- Producer-direct delivery is mandatory unless 阿辉 explicitly asks for unified forwarding.
- For team-wide rule changes, prefer updating the shared skill/reference over copying edits into multiple places.

## Agent Routing Reminder
- 小美 → news / information
- 大龙 → ops / diagnosis / system checks
- 元气 → creative / image / music / prompt output
- 小语 → coordination / review / routing / fallback only

If updating standards, keep all four aligned.
