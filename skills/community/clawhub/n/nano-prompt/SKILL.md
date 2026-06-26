---
name: nano-prompt
description: NanoBanana E-commerce Image Generation Prompt Engineering
license: MIT
---

# Nano Banana Prompt Engineering Skill for E-commerce

This skill, created by coopeai.com, provides comprehensive guidelines and prompt engineering patterns for writing professional image generation prompts for Google's **Nano Banana** model suite, optimized specifically for e-commerce merchants and digital designers.

---

## 1. Nano Banana Model Specifications Reference

To get the best results, prompts and configurations must align with the capabilities of the specific Nano Banana model in use.

### 1.1 Model Suite Overview
*   **Nano Banana (Gemini 2.5 Flash Image):** Optimized for high speed and low latency. Ideal for high-volume batch generation of simple product concepts.
*   **Nano Banana 2 (Gemini 3.1 Flash Image):** Balances high-efficiency generation with advanced reasoning. Integrates Search Grounding for real-world accuracy and handles extreme formats well.
*   **Nano Banana Pro (Gemini 3 Pro Image):** Flagship model with a powerful reasoning backbone. Acts as a "digital art director" that excels in complex compositions, fine text rendering, multi-turn conversational editing, and physical causality (reflections, lighting, shadow placement).

### 1.2 Image Quantities & Consistency
*   **Character/Subject Consistency:** Supports maintaining resemblance for up to **5 characters/subjects** across generations.
*   **Object Fidelity:** Accurately retains features and spatial layout for up to **14 objects**.
*   **Reference Images:** Supports mixing **5 to 20 reference images** to influence style, composition, layout, or color palette.

### 1.3 Supported Aspect Ratios
Select the correct aspect ratio according to the target e-commerce channel:
*   **Square / Standard (1:1, 4:5, 3:4):** Main product listing images, Taobao/Tmall/JD product detail cards, Instagram posts.
*   **Landscape (16:9, 4:3, 3:2):** Website banners, splash screens, landing page hero sections.
*   **Portrait (9:16, 2:3):** Mobile detail pages, Pinterest, Xiaohongshu (RED) feed graphics, TikTok ads.
*   **Panoramic / Extreme Banners (Nano Banana 2 only: 4:1, 8:1, 1:4, 1:8):** Ultra-wide website headers, billboard ads, skyscraper display ads, decorative sidebars.

### 1.4 Resolution & Output Quality
*   **Range:** Supported from **512px (0.5K)** to **4096px (4K)**.
*   **Standard Production Quality:** **1024×1024 (1K)** or **2048×2048 (2K)**. Use 2K for professional print or high-end product zoom-ins. Pro models support upscaling to 4K natively.

---

## 2. Prompt Engineering Best Practices

To get the most out of the Nano Banana model suite, follow these best practices:

### 2.1 Keyword Ordering & Attention Weighting
*   **Front-loading Rule:** Diffusion models allocate greater attention to keywords placed at the beginning of the prompt. Always define the **Core Product Subject** within the first 10-15 words.
*   **Semantic Proximity:** Place modifiers (colors, textures, materials) immediately adjacent to the noun they describe (e.g., use `"matte black ceramic bottle"` instead of `"ceramic bottle, black color, matte texture"`).

### 2.2 Text Rendering & Packaging Limitations
*   **Double-Quote Rule:** Wrap text to be rendered on labels or packages in double quotes (e.g., `"printed with the word 'GLOW'"`).
*   **Length Constraint:** Limit rendered text to short English words (under 12 characters). Do not attempt to render sentences or complex non-English characters directly; these should be overlaid in post-production.

### 2.3 Camera Lens & Focal Length Standards
*   **Focal Length Optimization:** Use **85mm macro lens** or **100mm lens** for product detail and close-up shots; use **35mm or 50mm lens** for environmental lifestyle shots. Avoid generic terms like "high resolution" and instead guide the model with specific lens focal lengths.
*   **Aperture & Depth of Field:** Explicitly specify the aperture (e.g., **f/1.8** or **f/2.4**) along with **shallow depth of field** or **soft bokeh** to draw focus to the core product subject and naturally blur out background distractions.

