---
name: ModelScope-Img
description: Generate images with ModelScope API. Use for image generation requests. Supports text-to-image + image-to-image; configurable models; use --input-image.
---

# ModelScope Image Generation

Generate new images or edit existing ones using ModelScope's community models.

## ⚠️ Security Notice

**This tool ONLY connects to the official ModelScope API endpoint.**

- **Fixed Endpoint**: `https://api-inference.modelscope.cn/`
- **Endpoint is NOT configurable**: There is NO ability to customize or redirect the API endpoint
- This prevents any possibility of API key or data being redirected to untrusted servers

## Prerequisites

**Required before use:**
1. **ModelScope API Key** - Get from https://modelscope.cn
   - Set as environment variable: `export MODELSCOPE_API_KEY="your-key-here"`
   - Or pass directly: `--api-key "your-key-here"`
2. **uv** - Python package manager (install via `pip install uv`)
3. **Python 3.10+** - Required runtime

**Python dependencies** (auto-installed by uv):
- requests>=2.31.0
- pillow>=10.0.0

## Usage

Run the script using absolute path (do NOT cd to skill directory first):

**Generate new image:**
```bash
uv run ~/.codex/skills/ModelScope_img_generator/scripts/generate_img.py --prompt "your image description" --filename "output-name.jpg" [--model MODEL_ID] [--api-key KEY]
```

**Edit existing image:**
```bash
uv run ~/.codex/skills/ModelScope_img_generator/scripts/generate_img.py --prompt "editing instructions" --filename "output-name.jpg" --input-image "path/to/input.jpg" [--model MODEL_ID] [--api-key KEY]
```

**Important:** Always run from the user's current working directory so images are saved where the user is working, not in the skill directory.

## Models

The script supports various ModelScope community models. Use `--model` to specify:

- **Default:** `Tongyi-MAI/Z-Image-Turbo` (fast, good quality)
- **Other options:** Browse [ModelScope Model Hub](https://modelscope.cn/models) for more image generation models

Popular alternatives:
- `MusePublic/wukong-1.8B` - Chinese style
- Other community models available on ModelScope

## LoRA Support

Enhance generation with LoRA adapters using `--lora`:

```bash
# Single LoRA
uv run ~/.codex/skills/ModelScope_img_generator/scripts/generate_img.py --prompt "anime girl" --filename output.jpg --lora "my-lora-repo"

# Multiple LoRAs with weights (must sum to 1.0)
uv run ~/.codex/skills/ModelScope_img_generator/scripts/generate_img.py --prompt "anime girl" --filename output.jpg --lora "lora1:0.6,lora2:0.4"
```

## API Key

The script checks for API key in this order:
1. `--api-key` argument (use if user provided key in chat)
2. `MODELSCOPE_API_KEY` environment variable

If neither is available, the script exits with an error message.

## Preflight + Common Failures (fast fixes)

- Preflight:
  - `command -v uv` (must exist)
  - `test -n "$MODELSCOPE_API_KEY"` (or pass `--api-key`)
  - If editing: `test -f "path/to/input.jpg"`

- Common failures:
  - `Error: No API key provided.` → set `MODELSCOPE_API_KEY` or pass `--api-key`
  - `Error: Input image not found:` → wrong path / unreadable file; verify `--input-image` points to a real image
  - API errors → wrong key, no access, or model not available; try a different key or model
  - Task timeout → generation took too long; try a simpler prompt or different model

## Filename Generation

Generate filenames with the pattern: `yyyy-mm-dd-hh-mm-ss-name.jpg`

**Format:** `{timestamp}-{descriptive-name}.jpg`
- Timestamp: Current date/time in format `yyyy-mm-dd-hh-mm-ss` (24-hour format)
- Name: Descriptive lowercase text with hyphens
- Keep the descriptive part concise (1-5 words typically)
- Use context from user's prompt or conversation
- If unclear, use random identifier (e.g., `x9k2`, `a7b3`)

Examples:
- Prompt "A serene Japanese garden" → `2025-11-23-14-23-05-japanese-garden.jpg`
- Prompt "sunset over mountains" → `2025-11-23-15-30-12-sunset-mountains.jpg`
- Prompt "create an image of a robot" → `2025-11-23-16-45-33-robot.jpg`
- Unclear context → `2025-11-23-17-12-48-x9k2.jpg`

## Image Editing

When the user wants to modify an existing image:
1. Check if they provide an image path or reference an image in the current directory
2. Use `--input-image` parameter with the path to the image
3. The prompt should contain editing instructions (e.g., "make the sky more dramatic", "remove the person", "change to cartoon style")
4. Common editing tasks: add/remove elements, change style, adjust colors, blur background, etc.

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

## Output

- Saves image to current directory (or specified path if filename includes directory)
- Script outputs the full path to the generated image
- **Do not read the image back** - just inform the user of the saved path

## Examples

**Generate new image:**
```bash
uv run ~/.codex/skills/ModelScope_img_generator/scripts/generate_img.py --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.jpg"
```

**Generate with specific model:**
```bash
uv run ~/.codex/skills/ModelScope_img_generator/scripts/generate_img.py --prompt "Chinese ink painting landscape" --filename "ink-landscape.jpg" --model "MusePublic/wukong-1.8B"
```

**Edit existing image:**
```bash
uv run ~/.codex/skills/ModelScope_img_generator/scripts/generate_img.py --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.jpg" --input-image "original-photo.jpg"
```

**Generate with LoRA:**
```bash
uv run ~/.codex/skills/ModelScope_img_generator/scripts/generate_img.py --prompt "anime style portrait" --filename "anime-portrait.jpg" --lora "anime-lora:0.8"
```
