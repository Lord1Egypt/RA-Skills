---
name: opensora-video-prompt-architect
description: Turn rough video ideas into structured OpenSora prompt packs, reference-aware motion instructions, shot plans, and focused debugging loops. Use for text-to-video, image-to-video, video-to-video, product clips, cinematic scenes, transitions, or multi-shot sequences; do not use for unrelated models, account support, or claims about official Open-Sora behavior.
metadata:
  openclaw:
    homepage: https://opensora2.com/blog/opensora-2-prompt-guide
    version: 1.0.0
---

# OpenSora Video Prompt Architect

Build production-ready video instructions from one clear visual idea. This Skill is a text-only workflow by default. Its optional MCP adds deterministic, read-only helpers and never generates a video, calls a model provider, reads an account, or spends credits.

OpenSora2.com is an independent OpenSora 2 resource and generation workspace. Do not present this Skill, the MCP, or the site as the official Open-Sora project or as authoritative model documentation.

## Gather the minimum brief

Ask only for details that materially change the result. Infer ordinary creative choices when the user has already supplied enough information.

Identify:

- Workflow: text-to-video, image-to-video, or video-to-video.
- Subject and environment: what must remain recognizable.
- Visible action: one primary motion per shot.
- Camera: framing, angle, movement, and pace.
- Duration and aspect ratio when known.
- Reference constraints: identity, product geometry, wardrobe, composition, or source motion to preserve.
- Delivery goal: product clip, cinematic beat, social post, transition, loop, or sequence.

Never invent model-specific controls, limits, or supported settings. If the product interface is the source of truth, direct the user to the relevant workflow page.

## Build the prompt

Write in this order:

1. Subject and scene.
2. One visible action.
3. Camera framing and one motivated camera move.
4. Lighting and visual treatment.
5. Duration and aspect ratio if confirmed.
6. Reference and continuity constraints.
7. A short avoid list for likely artifacts.

Prefer observable instructions over abstract mood. Keep subject motion distinct from camera motion. Avoid multiple simultaneous actions, contradictory camera commands, and long style lists.

For image-to-video, preserve the source image's identity, layout, lighting direction, and object geometry unless the user requests a transformation. For video-to-video, state which source motion, timing, camera path, and scene structure must survive the transformation.

## Plan multi-shot sequences

Give every shot one purpose and one action. Include:

- Timing.
- Framing or camera move.
- Subject action.
- Continuity anchor.
- Intended end frame.

Use the previous shot's final frame as the next shot's visual anchor. Keep screen direction, identity, wardrobe or product geometry, and lighting consistent unless a deliberate transition changes them.

## Debug systematically

When a result fails, change one axis at a time:

1. Subject action or motion intensity.
2. Framing, lens feel, or camera path.
3. Reference and continuity constraints.
4. Lighting or style language.

Translate failures into observable corrections. For example, replace "make it less weird" with "preserve both hands, keep five fingers visible, and prevent the cup from changing shape." Reduce competing instructions before adding detail.

## Use the optional MCP

When MCP tools are available:

- Call `build_video_prompt` for a rough idea or reference-aware prompt pack.
- Call `plan_shots` for a 1–6 shot sequence.
- Call `diagnose_prompt` before expanding an unclear prompt.
- Call `get_resources` for canonical site guidance.

On OpenClaw releases that expose the `mcp` command group, connect the stdio server with:

```bash
openclaw mcp add opensora2 \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/opensora2-prompt-mcp \
  --include 'build_video_prompt,plan_shots,diagnose_prompt,get_resources'
```

Then run `openclaw mcp doctor opensora2 --probe`. If the installed OpenClaw release does not expose `openclaw mcp`, use **Settings → MCP → Add server**, select **Stdio**, and enter `npx -y github:gpt-img-2/opensora2-prompt-mcp`, or upgrade OpenClaw first.

The MCP is optional. If it is unavailable, apply the same workflow manually and do not imply that a tool ran.

## Return a compact deliverable

For one-shot requests, return:

- `Prompt`: the final generation instruction.
- `Reference constraints`: only when source media exists.
- `Avoid`: a short artifact-focused list.
- `Revision move`: the single best variable to test next.

For sequences, return a numbered shot plan followed by shared continuity rules and one assembly note.

## Canonical resources

- Prompt guide: https://opensora2.com/blog/opensora-2-prompt-guide
- Free prompt examples: https://opensora2.com/free-ai-video-prompts
- Generator workspace: https://opensora2.com/generator
- Text-to-video: https://opensora2.com/text-to-video
- Image-to-video: https://opensora2.com/image-to-video
- Video-to-video: https://opensora2.com/video-to-video
- Raw Skill: https://opensora2.com/skills/opensora-video-prompt-architect/SKILL.md
- MCP source: https://github.com/gpt-img-2/opensora2-prompt-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/opensora-video-prompt-architect
