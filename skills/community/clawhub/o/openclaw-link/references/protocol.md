
## Overview

ClawLink uses a hub-and-spoke topology: a single **relay server** acts as the switchboard, and **agents** (OpenClaw sessions) connect as clients. The relay handles routing, queuing, and state — agents are stateless between polls.

## Transport Layers

ClawLink supports three transports, auto-negotiated by capability:

| Transport | Use Case | Latency | Setup |
|-----------|----------|---------|-------|
| HTTP REST | Universal fallback, works through firewalls | Poll-based (~1-5s) | Zero config |
| WebSocket | Real-time push when both sides support it | Instant (<100ms) | Same server |
| mDNS/Zeroconf | Zero-config LAN discovery of relay servers | N/A (discovery only) | `pip install zeroconf` |

For internet-wide access, expose the relay via **ngrok** (`ngrok http 9077`) or **Cloudflare Tunnel** (`cloudflared tunnel --url localhost:9077`).

## Message Types

### 1. Registration
```json
{
  "agent_id": "a1b2c3d4",
  "name": "researcher",
  "capabilities": ["search", "summarize", "analyze"],
  "machine": "hostname",
  "description": "Finds and summarizes academic papers"
}
```

### 2. Task Delegation
```json
{
  "type": "task_delegation",
  "message_id": "msg-abc123",
  "from_agent": "a1b2c3d4",
  "to_agent": "e5f6g7h8",
  "task": "Find the top 3 papers on neuromorphic computing from 2025",
  "context": {
    "related_to": "SpikeCache project",
    "output_format": "markdown summary"
  },
  "priority": "high"
}
```

### 3. Task Response
```json
{
  "type": "task_response",
  "message_id": "msg-abc123",
  "from_agent": "e5f6g7h8",
  "to_agent": "a1b2c3d4",
  "result": "Found 3 papers: ...",
  "status": "completed"
}
```

### 4. Knowledge Broadcast
```json
{
  "type": "knowledge_broadcast",
  "from_agent": "a1b2c3d4",
  "content": "Key finding: CIM architectures reduce DRAM access by 94% for attention layers",
  "topic": "research",
  "tags": ["CIM", "attention", "memory"]
}
```

### 5. Collaborative File Operations
```json
{
  "file_key": "shared-report.md",
  "content": "# Report\n\n## Findings\n...",
  "file_type": "text",
  "agent_id": "a1b2c3d4"
}
```

## Agent Capabilities Registry

Agents declare capabilities at registration. Common capability tags:

| Capability | Description |
|-----------|-------------|
| `code` | Can write and execute code |
| `search` | Can search the web or databases |
| `summarize` | Can summarize long content |
| `analyze` | Can perform data analysis |
| `write` | Can produce documents and reports |
| `review` | Can review and critique work |
| `debug` | Can diagnose and fix code issues |
| `translate` | Can translate between languages |
| `design` | Can create visual designs |
| `test` | Can write and run tests |

## Workflow Patterns

### Pattern 1: Research Pipeline
```
Agent A (coordinator) → delegates "search papers on X" → Agent B (researcher)
Agent B → broadcasts findings → All agents
Agent A → delegates "write summary from findings" → Agent C (writer)
Agent C → file-put "report.md" → Shared file store
```

### Pattern 2: Distributed Code Review
```
Agent A → file-put "code.py" → Shared file store
Agent A → delegates "review code.py for bugs" → Agent B
Agent A → delegates "review code.py for performance" → Agent C
Agent B → responds with bug report → Agent A
Agent C → responds with perf report → Agent A
Agent A → synthesizes and file-put "review-summary.md"
```

### Pattern 3: Parallel Research
```
Coordinator → delegates "research topic A" → Agent 1
Coordinator → delegates "research topic B" → Agent 2
Coordinator → delegates "research topic C" → Agent 3
[All agents broadcast findings as they discover them]
Coordinator → polls all results → Synthesizes final report
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Agent goes offline | Messages queued for up to 120s, then agent marked stale |
| Relay unreachable | Client retries with exponential backoff |
| WebSocket drops | Falls back to HTTP polling automatically |
| mDNS unavailable | Use explicit relay URL instead |

## Security Notes

- ClawLink is designed for **trusted networks** (home, office, lab)
- No authentication by default — all agents on the network can join
- For production/internet use, put the relay behind a reverse proxy with auth
- Messages are not encrypted in transit — use HTTPS/WSS via reverse proxy if needed
