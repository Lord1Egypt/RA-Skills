---
name: image-2
version: 1.1.0
description: "GPT-4o Image Generation & Editing Skill - Create, edit, transform, and analyze images using GPT-4o native image-2 API. Supports text-to-image, inpainting, outpainting, style transfer, background removal, and intelligent image analysis. Ideal for marketing, product photos, illustrations, UI mockups, and visual content creation."
metadata:
  openclaw:
    emoji: "🎨"
    homepage: "https://clawhub.ai/gpt/image-2"
    always: false
    skillKey: "image-2"
    requires:
      env:
        - OPENAI_API_KEY
    primaryEnv: OPENAI_API_KEY
    install:
      - kind: node
        package: openai
        bins: []
---

# Image-2 Skill

> Create, edit, transform, and analyze images with GPT-4o's native image generation API

## When to Use This Skill

Use this skill whenever the user needs to:
- **Generate images** from text descriptions ("画一张...", "生成图片...", "create an image of...")
- **Edit existing images** with natural language ("把背景去掉", "add a sunset", "换成蓝色")
- **Create variations** of an image ("生成几个变体", "make 4 variations")
- **Analyze/describe images** ("这张图是什么", "describe this image", "提取文字")
- **Remove backgrounds** ("去除背景", "remove background")
- **Style transfer** ("变成水彩风格", "make it look like Van Gogh")
- **Create marketing visuals** ("设计海报", "make a social media post")
- **Product photography** ("产品图", "product shot on white background")
- **UI/UX mockups** ("界面设计", "app mockup", "website screenshot")

## Core Workflows

### Workflow 1: Text-to-Image Generation

When the user describes an image they want to create:

1. **Enhance the prompt** — Automatically add quality boosters:
   - Append professional photography/art terms based on context
   - Add lighting, composition, and mood details if not specified
   - Specify output format and dimensions if needed

2. **Call the API** — Use `generateImage()` with the enhanced prompt:
   ```javascript
   const result = await generateImage(enhancedPrompt, { size, quality, style });
   ```

3. **Save and present** — Download the image to the project directory and show the user:
   - Save to `./generated-images/` by default
   - Return the file path and a brief description

### Workflow 2: Image Editing

When the user wants to modify an existing image:

1. **Locate the source image** — Find the image file path from the conversation context
2. **Parse the edit intent** — Understand what changes the user wants
3. **Call the edit API** — Use `editImage()` with the source and instruction:
   ```javascript
   const result = await editImage(imagePath, editInstruction, { mask: maskPath });
   ```
4. **Present the result** — Show the edited image and describe what changed

### Workflow 3: Image Analysis

When the user asks about an image:

1. **Get the image** — From file path or URL
2. **Analyze with GPT-4o Vision** — Use `describeImage()`:
   ```javascript
   const result = await describeImage(imageSource, question);
   ```
3. **Report findings** — Present the analysis in a structured format

### Workflow 4: Batch Generation

When the user needs multiple images:

1. **Parse the batch request** — Understand variations needed
2. **Generate in parallel** — Call `generateImage()` for each variant
3. **Organize results** — Save with descriptive filenames

## Prompt Enhancement Rules

When generating images, automatically enhance the user's prompt:

### Quality Boosters (always append unless user specifies quality)
```
professional quality, high resolution, sharp details
```

### Context-Based Additions
| User Intent | Auto-Add |
|-------------|----------|
| Product photo | "studio lighting, clean background, commercial photography" |
| Portrait | "professional portrait photography, natural lighting" |
| Social media | "eye-catching, vibrant colors, modern design" |
| Illustration | "detailed illustration, professional artist quality" |
| Logo/branding | "clean vector style, scalable, minimal details" |
| Architecture | "architectural visualization, realistic rendering" |
| Food | "appetizing, food styling, professional food photography" |
| UI mockup | "clean design, modern interface, pixel-perfect" |

### Size Recommendations
| Use Case | Recommended Size |
|----------|-----------------|
| Social media post | `1024x1024` (square) |
| Story/vertical | `1024x1792` |
| Banner/landscape | `1792x1024` |
| Product listing | `1024x1024` |
| Presentation | `1792x1024` |
| Wallpaper | `1792x1024` |

