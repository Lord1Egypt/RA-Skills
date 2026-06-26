# Platform Syntax Reference

## Midjourney

### Basic Syntax
```
/imagine prompt: [full description]
```

### Parameters
| Flag | Meaning | Example |
|------|---------|---------|
| `--ar` | Aspect ratio | `--ar 16:9`, `--ar 1:1` |
| `--v` | Version | `--v 6`, `--v 5.2` |
| `--style` | Style mode | `--style raw` |
| `--chaos` | Variation (0-100) | `--chaos 50` |
| `--seed` | Reproducibility | `--seed 12345` |
| `--s` | Stylize | `--s 250` |
| `--no` | Negative | `--no text, watermark` |
| `--iw` | Image weight | `--iw 0.5` |
| `--tile` | Tileable | `--tile` |
| `--cref` | Character reference | `--cref [url]` |
| `--sref` | Style reference | `--sref [url]` |

### Weighted Emphasis
```
 Subject ::weight   → higher weight = more emphasis
 (Subject)          → grouping
 Subject::0.5       → lower weight
```

### Useful Shortcuts
```
--q  → quality (1 or 2)
--w  → weirdness
--e  → explore (variation)
--re  → remix mode
```

## DALL-E

### Natural Language Optimization
- Write conversationally but precisely
- Specify exact colors, materials, textures
- Mention style混合: "in the style of X mixed with Y"
- Be explicit about composition

### Examples
```
"A professional product photograph of a minimalist watch on a marble 
surface, soft side lighting from the left, shallow depth of field 
with the watch in sharp focus and the background softly blurred, 
clean white backdrop fading to light gray, commercial photography 
style reminiscent of Apple product shots"

"An elderly man sitting on a wooden bench in a park, warm autumn 
light filtering through golden leaves, candid documentary style, 
slight motion blur on the leaves, Kodak Portra 400 film look, 
shallow depth of field, gentle smile, weathered hands"
```

## Stable Diffusion

### Prompt Syntax
```
[positive prompt], [more details], [lighting], [style]
Negative prompt: [unwanted elements]
```

### Weighting
```
(cat)              → weight 1.1
((cat))            → weight 1.21
(cat:1.5)         → explicit weight 1.5
[cat]             → weight 0.9
```

### LoRA
```
<lora:model_name:weight>  → LoRA model引用
<lora:lora_name:0.5>      → 50% strength
```

### Embeddings
```
bidish:0.7             → embedding reference
easynegative           → common negative embedding
```

### ControlNet
```
--controlnet model     → depth, canny, pose, etc.
--controlnet weight    → 0-2 range
--controlnet guidance  → guidance strength
```

## Flux

### Best Practices
- Detailed natural language descriptions
- Photorealistic is default strength
- Less jargon needed than Midjourney
- Still specify: subject, lighting, style, mood
- Use "photorealistic" explicitly if that's the goal

### Example
```
"A close-up portrait of a young woman with freckles and green eyes, 
natural makeup highlighting her features, soft window light from the 
right creating gentle shadows, shallow depth of field, skin texture 
visible and detailed, magazine editorial quality, neutral gray background, 
commercial beauty photography style, 85mm f/1.4"
```

## Common Parameters Across Platforms

| Feature | Midjourney | Stable Diffusion | DALL-E | Flux |
|---------|-----------|-----------------|--------|------|
| Aspect ratio | `--ar` | `--W --H` or aspect ratio | Auto | Auto |
| Negative prompt | `--no` | Neg prompt field | Limited | Limited |
| Seed | `--seed` | `--seed` | No | No |
| Style | `--style` | Prompt terms | Style terms | Natural lang |
| Quality | `--q` | `--quality` | Auto | Auto |
| Version | `--v` | Model version | Auto | Auto |

## Quick Reference Cheat Sheet

```
Midjourney:  "subject, details, lighting, style --ar 16:9 --v 6 --style raw --no text"
DALL-E:      "Natural language description of subject, style, mood, lighting"
SD:          "subject, lighting, camera settings, style, (negative: elements)"
Flux:        "Detailed description of subject, environment, lighting, style, mood"
```
