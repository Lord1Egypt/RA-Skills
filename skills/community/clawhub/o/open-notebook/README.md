# open-notebook-skill

**Open Notebook skill for OpenClaw**  -  bridge client for [lfnovo/open-notebook](https://github.com/lfnovo/open-notebook). Create themed notebooks, add sources, cross-notebook search, and RAG-chat with your research notes.

## What this is

This is a **bridge client skill** for OpenClaw agents. It wraps the open-notebook API through a local FastAPI bridge that adds per-agent authentication, per-notebook allowlists, and audit logging.

Without a running open-notebook deployment + bridge, this skill does nothing.

## Features

- **Create notebooks** by topic (research, health, travel, etc.)
- **Add sources** as text, URLs, or files
- **Cross-notebook vector search**  -  find anything you've saved
- **RAG chat**  -  ask questions about your research and get cited answers
- **Python fallback**  -  works even without `jq` installed

## Requirements

- OpenClaw agent with this skill installed
- A running [open-notebook](https://github.com/lfnovo/open-notebook) deployment (v1.9.0+)
- The open-notebook bridge service running on `127.0.0.1:5077`
- `curl` and optionally `jq` (python3 fallback included)

## Setup

### 1. Deploy open-notebook

Follow the [lfnovo/open-notebook deployment guide](https://github.com/lfnovo/open-notebook). You need:
- open-notebook running (Docker recommended)
- SurrealDB for storage
- An embedding model configured (e.g. `perplexity/pplx-embed-v1-4b` on OpenRouter)

### 2. Set up the bridge

The bridge is a small FastAPI app. Create `bridge/main.py`, `bridge/agents.json`, and a `bridge.env`:

```bash
# Create bridge directory
mkdir -p ~/open-notebook/bridge
cd ~/open-notebook/bridge

# Create agents.json  -  add your OpenClaw agent key
echo '{"<your-openclaw-agent-key>":{"name":"onyx","allowed_notebooks":"*","readwrite":true}}' > agents.json
chmod 600 agents.json

# Create bridge.env
echo 'OPEN_NOTEBOOK_PASSWORD=<your-open-notebook-password>' > bridge.env
echo 'AGENTS_FILE=~/open-notebook/bridge/agents.json' >> bridge.env
echo 'AUDIT_LOG=~/open-notebook/bridge/audit.log' >> bridge.env
echo 'BRIDGE_PORT=5077' >> bridge.env
chmod 600 bridge.env
```

### 3. Install the bridge service

```ini
# ~/.config/systemd/user/open-notebook-bridge.service
[Unit]
Description=Open Notebook Agent Bridge
After=docker.service
Wants=docker.service

[Service]
Type=simple
EnvironmentFile=%h/open-notebook/bridge/bridge.env
ExecStart=/usr/bin/env python3 %h/open-notebook/bridge/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now open-notebook-bridge
```

### 4. Get your agent key

```bash
openssl rand -base64 32 | tr -d '/+=' | head -c 40
```

Add the generated key to `agents.json` as shown above.

### 5. Configure OpenClaw

Add to `~/.openclaw/.env`:
```
OPEN_NOTEBOOK_BRIDGE_URL=http://127.0.0.1:5077
OPEN_NOTEBOOK_API_KEY=<your-agent-key>
```

Restart the gateway:
```bash
systemctl --user restart openclaw-gateway
```

### 6. Install this skill

```bash
clawhub install crabsticksalad/open-notebook
```

## Usage

The agent uses this skill only when you **explicitly** ask it to save, search, or retrieve stored content. Examples:

- "Save this to my notebook: ..."
- "What did I save about mushrooms?"
- "Search my notes about X"
- "Create a new notebook for my travel plans"
- "Ask my notes about the toxicity of Amanita muscaria"

## Commands

| Command | Description |
|---|---|
| `on.sh health` | Bridge + upstream liveness |
| `on.sh list-notebooks` | List notebooks this agent is allowed to access |
| `on.sh get-notebook <id>` | Notebook details |
| `on.sh create-notebook "Title" "Description"` | Create notebook |
| `on.sh add-source <nb-id> --text "..."` | Add text source |
| `on.sh add-source <nb-id> --url "..."` | Add URL source |
| `on.sh get-source <id>` | Check source status |
| `on.sh search "query"` | Cross-notebook search |
| `on.sh ask <nb-id> "question"` | RAG chat |
| `on.sh delete-source <id>` | ⚠️ Remove source (irreversible) |
| `on.sh delete-notebook <id>` | ⚠️ Remove notebook (irreversible) |

## Privacy

Notebooks are stored **unencrypted at rest** in SurrealDB. Do not put secrets, credentials, or sensitive PII into notebooks.

## Troubleshooting

### "bridge unreachable"
Bridge service is down. Restart it:
```bash
systemctl --user restart open-notebook-bridge
```

### HTTP 401 missing X-API-Key
The `OPEN_NOTEBOOK_API_KEY` env var is not set. Verify it's in `~/.openclaw/.env` and restart the gateway.

### HTTP 403 agent not allowed
The agent's key in `agents.json` doesn't have access to that notebook. Check `allowed_notebooks` in `agents.json`.

### Source not found in search
Embedding is async  -  the source may not be indexed yet. Poll `get-source <id>` until `status: completed`.

## License

MIT-0
