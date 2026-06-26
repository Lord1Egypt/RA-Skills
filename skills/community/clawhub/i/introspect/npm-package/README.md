# 🔍 @umang-boss/introspect

> Discover your developer DNA — one command installer for the Introspect skill for Claude Code.

[![npm version](https://img.shields.io/npm/v/@umang-boss/introspect.svg)](https://www.npmjs.com/package/@umang-boss/introspect)

## Install

```bash
npx @umang-boss/introspect
```

That's it. The installer will:

1. ✅ Check Python 3 is available
2. ✅ Check Claude Code (`~/.claude/`) exists
3. ✅ Copy the skill to `~/.claude/skills/introspect`
4. ✅ Track installed version for easy updates

## Commands

```bash
npx @umang-boss/introspect              # Install skill to Claude
npx @umang-boss/introspect install      # Same as above
npx @umang-boss/introspect update       # Update to latest version
npx @umang-boss/introspect check        # Check installed vs latest version
npx @umang-boss/introspect uninstall    # Remove skill from Claude
npx @umang-boss/introspect --version    # Show package version
npx @umang-boss/introspect --help       # Show all commands
```

**Tip:** Use `@latest` to ensure you always get the newest package:
```bash
npx @umang-boss/introspect@latest update
```

## After Installing

Open Claude Code and say:

```
introspect my last 7 days
```

Or be specific:

```
introspect my last 30 days, pick 20 sessions, only my-project
```

## What You Get

A personalized markdown report with:

- 🏆 **Overall Grade** (S/A/B/C/D) across 13 parameters
- 🧬 **Dreyfus Skill Ladder** — per-parameter placement from Novice → Expert
- 🎭 **Archetypes** — Primary, Secondary, and Shadow (under stress)
- 🏆 **Archetype Tier Ranking** — where your archetype sits (S/A/B/C/D tier)
- 🚀 **How to Level Up** — personalized evolution path to the next archetype tier
- 🧬 **Behavioral Patterns** — cognitive tendencies detected from your sessions
- 📈 **Session Journey Map** — how your sessions start, flow, and end
- ⏰ **Chrono Analysis** — when you're sharpest
- 🗣️ **Communication DNA** — your prompting style breakdown
- 📐 **Smart Completion Detection** — completed / paused / continued / abandoned (not just binary)
- 🌱 **Growth Tips** — actionable, personalized recommendations
- 🎲 **Fun Stats** — tokens burned, peak hours, favorite tools

## What's New in v1.1.0

- **Dreyfus Skill Model** — see your skill level per parameter (Novice → Expert)
- **Archetype Tier Ranking** — know where you stand (S-tier Sniper vs C-tier Bulldozer)
- **"How to Level Up" Section** — 75-85% personalized tips from YOUR sessions, evolution roadmap to next archetype
- **Smart Completion Detection** — sessions are now classified as completed / paused / continued / abandoned (not just "done vs abandoned")
- **`update` & `check` commands** — keep your skill up to date easily
- **Bug fixes** — project name detection now works for all systems (no more hardcoded paths)

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.10+ (no external dependencies — stdlib only)
- Some session history to analyze

## Also Available Via

- **ClawHub:** `clawhub install introspect --dir ~/.claude/skills`
- **GitHub:** `git clone https://github.com/umang-dabhi/introspect.git ~/.claude/skills/introspect`

## Privacy

- 🔒 Read-only — never modifies session data
- 🏠 Local only — nothing sent externally
- 🙈 No code in reports — analyzes patterns, not content

## License

MIT

---

*Built by [@umang-dabhi](https://github.com/umang-dabhi)*
