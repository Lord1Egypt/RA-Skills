## Deprecated

This file is now a compatibility index.

Use these focused references instead:

- [`contracts/create-task.md`](contracts/create-task.md)
- [`contracts/payload-rules.md`](contracts/payload-rules.md)
- [`flows/reference-image-to-video.md`](flows/reference-image-to-video.md)
- [`flows/text-to-video.md`](flows/text-to-video.md)
- [`limits/reference-media-rules.md`](limits/reference-media-rules.md)
- [`protocols/execution.md`](protocols/execution.md)
- [`protocols/event-stream.md`](protocols/event-stream.md)
- [`support/faq.md`](support/faq.md)
- [`support/troubleshooting.md`](support/troubleshooting.md)

## 🔊 Audio Generation Capability

**Seedance 2.0 supports optional audio generation via the `audio` parameter.**

### Audio Output Modes

| Mode | Parameter Setting | Output Behavior |
|------|------------------|-----------------|
| **Video with Audio** (Default) | `audio=true` or omitted | Video includes AI-generated audio/sound effects matching the visual content |
| **Silent Video** | `audio=false` | Video contains visual frames only, no audio track |

### Audio Input vs Audio Output (CRITICAL DISTINCTION)

**🎤 Audio Input** (via `reference_image_to_video` task type):
- **Purpose**: Use audio file as **reference for visual generation**
- **Input**: Upload .mp3/.wav/.m4a file to `--input-images`
- **Output**: Video visuals that match the audio's mood/rhythm/emotion
- **Use Cases**: Music visualization, rhythm-driven animation, mood-based generation
- **Example**: Generate abstract visuals that pulse/move to music beats
- **Important**: External audio input support means **reference conditioning**, not guaranteed final soundtrack preservation
- **Current behavior**: audio references are strictly validated before task creation and also go through asset compliance verification

**🔊 Audio Output** (via `audio` parameter):
- **Purpose**: AI-generated audio track **in the final video**
- **Default**: `audio=true` (audio **enabled by default**)
- **Disable**: Set `--extra-params '{"audio": false}'` for silent video
- **Output**: Video with embedded audio (background ambience, sound effects, atmospheric audio)
- **Use Cases**: Videos needing ambient sound, environmental audio, basic sound design
- **Note**: Generated audio is NOT voiceover/narration, but atmospheric/environmental sound
- **Important**: This is not the same as “use my uploaded MP3 as the final narration track”

**⚠️ Important**:
- These are **independent features** - you can use neither, one, or both
- **Audio Input** → Reference for **generating visuals**
- **Audio Output** → AI-generated **audio in final video**
- Combining both: Use audio file as visual reference AND generate new audio for output
- If the requirement is “final video must contain this exact uploaded narration/music file,” plan for separate composition/post-processing unless the API explicitly proves otherwise

### Audio Generation Limitations

**What `audio=true` DOES generate**:
- ✅ Background ambience (e.g., forest sounds, city noise)
- ✅ Environmental audio matching visuals (e.g., rain, wind)
- ✅ Basic sound effects (e.g., footsteps, object sounds)
- ✅ Atmospheric audio enhancing mood

**What `audio=true` does NOT generate**:
- ❌ Voiceover or narration (human speech)
- ❌ Specific background music tracks
- ❌ Dialogue or character speech
- ❌ Licensed music or copyrighted content

**For voiceover/narration**: Use separate text-to-speech tools and post-production editing.

---

## ⚠️ CRITICAL: Audio Capability Boundary

- The API can accept image/video/audio **reference inputs** for `reference_image_to_video`
- The `audio` parameter can request AI-generated ambient audio in the final output
- The current documented capability does **not** prove support for preserving an uploaded narration file as the final mixed soundtrack

---

## Supported Models

Only two models are exposed by this skill:

| Friendly Name | model_id | Positioning | Typical Time |
|---------------|----------|-------------|--------------|
| **Seedance 2.0** | `ima-pro` | Quality priority | 300~900s |
| **Seedance 2.0 Fast** | `ima-pro-fast` | Speed priority | 120~600s |

**Aliases:**
- IMA Video Pro = `ima-pro`
- IMA Video Pro Fast = `ima-pro-fast`

---

## 🔎 SEO Search Intent Coverage

This project can be positioned for the following search intents while still mapping to the same two models and four task types:

| Search intent | How Seedance 2.0 fits |
|---------------|-----------------------|
| `Seedance 2.0 video generator` | General-purpose AI video generator for prompt-driven video creation |
| `Seedance 2.0 text to video` | Use `text_to_video` for pure prompt-based generation |
| `Seedance 2.0 image to video` | Use `image_to_video` when one image should act as the first frame |
| `cinematic video generator` / `AI cinematic video` | Best fit for `ima-pro` with strong camera language and quality-first prompts |
| `multi-shot video generator` / `AI short film generator` | Best fit for repeated shot creation with reference-image workflows and consistency guidance |
| `consistent character video` | Use reference media plus consistency-oriented prompting |
| `camera motion video` | Seedance 2.0 supports push, pull, pan, tilt, track, and crane-style motion prompts |
| `storyboard to video` / `AI storytelling video` | Works well for converting shot descriptions, beat lists, and scene prompts into clips |
| `AI commercial video generator` / `AI ad video generator` | Strong fit for product launches, branded spots, and promo sequences |
| `AI music video generator` / `AI product video generator` / `AI short clip generator` | Good fit for rapid concepting, social edits, visualizers, and product demos |

---

## 🎯 Skill Capabilities

### Seedance 2.0 (Quality Priority | 质量优先)
- **Positioning | 定位**: Final production, texture priority, high camera language requirements, cinematic video generator work | 正式出片、质感优先、镜头语言要求高、电影感视频任务
- **Best for | 适合**: Ad shots, character narratives, stylized shorts, AI short film generator flows, AI commercial video generator work, scenes requiring high consistency | 广告镜头、角色叙事、风格化短片、AI 短片、商业广告、需要更高一致性的镜头段落

### Seedance 2.0 Fast (Speed Priority | 速度优先)
- **Positioning | 定位**: Rapid prototyping, batch style testing, creative iteration, storyboard to video exploration | 快速打样、批量试风格、创意迭代、分镜到视频探索
- **Best for | 适合**: Proposal-stage A/B versions, shot previews, low-latency validation, AI short clip generator use cases, AI music video generator concepting | 提案阶段 A/B 版本、镜头预演、低延迟验证、短视频、音乐视频概念打样

### Ability Positioning

- **Temporal & Subject Consistency | 时序与主体一致性**: High stability in continuous motion and subject retention | 在连续动作和主体保持上具备高稳定性表现
- **Camera Language Control | 镜头语言控制**: Supports push/pull/pan/tilt/track/crane driven by description | 支持对推拉摇移、节奏和运动感的描述驱动
- **Multimodal Conditioning | 多模态条件理解**: Combines text and reference materials for generation | 可结合文本与参考素材进行生成
- **High-Quality Output Focus | 高质量输出取向**: Targets high-resolution, high-quality video output | 面向高分辨率、高观感视频产出
- **Story and Shot Planning Friendly | 分镜与叙事友好**: Useful for storyboard to video prompts, multi-shot video generator workflows, and consistent character video pipelines | 适合分镜脚本、多镜头视频和角色一致性视频流程

---

## Workflow Coverage

| task_type | Description (EN / 中文) | Input |
|-----------|-------------------------|-------|
| `text_to_video` | Text to video generation / 文本直接生成视频 | prompt only |
| `image_to_video` | Image as first frame drives motion / 以首帧图驱动动态生成 | prompt + 1 image |
| `first_last_frame_to_video` | First+last frames constrain transition / 以首尾帧约束过渡与收束 | prompt + 2 images |
| `reference_image_to_video` | Reference media constrains style/subject / 以参考媒体约束风格/主体特征 | prompt + 1 image/video/audio 🆕 |

---

## Strict Input Validation For `reference_image_to_video`

Before task creation, validate all reference media. If any item fails, stop and ask the user to adjust inputs.

### Reference images

- Count: `1~9`
- Formats: `jpeg`, `png`, `webp`, `bmp`, `tiff`, `gif`
- Width / height: `300~6000 px`
- Aspect ratio: `0.4~2.5`
- Size: single image `< 30MB`

### Reference videos

- Count: `0~3`
- Formats: `mp4`, `mov`
- Duration: single video `2~15s`
- Total duration: all videos total `<= 15s`
- Width / height: `300~6000 px`
- Aspect ratio: `0.4~2.5`
- Pixels: `409600~927408`
- FPS: `24~60`
- Size: single video `<= 50MB`

