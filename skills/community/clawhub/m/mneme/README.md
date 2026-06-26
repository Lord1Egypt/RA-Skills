# Mneme skill

A Claude Code / agent skill that teaches an agent to maintain persistent cross-session memory
in the **Mneme** format (`*.mneme`). See the full spec at the repo root: [../SPEC.md](../SPEC.md).

## Install

From ClawHub:
```bash
clawhub install mneme
```

Or copy this folder into your skills dir:
```bash
cp -r skill ~/.claude/skills/mneme
```
Then the agent will, when an `.mneme` file is present or you ask it to remember something
across sessions, follow the Mneme protocol: read the spine, recall by cue, write/supersede
cells, calibrate trust by `state`/`seen`, and lint with `scripts/mneme_tool.py`.

## Contents
- `SKILL.md` — the skill definition (frontmatter + agent protocol).
- `scripts/mneme_tool.py` — zero-dep tool: `spine` / `lint` / `new-id`.

## License
This repository is **Apache-2.0** (© 2026 Casper Kwok). The copy published on **ClawHub**
(`mneme`) is distributed under ClawHub's platform default **MIT-0** (no attribution
required) — that applies to the ClawHub distribution only.
