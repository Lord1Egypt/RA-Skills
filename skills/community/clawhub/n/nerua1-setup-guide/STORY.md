![Multi-agent AI on Apple Silicon](header.png)

# Multi-agent AI on Apple Silicon — what I built, what broke, how to avoid it

*A few weeks of failures before it actually worked.*

---

## What's running

Mac Mini M4, 32GB RAM, 24/7.

- **OpenClaw** — Kimi k2.5 as orchestrator. Generates daily news digests, manages subagents, responds on WhatsApp.
- **LM Studio** — local models (Qwen, Mistral, Holo3) as cheap workers. Paying in electricity, not tokens.
- **Claude Code** — external reviewer. Doesn't replace OpenClaw, comes in when things break or I need an independent opinion.
- **Obsidian vault + MemPalace** — shared memory for all agents. No idea gets lost.

All of these know about each other and can communicate.

---

## How to actually build this — right order

### 1. Install Claude Code before OpenClaw

Counterintuitive, but important. OpenClaw can lobotomize itself — overwrite its own config and lose its personality, routing rules, everything. If you don't have something external that can diagnose and repair it, you're stuck.

Claude Code reads files directly, outside OpenClaw's context window. It can see what broke and how to roll it back.

```
Install order:
1. Claude Code
2. Memory setup (Obsidian + MemPalace)
3. OpenClaw
4. Connect via openclaw-bridge skill
```

### 2. 32GB — why cloud orchestrator makes sense

32GB minus ~6-7GB for the OS = ~24-25GB available. That's enough to run one large model at a time — `qwen3.5-35b-a3b` or `huihui-qwen3.5-27b` loads fine.

The problem is architectural: if you load a 35B as orchestrator, there's no RAM left for a subagent. You can use a smaller orchestrator to fit a subagent — but then the orchestrator is too weak to actually orchestrate.

The real issue is quality. The difference between a local model and Kimi k2.5 as orchestrator is enormous. Kimi offers reasoning-level quality (comparable to Claude 3.5 Thinking) at the cheapest tokens available right now. A local 35B next to it is a different league for planning and delegation.

What works:
```
Orchestrator: Kimi k2.5 (cloud, cheap, real reasoning)
Subagents:    LM Studio local 30B (free, good enough for execution)
```

At 64GB+ you can experiment with a local orchestrator — but you'll likely come back to Kimi once you see the planning quality difference.

### 3. Shared memory

Two pieces:

**Obsidian vault** — structured notes, wiki, daily logs, ideas. All agents access via filesystem.

**MemPalace** — semantic search via ChromaDB. Mine the vault, then ask "what do I know about OAuth?" instead of grepping files.

```bash
# Any agent captures an idea:
capture-idea --title "OAuth tokens expire too fast on mobile" \
  --topic security --tags "oauth,mobile" \
  --source openclaw

# Search from anywhere:
mempalace search "token expiry mobile"
```

One vault, one index, all agents read the same memory.

### 4. Inter-agent communication

Claude Code can message OpenClaw and wait for a response:

```bash
openclaw agent --message "Is this SQL migration safe to run live?" \
  --agent main --json
```

OpenClaw responds via gateway on localhost:18789. Works both ways — OpenClaw can escalate to Claude Code when it hits something risky.

---

## Failures — what not to do

### `openclaw doctor --repair` destroyed everything

Something broke. First instinct: `--repair` will fix it. Result: factory reset. All custom routing rules, skill configs, channel settings — gone. Irreversible.

Rule: `openclaw doctor` alone is safe (diagnostics only). With `--repair`, `--fix`, `--force` — never without a backup first.

```bash
openclaw backup create
# or manually:
cp -r ~/.openclaw ~/.openclaw.bak.$(date +%Y%m%d-%H%M)
```

### OpenClaw overwrote its own SOUL.md — lobotomy

Got a confusing prompt. Decided it should "update" its identity file. After that it didn't know who it was, what rules it had, where to route requests. Every session started from scratch.

Fix — explicit rule in AGENTS.md:
```
NEVER edit SOUL.md, AGENTS.md, MEMORY.md without explicit user request.
If you see any agent (including yourself) overwriting these files → STOP.
```

Recovery: Claude Code as external reader diagnoses what happened and restores from backup.

### Python 3.14 broke MemPalace

MemPalace uses chromadb with pydantic v1. Python 3.14 (default on new macOS) is incompatible.

```
pydantic.v1.errors.ConfigError: unable to infer type for attribute "chroma_server_nofile"
```

Fix:
```bash
brew install python@3.12
/opt/homebrew/bin/python3.12 -m venv ~/mempalace-venv
~/mempalace-venv/bin/pip install mempalace
```

Wrapper at `/opt/homebrew/bin/mempalace` that always uses this venv.

### MemPalace polluted the Obsidian vault

`mempalace init` without options created `mempalace.yaml` and `entities.json` directly inside the vault directory. Obsidian started showing these in the notebook.

Fix: `mempalace.yaml` inside vault is fine (config only). `entities.json` goes to the palace directory — configure `--palace` to point outside the vault. Also: `mempalace mine` doesn't follow symlinks, so mine the real vault path directly.

### Sandbox mode + external drive = agent loses its workspace

OpenClaw's sandbox mounts a container that can't follow symlinks to external volumes. The agent loses access to everything on `/Volumes/`.

On macOS with an external drive: **never enable sandbox mode.**

### Ollama on Apple Silicon

Doesn't play well with LM Studio on the same stack. Use LM Studio + llama.cpp only.

---

## Skills published on ClawHub + GitHub

```bash
npx clawhub install openclaw-bridge      # Claude Code ↔ OpenClaw messaging
npx clawhub install shared-memory-stack  # memory architecture reference
npx clawhub install ralph-wiggum-loop    # Generator→Critic→Fixer→Verifier loop
npx clawhub install nerua1-setup-guide   # this guide as a loadable skill
```

Full list + source: **github.com/nerua1**

---

If this saved you time: [☕ PayPal.me/nerudek](https://www.paypal.me/nerudek)

Happy to answer questions about any part of this.