### Reference audio

- Count: `0~3`
- Formats: `wav`, `mp3`
- Duration: single audio `2~15s`
- Total duration: all audio total `<= 15s`
- Size: single audio `<= 15MB`

### Remote URL policy

- Remote image/video/audio URLs must be probed successfully for metadata before task creation
- If metadata probe fails, stop and ask the user to provide a direct downloadable URL or a local file

### User-facing behavior

If validation fails, report:

1. which file failed
2. the current value
3. the allowed range
4. how the user should adjust it

Do **not** continue to upload / verify / create the task after validation failure.

## Asset Compliance Verification Scope

- **Image references**: verify
- **Video references**: verify
- **Audio references**: verify

All reference media still go through strict preflight validation before compliance verification.

---

## Estimated Generation Time

| Model | Estimated Time | Poll Every | Send Progress Every |
|-------|---------------|------------|---------------------|
| **ima-pro** | 300~900s | 8s | 45s |
| **ima-pro-fast** | 120~600s | 8s | 30s |

**Polling timeout:** 40 minutes (2400s)

---

## 💬 User Experience Protocol

### 🚫 Never Say to Users

| ❌ Never say | ✅ What users care about |
|-------------|--------------------------|
| `ima_video_create.py` / script / 脚本 | — |
| attribute_id / model_version / form_config | — |
| API calls / HTTP requests / API 调用 / HTTP 请求 / Any technical parameter names / 任何技术参数名 | — |

### UX Flow

**1. Pre-generation:**
- EN: "🎬 Starting video generation... Model: [Name], Est. [X~Y]s, Cost: [N] credits"
- 中文: "🎬 开始生成视频… 模型：[Name]，预计[X~Y]秒，消耗[N]积分"

**2. Progress (every 30-45s):**
- EN: "⏳ Generating... [P]%" (cap at 95%)
- 中文: "⏳ 正在生成中… [P]%" (cap at 95%)

**3. Success:**
Send video via `media=video_url` + caption with link

**4. Failure:**
Natural language error + suggest alternatives

**Progress formula:**
```
P = min(95, floor(elapsed_seconds / estimated_max_seconds * 100))
```

---

## ⚠️ Error Message Translation

| Technical Error | ✅ Say Instead (Chinese / 中文) | ✅ Say Instead (English / EN) |
|----------------|-------------------------------|------------------------------|
| `401 Unauthorized` | ❌ API密钥无效<br>💡 https://www.imaclaw.ai/imaclaw/apikey | ❌ API key invalid<br>💡 https://www.imaclaw.ai/imaclaw/apikey |
| `4008 Insufficient points` | ❌ 积分不足<br>💡 https://www.imaclaw.ai/imaclaw/subscription | ❌ Insufficient points<br>💡 https://www.imaclaw.ai/imaclaw/subscription |
| `500` | 服务器异常，正在重试 | Server error, retrying |
| `6009` | 参数缺失，正在自动补全 | Missing params, auto-completing |
| `6010` | 参数不匹配，正在调整 | Params mismatch, adjusting |
| `timeout` | 生成超时，请查看创作记录 | Timed out, check creation history |

**Fallback suggestion table:**

| Failed model | First alt | Second alt |
|--------------|-----------|------------|
| `ima-pro` | `ima-pro-fast` | `ima-pro` (retry with downgraded params) |
| `ima-pro-fast` | `ima-pro` | `ima-pro-fast` (retry with defaults) |

---

## 📥 User Input Parsing

### User phrasing → task_type

| User intent | task_type |
|-------------|-----------|
| Only text | `text_to_video` |
| One image as first frame | `image_to_video` |
| One image/video/audio as reference | `reference_image_to_video` 🆕 |
| Two images with explicit first+last-frame intent | `first_last_frame_to_video` |

**🆕 CRITICAL**: If input contains video (.mp4/.mov/.webm) or audio (.mp3/.wav/.m4a), **ALWAYS use `reference_image_to_video`**
**🆕 CRITICAL**: If user does not explicitly request first-last-frame mode, 2 or more images should default to `reference_image_to_video`.

### User phrasing → model_id

| User says | model_id |
|-----------|----------|
| `ima-pro`, `pro`, `专业版`, `高质量`, `seedance 2.0`, `seedance` | `ima-pro` |
| `ima-pro-fast`, `fast`, `极速`, `快速`, `seedance 2.0 fast`, `seedance fast` | `ima-pro-fast` |
| "默认" / "推荐" / "自动" | `ima-pro` |

