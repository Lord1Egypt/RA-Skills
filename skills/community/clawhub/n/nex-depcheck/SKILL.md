---
name: Nex DepCheck
description: Skill dependency checker. Scan Python skills for external dependencies. Verify stdlib-only compliance, check individual files or entire skill directories. No database needed, pure file scanner.
version: 1.0.0
metadata:
  author: Nex AI (Kevin Blancaflor)
  license: MIT-0
  website: https://nex-ai.be
  clawdbot:
    keywords:
      - dependency check
      - stdlib check
      - import scanner
      - external dependency
      - python imports
      - clean skill
      - dependency audit
      - afhankelijkheid check
      - import controle
    triggers:
      - check dependencies
      - scan for external imports
      - is this stdlib only
      - does this skill have external deps
      - check imports
      - scan skills for dependencies
      - controleer afhankelijkheden
---

# Nex DepCheck

Skill dependency checker. Scan Python skills to verify they only use stdlib and internal imports. Catch external dependencies before publishing.

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- No database needed

## Setup

```bash
bash setup.sh
```

## Commands

| Command | What it does |
|---------|-------------|
| `check` | Check one skill for external deps |
| `scan` | Scan all skills in a directory |
| `file` | Check a single Python file |
| `stdlib` | Check if a module is in Python stdlib |

## Tone Guide

**Check a skill before publishing:**
> "Does nex-timetrack have any external dependencies?"
```bash
nex-depcheck check /path/to/nex-timetrack
```

**Scan all skills at once:**
> "Check all my skills for external deps"
```bash
nex-depcheck scan /path/to/skills
```

**Check if a module is stdlib:**
> "Is pathlib part of the standard library?"
```bash
nex-depcheck stdlib pathlib
```

## Storage

No database. Pure file scanner. Reads Python files, parses imports, classifies them.

## License

MIT-0 on ClawHub (free for any use).
AGPL-3.0 on GitHub (commercial licenses via info@nex-ai.be).