### 2.4 Negative Exclusions & Positive State Descriptions
*   **Describe Positive States:** Modern Pro models follow positive descriptions more effectively. Instead of cluttering the prompt with negative phrasing like `"no watermark"` or `"no scratches"`, describe the desired state positively (e.g., `"pristine, clean surface"`, `"clear and transparent layout"`).
*   **Leverage Dedicated Negative Fields:** If the interface supports a dedicated Negative Prompt field, offload generic exclusion tags (e.g., `"watermark, text, signatures, low quality, deformed, cropped"`) into it to keep the main prompt semantic flow clean.

### 2.5 High-Fidelity Material & Color Combinations
*   **Material-Color Pairing:** Never define colors in isolation; always pair them with texture/material descriptions (e.g., use `"brushed champagne gold metallic surface"` instead of `"gold color"`, and `"matte off-white ceramic"` instead of `"white bottle"`).
*   **Reflectance & Specularity Mapping:** Specify the exact physical interactions of light on materials (e.g., `"soft diffused reflection on the metallic edges"` or `"sharp gloss reflection"`) to allow the Pro model's physics engine to render premium textures realistically.

### 2.6 Stylization & Reference Image Semantic Matching Guide
*   **Declare a Unified Aesthetic Style:** When mixing **5 to 20 reference images**, you must explicitly state a unified aesthetic style in the prompt (e.g., `"Wabi-Sabi aesthetic"` or `"mid-century modern style"`) to prevent the model from generating conflicting visuals due to slight variances among the references.

---

## 3. Platform-Specific Target Audience & Style Mapping

Different e-commerce platforms cater to distinct demographics. Aligning prompt vocabulary with the target platform's aesthetics ensures higher conversion rates.

### 3.1 Platform Visual Strategies

| Platform | Core Audience | Brand Positioning | Visual Style & Key Prompts |
|---|---|---|---|
| **Xiaohongshu (RED) / Instagram** | Gen Z, Young women, Trend-seekers | Aesthetics first, Lifestyle, High emotional value | **Style:** Soft, warm, film-like, editorial, natural light.<br>**Key Words:** `soft cinematic morning light`, `subtle bokeh`, `pastel color palette`, `cozy lifestyle setup`, `analogue film grain`. |
| **Taobao / Tmall** | Mass consumers, Families, Detail-focused buyers | Practicality, High clarity, Detail-oriented | **Style:** Bright, clean, professional studio photography, crisp details.<br>**Key Words:** `professional studio softbox lighting`, `ultra-sharp details`, `true-to-life textures`, `balanced central composition`. |
| **JD.com** | Tech enthusiasts, Men, White-collar professionals | High quality, Authenticity, Tech/Modern, Reliability | **Style:** Futuristic, sleek, metallic, premium desk setups, clean structured lighting.<br>**Key Words:** `futuristic tech aesthetic`, `metallic reflections`, `sleek carbon fiber texture`, `sharp laser beam highlights`, `cinematic sci-fi lighting`. |
| **Pinduoduo / Temu** | Price-conscious buyers, Deal hunters | Immediate value, High impact, Cost-efficient | **Style:** High contrast, vibrant saturated colors, bold angles, eye-catching.<br>**Key Words:** `vibrant colors`, `high contrast`, `dramatic studio lighting`, `bold product presentation`, `uncluttered foreground`. |
| **Amazon** | Global mass consumers, Convenience buyers | Product clarity, High utility, Direct comparison | **Style:** Bright, standard solid white background, front/clear product shots, clear dimensions.<br>**Key Words:** `pure white background`, `bright studio softbox lighting`, `front view`, `clear product dimensions`, `no clutter`. |
| **Shopify DTC / Brand Sites** | Design-conscious buyers, Brand loyalists | Storytelling, Sustainable, Premium brand value | **Style:** Modern minimalism, eco-friendly lifestyle, sun-dappled shadows, neutral earthy tones.<br>**Key Words:** `minimalist design`, `eco-friendly aesthetic`, `natural sun-dappled lighting`, `neutral earthy tones`, `curated environment`, `authentic textures`. |

### 3.2 Case Study: Adaption of a Single Product ("Scented Candle") Across Platforms

To illustrate how target audience and platform positioning change prompt writing, see how the prompt for a **Scented Candle in an Amber Glass Jar** is adapted:

