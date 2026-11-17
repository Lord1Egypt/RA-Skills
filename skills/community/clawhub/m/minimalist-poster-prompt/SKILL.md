---
name: gc-minimal-zine-poster
description: "Generate Minimal Zine Poster — poetic paper-poster prompts and the matching generated image. Use when the user gives a theme, sentence, object, mood, article idea, photo, or content brief and wants a quiet Japanese/Korean zine-like editorial poster with large negative space, aged paper texture, experimental typography, restrained color accents, and a generated bitmap image. Also triggers on: zine poster, minimal poster, zine style, editorial poster, poetry poster, paper poster, independent zine aesthetic."
agent_created: true
---

# Minimal Zine Poster

Turn the user's content into both:

1. a final image-generation prompt, and
2. a generated raster image made from that prompt using the **ImageGen** tool.

## Mode Policy

Use **Standard Mode** for all generation. Use the Standard Mode Prompt Compiler
(see `references/visual-rules.md`) to convert the user's content into a compact,
imageable, high-fidelity prompt. If the user asks for higher quality, strengthen
the prompt using the rules in the reference file.

## Standard Mode Prompt Compiler

Default generation should compile only the parts that become pixels in the final
image prompt. The full visual rules, color engine, and prompt field definitions
live in `references/visual-rules.md` — load that file before writing any prompt.

### Key Principles (always in context)

- **Visual identity:** poetic minimal paper poster, huge negative space, old
  paper, tiny anchor, sparse type, one clear high-chroma anchor, zine/editorial
  mood.
- **Non-negotiable must-haves:** vertical 3:5 paper canvas, small cluster
  (8%-25% of canvas), scanned-paper view, old print defects, serif/typewriter
  text, and a saturated color anchor visible at thumbnail size.
- **Negative space:** 70%-90% plain paper.
- **Color:** one unmistakably high-chroma anchor per image (cobalt, ultramarine,
  cyan, violet, magenta-pink, lemon yellow, pear green, orange, or tomato red).
  The high-chroma area occupies roughly 0.8%-2.5% of the canvas or 15%-35% of
  the visual cluster.
- **Hard avoids:** full-bleed scene, commercial headline, product ad, logo/CTA,
  glossy mockup, clean UI white, cinematic lighting, 3D, neon, cute cartoon,
  fashion editorial drama, dense scrapbook, too many colors, long clean text.

### Standard Prompt Shape

Write the final Standard Mode prompt as four compact paragraphs:

1. canvas + paper + negative space + cluster size/location
2. subject metaphor + anchor type + anchor treatment
3. typography + accent strategy + print defects
4. flat scan mood + avoid-list

In paragraph 3, state the exact high-chroma hue, its material form, and its
approximate visual share. This structure is more important than reciting every
rule. Prefer a concrete, imageable prompt over a long style essay.

## Variation Engine

Before writing the prompt, choose one option from each axis. Randomness must
change visual grammar, not only position. If recent outputs used the same layout
or anchor, choose a different one.

### Layout Family

- **center-fragment:** tiny central image or object with surrounding air
- **lower-left-float:** small anchor in the lower-left quadrant, lots of empty top space
- **upper-right-block:** small color/photo block in the upper-right with loose text drift
- **dual-panel:** two small overlapping or adjacent panels with a narrow gap
- **irregular-cutout:** torn or organic paper shape carrying image or type
- **type-led:** typography is the main visual anchor, image secondary or absent
- **dot-orbit:** dots, letters, or hairline create an orbit around a small subject
- **single-specimen:** one isolated object or mark with almost no support graphics

### Image Anchor

- tiny faded photo
- torn-paper clipping
- flat silhouette
- solid color block
- old printed illustration
- object specimen
- translucent geometric overlay
- abstract texture window

### Typography Mode

- fragmented floating letters
- short phrase pressed against image edge
- archive microtext with date/weather
- diagonal scattered words
- low-contrast gray ghost text
- headline-as-object with rough letterpress
- text inside a color block or cutout
- almost textless, only a tiny caption

### Texture Mode

- xerox softness
- risograph grain
- letterpress ink bleed
- halftone degradation
- film grain photo
- scan noise and paper fibers
- aged paper mottling
- soft motion blur on selected text

### Mood Mode

