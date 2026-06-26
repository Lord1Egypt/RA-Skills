# Security Statement

## Why ClawHub Flagged This Skill

ClawHub Security flagged this skill as "suspicious" due to these concerns:

### 1. Misleading "Local-Only" Claim
The SKILL.md previously emphasized "local Ollama — no cloud API" while the code actually supports cloud backends (Zhipu, OpenAI) if API keys are configured.

**Resolution in v0.3.0:** SKILL.md now clearly documents the privacy implications of each backend.

### 2. Cloud API Fallback
If `ZHIPU_API_KEY` or `OPENAI_API_KEY` environment variables are set, MEMORY.md content will be sent to cloud embedding endpoints.

**Mitigation:**
- To stay fully local, ensure Ollama is running and DO NOT set cloud API keys
- Use `python3 memory_tree.py config backend keyword` to force local keyword mode
- The skill auto-detects backends and prefers local Ollama when available

### 3. Cron Job Creation
The `setup` command creates persistent cron jobs for automatic indexing/decay/cleanup.

**Mitigation:**
- Review what the setup script writes to crontab before running
- You can also run index/decay/cleanup manually without cron
- Cron jobs are user-level (not system-wide) and can be removed anytime

## What This Skill Does

- ✅ Reads `~/.openclaw/workspace/MEMORY.md`
- ✅ Writes to `~/.openclaw/workspace/memory-tree/data/` (confidence, embeddings, archive)
- ⚠️ May send memory content to cloud embedding APIs (if configured)
- ✅ Creates cron jobs (only when you run `setup`)

## What This Skill Does NOT Do

- ❌ No hidden data exfiltration
- ❌ No execution of external code
- ❌ No network calls unless you configure cloud backends
- ❌ No modification of files outside its designated directories

## Verdict

🟡 **INSTALL WITH AWARENESS**

This is a legitimate memory management tool. The "suspicious" flag comes from:
1. Previously unclear documentation about cloud fallbacks
2. Automatic cron creation (user-visible, not hidden)

If you want **strictly local** operation:
1. Run `ollama serve` with an embedding model
2. Don't set `ZHIPU_API_KEY` / `OPENAI_API_KEY`
3. Verify with `python3 memory_tree.py config show`

## Source Code Review

All logic is in `scripts/memory_tree.py` — a single Python file using only standard library modules.