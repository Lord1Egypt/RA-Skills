---
name: openclaw-role-builder
description: >-
  Build and manage OpenClaw roles — create a full AI character role from any
  public figure or fictional character, then generate identity-consistent
  selfies and photos for that role. Use when building roles (创建角色, 创建clone,
  新建人物, build a role), switching the active role (/shift, 切换角色), taking
  selfies (自拍, 写真, 发张图), group shots (合影), or any image-generation request.
  Includes two sub-skills: openclaw-character-creator (6-file persona model)
  and tuqu-photo-api (tuqu.ai image generation). Requires: python3. Also
  handles 照片, 角色出镜, 风景, and edit-only images. No credentials stored to disk.
metadata: >-
  {"openclaw":{"emoji":"🎭","requires":{"anyBins":["python3"]},"os":["linux","darwin","win32"]}}
config_paths:
  - ~/.openclaw/ROLES.json
  - ~/.openclaw/workspace
  - ~/.openclaw/workspace-*
---

# OpenClaw Role Builder

Build and manage OpenClaw roles — create AI character personas and generate identity-consistent photos — installable via ClawHub or git clone.

## What This Skill Does

| Capability | Sub-skill | Example triggers |
|------------|-----------|-----------------|
| **Character creation** — build a full 6-file persona (identity, soul, voiceprint, …) for any public figure or fictional character | `openclaw-character-creator` | 创建角色, 创建clone, 新建人物, "create a character" |
| **Character switching** — swap the active character in your workspace | `openclaw-character-creator` | /shift, 切换角色 |
| **Identity-consistent selfies & portraits** — generate images where the character's face stays consistent | `tuqu-photo-api` | 自拍, 写真, 发张图, "take a selfie" |
| **Freestyle image generation** — landscapes, objects, edits without a character in frame | `tuqu-photo-api` | 风景, 物品, 角色出镜, edit-only |
| **Prompt enhancement, presets, billing** — discover styles, improve prompts, check balance, recharge | `tuqu-photo-api` | "enhance prompt", "check balance" |

## Installation

### Via ClawHub (recommended)

```bash
clawhub install openclaw-role-builder
```

### Via npx skills

```bash
npx skills add tuquai/openclaw-role-builder --all
```

Or install individual sub-skills:

```bash
npx skills add tuquai/openclaw-role-builder --skill openclaw-character-creator
npx skills add tuquai/openclaw-role-builder --skill tuqu-photo-api
```

### Manual (git clone)

```bash
git clone https://github.com/tuquai/openclaw-role-builder.git ~/.openclaw/skills/openclaw-role-builder
```

### Prerequisites

| Requirement | Why |
|-------------|-----|
| **python3** | Required by `tuqu-photo-api` for the `tuqu_request.py` helper |
| **TuQu service key** | Needed for authenticated image-generation calls — obtain from <https://billing.tuqu.ai/dream-weaver/dashboard> |
| **OpenClaw** | The host agent that loads and executes these skills |

### Verify Installation

```bash
openclaw skills list
# Both openclaw-character-creator and tuqu-photo-api should appear
```

## Quick Start

Once installed, start a new OpenClaw session and try:

- **"帮我创建一个科比的角色"** — creates a Kobe Bryant character with full persona files
- **"来张自拍"** — generates an identity-consistent selfie of the current character
- **"/shift"** — switches to a different character in your roster
- **"拍张风景照"** — generates a landscape without forcing the character into frame

## Included Skills

### openclaw-character-creator

Build high-consistency AI character personas with a full 6-file model (3 auxiliary + 3 main). Supports both **well-known public figures** and **fictional/original characters**, with workspace scaffolding and global role registration.

See [`openclaw-character-creator/SKILL.md`](./openclaw-character-creator/SKILL.md) for full usage.

### tuqu-photo-api

Generate identity-consistent selfies, portraits, group photos, and freestyle images for OpenClaw characters via the tuqu.ai API. Covers prompt enhancement, preset discovery, character management, billing, and recharge flows.

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

## Security Boundaries

1. **Write scope:** All file writes are confined to `~/.openclaw/` (the paths listed above). No
   skill in this collection writes outside that directory.
2. **Read scope:** Skills read only their own bundled reference files (under the skill's
   `references/` directory) and character workspace files under `~/.openclaw/`. No arbitrary
   filesystem reads.
3. **Credential handling:** TuQu service keys are passed exclusively via the `--service-key` CLI
   flag to `tuqu_request.py`. The script does not read credentials from environment variables,
   config files, or any persisted store. Keys must never be written to disk.
4. **Network scope:** All outbound API calls go through `scripts/tuqu_request.py`, which restricts
   requests to the known hosts (`photo.tuqu.ai`, `billing.tuqu.ai`). No ad-hoc `curl`, `wget`, or
   other HTTP tools.
5. **Shell commands:** Only the specific bundled Python scripts and `mkdir` for workspace
   scaffolding are executed. No arbitrary shell commands.

## Dependencies

The **openclaw-character-creator** skill expects **tuqu-photo-api** to be installed as well. Install both for full functionality.
