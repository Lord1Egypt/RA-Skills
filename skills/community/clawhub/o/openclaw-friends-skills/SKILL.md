---
name: openclaw-friends-skill
description: 为龙虾创建角色（世界知名人物或虚拟人物），并让角色支持自拍和拍照。Create a character for OpenClaw (either a world-famous figure or a fictional character), and enable the character to take selfies and photos.
config_paths:
  - ~/.openclaw/ROLES.json
  - ~/.openclaw/workspace
  - ~/.openclaw/workspace-*
---

# OpenClaw Friends Skills

A skill collection for [OpenClaw](https://github.com/nicepkg/openclaw) that provides AI character creation and TUQU photo generation capabilities.

## Installation

Via ClawdHub (recommended):

```
clawhub install openclaw-friends-skills
```

Manual:

```
git clone https://github.com/tuquai/openclaw-friends-skills.git ~/.openclaw/skills/openclaw-friends-skills
```

## Included Skills

### openclaw-character-creator

Create and manage OpenClaw AI character personas. Supports both **well-known public figures** and **fictional/original characters**, generating a full 6-file persona model with workspace scaffolding.

See [`openclaw-character-creator/SKILL.md`](./openclaw-character-creator/SKILL.md) for full usage.

### tuqu-photo-api

Interact with the TUQU Dream Weaver photo API for AI image generation, character selfies, preset application, prompt enhancement, character management, billing, and more.

See [`tuqu-photo-api/SKILL.md`](./tuqu-photo-api/SKILL.md) for full usage.

## File System Access

This skill collection writes to the following paths:

| Skill | Path | What is stored |
|-------|------|----------------|
| openclaw-character-creator | `~/.openclaw/ROLES.json` | Character names and workspace paths (no credentials) |
| openclaw-character-creator | `~/.openclaw/workspace-*/` | Character persona files and workspace state |
| openclaw-character-creator | `~/.openclaw/workspace/` | Active character workspace (managed by `/shift`) |

**No service keys, tokens, or other credentials are persisted to disk by any script in this collection.**
TuQu service keys are only used at runtime via `--service-key` CLI flags and are never written to config files.

## Dependencies

The **openclaw-character-creator** skill expects **tuqu-photo-api** to be installed as well. Install both for full functionality.
