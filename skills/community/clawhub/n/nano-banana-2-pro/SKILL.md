---
name: nano-banana-2
description: Generate/edit images with Nano Banana 2 (Gemini 3.1 Flash Image). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 512/1K/2K/4K; 14 aspect ratios; up to 14 input images; thinking levels; use --input-image.
---

# Nano Banana 2 Image Generation & Editing

Generate new images or edit existing ones using Google's Nano Banana 2 API (Gemini 3.1 Flash Image Preview).

## Usage

Run the script using absolute path (do NOT cd to skill directory first):

**Generate new image:**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "your image description" --filename "output.png" [--model MODEL] [--resolution 512|1K|2K|4K] [--aspect-ratio RATIO] [--thinking-level minimal|high] [--image-only] [--api-key KEY]
```

**Edit existing image:**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "editing instructions" --filename "output.png" --input-image "path/to/input.png" [--model MODEL] [--resolution 512|1K|2K|4K] [--aspect-ratio RATIO] [--api-key KEY]
```

**Multiple input images (up to 14):**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "combine these elements" --filename "output.png" --input-image "img1.png" "img2.png" "img3.png" [--model MODEL] [--resolution 2K] [--api-key KEY]
```

**Important:** Always run from the user's current working directory so images are saved where the user is working, not in the skill directory.

## Default Workflow (draft → iterate → final)

Goal: fast iteration without burning time on 4K until the prompt is correct.

- Draft (1K): quick feedback loop
  - `uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "<draft prompt>" --filename "yyyy-mm-dd-hh-mm-ss-draft.png" --resolution 1K`
- Iterate: adjust prompt in small diffs; keep filename new per run
  - If editing: keep the same `--input-image` for every iteration until you're happy.
- Final (4K): only when prompt is locked
  - `uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "<final prompt>" --filename "yyyy-mm-dd-hh-mm-ss-final.png" --resolution 4K`

## Model Selection

Use `--model` to specify the Gemini model. Default: `gemini-3.1-flash-image-preview`.

Available models:

| Model ID | 别名 | 分辨率 | 宽高比 | 多图输入 | Thinking | Google Search Grounding | 特点 |
|---|---|---|---|---|---|---|---|
| `gemini-3.1-flash-image-preview` | Nano Banana 2 | 512 / 1K / 2K / 4K | 14 种（含 1:4, 4:1, 1:8, 8:1） | 最多 14 张（10 物体 + 4 角色） | minimal / high | Web Search + Image Search | 速度/质量/成本最佳平衡，默认推荐 |
| `gemini-3-pro-image-preview` | Nano Banana Pro | 1K / 2K / 4K | 10 种 | 最多 11 张（6 物体 + 5 角色） | 默认开启（不可关闭） | Web Search | 专业素材制作，高级推理，高保真文字渲染 |
| `gemini-2.5-flash-image` | Nano Banana | 仅 1K（1024px） | 9 种 | 最多 3 张 | 不支持 | 不支持 | 最快最便宜，适合高并发低延迟场景 |

Map user requests:
- Default / no preference → `gemini-3.1-flash-image-preview`
- "pro", "best quality", "professional" → `gemini-3-pro-image-preview`
- "fast", "cheap", "basic" → `gemini-2.5-flash-image`

## Resolution Options

Gemini 3.1 Flash Image supports four resolutions (uppercase K required, except 512):

- **512** (0.5K) - ~512px resolution (fastest, lowest cost)
- **1K** (default) - ~1024px resolution
- **2K** - ~2048px resolution
- **4K** - ~4096px resolution

Map user requests to API parameters:
- No mention of resolution → `1K`
- "thumbnail", "tiny", "preview", "0.5K", "512" → `512`
- "low resolution", "1080", "1080p", "1K" → `1K`
- "2K", "2048", "normal", "medium resolution" → `2K`
- "high resolution", "high-res", "hi-res", "4K", "ultra" → `4K`

## Aspect Ratio Options

14 aspect ratios supported. Use `--aspect-ratio` to set:

- **1:1** - Square (default if no input image)
- **1:4**, **4:1** - Extreme vertical / horizontal (new in 3.1 Flash)
- **1:8**, **8:1** - Ultra-extreme vertical / horizontal (new in 3.1 Flash)
- **2:3**, **3:2** - Classic portrait / landscape
- **3:4**, **4:3** - Standard photo portrait / landscape
- **4:5**, **5:4** - Instagram-style portrait / landscape
- **9:16**, **16:9** - Phone vertical / widescreen
- **21:9** - Ultra-widescreen / cinematic

Map user requests:
- "square" → `1:1`
- "portrait", "vertical" → `3:4` or `9:16`
- "landscape", "horizontal" → `4:3` or `16:9`
- "widescreen", "cinematic" → `16:9` or `21:9`
- "phone", "story", "reel" → `9:16`
- "banner", "ultra-wide" → `21:9`
- "tall banner", "vertical banner" → `1:4` or `1:8`
- "horizontal banner" → `4:1` or `8:1`

If no `--aspect-ratio` is specified, the model defaults to matching the input image's ratio, or 1:1 for text-to-image.

## Thinking Level

Control the model's reasoning depth with `--thinking-level`:

- **minimal** (default) - Fastest response, lowest latency
- **high** - Best quality, model reasons more deeply about composition

Use `high` for complex scenes, detailed compositions, or when quality matters more than speed. The model always uses some thinking internally; `minimal` just reduces it.

## Multiple Input Images

Nano Banana 2 supports up to 14 reference images in a single request:
- Up to 10 images of objects with high-fidelity
- Up to 4 images of characters for character consistency

Use cases:
- **Character consistency**: Provide a character reference image, generate different poses/angles
- **Composition**: Combine elements from multiple images into one scene
- **Style transfer**: Provide a style reference + content image
- **Product mockups**: Place product on different backgrounds
- **360° views**: Generate different angles of a character by providing previous outputs

Example:
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "An office group photo of these people, they are making funny faces" \
  --input-image person1.png person2.png person3.png person4.png \
  --filename "2026-03-24-10-00-00-group-photo.png" \
  --resolution 2K --aspect-ratio 5:4
```