#### 1. Xiaohongshu (RED) / Instagram (Lifestyle & Emotion Focus)
*   **Target Audience & Positioning:** Gen Z, young female trend-seekers; premium lifestyles, emotional self-reward, home aesthetic enhancement.
*   **Goal:** Evoke a cozy, warm, and high-aesthetic lifestyle to generate clicks and social shares.
*   **Prompt:**
    > An atmospheric lifestyle photo of a minimalist amber glass jar scented candle lit, resting on a rustic wooden nightstand. A soft woolen throw blanket and a half-opened book are in the warm, out-of-focus background. The warm candle flame casts a soft, cozy orange glow, creating beautiful fireplace bokeh. Soft film grain aesthetic, cinematic feel, warm pastel colors. 3:4 aspect ratio, 2K.

#### 2. Taobao / Tmall (Detail, Quality & Clarity Focus)
*   **Target Audience & Positioning:** Mass consumer base, families, detail-focused buyers; practical, everyday utility, quality assurance.
*   **Goal:** Present accurate product information, texture, and high quality to drive purchase decisions.
*   **Prompt:**
    > A professional studio product photograph of a minimalist amber glass jar scented candle. The candle is placed centrally on a smooth, light beige concrete pedestal. Clean, bright studio softbox lighting highlighting the gold foil text "AURA" on the black label and the premium wax texture. Sharp focus on the lettering, clean soft shadows cast underneath, solid neutral background. 1:1 aspect ratio, 2K.

#### 3. JD.com (Tech/Modern Desk & Premium Focus)
*   **Target Audience & Positioning:** Tech enthusiasts, male consumers, white-collar professionals, business buyers; high tech/modern, reliability, premium authenticity.
*   **Goal:** Target tech enthusiasts and professionals by presenting a premium modern product in a clean, high-tech desk environment.
*   **Prompt:**
    > A high-end product photograph of a minimalist amber glass jar scented candle, placed on a sleek black walnut desk next to a modern mechanical keyboard and a premium metallic pen. In the dark background, a soft, out-of-focus warm light from a desk monitor bar is visible. The lighting is clean and structured, with cool blue ambient undertones from a smart light strip contrasting with the warm amber flame of the candle, highlighting the sharp edges of the glass. High fidelity, 1:1 aspect ratio, 2K.

#### 4. Pinduoduo / Temu (High-Impact & Eye-Catching Focus)
*   **Target Audience & Positioning:** Price-sensitive buyers, deal hunters; impulse buying, direct visual value, immediate utility.
*   **Goal:** Stand out immediately in a high-speed scrolling feed, conveying visual energy and immediate value.
*   **Prompt:**
    > A high-contrast, vibrant studio photograph of a premium amber glass jar scented candle sitting on a glossy black acrylic surface with a strong reflection. Bright, dramatic spotlight from the side highlighting the orange wax inside and casting a sharp shadow. Vibrant colors, clean minimalist background, bold product presentation designed to pop on a feed. 1:1 aspect ratio, 2K.

#### 5. Amazon (Product Clarity & Standard Focus)
*   **Target Audience & Positioning:** Global mass consumers, utility-focused buyers; functional standard, quick comparison, white-background compliance.
*   **Goal:** Showcase product parameters, label readability, and structural details with maximum clarity.
*   **Prompt:**
    > A clean, professional studio product photograph of a soy-wax scented candle in an amber glass jar, shot on a pure solid white background. Bright, even softbox lighting from the front-left illuminating all details of the brown amber glass and the white cotton wick. Sharp focus on the label, clean, soft shadows cast beneath the jar. High-end catalog photo, 1:1 aspect ratio, 2K.

#### 6. Shopify DTC / Brand Sites (Minimalist, Natural & Sustainable Focus)
*   **Target Audience & Positioning:** Global/Western mid-to-high-end consumers, design-conscious buyers; sustainable lifestyle, brand trust, organic/natural focus.
*   **Goal:** Convey organic ingredients, modern clean aesthetics, and eco-friendly brand value.
*   **Prompt:**
    > A clean, minimalist product presentation of a soy-wax scented candle in an amber glass jar. The candle is surrounded by natural ingredients: dried lavender sprigs and raw soy wax flakes scattered on a light linen tablecloth. Soft, natural sun-dappled lighting filtering through leaves, casting organic shadows. Neutral earthy tones, authentic texture. 4:5 aspect ratio, 2K.

---

## 4. Professional E-commerce Prompting Framework

