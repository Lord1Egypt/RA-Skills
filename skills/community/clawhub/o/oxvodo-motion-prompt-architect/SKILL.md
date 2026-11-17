---
name: oxvodo-motion-prompt-architect
description: Turn rough creative ideas into structured English or Chinese motion prompts, reference bindings, shot sequences, and focused debugging loops. Use for text-to-video, image-to-video, reference-to-video, video-to-video, product motion, cinematic scenes, transitions, or loops; do not use for account support, live model comparisons, or claims about official provider behavior.
metadata:
  openclaw:
    homepage: https://oxvodo.com/free-ai-video-prompts
    version: 1.0.0
---

# OXVODO Motion Prompt Architect

Turn one visual idea into production-ready motion instructions. This Skill is a text-only workflow by default. Its optional MCP adds deterministic, read-only helpers and never generates media, calls a provider, reads an account, compares live prices, or spends credits.

OXVODO is an independent creative motion workspace. Do not present this Skill, the MCP, or the site as official documentation for OpenSora, Seedance, Kling, Wan, or any other provider or model.

## Gather the minimum brief

Identify only details that materially change the result:

- Workflow: text-to-video, image-to-video, reference-to-video, or video-to-video.
- Subject and environment.
- One primary visible subject action per shot.
- Camera framing, movement, and pace.
- Duration and aspect ratio when known.
- The exact role of each `@Image`, `@Video`, or `@Audio` reference.
- Identity, product geometry, composition, motion, timing, or audio that must remain stable.
- Delivery goal: product motion, cinematic beat, social clip, transition, loop, or sequence.

Never invent model-specific controls, limits, input support, prices, or availability. Use the current product interface when exact settings matter.

## Separate subject motion from camera motion

Write in this order:

1. Subject and scene.
2. One observable subject action.
3. Camera framing and one motivated camera move.
4. Lighting and visual treatment.
5. Duration and aspect ratio if confirmed.
6. Reference bindings and continuity constraints.
7. A short artifact-focused avoid list.

Subject motion describes what changes inside the scene. Camera motion describes how the viewpoint changes. Never combine competing actions or contradictory camera moves in one shot.

For image-to-video, preserve identity, layout, lighting direction, and geometry unless transformation is requested. For reference-to-video, preserve every token exactly and assign one role per reference. For video-to-video, state which source motion, timing, camera path, and scene structure must survive.

Write in the user's language unless another is requested. Never translate, renumber, or remove `@Image1`, `@Video1`, or `@Audio1`-style tokens.

## Plan sequences

Give every shot one purpose and one action. Include timing, framing, subject action, reference binding, continuity anchor, and intended end frame. Use each final frame as the next shot's visual anchor. Preserve screen direction, identity, wardrobe or product geometry, and lighting unless a deliberate transition changes them.

## Debug one axis at a time

Revise in this order:

1. Subject motion.
2. Camera motion or framing.
3. Reference bindings and continuity constraints.
4. Lighting or visual treatment.

Translate vague failures into observable corrections and remove competing instructions before adding detail.

## Use the optional MCP

- `build_motion_prompt` creates a structured prompt pack.
- `plan_reference_sequence` creates a 1–6 shot plan.
- `diagnose_media_prompt` identifies missing controls.
- `get_oxvodo_resources` returns canonical site resources.

Connect the stdio server with:

```bash
openclaw mcp add oxvodo \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/oxvodo-prompt-mcp \
  --include 'build_motion_prompt,plan_reference_sequence,diagnose_media_prompt,get_oxvodo_resources'
```

Then run `openclaw mcp doctor oxvodo --probe`. If the installed release lacks the `mcp` command group, add `npx -y github:gpt-img-2/oxvodo-prompt-mcp` as a Stdio server in MCP settings. The MCP is optional; never imply it ran when unavailable.

## Return a compact deliverable

For one shot, return `Prompt`, optional `Reference bindings`, `Continuity constraints`, `Avoid`, and one `Revision move`. For sequences, return a numbered shot plan, shared continuity rules, and one assembly note.

## Canonical resources

- Free AI video prompts: https://oxvodo.com/free-ai-video-prompts
- OpenSora 2 prompt guide: https://oxvodo.com/blog/opensora-2-prompt-guide
- OpenSora image-to-video guide: https://oxvodo.com/blog/opensora-image-to-video-guide
- Generator: https://oxvodo.com/generator
- Text-to-video: https://oxvodo.com/text-to-video
- Image-to-video: https://oxvodo.com/image-to-video
- Video-to-video: https://oxvodo.com/video-to-video
- Raw Skill: https://oxvodo.com/skills/oxvodo-motion-prompt-architect/SKILL.md
- MCP source: https://github.com/gpt-img-2/oxvodo-prompt-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/oxvodo-motion-prompt-architect
