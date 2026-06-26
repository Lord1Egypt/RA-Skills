---
name: gpt-image-2
description: GPTImage2 E-commerce Image Generation Prompt Engineering
license: MIT
---

# GPTImage2 E-commerce Image Generation Prompt Engineering

This skill, created by coopeai.com, provides comprehensive guidelines and prompt engineering patterns for generating professional e-commerce product images using OpenAI's **GPTImage2** model, optimized specifically for e-commerce merchants, brand designers, and digital marketers.

---

## 1. GPTImage2 Model Specifications Reference

### 1.1 Model Capabilities Overview

*   **GPTImage2:** OpenAI's flagship image generation model with native reasoning integration. Excels at precise instruction following, accurate text rendering on labels and packaging, complex multi-element compositions, and photorealistic product photography simulation.
*   **Key Differentiator:** Powered by the same reasoning backbone as GPT-4o, GPTImage2 understands nuanced natural language and spatial relationships — enabling you to describe a shot like a professional photographer rather than using keyword tags.

#### Breakthrough 1: Reasoning / Thinking Mode
GPTImage2 is the **first agentic image generation model** — it researches, plans, and self-checks the composition *before* rendering a single pixel.

*   **Instant Mode** (free): Standard generation with strong instruction following.
*   **Thinking Mode** (paid): The model reasons deeply about layout, lighting, and subject relationships before generating. Use this for complex multi-product compositions, intricate label designs, or scenes with strict spatial requirements.

For e-commerce: use Thinking Mode for hero images, packaging mockups, or any shot where precise object placement and text accuracy are critical.

#### Breakthrough 2: Near-Perfect Multilingual Text Rendering
GPTImage2 achieves approximately **~99% character-level text accuracy** across Latin, CJK (Chinese/Japanese/Korean), Hindi, Bengali, and Arabic scripts — the biggest leap over any previous image generator.

*   Chinese product label text (e.g., brand names, ingredient callouts) renders accurately without warped or invented characters.
*   Always wrap target text in double quotes in the prompt: `label reads "GLOW 光感精华"`.

#### Breakthrough 3: Multi-Image Generation with Style Consistency
In Thinking Mode, GPTImage2 can generate **up to 8 coherent images** from a single prompt, maintaining consistent characters, objects, lighting, and visual style across the entire set.

*   Ideal for: product line campaigns, A/B creative variants, multi-angle product shots, and lookbook series.
*   Specify the count in your prompt: `"Generate 4 product images of the same bottle from different angles, maintaining consistent lighting and brand aesthetic."`

### 1.2 Image Quantities & Consistency

*   **Batch Generation:** Supports generating **1 to 8 images** per request in Thinking Mode, or 1 image in Instant Mode.
*   **Style Consistency:** In Thinking Mode, all images in a batch maintain consistent characters, objects, lighting, and visual style — no longer needing separate style reference prompts for multi-image campaigns.
*   **Object Fidelity:** Reliably retains product details — label text, brand colors, material finishes — when described precisely.

### 1.3 Supported Output Formats & Sizes

*   **Preset Aspect Ratios (1K & 2K):** GPTImage2 supports 9 aspect ratios at both 1K and 2K resolutions:

    | Aspect Ratio | 1K Resolution | 2K Resolution | Best For |
    |---|---|---|---|
    | 1:1 | 1024×1024 | 2048×2048 | Product main images, social posts |
    | 4:5 | 1024×1280 | 2048×2560 | Instagram feed, Xiaohongshu |
    | 3:4 | 1024×1365 | 2048×2730 | Portrait product shots |
    | 4:3 | 1365×1024 | 2730×2048 | Landscape product shots |
    | 3:2 | 1536×1024 | 3072×2048 | Wide product layouts |
    | 2:3 | 1024×1536 | 2048×3072 | Mobile detail pages, Pinterest |
    | 16:9 | 1820×1024 | 3640×2048 | Website banners, video thumbnails |
    | 9:16 | 1024×1820 | 2048×3640 | TikTok/Reels ads, mobile splash screens |
    | 21:9 | 2048×878 | — | Ultra-wide panoramic banners |

