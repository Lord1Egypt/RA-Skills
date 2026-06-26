# Supercharged Memory

**Stop explaining yourself every time you open a chat.**

Give your AI a perfect, searchable memory that lasts forever. It learns your preferences, recalls past conversations, and gets smarter the more you use it.

🛡️ **Codex Security Verified** — Your memories stay on your machine. No data leaves your workspace.

---

## What It Does

Supercharged Memory transforms your AI from a blank slate into a lifelong companion:

- **Automatic context capture** — Your agent notices important facts, decisions, and preferences without you ever saying "remember this"
- **Manual "Jedi" memory** — Say "remember that I prefer dark mode" and it's locked in forever
- **Built-in search engine (QMD)** — Every memory is indexed locally with keyword + semantic search. Ask "what did we discuss about the kitchen renovation?" and get an instant answer
- **Smart organization** — Memories auto-categorize by topic, person, project, preference
- **Self-cleaning** — Periodic consolidation removes outdated info and keeps the system lean
- **Context recovery** — When the AI hits a context limit, it rebuilds understanding efficiently instead of loading everything
- **Universal** — Plugs into ALL your other NormieClaw skills, making them smarter

---

## What's Included

```
supercharged-memory/
├── SKILL.md # Agent operating manual (the brain)
├── SETUP-PROMPT.md # First-run setup (paste to your agent)
├── README.md # This file
├── SECURITY.md # Security audit details
├── config/
│ ├── memory-config.json # Settings & thresholds
│ └── consolidation-rules.md # How memory cleanup works
├── examples/
│ ├── session-start-example.md # Boot sequence walkthrough
│ ├── memory-recall-example.md # Search & retrieval demo
│ └── consolidation-example.md # Periodic maintenance demo
├── scripts/
│ ├── qmd-reindex.sh # QMD reindex automation
│ └── memory-health-check.sh # System health validation
└── dashboard-kit/
 └── DASHBOARD-SPEC.md # Companion dashboard spec
```

---

## Quick Start

1. **Copy** the `supercharged-memory/` folder into your OpenClaw workspace `skills/` directory
2. **Paste** the contents of `SETUP-PROMPT.md` to your agent in chat
3. **Start talking** — your agent handles the rest

That's it. Your AI now has a memory.

---

## Requirements

- **OpenClaw** (any recent version)
- **QMD** (recommended, free) — `brew install qmd` or `cargo install qmd`. The skill works without it, but search falls back to basic `grep`.
- **No API keys required** for the base system — everything runs locally

### Optional: Vector DB Upgrade
For power users with 10,000+ memories who want deeper semantic search:
- **Qdrant** (free, runs locally via Docker or binary)
- **Mem0** (Python package, free)
- **Embedding API key** (e.g., OpenAI — has minor costs, typically pennies per 1K memories)

The setup prompt walks you through this upgrade if you want it.

---

## How It Works

Your agent runs a 4-layer memory stack:

1. **Workspace files** — Core identity files loaded every session (free, instant)
2. **QMD search** — Local BM25 + semantic search across all memory files (free, fast)
3. **File-based deep memory** — Daily notes, topic files, protocols (free, structured)
4. **Vector DB** — Optional Mem0/Qdrant for deep semantic recall (has minor costs)

Seven self-sustaining protocols handle the full lifecycle: capture → store → index → retrieve → consolidate → recover → health check. All automated. Zero babysitting.

---

## Pairs Great With

- **Daily Briefing** — Morning briefing powered by your memory (calendar, priorities, weather)

💡 **Starter Pack ($12.99):** Get Supercharged Memory + Dashboard Builder + Daily Briefing together and save.

---

## FAQ

**Is the memory system free to run?**
Yes. The included system — with full QMD search — runs entirely locally at zero cost.

**How does the search work?**
QMD combines traditional keyword matching with semantic understanding. It indexes every memory file automatically. Your agent can find relevant context even when you don't use the exact same words.

**What's the Vector DB upgrade?**
An optional layer for power users. It adds Mem0/Qdrant semantic search on top of QMD. Requires an embedding API key (minor costs). Most users won't need it.

**Does my data leave my machine?**
Never (unless you enable the Vector DB with a cloud embedding API — and even then, only embeddings are sent, not your raw memories). The base system is 100% local.

**Can I edit my memories?**
Yes. They're plain Markdown files in your workspace. Edit them directly or ask your agent to update them.
