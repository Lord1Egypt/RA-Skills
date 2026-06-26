
**Turn isolated AI sessions into a collaborative agent mesh.**

ClawLink lets multiple OpenClaw (or Claude Code) sessions discover each other, delegate tasks, share knowledge, and collaboratively edit files — across different machines on a LAN or across the internet.

## Why ClawLink?

Every OpenClaw session is a powerful AI agent — but they're isolated. ClawLink breaks that barrier:

- 🔍 **Agent Discovery** — See who's online and what they can do
- 📋 **Task Delegation** — Ask another agent to handle a subtask
- 📡 **Knowledge Broadcast** — Share findings with the entire mesh
- 📝 **Collaborative Files** — Co-author documents across agents
- ⚡ **Real-time + Fallback** — WebSocket when possible, HTTP polling always works
- 🌐 **LAN Auto-discovery** — Zero-config via mDNS/Zeroconf
- 🚇 **Internet-ready** — Works through ngrok or Cloudflare Tunnel

## Quick Start

### 1. Install

```bash
# As an OpenClaw skill
# Drop the clawlink/ folder into your skills directory

# Dependencies
pip install aiohttp requests
pip install zeroconf  # optional, for LAN auto-discovery
```

### 2. Start the Relay (one machine)

```bash
python3 scripts/server.py --host 0.0.0.0
```

### 3. Connect Agents (any machine)

```bash
# Machine A
python3 scripts/client.py --relay http://RELAY_IP:9077 \
  register --name "researcher" --caps "search,summarize"

# Machine B
python3 scripts/client.py --relay http://RELAY_IP:9077 \
  register --name "coder" --caps "code,debug,test"
```

### 4. Collaborate

```bash
# See who's online
python3 scripts/client.py discover

# Delegate a task
python3 scripts/client.py delegate --to AGENT_ID --task "Find papers on CIM"

# Share a finding
python3 scripts/client.py broadcast --content "CIM reduces DRAM access by 94%"

# Co-edit a file
python3 scripts/client.py file-put --key "report.md" --file ./report.md
```

## Architecture

```
  Machine A (OpenClaw)       Machine B (OpenClaw)       Machine C (OpenClaw)
       │                           │                           │
       └──── HTTP / WebSocket ─────┼──── HTTP / WebSocket ─────┘
                                   │
                           ┌───────┴───────┐
                           │  ClawLink      │
                           │  Relay Server  │
                           │  (port 9077)   │
                           └────────────────┘
```

## Transport Layers

| Transport | Use Case | Setup |
|-----------|----------|-------|
| **HTTP REST** | Universal, works everywhere | Zero config |
| **WebSocket** | Real-time push (<100ms) | Automatic upgrade |
| **mDNS** | Zero-config LAN discovery | `pip install zeroconf` |
| **Tunnel** | Internet-wide access | `ngrok http 9077` |

## Use Cases

- **Parallel Research** — Multiple agents research different subtopics simultaneously
- **Code Review Pipeline** — One agent writes code, another reviews, a third writes tests
- **Distributed Debugging** — Agents on different machines investigate different parts of a system
- **Document Co-authoring** — Research agent finds sources, writer agent drafts, editor agent polishes
- **Knowledge Mesh** — Agents broadcast discoveries so the whole team stays informed

## License

MIT

---

*Built for the OpenClaw community. Break the isolation barrier.* 🔗
