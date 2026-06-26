---
name: image-with-comfyui
description: 'Call a local ComfyUI instance for text-to-image (T2I), image-to-image/edit (I2I), and image-to-video (I2V) generation. Supports Z-Image, SD3.5 Medium, Qwen Image Edit, and Wan2.2 models with automatic prompt formatting and VRAM purge after run.'
metadata:
  openclaw:
    emoji: "🎨"
    version: "1.4.9"
    requires:
      anyBins: ["python3"]
      env:
        - COMFYUI_URL
        - COMFYUI_TIMEOUT
        - COMFYUI_POLL_INTERVAL
        - COMFYUI_OUTPUT_DIR
        - OPENCLAW_WORKSPACE
    config:
      path: "config.json"
---

# Image with ComfyUI

Call a local ComfyUI server to generate or edit images and videos. Four modes:

- **T2I** (Text → Image) → Z-Image or SD3.5 Medium model
- **I2I** (Image → Image / Edit) → Qwen Image Edit model
- **I2V** (Image → Video) → Wan2.2 model

## When to Use

- User asks to generate images from text
- User asks to edit an image
- User asks to generate a video from an image + text
- User provides a description and wants visual output

### Image-First Conversational Pattern (Image-First Mode)

**Detection rules:**
1. User sends **only an image** (no text, no other message in the same turn)
2. Within **2 minutes**, the user sends a **text message** that looks like an edit or video request (Chinese keywords like: 修一下/换背景/加个特效/变成动画/把颜色改蓝的)
3. The text intent is **I2I** (edit the image) or **I2V** (animate the image)

**Action:**
- Route the remembered image + the new text to `image_with_comfyui.py i2i` or `wan2.2` accordingly
- Use the latest image received as the `--image` input
- Use the text as the `--prompt`
- If unsure whether I2I or I2V, **default to I2I** (edit) unless the text clearly says video/animation
- Do NOT ask the user for the image again — the agent already has the image from the previous turn

**Context tracking:**
- Store the latest image media path (or URL) in a variable when no text is received
- Clear the stored image after it's used (or after 2 minutes of no new text)
- Only apply this to the **immediately preceding** message — don't look back further than 2 minutes

**Examples:**
- User: `[image: a photo of a dog]` → Agent: (wait)
- User: `[text: change the background to a beach]` → Agent: calls `i2i --image <path> --prompt "change the background to a beach"`
- User: `[image: a cat sitting on a chair]` → Agent: (wait)
- User: `[text: make it stand up and walk]` → Agent: calls `wan2.2 --image <path> --prompt "the cat stands up and walks"`

## Configuration

Read `config.json` relative to this SKILL's directory. All values can be overridden by environment variables:

| Env Variable | Overrides | Default |
|---|---|---|
| `COMFYUI_URL` | `comfyui_url` | `http://localhost:8188` |
| `COMFYUI_TIMEOUT` | `timeout_seconds` | `120` |
| `COMFYUI_POLL_INTERVAL` | `poll_interval_seconds` | `3` |
| `COMFYUI_OUTPUT_DIR` | `output_dir` | `/tmp/comfyui_output` |
| `OPENCLAW_WORKSPACE` | `workspace_root` | OpenClaw workspace dir |**Priority: Environment variables > config.json**

## Workflow Files

| Mode | Workflow | Location |
|---|---|---|
| T2I (Z-Image) | Z-Image T2I | `workflows/z-image_t2i_api.json` |
| T2I (SD3.5) | SD3.5 Medium T2I | `workflows/sd3.5-med_t2i_api.json` |
| I2I | Qwen Image Edit | `workflows/qwen_image-edit_api.json` |
| I2V | Wan2.2 Image-to-Video | `workflows/wan2.2_i2v_api.json` |

## Error Handling

The system automatically handles two types of errors:

### 1. Missing Node Detection

When a workflow references a custom node that isn't installed, the system detects it and reports:
- **Which node** is missing (class type name)
- **Which package** provides it
- **GitHub URL** for manual download
- **Manual install instruction** (the script does NOT execute git clone; ComfyUI may be on a remote server)

Example: If `ImpactKSamplerBasicPipe` is missing:
```
⚠️ Missing node: `ImpactKSamplerBasicPipe`
📦 Package: ComfyUI-Impact-Pack
🔗 GitHub: https://github.com/ltdrdata/ComfyUI-Impact-Pack
ℹ️ Install manually: cd ComfyUI/custom_nodes && git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack
```

### 2. Missing Model Substitution

When a workflow references a model file that doesn't exist, the system attempts to find a compatible substitute:

| Requested Model | Substitute |
|---|---|
| `sd3.5_medium` variants | `sd3.5_large.safetensors` |
| WAN High → Low or vice versa | Swap between variants |
| Other unknown models | No substitution (error returned) |

