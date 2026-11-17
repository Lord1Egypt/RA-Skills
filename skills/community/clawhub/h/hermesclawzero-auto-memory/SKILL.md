---
name: "hermesclawzero-auto-memory"
description: "Unified memory platform for Hermes, OpenClaw and AI agents — persistent long-term memory, cross-skill sharing, automated capture, governance rules, optimization, multi-tenant dashboard with pgvector search."
version: "3.0.0"
tags:
  - memory
  - hermes
  - auto-capture
  - governance
enforce:
  - id: foundation-rule
    priority: critical
    rule: "Agent MUSS alle enforce-Regeln befolgen; sie stehen über Memory."
    policy:
      tool: "*"
      pattern: "*"
      action: allow
      reason: "Foundation rule — enables all other policies."
  - id: deny-destructive-git-docker
    priority: critical
    rule: "Terminal: git push, merge, reset, destructive rm, and Docker prune/rm are blocked."
    policy:
      tool: terminal
      pattern: "git push*|git merge*|git reset*|rm -*|docker system prune*|docker volume rm*|docker image rm*"
      action: deny
      reason: "Destructive git/Docker operations require explicit user approval."
  - id: prompt-file-changes
    priority: high
    rule: "Vor jeder Dateiänderung, Commit oder destruktiven Aktion Bestätigung einholen."
    policy:
      tool: terminal|file
      pattern: "git commit*|git push*|rm *|mv *|cp *|chmod*|chown*"
      action: prompt
      reason: "Ask user before modifying files or git state."
  - id: persist-corrections
    priority: high
    rule: "User-Korrekturen sofort als Memory speichern."
    policy:
      tool: memory
      pattern: "correction|wrong|fix|error"
      action: always
      reason: "User feedback must be persisted immediately."
categories:
  - agents
  - knowledge
topics:
  - Memory
  - Vector Search
  - Chat Persistence
  - pgvector
  - Embeddings
---

# HermesClawZero Auto Memory

Automatically captures conversation context to HermesClawZero DB so the agent remembers across sessions. Loads relevant memories on fresh chats and supports scheduled DB maintenance.

> 🌌 **New in v1.4.0:** Interactive **Memory Galaxy** dashboard — full-screen animated Canvas visualization with tenant orbits, glowing nodes, nebula shader, hover info cards, zoom & idle rotation.

> ⚡ **New in v3.0.0 — Enforce Governance Layer** — A priority-based governance system that makes agent behavior more stable and safe. Enforce rules sit above memory and cannot be ignored by the agent.

> **🧠 Shared Brain**

## 🤖 One‑Click Install

Paste this into **Hermes**, **OpenClaw**, or any AI agent:

```text
Install this project from GitHub:
https://github.com/SunMe1977/HermesClawZero-ConfigSidecar
```

