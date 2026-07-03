# MemoryAI — Your AI Never Forgets 🧠

> **Session ends. Memory stays.**

MemoryAI gives your AI agent persistent long-term memory. It remembers what you
said, what you decided, and what you prefer — not for hours, but for months and
years. Important things stay sharp; unused details fade gently and snap back the
moment they're needed. Just like the human brain.

## Installation

### ClawdHub (recommended)
```bash
clawdhub install memoryai
```
Then add your API key to `skills/memoryai/config.json`.

### Manual
Copy the skill folder into your OpenClaw workspace:

```
~/.openclaw/workspace/skills/memoryai/
├── SKILL.md
├── config.json
├── CHANGELOG.md
├── README.md
└── scripts/
    └── memory.py
```

Edit `config.json`:
```json
{
  "endpoint": "https://memoryai.dev",
  "api_key": "hm_sk_your_key_here"
}
```

Test: `python skills/memoryai/scripts/memory.py health`

## Commands

```bash
# Store / recall
python scripts/memory.py store "User prefers dark mode" --type preference
python scripts/memory.py recall "what does the user prefer"

# Session lifecycle
python scripts/memory.py bootstrap "working on payment feature"   # wake up
python scripts/memory.py track "message content" --role user       # each message
python scripts/memory.py save "summary of this session"            # when prompted

# Insight
python scripts/memory.py profile   # who is this user?
python scripts/memory.py health    # memory health
```

Memory types: `fact`, `decision`, `preference`, `identity`, `goal`, `procedure`,
`life_event`. Preferences, decisions, identity and procedures never fade.

## Context Guard (Auto)

You don't manage context. The loop is simple:

1. `bootstrap` once at session start.
2. `track` every message — the brain keeps context healthy on its own.
3. `save` when `track` tells you to — you continue on a clean slate, nothing lost.

No cron jobs, no tuning. (Older versions used a periodic background command — that
approach is retired. If you set one up before, remove it.)

## Security & Privacy

- All data is sent over HTTPS to your configured endpoint only.
- No automatic transmission — every call is an explicit invocation.
- `memory.py` uses only the Python standard library — zero third-party dependencies.
- Treat your API key (`HM_API_KEY`) as sensitive and rotate it regularly.
- Export or delete your data anytime from your MemoryAI account.

## Requirements

- Python 3.10+ (no pip install needed)
- A MemoryAI API key — get one at https://memoryai.dev