Example: If `my_custom_sd3_medium_v2.safetensors` is missing:
```
⚠️ Model missing: `my_custom_sd3_medium_v2.safetensors`
🔄 Substituted: `sd3.5_large.safetensors`
📦 Loader: CheckpointLoaderSimple.ckpt_name
```

After substitution, the workflow is retried automatically with the substitute model.

### 3. Missing Utility Node Bypass (UnloadAllModels)

When the workflow references `UnloadAllModels` (a memory cleanup node) which isn't available, the system **automatically bypasses it** by rerouting the signal path:
- Removes the missing `UnloadAllModels` node
- Redirects the upstream processing node directly to the downstream output node
- Generation continues without interruption
- User receives a warning about the bypass

Example:
```
⚠️ Workflow missing node: `UnloadAllModels` (memory cleanup, non-critical)
🔄 Auto-bypassed — generation continues
```

## Core Rules

1. **Send media attachment**: After generating an image or video, you **must** send it via the `message` tool using `media` or `filePath`.
2. **Send in original session**: Always deliver generated media **in the user's original request session/thread** — do not send to a separate topic, group, or thread unless explicitly told otherwise.
3. **Don't include paths**: Unless the user explicitly asks, **never** send local file paths, ComfyUI URLs, or other address info.

---

## Prompt Formatting

### Z-Image (T2I)

Z-Image works best with **structured natural language prompts**, not keyword spam.

**6-part formula:**
```
Subject + Scene + Composition + Lighting + Style + Constraints
```

**Rules:**
- ✅ Use natural language sentences (not comma-separated tags)
- ✅ Be specific about subject, camera, lighting, style
- ❌ **NO negative prompts** — Z-Image Turbo ignores them completely
- ❌ No weighted tags like `(word:1.2)`

**Example:**
```
A young woman with long wavy blonde hair sits at a wooden café table,
steam rising from a ceramic cup. Shot from a 3/4 angle, close-up framing.
Soft morning light filters through sheer curtains, casting warm golden tones.
Cinematic photography, shallow depth of field, Kodak Portra 400 aesthetic.
No text, no logos, photorealistic skin texture.
```

**Aspect ratios:** `1:1`, `4:3`, `3:4`, `16:9`, `9:16`, `3:2`, `2:3`

---

### SD3.5 Medium (T2I)

SD3.5 Medium uses **natural language prompts** with optional negative prompts.

**Prompt formula:**
```
[Composition/Angle] + [Subject] + [Scene/Environment] + [Lighting/Color] + [Style/Texture] + [Details]
```

**Rules:**
- ✅ **Complete natural language sentences** — describe like telling a human what to see
- ✅ Subject first (model prioritizes early text)
- ✅ Be specific about colors, materials, mood, atmosphere
- ✅ Mixed CN/EN is fine (Chinese works better for Chinese scenes)
- ✅ Use `--negative` for elements to exclude
- ✅ Default 1:1 (1024×1024), use `--aspect` to change
- ✅ Default 20 steps, CFG 4.01 (higher = stronger control)
- ✅ Seed defaults to random; specify `--seed` for reproducibility
- ❌ No comma-separated keyword spam (`beautiful, amazing, 4k`)
- ❌ No weighted tags `(word:1.2)` — SD3.5 doesn't recognize them

**Parameter recommendations:**
- **CFG**: 4-7 (4.01 = softer, 5-7 = stronger control)
- **Steps**: 20-25 (below 20 may lack detail)
- **Negative prompt**: Highly effective in SD3.5

**Common negative prompt words:**
```
blurry, low quality, pixelated, grainy,
overexposed, underexposed, flat lighting,
text, watermark, logo, signature, caption,
poorly drawn face, deformed, mutated, disfigured, extra limbs,
cartoonish (when realism is wanted)
```

**Chinese example:**
```
上海魔都春日花海 — 黄浦江畔，大片郁金香、樱花、油菜花盛开，繁花似锦，
春日和煦阳光，远景陆家嘴三件套天际线，湿润的滨江步道倒映花影，
低饱和胶片色调，文艺清新，广角视野
```

**English example:**
```
Cinematic photography, wide-angle shot of a bustling Tokyo street at night,
neon signs reflecting on wet pavement, people with transparent umbrellas,
moody atmospheric lighting, deep blues and vibrant reds, street photography,
shallow depth of field with bokeh background
```

---

### Qwen Image Edit (I2I) — Concise Prompts

I2I prompts must be **concise and direct**. Keep the user's original language.

**Rules:**
- ✅ **Positive prompt only** — no negative prompts
- ✅ Use user's exact words (don't translate or expand)
- ✅ Concise: "换件红色外套", "把背景换成蓝天白云", "将女孩换成男孩"
- ❌ Don't translate between languages
- ❌ Don't over-explain or add details

