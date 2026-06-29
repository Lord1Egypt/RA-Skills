---
name: "imagegen"
description: "Generate or edit raster images when the task benefits from AI-created bitmap visuals such as photos, illustrations, textures, sprites, mockups, or transparent-background cutouts. Use when Codex should create a brand-new image, transform an existing image, or derive visual variants from references, and the output should be a bitmap asset rather than repo-native code or vector. Do not use when the task is better handled by editing existing SVG/vector/code-native assets, extending an established icon or logo system, or building the visual directly in HTML/CSS/canvas."
---

# Image Generation Skill

Use this skill when the user needs a bitmap image rather than repo-native code,
SVG, HTML, CSS, canvas, or an existing vector/icon system.

This public ClawHub release is instruction-only. It does not bundle executable
API helpers, dependencies, or generated assets. In Codex sessions, use the
available built-in image generation or image editing tool. In other agent
hosts, use the host's approved image-generation capability and keep the same
prompting and verification standards.

## When To Use

- Generate a new raster image: product shot, hero image, concept art, cover,
  sprite, texture, UI mockup, infographic, or educational visual.
- Edit an existing image while preserving important invariants such as identity,
  product shape, text, lighting direction, or composition.
- Derive visual variants from supplied reference images.
- Produce multiple related bitmap assets when each output has a distinct prompt
  or role.

## When Not To Use

- The requested asset should be an SVG, icon font, HTML/CSS composition, canvas
  graphic, or repo-native component.
- The repo already has an editable vector/logo/icon system that should be
  extended directly.
- The user asks for deterministic code-native output rather than generated
  imagery.

## Workflow

1. Decide intent: `generate` for a new image, `edit` for changing an existing
   image while preserving parts of it.
2. Decide whether the image is preview-only or project-bound.
3. Label every input image by role: edit target, reference image, style source,
   insert, or supporting context.
4. Normalize the prompt into a compact production spec. Preserve user
   constraints and avoid adding unrelated characters, brands, slogans, or story
   elements.
5. Use the host-provided image generation/editing tool. For distinct assets,
   make separate tool calls or jobs rather than relying on variants of one
   prompt.
6. Inspect the output for subject accuracy, composition, text rendering,
   style fit, prohibited content, and requested invariants.
7. Iterate with one targeted change when needed.
8. For project-bound assets, place the selected final artifact in the workspace
   and update consuming references. Never leave a project-referenced final image
   only in a host default output directory.
9. Report final saved path(s), whether the output is preview-only or
   project-bound, and the final prompt used.

## Transparent Or Cutout Requests

For simple opaque subjects, request a flat removable chroma-key background and
remove it locally with an approved project or host helper if available.

Prompt the source image like this:

```text
Create the requested subject on a perfectly flat solid #00ff00 chroma-key background for background removal.
The background must be one uniform color with no shadows, gradients, texture, reflections, floor plane, or lighting variation.
Keep the subject fully separated from the background with crisp edges and generous padding.
Do not use #00ff00 anywhere in the subject.
No cast shadow, no contact shadow, no reflection, no watermark, and no text unless explicitly requested.
```

Use a different key color when green appears in the subject. If the subject has
hair, smoke, glass, translucent material, soft shadow, reflection, or colors
that conflict with practical key colors, explain that true native transparency
or manual editing may be required before proceeding.

## Prompt Schema

Use only the lines that help the request:

```text
Use case: <taxonomy slug>
Asset type: <where the image will be used>
Primary request: <user's main prompt>
Input images: <Image 1: role; Image 2: role>
Scene/backdrop: <environment>
Subject: <main subject>
Style/medium: <photo, illustration, 3D render, diagram, etc.>
Composition/framing: <wide, close, top-down, centered, negative space>
Lighting/mood: <lighting and mood>
Color palette: <palette notes>
Materials/textures: <surface details>
Text (verbatim): "<exact text>"
Constraints: <must keep or must avoid>
Avoid: <negative constraints>
```

## Use-Case Slugs

Generation:

- `photorealistic-natural`
- `product-mockup`
- `ui-mockup`
- `infographic-diagram`
- `scientific-educational`
- `ads-marketing`
- `productivity-visual`
- `logo-brand`
- `illustration-story`
- `stylized-concept`
- `historical-scene`

Editing:

- `text-localization`
- `identity-preserve`
- `precise-object-edit`
- `lighting-weather`
- `background-extraction`
- `style-transfer`
- `compositing`
- `sketch-to-render`

## Prompting Rules

- Start with the visual job and intended use.
- Specify subject, scene, style, composition, lighting, and constraints.
- Quote exact text and keep it short; generated text can still need correction.
- For edits, repeat invariants plainly: what must change and what must stay
  unchanged.
- For reference images, state exactly how each reference should influence the
  output.
- Avoid fake UI evidence, fake policy proof, fake screenshots, endorsements, or
  brand marks unless the user has rights and asks for them.
- Prefer real product screenshots or rendered app state where users or reviewers
  need factual evidence.

## Reference Map

- `references/prompting.md`: shared prompting principles.
- `references/sample-prompts.md`: copy/paste prompt recipes by asset type.
