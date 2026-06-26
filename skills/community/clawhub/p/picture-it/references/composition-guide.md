# Composition Guide

Techniques for creating professional images with picture-it, learned from real production use.

## Table of Contents

1. Typography & Font Size Calculator
2. Text Behind Subject
3. Multi-Pass Editing
4. Product Photography with Real Images
5. Magazine Covers and Posters
6. Color Grading and Post-Processing
7. Background Removal Best Practices
8. Writing Effective FAL Prompts
9. Overlay Composition with JSON

---

## 1. Typography

### When to Use Which

- **Big titles, hero text, headlines:** Use FAL via `edit` command. The model renders text naturally into the scene. Just say "very large bold" in the prompt — no pixel math needed.
- **Precise small text** (credits, URLs, badges, coverlines): Use `compose` or `text` with Satori. Run `picture-it download-fonts` first if fonts aren't installed.

### Satori Font Sizing (only applies to `compose`/`text` commands)

Images display much smaller on phones. Quick rule: **on a 1080px image, nothing under 36px is readable on a phone.**

| Platform | Image width | Scale | Min readable |
|---|---|---|---|
| Instagram | 1080px | 3× | 36px+ |
| Blog/OG | 1200px | 2× | 24px+ |
| YouTube thumb | 1280px | 6× | 80px+ |

### Typography Rules

- **Max 3 text sizes** per image — more creates noise
- **Brand name > tagline** — brand should be the largest text, not the tagline
- **Font pairing:** Use a serif + sans-serif pair or two complementary sans-serifs. Some proven combinations:

| Pair | Vibe |
|---|---|
| Playfair Display + Inter | Elegant editorial |
| DM Serif Display + Inter | Classic luxury |
| Cormorant Garamond + Montserrat | Refined modern |
| Lora + Montserrat | Warm editorial |
| Space Grotesk + Inter | Tech / SaaS |
| Poppins + Open Sans | Friendly modern |
| Work Sans + Merriweather | Professional |
| Bricolage Grotesque + Crimson Text | Creative editorial |
| Roboto + Nunito | Clean neutral |

**For FAL model text** (`edit`/`generate`): Any font works — just describe it in the prompt ("elegant serif", "bold condensed sans-serif", "thin futuristic"). The model renders it.

**For Satori text** (`compose`/`text`): picture-it bundles Inter, Space Grotesk, and DM Serif Display. Drop additional `.ttf` files into `~/.picture-it/fonts/` to use more. Run `picture-it download-fonts` to install the bundled set.

- **Contrast:** White text on light backgrounds needs a gradient overlay behind it
- **Padding:** Keep text at least 5% from canvas edges

---

## 2. Text Behind Subject

The most impactful technique for thumbnails and posters. The text appears to be part of the 3D scene, not floating on top.

**How it works:** Generate or provide a scene with a clear subject, then use `edit` to add text that the subject partially occludes.

```bash
picture-it generate --prompt "basketball player mid-jump, low angle, stadium lights" --model flux-dev --size 1280x720 -o player.png

picture-it edit -i player.png \
  --prompt "Add 'CLUTCH' in very large bold white block capital letters BEHIND the basketball player. The player's body overlaps and partially covers the letters, proving the text is behind her. Bold condensed sans-serif font. Keep everything else identical." \
  --model seedream -o thumbnail.png
```

**Key prompt patterns:**
- "Add [TEXT] BEHIND the [subject]"
- "The [subject's] body overlaps and partially covers the letters"
- "Bold condensed sans-serif font, solid [color]"
- "Keep everything else identical"

Then layer additional text ON TOP with `compose` or `text` commands for credits, subtitles, badges.

---

## 2. Multi-Pass Editing

The most powerful technique. Each pass adds one layer of complexity.

**Pattern: Generate → Edit → Post-process**

```bash
# Pass 1: Base environment
picture-it generate --prompt "dark stage with emerald spotlight, reflective floor, volumetric fog" --size 2048x1080 -o stage.png

# Pass 2: Place objects into the scene
picture-it edit -i stage.png -i logo.png \
  --prompt "Place Figure 2 as a large glowing 3D object in the center spotlight. Green energy emanates behind it." \
  --model seedream -o composed.png

# Pass 3: Add atmosphere
picture-it edit -i composed.png \
  --prompt "Add volumetric fog at ground level and more dust particles in the light beams. Keep everything else identical." \
  --model seedream -o atmospheric.png

# Pass 4: Final sizing and grading
picture-it crop -i atmospheric.png --size 1200x630 --position attention -o cropped.png
picture-it grade -i cropped.png --name cinematic -o final.png
picture-it vignette -i final.png --opacity 0.3 -o hero.png
```

Each `edit` call costs $0.04 (seedream). A 4-pass workflow is ~$0.16 total.

---

## 3. Product Photography with Real Images

When comparing real products (phones, apps, hardware), AI edit models alter details. The reliable approach:

```bash
# 1. Remove backgrounds from product photos (use bria for clean edges)
picture-it remove-bg -i product-a.png --model bria -o a-cutout.png
picture-it remove-bg -i product-b.png --model bria -o b-cutout.png

# 2. Trim whitespace (use Sharp directly or crop)
# The cutouts retain the full canvas — trim before compositing

# 3. Generate or create a background
picture-it generate --prompt "split gradient blue left to orange right, dark, premium" --size 1200x630 -o bg.png

# 4. Compose with overlays JSON
picture-it compose -i bg.png --overlays comparison.json -o result.png
```

**Why not use `edit` for products?** AI models change product details — camera bumps get modified, logos get altered, colors shift. For product blogs, `remove-bg` → `compose` preserves the original image pixel-perfectly. The only AI involvement is the background removal.

