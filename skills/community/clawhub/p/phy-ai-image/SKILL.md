---
name: ai-image
description: Full AI image creation workflow — intent classification, prompt enhancement, multi-direction generation via fal.ai, and error recovery. Triggers on "generate image", "ai image", "create image", "make an image", "image generation", "/ai-image", or any image creation request.
homepage: https://canlah.ai
metadata: {"openclaw": {"emoji": "🎨", "os": ["darwin", "linux"]}}
---

# AI Image Creation Workflow

Complete image creation pipeline: classify intent, enhance prompt, generate via fal.ai, recover from errors.

For brand-specific visuals, use a dedicated brand image skill if available.
For model selection help, reference `/fal-model-selector`.

---

## Phase 1: Intent Classification

When a user mentions image creation, FIRST classify their intent into one of six categories:

### A. EXPLORING — No clear idea yet
**Signals:** "help me think of something", "any inspiration", "not sure what to make"

**Action:**
1. Ask about use case (social media? product? marketing? personal?)
2. Search `references/prompt-library-curated.json` for relevant examples
3. Show 3-5 options with descriptions
4. Let user pick, THEN proceed to generation

### B. BRIEF IDEA — Intent but underspecified
**Signals:** Description under ~30 words, lacks visual details (composition, lighting, color, texture, perspective)
**Examples:** "portrait photo", "tech logo", "gazebo in garden"

**Action:**
1. Enhance the prompt using the appropriate style template from `references/prompt-templates.md`
2. Show the enhanced prompt with brief creative rationale
3. Wait for user confirmation before generating

### C. DETAILED PROMPT — User knows what they want
**Signals:** Multi-sentence prompt with specific visual details, style references, or technical terms
**Examples:** Prompt with lens specs, lighting setup, material descriptions

**Action:**
1. Generate directly — do NOT over-process
2. Only suggest minor tweaks if obvious improvements spotted

### D. EDIT/MODIFY — Change an existing image
**Signals:** User provides/references an image AND describes a specific change
**Examples:** "add text to this", "change the background", "remove the person"

**Action:**
1. Keep prompt minimal and edit-focused
2. Upload reference image if local (use fal.ai upload or public URL)
3. Prompt describes ONLY the edit, not the entire image
4. Use edit-capable models: `fal-ai/flux-2/edit`, `fal-ai/gpt-image-1.5/edit`, `fal-ai/bytedance/seedream/v4.5/edit`

### E. BATCH REQUEST — Multiple variations
**Signals:** "4 directions", "multiple versions", "a set of assets"

**Action:**
1. Plan the variants first, present as a table
2. ASK user which direction(s) to try: "Pick a number, or I can generate all N"
3. NEVER auto-generate all variants without explicit choice
4. Generate AFTER user responds
5. Max 4 parallel per batch

### F. CREATIVE + EXTENSIONS — Multi-step workflow
**Signals:** "design a logo and make mockups", "create X and apply to Y"

**Action:**
1. Plan 3-5 design directions, present to user, ASK which to try
2. Generate ONLY the chosen direction(s)
3. Show result, get approval
4. THEN plan and generate extensions/derivatives
5. NEVER jump from plan to generating everything

---

## Phase 2: Prompt Enhancement

When the user provides a brief idea (Intent B), enhance using the appropriate style template.

### Style Selection

| Style | When to Use | Template |
|-------|-------------|----------|
| **Realistic** | Product photography, architecture, portraits, any photorealistic need | See `references/prompt-templates.md` Section 1 |
| **Anime** | 2D illustration, manga style, character art | See `references/prompt-templates.md` Section 2 |
| **Illustration** | Concept art, digital painting, editorial illustration | See `references/prompt-templates.md` Section 3 |

### Enhancement Protocol

1. Read the appropriate template from `references/prompt-templates.md`
2. Apply the template's methodology to transform the user's brief input
3. Output the enhanced prompt in two parts:
   - **Narrative Specification**: Dense descriptive paragraph
   - **Technical Metadata**: Visual style, key elements, lighting, composition
4. Show to user, explain creative choices briefly
5. Proceed only after confirmation

### Key Principles (from "Blueprint Method")
- **Technical precision over feeling**: Not "cinematic" but "three-point lighting with warm key, cool fill, 85mm f/1.4"
- **Quantifiable spatial logic**: Foreground/midground/background, lens specs, lighting setup
- **Material physics**: How materials interact with light — "brushed aluminum catching overhead softbox", not just "shiny metal"
- **Cohesive narrative**: Prompt reads like a director's brief, not a tag list

---

## Phase 3: Generation via fal.ai

### Default Models by Task

| Task | Model | Price | Notes |
|------|-------|-------|-------|
| **General image** | `fal-ai/flux-2-pro` | $0.03/MP | Zero-config, production-ready |
| **Product photo** | `fal-ai/image-apps-v2/product-photography` | - | Studio lighting presets |
| **Text in image** | `fal-ai/ideogram/v3` | $0.03-0.09 | Best typography |
| **Photo-real portrait** | `fal-ai/nano-banana-pro` | ~$0.10 | High quality portraits |
| **Scene editing** | `fal-ai/bytedance/seedream/v4.5/edit` | - | Best for scene changes |
| **General editing** | `fal-ai/flux-2/edit` | $0.012/MP | Multi-image support |
| **Google quality** | `fal-ai/gemini-3-pro-image-preview` | $0.15-0.30 | Up to 4K |

### Generation Code Pattern

