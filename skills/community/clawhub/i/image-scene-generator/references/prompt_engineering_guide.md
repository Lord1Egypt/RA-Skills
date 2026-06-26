# Prompt Engineering Guide — Product Scene Photography

A reference for material keywords, lighting vocabulary, and platform-specific conventions used in product scene generation prompts.

## Table of Contents

1. [Material Keyword Library](#material-keyword-library)
2. [Lighting Vocabulary](#lighting-vocabulary)
3. [Camera & Composition Terms](#camera--composition-terms)
4. [Color Temperature Reference](#color-temperature-reference)
5. [Platform Aspect Ratio Table](#platform-aspect-ratio-table)
6. [Prompt Structure Patterns](#prompt-structure-patterns)
7. [Common Failure Modes & Fixes](#common-failure-modes--fixes)
8. [Negative Prompt Library](#negative-prompt-library)

---

## Material Keyword Library

### Glass & Transparent Materials
- **Clear glass**: transparent, light refraction, caustics, crystal clear
- **Frosted glass**: semi-translucent, diffused light transmission, soft glow, etched surface
- **Amber glass**: warm-toned transparency, honey-colored light refraction
- **Colored glass**: [color] tinted transparency, stained glass effect

### Metals
- **Brushed aluminum**: fine linear texture, subtle directional reflection, anodized surface
- **Polished stainless steel**: mirror-like reflection, high specular highlights, chrome finish
- **Matte black metal**: non-reflective dark surface, soft light absorption, powder-coated
- **Rose gold**: warm pink-copper metallic sheen, soft reflection
- **Brass / antique brass**: warm gold tone, patina, aged character, oxidized highlights

### Wood & Natural
- **Raw wood**: visible grain, natural knots, unfinished texture, organic warmth
- **Walnut**: dark rich grain, warm brown, fine texture
- **Oak**: light honey tone, prominent grain, natural character
- **Bamboo**: light, tight grain, eco-natural feel
- **Cork**: porous texture, warm tan, natural imperfections

### Fabric & Soft Materials
- **Linen**: natural weave, slight wrinkle, organic texture, breathable look
- **Velvet**: deep pile, light-absorbing, rich color saturation, luxury feel
- **Cotton canvas**: sturdy weave, matte surface, casual texture
- **Knit / wool**: cable pattern, cozy texture, soft fiber detail
- **Leather**: grain texture, natural patina, stitching detail, premium feel
- **Silk / satin**: smooth, light-catching, subtle sheen, fluid drape

### Ceramic & Stone
- **Matte ceramic**: smooth non-reflective surface, chalky texture, handmade imperfections
- **Glazed ceramic**: glossy coating, depth of color, reflective surface
- **Marble**: veined pattern, cool tone, polished or honed surface
- **Terrazzo**: speckled aggregate, colorful chips, modern surface
- **Concrete**: raw, industrial, grey tones, porous texture

### Plastic & Synthetic
- **Matte plastic**: non-reflective, smooth, modern feel
- **Glossy plastic**: reflective surface, bright highlights, clean finish
- **Silicone**: soft-touch, slightly translucent, flexible appearance
- **Acrylic / plexiglass**: glass-like clarity, lightweight transparency

---

## Lighting Vocabulary

### Studio Lighting Setups

| Setup | Description | Best For |
|-------|-------------|----------|
| **Single key + fill** | One main directional light + softer fill on opposite side | Clean product shots, e-commerce |
| **Three-point** | Key, fill, and rim/back light | Dimensional hero shots |
| **Softbox diffused** | Large soft light source, minimal shadows | Beauty, skincare, food |
| **Ring light** | Even, shadowless front illumination | Flat lay, social content |
| **Strip light + dark** | Narrow light strips on dark background | Dramatic, premium, electronics |

### Natural Lighting Keywords

| Keyword | Effect |
|---------|--------|
| **Golden hour** | Warm (3000–3500K), low angle, long soft shadows |
| **Blue hour** | Cool (7000–9000K), diffused, moody |
| **Overcast / cloudy** | Neutral (5500–6500K), even, no harsh shadows |
| **Window light** | Directional soft light, gradient falloff, natural feel |
| **Dappled sunlight** | Broken light through leaves, organic shadow patterns |
| **Backlit / contre-jour** | Rim glow, translucent material highlight, silhouette potential |

### Light Direction Terms
- **Key light upper-left**: classic product photography default
- **Rim light**: edge highlight from behind, separates product from background
- **Under-light**: dramatic upward illumination (rarely used for products)
- **Side light**: strong dimensionality, long shadows
- **Top-down**: even illumination for flat lay

---

## Camera & Composition Terms

### Focal Length Equivalents (for prompts)

| Focal Length | Effect | Use |
|-------------|--------|-----|
| **24mm** | Wide, environmental, slight distortion | Room scenes, wide lifestyle |
| **35mm** | Natural wide, editorial feel | Lifestyle, environmental |
| **50mm** | Natural perspective, no distortion | Hero shots, eye-level |
| **85mm** | Portrait compression, beautiful bokeh | Hero detail, beauty |
| **100mm macro** | Extreme detail, very shallow DoF | Texture, macro detail |

### Depth of Field Keywords
- **f/1.4–2.0**: Extreme bokeh, single-point focus, dreamy background
- **f/2.8–4.0**: Moderate bokeh, subject isolation with readable environment
- **f/5.6–8.0**: Moderate depth, sharp across product, soft background
- **f/11–16**: Deep focus, everything sharp, architectural/flat lay

### Composition Keywords
- **Rule of thirds**: subject placed on intersection points
- **Center composition**: symmetrical, formal, impactful
- **Negative space**: large empty area for text overlay or visual breathing room
- **Leading lines**: directional elements guiding eye to product
- **Frame within frame**: environmental elements creating natural border
- **Dutch angle**: tilted frame for dynamic energy (use sparingly)

---

## Color Temperature Reference

| Description | Kelvin | Mood |
|-------------|--------|------|
| Candlelight | 1800–2200K | Intimate, warm, cozy |
| Warm tungsten | 2700–3000K | Home, comfort, traditional |
| Golden hour | 3000–3500K | Romantic, warm, inviting |
| Neutral daylight | 5000–5500K | Clean, natural, true color |
| Overcast / shade | 6000–6500K | Cool, fresh, clinical |
| Blue hour / shade | 7000–9000K | Moody, cool, dramatic |

---

## Platform Aspect Ratio Table

| Platform / Use | Aspect Ratio | Pixels (recommended) | Notes |
|---------------|-------------|---------------------|-------|
| Shopify PDP | 1:1 or 4:5 | 2048×2048 or 2048×2560 | Square is safest default |
| Amazon listing | 1:1 | 2000×2000 min | White background for main; lifestyle for secondary |
| Instagram feed | 1:1 or 4:5 | 1080×1080 or 1080×1350 | 4:5 gets more screen real estate |
| Instagram Story / Reels | 9:16 | 1080×1920 | Vertical, full screen |
| Pinterest | 2:3 | 1000×1500 | Tall pins perform best |
| Facebook ad | 1:1 or 4:5 | 1080×1080 or 1080×1350 | Match Instagram for cross-posting |
| Website hero banner | 16:9 or 21:9 | 1920×1080 or 2560×1080 | Wide, landscape |
| Email header | 3:1 or 2:1 | 600×200 or 600×300 | Narrow banner |
| TikTok | 9:16 | 1080×1920 | Vertical, full screen |

### Midjourney Aspect Ratio Syntax
- `--ar 1:1` (square), `--ar 4:5` (Instagram), `--ar 16:9` (banner), `--ar 2:3` (Pinterest), `--ar 9:16` (story)

---

## Prompt Structure Patterns

### Midjourney Optimal Structure

```
[Subject description with material], [scene/environment], [lighting setup], [camera specs], [mood/style keywords], [negative conditions] --ar X:Y --style raw --v 6.1 --q 2
```

**Example:**
```
Amber glass candle jar with soy wax and cotton wick, resting on a raw oak wood table, soft window light from upper left, natural contact shadow, surrounded by dried eucalyptus branches and linen napkin, 50mm lens, f/4, shallow depth of field, cozy minimalist aesthetic, warm color palette, professional product photography --ar 4:5 --style raw --v 6.1 --q 2
```

### DALL-E 3 Optimal Structure

```
Professional product photograph of [subject with material details]. [Scene description]. [Lighting]. [Camera perspective]. [Mood]. Photorealistic, studio quality.
```

### Stable Diffusion Structure

```
Positive: [Subject], [scene], [lighting], [camera], [quality boosters: professional photography, 8k, detailed, sharp focus]
Negative: [failure modes to avoid]
```

---

## Common Failure Modes & Fixes

| Problem | Cause | Prompt Fix |
|---------|-------|------------|
| Product floating in air | No surface contact described | Add "resting on [surface], natural contact shadow" |
| Wrong proportions | No scale reference | Add nearby object with known size, state "life-sized" |
| Plastic / fake look | Missing material detail | Add specific texture keywords (grain, weave, finish) |
| Inconsistent shadows | Multiple implied lights | State single light direction explicitly |
| Overpowered by props | Props too prominent | Add "product as focal point, props in soft focus" |
| Cartoonish render | Wrong style mode | Use `--style raw` (MJ) or "photorealistic, not illustration" |
| Text on product garbled | AI text generation weakness | Avoid text on product; note "no text, no logos, no labels" if needed |
| Wrong aspect ratio | Default square used | Always specify `--ar` matching use case |

---

## Negative Prompt Library (Stable Diffusion / Flux)

### Universal Negative
```
cartoon, illustration, painting, drawing, sketch, anime, 3d render, CGI, digital art, distorted, deformed, disfigured, blurry, out of focus, low quality, low resolution, watermark, text, logo, signature, floating, levitating, unrealistic shadows, multiple light sources
```

### Product-Specific Negative
```
product label text, brand name text, warped product, stretched, squished, wrong proportions, melted, broken, damaged, dirty, stained
```

### Scene-Specific Negative
```
cluttered, messy, chaotic, oversaturated, neon colors, harsh flash, overexposed, underexposed, motion blur, chromatic aberration
```
