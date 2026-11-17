# ontology-clawra Installation Guide

## Overview

| Item | Description |
|------|-------------|
| Version | v5.0.0 |
| Type | Local reasoning engine (not cross-skill scheduler) |
| Dependencies | Python 3.9+, OpenClaw |
| Network | No automatic network requests |

## Installation

```bash
# Method 1: Install via ClawHub
clawhub install ontology-clawra

# Method 2: Manual installation
git clone https://github.com/wu-xiaochen/ontology-clawra.git
```

## File Access Permissions

| Access | Path | Description |
|--------|------|-------------|
| Read | `~/.openclaw/skills/ontology-clawra/memory/` | Ontology knowledge base |
| Read | `~/.openclaw/workspace/memory/*.md` | User context |
| Write | `~/.openclaw/skills/ontology-clawra/memory/` | Learning results |

## Security Boundaries

- ✅ No automatic network requests
- ✅ No credential access
- ✅ Auto-write disabled by default
- ✅ Ontology write requires user confirmation
- ✅ No user data uploaded to any server

## Version

- SKILL.md: v5.0.0
- CHANGELOG.md: v5.0 (2026-03-25)
- GitHub: https://github.com/wu-xiaochen/ontology-clawra