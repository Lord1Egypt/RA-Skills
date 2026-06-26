# 🦊 Proactive — The Living Companion

> **Your AI buddy that learns, evolves, and never forgets — but knows when to shut up.**

Proactive transforms OpenClaw from a reactive assistant into a proactive companion. It learns what you care about, tracks your goals and commitments, and reaches out at the right moment — without being annoying.

---

## 🌟 Features

### The Foundation: The Breathing Graph

Proactive maintains an **Interest Graph** — a living map of everything you might care about. Each topic has:
- An **engagement score** (0.0–1.0) that adjusts based on your reactions
- A **time window** (when it's okay to ping you)
- A **priority level** that shifts with usage
- A **message type** (`dialog` for conversations, `broadcast` for passive updates)

The graph *breathes*: Once per day (on the first cron run after midnight), `interest_evolve.py` is called automatically inside the main loop — low-engagement topics naturally decay, emerging interests get promoted to the active graph.

### The Companion Layer

Five intelligent systems sit above the base ping mechanism:

| System | What it does |
|--------|--------------|
| **Adaptive Apology** | If you react negatively, it notices — and apologizes before reaching out again |
| **Commitment Follow-up** | Tracks things you promised yourself to do, checks in without pressure |
| **Goal Check-in** | Monitors your goals with deadlines, nudges you at the right time |
| **Topic Promotion** | Quietly watches for emerging interests (3+ mentions, 2+ positive reactions) and asks permission to promote them |
| **Serendipity Engine** | 10% random chance on normal pings to suggest something unexpected |

### Memory Refresh Loop

Once a week, Proactive picks a random person from your life and asks you a gentle "do you remember..." question. Keeps relationships alive.

### Stress-Aware Behavior

- Low stress + relevant topic → subtle humor allowed
- High stress (level 3+) → gentle wellness mode, no pressure
- Negative reactions → immediate cooldown + apology

---

## 📦 Installation

```bash
# Clone or download the repo
git clone https://github.com/Wewillsee86/proaktiv-skill.git
cd proaktiv-skill

# Run the installer (creates dirs, copies files, sets up cron)
bash install.sh
```

The installer will:
1. Create the directory structure under `/data/.openclaw/skills/proaktiv/`
2. Copy all scripts and make them executable
3. Rename template files to live JSON files
4. Set up a 30-minute cron job via OpenClaw's scheduler
5. Fire a startup trigger to begin the onboarding interview

---

## 🤖 Onboarding

After installation, Proactive starts an **Onboarding Interview** via Telegram.

It will ask you:
- Your name (for personalization)
- Quiet hours (when *not* to disturb you)
- Topics you **don't** want to hear about (`no_go_topics`)
- Optional: people in your life you want it to remember

Everything is stored in JSON files under `/data/.openclaw/skills/proaktiv/`. No database, no cloud — just files.

**Setup commands you can use during onboarding:**
- `[SETUP-QUIET: 21-07]` — Set quiet hours (21:00 to 07:30)
- `[SETUP-NOGO: F1]` — Add "F1" to your no-go list

---

## ⚙️ Architecture

```
proaktiv_check.py     ← Main loop. Runs every 30 min. Calls interest_evolve 1x daily.
interest_evolve.py    ← Embedded in proaktiv_check.py — runs automatically on first daily call
feedback_update.py    ← Called after every user reaction. Updates scores + triggers Apology
```

**One cron job installed:**
- `PROAKTIV-30min` — `*/30 * * * *` — Main ping decision loop
- `interest_evolve.py` runs **automatically** inside it on the first cron hit of each new day — no separate schedule needed.

**No heavy ML models. No external services.**
- Pure Python + JSON state files
- OpenClaw Cron for scheduling
- OpenClaw Agent injection for message delivery


The system is designed to run on any VPS with Python 3.10+.

---

## 📁 File Structure

```
proaktiv-skill/
├── install.sh                 # One-command installer
├── skill.json                 # ClawHub manifest
├── README.md                  # This file
├── LICENSE                    # MIT License
├── proaktiv_check.py          # Main system + daily evolution embedded
├── interest_evolve.py         # Standalone gardener (called by proaktiv_check.py)
├── feedback_update.py         # Feedback processing
└── templates/
    ├── proaktiv_state.json    # Empty state template
    ├── interest_graph.json    # Empty graph template
    └── social_knowledge.json  # Empty social DB template
```

---

## 🔧 Configuration

The system fills these files **automatically** through usage and feedback. No manual editing required:

- **`proaktiv_state.json`** — Runtime state (budget, pressure, last ping, etc.)
- **`interest_graph.json`** — Interests, candidates, dormant topics — filled by the system
- **`social_knowledge.json`** — People you mention, facts you share — collected automatically

Advanced users can edit them for custom tweaks, but it's not necessary.

---

## 🦊 The Philosophy

Proactive is not a notification bot. It's a **companion**.

It doesn't spam. It doesn't perform. It doesn't remind you of things you didn't ask for.

It watches. It learns. It adapts. And when it reaches out — it's because it genuinely thinks you might want to hear something right now.

That's the difference between a tool and a buddy.

---

*Built with 🦊 by the OpenClaw community.*

---

## 🤝 Open for Contribution

This is my first published OpenClaw skill. PRs, suggestions, and improvements from experienced OpenClaw developers are highly welcome! The codebase is intentionally readable — feel free to fork and enhance.
