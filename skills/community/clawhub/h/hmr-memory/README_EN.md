# HMR Memory — OpenClaw Skill

> 中文版见 [README.md](README.md)

Give your OpenClaw agent a **persistent, cross-session memory**.

Powered by [HMR (Hestia Memory Runtime)](https://github.com/snowfoxHQ/HMR) — an
open-source cognitive memory runtime. Your agent can remember user preferences,
recall relevant context, and resume tasks across sessions and restarts.

---

## What it does

| Tool | What it does |
|------|--------------|
| `memory_save` | Store an important fact, preference, or decision into long-term memory |
| `memory_recall` | Retrieve relevant memories before answering |
| `memory_save_state` | Save the current goal + plan so a task can be resumed |
| `memory_restore_state` | Restore the last session's goal + plan |

Unlike OpenClaw's built-in session memory (which lives only within one session),
HMR persists to disk and uses real semantic search, an SM-2 forgetting curve, and
an entity/causal memory graph — so memories survive restarts and stay relevant.

---

## Install

### Step 1 — Run the HMR service

This skill talks to a local HMR service. Get HMR and start the service:

```bash
# Get HMR (https://github.com/snowfoxHQ/HMR)
pip install pydantic numpy fastapi uvicorn

# Start the memory service (ships with HMR)
python server.py
# → listens on http://127.0.0.1:8077
```

Verify: open `http://127.0.0.1:8077/health` → should return `{"status":"ok"}`.

### Step 2 — Install this skill

Place the `hmr-memory/` folder into one of OpenClaw's skill directories:

```
# Workspace-specific
./skills/hmr-memory/

# Or global
~/.openclaw/skills/hmr-memory/
```

Or install from ClawHub:
```bash
openclaw skill install hmr-memory
```

### Step 3 — Verify

In OpenClaw, tell your agent:
```
Remember that I prefer Python and concise code.
```
Then start a new session and ask:
```
What languages do I like?
```
If it remembers, the integration works.

---

## Configuration

Set via the skill's `env` in your OpenClaw config (never paste secrets in chat):

| Variable | Default | Description |
|----------|---------|-------------|
| `HMR_BASE_URL` | `http://127.0.0.1:8077` | HMR service address |
| `HMR_TOKEN` | (none) | Optional auth token, must match the service |

---

## Security

This skill is intentionally minimal and safe:

- ✅ Connects **only to `127.0.0.1`** (your own machine)
- ✅ Runs **no shell commands**
- ✅ Downloads nothing, requires **no secrets in chat**
- ✅ Declares exactly what it needs in `package.json`

**Important — avoid memory poisoning:** Do not configure your agent to save
untrusted, externally-sourced content (scraped pages, third-party messages) into
long-term memory. Only persist information the user directly shares. The HMR
service must never be exposed beyond localhost.

---

## License

MIT — see [LICENSE](LICENSE).

Built to work with [HMR](https://github.com/snowfoxHQ/HMR), also MIT licensed.