*   **Custom Dimensions:** Any custom size is valid as long as:
    *   Both width and height are **multiples of 16**
    *   Neither edge exceeds **3840 px**
    *   Aspect ratio does not exceed **3:1**
    *   Total pixels between **655,360** (min) and **8,294,400** (max)

*   **4K Output (Beta):** Sizes above 2K (e.g., `3840×2160` for 4K landscape, `2160×3840` for 4K portrait) are supported but currently experimental.

*   **Quality Tiers:**
    *   `low` — Fast generation for rapid prototyping and concepts.
    *   `medium` — Balanced speed and quality for standard production use.
    *   `high` — Maximum fidelity for hero images, print assets, and final campaign materials.

*   **Output Formats:** `png` (default, lossless), `jpeg` (smaller file size), `webp` (optimized for web delivery).

*   **Note:** GPTImage2 does **not** support transparent backgrounds.

### 1.4 Image Editing Capabilities

*   **Inpainting (Edit API):** Selectively modify regions of an existing product image using a mask — swap backgrounds, adjust props, refine details — without re-generating the full image.
*   **Outpainting:** Expand the canvas of an existing image to create wider banner formats or add environmental context.
*   **Partial Edits:** Change a single element (e.g., replace a product label) while keeping the rest of the composition intact.

---

## 2. Prompt Engineering Best Practices

### 2.1 Natural Language Over Keyword Stacking

GPTImage2 is a reasoning model — describe your shot in plain English as you would brief a photographer.

*   **Avoid:** `"product photo, white background, 8k, sharp, studio lighting"`
*   **Prefer:** `"A professional studio photograph of the product centered on a pure white background, lit with a large softbox from the upper left to create soft, even illumination with a subtle shadow beneath."`

### 2.2 Precise Text Rendering on Packaging

GPTImage2 has significantly improved text rendering compared to previous models. Use these techniques for maximum accuracy:

*   **Explicit Quote Wrapping:** Surround the exact text you want rendered in double quotes: `label reads "PURE GLOW"`.
*   **Font Style Guidance:** Specify font weight and style: `bold sans-serif`, `thin serif italic`, `handwritten script`.
*   **Keep It Short:** Limit rendered text to short phrases under 20 characters per line for best accuracy. Use post-production tools to overlay long body copy.
*   **Position Anchoring:** State where text appears: `centered on the front label`, `printed along the top edge of the lid`.

### 2.3 Lighting Specification

Describe lighting as a cinematographer would:

*   **Source:** `large softbox`, `ring light`, `window light from camera-left`, `single hard spotlight`.
*   **Quality:** `soft and diffused`, `hard and directional`, `golden hour warm glow`, `cool overcast daylight`.
*   **Shadows:** `subtle drop shadow beneath the product`, `dramatic elongated shadow to the right`, `no visible shadow`.
*   **Reflections:** `mirror reflection on the glossy black surface`, `soft matte finish with no specular highlights`.

### 2.4 Depth of Field & Camera Simulation

*   **Shallow DoF:** `shallow depth of field with soft background bokeh, simulating an 85mm f/1.8 portrait lens`.
*   **Full Focus:** `everything in sharp focus from foreground to background, simulating f/11 aperture`.
*   **Macro Detail:** `extreme close-up macro shot revealing the fabric texture and stitching detail`.

### 2.5 Positive State Descriptions

Describe the desired final state rather than what to exclude:

*   **Avoid:** `no watermark, no text, no blurry areas`
*   **Prefer:** `clean, unmarked surface`, `sharp focus throughout`, `pristine product with no imperfections`

### 2.6 Style Reference Anchoring

When consistency across a product line is required, anchor all prompts to a shared aesthetic statement:

