---
name: lobster-comm
description: >
  Bot-to-Bot P2P communication over Tailscale using the LCP/1.1 UDP protocol.
  Enables AI agents on different machines to exchange signed, reliable messages
  in real-time. Features Ed25519 cryptographic signing, application-layer ACK
  with retransmission, heartbeat keep-alive, duplicate detection, and local
  IPC daemon control. Use when you need inter-agent communication, bot-to-bot
  messaging, cross-machine task delegation, or distributed agent orchestration
  over a Tailscale network.
  Triggers: "bot-to-bot", "inter-agent", "P2P messaging", "lobster-comm",
  "cross-machine communication", "agent delegation", "distributed agents"
---

# Lobster Comm 🦞 — LCP/1.1

Peer-to-peer messaging between AI agents on different machines via UDP over Tailscale.

## Architecture

```
Agent A (Machine 1)                 Agent B (Machine 2)
┌──────────────────┐                ┌──────────────────┐
│  lcp_node.py     │  UDP :9528     │  lcp_node.py     │
│  (daemon)        │ ◄────────────► │  (daemon)        │
│                  │  Ed25519 signed │                  │
│  IPC: Unix sock  │  ACK + Retry   │  IPC: TCP :9529  │
└──────────────────┘                └──────────────────┘
     ▲                                    ▲
     │ Local IPC                          │ Local IPC
  lcp_send / lcp_check / lcp_ack      (same commands)
```

## Features

- **UDP direct**: Low-latency messaging over Tailscale (vs file-based transfers)
- **Ed25519 signing**: Every message cryptographically signed and verified
- **Reliable delivery**: Application-layer ACK + exponential backoff retry (5 attempts)
- **Heartbeat**: 30s keep-alive, 120s peer timeout detection
- **Duplicate detection**: Idempotent message receipt via seen-ID tracking
- **Daemon model**: Background service with local IPC for agent interaction
- **Cross-platform**: macOS (Unix socket IPC) + Windows (TCP localhost IPC)

## Prerequisites

- Python 3.9+
- [PyNaCl](https://pypi.org/project/PyNaCl/) (`pip install pynacl`)
- [Tailscale](https://tailscale.com/) with both machines on the same Tailnet
- UDP port 9528 open between peers

## Quick Start

### 1. Configure peer IPs

Edit `scripts/lcp_node.py` and set:

```python
MY_NAME = "AgentA"        # Your agent name
PEER_NAME = "AgentB"      # Peer agent name
MY_IP = "100.x.x.x"      # Your Tailscale IP
PEER_IP = "100.y.y.y"     # Peer Tailscale IP
```

### 2. Start daemon

```bash
# macOS
python3 scripts/lcp_node.py

# Windows
python scripts/windows/lcp_node_win.py
```

### 3. Send & receive

```bash
# Send a message
python3 scripts/lcp_send.py "Hello from Agent A!"
python3 scripts/lcp_send.py --type task "Please process data X"
python3 scripts/lcp_send.py --type result --reply-to <msg-id> "Done!"

# Check inbox
python3 scripts/lcp_check.py --pretty

# Archive processed messages
python3 scripts/lcp_ack.py

# Check daemon status
python3 scripts/lcp_status.py
```

## Message Protocol

JSON messages with structure:

```json
{
  "id": "uuid",
  "from": "AgentA",
  "to": "AgentB",
  "timestamp": "ISO-8601",
  "type": "chat|task|result|ping|pong",
  "message": "content",
  "replyTo": "optional-msg-id",
  "security": {
    "algo": "ed25519",
    "pubkey": "<base64>",
    "signature": "<base64>"
  }
}
```

## Wire Format (UDP)

```
[Magic 4B: "LCP1"][Seq 4B][Type 1B][JSON payload...]
Type: 0x01=DATA, 0x02=ACK, 0x03=HEARTBEAT
```

## Auto-start (macOS)

Create a LaunchAgent plist pointing to `lcp_node.py` with `RunAtLoad=true` and `KeepAlive` for crash recovery.

## Auto-start (Windows)

Use Task Scheduler or [nssm](https://nssm.cc/) to run `lcp_node_win.py` as a service.

## Data Directories

- `data/inbox/` — incoming messages (pending)
- `data/inbox_archive/` — processed messages
- `data/outbox/` — sent message copies
- `data/seen_ids.json` — duplicate detection state

## Configuration Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| LCP_PORT | 9528 | UDP port for peer communication |
| IPC_SOCKET | /tmp/lcp.sock | Unix socket for local IPC (macOS) |
| IPC_PORT | 9529 | TCP port for local IPC (Windows) |
| MAX_RETRIES | 5 | ACK retry attempts |
| HEARTBEAT_INTERVAL_S | 30 | Seconds between heartbeats |
| PEER_TIMEOUT_S | 120 | Seconds before marking peer offline |

## Extending

For multi-peer support, run multiple daemon instances on different ports or extend `lcp_node.py` with a peer registry. See `references/protocol-spec.md` for the full LCP/1.1 specification.
