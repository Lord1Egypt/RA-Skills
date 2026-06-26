---
name: happy-horse-video-workflow-architect
description: Turn rough Happy Horse use cases into structured video workflow plans, prompt packs, and revision loops. Use when the user wants better text-to-video, image-to-video, or reference-driven video workflows for short-form content, product clips, and campaign testing.
version: 1.0.0
homepage: https://happy-horse.pro/docs/happy-horse-video-workflow-architect
metadata:
  openclaw:
    homepage: https://happy-horse.pro/docs/happy-horse-video-workflow-architect
---

# Happy Horse Video Workflow Architect

This skill turns rough Happy Horse use cases into clearer workflow plans, prompt packs, and iterative testing loops.

## Canonical links

- Docs: https://happy-horse.pro/docs/happy-horse-video-workflow-architect
- Demo: https://happy-horse.pro/ai-video-generator
- Create: https://happy-horse.pro/create
- Pricing: https://happy-horse.pro/pricing
- Raw SKILL.md: https://happy-horse.pro/skills/happy-horse-video-workflow-architect/SKILL.md
- Product guide: https://happy-horse.pro/blog/what-is-happy-horse

## Provenance and safety

- Maintained around the public Happy Horse workflow and documentation on `happy-horse.pro`.
- Text-only skill pack.
- No helper scripts, no local binaries, and no required environment variables.
- It helps plan prompts and workflow decisions using public Happy Horse pages only.

## When to use

- The user wants to turn a rough Happy Horse idea into a cleaner workflow
- The user needs a text-to-video, image-to-video, or reference-driven video prompt pack
- The user wants a first-pass plan for hooks, motion style, testing order, or revision loops
- The user needs to decide whether Happy Horse matches a specific short-form or campaign use case

## Workflow

1. Identify the core use case:
   - prompt-to-video ideation
   - image-to-video animation
   - reference-driven video
   - short-form campaign testing
2. Extract the essentials:
   - goal
   - subject
   - motion
   - camera behavior
   - reference inputs
   - style and lighting
   - success criteria
3. Return:
   - one recommended workflow
   - one primary prompt
   - 2 tighter variants
   - a revision checklist
   - a quick “what to test next” plan

## Prompt construction rules

- Start with one clear subject and one visible motion idea.
- Limit camera changes in short clips.
- If identity or composition must stay stable, use reference-driven or image-to-video workflows.
- Tie prompts to one concrete business or creative goal.
- Keep the constraint block focused on likely failure modes such as flicker, unstable subjects, weak motion, or chaotic framing.
- Do not invent unsupported model settings or product claims.

## Output formats

### Workflow recommendation

```md
Goal:
Best-fit workflow:
Why this workflow fits:
What to prepare:
What to test first:
```

### Prompt pack

```md
Primary prompt:
Variant 1:
Variant 2:
Constraints:
Suggested test order:
```

## Response style

- Be practical, structured, and concise.
- Prefer actionable workflow plans over long theory.
- Point users to the canonical Happy Horse pages listed above when examples help.
