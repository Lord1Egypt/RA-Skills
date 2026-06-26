# 🔍 Introspect — Discover Your Developer DNA

> A gamified self-reflection tool that analyzes your Claude Code sessions and generates a personalized performance profile — archetypes, letter grades, behavioral patterns, and actionable growth tips.

**Not a boss tool. A self-discovery tool.** No judgment, just signal.

---

## What It Does

Introspect reads your Claude Code conversation history and creates a detailed report covering:

- 🏆 **Overall Grade** (S/A/B/C/D) across 13 parameters
- 🎭 **Developer Archetypes** — Primary, Secondary, and Shadow (stress) archetype
- 🧬 **Behavioral Patterns** — cognitive tendencies like "Mind Reader Expectation" or "Scope Creep"
- 📈 **Session Journey Map** — how your sessions start, flow, and end
- ⏰ **Chrono Analysis** — when you're sharpest (time of day, day of week)
- 🗣️ **Communication DNA** — Directive vs Collaborative vs Exploratory vs Passive
- 🔀 **Context Switching** — focus score and project fragmentation
- 🌱 **Growth Tips** — 2-3 actionable, personalized recommendations
- 🎲 **Fun Stats** — tokens burned, peak hour, favorite tools, and more

## How It Works

**Hybrid Architecture** — Python extracts data, Claude interprets it.

```
1. Python reads your ~/.claude session JSONLs
2. Extracts raw metrics + conversation snippets
3. Claude (the AI) reads the data
4. Claude THINKS about patterns & behaviors
5. Claude writes a personalized report (not a template!)
```

Every report is unique — written by Claude based on YOUR actual conversations.

## Parameters Measured

| Param | What It Measures |
|-------|-----------------|
| 🎯 Clarity | How precise and clear are your prompts? |
| 🔄 Iteration Efficiency | Back-and-forth count per task |
| 🧩 Decomposition | Do you break big tasks into pieces? |
| 🏃 Momentum | Do sessions reach resolution or trail off? |
| 🛠️ Tool Leverage | How well you use Claude's capabilities |
| 😤 Frustration Recovery | Pivot strategy or repeat same prompt? |
| 👁️ Verification | Test/verify output or blindly accept? |
| 💬 Engagement | Debate & suggest or just "ok proceed"? |
| 📊 Token Efficiency | Tokens burned vs productive output |
| 🧠 Cognitive Load | Complexity management per session |
| 🔀 Context Switching | Focused deep work or scattered? |
| 🎯 Goal Clarity | Do sessions start with clear intent? |
| 📐 Scope Discipline | Does the task stay focused or balloon? |

## Archetypes

Your report assigns you a **Primary**, **Secondary**, and **Shadow** (under stress) archetype:

| Archetype | Description |
|-----------|-------------|
| 🎯 The Sniper | Precise prompts, few iterations, surgical |
| 🚜 The Bulldozer | Brute force persistence, gets it done |
| 🧪 The Scientist | Tests, verifies, debates everything |
| 🏃 The Sprinter | Fast sessions, quick tasks, high throughput |
| 🎭 The Director | Orchestrates complex work, delegates |
| 🧘 The Philosopher | Deep discussions, thinks WITH the AI |
| ⚡ The Hacker | Rapid-fire, exec-heavy, terminal warrior |
| 🎨 The Architect | Structured, plans before executing |
| 🔥 The Phoenix | Resilient, recovers from failures |
| 🌀 The Explorer | Still finding their style |

## Installation

### Option 1: npm (one command)

```bash
npx @umang-boss/introspect
```

The installer checks prerequisites, copies the skill to `~/.claude/skills/introspect`, and you're ready to go.

**Keep it updated:**
```bash
npx @umang-boss/introspect update    # Update to latest
npx @umang-boss/introspect check     # Check installed vs latest version
```

[![npm version](https://img.shields.io/npm/v/@umang-boss/introspect.svg)](https://www.npmjs.com/package/@umang-boss/introspect)

### Option 2: ClawHub

```bash
clawhub install introspect --dir ~/.claude/skills
```

### Option 3: Git Clone

```bash
git clone https://github.com/umang-dabhi/introspect.git
cp -r introspect/SKILL.md introspect/scripts ~/.claude/skills/introspect/
```

### Option 4: Manual

1. Download/clone this repo
2. Copy `SKILL.md` and `scripts/` to `~/.claude/skills/introspect/`
3. Done!

### Verify Installation

```
~/.claude/skills/introspect/
├── SKILL.md              # Skill instructions for Claude
├── scripts/
│   └── analyze.py        # Data extraction engine
└── README.md             # This file
```

## Usage

Open Claude Code in any project and say:

```
introspect my last 7 days
```

Or be specific:

```
introspect my last 30 days, pick 20 sessions, only myproject
```

Or run the data extractor directly:

```bash
python3 ~/.claude/skills/introspect/scripts/analyze.py --days 7 --sessions 10 --project all
```

### Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--days` | 7 | Number of days to look back |
| `--sessions` | 10 | Number of sessions to analyze (max 50) |
| `--project` | all | Project filter (substring match) |
| `--output` | `~/.claude/skills/introspect/reports/` | Output directory |

## What's New in v1.1.0

- 🧬 **Dreyfus Skill Model** — per-parameter placement from Novice → Expert
- 🏆 **Archetype Tier Ranking** — S/A/B/C/D tiers for all 10 archetypes
- 🚀 **"How to Level Up" Section** — 75-85% personalized tips from YOUR sessions + evolution roadmap
- 📐 **Smart Completion Detection** — 4 categories (completed / paused / continued / abandoned) instead of binary
- 🔄 **npm update/check commands** — `npx @umang-boss/introspect update`
- 🔧 **Bug fixes** — project name detection now dynamic (works on any system)

## Requirements

- **Claude Code** (Claude CLI) installed with `~/.claude/` directory
- **Python 3.10+** (no external dependencies — stdlib only!)
- Some Claude session history to analyze

## Privacy & Safety

- 🔒 **Read-only** — never modifies your session data
- 🏠 **Local only** — nothing is sent externally
- 🙈 **No code in reports** — analyzes patterns, doesn't expose your code
- 🎯 **No judgment on content** — we analyze HOW you work, not WHAT you build
- ✍️ **No spelling/grammar judgment** — workflow analysis only

## Example Output

```
🏆 Overall Grade: A (78/100)

🎭 Primary: 🧪 The Scientist
   Secondary: 🔥 The Phoenix
   Shadow: 🚜 The Bulldozer (emerges under stress)

📊 Scorecard:
   🎯 Clarity:          B (68)
   🛠️ Tool Leverage:    S (95)
   👁️ Verification:     S (90)
   💬 Engagement:        A (82)
   ...

🌱 Growth Tips:
   1. Try breaking mega-prompts into 3 smaller asks
   2. Provide project context in your first message
   3. When stuck on retry #3, change approach entirely
```

## Contributing

Ideas, suggestions, PRs welcome! This is an open tool for the community.

## License

MIT

---

*Built with ❤️ by [@umang-dabhi](https://github.com/umang-dabhi)*
*Powered by Claude Code + ClawHub*