### User phrasing → parameters

| User says | Parameter | Value |
|-----------|-----------|-------|
| 5秒 / 5s | duration | 5 |
| 10秒 / 10s | duration | 10 |
| 15秒 / 15s | duration | 15 |
| 横屏 / 16:9 | aspect_ratio | 16:9 |
| 竖屏 / 9:16 | aspect_ratio | 9:16 |
| 正方形 / 1:1 | aspect_ratio | 1:1 |
| 4:3 | aspect_ratio | 4:3 |
| 3:4 | aspect_ratio | 3:4 |
| 超宽屏 / 21:9 | aspect_ratio | 21:9 |
| 自适应 / adaptive | aspect_ratio | adaptive |
| 480P | resolution | 480P |
| 720P | resolution | 720P |

---

## 🌐 Network Endpoints

### Production Environment (Default)

| Domain | Purpose | What's Sent |
|--------|---------|-------------|
| `api.imastudio.com` | Task create + polling | prompt, model params, task IDs, API key |
| `imapi.liveme.com` | Media upload | media bytes, API key |

### Environment Configuration

This skill is configured for **Production Environment** only.

```bash
# Production environment (default and only)
python3 ima_video_create.py --prompt "test prompt" --model-id ima-pro
```

**Base URLs:**
- API: `https://api.imastudio.com`
- Upload: `https://imapi.liveme.com`

---

## 🔐 Security & Privacy

### Credentials
- **API Key**: Required, user-provided via `--api-key` or `IMA_API_KEY` env var
- **APP_ID/APP_KEY**: Hardcoded in `ima_constants.py` for upload signature generation
  - These are public constants, not secrets
  - Same keys used by all IMA web/mobile clients
  - Visible in browser DevTools and app decompilation
  - Used only for request signing, not authentication

### Data Flow
1. **Text prompts** → sent to `api.imastudio.com`
2. **Media files** → uploaded to `imapi.liveme.com`, returns URLs
3. **Task creation** → sends prompt + media reference URLs to `api.imastudio.com`
4. **Generated videos** → returned as URLs from IMA CDN

**No data is stored locally except:**
- Preferences in `~/.openclaw/memory/ima_prefs.json`
- Logs in `logs/ima_video_*.log`

See [SECURITY.md](SECURITY.md) for complete security details.

---

## 📊 Model Parameters Structure

### Product List Response

When you call `list_models()`, the API returns models with this structure:

```json
{
  "model_id": "ima-pro",
  "model_name": "Seedance 2.0",
  "model_version": "ima-pro",
  "app": "ima",
  "platform": "web",
  "category": "text_to_video",
  "all_credit_rules": [
    {
      "attribute_id": 1234,
      "points": 25,
      "attributes": {
        "resolution": "720P",
        "duration": 5,
        "aspect_ratio": "16:9"
      }
    }
  ],
  "form_params": {
    "prompt": "",
    "duration": 5,
    "resolution": "720P",
    "aspect_ratio": "16:9",
    "n": 1
  }
}
```

**Key fields:**
- `all_credit_rules`: List of valid parameter combinations with costs
- `form_params`: Default parameters for this model
- `attribute_id`: Links to specific credit rule (auto-selected by script)

---

## 🔄 Task Creation Flow

### 1. Select Model

```python
from ima_param_resolver import list_models

models = list_models(base_url, api_key)
ima_pro = next(m for m in models if m["model_id"] == "ima-pro")
```

### 2. Merge Parameters

```python
# Start with model defaults
params = dict(ima_pro["form_params"])

# Override with user preferences
params.update({"resolution": "720P", "duration": 10})

# Select matching credit rule
from ima_param_resolver import select_credit_rule_by_params
rule = select_credit_rule_by_params(ima_pro["all_credit_rules"], params)
```

### 3. Create Task

```python
from ima_api_client import create_task

task_id = create_task(
    base_url=base_url,
    api_key=api_key,
    task_type="text_to_video",
    model_params={
        **ima_pro,
        "attribute_id": rule["attribute_id"],
        "credit": rule["points"]
    },
    prompt="a puppy dancing",
    extra_params=params
)
```

### 4. Poll Until Complete

