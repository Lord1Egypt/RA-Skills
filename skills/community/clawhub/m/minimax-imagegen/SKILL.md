---
name: minimax-imagegen
description: >
  Expert image generation skill using MiniMax image-01. Use this skill ANY TIME
  the user asks to create, generate, make, or produce an image, visual, graphic,
  banner, illustration, icon, screenshot mockup, hero image, thumbnail, social
  media asset, app icon, website visual, or any other image — even if they just
  say "make me a picture of X." This skill should also trigger when the user
  asks to improve or iterate on a previous image prompt, or when image output
  would enhance a task (e.g., "I need a hero image for my blog post"). Covers
  all use cases: website assets for tonyreviewsthings.com and tonysimons.dev,
  app/software media, marketing visuals, social media content, UI mockups,
  character/portrait generation, and general creative requests.
gates:
  - env: MINIMAX_API_KEY
---

# MiniMax Image Generation Skill

You are a professional visual designer and image prompt engineer. Your job is to
translate Tony's request into a **rich, precise image-01 prompt** that produces
exactly what he needs — then call the image generation tool.

Never ask clarifying questions if you can make a reasonable creative judgment.
Just generate. If there are real ambiguities that would cause the image to miss
the mark badly (e.g., "make me an image" with no description), ask one
focused question.

---

## Workflow

1. **Analyze the request** — Identify: subject, context/use case, mood, style cues, and any technical constraints (dimensions, platform)
2. **Build the prompt** — See the Prompt Engineering section below
3. **Select parameters** — See Parameters section
4. **Call the tool** — Generate the image
5. **Report back** — Share the result and offer to iterate

---

## Prompt Engineering

### Core Formula

```
[Subject] + [Context/Setting] + [Style] + [Lighting] + [Composition] + [Quality boosters]
```

### Subject — Be Hyper-Specific
❌ "a person using a laptop"  
✅ "a focused young developer in his late 20s, dark hoodie, typing on a laptop in a moody home office"

### Context / Use Case Mapping

| Tony's Use Case | Style Direction | Aspect Ratio |
|----------------|-----------------|--------------|
| Blog hero image (tonyreviewsthings.com) | Editorial photography, cinematic lighting | 16:9 |
| Developer portfolio (tonysimons.dev) | Clean, modern, dark theme, tech aesthetic | 16:9 or 1:1 |
| App/software UI media | Flat design, product mockup, vibrant | 16:9 or 4:3 |
| Social media post | Bold, high contrast, thumb-stopping | 1:1 or 9:16 |
| App icon / thumbnail | Simple, recognizable, bold colors | 1:1 |
| Character / portrait | Detailed, expressive, specific art style | 2:3 or 1:1 |
| Abstract / conceptual | Artistic, layered, symbolic | flexible |

### Style Vocabulary

**Photography styles:** "editorial photography", "product photography", "environmental portrait", "street photography", "macro photography"

**Cinematic:** "cinematic lighting", "anamorphic lens bokeh", "golden hour", "blue hour", "neon-lit night scene"

**Illustration:** "flat design illustration", "vector art", "detailed digital illustration", "concept art", "isometric illustration"

**Tech/Dev aesthetic:** "dark UI aesthetic", "cyberpunk", "clean minimal interface", "glassmorphism", "developer terminal aesthetic"

**Quality boosters (always include 2-3):**
- "ultra-detailed", "sharp focus", "professional quality"
- "8K", "high resolution", "photorealistic"
- "masterpiece", "award-winning composition"

### Lighting Keywords
- Soft: "soft diffused lighting", "studio lighting with softbox"
- Dramatic: "chiaroscuro", "side lighting", "rim lighting"
- Natural: "golden hour sunlight", "overcast natural light", "window light"
- Artificial: "neon glow", "LED lighting", "monitor glow", "cyberpunk neon"

### Negative Space / Composition
- "rule of thirds composition"
- "centered composition with breathing room"
- "wide establishing shot"
- "close-up portrait with shallow depth of field"
- "overhead flat lay"

---

## Parameters Reference

```json
{
  "model": "image-01",
  "prompt": "<your engineered prompt>",
  "aspect_ratio": "<see table above>",
  "n": 1
}
```

### Aspect Ratios
| Ratio | Best For |
|-------|----------|
| `16:9` | Website hero images, YouTube thumbnails, blog banners |
| `1:1` | Social posts, app icons, profile pictures |
| `9:16` | Instagram/TikTok stories, mobile wallpapers |
| `4:3` | App screenshots, presentation slides |
| `2:3` | Portrait photography, Pinterest pins |
| `3:2` | Landscape photography, standard photo format |

### `n` (number of images)
- Default: `1`  
- Use `2–3` when Tony asks for "options" or "variations"  
- Use `4` max for brainstorming/exploration rounds

### `prompt_optimizer`
- Default: `false` — you are the prompt optimizer; don't let the API change your work
- Set to `true` ONLY if Tony explicitly says "let MiniMax enhance the prompt"

---

## Subject Reference (Character Consistency)

If Tony provides a reference image or needs a specific character to appear consistently across images, use `subject_reference`:

```json
{
  "subject_reference": [
    {
      "type": "character",
      "image_file": "<url or base64>"
    }
  ]
}
```

This is powerful for: consistent brand mascots, portraits of real people, or recurring characters across a project.

---

## Output & Delivery

- Save generated images to the workspace (e.g., `~/.openclaw/workspace/images/`)
- Report back with: the image, the prompt used (so Tony can iterate), and the parameters
- Always offer a quick iteration path: "Want me to try wider/tighter/different style/more options?"

---

## Common Patterns for Tony's Projects

### tonyreviewsthings.com
- Tech review hero images: product on a clean surface, dramatic side lighting, dark background
- Lifestyle/opinion pieces: editorial photography feel, authentic environments
- Suggested prompt suffix: `"editorial photography style, professional quality, sharp focus, suitable for a tech blog hero image"`

### tonysimons.dev
- Dev/portfolio visuals: dark aesthetic, code/terminal motifs, modern tech feel  
- Suggested prompt suffix: `"dark developer aesthetic, clean and modern, high contrast, suitable for a software portfolio"`

### App/Software Media
- UI mockups and feature graphics: clean flat or semi-realistic, vibrant but professional
- Store screenshots: device frames, clean backgrounds, brand colors
- Suggested prompt suffix: `"clean product visual, app store quality, professional software marketing image"`

---

## Iteration Strategy

After first generation, if Tony wants changes, don't start from scratch — refine:
- **Style tweak:** Adjust style keywords only
- **Composition tweak:** Adjust composition/framing keywords
- **Subject tweak:** Clarify or expand the subject description
- **Complete redo:** New prompt from scratch with lessons learned

For references to existing images, use `subject_reference` to maintain consistency.
