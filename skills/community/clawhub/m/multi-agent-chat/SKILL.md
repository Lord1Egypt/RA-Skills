---
name: multi-agent-chat
description: Prevent common failures in multi-agent Discord conversations. Use when multiple AI agents (bots) are chatting in the same channel — townhalls, group discussions, collaborative sessions. Prevents context window overflow, token waste, duplicate responses, reaction spam, rate limit collisions, and infinite loops. Triggers on bot-to-bot chat, townhall, multi-agent meeting, group agent discussion.
---

# Multi-Agent Chat Protocol

Rules for AI agents participating in multi-bot Discord conversations. Follow strictly to prevent token waste, context overflow, and communication failures.

## Core Rules

### 1. Turn-Based Communication
- **One agent answers at a time** — wait for your turn
- **Mention one agent per message** when directing questions
- **Never answer a question directed at another agent**

### 2. One Response Per Topic
- **One answer per agenda item** — never repeat yourself
- If someone missed your answer: reply "위에 있어" (one line only)
- **Never re-explain** what you already said

### 3. No Bot-to-Bot Reactions
- **Never add emoji reactions to bot messages** — each reaction event consumes hundreds of tokens
- Reactions are for humans only
- Set `reactionNotifications: "off"` in config to stop receiving reaction events

### 4. Short Responses
- Keep answers under 200 words unless explicitly asked for detail
- No filler ("네 알겠습니다!", "감사합니다!" alone) — use NO_REPLY instead
- If you have nothing to add: NO_REPLY

### 5. Follow the Agenda
- When a new topic is announced, stop discussing the previous one
- Don't circle back to resolved topics
- If asked a question, answer that specific question — not a previous one

### 6. Loop Prevention
- **Max 4 consecutive bot-to-bot exchanges** before requiring human input
- If the same question is asked 3+ times, stop and flag to the human operator
- Never create ping-pong chains between bots

## Config Optimization

Each bot should set in `config.yml`:

```yaml
channels:
  discord:
    reactionNotifications: "off"
```

## Token Budget Guidelines

- Multi-agent channels: use Sonnet or cheaper models (not Opus)
- Separate API keys per bot to avoid shared rate limits
- Estimate: 3+ bots on Opus = ~1000 KRW per round of conversation

## Red Flags (Stop & Alert Human)

- Same question repeated 3+ times → context window issue, alert operator
- Rate limit errors appearing → need API key separation
- Bot responding to wrong agenda item → confusion, pause and clarify
- Token usage spiking → check for reaction events or verbose responses

## Lessons Learned

These rules come from a real 2026-03-07 townhall incident:
- 3 bots simultaneously responding caused context overflow
- Lead agent repeated same question 6+ times (couldn't see answers in context)
- Emoji reactions (👀🤔👨‍💻👍 cycles) consumed massive tokens silently
- Shared API key caused rate limits for all bots simultaneously
- Cost: ~1000 KRW per exchange on Opus model
