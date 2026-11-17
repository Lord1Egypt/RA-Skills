---
name: product-page-designer
description: Design and generate international-brand-quality product detail pages for cross-border e-commerce. Generates complete product page content (Hero, Features, Lifestyle, Specs, FAQ) plus AI image prompts and visual assets for any consumer electronics product. Output meets Apple/Nothing brand standards.
category: creative
---

# Product Page Designer Skill

Generate complete, conversion-optimized product detail pages for consumer electronics that meet international brand standards (Apple, Nothing, Sonos level).

## Workflow

### Step 1: Gather Product Info

Ask the user for:
- **Product name** (e.g., "Bluetooth Earbuds", "Smart Watch")
- **Product category** (headphones, earbuds, speaker, watch, etc.)
- **Key specs** (battery, connectivity, waterproof rating, etc.) — if unknown, use standard industry specs for the category
- **Target price range** (budget/mid/premium) — affects copy tone
- **Brand voice preference** (minimalist, energetic, technical, lifestyle) — default: minimalist

### Step 2: Generate Product Page Content

Create a complete product detail page with these sections:

#### A. Hero Section
- Product name (original, no brand infringement)
- One-line slogan (max 5 words, punchy)
- CTA with price
- Visual direction: product on dark background, dramatic lighting, no clutter

#### B. Key Features (4-6 points)
Each feature card needs:
- Icon suggestion
- Title (2-4 words, benefit-driven)
- One-line description (max 20 words)
- Image concept description

Standard features to consider (pick 4-6 relevant):
- ANC / Sound isolation
- Hi-Res / Audio quality
- Battery life
- Connectivity (Bluetooth version, multipoint)
- Latency / Gaming mode
- Waterproof rating
- Comfort / Fit
- Smart features (app, EQ, spatial audio)

#### C. Lifestyle Showcase (4 scenes)
Pick scenes relevant to the product category. Each needs:
- Scene name
- Image style description
- Photography direction
- Overlay copy (headline + subheadline)

Common scenes: Office/Work, Travel, Fitness/Outdoors, Relax/Home

#### D. Product Details
Three paragraphs:
1. Introduction (what it is, why it matters)
2. Experience (how it feels to use)
3. Why buy (differentiators, warranty, trial)

#### E. Specifications
Markdown table with standard specs for the category.

#### F. What's in the Box
Standard packaging list.

#### G. FAQ
8-10 questions covering: calls, compatibility, charging, returns, app, special features.

### Step 3: Generate AI Image Prompts

For EVERY image in the page, create a prompt following this template:

```
[Shot type] of [product description] in [setting/background],
[lighting description],
[composition notes],
[style keywords]:
professional commercial product photography, minimalist composition, clean studio lighting, modern aesthetic, premium feel, photorealistic, high-end consumer electronics, no visible branding, no text, no logos
```

**Critical rules for image prompts:**
1. ALWAYS append `no visible branding, no text, no logos` to every prompt
2. ALWAYS include `professional commercial product photography` as style anchor
3. ALWAYS specify aspect ratio and resolution
4. Product must be described generically (matte black, premium build) — never use real brand names
5. For lifestyle shots, describe the person/product relationship, not the person's identity

### Step 4: Generate Images with WaveSpeed

Use `wavespeed` skill to generate all images:

1. **Hero + Lifestyle images** → `google/nano-banana-2/text-to-image` at 2K resolution
2. **Feature cards** → `google/nano-banana-2/text-to-image` at 2K resolution
3. **Brand removal** (if AI generates fake logos) → `bytedance/seedream-v4.5/edit`

**Common pitfall**: AI models love to generate fake brand names on products ("SONY", "Bose", "Razer", etc.) — expect 10-30% of images to need cleaning. Always:
- Add `no visible branding, no text, no logos, unbranded, generic design` to every prompt
- After generation, check each image with `vision_analyze` for brand text
- If found, use `bytedance/seedream-v4.5/edit` to remove it (~$0.04/edit)
- Budget extra time and credits for the brand removal pass

### Step 5: Quality Review Checklist

Before delivering, verify:

- [ ] All copy is original (no brand infringement)
- [ ] Slogan is ≤ 5 words and memorable
- [ ] Feature descriptions are benefit-driven, not spec-driven
- [ ] Lifestyle copy matches the scene emotion
- [ ] All images are unbranded (no text, no logos)
- [ ] Image style is consistent across all shots
- [ ] Specs table is complete and accurate
- [ ] FAQ covers real customer concerns
- [ ] Overall tone matches the chosen brand voice

### Step 6: Deliver

Output as a single comprehensive Markdown document with:
1. Complete product page content (ready for web developers)
2. All image prompts organized by section
3. Generated image URLs (if wavespeed was used)
4. Layout suggestions for each section

## Product Category Templates

### Headphones / Earbuds
Standard specs: Bluetooth 5.x, ANC, 20-60h battery, IPX4-IPX7, 32Ω impedance, USB-C charging, multipoint, companion app

### Bluetooth Speakers
Standard specs: Bluetooth 5.x, 10-30h battery, IPX7, 10-40W output, stereo pairing, USB-C, built-in mic

### Smart Watches
Standard specs: AMOLED display, heart rate, SpO2, GPS, NFC, 5-14 day battery, IP68, smartphone notifications, sleep tracking

