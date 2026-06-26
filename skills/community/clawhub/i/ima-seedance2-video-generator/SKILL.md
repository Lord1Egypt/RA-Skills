---

name: "IMA Seedance 2.0 Video Generator"
version: 1.0.0
category: file-generation
author: IMA Studio (imastudio.com)
keywords: imastudio, Seedance 2.0, Seedance, seedance video, Seedance 2.0 video generator, Seedance 2.0 image to video, Seedance 2.0 text to video, AI video generator, video generator, text to video, image to video, cinematic video generator, AI cinematic video, multi-shot video generator, AI short film generator, consistent character video, camera motion video, storyboard to video, AI commercial video generator, AI ad video generator, AI storytelling video, AI music video generator, AI product video generator, AI short clip generator, short video generator, promo video generator, character animation, temporal consistency, camera control, 2K video, multimodal video, first-last-frame, reference-image video
argument-hint: "[text prompt or media URL]"
description: >
  Seedance 2.0 AI video generator — two models in one skill: Seedance 2.0 (ima-pro) for
  cinema-grade quality with high frame-rate temporal consistency, precise camera language control,
  and 2K output; Seedance 2.0 Fast (ima-pro-fast) for faster iteration. Supports text-to-video,
  image-to-video, first-last-frame, and reference-media video generation with image, video, and
  audio references. Works for cinematic prompting, storyboard-driven clips, consistent-character
  workflows, product demos, and short-form content generation. Requires IMA_API_KEY.
requires:
  env:
    - IMA_API_KEY
  runtime:
    - python3
    - ffmpeg
    - ffprobe
  packages:
    - requests
  primaryCredential: IMA_API_KEY
  credentialNote: "IMA_API_KEY is required at runtime. It is sent to api.imastudio.com and, for local/non-HTTPS media uploads, to imapi.liveme.com."
metadata:
  openclaw:
    primaryEnv: IMA_API_KEY
    homepage: https://www.imaclaw.ai
    requires:
      bins:
        - python3
        - ffmpeg
        - ffprobe
      env:
        - IMA_API_KEY
    envVars:
      - name: IMA_API_KEY
        required: true
        description: Primary IMA credential used for product list, task creation, task polling, compliance verification, and upload-token calls.
      - name: IMA_STDOUT_MODE
        required: false
        description: Optional stdout mode toggle for event-stream integrations. Supported values are events, mixed, and auto.
      - name: IMA_AUTO_CONSENT
        required: false
        description: Optional non-interactive flag to auto-approve asset compliance verification prompts.
      - name: IMA_DEBUG
        required: false
        description: Optional debug flag that enables verbose logging for troubleshooting.
    dependencies:
      - name: requests
        type: pip
        version: ">=2.25.0"
    # Multi-tier instruction strategy | 多级指令策略
    instructionStrategy:
      mode: "adaptive"  # adaptive | fixed
      default: "SKILL.md"
      variants:
        # Tier 1: Current frontier models (2025-2026, long context, advanced reasoning)
        - name: "full"
          file: "SKILL.md"
          description: "Complete instruction set with all features"
          targetModels:
            - "gpt-5.4"
            - "gpt-5.1"
            - "o3"
            - "claude-opus-4-1"
            - "claude-sonnet-4-0"
            - "claude-3-7-sonnet-latest"
            - "gemini-2.5-pro"
            - "gemini-2.5-flash"
            - "kimi-k2.5"
            - "doubao-seed-1.6"
            - "deepseek-reasoner"
            - "glm-4.7"
            - "qwen3-max"
          minContextWindow: 128000
          capabilities: ["long-context", "complex-reasoning", "table-parsing"]
        
        # Tier 2: Smaller or compatibility models (32K-128K context)
        - name: "lite"
          file: "references/lite-instructions.md"
          description: "Simplified instruction optimized for weak models"
          targetModels:
            - "gpt-4o-mini"
            - "o4-mini"
            - "claude-3-5-haiku-latest"
            - "gemini-2.5-flash-lite"
            - "doubao-1.5-lite-32k"
            - "deepseek-chat"
            - "glm-4.7-flash"
            - "qwen-flash"
          minContextWindow: 8000
          maxContextWindow: 128000
          capabilities: ["basic-reasoning", "strict-mapping"]
      
      # Selection priority | 选择优先级
      selectionPriority:
        - "exact-model-match"      # Exact model name match | 精确匹配模型名
        - "context-window-size"    # Context window size | 上下文窗口大小
        - "capability-match"       # Capability match | 能力匹配
        - "fallback"               # Fallback strategy | 兜底策略
      
      # Detail reference (for agent deep learning) | 详细文档引用
      detailReference: "references/skill-detail.md"
      detailReferenceUsage: "on-demand"  # on-demand | always | never

persistence:
  readWrite:
    - ~/.openclaw/memory/ima_prefs.json
    - ~/.openclaw/logs/ima_skills/

