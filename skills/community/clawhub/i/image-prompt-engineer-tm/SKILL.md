---
name: image-prompt-engineer
description: "Expert photography prompt engineering skill for AI image generation. Use when: generating prompts for Midjourney/DALL-E/Stable Diffusion/Flux, creating product shots, portraits, landscapes, fashion photography, or any visual content that needs precise AI-generated imagery. Triggers on: 'write a prompt', 'AI image', 'Midjourney prompt', 'DALL-E prompt', 'generate an image of', 'product photography prompt'."
---

# Image Prompt Engineer 📷

Expert at crafting detailed, structured prompts for AI image generation tools (Midjourney, DALL-E, Stable Diffusion, Flux).

## Core Workflow

1. **Concept Intake** — Understand visual goal, platform, style, brand requirements
2. **Reference Analysis** — Lighting, composition, style elements from references
3. **Prompt Construction** — Layer: Subject → Environment → Lighting → Technical → Style
4. **Optimization** — Negative prompts, platform-specific syntax, quality enhancers
5. **Documentation** — Save successful patterns

## Prompt Structure Framework

### Layer 1: Subject
```
- Primary subject (person, object, scene)
- Details: age, ethnicity, expression, attire, textures, materials
- Interaction with environment
- Scale and proportion
```

### Layer 2: Environment
```
- Location type (studio, outdoor, urban, natural, interior)
- Environmental details (weather, time of day, textures)
- Background treatment (sharp, blurred, gradient, minimalist)
- Atmospheric conditions (fog, rain, haze, clarity)
```

### Layer 3: Lighting
```
- Light source (golden hour, overcast, softbox, neon, rim light)
- Light direction (front, side, back, Rembrandt, butterfly, split)
- Light quality (hard/soft, diffused, specular, volumetric)
- Color temperature (warm, cool, neutral, mixed)
```

### Layer 4: Technical (Photography Specs)
```
- Camera perspective (eye-level, low angle, bird's eye, worm's eye)
- Focal length effect (wide angle, telephoto compression, standard)
- Depth of field (shallow for portrait, deep for landscape)
- Exposure style (high key, low key, balanced, HDR, silhouette)
```

### Layer 5: Style
```
- Photography genre (portrait, fashion, editorial, commercial, documentary, fine art)
- Era/period (vintage, contemporary, retro, futuristic, timeless)
- Post-processing (film emulation, color grading, contrast, grain)
- Reference photographers (Annie Leibovitz, Peter Lindbergh, etc.)
```

## Genre Templates

### Portrait
```
[Subject: age, ethnicity, expression, attire] |
[Pose and body language] |
[Background treatment] |
[Lighting: key, fill, rim, hair light] |
[Camera: 85mm, f/1.4, eye-level] |
[Style: editorial/fashion/corporate/artistic] |
[Color palette and mood] |
[Reference photographer]
```

### Product Photography
```
[Product description with materials and details] |
[Surface/backdrop description] |
[Lighting: softbox positions, reflectors, gradients] |
[Camera: macro/standard, angle, distance] |
[Hero shot/lifestyle/detail/scale context] |
[Brand aesthetic alignment] |
[Post-processing: clean/moody/vibrant]
```

### Landscape
```
[Location and geological features] |
[Time of day and atmospheric conditions] |
[Weather and sky treatment] |
[Foreground, midground, background] |
[Camera: wide angle, deep focus, panoramic] |
[Light quality and direction] |
[Color palette: natural/enhanced/dramatic] |
[Style: documentary/fine art/ethereal]
```

### Fashion
```
[Model description and expression] |
[Wardrobe details and styling] |
[Hair and makeup direction] |
[Location/set design] |
[Pose: editorial/commercial/avant-garde] |
[Lighting: dramatic/soft/mixed] |
[Camera movement: static/dynamic] |
[Magazine/campaign aesthetic reference]
```

## Platform Syntax

### Midjourney
```
/imagine prompt: [subject] --ar 16:9 --v 6 --style raw --chaos 5 --seed [n]
--ar     → aspect ratio
--v      → version (5, 6, etc.)
--style  → style mode
--chaos  → variation (0-100)
--seed   → reproducibility
--no     → negative prompt
::       → weighted emphasis
```

### DALL-E
```
Natural language, conversational
Style mixing: "in the style of [X] mixed with [Y]"
Be specific about what you want
```

### Stable Diffusion
```
[subject], [details], [lighting], [style]
Negative: [unwanted elements]
(lora:model:weight) → LoRA weighting
[token:weight] → explicit weighting
```

### Flux
```
Detailed natural language descriptions
Photorealistic emphasis
Less need for photography jargon
```

## Negative Prompts (Midjourney/SD)

```
--no blurry, low quality, distorted, watermark, text, logo, noisy
(negative weighting where supported)
```

## Photography Terminology (Use Correctly)

| ❌ Vague | ✅ Technical |
|---------|-------------|
| Blurry background | Shallow depth of field, f/1.8 bokeh |
| Big picture | Wide-angle, 24mm, environmental portrait |
| Dark shadows | Deep shadows, high contrast, Rembrandt lighting |
| Nice lighting | Soft golden hour, butterfly lighting, rim light |
| Old looking | Film grain, Kodak Portra 400, faded contrast |

## Success Metrics

- Generated images match concept ≥ 90% first attempt
- Consistent results across generations
- Technical elements (lighting, DOF, composition) render accurately
- Minimal iteration needed
- Suitable for professional/commercial use

## Reference Files

- `references/platform-syntax.md` — Platform-specific syntax cheat sheet
- `references/photography-terms.md` — Correct photography terminology
- `references/lighting-patterns.md` — Lighting setups and effects
- `references/film-emulation.md` — Film stock references and looks
