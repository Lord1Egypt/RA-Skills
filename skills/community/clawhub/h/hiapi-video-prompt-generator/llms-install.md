# HiAPI Video Prompt Generator Skill — AI Agent Notes

This file is written for AI agents. Read it before installing or using this skill.

Important links:

- HiAPI Seedance 2.0 video skill: https://github.com/HiAPIAI/hiapi-seedance-2-0-video-skill
- HiAPI HappyHorse 1.0 video skill: https://github.com/HiAPIAI/hiapi-happyhorse-1-0-video-skill
- Get API key: https://www.hiapi.ai/en/register
- Pricing: https://www.hiapi.ai/en/pricing
- HiAPI docs: https://docs.hiapi.ai
- HiAPI skills directory: https://github.com/HiAPIAI/hiapi-skills
- Remote MCP: https://mcp.hiapi.ai/mcp

## Purpose

Install `hiapi-video-prompt-generator`, a prompt-engineering skill that turns briefs, links, and research topics into directed video prompts ready for HiAPI Seedance 2.0 or HappyHorse 1.0.

This skill does **not** call any video API. It produces prompts. A separate HiAPI video skill renders them.

## Requirements

- No API key is required to use this skill itself.
- To run the directed prompt afterward, the target HiAPI video skill must be installed and `HIAPI_API_KEY` must be set in its environment.

## Install Into Codex

```bash
git clone https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R hiapi-video-prompt-generator "${CODEX_HOME:-$HOME/.codex}/skills/hiapi-video-prompt-generator"
```

Restart Codex after installation.

## Install Into A Generic Agent Runtime

```bash
git clone https://github.com/HiAPIAI/hiapi-video-prompt-generator-skill.git
export AGENT_SKILLS_DIR="/path/to/agent/skills"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R hiapi-video-prompt-generator "$AGENT_SKILLS_DIR/hiapi-video-prompt-generator"
```

## Agent Contract

When the agent invokes this skill:

1. Read `SKILL.md`.
2. Read `references/source-extraction.md` if the user supplied a link, document, or topic.
3. Read `references/prompt-patterns.md` to choose a pattern that matches the request type.
4. Read `references/hiapi-handoff.md` to pick the target HiAPI skill and fill the handoff command.
5. Return the 13 sections defined in `SKILL.md`'s Output Contract, in order, in the user's language.
6. Constrain parameters to the chosen target model:
   - **Seedance 2.0**: `--seconds` is any integer from `4` to `15`, `--resolution` ∈ {`480p`,`720p`,`1080p`}, `--ratio` ∈ {`16:9`,`9:16`,`1:1`,`4:3`,`3:4`,`21:9`,`adaptive`}. Media modes are mutually exclusive: first-frame, first+last-frame, or multimodal references. Reference images plus frame images <= 9; reference video/audio each <= 3 clips, each 2-15 s and total <= 15 s.
   - **HappyHorse 1.0**: `--seconds` is any integer from `3` to `15`, `--resolution` ∈ {`720p`,`1080p`} (no `480p`), `--size` ∈ {`16:9`,`9:16`,`1:1`,`4:3`,`3:4`} (no `21:9`), optional `--seed` is 0-2147483647. Text-to-video only.
7. If the user requests an unsupported value, return the closest supported value and note the change.
8. Tag only **staging choices** (camera, layout, lighting, generic visual treatment) as `[creative assumption]`. Never tag an invented fact, metric, or UI label that way.
9. Do not invent product facts, metrics, UI labels, commands, testimonials, or feature claims. Creative staging text is allowed only when tagged `[creative assumption]` and listed in Required Screen Text.
10. End with the handoff: a `cd` line into the installed target skill directory, followed by the `node scripts/...` command for that skill with all parameters filled.

## Routing Rules

- If the user supplies a starting image or asks for image-to-video, set Target Model to `hiapi-seedance-2-0-video`.
- If the user asks for a fast text-to-video draft and the duration is `3` or `5`, prefer `hiapi-happyhorse-1-0-video`. If they want `4` seconds at draft speed, either nudge to `5` s on HappyHorse or switch to Seedance 2.0.
- If the user names a model, respect the name even if the default would differ.
- If the user wants a still-image starting frame, route to `hiapi-gpt-image-2-skill` first, then return for this skill pass once they have the image.

## What Not To Do

- Do not call a video API. This skill is prompt-only.
- Do not return `30`-second plans. The HiAPI video models do not support that duration.
- Do not invent product facts, metrics, UI labels, commands, testimonials, or feature claims.
- Do not emit `21:9` for HappyHorse 1.0, and do not emit `480p` for HappyHorse 1.0.
- Do not mix Seedance and HappyHorse flag names — Seedance uses `--ratio`, HappyHorse uses `--size`.
- Do not mix Seedance first/last-frame fields with multimodal reference image/video/audio fields.
- Do not return Markdown without the 13 contract sections.
