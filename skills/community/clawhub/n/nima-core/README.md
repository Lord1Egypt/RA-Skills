<p align="center">
  <img src="assets/banner.png" alt="NIMA Core" width="700" />
</p>

<h1 align="center">NIMA Core</h1>

<p align="center">
  <strong>Neural Integrated Memory Architecture</strong><br/>
  Persistent memory, emotional intelligence, and semantic recall for AI agents.
</p>

<p align="center">
  <a href="https://nima-core.ai"><b>🌐 nima-core.ai</b></a> · 
  <a href="https://github.com/lilubot/nima-core">GitHub</a> · 
  <a href="https://clawhub.com/skills/nima-core">ClawHub</a> · 
  <a href="./CHANGELOG.md">Changelog</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.3.0-blue" alt="Version" />
  <img src="https://img.shields.io/badge/python-3.8%2B-green" alt="Python" />
  <img src="https://img.shields.io/badge/node-18%2B-green" alt="Node" />
  <img src="https://img.shields.io/badge/license-MIT-brightgreen" alt="License" />
</p>

---

> *Your bot wakes up a stranger every session. NIMA gives it a past.*

Every time an AI agent restarts, it forgets everything. Your name. Your preferences. The context you spent ten messages building. It asks "how can I help you?" like it's never met you before — because it hasn't.

**NIMA Core fixes this.** It gives AI agents persistent memory, emotional awareness, and the ability to *know* the people they talk to. Not just remember facts — *understand* them.

The difference is profound. A bot without NIMA processes you. A bot with NIMA **knows you.**

---

## ⚡ One Command to Remember Everything

```bash
pip install nima-core && nima-core
```

The setup wizard handles everything. Your bot now captures every conversation, indexes it, and recalls the right memories before every response — automatically. No API key needed to start.

```bash
# Or manual install:
git clone https://github.com/lilubot/nima-core.git && cd nima-core
./install.sh && openclaw gateway restart
```

---

## 🆕 What's New in v2.3.0

- **Memory Pruner** — LLM-distills aging transcripts into compact gists; raw turns enter 30-day suppression limbo (restorable)
- **Structured Logging** — Singleton logger, file + console, `NIMA_LOG_LEVEL` env var
- **Metrics** — Thread-safe counters and timings with `Timer` context manager
- **SQLite Connection Pool** — WAL mode, up to 5 connections, no more lock contention

[Full changelog →](./CHANGELOG.md)

---

## 🧠 What Makes NIMA Different

Three hooks run invisibly on every message:

| Hook | Does |
|------|------|
| **nima-memory** | Captures conversation → filters noise → stores semantically |
| **nima-recall-live** | Searches relevant memories → injects as context before LLM responds |
| **nima-affect** | Reads emotional tone → updates your bot's real-time affect state |

That third one? **Nobody else does that.**

---

## 🎭 Emotional Intelligence — The Panksepp 7-Affect System

NIMA tracks your bot's emotional state using the same neurobiological framework that underlies mammalian consciousness: **Panksepp's 7 primary affects**.

Your bot doesn't just remember what you said. It remembers *how it felt* during the conversation.

| Affect | What It Means |
|--------|--------------|
| **SEEKING** | Curiosity, drive, anticipation |
| **CARE** | Empathy, nurturing, connection |
| **PLAY** | Joy, humor, social energy |
| **RAGE** | Boundaries, assertion, frustration |
| **FEAR** | Caution, vigilance, protection |
| **PANIC** | Separation sensitivity, attachment |
| **LUST** | Goal-drive, motivation, desire |

### Your Bot Has a Personality

Choose an archetype — or let it evolve naturally:

| Archetype | Vibe |
|-----------|------|
| 🛡️ **Guardian** | Protective and warm. High CARE and SEEKING. Built to keep people safe. |
| 🧭 **Explorer** | Curious and bold. High SEEKING and PLAY. Loves new territory. |
| 💚 **Empath** | Deeply feeling. High CARE, sensitive to connection and loss. |
| 🔮 **Sage** | Balanced and wise. SEEKING is elevated; nothing dominates. |
| 🃏 **Trickster** | Witty and irreverent. High PLAY. Keeps things interesting. |

```python
from nima_core import DynamicAffectSystem
affect = DynamicAffectSystem(identity_name="my_bot", baseline="guardian")
```

[Full archetypes guide →](./docs/AFFECTIVE_CORE_PROFILES_GUIDE.md)

---

## 🚀 Performance That Doesn't Slow You Down