> `"Maintain the brand's clean minimalist aesthetic: neutral white and warm gray tones, soft diffused natural lighting, no harsh shadows, subtle linen texture surfaces."`

---

## 3. Platform-Specific Target Audience & Style Mapping

### 3.1 Platform Visual Strategies

| Platform | Core Audience | Brand Positioning | Visual Style & Key Prompts |
|---|---|---|---|
| **Xiaohongshu (RED) / Instagram** | Gen Z, Young women, Trend-seekers | Aesthetics first, Lifestyle, Emotional value | **Style:** Warm, soft, film-inspired, editorial layout, natural window light.<br>**Key Words:** `warm morning window light`, `soft film grain`, `pastel color palette`, `cozy lifestyle vignette`, `editorial magazine composition`. |
| **Taobao / Tmall** | Mass consumers, Families, Detail-focused buyers | Practicality, High clarity, Detail-oriented | **Style:** Bright, clean, true-to-color, professional studio, sharp details.<br>**Key Words:** `professional studio softbox lighting`, `ultra-sharp product detail`, `true-to-life color accuracy`, `centered balanced composition`, `clean neutral background`. |
| **JD.com** | Tech enthusiasts, Men, White-collar professionals | High quality, Authenticity, Modern, Reliability | **Style:** Futuristic, sleek metallic, premium desk environment, structured dramatic lighting.<br>**Key Words:** `futuristic tech product aesthetic`, `brushed metal reflections`, `sleek carbon fiber surface`, `cinematic sci-fi rim lighting`, `premium workspace context`. |
| **Pinduoduo / Temu** | Price-conscious buyers, Deal hunters | Immediate value, High visual impact | **Style:** High contrast, vibrant saturated colors, bold eye-catching composition.<br>**Key Words:** `vibrant saturated colors`, `high contrast dramatic lighting`, `bold central product placement`, `punchy studio spotlight`, `energetic visual presentation`. |
| **Amazon** | Global mass consumers, Convenience buyers | Product clarity, High utility, Direct comparison | **Style:** Bright, standard pure white background, front-facing product shots, full detail clarity.<br>**Key Words:** `pure white background`, `bright even softbox lighting`, `front-facing product view`, `all label text legible`, `no environmental props`. |
| **Shopify DTC / Brand Sites** | Design-conscious buyers, Brand loyalists | Storytelling, Sustainable, Premium brand value | **Style:** Modern minimalism, eco-lifestyle, organic sun-dappled light, neutral earthy palette.<br>**Key Words:** `minimalist brand aesthetic`, `natural sun-dappled light through linen curtains`, `neutral earthy tones`, `organic textures`, `intentional negative space`. |

### 3.2 Case Study: "Vitamin C Face Serum" Across Platforms

#### 1. Xiaohongshu (RED) / Instagram
*   **Prompt:**
    > An atmospheric lifestyle photograph of a frosted glass dropper bottle of Vitamin C face serum placed on a warm marble vanity top. A single fresh orange slice and scattered dried flower petals surround the bottle. Warm, soft morning light streams in from a nearby window, creating a gentle golden glow on the glass. Soft film grain, editorial beauty aesthetic, warm pastel color palette. 4:5 aspect ratio, high quality.

#### 2. Taobao / Tmall
*   **Prompt:**
    > A professional studio product photograph of a frosted glass Vitamin C face serum bottle with a gold dropper cap, centered on a smooth light gray concrete pedestal. Clean, bright softbox lighting from the upper left highlights the bottle's embossed texture and the label reading "VITAMIN C 20%". Sharp focus throughout, soft clean shadow beneath the bottle, neutral white background. 1:1 aspect ratio, high quality.

#### 3. JD.com
*   **Prompt:**
    > A premium product photograph of a Vitamin C face serum bottle on a sleek dark gray slate surface. The bottle is surrounded by abstract molecular structure props and a single clean test tube. Cool-toned studio lighting with subtle blue rim light creates a modern science-backed aesthetic. Clean background with a shallow gradient. 1:1 aspect ratio, high quality.