---

# IMA Seedance 2.0 — OpenClaw Calling Protocol

## Hard Rule

OpenClaw must call `scripts/ima_video_create.py`.

OpenClaw must **not**:

- build `/open/v1/tasks/create` payloads
- compute `attribute_id`
- compute `credit`
- build `src_img_url`
- build `src_image`
- build `src_video`
- build `src_audio`

## Required Read Order

1. [`references/protocols/execution.md`](references/protocols/execution.md)
2. [`references/protocols/event-stream.md`](references/protocols/event-stream.md)
3. On demand:
   - [`references/contracts/create-task.md`](references/contracts/create-task.md)
   - [`references/contracts/credit-rules.md`](references/contracts/credit-rules.md)
   - [`references/contracts/payload-rules.md`](references/contracts/payload-rules.md)
   - [`references/flows/reference-image-to-video.md`](references/flows/reference-image-to-video.md)
   - [`references/limits/reference-media-rules.md`](references/limits/reference-media-rules.md)

## Supported User Intents

- text-to-video
- image-to-video
- first-last-frame transition
- reference-image-to-video
- multimodal reference-image-to-video with image / video / audio inputs

## Input Entry Points

- `--prompt`
- `--model-id`
- `--task-type` when explicit task type is required
- `--input-images`
- `--reference-image`
- `--reference-video`
- `--reference-audio`
- `--extra-params`

## Stop Conditions

Stop before task creation if:

- prompt is missing
- model cannot be resolved
- reference media preflight validation fails
- any reference media compliance verification fails
- create-task returns a hard failure

## Task Type Rules

| Input pattern | task_type |
|---|---|
| text only | `text_to_video` |
| one image | `image_to_video` |
| explicit first-last-frame with 2 images | `first_last_frame_to_video` |
| any video input | `reference_image_to_video` |
| any audio input | `reference_image_to_video` |
| multiple images without explicit first-last-frame intent | `reference_image_to_video` |

## Model ID Reference (CRITICAL)

Use **exact model_id** from this table. Do NOT infer from friendly names.


| Friendly Name     | model_id       | Notes                        |
| ----------------- | -------------- | ---------------------------- |
| Seedance 2.0      | `ima-pro`      | ✅ Quality priority, 300~900s |
| Seedance 2.0 Fast | `ima-pro-fast` | ⚠️ Speed priority, 120~600s   |


**User input aliases:**
- Quality/Professional/Pro/专业版/高质量 → `ima-pro`
- Fast/Speed/Quick/极速/快速 → `ima-pro-fast`
- Default/默认 → `ima-pro`

## Model Selection Priority

1. **User preference** (if explicitly stated) → highest priority
2. **Fallback default:** `ima-pro`


| Task | Default | Fast Alternative |
|---|---|---|
| `text_to_video` | `ima-pro` | `ima-pro-fast` |
| `image_to_video` | `ima-pro` | `ima-pro-fast` |
| `first_last_frame_to_video` | `ima-pro` | `ima-pro-fast` |
| `reference_image_to_video` | `ima-pro` | `ima-pro-fast` |

## Minimal Invocation Examples

```bash
# Text to video
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "a puppy runs across a sunny meadow, cinematic"

# Single image
python3 {baseDir}/scripts/ima_video_create.py \
  --prompt "camera slowly zooms in" \
  --input-images https://example.com/photo.jpg \
  --model-id ima-pro-fast

# Explicit first-last-frame
python3 {baseDir}/scripts/ima_video_create.py \
  --task-type first_last_frame_to_video \
  --prompt "smooth transition" \
  --input-images https://example.com/first.jpg https://example.com/last.jpg

# Multimodal reference mode
python3 {baseDir}/scripts/ima_video_create.py \
  --reference-image https://example.com/product.jpg \
  --reference-video https://example.com/clip.mp4 \
  --reference-audio https://example.com/narration.mp3 \
  --model-id ima-pro-fast
```

## References

- Execution protocol: [`references/protocols/execution.md`](references/protocols/execution.md)
- Event stream: [`references/protocols/event-stream.md`](references/protocols/event-stream.md)
- Create-task contract: [`references/contracts/create-task.md`](references/contracts/create-task.md)
- Credit rules: [`references/contracts/credit-rules.md`](references/contracts/credit-rules.md)
- Payload rules: [`references/contracts/payload-rules.md`](references/contracts/payload-rules.md)
- Reference-image-to-video flow: [`references/flows/reference-image-to-video.md`](references/flows/reference-image-to-video.md)
- Text-to-video flow: [`references/flows/text-to-video.md`](references/flows/text-to-video.md)
- Reference media limits: [`references/limits/reference-media-rules.md`](references/limits/reference-media-rules.md)
- FAQ: [`references/support/faq.md`](references/support/faq.md)
- Troubleshooting: [`references/support/troubleshooting.md`](references/support/troubleshooting.md)
