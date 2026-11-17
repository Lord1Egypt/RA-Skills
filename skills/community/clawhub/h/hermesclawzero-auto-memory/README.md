# HermesClawZero Auto Memory

[![ClawHub](https://img.shields.io/badge/ClawHub-hermesclawzero--auto--memory-blue)](https://clawhub.ai/sunme1977/skills/hermesclawzero-auto-memory)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Your agent remembers across conversations.** Facts, preferences, project context, past decisions — the agent captures them automatically and loads relevant context on every new session.

All processing runs **locally** via HermesClawZero Sidecar (PostgreSQL + pgvector + Ollama for embeddings). No data leaves your machine.

---

## Features

| Capability | What it means for you |
|---|---|
| **Auto-Capture** | Agent saves new facts, preferences, and project details *as you talk* — no manual saving needed |
| **Auto-Load** | On fresh chats, the agent searches past memories and picks up where you left off |
| **Semantic Search** | Finds memories by meaning, not just keywords (hybrid vector + lexical) |
| **Chat Backup** | Say "save this session" and get a full searchable snapshot |
| **DB Maintenance** | Optional nightly tagging + daily reminders (cron, opt-in) |

---

## Quickstart (3 minutes)

### 1. Install

```bash
openclaw skills install hermesclawzero-auto-memory
```

### 2. Configure

The memory.py CLI lives at `C:\dev\HermesClawZero-ConfigSidecar\memory.py`.  
It reads config from `.env` or environment variables.

Create or edit your `.env` with:

```bash
MEM_PUBLIC_URL=http://localhost:8010
API_KEY=your_api_key_here
```

> 💡 `MEM_PUBLIC_URL` points to the HermesClawZero Sidecar API. Default is `http://localhost:8010`.
> `API_KEY` must match the `API_KEY` in your Sidecar's `.env`.

### 3. Verify connectivity

```bash
python C:\dev\HermesClawZero-ConfigSidecar\memory.py search "hello world" 3
```

If the Sidecar is running, you'll see matching memories (or no output if the DB is empty — that's fine).

### 4. Done! The skill is active.

Now when you talk to the agent, it will:
- **Silently load** context from past memories on fresh sessions
- **Automatically capture** new facts, preferences, and project details
- **Respond without re-introducing** who you are or what you're working on

---

## Example Workflow

```
── Session 1 ──
You: "Hey, I'm Hans. I work on DiskRaptor v0.3, mostly UI tests."
Agent: *silently captures: "User's name is Hans", "Working on DiskRaptor v0.3", "Focus: UI tests"*
Agent: "Hi Hans! What would you like to do with DiskRaptor today?"

You: "I prefer dark mode in all my tools."
Agent: *silently captures: "User prefers dark mode in all UIs"*

Some time passes. A new session starts.

── Session 2 (fresh chat) ──
Agent: *silently loads past memories*
Agent: "Welcome back, Hans! Last time you were working on DiskRaptor v0.3 UI tests.
       Shall we pick that up, or is there something new?"
```

## Deterministic Capture Triggers

The agent captures when you share:

| Trigger | Example | Gets captured |
|---|---|---|
| **Name / identity** | "Call me Hans" | `"User's name is Hans"` |
| **Preference** | "I hate notifications" | `"User prefers notifications off"` |
| **Project detail** | "The API is on port 8080" | `"API runs on port 8080"` |
| **Decision** | "Let's use SQLite" | `"Chose SQLite for storage"` |
| **Correction** | "No, the branch is 'main'" | `"Default branch: main"` |
| **Blocker/error** | "The build fails" | `"Build fails on Windows, needs fix"` |

The agent does **not** capture: small talk ("thanks", "ok"), raw questions, or temporary/throwaway info.

---

## Usage (manual commands)

```bash
# Capture a fact
python C:\dev\HermesClawZero-ConfigSidecar\memory.py capture "User prefers dark mode" ui_preferences

# Search memories
python C:\dev\HermesClawZero-ConfigSidecar\memory.py search "project preferences" 5

# Backup session history
python C:\dev\HermesClawZero-ConfigSidecar\memory.py autosave "$(cat backup.md)" "session_backup.md"
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `memory.py search` returns nothing but DB has data | API_KEY mismatch | Check `.env` API_KEY matches Sidecar's |
| `ConnectionError` on any command | Sidecar not running | `docker compose up -d` in the Sidecar directory |
| `HTTP 500` on capture | Ollama not running or misconfigured | `ollama pull nomic-embed-text` and check `/healthz` |
| Agent doesn't seem to capture anything | Fresh install — no .env configured | Check `MEM_PUBLIC_URL` and `API_KEY` in `.env` |
| Agent captures duplicates | No dedup check in SKILL.md triggers | Update if you see repeated captures of the same fact |
| Cron jobs not working | User didn't opt in | Ask to run: "setup memory background jobs" |

### Debug mode

Run with verbose logging to see what the CLI is doing:

```bash
python C:\dev\HermesClawZero-ConfigSidecar\memory.py search "test" 1
```

If you see nothing, check:
1. Is the Sidecar accessible? → `curl http://localhost:8010/healthz`
2. Is the API key correct? → Check the exact `.env` content
3. Is Ollama running? → `curl http://localhost:11434/api/tags`

---

## Skill Structure

```
hermesclawzero-auto-memory/
├── SKILL.md              # Agent instructions (deterministic triggers)
├── skill-card.md         # ClawHub marketplace card
├── permissions.yaml      # Declared permissions
├── secrets.yaml          # Declared secrets
├── README.md             # This file
├── CHANGELOG.md          # Version history
└── scripts/
    ├── install.ps1       # Install verification
    ├── update.ps1        # Update check
    └── smoke_test.ps1    # Integration smoke tests
```

The core script lives alongside the sidecar:
```
C:\dev\HermesClawZero-ConfigSidecar\
├── memory.py             # CLI tool (capture/search/autosave)
├── gardener.py           # Nightly tagging
├── daily_reminder.py     # Daily highlights
├── .env                  # API config
└── ...
```

---

## Repository

Source: [github.com/SunMe1977/HermesClawZero-ConfigSidecar](https://github.com/SunMe1977/HermesClawZero-ConfigSidecar)  
Skill: [ClawHub hermesclawzero-auto-memory](https://clawhub.ai/sunme1977/skills/hermesclawzero-auto-memory)

---

## License

MIT — see [LICENSE](LICENSE).