#### 4. Pinduoduo / Temu
*   **Prompt:**
    > A vibrant, high-contrast studio product photograph of a Vitamin C face serum bottle placed on a glossy yellow acrylic platform with a bold reflection. A dramatic spotlight from above creates intense highlights on the orange-tinted bottle. Vivid saturated colors, bold composition, designed to immediately catch the eye in a fast-scrolling feed. 1:1 aspect ratio, high quality.

#### 5. Amazon
*   **Prompt:**
    > A clean, professional studio product photograph of a Vitamin C face serum bottle shot straight-on against a pure white background. Bright, even softbox lighting from front-left illuminates all label details, including the text "VITAMIN C 20% SERUM" and the ingredient list. No props, no background elements. All product details clearly visible. 1:1 aspect ratio, high quality.

#### 6. Shopify DTC
*   **Prompt:**
    > A minimalist product presentation of a Vitamin C face serum bottle nestled among fresh sliced oranges and green eucalyptus leaves on a white linen tablecloth. Soft, natural sun-dappled light filters through a nearby window creating organic soft shadows. Neutral earthy tones with a clean, premium brand feel. 4:5 aspect ratio, high quality.

---

## 4. Professional E-commerce Prompt Framework

Structure prompts using this sequence for consistent, professional results:

```
[Shot Type & Mood] + [Core Product Subject & Details] + [Surface & Environment] + [Props & Context] + [Lighting Description] + [Camera & Lens Simulation] + [Technical Specs]
```

### Key Rules:
1. **Describe the scene, not the keywords.** Write as if briefing a photographer: setting, mood, light source, camera position.
2. **Anchor text in quotes.** Any label or packaging text must be quoted: `label reads "EARTH BREW"`.
3. **Specify surface interactions.** State whether the product casts a shadow, has a reflection, or sits flush with the surface.
4. **Name the aesthetic.** End with a style anchor: `editorial beauty aesthetic`, `premium catalog photography`, `cozy lifestyle vignette`.

---

## 5. E-commerce Scenarios & Prompt Examples

### Scenario 1: Studio White Background Product Shot
*   **Target Channels:** E-commerce main listing images, Amazon, Taobao/Tmall main images.

#### Prompt Template:
> A professional studio product photograph of [Product Description] centered on a [pure white / light gray / off-white] background. [Lighting setup, e.g., "bright even softbox lighting from the upper left"]. [Focus detail, e.g., "sharp focus on the label text reading '[TEXT]'"]. Clean soft shadow beneath the product, no props. [Size], [Quality].

#### Example (Skincare Moisturizer):
> A professional studio product photograph of a matte white ceramic jar of face moisturizer with a gold lid, centered on a pure white background. Bright even softbox lighting from the upper left highlights the embossed logo and smooth ceramic texture. Sharp focus on the label reading "HYDRA GLOW CREAM". Clean soft shadow beneath the jar, no props. 1024×1024, high quality.

---

### Scenario 2: Lifestyle & Atmosphere Shot
*   **Target Channels:** Xiaohongshu (RED), Instagram, homepage banners, detail pages.

#### Prompt Template:
> An atmospheric lifestyle photograph of [Product] arranged on [Surface] in [Environment]. [Props] are placed around to evoke [Target Mood]. [Lighting description]. [Camera simulation]. [Size], [Quality].

#### Example (Scented Candle):
> An atmospheric lifestyle photograph of a white marble-effect candle jar, lit, resting on a rustic oak bedside table. A linen-bound notebook and a small sprig of dried lavender are placed nearby to evoke a peaceful evening reading mood. Warm, dim tungsten light from a bedside lamp casts a soft glow across the scene. Shallow depth of field with a soft out-of-focus bedroom background, simulating a 50mm f/2.0 lens. 1024×1536, high quality.

---