**Prompt routing fix (2026-04-22):**
- The Qwen workflow has TWO `TextEncodeQwenImageEditPlus` nodes:
  - `115:110` — empty negative prompt node
  - `115:111` — positive prompt node (contains default text like "the girl")
- Script must route prompts to **node 111 (positive)**, not node 110
- The `prepare_i2i_workflow()` function auto-detects by scanning for existing default text

---

### Wan2.2 I2V (Image → Video)

Wan2.2 generates short videos (~5 seconds) from a static image + motion description.

**Rules:**
- ✅ Prompt describes **actions/movement** (not scene description)
- ✅ Write motion description in English for best results
- ✅ Focus on "who does what" and "how the camera moves"
- ❌ Don't describe static scene elements in motion prompt

- Default: 81 frames (~5s @ 16fps), 4 steps, CFG 4.5
- Base resolution: **560×720** (3:4, fast and OK quality)
- Auto-detect input image aspect ratio and select reference resolution:

### Resolution Reference

| Aspect | Fast & OK | User Fav | WAN 2.2 Native |
|--------|-----------|----------|----------------|
| 3:4 | 560×720 | 720×912 | 848×1088 |
| 2:3 | 528×768 | 656×960 | 784×1136 |
| 9:16 | 480×848 | 608×1072 | 720×1264 |

Other available resolutions:
- **3:4**: 416×544, 672×864, 784×1008
- **2:3**: 384×576, 624×912, 736×1072
- **9:16**: 368×624, 576×1008, 672×1184

**Examples:**
```
prompt: "the cat walks forward and looks at the camera, tail wagging"
prompt: "the girl smiles and turns her head, wind blowing her hair"
prompt: "the person stands in a busy street, camera pans left and slowly zooms in, cars driving, red flag fluttering"
```

---

## CLI Usage

### T2I (Text → Image)

```bash
# Z-Image (default model)
python3 image_with_comfyui.py t2i \
  --prompt "Your detailed image description" \
  --aspect 16:9 \
  --steps 9

# SD3.5 Medium
python3 image_with_comfyui.py sd35 \
  --prompt "A beautiful sunset over mountains" \
  --aspect 16:9 \
  --negative "text, watermark, blurry" \
  --steps 20 \
  --cfg 5.5
```

### I2I (Edit Image)

```bash
python3 image_with_comfyui.py i2i \
  --prompt "Change background to a beach" \
  --image /path/to/source.jpg \
  --steps 4
```

### I2V (Image → Video)

```bash
python3 image_with_comfyui.py wan2.2 \
  --prompt "the person walks forward and smiles" \
  --image /path/to/source.jpg \
  --length 81 --steps 4
```

### Health Check

```bash
python3 image_with_comfyui.py test
```

---

## Output Delivery

**Send the media attachment directly. Be minimal.**

### 🚨 Delivery Rules

**⚠️ Absolutely forbidden: Only writing text descriptions without actually sending files!**

**✅ Correct approach: Send MEDIA path with the appropriate prefix for the current Channel**

| Channel | Format | Example |
|---------|--------|---------||
| **WhatsApp** | `MEDIA:./image.jpg` | `MEDIA:./angel_video.mp4` |
| Telegram | `MEDIA:` or `filePath:` | Varies by implementation |
| Discord | Direct attachment | Varies by implementation |

**Rules:**
1. When sending images/videos/audio on WhatsApp, **must** add `MEDIA:` prefix + relative path
2. Place files in `./media/outbound/` directory to ensure accessibility
3. Don't just write text descriptions like "video attachment" — that does not equal sending a file
4. First `cp` the file to `~/.openclaw/media/outbound/`, then send via `MEDIA:`
5. Other Channels use their corresponding formats (see respective Channel docs)
6. **Default to sending to the requesting session**: Generated images/videos must be sent back to the session that initiated the request, unless the user explicitly says "don't send" or "only save locally"
7. **Pure MEDIA line for WhatsApp — no text prefix**: The `MEDIA:` line must be the **sole content of the message**, with no `[[reply_to_current]]`, text, or anything else before it. Otherwise WhatsApp splits the text and attachment into two separate messages, making it look like "sent twice". If caption text is needed, use `MEDIA:./file.ext caption=description` format.

### Example delivery

**WhatsApp:**
```
MEDIA:./output_image.png
```

**Universal：**
```
[📎 Image attachment via MEDIA prefix]
```

**Never replace actual file sending with text descriptions!**

---

## Timeout Reference

| Model | Timeout |
|---|---|
| T2I (Z-Image) | 100s |
| SD3.5 Medium | 100s |
| I2I (Qwen) | 600s |
| I2V (Wan2.2) | 1000s |

---

## Additional Notes

- **ComfyUI unreachable** → report error with URL tried
- **Generation fails** (empty output) → report prompt_id for debugging
- **Missing required node** → report which node was not found
- **Timeout** → report elapsed time and prompt_id
