# Recommended Model List

> This file lists recommended models for storyboard design. For actual API calls, use the `myreels-api` skill.

## Character Image Models (t2i)

Generate character reference images as a single-image turnaround sheet (front/side/back views on one canvas):

Preferred default for three-view character sheets:
- `nano-banana2` should be the first recommendation for base character turnaround generation
- Use other models as fallback or for style-specific adjustments after the base sheet is approved

| Model | Use Case | Quality |
|-------|----------|---------|
| **nano-banana2** | Character art | ⭐⭐⭐⭐⭐ |
| **nano banana pro** | Character art | ⭐⭐⭐⭐⭐ |
| **seedream 5.0** | Character art | ⭐⭐⭐⭐⭐ |
| **kling v3 image** | Character art | ⭐⭐⭐⭐⭐ |
| **kling o3 image** | Character art | ⭐⭐⭐⭐⭐ |

## Storyboard Image Models (t2i)

Generate storyboard shot images:

| Model | Use Case | Quality |
|-------|----------|---------|
| **nano-banana2** | Storyboard shots | ⭐⭐⭐⭐⭐ |
| **nano banana pro** | Storyboard shots | ⭐⭐⭐⭐⭐ |
| **seedream 5.0** | Storyboard shots | ⭐⭐⭐⭐⭐ |
| **kling v3 image** | Storyboard shots | ⭐⭐⭐⭐⭐ |
| **kling o3 image** | Storyboard shots | ⭐⭐⭐⭐⭐ |
| FLUX.1 / Relay | High-quality images | ⭐⭐⭐⭐ |
| Recolor / SuperImage | Image editing | ⭐⭐⭐⭐ |

## Video Models (i2v / t2v)

Generate video from images or text:

| Model | Type | Stability | Best For |
|-------|------|-----------|----------|
| **Kling O3** | i2v / t2v | ⭐⭐⭐⭐⭐ | General video, complex motion |
| **Kling V3** | i2v / t2v | ⭐⭐⭐⭐⭐ | General video, high quality |
| **Seedance 1.5 Pro SE** | i2v / t2v | ⭐⭐⭐⭐⭐ | High-quality short films |
| **Wan 2.6 i2v** | i2v | ⭐⭐⭐⭐ | Anime style, smooth motion |
| **Minimax Hailuo-2.3** | i2v | ⭐⭐⭐⭐ | Quick previews |

## Model Selection Guide

### By Content Type

| Content | Recommended Models |
|---------|-------------------|
| Character reference | nano-banana2, seedream 5.0, kling v3 image |
| Scene establishing | nano-banana2, seedream 5.0 |
| Action shots | kling v3/o3 image → Kling O3/V3 video |
| Dialogue scenes | seedream 5.0, kling v3 image |
| Alien/sci-fi environments | kling o3 image, seedream 5.0 |

### By Style

| Style | Image Model | Video Model |
|-------|-------------|-------------|
| Cinematic realistic | kling v3/o3 image | Kling O3 / Kling V3 |
| Anime | nano-banana2, seedream 5.0 | Wan 2.6, Kling |
| 3D cartoon | nano banana pro | Seedance, Kling |
| Quick preview | seedream 5.0 | Hailuo-2.3 |

## Difficulty-Based Model Selection

| Difficulty | Image Model | Video Model | Duration Suggestion |
|-------------|-------------|-------------|---------------------|
| 🟢 Simple | seedream 5.0 | Hailuo-2.3 | 5-10s |
| 🟡 Medium | kling v3 image | Wan 2.6 i2v | 5-10s |
| 🔴 Complex | kling o3 image | Kling O3 / Seedance | 10s+ / multiple clips |

## Prompt Engineering Notes

### For Character Images

Include in prompt:
- `one image`
- `character turnaround sheet` / `character sheet` / `model sheet`
- `three-view diagram`
- `front view` / `side view` / `back view`
- `aligned left to right`
- `exact same character shown three times`
- `full body`
- Character tags from design
- Clean background for reference
- `16:9` if you want to help the model fit three views on one sheet

For `nano-banana2`, this practical pattern is worth trying first:

```text
[SUBJECT], three-view diagram, one image, same character, white background, front view: [front details], side view: [side details], back view: [back details], high quality, 16:9
```

Notes:
- Put the layout instruction before `cinematic` or other style-heavy tags
- Mild stance language can work, but neutral standing pose is safer for approval sheets
- If the model already returns a correct three-view layout, keep the structure and only refine character details

Avoid:
- poster composition
- strong action pose
- dramatic camera
- split-scene collage
- cropped body

### For Scene Images

Include in prompt:
- Scene code reference
- Time of day / lighting
- Atmosphere tags

### For Video Models

- Motion description important for Luma-style models
- Physics interaction keywords for Runway-style models
- Use negative prompts for unwanted elements

For specific parameters, refer to myreels-api's `GET /api/v1/models/api` endpoint.
