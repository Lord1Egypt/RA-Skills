---
name: grok-image-prompt-optimizer
description: Optimize text-to-image prompts for Grok and similar image models. Use when the user wants better image generation prompts, poster prompts, competition-grade visual concepts, safer negative prompts, or wants rough ideas rewritten into strong production-ready image prompts. Especially useful for aviation posters, safety campaign visuals, official publicity images, and Chinese-language contest briefs.
---

# Grok Image Prompt Optimizer

Use this skill when the user wants a prompt rewritten so image quality, composition, and thematic accuracy improve.

## Goal

Turn vague or overstuffed requests into prompts that are:
- visually focused
- easy for Grok to parse
- poster-friendly
- print-friendly
- less likely to produce clutter, cheap ad style, or incorrect details

## Core workflow

1. Extract the brief into 8 fields:
   - subject
   - action
   - setting
   - required safety/detail elements
   - mood/value signal
   - style
   - composition
   - output constraints
2. Reduce the scene to **one main visual idea**. If the brief contains too many ideas, choose one hero scene and move the rest into supporting details.
3. Rewrite into a structured prompt instead of a rambling paragraph.
4. Add a matching negative prompt.
5. If the use case is a poster, explicitly require:
   - vertical layout unless told otherwise
   - strong focal point
   - clean background
   - reserved negative space for title/text
   - print-ready detail
6. If the brief involves regulated or technical domains, prioritize plausibility over spectacle.

## Prompt structure

Default structure:

```text
[subject], [action], [setting], [key required elements], [mood / value], [visual style], [composition], [lighting / palette], [output format]
```

For Grok, prefer 1 clean prompt over multiple conflicting clauses.

## Default output format

When optimizing a prompt, output:

1. **Main prompt (CN)**
2. **Main prompt (EN)**
3. **Negative prompt**
4. **Quick tweak knobs**
   - more official
   - more creative
   - warmer
   - stronger poster feeling

## Grok-specific heuristics

- Prefer **clear nouns and visible actions** over abstract slogans.
- Keep **1–3 human subjects** unless the user explicitly wants a crowd.
- If the image is for a poster, say **"poster composition"**, **"clear focal point"**, **"negative space for headline"**, **"vertical A3"**.
- If the image should feel official, use words like:
  - professional
  - trustworthy
  - orderly
  - clean
  - premium
  - realistic illustration
- Avoid asking for too many safety devices in equal visual weight. Choose one primary action and let the rest support it.
- If the user says results feel generic, strengthen:
  - camera angle
  - lighting
  - focal hierarchy
  - signature scene detail
  - emotional tone
- If the model keeps making commercial-ad images, add:
  - public service poster
  - official campaign visual
  - not commercial advertising
  - restrained design
- If the model keeps making messy scenes, add:
  - minimal clutter
  - clean cabin background
  - strong central composition
  - limited supporting elements

## Technical-domain guardrails

For aviation, transport, healthcare, industrial safety, or emergency imagery:
- keep actions believable
- keep equipment recognizable
- avoid sci-fi styling unless requested
- avoid disaster-movie panic unless requested
- avoid sexualized uniforms or fashion-shoot styling
- avoid impossible cabin layouts

## Aviation / cabin-safety pattern

When the brief is about cabin safety posters, use this recipe:

```text
Chinese civil aviation cabin safety poster,
[1 main crew subject or 1 small crew group],
[one concrete safety action],
inside a clean modern aircraft cabin,
[1-3 supporting safety elements],
conveying professionalism, responsibility, warmth, and trust,
realistic illustration, premium official campaign poster,
clean blue-white palette with restrained safety-orange accents,
vertical A3 composition, clear focal point, reserved negative space for Chinese headline and copy, print-ready detail
```

Good primary actions:
- demonstrating seat belt use
- guiding passengers to stow baggage correctly
- pre-departure cabin safety briefing
- calm emergency procedure demonstration
- assisting compliant passengers during safety preparation

Avoid combining all of these equally in one frame.

## Contest-poster rules

If the user is entering a contest, bias toward:
- one memorable hero shot
- strong symbolic clarity
- emotionally legible values
- less stock-photo feeling
- less corporate ad feeling
- more designed poster feeling

Useful style phrases:
- competition-grade poster
- public service campaign visual
- premium realistic illustration
- editorial poster design
- cinematic but restrained lighting

## Negative prompt starter

Adapt as needed:

```text
low resolution, blurry, distorted hands, extra fingers, deformed face, messy composition, cluttered background, incorrect equipment details, incorrect cabin layout, cheap commercial advertising style, overdone sci-fi, anime style, childish cartoon style, garish colors, random text, watermark, logo errors
```

## Tuning patterns

### If result is too plain
Add:
- dramatic but restrained lighting
- stronger visual hierarchy
- competition-grade poster design
- more iconic hero composition

### If result is too busy
Add:
- simplified background
- only one main action
- minimal clutter
- fewer secondary subjects

### If result is too much like a photo
Add:
- premium realistic illustration
- poster design quality
- editorial composition

### If result is too much like an ad
Add:
- public service campaign poster
- official safety communication visual
- restrained, serious, trustworthy tone

## Response style

Be decisive. Do not dump theory unless asked.

When the user provides a brief, produce polished prompts immediately.

## Optional reference

If the task is specifically about aviation safety or official poster work, also read:
- `references/aviation-poster-patterns.md`
