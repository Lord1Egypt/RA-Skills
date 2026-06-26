---
name: gif-cog
description: "AI GIF generation powered by CellCog. Reaction GIFs, product loops, cinemagraphs, social media animations. Seamless looping, platform-optimized for Discord, Twitter, Slack, WhatsApp. Created from scratch, not converted."
metadata:
  openclaw:
    emoji: "🎞️"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# GIF Cog - Every GIF Is a Different Production Challenge

**A product rotation, a reaction face, a cinemagraph, a social media animation — each needs a completely different creative pipeline.** CellCog has them all.

Most "AI GIF tools" are just video-to-GIF converters. CellCog creates GIFs from scratch — generating the visual, animating it with AI video models, optimizing the palette and file size for your target platform, and delivering both the GIF and a high-quality MP4 source. Every GIF is a custom production.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
print(result["message"])
```


---

## Why Good GIFs Are Harder Than They Look

Creating a GIF that actually looks professional involves surprising complexity:

- **Seamless loops are hard**: The first and last frame need to match perfectly, or the loop stutters
- **256-color limit**: GIFs only support 256 colors — intelligent palette selection makes the difference between crisp and muddy
- **File size constraints are brutal**: Discord caps at 8MB, WhatsApp at 6MB, email at 1MB — every frame and pixel counts
- **Different GIFs need different tools**: A product rotation needs 3D rendering, a cinemagraph needs motion isolation, a reaction GIF needs character design

CellCog deploys different tool combinations for each request — image generation, video animation, coding tools for custom effects, ffmpeg for optimization — all orchestrated by an agent that understands what your specific GIF needs.

---

## What Makes This Different

CellCog doesn't just convert video to GIF. It has access to world-class video generation models, image generation models, audio models, and a frontier coding agent — and it deploys whichever combination your specific GIF needs.

| What You Want | What CellCog Actually Does |
|--------------|---------------------------|
| Product rotation GIF | Generates the product image → animates a smooth rotation → optimizes to seamless loop → delivers platform-sized GIF |
| Cinemagraph | Generates the scene → isolates the motion element → creates subtle, infinite loop → optimizes palette |
| Reaction GIF | Designs the character → generates expressive animation → adds text overlay → loop optimization |
| UI demo GIF | Captures the interaction flow → animates transitions → crops to feature area → optimizes for embedding |

No other platform combines frontier image generation + video animation + coding tools + intelligent GIF optimization in a single request.

---

## What GIFs You Can Create

### Reaction GIFs

Custom reactions that don't exist yet:

- **Custom Expressions**: "Create a reaction GIF of a cartoon cat doing a slow clap"
- **Meme Reactions**: "Make a 'this is fine' style reaction GIF with a robot at a computer"
- **Emotion GIFs**: "Create a GIF of a character going from confused to enlightened — lightbulb moment"
- **Text Reactions**: "Make a GIF with animated text that says 'NAILED IT' with confetti"

**Example prompt:**
> "Create a reaction GIF for Slack:
> 
> Concept: A cute penguin character giving a standing ovation
> Style: Kawaii, simple, clean lines
> Loop: Seamless — penguin claps continuously
> Duration: 2 seconds
> 
> Optimize for Slack (under 20MB, 128×128 works best for emoji).
> Also give me a larger version for general use."

### Product & E-commerce

Professional product animations:

- **360° Rotations**: "Create a rotating GIF of a sneaker on a clean white background"
- **Feature Highlights**: "Make a GIF showing the key features of a smartwatch — zoom into the display, show the band"
- **Before/After**: "Create a before/after GIF for a photo editing app — toggle between unedited and edited"
- **Unboxing Reveals**: "Make a GIF of a product box opening to reveal the product inside"

**Example prompt:**
> "Create a product GIF for our e-commerce listing:
> 
> Product: Premium wireless earbuds in a matte black case
> Animation: Case opens slowly, earbuds float up with a subtle glow effect
> Style: Clean, minimal, dark background with dramatic lighting
> Duration: 3 seconds, seamless loop
> 
> Optimize for both web (under 5MB) and email (under 1MB).
> Deliver the GIF and the MP4 source."

### Cinemagraphs

Still photos with mesmerizing subtle motion:

- **Coffee Steam**: "Create a cinemagraph of a coffee cup — everything still except the steam rising"
- **Rain on Window**: "Make a cinemagraph of a city view through a window with rain drops running down the glass"
- **Flickering Candle**: "Create a cinemagraph of a cozy reading nook — only the candle flame moves"
- **Flowing Water**: "Make a cinemagraph of a forest stream — trees are still, water flows endlessly"
- **Hair in Wind**: "Create a cinemagraph of a woman looking at the ocean — only her hair moves in the breeze"

**Example prompt:**
> "Create a cinemagraph for our café's website:
> 
> Scene: A latte on a marble counter by a window, morning light streaming in
> Motion: Only the steam from the latte moves — everything else is perfectly still
> Mood: Warm, inviting, cozy
> Loop: Seamless, infinite
> Duration: 4 seconds
> 
> This needs to feel like a photograph that's alive. Subtle is better."

### Social Media Animations

Eye-catching content for feeds and stories:

- **Announcement GIFs**: "Create an animated 'We're Hiring!' GIF for LinkedIn"
- **Seasonal Content**: "Make a holiday-themed animated banner for our Instagram"
- **Branded Loops**: "Create a subtle animated version of our logo for email signatures"
- **Countdown GIFs**: "Make a countdown animation for our product launch — 3, 2, 1, Launch!"

### Animated Art & Illustrations

Creative and artistic GIFs:

- **Pixel Art Animations**: "Create a pixel art GIF of a campfire with flickering flames"
- **Isometric Loops**: "Make an isometric GIF of a tiny coffee shop with people walking in and out"
- **Abstract Loops**: "Create a mesmerizing abstract GIF with flowing geometric shapes in gradient colors"
- **Character Animations**: "Make a GIF of a pixel art character running endlessly — side-scroller style"

**Example prompt:**
> "Create an isometric pixel art GIF:
> 
> Scene: A tiny Japanese ramen shop at night, neon signs glowing
> Animation: Steam rises from bowls, neon signs flicker subtly, a cat walks by occasionally
> Style: Detailed pixel art, warm color palette
> Loop: Seamless, 4 seconds
> 
> I want this to feel like a living diorama. The kind of GIF people stare at for 30 seconds."

### UI/UX Demo GIFs

Show off your product:

- **Feature Walkthroughs**: "Create a GIF showing the drag-and-drop feature in our project management tool"
- **Micro-interactions**: "Make a GIF demonstrating our satisfying toggle animation"
- **Loading Animations**: "Create a branded loading animation GIF for our app"
- **Onboarding Flow**: "Make a GIF showing the 3-step signup flow for our landing page"

---

## Output Specifications

| Feature | Details |
|---------|---------|
| **Duration** | 1-6 seconds (shorter is better for GIFs) |
| **Loop Types** | Seamless, boomerang (ping-pong), one-shot |
| **Aspect Ratios** | 1:1, 16:9, 9:16, 4:3, custom |
| **Frame Rate** | 10-20 FPS (optimized per use case) |
| **Color Depth** | Up to 256 colors (intelligent palette selection) |
| **Output** | GIF (primary) + MP4 source (bonus) |

### Platform Size Limits

| Platform | Max Size | Recommended Width |
|----------|----------|-------------------|
| Discord | 8 MB | 400px |
| Twitter/X | 15 MB | 480px |
| Slack | 20 MB | 400px |
| WhatsApp | 6 MB | 400px |
| Email | 1 MB | 300px |
| Website/Blog | No hard limit | 600-800px |

Tell CellCog which platform you're targeting and it will optimize automatically.

---

## Chat Mode for GIFs

| Scenario | Recommended Mode |
|----------|------------------|
| Individual GIFs — reactions, product shots, cinemagraphs | `"agent"` |
| GIF sets — multiple coordinated GIFs for a campaign or sticker pack | `"agent team"` |

**Use `"agent"` for most GIF work.** Single GIFs execute well in agent mode.

**Use `"agent team"` when you need a cohesive set** — like 10 reaction GIFs with the same character, or a suite of product GIFs that share a visual style.

---

## Example Prompts

**Quick reaction GIF:**
> "Create a reaction GIF: a cartoon dog tilting its head in confusion, then a question mark pops up. Cute, simple style. Seamless loop, 2 seconds. Optimize for Discord."

**Product showcase:**
> "Create a GIF for our landing page hero section:
> 
> Show our app dashboard loading in — data fills the charts, numbers count up, everything comes alive.
> Style: Clean, modern, our brand colors (blue #2563EB, white, gray)
> Duration: 3 seconds, seamless loop
> Size: 800px wide, optimize for web (under 5MB)"

**Artistic cinemagraph:**
> "Create a cinemagraph of a mountain landscape at golden hour.
> 
> Everything is still — the mountains, the trees, the lake.
> But the clouds move slowly across the sky, and there's a subtle shimmer on the lake surface.
> 
> Mood: Peaceful, majestic, meditative.
> Seamless loop, 5 seconds. High quality for website hero section."

**Social media animation:**
> "Create an animated GIF announcing our Series B funding:
> 
> Text: '$25M Series B' appears with a satisfying animation
> Background: Subtle confetti or particle effect
> Style: Professional but celebratory, our brand teal (#2e7e7e)
> Format: Square 1:1 for LinkedIn and Twitter
> Duration: 3 seconds, loops once then holds"

---

## Tips for Better GIFs

1. **Shorter is better**: 2-3 second GIFs loop more satisfyingly than 6-second ones. Keep it tight.

2. **Specify your platform**: "For Discord" vs. "For email" dramatically changes optimization. Discord allows 8MB; email needs under 1MB.

3. **Seamless loops need planning**: Describe the motion as cyclical — "steam rises endlessly", "pendulum swings back and forth", "character walks in place."

4. **Fewer colors = smaller files**: If you don't need photorealism, suggest a limited color palette. Pixel art and flat design GIFs are naturally smaller.

5. **Request both formats**: CellCog delivers both GIF and MP4. Use the MP4 on platforms that support it (Twitter, web) — it's higher quality at smaller file sizes.

6. **Cinemagraph secret**: The best cinemagraphs have 95% of the image perfectly still with only one small element moving. More motion = less magic.

---

## If CellCog is not installed

Run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
**OpenClaw users:** Run `clawhub install cellcog` instead.
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