```python
import fal_client
import os

# Set your FAL API key via environment variable
fal_client.api_key = os.environ.get("FAL_API_KEY")

# Text to image
result = fal_client.subscribe(
    "fal-ai/flux-2-pro",
    arguments={
        "prompt": "YOUR ENHANCED PROMPT HERE",
        "image_size": "landscape_16_9",  # or square, portrait_4_3, etc.
        "num_images": 1,
    }
)
image_url = result["images"][0]["url"]
print(f"Generated: {image_url}")

# Download locally
import urllib.request
urllib.request.urlretrieve(image_url, os.path.expanduser("~/Pictures/ai-image/output.jpg"))
```

### Multi-Direction Parallel Generation

For batch requests (Intent E), generate up to 4 in parallel:

```python
import fal_client
import concurrent.futures
import os

fal_client.api_key = os.environ.get("FAL_API_KEY")

prompts = [
    "Direction 1: ...",
    "Direction 2: ...",
    "Direction 3: ...",
]

def generate(prompt):
    return fal_client.subscribe(
        "fal-ai/flux-2-pro",
        arguments={"prompt": prompt, "image_size": "landscape_16_9"}
    )

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(generate, prompts))

for i, r in enumerate(results):
    print(f"Direction {i+1}: {r['images'][0]['url']}")
```

### Image Size Options (fal.ai)

| Size Name | Dimensions | Use Case |
|-----------|------------|----------|
| `square` | 1024x1024 | Social media, profile |
| `square_hd` | 1536x1536 | High-res square |
| `portrait_4_3` | 768x1024 | Portrait |
| `portrait_16_9` | 576x1024 | Stories, vertical |
| `landscape_4_3` | 1024x768 | Standard landscape |
| `landscape_16_9` | 1024x576 | Banner, cinematic |

### Reference Image Usage

```python
# Edit with reference
result = fal_client.subscribe(
    "fal-ai/flux-2/edit",
    arguments={
        "prompt": "Change the background to a sunset beach",
        "image_url": "https://example.com/original.jpg",
    }
)

# Product photography with reference
result = fal_client.subscribe(
    "fal-ai/image-apps-v2/product-photography",
    arguments={
        "product_image_url": "https://example.com/product.jpg",
        "aspect_ratio": "1:1",
    }
)
```

---

## Phase 4: Presenting Results

### Before generating:
- When enhancing prompts, briefly explain creative direction
- When planning variants, describe each direction distinctively

### After generating:
- Show the image URL and local file path
- Do NOT describe or imagine what the image looks like (you cannot see it)
- Keep it brief
- Suggest next steps: "Want to try a different direction?" or "Ready to create extensions?"

### Format:
```
**Direction 1: Modern Minimal**
Image: [url]
Saved to: ~/Pictures/ai-image/...

**Direction 2: Dramatic Lighting**
Image: [url]
Saved to: ~/Pictures/ai-image/...
```

---

## Phase 5: Error Recovery

When generation fails, diagnose and guide:

| Error Type | Detection | Recovery |
|-----------|-----------|----------|
| **Safety/content** | "safety", "policy", "flagged" | Auto-rephrase prompt, offer cleaned version |
| **Rate limit** | 429, "rate limit" | Wait 30s and retry once |
| **Model unavailable** | "not found", "inactive" | Suggest alternative from `/fal-model-selector` |
| **Invalid size/ratio** | "not supported" | Show valid options |
| **Network error** | "fetch failed", "timeout" | Retry once automatically |
| **Credit/billing** | 402, "insufficient" | Warn user, suggest cheaper model |

### Auto-retry logic:
- Network errors: retry once after 5s
- Rate limits: retry once after 30s
- All others: show error + guidance, don't retry

---

## Prompt Library

A curated collection of high-quality prompt templates is available at `references/prompt-library-curated.json`.

Search it when user is exploring (Intent A) or needs inspiration.

### How to search:
```python
import json
import os

with open(os.path.expanduser("~/.claude/skills/ai-image/references/prompt-library-curated.json")) as f:
    library = json.load(f)

# Search by keyword
keyword = "product"
matches = [p for p in library if keyword.lower() in p["prompt"].lower() or keyword.lower() in " ".join(p["categories"]).lower()]
```

### Categories available:
- Product (product photography, packaging, advertising)
- 3D (icons, infographics, typography)
- Photograph (editorial, fashion, landscape)
- Food (food photography, restaurant)
- App (UI/UX mockups)

---

## Decision Tree Summary

```
User mentions image creation
    |
    v
Classify intent (A-F)
    |
    +-- A (Exploring) --> Search prompt library --> Show options --> User picks --> Enhance --> Generate
    +-- B (Brief idea) --> Enhance prompt --> Show to user --> Confirm --> Generate
    +-- C (Detailed) --> Generate directly
    +-- D (Edit) --> Upload ref image --> Minimal edit prompt --> Generate with edit model
    +-- E (Batch) --> Plan variants --> User picks --> Generate in parallel (max 4)
    +-- F (Multi-step) --> Plan directions --> User picks --> Generate --> Approve --> Extensions
    |
    v
Present results (URL + local path, no description)
    |
    v
Suggest next steps
```

---

## Integration with Other Skills

| Need | Skill |
|------|-------|
| Brand-specific visuals | Use your brand image skill |
| Model selection help | `/fal-model-selector` |
| Video generation | `/fal-model-selector` (video section) |
| Full model database | `/fal-ai-models` |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
