<div align="center">

# Personal AI Memory System.skill

> *"Every day of your life is a digital asset — don't let it slip away"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![Version](https://img.shields.io/badge/version-3.1.0-blue)](SKILL.md)
[![Privacy](https://img.shields.io/badge/data-local%20only-brightgreen)](SKILL.md)

<br>

**A continuously growing personal AI memory system — your life recorder and personal decision advisor in one.**

<br>

The more you give it, the better it knows you.<br>
After 3 months, it starts recognizing your patterns.<br>
After a year, it understands you better than you understand yourself.

<br>

[Quick Start](#quick-start) · [Features](#features) · [Privacy & Security](#privacy--security) · [Multi-Tool Support](#multi-tool-support) · [File Structure](#file-structure)

<br>

**其他语言 / Other Languages：**
[中文](README.md)

</div>

---

## What Is This

The **Personal AI Memory System** is an AI Skill that transforms your AI assistant from "a stranger you have to re-introduce yourself to every time" into "a friend who truly knows you."

It's not a journaling app. It's not a to-do list. It's your **second brain** in the AI era:

- 📔 **Life Recorder**: Daily logs, pattern recognition, emotional tracking
- 🧭 **Personal Decision Advisor**: Scenario-based analysis using your own historical data
- 🎯 **Goal Tracker**: Record and continuously track your life goals
- 🔮 **State Predictor**: Weekly, monthly, and annual reports with data-driven forecasts

---

## Features

### Three Dimensions

**Present Dimension** — Daily Recording System
- Journal entries (zero format requirements)
- Quick capture mode (works in 2 minutes)
- AI smart responses (empathy + suggestions + pattern detection)
- Weekly review + intention setting
- Monthly summary
- Letters to your future self (time-locked)

**Past Dimension** — Life Archive System
- Timeline (year by year)
- 9 theme files: career, relationships, major decisions, health, finances, personality, habits, values, cognitive evolution
- AI-assisted memory retrieval
- Import existing content (articles, old journals, etc.)

**Future Dimension** — Decision Analysis & Prediction
- 3-layer signal system (extract → analyze → predict)
- Behavior pattern tracking
- Goal tracking (active / completed)
- Decision scenario analysis (3-scenario sandbox)
- Decision verification (check if AI's predictions were accurate)
- Weekly / monthly / annual reports

### Special Protocols

- 🆘 **Crisis Protocol**: Dedicated flow when user is in emotional distress — no analysis, just presence
- 💬 **Venting Protocol**: Listen first, then suggest, never rush to "fix"
- 📝 **Backdating Protocol**: Missed a few days? No problem, catch up gracefully
- 🔄 **Restart Protocol**: Warm re-entry after long absences
- 🎉 **Celebration Protocol**: Genuinely celebrate when goals are achieved
- 📅 **Anniversary Detection**: "One year ago today, you were dealing with..."

---

## Quick Start

### Install

**Claude Code (recommended):**
```bash
npx skills add ChenChen913/memory-system
```

**Manual install:**
```bash
git clone https://github.com/ChenChen913/memory-system.git
cp -r memory-system/ ~/.claude/skills/
```

**Other tools** → See [AGENTS.md](AGENTS.md)

### Initialize

After installing, tell your AI:
```
Initialize memory system
```

The AI will guide you through:
1. Creating the local directory structure (one command)
2. Filling in your basic profile (conversational, ~10 minutes)
3. Setting initial goals
4. Importing existing content (optional)

### Daily Usage

```
"Record today"              → Start today's journal entry
"Quick note"                → Capture a few sentences fast
"Help me analyze a decision" → Scenario sandbox for decisions
"Generate this week's report" → Weekly status summary
"What do you think of me?"  → See AI's portrait of you
```

---

## Privacy & Security

### What This Skill Does

| Action | Performed? |
|---|---|
| Write to local `/memory/` directory | ✅ Yes |
| Read local files | ✅ Only when user explicitly triggers |
| Call external APIs | ❌ No |
| Proactively send data to any server | ❌ No |
| Run autonomously without user trigger | ❌ No (autonomous_invocation: false) |

### What You Should Know

When you send journal content to the AI, that content is transmitted as conversation context to the AI platform you're using (e.g., Anthropic, Google). This is how AI tools work and is outside this Skill's control.

**Recommendations:**
- Choose AI platforms with clear data retention commitments
- Use encrypted storage for your `/memory/` directory
- Add `/memory/` to `.gitignore`
- For maximum privacy, consider using local models (Ollama, etc.)

```bash
# Quick security setup
chmod 700 ~/memory/
echo "memory/" >> .gitignore
```

---

## Multi-Tool Support

| Tool | Support Level | Notes |
|---|---|---|
| Claude Code | ⭐⭐⭐⭐⭐ | Native support, best experience |
| OpenClaw | ⭐⭐⭐⭐⭐ | Full support, local model compatible |
| Gemini CLI | ⭐⭐⭐⭐ | Works with manual trigger config |
| Cursor | ⭐⭐⭐⭐ | Via .cursorrules configuration |
| Trae | ⭐⭐⭐ | Via System Prompt |
| Codex | ⭐⭐⭐ | Via instructions file |
| Local models (Ollama, etc.) | ⭐⭐⭐⭐⭐ | Maximum privacy protection |

Full configuration guide → [AGENTS.md](AGENTS.md)

---

## File Structure

```
memory-system/
├── SKILL.md                    # Main file (AI operating spec)
├── AGENTS.md                   # Multi-tool configuration
├── README.md                   # Chinese README
├── README_EN.md                # This file
├── LICENSE
├── references/
│   ├── 00-initialization.md    # Initialization flow
│   ├── 01-present.md           # Present dimension spec
│   ├── 02-past.md              # Past dimension spec
│   ├── 03-future.md            # Future dimension spec
│   ├── 05-protocols.md         # Special scenario protocols
│   └── 06-ai-voice.md          # AI voice & persona spec
└── templates/
    ├── profile-template.md
    ├── ai-portrait-template.md
    ├── signals-log-template.md
    ├── pattern-alerts-template.md
    └── active-goals-template.md
```

---

## Publishing to skills.sh

1. Visit [skills.sh](https://skills.sh) and create an account
2. Click "Publish Skill"
3. Upload the `memory-system.skill` package file
4. Fill in Skill info: name, description, tags (journaling / productivity / personal-growth)
5. Submit for review

**Package command:**
```bash
zip -r memory-system.skill memory-system/
```

---

## Contributing

Issues and PRs welcome:
- New special scenario protocols
- Better AI response templates
- Additional tool integrations
- Privacy protection improvements

---

## License

MIT License — free to use, modify, and distribute with attribution.
