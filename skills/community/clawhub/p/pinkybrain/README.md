# PinkyBrain — P2P Distributed AI Network

> **Turn your OpenClaw agent into a PinkyBrain node.** Share compute, query AI specialists, sync memory across peers — with Ed25519 identity, E2E encryption, and Web of Trust.

[![Version](https://img.shields.io/badge/version-5.2.0-blue)](https://github.com/PinkyBrain-ai/pinkybrain)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/PinkyBrain-ai/pinkybrain)
[![ClawHub](https://img.shields.io/badge/ClawHub-skill-orange)](https://clawhub.ai/PinkyBrain-ai/pinkybrain)

---

## What is PinkyBrain?

PinkyBrain is a platform for AI development in **every domain** — health, education, science, art, music, agriculture, law, and more. Your OpenClaw agent becomes a first-class PinkyBrain node.

---

## Features

- 🕸️ **P2P Networking** — WebSocket sync, gossip protocol, auto-discovery (mDNS, Tailscale)
- 🧠 **CRDT Memory** — Distributed key-value store, eventually consistent across peers
- 🎯 **Specialist Router** — 12 profiles, 6 multi-LLM modes (single, vote, chain, fuse, compare, specialist)
- 📦 **Model Registry** — Catalog, hash verification, Ed25519 signatures
- 💰 **Credit System** — Earn by sharing compute, spend by querying
- 🛡️ **Ed25519 + Web of Trust** — Decentralized authentication
- 🔒 **E2E Encryption** — Queries encrypted end-to-end through distributed inference
- 🚦 **Resource Guard** — Auto-pauses sharing when CPU/RAM thresholds exceeded
- 👻 **Stealth Mode** — Share compute but stay hidden on tracker
- 💬 **Conversation Store** — Persistent history, search, export, privacy levels
- 🔄 **Auto-Update** — Check and apply updates from the network
- 🚫 **Zero Logging** — No data logging on public mesh
- 🌍 **World Models (coming soon)** — DreamX-World integration for interactive world generation on GPU nodes

---

## Security Model

| Principle | Implementation |
|-----------|---------------|
| Cloud models stay private | OpenAI/Anthropic models **never** shared on mesh |
| Strong authentication | Ed25519 identity + HMAC on every API call |
| Web of Trust | Decentralized peer verification for public mesh |
| E2E encryption | All distributed inference queries encrypted |
| Sharing isolation | Only `shared_models/` visible to mesh — nothing else |
| Resource Guard | Auto-pause sharing under high load |
| Zero logging | No query/data logging on public mesh |
| Network isolation | No leakage between private and public networks |

---

## Installation

```bash
# Clone and setup
git clone https://github.com/PinkyBrain-ai/pinkybrain.git ~/pinkybrain
cd ~/pinkybrain
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate identity
python -m pinkybrain.v5 identity init

# Configure
python -m pinkybrain.v5 config init

# Start
python -m pinkybrain.v5 serve --daemon
```

---

## Quick Usage

```bash
# Query the mesh
pinkybrain query "Explain quantum computing" --mode single
pinkybrain query "Debug this code" --mode chain --specialist coder

# Share a model (must be in shared_models/)
pinkybrain models share llama3

# Read/write distributed memory
pinkybrain memory get shared_key
pinkybrain memory set shared_key "hello mesh"

# Join the public mesh
pinkybrain mesh join

# Check status
pinkybrain status
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Node status |
| GET | `/api/ping` | Health check |
| POST | `/api/query` | AI query |
| GET | `/api/peers` | Connected peers |
| GET | `/api/memory/{key}` | Read CRDT memory |
| POST | `/api/memory/set` | Write CRDT memory |
| GET | `/api/capabilities` | Hardware report |
| GET | `/api/score/{peer}` | Peer credit score |
| GET | `/api/discover` | Auto-discovered peers |
| GET | `/api/update` | Check for updates |
| GET | `/api/daemon` | Daemon status |
| POST | `/api/models/{name}/share` | Share model |
| POST | `/api/models/{name}/unshare` | Unshare model |
| GET | `/api/models` | List models |
| POST | `/api/network/mesh/join` | Join public mesh |
| POST | `/api/network/mesh/leave` | Leave public mesh |

---

## Auto-Discovery

The skill automatically finds your PinkyBrain node by checking:

1. `PINKYBRAIN_URL` environment variable
2. `http://localhost:8080/api/ping` (default)
3. `http://localhost:8081/api/ping` (alternate)
4. Tailscale peers
5. mDNS (`_pinkybrain._tcp.local.`)

---

## Links

- **Repository:** [github.com/PinkyBrain-ai/pinkybrain](https://github.com/PinkyBrain-ai/pinkybrain)
- **Website:** [pinkybrain-ai.github.io](https://PinkyBrain-ai.github.io/pinkybrain/)
- **ClawHub Skill:** [clawhub.ai/PinkyBrain-ai/pinkybrain](https://clawhub.ai/PinkyBrain-ai/pinkybrain)

---

*PinkyBrain v5.2.0 — Welcome to the mesh. 🕸️*