### Wireless Earbuds (TWS)
Standard specs: Bluetooth 5.x, ANC, 6-8h + case 24-32h total, IPX4-IPX5, touch controls, spatial audio, fast charge, wireless charging case

## Naming Convention

When generating product names, use this pattern:
- Brand prefix: Abstract, tech-sounding (AURA, NOVA, PULSE, VELO, ORBIT, LUMA, ZEN, CORE, FLUX, NEXUS)
- Product type: Pro, Ultra, Air, Lite, Max, SE
- Number: X1, Z3, S2 (optional, adds specificity)

Examples: AURA Pro X1, NOVA Ultra S2, PULSE Air SE

## Tone Guidelines

### Minimalist (Apple/Nothing style)
- Short sentences. Period. Like this.
- Numbers speak louder than adjectives
- "40 hours. Not 39. Not 41."
- Focus on feeling, not features

### Energetic (Nike/Adidas style)
- Action verbs. Movement. Energy.
- "Push harder. Go further."
- Emojis in social copy only
- Bold claims, backed by specs

### Technical (Sony/Bose style)
- Precise language. Measurements. Certifications.
- "40mm custom neodymium drivers"
- "Hybrid ANC with 45dB reduction"
- Data-driven comparisons

## Output Format

Always deliver in this structure:

```markdown
# [Product Name] — Product Detail Page

## Brand Style
[Tone selected]

## 1. Hero Section
- Name: [product name]
- Slogan: [tagline]
- CTA: [button text]
- Visual: [description]

## 2. Key Features
| # | Feature | Title | Description | Image Concept |
|---|---------|-------|-------------|---------------|
| 1 | ... | ... | ... | ... |

## 3. Lifestyle Showcase
### Scene 1: [Name]
- Copy: [headline + subheadline]
- Image style: [description]
- Photography: [direction]

...

## 4. Product Details
[Introduction paragraph]
[Experience paragraph]
[Why buy paragraph]

## 5. Specifications
| Spec | Value |
|---|---|

## 6. What's in the Box
- Item 1
- Item 2

## 7. FAQ
**Q:** ...
**A:** ...

## 8. Image Prompts
[All prompts organized by section, ready for wavespeed]
```

## Implementation Notes

### Next.js Product Page Pattern
When implementing in a Next.js project:
- Create route at `/product/[slug]/page.tsx`
- Use `ScrollReveal` component for scroll animations
- Use Tailwind CSS with custom nav-* color tokens (defined in globals.css)
- Hero: 2-column grid, product image + CTA
- Features: 3-column grid with image overlay cards
- Lifestyle: alternating 2-column blocks (image left/right, use `lg:[&>*:nth-child(1)]:order-2` for even items)
- Specs: table with alternating row styling (use divs instead of table for better Tailwind control)
- FAQ: accordion pattern with React useState
- Sticky bottom bar for CTA
- All images should be generated via wavespeed and hosted on CDN (cloudfront)
- Use `"use client"` directive on product pages (needed for interactive FAQ/cart)
- Move interactive state (useState) to the top-level component, not sub-components, to avoid "Cannot find name" errors
- Toast notifications: create DOM element dynamically rather than relying on global functions

### Brand Removal Workflow
When AI generates brand text on product images (very common — expect 10-30% of images to need cleaning):

**Prevention**: Always append `no visible branding, no text, no logos, unbranded, generic design` to every product prompt.

**Detection**: After generation, check each image with `vision_analyze` for brand text before integrating into the page.

**Fix** (use `bytedance/seedream-v4.5/edit` — cheapest at $0.04/edit, strongest prompt adherence):
```bash
# 1. Upload original
URL=$(npx @wavespeed/cli upload ./generated.png --json | jq -r .url)
# 2. Edit to remove branding
PROMPT="Remove all text and brand logos from the image. Keep everything else identical — same lighting, pose, composition, colors. Clean unbranded surface."
npx @wavespeed/cli run bytedance/seedream-v4.5/edit \
  -i prompt="$PROMPT" \
  -i images="[\"$URL\"]" \
  --json --download "./clean-{index}.{ext}"
```

**Budget**: ~$0.04/edit. Allow 2-3 edits per image if needed. Total brand-removal cost typically $0.10-$0.30 per product page.

**Common hallucinations observed**: "SONY", "Bose", "Razer", "AXIS AUDIO", "Sennheiser", "NIKE", "LEICA", "ANALOG VIBRATIONS" — on headphones, mice, vinyl sleeves, and other products.

**Proven prompt for brand removal**: Write the prompt to a file and read with `PROMPT=$(cat ...)`. Be specific about WHICH object to clean (e.g., "the gaming mouse should have no visible logo", "vinyl record sleeves should have no readable text"). Generic "remove all branding" prompts are less effective than targeted ones.

### End-to-End Session Pattern (Validated)
This workflow was tested end-to-end in a real session and proven to work:
1. Design product page content in Markdown → 2. Write image prompts to files → 3. Generate images in parallel batches (8-10 at a time) using background mode → 4. Evaluate images with `vision_analyze` → 5. Fix branded images with `seedream-v4.5/edit` → 6. Build Next.js product page → 7. Deploy to Netlify