For professional e-commerce product design, avoid simple keywords. Use the following structured prompt structure:

```
[Core Product Subject] + [Product Packaging & Fine Details] + [Environment & Setting] + [Composition, Focus & Angle] + [Lighting & Style] + [Technical Specifications (Aspect Ratio & Resolution)]
```

### Key Formatting Rules:
1.  **Semantic Description over Tag Clutter:** Nano Banana Pro understands natural language, physical causality, and semantic logic. Describe the scene as a story or a professional photo setup rather than using comma-separated keywords (e.g., use `"soft morning sunlight filtering through a nearby window"` instead of `"soft light, sun light, windows light, 8k"`).
2.  **Explicit Text Rendering:** For labels and packaging, wrap the target text in double quotes inside the prompt (e.g., `"a sleek glass bottle with the word 'PURE' printed in minimalist black font"`).
3.  **Physical Relations:** Specify how shadows, reflections, and water droplets behave to leverage the Pro model's reasoning capabilities.

---

## 5. E-commerce Scenarios & Prompt Examples

Here are the optimal prompt templates and examples for the five primary e-commerce scenarios.

### Scenario 1: Studio Product Shot with White/Clean Background
*   **Target Channels:** E-commerce main listing images (Taobao/Tmall/JD, Amazon).
*   **Design Focus:** True-to-life product textures, accurate color rendition, clean soft shadows, clean background.

#### 📝 Prompt Template:
> A professional studio product photograph of [Product Description] placed on a pristine, neutral [white/light gray] solid background. The surface has a [subtle matte texture / soft reflection]. Bright, even studio softbox lighting highlighting the details and texture of the product. Sharp focus, shot with a high-end 85mm lens. Minimalist composition, clean soft shadows cast beneath the product. High fidelity.

#### 💡 Example (Cosmetics):
> A professional studio product photograph of a minimalist matte ceramic bottle of face serum, with a dropper next to it. The bottle is placed on a pristine, neutral off-white solid plaster surface with a subtle matte texture. Bright, even studio softbox lighting coming from the top-left, highlighting the delicate ceramic texture and the clear glass dropper. Sharp focus on the bottle's label, shot with a high-end 85mm lens. Minimalist composition, clean soft shadows cast beneath the bottle. High fidelity, 1:1 aspect ratio, 2K resolution.

---

### Scenario 2: Scene-based Lifestyle & Atmosphere Shot
*   **Target Channels:** Xiaohongshu (RED) post covers, detail pages, social media marketing graphics.
*   **Design Focus:** Emotional resonance, natural environment, warm/themed lighting, rich storytelling.

#### 📝 Prompt Template:
> An atmospheric lifestyle photo of [Product Description] arranged on [Surface Details] in a [Detailed Environment]. [Context Elements / Supporting Props] are placed around to create a mood of [Target Mood]. Warm, natural [Lighting details, e.g., morning sunbeams filtering through leaves], casting organic shadows across the scene. Deep depth of field with a soft out-of-focus background. Organic, cinematic feel.

#### 💡 Example (Thermos / Mug):
> An atmospheric lifestyle photo of a green stainless steel thermos mug sitting on a rustic wooden picnic table in a sunlit pine forest. In the background, a soft-focus tent and campfire smoke are visible. Pine cones and a folded woolen blanket are placed near the mug to create a warm outdoor adventure mood. Warm morning sunbeams filter through the tree leaves, casting organic leaf shadows across the scene. Deep depth of field with a soft out-of-focus forest background, shot on a 50mm lens. Organic, cinematic feel, 3:4 aspect ratio, 2K resolution.

---

### Scenario 3: E-commerce Banner & Panoramic Header
*   **Target Channels:** PC website banners, app homepage hero images, shop category headers.
*   **Design Focus:** Wide composition, copy space (negative space for marketing text), balanced elements.

#### 📝 Prompt Template:
> A panoramic e-commerce marketing banner featuring [Product/Subject] on the [left/right] side of the frame, leaving clean, uncluttered negative space on the [right/left] for text overlay. The background is a [Background Description]. Seamless, modern design with a [Color Palette / Style] aesthetic. Clean studio lighting, balanced composition.

