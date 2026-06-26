
---
name: openclaw-dual-agent
description: "Run two OpenClaw agents simultaneously — a paid Anthropic agent and a free agent using either OpenRouter (cloud) or local Ollama models. Note: Ollama example defaults to hybrid setup with OpenRouter fallback — remove fallback/heartbeat refs for fully offline operation. Trigger phrases: multi-agent setup, add a second agent, free agent openclaw, run two agents, openrouter openclaw, ollama agent, local model openclaw, parallel agents, cost optimization agent."
metadata: {"clawdbot": {"emoji": "🤖", "requires": {"bins": ["jq"]}, "env": ["ANTHROPIC_API_KEY"], "os": ["darwin", "linux", "win32"]}, "homepage": "https://clawhub.com/djc00p/openclaw-dual-agent"}
---

# Multi-Agent OpenClaw Setup

Run a paid Anthropic agent and free OpenRouter agent side by side with separate Telegram bots.

## Quick Start

1. **Create two Telegram bots** via @BotFather and extract chat IDs:
   ```bash
   curl https://api.telegram.org/bot{TOKEN}/getUpdates | jq '.result[0].message.chat.id'
   ```

2. **Authenticate agents:**
   ```bash
   # Run interactively — avoids exposing keys in shell history
   openclaw onboard
   ```
   > ⚠️ Never pass API keys directly on the CLI (e.g. `--anthropic-api-key ...`) — it exposes them in shell history. Always use `openclaw onboard` interactively. Credential files (`auth-profiles.json`, `openclaw.json`) should be `chmod 600`.

3. **Configure** `openclaw.json` with two agents, separate bindings, and Telegram accounts.

4. **Verify setup:**
   ```bash
   openclaw doctor
   openclaw sessions cleanup \
     --store /Users/YOUR_USERNAME/.openclaw/agents/main/store \
     --enforce --fix-missing
   openclaw restart
   ```

## Key Concepts

- **Agent isolation:** Each agent has its own `agentDir`, workspace, and model config.
- **Binding routing:** `accountId` in bindings directs Telegram messages to the correct agent.
- **Model refs:** Use `provider/modelid` format (e.g., `anthropic/claude-sonnet-4-6`).
- **Per-agent auth:** OpenRouter requires `auth-profiles.json` in each agent's directory.

## Common Usage

**Adding a free agent:**
- Create agentDir at `/Users/YOUR_USERNAME/.openclaw/agents/free-agent/agent`
- Add agent entry to `openclaw.json` with `model.primary: "openrouter/..."`
- Create `auth-profiles.json` with OpenRouter API key in agent's directory
- Add binding with unique `accountId` (e.g., `"tg2"`)
- Restart: `openclaw restart`

**Switching models:**
Edit `openclaw.json` agent's `model.primary` and `fallbacks` with valid provider/id strings.

**Masking secrets for logs:**
```bash
cat ~/.openclaw/openclaw.json | \
  jq '.channels.telegram.accounts |= map_values(.botToken = "[REDACTED]")'
```

## Option B: Local Ollama Agent (Free + Hybrid)

Instead of OpenRouter, run your second agent on a local Ollama model — free, private, and locally-hosted. The default config uses a hybrid approach with OpenRouter cloud fallback for reliability. For fully offline operation, see "Fully Offline Config" below.

### Install & Configure Ollama

**macOS:**
```bash
# Install via Homebrew
brew install ollama

# Or download from https://ollama.ai
```

**Start Ollama:**
```bash
# In a dedicated terminal, keep it running
ollama serve
```

**Pull a model** (choose one based on your needs):
```bash
# Google Gemma 4 26B — good balance of capability and speed (17GB)
ollama pull gemma4:26b

# Meta Llama 3.3 70B — very capable, excellent reasoning (43GB)
ollama pull llama3.3:70b

# Qwen 2.5 32B — strong coding and multilingual (20GB)
ollama pull qwen2.5:32b

# Mistral 7B — fast and lightweight, good for quick responses (4GB)
ollama pull mistral:7b
```

### Configure OpenClaw with Ollama Agent

Add the agent entry to `openclaw.json` (e.g., `id: "ayo"`):

```json
{
  "id": "ayo",
  "name": "Ayo",
  "workspace": "/Users/YOUR_USERNAME/.openclaw/workspace-ayo",
  "agentDir": "/Users/YOUR_USERNAME/.openclaw/agents/ayo/agent",
  "model": {
    "primary": "ollama/gemma4:26b",
    "fallbacks": [
      "openrouter/free"
    ]
  },
  "heartbeat": {
    "every": "1h",
    "model": "openrouter/free"
  }
}
```

**Key points:**

- **Model format:** Always use `ollama/modelname:tag` (e.g., `ollama/gemma4:26b`, `ollama/llama3.3:70b`)
- **No API key needed for Ollama:** Ollama runs entirely locally. No `auth-profiles.json` required.
- **Ollama must be running:** Start `ollama serve` in a terminal before the gateway starts
- **Pull first:** Run `ollama pull modelname:tag` before configuring (the model must exist locally)
- **⚠️ Hybrid setup:** The default example uses `openrouter/free` for fallback and heartbeat — this means prompts and context MAY route to OpenRouter cloud. See below for fully offline config.
- **Add Telegram binding:** Include a separate binding with a unique `accountId` (e.g., `"tg_ollama"`) to route messages to Ayo

### Fully Offline Config (No Cloud Routing)

If you want a truly local, offline-only Ollama agent with no external provider calls:

```json
{
  "id": "ayo",
  "name": "Ayo",
  "workspace": "/Users/YOUR_USERNAME/.openclaw/workspace-ayo",
  "agentDir": "/Users/YOUR_USERNAME/.openclaw/agents/ayo/agent",
  "model": {
    "primary": "ollama/gemma4:26b",
    "fallbacks": []
  },
  "heartbeat": {
    "every": "1h",
    "model": "ollama/gemma4:26b"
  }
}
```

This config uses ONLY local Ollama models — no cloud provider traffic for primary, fallback, or heartbeat.

**After config change:**
```bash
# Verify no errors
openclaw doctor

# Restart the gateway
openclaw gateway restart
```

### Common Gotchas

| ❌ Wrong | ✅ Correct | Issue |
|---------|----------|-------|
| `gemma4:26b:local` | `ollama/gemma4:26b` | Invalid format; always use `provider/model:tag` |
| `gemma4:26b` | `ollama/gemma4:26b` | Without prefix, OpenClaw won't route to Ollama |
| `ollama/kimi-k2.5:cloud` | `openrouter/kimi-k2.5:cloud` | Cloud models don't belong in Ollama fallbacks |
| Model not pulled | `ollama pull gemma4:26b` | Gateway fails silently if model doesn't exist locally |

If you see "Invalid input" errors in `openclaw doctor`, check the `model.primary` format — it must start with `ollama/`.

## References

- `references/config-reference.md` — Full openclaw.json, bindings, and auth-profiles.json examples
- `references/troubleshooting.md` — Common errors, fixes, and Node.js compatibility notes