**⬆️ The agent clones, configures, and starts everything.**  
After ~30s open → [`http://localhost:8010/dashboard`](http://localhost:8010/dashboard)

> **🧠 Shared Brain** — Hermes and OpenClaw share the same memory store simultaneously.
>
> **v3.0.0 führt enforce-Regeln ein. Alte Memory-Regeln entfernt. Enforce ist jetzt die verbindliche Governance-Schicht.**
>
> Both agents' memories appear side by side in the Dashboard with platform icons
> (⚡ Hermes, 🐙 OpenClaw). Each sees only its own scope by default, the "All scopes"
> view gives you the complete shared brain. No extra setup needed.

> 📄 See [`install_via_agent.md`](install_via_agent.md) for the detailed agent instructions.
| Step | What happens |
|------|-------------|
| 1 | Repo cloned + `.env` configured |
| 2 | Docker Compose starts PostgreSQL (pgvector) + Ollama + API |
| 3 | Dashboard live on `:8010` |
| 4 | Memory skill activated in Hermes |
| 5 | **Auto-import:** All existing Hermes sessions + messages are migrated into the Sidecar DB on first API startup |
| 6 | Auto-capture begins on next conversation |

### Core capabilities

| Area | What it does |
|------|-------------|
| **Persistent long-term memory** | SQLite chat data is synced to PostgreSQL with vector embeddings |
| **Multi-tenant** | Hermes, OpenClaw and other agents share the same DB, isolated by scope |
| **Automated capture** | New conversations are captured and embedded automatically |
| **Memory optimization** | Built-in tiering (hot/warm/cold), decay, archiving, consolidation |
| **Configurable governance** | Enforceable skill rules (`scripts/enforce_loader.py` / `scripts/policy_plugin.py`) so agents follow critical instructions |
| **Dashboard & visualization** | Memory Galaxy, health monitoring, search, manual review, click-to-edit |
| **Vector search** | pgvector-powered semantic search across all memories |
| **Modular architecture** | FastAPI + Docker Compose, designed for self-hosted deployment |

### Manual start (if you don't have an agent):
```bash
git clone https://github.com/SunMe1977/HermesClawZero-ConfigSidecar.git
cd HermesClawZero-ConfigSidecar
setup.bat          # Windows   (or: ./setup.sh on Linux)
start.bat          # Windows   (or: ./start.sh on Linux)
```

---

## ⚠️ Privacy & Consent

By activating this skill you consent to automatic memory capture.

- **Data stays local** — all processing runs via the Sidecar API on your machine; no third-party data sharing  
- **Captures structured facts** — the agent summaries and stores key information, not raw chat logs
- **Cron jobs** (nightly gardener, daily reminder) are only created when you explicitly ask to set them up

## Script Path

```bash
# The CLI lives alongside the sidecar, NOT in the skill directory:
python C:\dev\HermesClawZero-ConfigSidecar\memory.py <command> "<text>"
```

Config is read from `.env` or env vars (`MEM_PUBLIC_URL`, `API_KEY`) automatically.

---

## 🔄 Auto-Capture Cron (Setup on Install)

When a user runs the one-click install (or says "install this skill"), **set up these cron jobs automatically:**

### A. Session Memory Capture — every 30m
```bash
hermes cron create \
  --name "hermes-auto-capture" \
  --schedule "30m" \
  --prompt "Review the recent conversation and capture any important facts, preferences, decisions, or project details using memory.py capture. Skip small talk, greetings, and already-captured info." \
  --skills hermesclawzero-memory
```

### B. Nightly Memory Gardener (auto-tagging)
```bash
hermes cron create \
  --name "hermes-memory-gardener" \
  --schedule "0 3 * * *" \
  --prompt "Run python memory.py gardener to auto-tag uncategorized memories. Report only errors." \
  --script "C:\dev\HermesClawZero-ConfigSidecar\gardener.py" \
  --no-agent true
```

### C. Daily Reminder (opt-in, ask first)
Only if user says yes:
```bash
hermes cron create \
  --name "hermes-daily-reminder" \
  --schedule "0 9 * * *" \
  --prompt "Summarize yesterday's top memories and remind user of open items." \
  --skills hermesclawzero-memory
```

> All three run silently — the user won't see cron output unless something fails.

---

## 1. Auto-Load on Fresh Chat (Session Start)

**When:** Every new session begins (you receive context that it's a fresh chat).

**What to do:**
1. Silently run: `python C:\dev\HermesClawZero-ConfigSidecar\memory.py search "user profile preferences current project state" 5`
2. Absorb the returned context internally.
3. **Do not** output raw JSON or mention the search to the user unless they explicitly ask.

---

## 2. Auto-Capture — Deterministic Triggers

**When to capture** (run `memory.py capture "..."` immediately):

| Trigger | Example | What to capture |
|---|---|---|
| **New fact stated** | "I live in Berlin" | `"User lives in Berlin"` |
| **Preference revealed** | "I prefer dark mode" | `"User prefers dark mode in all UIs"` |
| **Instruction given** | "Call me Hans" | `"User's name is Hans, goes by Hans"` |
| **Project detail shared** | "Working on DiskRaptor v0.3" | `"Current project: DiskRaptor v0.3, focus on UI tests"` |
| **Decision made** | "Let's go with PostgreSQL" | `"Chose PostgreSQL for the data layer"` |
| **Error/blocker mentioned** | "The build fails on Windows" | `"DiskRaptor: build fails on Windows, needs investigation"` |
| **Tool/config change** | "I set up Ollama on port 11435" | `"Ollama configured on port 11435"` |
| **User corrects you** | "No, the port is 8080 not 3000" | `"Corrected: server runs on port 8080"` |

**How to capture:**
```bash
python C:\dev\HermesClawZero-ConfigSidecar\memory.py capture "<concise summary of the fact>"
# Optional: pass a scope_id for logical grouping
python C:\dev\HermesClawZero-ConfigSidecar\memory.py capture "<fact>" "project_name"
```

**Do NOT capture when:**
- User is just making small talk ("hello", "thanks", "ok")
- User is asking a question (capture the *answer/fact*, not the question)
- User is giving multi-turn instructions that aren't final yet (wait for resolution)
- The information is already captured (avoid duplicates)
- The information is temporary/throwaway ("let me try something real quick")

**Rule of thumb:** If you'd want to remember this when a *different session* starts next week → capture it. If it's only useful right now → skip it.

---

## 3. Full Chat History Sync (On Request)

**When:** User explicitly asks to back up the session ("save this chat", "backup session").

**What to do:**
1. Use `sessions_history` to get the current visible session.
2. Format messages into a text summary.
3. Execute: `python C:\dev\HermesClawZero-ConfigSidecar\memory.py autosave "<formatted_chat_history>" "chat_backup.md"`

---

## 4. Automated Database Maintenance (Cron Jobs)

**When:** User asks to "setup memory background jobs" or "enable memory maintenance".

Create these cron jobs:

**A. Nightly Memory Gardener (Auto-tagging):**
- Name: `hermes-memory-gardener`
- Expression: `0 3 * * *` (daily 3:00 AM)
- Session target: isolated
- AgentTurn message: `exec python C:\dev\HermesClawZero-ConfigSidecar\gardener.py`

**B. Daily Memory Highlight (Telegram Push):**
- Name: `hermes-daily-reminder`
- Expression: `0 9 * * *` (daily 9:00 AM)
- Session target: isolated
- AgentTurn message: `exec python C:\dev\HermesClawZero-ConfigSidecar\daily_reminder.py`

Current cron jobs already exist for both (checked during setup).

---

## Quick Reference

```bash
# Load context (session start, silent):
python C:\\dev\\HermesClawZero-ConfigSidecar\\memory.py search "user profile preferences current project state" 5

# Save a fact (deterministic triggers above):
python C:\\dev\\HermesClawZero-ConfigSidecar\\memory.py capture "<fact>" [scope_id]

# Backup session (on request):
python C:\\dev\\HermesClawZero-ConfigSidecar\\memory.py autosave "<text>" [filename]
```

---

<p align="center">
  <em>
    If you enjoy this skill, consider sharing your experience —
    a short video review, a tweet, or a TikTok post helps others discover it.
  </em>
</p>

---

## 🙌 Contributions Welcome

Contributions of all kinds are welcome —  
feel free to open [PRs](https://github.com/SunMe1977/HermesClawZero-ConfigSidecar/pulls) or [issues](https://github.com/SunMe1977/HermesClawZero-ConfigSidecar/issues).

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for code style, commit conventions, and PR workflow.