#### 💡 Example (Running Shoes - 4:1 Aspect Ratio):
> A panoramic e-commerce marketing banner featuring a futuristic orange running shoe frozen in mid-air on the left side of the frame, with dynamic water splashes exploding around it. The right three-quarters of the frame is a clean, dark gray concrete wall with minimal texture, leaving wide, uncluttered negative space for text overlay. Seamless, modern design with an energetic neon orange and slate gray aesthetic. Low-key dramatic side lighting, sharp focus on the shoe's mesh texture. 4:1 aspect ratio, 4K width.

---

### Scenario 4: Model Try-on & Apparel Presentation
*   **Target Channels:** Apparel listings, fashion lookup books, detail pages.
*   **Design Focus:** Natural skin textures, realistic fabric folds, lifelike postures, model-product consistency.

#### 📝 Prompt Template:
> A high-fashion e-commerce catalog photo of a [Model Details: gender, ethnicity, age] model wearing [Apparel Details: clothing type, color, fabric] in a [Setting/Location]. The model is standing in a [Posture/Expression]. Soft, natural daylight illuminating the model and the clothing, highlighting the fabric texture and drapes. Sharp details, professional fashion photography, natural skin texture, realistic wrinkles on the fabric.

#### 💡 Example (Linen Shirt):
> A high-fashion e-commerce catalog photo of a East Asian female model wearing a cream-colored organic linen button-up shirt and khaki trousers in a brightly lit, minimalist loft apartment. The model is standing near a large window in a relaxed, natural posture, looking slightly away from the camera with a gentle smile. Soft, natural daylight illuminating the model, highlighting the linen fabric texture and natural drapes. Sharp details, professional fashion photography, natural skin texture, realistic wrinkles on the fabric, 2:3 aspect ratio, 2K resolution.

---

### Scenario 5: Packaging Design & Text Mockups
*   **Target Channels:** Product conceptual designs, packaging mockups, promotional poster templates.
*   **Design Focus:** Legible text rendering, precise placement, realistic print textures (embossing, matte, gloss).

#### 📝 Prompt Template:
> A close-up packaging mockup of a [Package Type] designed for [Brand/Product Type]. The packaging has a [Color/Pattern] design and features the text "[EXACT TEXT]" printed in a [Font Style, e.g., minimalist sans-serif] font on the front label. The surface of the packaging has a [matte/glossy] finish with [fine details, e.g., embossed gold foil accents]. Shot under controlled studio lighting on a complementary colored background. Sharp focus on the lettering.

#### 💡 Example (Organic Coffee Bag):
> A close-up packaging mockup of a kraft paper coffee bag designed for specialty coffee beans. The packaging has a clean, minimalist design and features the text "EARTH BREW" printed in a bold, clean black sans-serif font on the front label, with smaller text "ORGANIC COFFEE" printed directly below it. The surface of the kraft paper has a textured, recycled feel with matte black print. Shot under soft, warm studio lighting on a neutral slate stone background. Sharp focus on the lettering, high-fidelity text rendering, 1:1 aspect ratio, 2K resolution.

---

## 6. Multi-Turn Conversational Editing Guidelines

When using Nano Banana Pro for iterative product design, guide the model through multi-turn adjustments using natural commands:

1.  **Replacing Elements:**
    *   *Bad:* "Make background beach"
    *   *Good:* "Keep the product and its shadows exactly as they are, but change the background from the concrete floor to a sun-drenched sandy beach with gentle ocean waves in the distance."
2.  **Adjusting Lighting & Colors:**
    *   *Bad:* "Brighten"
    *   *Good:* "Increase the warm yellow sunlight coming from the left to create a golden hour effect on the product's surface, making the reflections more prominent."
3.  **Adding Objects:**
    *   *Bad:* "Add flower"
    *   *Good:* "Place a single white lily flower lying flat on the surface next to the perfume bottle, ensuring it casts a realistic shadow that aligns with the existing light source."
4.  **Detail Retouching & Flaw Removal:**
    *   *Bad:* "Fix the scratches on the bottle"
    *   *Good:* "Smooth out the surface scratches on the bottle, ensuring the original transparency, refraction rate, and rim reflections of the glass remain completely unaffected."
5.  **Composition Adjustment & Outpainting:**
    *   *Bad:* "Move the product to the left"
    *   *Good:* "Keep the item's lighting and shadow logic identical, shift the coffee bag in the center 15% to the left, and naturally extend the smooth gray slate background texture into the newly opened space on the right."
