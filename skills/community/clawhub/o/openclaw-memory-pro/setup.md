# Setup Guide — OpenClaw Memory Pro System

## 1. Clone the Repository

```bash
cd ~/.openclaw/workspace
git clone https://github.com/FluffyAIcode/openclaw-memory-pro-system.git memory-pro
cd memory-pro
```

Or if the code is already in your workspace, skip this step.

## 2. Install Python Dependencies

```bash
pip install -e .                     # basic install
pip install -e ".[embeddings]"       # recommended: real embedding model
```

Requirements: Python 3.9+, macOS (Apple Silicon) or Linux.

## 3. Configure LLM API Key

The system auto-detects API keys in this order:

1. `OPENROUTER_API_KEY` env var
2. OpenClaw `auth-profiles.json` (openrouter:default)
3. `XAI_API_KEY` env var
4. OpenClaw `auth-profiles.json` (xai:default)

Set one:

```bash
export OPENROUTER_API_KEY=sk-or-v1-...    # preferred
# or
export XAI_API_KEY=xai-...                # fallback
```

The system works without an LLM key — advanced features (collision, distillation, MSA multi-hop) gracefully degrade to local heuristics.

## 4. Start the Memory Server

```bash
memory-cli server-start    # start in background
memory-cli health          # confirm ready (first run ~3 min to load embedding model)
```

## 5. Verify

```bash
memory-cli remember "Testing the memory system" --tag thought
memory-cli recall "memory system"
memory-cli status
```

## 6. (Optional) Enable Scheduled Tasks

The memory server includes a built-in scheduler for:
- Daily briefing generation
- Periodic collision rounds (every 6 hours)
- Dormancy checks
- Digest distillation (weekly)

These run automatically when the server is running.

## 7. (Optional) Telegram Push

Configure in `openclaw.json` under `channels.telegram` to receive briefings and collision insights via Telegram.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `memory-cli health` fails | Check if server is running: `memory-cli server-start` |
| Embedding model slow to load | First run downloads ~500MB model. Subsequent starts are fast. |
| LLM features not working | Verify API key: `python3 -c "import llm_client; print(llm_client.get_provider_info())"` |
| Port 18790 in use | Kill existing process: `lsof -ti :18790 \| xargs kill -9` |
