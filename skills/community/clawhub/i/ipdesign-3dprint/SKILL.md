---
name: IPdesign-3Dprint
title: IP Character Design → 3D Print Pipeline
description: End-to-end AI-powered pipeline for creating 3D-printable IP character figurines (Pop Mart style). Three-mode image generation: ComfyUI local (GPU), ComfyUI Cloud, or API-only (Gemini/Imagen/FLUX). Automates Blender modeling with Solidify + Subdivision + color + STL export.
version: 1.0.0
author: Approxima (via Hermes Agent)
tags: [3d-printing, blender, character-design, skullpanda, pop-mart, ip-design, procedural-modeling]
requires:
  bins: [blender, curl, python3]
---

# IPdesign-3Dprint — IP Character to 3D Print Pipeline

## Overview

Turn any text description or reference image into a 3D-printable IP character figurine. Designed for Pop Mart / Skullpanda-style collectible figures.

```
User Prompt → [Image Generation Layer] → 3-View References
                                                ↓
User Confirms? → Yes → [Blender Modeling Layer] → Solidify + Subdiv + Color
      ↕ No (adjust prompt)                             ↓
Manual Upload →                          [Export Layer] → STL / OBJ / 3MF
```

## Three Work Modes

The skill auto-detects which image generation method is available:

| Mode | Requirement | Cost |
|:---|:---|:---:|
| **A — ComfyUI Local** | NVIDIA GPU ≥6GB VRAM (local) | $0 (electricity only) |
| **B — ComfyUI Cloud** | `COMFY_CLOUD_API_KEY` | Pay-per-use (~$0.003-0.01/img) |
| **C — API-Only** ⭐ | `GEMINI_API_KEY` (or other) | Imagen 4.0 via Gemini key (free tier available) |

**Default (no GPU, no ComfyUI Cloud):** Uses Google Imagen 4.0 via `GEMINI_API_KEY`.

## Prerequisites

### Required
```bash
# Blender (any version ≥4.0)
apt-get install blender   # Linux
brew install blender      # macOS

# Verify
blender --version
```

### For Image Generation (pick one)
```bash
# Mode A: ComfyUI Local — see comfyui skill
# Mode B: ComfyUI Cloud — export COMFY_CLOUD_API_KEY

# Mode C: API-Only (recommended for no-GPU)
export GEMINI_API_KEY="your-key-here"
# Or use any of: EVOLINK_API_KEY, OPENAI_API_KEY, BFL_API_KEY
```

## Pipeline Stages

### Stage 1: Image Generation (Three-View References)

**Option A: From Prompt**
Generate three-view character concept images (front/side/back):

```bash
# Using Gemini/Imagen 4.0 (API-only mode)
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [{"prompt": "Skullpanda-style character, front view..."}],
    "parameters": {"sampleCount": 2, "aspectRatio": "1:1"}
  }'
```

**Option B: Manual Upload**
User provides front/side/back view images directly.

**Option C: User Confirmation Loop**
1. Generate → show images to user
2. User says "OK" → proceed to Stage 2
3. User says "adjust X" → modify prompt → regenerate
4. User provides own reference images → skip generation

### Stage 2: Blender Modeling

Based on the reference images, generate a Blender script that:

1. **Load references** as background planes (front/side/top)
2. **Build base geometry**:
   - Head: UV sphere → sculpt to Skullpanda proportions
   - Eye sockets: Boolean cutout (rounded triangular shape)
   - Eyes: Sclera + iris + pupil + highlight spheres
   - Cat ears: Spherical buttons (NOT pointed!)
   - Body: Short chunky cylinder (1:1 head:body ratio)
   - Arms/Legs: Short rounded cylinders
   - Tail: Curved thin tube
   - Base: Circular disc with raised rim
3. **Apply 3D printing modifiers**:
   - Solidify (1.2mm wall thickness)
   - Subdivision Surface (Catmull-Clark, level 1-2)
4. **Color/Material**:
   - Helmet: White (#F5F0EB), low roughness, slight subsurface
   - Eyeshadow: Dark charcoal (#19191E), matte
   - Eyes: Amber/brown iris with highlights
   - Bodysuit: Black (#1A1A1A), medium roughness
   - Base: Dark gray (#141414), matte
5. **Export**:
   - STL for 3D printing (manifold, watertight)
   - .blend for further editing

### Stage 3: 3D Print Preparation

```python
# Solidify — wall thickness
solidify = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
solidify.thickness = 0.12   # 1.2mm
solidify.offset = -1.0       # inward offset

# Subdivision — smooth surface
subsurf = obj.modifiers.new(name="SubSurf", type='SUBSURF')
subsurf.levels = 1
subsurf.subdivision_type = 'CATMULL_CLARK'

# Export
bpy.ops.export_mesh.stl(filepath="figure.stl", use_selection=True)
```

## Configuration

### Default Scale
```
1 Blender unit = 1 cm
Total figure height: ~10.5 cm (including base)
```

### Key Proportions (Skullpanda standard)
| Feature | Ratio |
|:---|:---:|
| Head:Total Height | ~40% |
| Head:Body | ~1:1 |
| Eye Width:Head Width | ~1:3 |
| Ear Diameter:Head Width | ~1:5 |
| Body Width:Head Width | ~0.7:1 |

## Verifying with Skullpanda

The skill includes a complete Skullpanda build script at `scripts/skullpanda_build.py`.

```bash
blender --background --python scripts/skullpanda_build.py
```

Expected output:
- `skullpanda_base_mesh.stl` (~1.6 MB, 16K verts) — 3D print ready
- `skullpanda_subdiv1.stl` (~6.5 MB, 67K verts) — smooth version
- `skullpanda_figure.blend` (~1.8 MB) — editable source

## Color Palette Reference

| Part | Hex | RGB | Roughness | Metallic |
|:---|:---:|:---:|:---:|:---:|
| Helmet | #F5F0EB | (245,240,235) | 0.35 | 0.0 |
| Eyeshadow | #19191E | (25,25,30) | 0.9 | 0.0 |
| Iris | #503C28 | (80,60,40) | 0.3 | 0.0 |
| Bodysuit | #1A1A1A | (26,26,26) | 0.6 | 0.05 |
| Base | #141414 | (20,20,20) | 0.8 | 0.0 |

## Dependencies

### Required (auto-installed by setup)
- `blender` ≥ 4.0

### Optional (for image generation)
| Variable | Provider | Get Key |
|:---|:---|:---|
| `GEMINI_API_KEY` | Google AI | https://aistudio.google.com |
| `COMFY_CLOUD_API_KEY` | Comfy Cloud | https://platform.comfy.org |
| `EVOLINK_API_KEY` | EvoLink | https://evolink.ai |

## Common Pitfalls

1. **Skullpanda ears are SPHERICAL, not pointed** — this is the most common modeling mistake
2. **Boolean eye sockets** — must be rounded triangular shape (point down)
3. **STL too large** — use Decimate modifier (ratio 0.15) to reduce face count
4. **Memory limit on VPS** — skip subdivision rendering; export base mesh STL instead
5. **Imagen 4.0 credits** — Google AI Studio free tier has usage limits; check your quota
6. **Multi-view consistency** — generate front view first, then describe for side/back views
