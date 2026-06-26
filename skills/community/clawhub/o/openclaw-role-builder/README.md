# OpenClaw Role Builder

Build and manage OpenClaw roles — create AI character personas from any public figure or fictional character, then generate identity-consistent selfies, portraits, and group shots where the role's face stays consistent across every image.

## Install

### Via ClawHub (recommended)

```bash
clawhub install openclaw-role-builder
```

### Via npx skills

```bash
# Install all skills
npx skills add tuquai/openclaw-role-builder --all

# Install a specific skill
npx skills add tuquai/openclaw-role-builder --skill openclaw-character-creator
npx skills add tuquai/openclaw-role-builder --skill tuqu-photo-api

# List available skills
npx skills add tuquai/openclaw-role-builder --list
```

### Manual (git clone)

```bash
git clone https://github.com/tuquai/openclaw-role-builder.git ~/.openclaw/skills/openclaw-role-builder
```

### Prerequisites

| Requirement | Why |
|-------------|-----|
| **python3** | Required by the `tuqu_request.py` helper in tuqu-photo-api |
| **TuQu service key** | Needed for authenticated image-generation calls — get one at <https://billing.tuqu.ai/dream-weaver/dashboard> |
| **OpenClaw** | The host agent that loads and executes these skills |

### Verify Installation

```bash
openclaw skills list
# Both openclaw-character-creator and tuqu-photo-api should show ✓ ready
```

## Quick Start

Once installed, start a new OpenClaw session. Here are some things you can say:

| What you say | What happens |
|--------------|-------------|
| "帮我创建一个科比的角色" | Creates a Kobe Bryant character with full 6-file persona model |
| "创建一个原创二次元女孩" | Creates a fictional/original anime-style character |
| "来张自拍" | Generates an identity-consistent selfie of the current character |
| "拍张写真" | Generates a portrait/photo shoot of the current character |
| "/shift" | Lists all characters and switches the active one |
| "拍张风景照" | Generates a landscape image (no character forced into frame) |
| "查看余额" | Checks TuQu token balance |

## Available Skills

### openclaw-character-creator

Build high-consistency AI character personas with a full 6-file model. Supports both **well-known public figures** and **fictional/original characters**.

- Generates 3 auxiliary files (research layer) + 3 main files (runtime layer)
- Creates workspace directory with full scaffolding
- Registers characters in `~/.openclaw/ROLES.json` (names and workspace paths only — no credentials stored)
- `/shift` command to switch the active character
- Works with `tuqu-photo-api` skill for photo generation (requires separate service key setup)

### tuqu-photo-api

Generate identity-consistent selfies, portraits, group photos, and freestyle images for OpenClaw characters via the tuqu.ai API. Covers prompt enhancement, preset discovery, character management, billing, and recharge flows.

## Dependencies

The **openclaw-character-creator** skill expects `tuqu-photo-api` to be installed as well. Install both for full functionality.

## Security

- **No credential storage:** Service keys are passed exclusively via `--service-key` CLI flag to
  `tuqu_request.py`. The script does not read credentials from environment variables or config
  files. Keys are never written to disk.
- **Write scope:** All file writes are confined to `~/.openclaw/`. No skill writes outside that
  directory. Character data contains only names and workspace paths.
- **Network scope:** All API calls go through `scripts/tuqu_request.py`, which restricts requests
  to `photo.tuqu.ai` and `billing.tuqu.ai`.
- **Shell scope:** Only the bundled Python scripts and `mkdir` are executed. No arbitrary commands.