**Background removal gotcha:** Always use `--model bria`. The default birefnet leaves rectangular alpha boundaries that cause ugly box-shaped artifacts when you add glow or shadow effects. Also avoid `glow` and `shadow` overlay effects on cutout images — they blur the rectangular buffer, not the shape.

---

## 4. Magazine Covers and Posters

Two-layer approach: FAL for the hero image/scene, Satori for precise typography.

**Magazine cover:**
```bash
# 1. Generate editorial portrait
picture-it generate --prompt "sports photography, basketball player mid-action, low angle, stadium lights, dramatic" --model flux-dev --size 1080x1440 -o portrait.png

# 2. Add title BEHIND subject with FAL
picture-it edit -i portrait.png --prompt "Add 'CLUTCH' in very large bold white letters behind the player..." --model seedream -o titled.png

# 3. Add coverlines, badges, credits with Satori (pixel-perfect)
picture-it compose -i titled.png --overlays magazine-overlays.json --size 1080x1440 -o cover.png
```

**Movie poster:**
```bash
# Same pattern — generate scene, edit to add atmosphere, compose text
picture-it generate --prompt "astronaut on alien planet, black hole in sky..." --model flux-dev --size 1080x1620 -o scene.png
picture-it edit -i scene.png --prompt "Add volumetric fog, add title 'THRESHOLD'..." --model seedream -o titled.png
picture-it compose -i titled.png --overlays poster-credits.json -o poster.png
picture-it grade -i poster.png --name cinematic -o final.png
```

---

## 5. Color Grading and Post-Processing

Apply after all compositing is done. These are free (Sharp, no API calls).

| Grade | Effect | Good for |
|---|---|---|
| `cinematic` | Teal shadows, warm highlights | Movie posters, dramatic content |
| `moody` | Desaturated, crushed blacks | Dark/brooding content |
| `vibrant` | Boosted saturation | Product shots, social media |
| `clean` | Slight sharpening | Minimal, professional |
| `warm-editorial` | Golden tones | Editorial, luxury content |
| `cool-tech` | Blue shift, high contrast | Tech, SaaS content |

```bash
picture-it grade -i input.png --name cinematic -o graded.png
picture-it grain -i graded.png --intensity 0.05 -o grained.png
picture-it vignette -i grained.png --opacity 0.3 -o final.png
```

---

## 6. Background Removal Best Practices

| Model | Best for | Edge quality |
|---|---|---|
| `bria` | Product photos, clean objects | Best — tight edges |
| `birefnet` | General purpose | Good but rectangular artifacts |
| `pixelcut` | Alternative | Good |
| `rembg` | Budget option | Acceptable |

Always trim after removing background — the cutout retains the full original canvas dimensions.

---

## 7. Writing Effective FAL Prompts

**For generation (flux):**
- Be specific about lighting: "golden hour sunset from upper left", "dramatic side lighting"
- Mention camera: "shot on Hasselblad 85mm f1.8, shallow depth of field"
- Specify composition: "low angle looking up", "wide establishing shot", "extreme close-up macro"
- Include atmosphere: "volumetric fog", "dust particles in light", "lens flare"

**For editing (seedream/banana):**
- Reference figures: "Figure 1 is the background scene, Figure 2 is the logo"
- Be explicit about preservation: "Keep everything else exactly identical"
- Describe placement physically: "floating in the center spotlight", "sitting on the dark floor to the right"
- For text: "large bold [color] [style] letters BEHIND the [subject]"
- Avoid vague instructions: "make it look cool" → "add volumetric fog at ground level and golden god rays through the windows"

**Common mistakes:**
- Prompts too vague → AI makes random choices
- Not saying "keep everything else identical" → AI changes things you wanted preserved
- Using `edit` for product images → details get altered
- Not specifying font style for text → AI picks randomly

---

## 8. Overlay Composition with JSON

The `compose` command accepts a JSON array of overlay objects. Each overlay has a `type`, position, and rendering properties.

**Overlay types:** `image`, `satori-text`, `shape`, `gradient-overlay`, `watermark`

**Positioning:** Use named zones (`hero-center`, `title-area`, `top-bar`, `bottom-bar`, etc.) or raw `{x, y}` percentages.

**Depth layers:** `background` → `midground` → `foreground` → `overlay` → `frame` (composited in this order)

Example overlay for a badge + title + subtitle:
```json
[
  {
    "type": "gradient-overlay",
    "gradient": "linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.7) 100%)",
    "opacity": 1,
    "depth": "overlay"
  },
  {
    "type": "satori-text",
    "jsx": {
      "tag": "div",
      "props": {
        "style": { "display": "flex", "flexDirection": "column", "alignItems": "center", "justifyContent": "center", "width": "100%", "height": "100%" }
      },
      "children": [
        {
          "tag": "span",
          "props": { "style": { "fontSize": 48, "fontFamily": "Space Grotesk", "fontWeight": 700, "color": "white" } },
          "children": ["Title Here"]
        }
      ]
    },
    "zone": "hero-center",
    "width": 800,
    "height": 200,
    "depth": "frame"
  }
]
```

**Available fonts:** Inter (400, 600, 700), Space Grotesk (500, 700), DM Serif Display (400)

**Satori CSS subset:** flexbox, fontSize, fontFamily, fontWeight, color, backgroundColor, backgroundImage (linear-gradient), textShadow, letterSpacing, lineHeight, borderRadius, border, padding, margin, opacity, gap.

**Satori does NOT support:** display:grid, transforms, animations, box-shadow, filters.