## Style Presets

Quick style references for common requests:

| Preset Name | Style Description |
|-------------|-------------------|
| `product` | Clean white background, studio lighting, commercial photography |
| `lifestyle` | Natural setting, warm lighting, aspirational mood |
| `minimalist` | Simple composition, negative space, clean lines |
| `vintage` | Retro color grading, film grain, nostalgic mood |
| `futuristic` | Neon accents, dark background, sci-fi aesthetic |
| `watercolor` | Soft edges, pastel palette, artistic brush strokes |
| `3d-render` | Octane render, realistic materials, dramatic lighting |
| `anime` | Japanese animation style, vibrant, expressive |
| `sketch` | Pencil drawing, hand-drawn, artistic |
| `flat-design` | Vector style, bold colors, geometric shapes |

## API Reference

### `generateImage(prompt, options)`
Generate a new image from text description.

**Parameters:**
- `prompt` (string) — Image description (auto-enhanced by this skill)
- `options` (object):
  - `size` — `1024x1024` | `1024x1792` | `1792x1024` (default: `1024x1024`)
  - `quality` — `standard` | `hd` (default: `standard`)
  - `style` — `vivid` | `natural` (default: `vivid`)
  - `model` — `gpt-image-2` | `dall-e-3` (default: `gpt-image-2`)
  - `saveTo` — File path to save the image (default: `./generated-images/`)

**Returns:** `{ success, url, localPath, revisedPrompt }`

### `editImage(imagePath, prompt, options)`
Edit an existing image with natural language instructions.

**Parameters:**
- `imagePath` (string) — Path to the source image
- `prompt` (string) — Edit instruction
- `options` (object):
  - `mask` — Path to mask image (white = edit area, black = keep)
  - `size` — Output size
  - `model` — `gpt-image-2` | `dall-e-3` (default: `gpt-image-2`)

**Returns:** `{ success, url, localPath }`

### `generateVariations(imagePath, options)`
Generate creative variations of an existing image.

**Parameters:**
- `imagePath` (string) — Path to the source image
- `options` (object):
  - `count` — Number of variations 1-4 (default: 2)
  - `size` — Output size

**Returns:** `{ success, variations: [{ url, localPath }] }`

### `describeImage(imageSource, question)`
Analyze an image using GPT-4o Vision.

**Parameters:**
- `imageSource` (string) — File path or URL of the image
- `question` (string|null) — Specific question about the image (default: general description)

**Returns:** `{ success, description }`

### `downloadImage(url, savePath)`
Download a generated image to local storage.

**Parameters:**
- `url` (string) — Image URL from generation API
- `savePath` (string|null) — Local file path (default: auto-generated in `./generated-images/`)

**Returns:** `{ success, localPath }`

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Invalid API key` | OPENAI_API_KEY not set or invalid | Check environment variable |
| `Content policy violation` | Prompt violates safety guidelines | Rephrase the prompt |
| `Rate limit exceeded` | Too many requests | Wait and retry with backoff |
| `Image too large` | Source image exceeds size limit | Resize to under 4MB |
| `Timeout` | Generation took too long | Simplify prompt or retry |

## Best Practices

1. **Always enhance prompts** — Don't pass raw user input directly to the API
2. **Save locally** — Download generated images; URLs expire after 1 hour
3. **Use appropriate sizes** — Match the output size to the use case
4. **Prefer gpt-image-2** — Better quality and text rendering than dall-e-3
5. **Batch thoughtfully** — Generate 2-4 images max per request to avoid rate limits
6. **Describe edits clearly** — Be specific about what to change and where

## Changelog

### v1.1.0
- Added GPT-4o native image generation support (gpt-image-2 model)
- Added automatic prompt enhancement workflow
- Added image download and local save functionality
- Added style presets for quick reference
- Added batch generation workflow
- Improved error handling and documentation

### v1.0.0
- Initial release with DALL-E 3 support
- Basic generate, edit, variations, and describe functions

---

**Tags:** `image-generation` `AI-art` `GPT-4o` `image-2` `gpt-image-2` `visual-creation` `marketing` `product-photos` `illustration` `design` `openai` `dall-e` `image-editing` `background-removal` `style-transfer` `ui-mockup`
