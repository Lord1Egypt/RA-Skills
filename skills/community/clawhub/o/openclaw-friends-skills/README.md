# OpenClaw Friends Skills

Agent skills for [OpenClaw](https://github.com/nicepkg/openclaw) — installable via [`npx skills`](https://github.com/vercel-labs/skills).

## Install

```bash
# Install all skills
npx skills add tuquai/openclaw-friends-skills --all

# Install a specific skill
npx skills add tuquai/openclaw-friends-skills --skill openclaw-character-creator
npx skills add tuquai/openclaw-friends-skills --skill tuqu-photo-api

# List available skills
npx skills add tuquai/openclaw-friends-skills --list
```

## Available Skills

### openclaw-character-creator

Create and manage OpenClaw AI character personas. Supports both **well-known public figures** and **fictional/original characters**, generating a full 6-file persona model with workspace scaffolding.

- Generates 3 auxiliary files (research layer) + 3 main files (runtime layer)
- Creates workspace directory with full scaffolding
- Registers characters in `~/.openclaw/ROLES.json` (names and workspace paths only — no credentials stored)
- `/shift` command to switch the active character
- Works with `tuqu-photo-api` skill for photo generation (requires separate service key setup)

### tuqu-photo-api

Interact with the TUQU Dream Weaver photo API for AI image generation, character selfies, preset application, prompt enhancement, character management, billing, and more.

## Dependencies

The **openclaw-character-creator** skill expects `tuqu-photo-api` to be installed as well. Install both for full functionality.