- quiet
- summer
- solitude
- childhood
- seaside
- afternoon
- night
- memory
- slight surrealism

## Workflow

1. **Determine mode.** Use Standard Mode.

2. **Parse the user's content.** Identify the core subject, mood, exact text if
   supplied, possible visual metaphor, and any reference image role. For an
   article or complex idea, extract one central imageable idea rather than
   summarizing the whole argument. If no image text is supplied, invent one
   short poetic English or Chinese phrase.

3. **Load visual rules.** Read `references/visual-rules.md` to get the full
   first-principles prompt fields, standard color engine, and standard prompt
   shape details.

4. **Select a variation recipe.** Pick layout, image anchor, typography,
   texture, and mood from the Variation Engine above. Choose color through the
   Standard Color Engine (in the reference file). Do not select
   `near-monochrome` unless the user explicitly asks for it. Do not default to
   "tiny photo + blue dots + microtext" unless it truly fits. If the recipe
   becomes too dense, simplify typography or color treatment first.

5. **Write the final image prompt.** Use the Standard Mode Prompt Compiler to
   compile the user's content into the four-paragraph prompt shape: canvas,
   anchor, typography/accent/print, flat-scan mood and avoid-list. Specify
   exact in-image text only when useful. Keep it short because image models
   distort long text. Make the prompt decisive: say where the anchor sits, how
   large it is, how text behaves, what accent appears, and how the print/scan
   texture looks.

6. **Generate the image.** Use the **ImageGen** tool to generate the image.
   Before calling ImageGen, inform the user that image generation consumes
   credits (roughly 5-10 credits per image). Do not stop after prompt-only
   unless the user explicitly asks for prompt-only. If the result obviously
   violates the selected mode or recipe, tighten the prompt and regenerate
   once. Inspect the result at thumbnail scale — if the high-chroma anchor is
   absent, washed out, or reduced to an imperceptible mark, regenerate once
   with stronger color wording and a larger colored area.

7. **Return the image and prompt.** Present the generated image and the final
   prompt in the output format specified below.

### ImageGen Tool Usage

To generate the image, use ToolSearch to load the `ImageGen` tool schema, then
call it via DeferExecuteTool. Pass the compiled prompt as the `prompt`
parameter. If the user provided a reference photo and wants it incorporated,
pass it via the `image` parameter for image-to-image transformation.

## Negative Constraints

Always avoid:

- full-bleed subject or scene
- commercial poster headline hierarchy
- product ad layout, logo lockup, CTA, or brand campaign feeling
- clean digital UI background
- glossy paper mockup or heavy paper shadow
- 3D rendering, cinematic lighting, hard shadows, depth of field, neon, cyberpunk
- cute cartoon, kawaii illustration, anime poster, fashion editorial drama
- too many objects, stickers, colors, captions, or decorative textures
- high-resolution stock-photo realism
- long, clean, perfectly readable text blocks

## Output Format

After generating the image, present the result in this format:

```markdown
**生成图**

![Minimal Zine Poster](generated-image)

**最终 Prompt**

[final prompt used for image generation]

**说明**

- Mode: Standard
- Recipe: [layout / anchor / typography / accent / texture / mood]
- [one short note about the content interpretation]
```

## Quality Gate

Before finalizing, check every item:

- Did the run use the Standard Mode Prompt Compiler?
- Did the run choose a variation recipe across layout, anchor, typography, accent, texture, and mood?
- Is the structure materially different from recent visible outputs?
- Does the image remain a sparse vertical paper poster?
- Does 70%-90% of the poster read as paper?
- Is the subject cluster roughly 8%-25% of the canvas?
- Is there one clear visual metaphor rather than a whole illustrated scene?
- Does the anchor have old-photo, clipping, print, scan, or paper-specimen treatment?
- Are typography and microtext part of the composition?
- Is there only one restrained accent strategy?
- Is the high-chroma anchor clearly visible at thumbnail size?
- Does saturated color occupy about 0.8%-2.5% of the canvas or 15%-35% of the visual cluster?
- Did the prompt avoid weakening the color anchor with `pale`, `muted`, `faded`, `pastel`, `low saturation`, or `near-monochrome` wording?
- Did the prompt avoid full-bleed, commercial, 3D, neon, cinematic, cartoon, cute, brand, and generic template aesthetics?
- Was the image actually generated via ImageGen?
