---
name: product-image-prompt
description: Craft effective AI image generation prompts for product photography, store branding, and marketing visuals. Use when you need product images, lifestyle shots, logos, or promotional graphics for your Mobazha store.
---

# Product Image Prompt Guide

Create professional product images, lifestyle shots, and store branding visuals using AI image generation tools (DALL-E, Midjourney, Flux, etc.) — without a photography studio.

## When to Use

- Need product images but don't have professional photos
- Want lifestyle/context shots for listings
- Creating store branding (header, avatar, banner)
- Generating promotional graphics for campaigns
- Improving existing product images

## Golden Rules

| Rule | Description |
|------|-------------|
| **Be Specific** | Define subject, environment, lighting, mood explicitly |
| **Natural Language** | Use complete sentences, not keyword stacking |
| **Edit, Don't Re-roll** | If 80% right, refine the prompt instead of starting over |
| **Context Matters** | Include "who it's for" to guide aesthetic decisions |
| **No Brand Logos** | Avoid including recognizable brand elements unless you own them |

## Prompt Structure

```
[Shot type] of [Subject] in [Setting], [Action/State].
[Style], [Composition], [Lighting], [Color], [Quality].
```

### Required Elements

| Element | Description | Examples |
|---------|-------------|---------|
| **Subject** | What to show (be specific) | "slim bifold leather wallet", "handmade ceramic mug" |
| **Setting** | Where it is | "on a marble countertop", "in a cozy home office" |
| **Style** | Overall feel | "minimalist", "lifestyle", "studio product shot" |
| **Composition** | Camera angle | "overhead flat lay", "45-degree angle", "close-up" |
| **Lighting** | Light source | "soft natural window light", "studio softbox", "golden hour" |
| **Color** | Palette | "warm earth tones", "clean white background", "moody dark" |

## Product Photography Styles

### Studio Shot (E-commerce Standard)

Best for: primary product image, clean and professional.

```
Professional product photograph of [product] on a clean white background.
Studio lighting with soft shadows, sharp focus, high resolution.
Shot at 45-degree angle showing product details. Commercial photography style.
```

### Lifestyle Shot (Context)

Best for: secondary images, showing the product in use.

```
Lifestyle photograph of [product] being used by [person description] in [setting].
Natural lighting, warm color palette, shallow depth of field.
Candid feel, authentic and aspirational. Editorial photography style.
```

### Flat Lay (Curated Collection)

Best for: collections, "what's included", accessories.

```
Overhead flat lay of [products] arranged on [surface].
Organized composition with balanced spacing. Soft diffused lighting.
Minimalist styling with [2-3 complementary props]. Clean editorial look.
```

### Detail / Macro

Best for: showcasing craftsmanship, texture, materials.

```
Extreme close-up macro shot of [specific detail] on [product].
Sharp focus on texture/stitching/grain, background softly blurred.
Natural directional lighting emphasizing surface detail. High resolution.
```

## Store Branding

### Store Header Image

```
Wide banner image (3:1 aspect ratio) showing [theme related to your products].
[Style] aesthetic, [color palette]. Clean and modern with space for text overlay.
Professional commercial photography. No text in image.
```

### Store Avatar

```
Minimalist logo icon for [store name/concept]. Simple, recognizable at small sizes.
[Color] on [background]. Modern, clean design suitable for a circular crop.
Geometric/iconic style, no fine text. Vector illustration aesthetic.
```

## Materials and Textures (Be Precise)

| Generic (weak) | Precise (strong) |
|---------------|-----------------|
| "metal finish" | "brushed titanium with subtle anodized reflections" |
| "glass bottle" | "frosted borosilicate glass with matte coating" |
| "leather" | "vegetable-tanned full-grain leather with natural patina" |
| "wood" | "live-edge walnut with hand-rubbed oil finish" |
| "fabric" | "heavyweight organic cotton with a slightly slubbed texture" |

## Lighting Quality (Be Specific)

| Basic (weak) | Professional (strong) |
|-------------|----------------------|
| "bright light" | "diffused golden hour light with soft rim lighting" |
| "dark background" | "deep shadows with subtle gradient falloff" |
| "natural light" | "north-facing window light, soft and directional" |
| "studio light" | "dual softbox setup with subtle fill from below" |

## Anti-Patterns

| Avoid | Why | Better |
|-------|-----|--------|
| "beautiful design" | Too vague | Describe specific visual elements |
| "high quality" | Non-visual | Describe textures, materials, lighting |
| "professional look" | Subjective | Reference specific aesthetic styles |
| "make it pop" | Meaningless | Specify contrast, saturation, or focal emphasis |
| Tag stacking ("4K, HDR, RAW") | AI understands intent | Use natural sentences |

## Product Type Examples

### Physical Product — Handmade Jewelry

```
Professional product photograph of a hand-hammered gold bangle bracelet
on a natural linen cloth. Soft directional lighting creating gentle shadows.
Close-up showing hammer texture detail. Warm, luxurious color palette.
Clean, minimal composition. Commercial jewelry photography style, high resolution.
```

### Digital Product — Design Template

```
Clean mockup showing a digital planner template displayed on an iPad
placed on a light oak desk beside a cup of coffee and a succulent.
Overhead angle, natural window light, soft shadows. Modern minimalist aesthetic.
Warm, inviting color palette. Lifestyle tech photography style.
```

### Apparel — T-Shirt

```
Lifestyle photograph of a person wearing a [color] organic cotton t-shirt,
standing in an urban setting with soft morning light. Shot at medium distance,
natural pose, shallow depth of field on the subject. Clean, modern streetwear
editorial style. Neutral color palette with [accent color] from the shirt.
```

## Workflow: From Prompt to Listing

1. **Generate** — Use your preferred AI image tool with the prompt
2. **Review** — Check quality, accuracy, and brand consistency
3. **Edit** — Refine the prompt or use image editing for adjustments
4. **Resize** — Ensure images meet Mobazha requirements:
   - Primary image: square (1:1) or landscape, minimum 600px
   - Recommended: 1200x1200px for sharp display on all devices
5. **Upload** — Use `listings_create` or `listings_update` with image data

## Integration with Other Skills

| Skill | Connection |
|-------|-----------|
| `product-description` | Write copy to match the visual style |
| `product-import` | Generate images for imported products that lack them |
| `storefront-cro` | Improve product images based on CRO audit |
| `store-onboarding` | Create initial store branding during setup |

## Example Prompts for Your Agent

> "Generate a product photo prompt for my handmade candles. They're soy wax in amber glass jars."
>
> "I need a lifestyle shot for my leather laptop sleeve — show it in a modern workspace."
>
> "Create a store header image for my organic skincare brand. Aesthetic: clean, natural, botanical."
