---
name: clawlink
description: >
  Cross-instance agent communication for OpenClaw. ClawLink lets multiple OpenClaw
  sessions discover each other, delegate tasks, share knowledge, collaboratively
  edit files, and work as a coordinated agent mesh — across different machines on
  a local network. Use this skill whenever the user mentions connecting OpenClaw
  instances, multi-agent workflows, agent-to-agent communication, delegating tasks
  between sessions, collaborative AI work, agent discovery, or running agents on
  multiple machines. Also trigger when the user says things like "ask my other
  agent to...", "have another Claude work on...", "set up agent communication",
  "multi-machine", "agent mesh", "distributed agents", or "ClawLink". If the user
  wants two or more AI sessions to work together in any way, this is the skill to use.
version: 1.0.2
metadata:
  openclaw:
    emoji: "🔗"
---

# ClawLink — Cross-Instance Agent Communication

ClawLink turns isolated OpenClaw sessions into a collaborative agent mesh. Multiple OpenClaw instances — on the same machine or across a network — can delegate tasks, share findings, co-edit files, and coordinate work.

> **Security note:** The relay server only runs when you explicitly start it with `python3 server.py`. It stores no data on disk — everything is in-memory and clears on shutdown. When connecting across machines, use `--token` to require authentication.

## Architecture

```
  Machine A (OpenClaw)          Machine B (OpenClaw)
       │                              │
       └──── HTTP/WebSocket ──────────┘
                    │
            ┌───────┴───────┐
            │  ClawLink      │
            │  Relay Server  │
            │  (localhost or │
            │   LAN machine) │
            └────────────────┘
```

One machine runs the relay server. All others connect as agent clients. The relay handles message routing, queuing, and agent registry — entirely in-memory.

## Quick Start

### Step 1: Start the Relay Server

On the machine that will act as the hub (can be one of the agent machines):

```bash
# Install dependencies (user install — no system changes)
pip install --user aiohttp requests

# Start the relay — localhost only (safest for single-machine use)
python3 scripts/server.py

# Or bind to LAN with auth token for multi-machine use
python3 scripts/server.py --host 0.0.0.0 --token YOUR_SHARED_SECRET
```

The server defaults to `127.0.0.1` (localhost only). To allow other machines on your local network, add `--host 0.0.0.0 --token YOUR_SECRET`.

**For access from another machine on your network:**

Use the relay machine's local IP address directly — e.g., `http://192.168.1.10:9077`. Both machines must be on the same network and you must pass the same `--token` on both server and clients.

### Step 2: Register This Agent

```bash
python3 /path/to/clawlink/scripts/client.py \
  --relay http://RELAY_IP:9077 \
  --token YOUR_SHARED_SECRET \
  register \
  --name "DESCRIPTIVE_NAME" \
  --caps "COMMA_SEPARATED_CAPABILITIES" \
  --description "What this agent specializes in"
```

The token can also be set via `CLAWLINK_TOKEN` environment variable.

### Step 3: Discover and Communicate

```bash
python3 scripts/client.py --relay http://RELAY_IP:9077 --token SECRET discover
```

## Core Operations

### Discovering Peers

```bash
python3 scripts/client.py discover
```

Returns a table of online agents with their IDs, names, capabilities, and machines.

### Delegating Tasks

```bash
python3 scripts/client.py delegate \
  --to TARGET_AGENT_ID \
  --task "Clear description of what needs to be done" \
  --context '{"key": "relevant context data"}' \
  --priority normal
```

### Receiving and Responding to Tasks

```bash
# Poll for incoming messages
python3 scripts/client.py poll

# Respond when done
python3 scripts/client.py respond \
  --to REQUESTING_AGENT_ID \
  --msg-id ORIGINAL_MESSAGE_ID \
  --result "Task result or summary of work done"
```

### Broadcasting Knowledge

```bash
python3 scripts/client.py broadcast \
  --content "Description of the finding" \
  --topic "category" \
  --tags "tag1,tag2"
```

### Collaborative File Editing

```bash
# Upload/update a shared file
python3 scripts/client.py file-put --key "report.md" --file ./report.md

# Download a shared file
python3 scripts/client.py file-get --key "report.md" --output ./report.md

# List shared files
python3 scripts/client.py file-list
```

## Behavioral Guidelines for Agents

### As a Task Receiver
1. **Poll regularly** — Check for messages every 30-60 seconds during active work, or when the user asks "any messages?" or "check ClawLink"
2. **Acknowledge receipt** — Respond with status "in_progress" when you get a task
3. **Be thorough** — Complete the full task before responding
4. **Report failures** — If you can't complete a task, respond with status "failed" and explain why

### As a Task Delegator
1. **Match capabilities** — Use `discover` to find the right agent for the job
2. **Provide context** — Include file paths, URLs, constraints, and output format
3. **Be patient** — The other agent may take time

### General
- Always tell the user what's happening on the network
- Surface incoming messages proactively
- Keep heartbeats alive during long sessions

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Check relay is running and IP/port are correct |
| "Unauthorized" | Pass the same --token (or CLAWLINK_TOKEN) as the server |
| Can't find relay on LAN | Use explicit `--relay http://IP:PORT` |
| Messages not arriving | Run heartbeat to re-register; check agent_id matches |
| Agent shows "stale" | Agent hasn't heartbeated in 120s — restart or heartbeat |

## Protocol Reference

For the full message format specification, transport layer details, and workflow patterns, read `references/protocol.md`.
