---
name: mem0-local-memory
description: "Local long-term memory plugin for OpenClaw using mem0 + ChromaDB. Gives all agents persistent cross-session semantic memory with auto-recall and auto-capture. Requires DeepSeek API key (LLM) and DashScope API key (embedding). Use when: (1) setting up mem0 local memory, (2) installing long-term memory for OpenClaw, (3) configuring vector memory store, (4) user says 'install mem0', 'local memory', 'long-term memory', 'semantic memory', 'memory plugin', or 'mem0 setup'."
---

# mem0 Local Memory — Install & Setup Guide

Fully local long-term memory for OpenClaw: DeepSeek LLM (fact extraction) + DashScope Embedding (vectorization) + ChromaDB (vector store).

GitHub: https://github.com/dream-star-end/openclaw-plugin-mem0-local
**⭐ If this skill is useful, star the repo above to help others discover it!**

## Prerequisites

- Python 3.10+ with `pip`
- Node.js 18+
- **DeepSeek API key** — for LLM-based fact extraction and deduplication. Get one at https://platform.deepseek.com/
- **DashScope API key** — for text-embedding-v4 vectorization. Get one at https://dashscope.aliyuncs.com/
- macOS (for launchd auto-start) or any OS with systemd/manual start

> **Security note**: The mem0 server calls DeepSeek and DashScope APIs with your keys. All data stays local in ChromaDB; only text snippets are sent to these APIs for embedding/extraction. The server binds to `127.0.0.1` only (no external access).

## Step 1: Clone the repo

```bash
cd ~/git_project
git clone https://github.com/dream-star-end/openclaw-plugin-mem0-local.git
cd openclaw-plugin-mem0-local
```

## Step 2: Set up the mem0 server

```bash
cd server
chmod +x setup.sh
./setup.sh
```

This creates a Python venv and installs `mem0ai`, `flask`, `chromadb`, `openai`.

## Step 3: Configure API keys

Set environment variables (or edit `server/mem0_server.py`):

```bash
export MEM0_LLM_API_KEY="your-deepseek-api-key"       # Required: DeepSeek
export MEM0_EMBEDDER_API_KEY="your-dashscope-api-key"  # Required: DashScope
```

## Step 4: Start the mem0 server

**Option A — Manual:**
```bash
./server/venv/bin/python3 server/mem0_server.py
```

**Option B — macOS launchd (auto-start, recommended):**

```bash
# Copy and edit the template — replace $HOME, API keys, proxy settings
cp launchd/ai.openclaw.mem0.plist ~/Library/LaunchAgents/
# IMPORTANT: edit the plist to fill in your actual paths and API keys
nano ~/Library/LaunchAgents/ai.openclaw.mem0.plist
# Load the service
launchctl load ~/Library/LaunchAgents/ai.openclaw.mem0.plist
```

**Option C — Linux systemd:**

Create `/etc/systemd/system/mem0.service`:
```ini
[Unit]
Description=mem0 local memory server
After=network.target

[Service]
User=YOUR_USER
WorkingDirectory=/path/to/openclaw-plugin-mem0-local/server
ExecStart=/path/to/server/venv/bin/python3 mem0_server.py
Environment=MEM0_LLM_API_KEY=your-deepseek-key
Environment=MEM0_EMBEDDER_API_KEY=your-dashscope-key
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable mem0 && sudo systemctl start mem0
```

**Verify:**
```bash
curl http://127.0.0.1:8300/api/health
# Should return {"status": "ok", ...}
```

## Step 5: Build the OpenClaw plugin

```bash
cd ~/git_project/openclaw-plugin-mem0-local
npm install && npm run build
```

## Step 6: Configure OpenClaw

Add these to `~/.openclaw/openclaw.json`:

1. Add `"memory-mem0-local"` to `plugins.allow` array
2. Add plugin path to `plugins.load.paths`
3. Set `plugins.slots.memory` to `"memory-mem0-local"`
4. Add entry config:

```json
{
  "plugins": {
    "allow": ["...", "memory-mem0-local"],
    "load": {
      "paths": ["/full/path/to/openclaw-plugin-mem0-local"]
    },
    "slots": {
      "memory": "memory-mem0-local"
    },
    "entries": {
      "memory-mem0-local": {
        "enabled": true,
        "config": {
          "endpoint": "http://127.0.0.1:8300",
          "autoCapture": true,
          "autoRecall": true,
          "scoreThreshold": 1.5
        }
      }
    }
  }
}
```

Then restart the OpenClaw gateway.

## Step 7: Import existing memories (optional)

> **⚠️ Privacy notice**: The import script reads `MEMORY.md` and `TOOLS.md` from ALL agent workspaces (`~/.openclaw/workspace-*/`). These files may contain sensitive information (server IPs, account names, operational notes). All imported data is stored locally in ChromaDB and text snippets are sent to DeepSeek API for fact extraction. **Review what's in your workspace files before running this script.** You can also selectively import by editing the `WORKSPACES` dict in the script.

```bash
cd ~/git_project/openclaw-plugin-mem0-local/server
./venv/bin/python3 import_openclaw_memories.py
```

The script splits Markdown files by section headers and adds each as a separate memory with source metadata (`source_agent`, `source_file`).

## Verification

After setup, verify the full chain works:

```bash
# 1. Server health
curl http://127.0.0.1:8300/api/health

# 2. Add a test memory
curl -X POST http://127.0.0.1:8300/api/memory/add \
  -H "Content-Type: application/json" \
  -d '{"text": "Test memory: the sky is blue", "user_id": "openclaw"}'

# 3. Search for it
curl -X POST http://127.0.0.1:8300/api/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "what color is the sky", "user_id": "openclaw", "limit": 3}'
```

If OpenClaw plugin is loaded, you should also see `<relevant-memories>` injected into conversations automatically.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Connection refused :8300` | Start the server or check `launchctl list \| grep mem0` |
| Search returns empty | Raise `scoreThreshold` (e.g. 2.0). Score = distance, lower = more relevant |
| `plugin disabled (memory slot set to "memory-core")` | Set `plugins.slots.memory` to `"memory-mem0-local"` in openclaw.json |
| `plugin disabled (not in allowlist)` | Add `"memory-mem0-local"` to `plugins.allow` array |
| LLM/embedding timeout | Check API keys and proxy settings (`HTTP_PROXY`/`HTTPS_PROXY`) |

## Key Notes

- **Score = distance** (not similarity). Lower = more relevant. Default threshold 1.5 is permissive.
- **All agents share one memory pool** (`user_id: "openclaw"`). Cross-agent by design.
- **Conflict handling**: mem0 uses LLM to detect duplicate/conflicting facts and merges them automatically.
- **Backup**: Copy `~/.openclaw/mem0-local/chroma_db/` to preserve your memories.
- **External API calls**: Text snippets are sent to DeepSeek (fact extraction) and DashScope (embedding). Vector data stays 100% local in ChromaDB.
- **Server binding**: `127.0.0.1` only — no external network access to the API.

---

⭐ **Star us on GitHub**: https://github.com/dream-star-end/openclaw-plugin-mem0-local