```python
from ima_api_client import poll_task

video_url = poll_task(
    base_url=base_url,
    api_key=api_key,
    task_id=task_id,
    task_type="text_to_video",
    model_name="Seedance 2.0"
)
```

---

## 🧪 Example: Complete Task Creation

### Request Body Structure

```json
{
  "product_id": "ima-pro",
  "tasks": [{
    "model_id": "ima-pro",
    "model_name": "Seedance 2.0",
    "model_version": "ima-pro",
    "app": "ima",
    "platform": "web",
    "category": "text_to_video",
    "credit": 25,
    "parameters": {
      "prompt": "a puppy dancing happily",
      "duration": 5,
      "resolution": "720P",
      "aspect_ratio": "16:9",
      "n": 1,
      "input_images": [],
      "cast": {"points": 25, "attribute_id": 1234}
    }
  }]
}
```

### Task Detail Response

| Field | Meaning |
|-------|---------|
| `resource_status` | 0/null=processing, 1=ready, 2=failed, 3=deleted |
| `status` | "pending" / "processing" / "success" / "failed" |
| `url` | Video URL when resource_status=1 |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Polling too fast | Use 8s interval |
| Missing nested fields | Include `prompt`, `cast`, `n` |
| Credit/attribute mismatch | Query product list first |
| Inconsistent `src_img_url` and `input_images` | Keep them consistent |
| Wrong mode choice | `image_to_video` ≠ `reference_image_to_video` (see media type guide below) |

**Media Type Guide for `reference_image_to_video`:**
- **Images**: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif` - Use as style/subject reference
- **Videos**: `.mp4`, `.mov`, `.webm`, `.avi`, `.mkv` - Extract style/motion reference
- **Audio**: `.mp3`, `.wav`, `.m4a`, `.aac`, `.ogg` - Generate visuals matching audio mood/rhythm

**When to use `reference_image_to_video` vs `image_to_video`:**
- `image_to_video`: Image becomes **first frame** (动画从这张图开始)
- `reference_image_to_video`: Media provides **style/subject reference** (风格/主体参考，不是首帧)

---

## 🚀 CLI Usage (Recommended)

The modularized script provides a clean command-line interface:

```bash
# Basic text-to-video
python3 ima_video_create.py --prompt "a puppy dancing happily"

# With model selection
python3 ima_video_create.py \
  --prompt "cyberpunk city at night" \
  --model-id ima-pro-fast

# Image-to-video (first frame)
python3 ima_video_create.py \
  --prompt "gentle waves rolling" \
  --input-images https://example.com/beach.jpg

# First + last frame (explicit task_type required)
python3 ima_video_create.py \
  --task-type first_last_frame_to_video \
  --prompt "character transformation sequence" \
  --input-images https://example.com/before.jpg https://example.com/after.jpg

# Multiple images without explicit first-last-frame intent default to reference mode
python3 ima_video_create.py \
  --prompt "keep the same character across shots" \
  --input-images https://example.com/shot1.jpg https://example.com/shot2.jpg

# Reference image (style/subject consistency, auto-inferred from --reference-image)
python3 ima_video_create.py \
  --prompt "character walking through forest" \
  --reference-image https://example.com/character.jpg

# Image + video references
python3 ima_video_create.py \
  --prompt "keep the product identity while extending the original motion" \
  --reference-image https://example.com/product.jpg \
  --reference-video https://example.com/clip.mp4 \
  --model-id ima-pro-fast

# Image + audio references
python3 ima_video_create.py \
  --prompt "generate visuals matching the narration mood while preserving the character look" \
  --reference-image https://example.com/character.jpg \
  --reference-audio https://example.com/narration.mp3 \
  --model-id ima-pro-fast

# Image + video + audio references
python3 ima_video_create.py \
  --prompt "create a polished 15-second ad using the product image, motion reference, and narration rhythm" \
  --reference-image https://example.com/product.jpg \
  --reference-video https://example.com/clip.mp4 \
  --reference-audio https://example.com/narration.mp3 \
  --model-id ima-pro-fast \
  --extra-params '{"duration": 15, "aspect_ratio": "9:16", "audio": true}'

# Video + audio references
python3 ima_video_create.py \
  --prompt "generate new visuals that follow the source motion and narration pacing" \
  --reference-video https://example.com/clip.mp4 \
  --reference-audio https://example.com/narration.mp3 \
  --model-id ima-pro-fast