## Image-Only Mode

Use `--image-only` to suppress text in the response and return only the generated image. Useful when you don't need the model's text commentary.

```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "a sunset" --filename "sunset.png" --image-only
```

## API Key

The script checks for API key in this order:
1. `--api-key` argument (use if user provided key in chat)
2. `GEMINI_API_KEY` environment variable

If neither is available, the script exits with an error message.

## Preflight + Common Failures (fast fixes)

- Preflight:
  - `command -v uv` (must exist)
  - `test -n "$GEMINI_API_KEY"` (or pass `--api-key`)
  - If editing: `test -f "path/to/input.png"`

- Common failures:
  - `Error: No API key provided.` → set `GEMINI_API_KEY` or pass `--api-key`
  - `Error loading input image:` → wrong path / unreadable file; verify `--input-image` points to a real image
  - `Maximum 14 input images supported.` → reduce the number of input images
  - "quota/permission/403" style API errors → wrong key, no access, or quota exceeded; try a different key/account

## Filename Generation

Generate filenames with the pattern: `yyyy-mm-dd-hh-mm-ss-name.png`

**Format:** `{timestamp}-{descriptive-name}.png`
- Timestamp: Current date/time in format `yyyy-mm-dd-hh-mm-ss` (24-hour format)
- Name: Descriptive lowercase text with hyphens
- Keep the descriptive part concise (1-5 words typically)
- Use context from user's prompt or conversation
- If unclear, use random identifier (e.g., `x9k2`, `a7b3`)

Examples:
- Prompt "A serene Japanese garden" → `2025-11-23-14-23-05-japanese-garden.png`
- Prompt "sunset over mountains" → `2025-11-23-15-30-12-sunset-mountains.png`
- Prompt "create an image of a robot" → `2025-11-23-16-45-33-robot.png`
- Unclear context → `2025-11-23-17-12-48-x9k2.png`

## Image Editing

When the user wants to modify an existing image:
1. Check if they provide an image path or reference an image in the current directory
2. Use `--input-image` parameter with the path to the image
3. The prompt should contain editing instructions (e.g., "make the sky more dramatic", "remove the person", "change to cartoon style")
4. Common editing tasks: add/remove elements, change style, adjust colors, blur background, inpainting, style transfer, sketch-to-photo, etc.

## Prompt Handling

**For generation:** Pass user's image description as-is to `--prompt`. Only rework if clearly insufficient.

**For editing:** Pass editing instructions in `--prompt` (e.g., "add a rainbow in the sky", "make it look like a watercolor painting")

Preserve user's creative intent in both cases.

## Prompt Templates (high hit-rate)

Use templates when the user is vague or when edits must be precise.

- Generation template:
  - "Create an image of: <subject>. Style: <style>. Composition: <camera/shot>. Lighting: <lighting>. Background: <background>. Color palette: <palette>. Avoid: <list>."

- Editing template (preserve everything else):
  - "Change ONLY: <single change>. Keep identical: subject, composition/crop, pose, lighting, color palette, background, text, and overall style. Do not add new objects. If text exists, keep it unchanged."

- Photorealistic template:
  - "A photorealistic [shot type] of [subject], [action or expression], set in [environment]. The scene is illuminated by [lighting description], creating a [mood] atmosphere. Captured with a [camera/lens details], emphasizing [key textures and details]."

- Inpainting template (semantic masking):
  - "Using the provided image, change only the [specific element] to [new element/description]. Keep everything else in the image exactly the same, preserving the original style, lighting, and composition."

- Style transfer template:
  - "Transform the provided photograph of [subject] into the artistic style of [artist/art style]. Preserve the original composition but render it with [description of stylistic elements]."

- Multi-image composition template:
  - "Create a new image by combining the elements from the provided images. Take the [element from image 1] and place it with/on the [element from image 2]. The final image should be a [description of the final scene]."

## Output

- Saves PNG to current directory (or specified path if filename includes directory)
- Script outputs the full path to the generated image
- **Do not read the image back** - just inform the user of the saved path
- All generated images include a SynthID watermark

## Examples

**Generate new image:**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

**Edit existing image:**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```

**Widescreen cinematic shot:**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "Epic fantasy castle on a cliff at sunset" --filename "2025-11-23-15-00-00-castle.png" --resolution 4K --aspect-ratio 21:9
```

**High-quality with deep thinking:**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "A detailed infographic explaining photosynthesis as a recipe" --filename "2025-11-23-15-30-00-infographic.png" --resolution 2K --aspect-ratio 3:4 --thinking-level high
```

**Combine multiple images:**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "Create a professional e-commerce fashion photo. Put the dress from the first image on the model from the second image" --filename "2025-11-23-16-00-00-fashion.png" --input-image dress.png model.png --resolution 2K
```

**Quick thumbnail preview:**
```bash
uv run ~/.codex/skills/nano-banana-pro/scripts/generate_image.py --prompt "Logo for a coffee shop called The Daily Grind" --filename "2025-11-23-16-30-00-logo.png" --resolution 512 --aspect-ratio 1:1 --image-only
```