### Scenario 3: E-commerce Banner & Panoramic
*   **Target Channels:** Website homepage banners, app hero images, category headers.

#### Prompt Template:
> A wide-format e-commerce marketing banner with [Product/Hero Subject] positioned on the [left/right] side, leaving clean negative space on the [right/left] for text overlay. Background is [description]. [Style]. [Lighting]. 1536×1024, [Quality].

#### Example (Sneakers):
> A wide-format e-commerce marketing banner with a neon green performance running shoe floating in mid-air on the left side of the frame, with dynamic motion blur trails suggesting speed. The right two-thirds of the frame is a clean deep charcoal gray gradient, leaving generous negative space for headline text. Dramatic rim lighting on the shoe's upper. Energetic athletic aesthetic. 1536×1024, high quality.

---

### Scenario 4: Model & Apparel Presentation
*   **Target Channels:** Apparel listings, lookbooks, detail pages.

#### Prompt Template:
> A high-fashion e-commerce catalog photograph of a [Model description] wearing [Apparel description] in [Setting]. [Posture and expression]. [Lighting]. Natural skin texture, realistic fabric drape and wrinkle detail. [Size], [Quality].

#### Example (Oversized Blazer):
> A high-fashion e-commerce catalog photograph of a South Asian female model in her late twenties wearing an oversized camel wool blazer with relaxed trousers in a minimalist Copenhagen-style apartment. She stands near a large window in a natural relaxed pose, one hand in pocket, looking slightly off-camera with a calm expression. Soft diffused natural window light from the left highlights the wool texture and structured shoulders. Natural skin texture, realistic fabric drape. 1024×1536, high quality.

---

### Scenario 5: Packaging Design & Text Mockup
*   **Target Channels:** Packaging concepts, label designs, promotional mockups.

#### Prompt Template:
> A close-up packaging mockup of a [Package type] for [Product/Brand]. The packaging features [color/design description] with the text "[EXACT TEXT]" in [font style] on the front. Surface finish is [matte/gloss/foil]. [Lighting]. Sharp focus on all printed text. [Size], [Quality].

#### Example (Coffee Bag):
> A close-up packaging mockup of a kraft paper stand-up pouch for specialty coffee. The packaging features a minimalist cream-colored label design with the text "MORNING RITUAL" in a bold geometric sans-serif font and "SINGLE ORIGIN ETHIOPIA" in a smaller light-weight font below. The pouch has a natural kraft texture with a subtle matte finish. Soft warm studio lighting on a slate gray surface. Sharp focus on all printed text, high-fidelity text rendering. 1024×1024, high quality.

---

## 6. Image Editing with the Edit API

GPTImage2 supports targeted edits via the image editing API. Use these patterns for iterative product image refinement:

1.  **Background Replacement:**
    *   *Mask:* The background area around the product.
    *   *Prompt:* `"Replace the background with a sun-drenched sandy beach with soft ocean waves in the far distance, keeping the product and its shadow exactly as they are."`

2.  **Lighting Adjustment:**
    *   *Mask:* The entire image or specific highlight areas.
    *   *Prompt:* `"Enhance the warm golden-hour sunlight on the product's left side to create stronger rim lighting and a glowing highlight on the metallic cap."`

3.  **Prop Addition:**
    *   *Mask:* The empty surface area next to the product.
    *   *Prompt:* `"Add a single fresh white peony flower lying flat on the surface to the right of the bottle, casting a soft shadow that matches the existing light direction."`

4.  **Label Text Correction:**
    *   *Mask:* The label area only.
    *   *Prompt:* `"Replace the label text with 'RENEWED' in the same bold black sans-serif font, same size and position, keeping all other visual elements identical."`

5.  **Blemish & Imperfection Removal:**
    *   *Mask:* The specific blemish area.
    *   *Prompt:* `"Smooth out this surface imperfection while maintaining the original gloss level, refraction, and edge reflections of the glass bottle."`