# Reference video (auto-inferred from --reference-video)
python3 ima_video_create.py \
  --prompt "extend the original motion with a cinematic continuation" \
  --reference-video https://example.com/clip.mp4

# Reference audio (auto-inferred from --reference-audio)
python3 ima_video_create.py \
  --prompt "generate visuals that follow the narration rhythm and mood" \
  --reference-audio https://example.com/narration.mp3

# Custom parameters (JSON format required)
python3 ima_video_create.py \
  --prompt "dancing robot" \
  --extra-params '{"duration": 10, "aspect_ratio": "16:9"}'

# Text to video WITHOUT audio
python3 ima_video_create.py \
  --prompt "cinematic scene" \
  --model-id ima-pro \
  --extra-params '{"audio": false}'

# List available models
python3 ima_video_create.py \
  --api-key ima_xxx \
  --task-type text_to_video \
  --list-models
```

---

## 🐍 Python Integration

### Basic Usage

```python
from ima_video_create import main as create_video

# Simple text-to-video
result = create_video(
    prompt="a puppy dancing happily",
    api_key="your-api-key-here"
)
print(f"Video URL: {result['url']}")
```

### Advanced Usage

```python
# Image-to-video with custom parameters
result = create_video(
    prompt="waves crashing on shore",
    api_key="your-api-key-here",
    model_id="ima-pro",
    input_images=["https://example.com/beach.jpg"],
    extra_params={
        "duration": 10,
        "resolution": "720P",
        "aspect_ratio": "16:9"
    }
)
```

### Error Handling

**Basic exception handling:**
```python
try:
    result = create_video(
        prompt="test",
        api_key="invalid-key"
    )
except RuntimeError as e:
    if "401" in str(e):
        print("Invalid API key")
    elif "4008" in str(e):
        print("Insufficient credits")
    else:
        print(f"Error: {e}")
```

**Critical Rule: Requirement Validation**

When user requirements cannot be met, **STOP execution immediately**:

```python
# ❌ WRONG: Silently downgrade requirements
user_requires_image = "use this image" in user_input.lower()
if asset_verification_fails and user_requires_image:
    # Don't do this:
    task_type = "text_to_video"  # Silent downgrade
    create_video(prompt, task_type=task_type)

# ✅ CORRECT: Stop and report
if asset_verification_fails and user_requires_image:
    raise RequirementNotMetError(
        requirement="Image input (user requested: 'use this image')",
        issue="Asset verification API returned 500",
        api="/open/v1/assets/verify",
        http_status=500,
        error_code=400,
        error_message="Invalid parameter",
        options=[
            "A. Use production environment (requires prod API key)",
            "B. Wait for test environment fix (contact IMA support)",
            "C. Accept text-only video (⚠️ No character consistency)"
        ]
    )
```

**Error Response Template**

```python
def format_requirement_error(requirement, issue, details, options):
    return f"""
❌ Cannot complete task

Your requirement: {requirement}
Issue: {issue}

Error details:
{details}

Available options:
{chr(10).join(options)}

Which option do you prefer?
"""
```

**Common Scenarios**

| User Input | Required Task Type | If Verification Fails | Action |
|------------|-------------------|----------------------|--------|
| "use this image" | image_to_video | ❌ STOP | Report + options |
| "reference this photo" | reference_image_to_video | ❌ STOP | Report + options |
| "keep character consistent" | image_to_video | ❌ STOP | Report + options |
| "generate video" (no image) | text_to_video | ✅ Continue | No image needed |

```python
# Production-only configuration
params = {
    "app": "ima",
    "platform": "web",
    "category": task_type,
    "model_ids": "ima-pro,ima-pro-fast"
}
```

---

## 📦 Module Structure

```
scripts/
├── ima_video_create.py      # Main CLI entry + high-level API
├── ima_api_client.py         # HTTP client (create_task, poll_task)
├── ima_param_resolver.py     # Model selection + credit rule matching
├── ima_media_upload.py       # Media upload to imapi.liveme.com
├── ima_compliance.py         # Asset compliance verification
├── ima_reflection.py         # Error diagnosis + auto-retry
├── ima_constants.py          # Config (endpoints, models, aliases)
└── ima_logger.py             # Structured logging
```

**Import Hierarchy:**
- `ima_video_create.py` → imports all other modules
- Each module can be imported independently for programmatic use
- No circular dependencies

---

## 🔧 Configuration

### Environment Variables

```bash
# Required - Production API Key
export IMA_API_KEY="your-production-api-key"
```

**Note:** This skill is configured for production environment only (`https://api.imastudio.com`).

