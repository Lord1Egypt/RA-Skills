---
name: image-create
description: Generate images from text prompts and iterate on style/composition for posters, thumbnails, product mockups, logos, concept art, and social visuals. Use when the user asks to create a new image, restyle an image idea, produce prompt variants, or refine outputs with constraints like aspect ratio, mood, color palette, and text placement.
---

# Image Create

## Quick workflow

1. Confirm goal in one line (what image should achieve).
2. Collect minimum constraints:
   - subject
   - style
   - aspect ratio / resolution
   - must-include elements
   - must-avoid elements
3. Produce 3 prompt variants:
   - safe/default
   - bold/creative
   - minimal/clean
4. Generate image(s) with the selected variant.
5. Iterate with precise edits (lighting, framing, typography, colors, detail level).

## Prompt template

Use this template and fill all placeholders:

```text
[TYPE OF IMAGE], featuring [MAIN SUBJECT], in [STYLE],
composition: [CAMERA/FRAMING], lighting: [LIGHTING],
background: [BACKGROUND], color palette: [COLORS],
mood: [MOOD], quality: high detail, clean edges,
output: [ASPECT RATIO OR SIZE].

Avoid: [NEGATIVE CONSTRAINTS]
```

## Fast defaults

- If user gives little detail, default to:
  - style: photorealistic (real camera look, natural skin texture, true-to-life materials)
  - lighting: soft natural light
  - composition: centered medium shot
  - lens/camera feel: 50mm, shallow depth of field, realistic dynamic range
  - avoid: CGI/plastic look, over-smoothing, blur, watermark, extra limbs, unreadable text, distorted faces
- If text appears in image, keep wording short and ask for exact spelling.

## Realistic style tuning

Use these additions whenever the user asks for realistic output:

- Add quality cues: `photorealistic, natural textures, physically plausible lighting, realistic shadows`.
- Add camera cues: `shot on full-frame camera, 50mm lens` (or 85mm for portraits).
- Keep color grading subtle; avoid neon oversaturation unless requested.
- Prefer environmental detail that supports realism (imperfections, material grain, natural reflections).

## Iteration rules

- Change one major variable per iteration when debugging quality.
- Keep successful parts of previous prompt; only patch weak parts.
- For brand visuals, preserve palette and typography constraints across iterations.
- For thumbnails/posters, prioritize readability and high contrast.

## Output format

When helping with generation requests, return:

1. **Primary prompt**
2. **2 alternatives**
3. **Negative prompt**
4. **Suggested settings** (aspect ratio, style strength, number of outputs)
5. **One-line revision plan** for next iteration