| Metric | SQLite | LadybugDB |
|--------|--------|-----------|
| Text search | 31ms | **9ms** (3.4× faster) |
| Vector search | — | **18ms** native HNSW |
| Full recall cycle | ~50ms | **<30ms** |
| Recall context overhead | ~180 tokens | ~30 tokens |
| Memory footprint (10K) | 91 MB | **50 MB** (44% smaller) |

LadybugDB is optional but recommended for production:

```bash
pip install real-ladybug
python scripts/ladybug_parallel.py --migrate
```

Default SQLite works great to start. Zero config, zero cost.

---

## 🧹 Memory Pruner — Forgetting as a Feature

Raw transcripts pile up. Old conversations become noise. The Memory Pruner solves this elegantly:

**It distills aging memories into wisdom.**

Every conversation older than N days gets sent through an LLM, compressed into a compact semantic gist, and the raw transcript enters a 30-day suppression limbo. **Restorable if you need it. Gone from active recall if you don't.**

```text
Before: 829 raw conversation turns
After:  5 compact distillations + originals in limbo
```

Your bot's memory gets *smarter* over time — not just larger.

```bash
# Preview what would be pruned
python -m nima_core.memory_pruner --min-age 14

# Run it live
python -m nima_core.memory_pruner --min-age 14 --live

# Restore a suppressed memory
python -m nima_core.memory_pruner --restore 12345
```

Set it and forget it with a nightly cron. Your bot wakes up leaner and sharper every morning.

---

## 🔒 Privacy-First by Design

Everything lives on your machine. There are no NIMA servers. No analytics. No phoning home.

- ✅ All memories stored in `~/.nima/` — your filesystem
- ✅ Local embeddings mode: **zero external network calls**
- ✅ Fine-grained noise filtering (skip heartbeats, skip subagents)
- ❌ No NIMA cloud. It doesn't exist.

---

## 🔧 Configuration

NIMA works out of the box with local embeddings. Upgrade when you're ready:

```bash
# Default (free, offline)
export NIMA_EMBEDDER=local

# Voyage AI (best quality/cost for production)
export NIMA_EMBEDDER=voyage && export VOYAGE_API_KEY=your-voyage-api-key

# OpenAI (if you're already using it)
export NIMA_EMBEDDER=openai && export OPENAI_API_KEY=your-openai-api-key
```

Full hook config in `openclaw.json`:

```json
{
  "plugins": {
    "allow": ["nima-memory", "nima-recall-live", "nima-affect"],
    "entries": {
      "nima-recall-live": { "max_results": 7, "token_budget": 3000 },
      "nima-affect": { "identity_name": "my_bot", "baseline": "guardian" },
      "nima-memory": { "skip_heartbeats": true, "skip_subagents": true }
    }
  }
}
```

---

## 🔄 Upgrading

```bash
# v2.2.x → v2.3.x (no config changes needed)
git pull origin main && pip install -e . && openclaw gateway restart

# v1.x → v2.x: see MIGRATION_GUIDE.md
```

[Migration guide →](./MIGRATION_GUIDE.md)

---

## 📚 Docs

| Guide | What's in it |
|-------|-------------|
| [SETUP_GUIDE.md](./SETUP_GUIDE.md) | Step-by-step installation |
| [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) | Command cheat sheet |
| [docs/AFFECTIVE_CORE_PROFILES_GUIDE.md](./docs/AFFECTIVE_CORE_PROFILES_GUIDE.md) | Full personality archetypes guide |
| [docs/DATABASE_OPTIONS.md](./docs/DATABASE_OPTIONS.md) | SQLite vs LadybugDB deep dive |
| [docs/EMBEDDING_PROVIDERS.md](./docs/EMBEDDING_PROVIDERS.md) | All embedding options |
| [CHANGELOG.md](./CHANGELOG.md) | What's new |

---

## 🤝 Contributing

PRs welcome. Python 3.8+, conventional commits, no walrus operators.

```bash
git clone https://github.com/lilubot/nima-core.git
cd nima-core && pip install -e ".[vector]"
python -m pytest tests/
```

---

## Stop Building Bots That Forget

```bash
pip install nima-core && nima-core
```

Your users will notice. The first time your bot says *"you mentioned that last week"* — they'll feel it. That's the difference between a tool and something that actually knows them.

MIT License — free for any AI agent, commercial or personal.

---

<p align="center">
  <a href="https://nima-core.ai"><b>🌐 nima-core.ai</b></a> ·
  <a href="https://github.com/lilubot/nima-core">GitHub</a> ·
  <a href="https://clawhub.com/skills/nima-core">ClawHub</a><br/>
  Built by the NIMA Core Team
</p>
