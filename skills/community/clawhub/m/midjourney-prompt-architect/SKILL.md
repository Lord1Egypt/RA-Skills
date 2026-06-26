---
name: Midjourney Prompt Architect
description: Generate detailed, creative, and optimized prompts for Midjourney and other AI image generation tools (Stable Diffusion, DALL-E, Flux). Covers style specification, composition, lighting, camera parameters, and negative prompting. Use when creating image generation prompts, refining visual concepts, or building prompt templates for batch generation.
---

# Midjourney Prompt Architect

Generate production-quality prompts for AI image generation tools.

## Prompt Architecture

### Structure (in order)
```
[Subject] + [Action/Pose] + [Setting/Environment] + [Style] + [Lighting] + [Camera/Composition] + [Color Palette] + [Technical Parameters] + [Negative Prompt]
```

### Component Details

#### Subject & Action
- Be specific: "a lone astronaut floating" not "a person in space"
- Include age, clothing, expression when relevant
- Use participial phrases for dynamic poses: "reaching toward a glowing orb"

#### Setting & Environment
- Time of day, weather, season
- Specific location details: "abandoned cathedral with stained glass"
- Atmospheric elements: "mist curling between pillars"

#### Style
Reference established art movements, artists, or media:
- `oil painting in the style of J.M.W. Turner`
- `Studio Ghibli animation cel`
- `macro photograph, focus stacking`
- `Brutalist architecture, concrete, raw textures`
- `ukiyo-e woodblock print, Hokusai`

#### Lighting (critical for quality)
```
golden hour, volumetric light, rim lighting
bioluminescent glow, neon reflections on wet pavement
chiaroscuro, Rembrandt lighting
studio lighting, softbox, three-point setup
harsh midday sun, deep shadows
```

#### Camera & Composition
```
35mm lens, f/1.4, shallow depth of field
drone shot, 200m altitude, bird's eye view
Dutch angle, low angle looking up
wide-angle distortion, fisheye
tilt-shift miniature effect
```

#### Color Palette
```
monochromatic blue, desaturated
complementary orange and teal
muted earth tones, ochre and sage
high contrast, saturated primaries
pastel, soft pinks and lavenders
```

#### Midjourney Parameters
```
--ar 16:9          # aspect ratio
--s 750            # stylize (0-1000)
--c 50             # chaos (0-100)
--q 2              # quality
--v 6.1            # model version
--no text, watermark  # negative prompt
--tile             # seamless tile
--iw 2.0           # image weight (for image refs)
```

## Workflow

### 1. Understand the Vision
Ask clarifying questions if the request is vague:
- What mood or emotion?
- Any reference images or artists?
- Realistic, stylized, or abstract?
- Intended use (print, social, web, concept art)?

### 2. Draft → Refine → Test Cycle
1. Write initial prompt from the architecture above
2. Evaluate against common failure modes (see below)
3. Add Midjourney-specific parameters
4. Provide 3-4 variations with different creative directions
5. Suggest negative prompts to avoid common artifacts

### 3. Batch Generation Template
For repeated themes, create a parameterized template:
```
[SUBJECT] in [STYLE], [SETTING], [LIGHTING], [CAMERA], --ar [RATIO] --s [STYLE_VAL] --v 6.1 --no [NEGATIVES]
```

## Common Failure Modes & Fixes

| Problem | Fix |
|---------|-----|
| Text appears in image | Add `--no text, letters, typography, watermark` |
 Faces look distorted | Reduce `--s`, add `detailed face, symmetrical` |
 Multiple subjects merge | Specify `two separate figures, clear spacing` |
 Too busy/cluttered | Reduce subject count, add `minimalist, clean composition` |
 Looks like AI art | Reference specific artist/medium, avoid `AI art, digital illustration` |
 Inconsistent style across batch | Fix seed with `--seed [value]`, keep parameters identical |
 Watermarks | Add `--no watermark, logo, signature` |

## Prompt Examples

### Cinematic Portrait
```
A weathered fisherman standing on a wooden pier at dawn, face illuminated by warm golden light, salt-crusted beard, holding a hand-woven net, calm sea reflecting orange sky, shot on Hasselblad 500C, 80mm lens, f/2.8, shallow depth of field, Kodak Portra 400 film emulation --ar 4:5 --s 800 --v 6.1
```

### Architectural Concept
```
Futuristic brutalist library built into a cliffside, cantilevered concrete shelves overflowing with books, floor-to-ceiling glass overlooking a fjord, moss growing between cracks, dappled light filtering through geometric skylights, architectural photography, wide-angle lens, blue hour lighting --ar 21:9 --s 600 --v 6.1 --no people, cars, modern signage
```

### Fantasy Illustration
```
A tiny fox spirit with iridescent fur sitting on a crescent moon, reading a scroll that unfolds into a river of stars, surrounded by floating lanterns, Japanese ink painting meets Art Nouveau, gold leaf accents on deep indigo background --ar 1:1 --s 900 --c 30 --v 6.1
```

## Style Quick Reference

| Want This | Use This |
|-----------|----------|
| Photorealistic | `photograph, shot on [camera], [film stock], f/[aperture]` |
| Oil painting | `oil painting, impasto technique, visible brushstrokes` |
| Watercolor | `watercolor wash, wet-on-wet, soft edges, paper texture` |
| 3D render | `3D render, Unreal Engine 5, octane render, ray tracing` |
| Pencil sketch | `graphite pencil sketch, cross-hatching, on textured paper` |
| Pixel art | `16-bit pixel art, limited color palette, retro game aesthetic` |
| Anime | `anime style, cel shading, clean lineart, vibrant colors` |

## Cross-Tool Compatibility

These prompts work with minor adjustments:
- **Stable Diffusion**: Remove `--` parameters, add to negative prompt box
- **DALL-E 3**: Use natural language, drop camera specs
- **Flux**: Keep descriptive, reduce technical jargon
