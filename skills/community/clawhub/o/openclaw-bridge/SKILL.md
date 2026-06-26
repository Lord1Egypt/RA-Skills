---
name: openclaw-bridge
description: >
  Send messages to a local OpenClaw/Rook gateway and receive responses directly
  from Claude Code. Enables bidirectional agent-to-agent communication via the
  `openclaw agent --message` CLI. Use when you need to delegate work to OpenClaw,
  ask for Kimi's opinion, trigger an OpenClaw skill, or hand off context between
  agents. Trigger phrases: "ask openclaw", "tell rook", "delegate to kimi",
  "send to openclaw", "ask the local agent".
allowed-tools: "Bash(openclaw:*)"
version: "1.0.0"
author: "claude-code-agent"
license: "MIT"
compatible-with: claude-code
tags: [agent-communication, openclaw, inter-agent, gateway, local-ai]
---

# openclaw-bridge

Send messages to a running OpenClaw gateway and get responses back — directly from Claude Code, without leaving the terminal.

## When to use

- Delegate a task to OpenClaw that benefits from Kimi's context or local skills
- Ask for a second opinion from a different model/agent
- Hand off work between sessions (Claude Code → OpenClaw or vice versa)
- Trigger OpenClaw skills (e.g. run a cron, call a subagent) from Claude Code
- Notify OpenClaw about changes you made (shared filesystem, config updates)

## Prerequisites

- OpenClaw gateway running locally (`openclaw health` should return `ok`)
- `openclaw` CLI in PATH

## Commands

### ask — send a message and wait for response

```
/ask-openclaw <message>
```

Internally runs:
```bash
openclaw agent --message "<message>" --agent main --json
```

Response is parsed and returned inline.

### notify — fire-and-forget (no wait)

```bash
openclaw agent --message "<message>" --agent main --json --timeout 5
```

Use when you don't need a response — just informing OpenClaw of a state change.

### agents — list available agents

```bash
openclaw agents list
```

### health — check gateway is up

```bash
openclaw health
```

## Usage patterns

### Ask for opinion / second review

```
Ask openclaw: "Review this SQL migration — is it safe to run on a live table with 10M rows?"
```

Claude Code will call `openclaw agent --message "Review this SQL migration..."` and show you Kimi's response.

### Delegate a task

```
Tell openclaw to run the skills-rag-update cron manually
```

```bash
openclaw agent --message "Uruchom ręcznie cron skills-rag-update i podaj wynik" --agent main --json
```

### Handoff with context

When ending a Claude Code session, hand off state to OpenClaw:

```bash
openclaw agent --message "HANDOFF od Claude Code: $(cat /path/to/.continue-here.md)" --agent main --json
```

### Capture idea via OpenClaw

```bash
openclaw agent --message "capture-idea --title 'X' --topic architektura --tags 'a,b' --body 'Y'" --agent main --json
```

## How Claude Code should handle this skill

1. When user says "ask openclaw [something]" or "tell rook [something]":
   - Check gateway: `openclaw health`
   - If down: warn user, suggest `openclaw daemon start`
   - If up: run `openclaw agent --message "<message>" --agent main --json`
   - Parse `.result.payloads[].text` from JSON response
   - Show response inline

2. When delegating a multi-step task:
   - Write context to a temp file or shared vault note first
   - Send message with reference to that file
   - Wait for confirmation

3. When gateway is unreachable:
   - Do NOT retry in a loop
   - Report: "OpenClaw gateway not responding on localhost:18789 — check `openclaw daemon start`"

## Response format

```json
{
  "runId": "...",
  "status": "ok",
  "summary": "completed",
  "result": {
    "payloads": [
      { "text": "agent response here", "mediaUrl": null }
    ],
    "meta": {
      "durationMs": 90617,
      "model": "kimi-k2.5",
      "usage": { ... }
    }
  }
}
```

Extract with:
```bash
openclaw agent --message "..." --agent main --json | python3 -c "
import json, sys
d = json.load(sys.stdin)
for p in d['result']['payloads']:
    if p['text']: print(p['text'])
"
```

## Limitations

- Gateway must be running locally (loopback only by default)
- Auth token is read from `~/.openclaw/openclaw.json` automatically by the CLI
- Large responses may be split across multiple payloads — concatenate them
- No streaming — waits for full response before returning
- Default timeout: 600s (override with `--timeout`)