### Preferences File

Location: `~/.openclaw/memory/ima_prefs.json`

```json
{
  "model_id": "ima-pro",
  "model_name": "Seedance 2.0",
  "resolution": "720P",
  "aspect_ratio": "16:9"
}
```

---

## 🧰 Asset Compliance Verification

For tasks using input media (image, video, audio references in image-to-video, reference-image, first-last-frame), the system automatically:

1. **Uploads images** to `imapi.liveme.com`
2. **Verifies compliance** via `/api/asset-compliance/v1/verification/create`
3. **Polls verification status** until success/failure
4. **Proceeds with video generation** only if all assets pass

**Timeline:**
- Verification is synchronous and may take up to 5 minutes per asset
- **Parallel processing**: Up to 3 assets verified concurrently
- **Example**: 3 images verified in ~5 minutes (not 15 minutes)
- Failed assets prevent task creation with clear error message

**Supported formats:**
- Images: JPG, JPEG, PNG, GIF, WEBP, BMP
- Videos: MP4, WEBM, MOV, AVI, MKV, FLV
- Audio: MP3, WAV, M4A, AAC, OGG, FLAC

See [ima_compliance.py](scripts/ima_compliance.py) for implementation details.

---

## 🔄 Automatic Error Recovery

The `ima_reflection.py` module provides intelligent error handling:

### Supported Error Codes

| Code | Strategy |
|------|----------|
| 500 | Parameter degradation (720P→480P, 10s→5s) |
| 6009 | Add missing params from credit_rules |
| 6010 | Reselect matching credit_rule |
| 401 | Prompt for new API key |
| 4008 | Suggest credit top-up |
| timeout | Suggest faster model or check creation history |

### Retry Logic

```python
from ima_reflection import create_task_with_reflection

task_id = create_task_with_reflection(
    base_url=base_url,
    api_key=api_key,
    task_type="text_to_video",
    model_params=model_params,
    prompt=prompt,
    extra_params=params,
    max_attempts=3  # Will auto-retry with adjusted params
)
```

**Degradation sequence:**
- Resolution: 720P → 480P
- Duration: 15 → 10 → 5

---

## 📝 Logging

Logs are written to `logs/ima_video_*.log` with:
- Timestamps
- Log levels (INFO, WARNING, ERROR)
- Request/response details (truncated for readability)
- Error diagnostics

**Log rotation:**
- New log file per script invocation
- Format: `ima_video_YYYYMMDD_HHMMSS.log`
- No automatic cleanup (manage manually)

---

## 🎯 Best Practices

1. **Always check model list first** via `--list-models` to see current costs
2. **Use compliance verification** for all media-based tasks (default behavior)
3. **Let reflection handle errors** instead of manual retry logic
4. **Monitor logs** for debugging and audit trail
5. **Use JSON format** for all `--extra-params` values

---

## 🚨 Troubleshooting

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "401 Unauthorized" | Invalid API key | Regenerate at https://www.imaclaw.ai/imaclaw/apikey |
| "4008 Insufficient points" | Out of credits | Top up at https://www.imaclaw.ai/imaclaw/subscription |
| "6009/6010" | Parameter mismatch | Remove `--extra-params` and use defaults |
| Task timeout | Model taking too long | Check creation history or switch to faster model |
| "Asset verification failed" | Image violates policy | Use different image or check content guidelines |

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or check generated log files in `logs/` directory.

---

## 📚 Additional Resources

- **API Documentation**: Contact IMA Studio for official API docs
- **Model Updates**: Check https://www.imastudio.com for new models
- **Support**: https://www.imaclaw.ai/support
- **Creation History**: https://www.imastudio.com/ai-creation/text-to-video

---

## 🔄 Version History

**v1.0.0** (Current)
- Modularized implementation
- Two-model support (ima-pro, ima-pro-fast)
- Four task types (text, image, first-last, reference)
- Asset compliance verification
- Auto-retry and error reflection
- CLI + Python API

---

*This is complete technical documentation. For user-facing documentation, see [SKILL.md](../SKILL.md) or [lite-guide.md](lite-guide.md).*
