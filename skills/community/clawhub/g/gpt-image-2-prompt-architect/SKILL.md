---
name: gpt-image-2-prompt-architect
description: Turn rough AI image ideas into structured GPT Image 2 prompt packs, reference-image edit instructions, product photo prompts, UI mockup prompts, and debugging loops. Use when the user wants better AI image prompts for ecommerce visuals, readable text, posters, social media creatives, product mockups, character sheets, storyboards, headshots, image-to-video source frames, or GPT Image 2 prompt rewriting.
metadata:
  openclaw:
    homepage: https://gptimg2.art/docs/gpt-image-2-prompt-architect
    version: 1.0.0
---

# GPT Image 2 Prompt Architect

This skill turns loose creative ideas into cleaner GPT Image 2 prompt packs with stronger subject control, composition, text rendering, reference-image handling, and revision loops.

## Canonical links

- Docs: https://gptimg2.art/docs/gpt-image-2-prompt-architect
- Demo: https://gptimg2.art/models/gpt-image-2
- Create: https://gptimg2.art/ai-image
- Prompt gallery: https://gptimg2.art/prompts/gpt-image-2
- Raw SKILL.md: https://gptimg2.art/skills/gpt-image-2-prompt-architect/SKILL.md
- Prompt guide: https://gptimg2.art/blog/gpt-image-2-prompt-guide
- Product photo prompts: https://gptimg2.art/blog/gpt-image-2-product-photo-prompts
- Image-to-video workflow: https://gptimg2.art/blog/gpt-image-2-image-to-video-workflow

## Provenance and safety

- Maintained around the public GPTImg2.art prompt workflow, prompt gallery, and documentation on `gptimg2.art`.
- Text-only skill pack.
- No helper scripts, no local binaries, no required environment variables, and no autonomous network calls.
- It guides prompt design and references public pages only.

## When to use

- The user has a rough AI image idea and wants a stronger GPT Image 2 prompt
- The user wants product photos, ecommerce listing images, lifestyle ads, packaging mockups, or detail shots
- The user needs UI mockups, posters, infographics, social media creatives, readable text, or branded layouts
- The user is editing from reference images and needs identity, product, composition, or style preservation
- The user wants source frames, character sheets, product references, or storyboard frames for image-to-video workflows
- The user has unstable image outputs and needs diagnosis plus a cleaner second-pass prompt

## When not to use

- The request is mainly about a different model or non-image workflow
- The user only wants final image generation, API integration, payment help, or account support
- The user asks for unsupported model settings, hidden system behavior, or official provider claims

## Workflow

1. Classify the request:
   - text-to-image
   - reference-image edit
   - product photo or ecommerce visual
   - UI, poster, infographic, or readable-text layout
   - image-to-video source frame or storyboard
2. Extract or ask for only the missing essentials:
   - subject or product
   - intended use
   - composition and camera/framing
   - environment or background
   - visual style and lighting
   - text that must appear exactly
   - reference-image constraints
   - aspect ratio or output format
   - hard negatives and brand safety constraints
3. Keep the first draft focused:
   - one primary subject or product
   - one clear composition rule
   - one lighting or style direction
   - one concise constraint block
4. Return a prompt pack with:
   - a brief diagnosis or strategy note
   - one primary prompt
   - 2 or 3 focused variants
   - a short avoid list
   - 3 concrete revision moves for the next round

## Prompt construction rules

- Prefer concrete visual language over broad style adjectives.
- Name the subject, product, materials, scale, framing, and lighting before adding mood.
- For product photos, preserve label readability, product geometry, material texture, and commercial usability.
- For reference-image edits, state what must remain unchanged before describing what may change.
- For readable text, quote the exact text and keep the layout simple.
- For UI mockups, describe the device, screen type, layout hierarchy, content density, and visual system.
- For image-to-video source frames, prioritize stable identity, clear silhouette, coherent lighting, and simple motion-ready composition.
- Avoid stacking many subjects, styles, camera angles, and layout goals into one prompt.
- Do not invent unsupported model settings.

## Output formats

### Text-to-image

```md
Goal:
Subject:
Composition:
Environment:
Style and lighting:
Text requirements:
Constraints:
Prompt:
```

### Reference-image edit

```md
Reference anchor:
What must stay stable:
What may change:
Edit direction:
Style and lighting:
Constraints:
Prompt:
```

### Product photo

```md
Commercial goal:
Product anchor:
Hero angle:
Background or scene:
Lighting:
Label and material rules:
Constraints:
Prompt:
```

### UI, poster, or readable-text layout

```md
Format:
Audience:
Layout hierarchy:
Exact text:
Visual system:
Constraints:
Prompt:
```

### Image-to-video source frame

```md
Video goal:
Source frame subject:
Motion-ready composition:
What must remain stable:
Lighting and style:
Constraints:
Prompt:
```

## Debugging heuristics

- If the image is visually attractive but off-brief, rewrite around the intended use first.
- If product geometry drifts, reduce scene complexity and strengthen product anchor language.
- If text is wrong, shorten the text, quote it exactly, and simplify surrounding design.
- If the subject changes identity, state preservation rules before the edit request.
- If the composition is cluttered, reduce secondary objects and specify one dominant framing.
- If the result cannot become a good video source frame, simplify pose, background, and lighting.

## Response style

- Be structured and concise.
- Prefer prompt packs over long theory.
- Offer practical variants that test one axis at a time: subject, composition, lighting, style, or constraints.
- When external examples are useful, point the user to the canonical GPTImg2.art pages listed above.
