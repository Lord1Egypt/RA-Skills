---
name: kenerateai-creative-workflow
description: Plan and review image, video, and audio generation workflows. Use for creative briefs, workflow selection, prompt design, prompt audits, reference-media checks, iteration plans, and Kenerate AI navigation; verify live model capabilities and costs before generation.
metadata:
  openclaw:
    homepage: https://kenerateai.org/workspace
    version: 1.0.0
---

# Kenerate AI Creative Workflow

Turn a creative goal into an inspectable image, video, or audio production plan. This Skill is text-only by default. Its optional MCP is deterministic and read-only: it does not call models, upload media, access accounts, consume credits, submit jobs, or promise output quality, pricing, or current availability.

## Build the brief

State the objective, audience, subject, deliverables, required formats, deadline, brand constraints, and source-media rights. Use only references that the user owns or has permission to use. Do not imitate a living artist or clone a person's face or voice without authorization.

## Choose the workflow

- Use text-to-image when the starting point is a written visual description.
- Use image-to-image for a permitted reference and a requested variation.
- Use image-to-prompt to extract editable visible details from a reference.
- Use PNG Maker for a transparent-background image when supported.
- Use text-to-video for a written scene, action, and camera plan.
- Use image-to-video to animate a permitted starting image.
- Use text-to-music for genre, mood, tempo, instrumentation, and structure.

Model support, formats, duration, resolution, and credit cost can change. Check the live studio before submission.

## Use the optional MCP

- `build_creative_brief` structures the goal, audience, subject, deliverables, constraints, and rights check.
- `choose_generation_workflow` maps the medium and available source material to a public Kenerate AI workflow.
- `audit_generation_prompt` checks concrete direction, rights, vague wording, and changing claims.
- `get_kenerateai_resources` returns canonical public Kenerate AI pages.

Connect the stdio server with:

```bash
openclaw mcp add kenerateai \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/kenerateai-creative-workflow-mcp \
  --include 'build_creative_brief,choose_generation_workflow,audit_generation_prompt,get_kenerateai_resources'
```

Then run `openclaw mcp doctor kenerateai --probe`. If the installed release lacks that command group, add `npx -y github:gpt-img-2/kenerateai-creative-workflow-mcp` as a Stdio server in MCP settings. Never imply that the MCP or Kenerate AI generated media when it did not.

## Return an actionable plan

Return `Objective`, `Audience`, `Workflow`, `Inputs`, `Prompt`, `Settings to verify`, `Rights check`, `Iteration plan`, and `Success criteria`. Change one variable per iteration so differences remain attributable.

## Canonical resources

- Workspace: https://kenerateai.org/workspace
- Agent: https://kenerateai.org/agent
- AI video: https://kenerateai.org/workspace/ai-video
- Text to video: https://kenerateai.org/workspace/text-to-video
- Image to video: https://kenerateai.org/workspace/image-to-video
- AI image: https://kenerateai.org/workspace/ai-image
- Text to image: https://kenerateai.org/workspace/text-to-image
- Image to prompt: https://kenerateai.org/workspace/image-to-prompt
- AI audio: https://kenerateai.org/workspace/ai-audio
- Text to music: https://kenerateai.org/workspace/text-to-music
- Pricing: https://kenerateai.org/pricing
- Privacy: https://kenerateai.org/privacy-policy
- Terms: https://kenerateai.org/terms-of-service
- Raw Skill: https://kenerateai.org/skills/kenerateai-creative-workflow/SKILL.md
- MCP source: https://github.com/gpt-img-2/kenerateai-creative-workflow-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/kenerateai-creative-workflow
