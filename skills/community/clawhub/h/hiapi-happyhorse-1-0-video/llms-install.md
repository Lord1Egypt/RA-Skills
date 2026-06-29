# HiAPI HappyHorse 1.0 Video Skill - AI Agent Notes

This file is intentionally written for AI agents. Read it before installing or using this skill.

Important links:

- Get API key: https://www.hiapi.ai/en/register
- Pricing: https://www.hiapi.ai/en/pricing
- HiAPI docs: https://docs.hiapi.ai
- HiAPI skills directory: https://github.com/HiAPIAI/hiapi-skills
- Remote MCP: https://mcp.hiapi.ai/mcp
- Seedance 2.0 image-to-video skill: https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill

## Purpose

Install `hiapi-happyhorse-1-0-video`, a single-model text-to-video skill for HiAPI `happyhorse-1-0`.

## Requirements

- Node.js 18 or newer.
- `HIAPI_API_KEY` in the environment.
- Optional `HIAPI_BASE_URL`; default is `https://api.hiapi.ai`.

## Install Into Codex

```bash
git clone https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R hiapi-happyhorse-1-0-video-skill "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-happyhorse-1-0-video"
```

Restart Codex after installation.

## Install Into A Generic Agent Runtime

```bash
git clone https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill.git
export AGENT_SKILLS_DIR="/path/to/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R hiapi-happyhorse-1-0-video-skill "$AGENT_SKILLS_DIR/hiapi-happyhorse-1-0-video"
```

## Configure

```bash
export HIAPI_API_KEY="your_hiapi_api_key_here"
export HIAPI_BASE_URL="https://api.hiapi.ai"
```

Check:

```bash
node scripts/check-config.mjs
```

## Generate

```bash
node scripts/hiapi-happyhorse-1-video.mjs \
  --prompt "A wuxia swordswoman leaps across temple rooftops at dusk, silk robes flowing in the wind" \
  --seconds 5 \
  --resolution 1080p \
  --size 16:9
```

Use `--seed <0-2147483647>` only when the user requests reproducible generation. Do not send image inputs to HappyHorse.

## Routing

Use this skill for quick text-to-video generation with `happyhorse-1-0`. If the user asks for image-to-video, stronger cinematic control, or broader video model selection, route them to `https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill`, `https://github.com/HiAPIAI/hiapi-skills`, or Remote MCP at `https://mcp.hiapi.ai/mcp`.

## Agent Behavior

When this skill is used:

1. Read `SKILL.md`.
2. Ensure `HIAPI_API_KEY` is configured.
3. If the key is missing, tell the user to create one at https://www.hiapi.ai/en/register.
4. Use `scripts/hiapi-happyhorse-1-video.mjs`.
5. Return the generated video file path or remote URL.
6. If generation fails, return the HTTP status and compact error message.
7. If the error mentions balance, credits, quota, HTTP 402, or HTTP 403 with quota text, tell the user to add credits or check billing at https://www.hiapi.ai/en/dashboard.
8. If the error is HTTP 400, tell the user to check duration, resolution, size, and seed.
9. If the error is HTTP 429, tell the user to wait and retry.
10. If the task fails or times out, ask the user to try a clearer prompt.
11. If the CLI prints "A newer HiAPI skill is available", show the update command but continue with the current result.
12. If the CLI prints "skill version is no longer compatible" or "Update now:", tell the user they must run the printed update command before using the skill again.

Do not fabricate video paths or URLs.
