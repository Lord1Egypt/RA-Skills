---
name: llm-video-generator
description: >
  Generate videos from text descriptions using ZhipuAI CogVideoX-3 model.
  Supports text-to-video, image-to-video, and first/last frame-to-video generation.
  Automatically handles long videos (over 5s) by chaining multiple generation calls
  with last-frame continuation. Use when the user asks to create/generate a video
  from text, make a video, text-to-video, 文生视频, 生成视频, 做个视频, or any
  request involving converting text/images into a video. Supports configuring video
  content, style, resolution (up to 4K), frame rate (30/60fps), audio, and duration.
---

# LLM Video Generator

Generate videos via ZhipuAI CogVideoX-3. Each API call produces ~5s of video.
For longer videos, chain multiple calls using last-frame continuation, then concatenate.

## Scripts

All scripts use `/opt/anaconda3/bin/python3`. Resolve `<skill-dir>` to this skill's directory.

| Script | Purpose |
|--------|---------|
| `scripts/video_gen.py` | Core generation (3 modes: text2video, image2video, frames2video) |
| `scripts/extract_last_frame.py` | Extract last frame from a video (for continuation) |
| `scripts/concat_videos.py` | Concatenate multiple video segments into one |

## Workflow

### Step 1: Assess Request & Clarify

**Clear request** → proceed to Step 2. A request is clear when:
- Video content/scene is described with enough detail
- Style or visual tone is specified or implied
- Duration is stated (default: 5s if not specified)

**Vague request** → propose a plan first:

```
基于你的需求，我拟定了以下视频方案：

📹 **视频内容**: [detailed scene description with key moments]
🎨 **视频风格**: [e.g., 写实/动画/电影感/温馨...]
⏱️ **视频时长**: [Xs, note: will be generated in 5s segments]
🔊 **背景音乐**: 有/无
📐 **分辨率**: 1920x1080
🎞️ **帧率**: 30fps

你觉得这个方案可以吗？需要调整哪些部分？
```

Iterate with the user until confirmed.

### Step 2: Estimate Time & Notify User

Before starting generation, calculate and report the estimated time:

**Time estimation formula:**
- Base: 1 minute per second of video (e.g., 20s video ≈ 20 minutes)
- High-definition (4K or 60fps): add +30% (e.g., 20s 4K video ≈ 26 minutes)
- Additional overhead: ~2 minutes for frame extraction, concatenation, and compression
- Segments: ceil(target_duration / 5)

**MUST send this message to the user before starting generation:**

```
⏳ **视频生成预估**

📊 分段计划：{N} 段（每段约5秒）
⏱️ 预计总耗时：约 {estimated_minutes} 分钟
📐 分辨率：{resolution}

视频生成是一个耗时过程，请耐心等待。我会在每段完成后实时汇报进度。
```

Example for a 30s 1080P video:
- 6 segments, base time = 30 minutes, +2 min overhead → ~32 minutes
- Message: "预计总耗时：约 32 分钟"

Example for a 20s 4K video:
- 4 segments, base time = 20 * 1.3 = 26 min, +2 min → ~28 minutes

### Step 3: Plan Generation Segments

Each API call produces ~5 seconds. Calculate segments: `ceil(target_duration / 5)`

For multi-segment videos, plan how the content evolves across segments. Write a prompt for each segment describing what happens in that 5-second window, maintaining visual continuity.

### Step 4: Execute Generation with Progress Reports

**CRITICAL: After each segment completes, IMMEDIATELY send a progress message to the user before starting the next segment.** Do not wait until all segments are done.

**Progress message format (send via message tool or inline reply after each segment):**

```
✅ 进度：{completed}/{total} 段完成（第{N}段已生成）
📝 内容：{brief segment description}
⏱️ 本段耗时：{minutes}分钟
📊 预计剩余：约 {remaining_minutes} 分钟
```

**Generation process:**

**Segment 1 — Text-to-Video:**

```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/video_gen.py text2video \
  --prompt "<segment_1_prompt>" \
  --quality quality --audio true --size 1920x1080 --fps 30 \
  --output-dir <output-dir> --max-wait 900
```

→ **Send progress message to user**

**Segments 2+ — Image-to-Video (last-frame continuation):**

For each subsequent segment:

1. Extract last frame from the previous segment's video:
```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/extract_last_frame.py \
  <previous_video.mp4> --output <output-dir>/frame_segN.png
```

2. Generate next segment using the last frame as input:
```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/video_gen.py image2video \
  --prompt "<segment_N_prompt>" \
  --image-url <output-dir>/frame_segN.png \
  --quality quality --audio true --size 1920x1080 --fps 30 \
  --output-dir <output-dir> --max-wait 900
```

3. → **Send progress message to user**

Repeat for all segments.

**Alternative — Frames-to-Video mode:**

If you have both a starting and ending image for a segment:
```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/video_gen.py frames2video \
  --prompt "<description>" \
  --first-frame <first.png> --last-frame <last.png> \
  --quality quality --audio true --size 1920x1080 --fps 30 \
  --output-dir <output-dir>
```

### Step 5: Concatenate Segments

After all segments are generated, combine them:

```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/concat_videos.py \
  --inputs <seg1.mp4> <seg2.mp4> ... \
  --output <output-dir>/final_video.mp4
```

If the final file exceeds 25MB (Feishu upload limit), compress with ffmpeg:
```bash
ffmpeg -i <input> -c:v libx264 -crf 32 -c:a aac -b:a 96k -vf "scale=1280:720" -y <output>
```

### Step 6: Deliver

- Share the final video file with the user
- For Feishu delivery: use feishu-send-file skill to send the .mp4 file
- Final report:

```
🎬 **视频生成完成！**

⏱️ 总时长：{duration}秒
📦 文件大小：{size}MB
📊 共 {N} 段，总耗时 {total_minutes} 分钟
```

## Prompt Tips

- Use **English prompts** for best quality (translate Chinese descriptions)
- Be specific: scene, camera angle, lighting, motion, atmosphere
- Include style keywords: cinematic, realistic, cartoon, watercolor, etc.
- For continuation segments, describe the **action progression**, not the full scene from scratch
- Keep each segment prompt concise (1-3 sentences)

## Parameters Reference

| Parameter | Flag | Default | Options |
|-----------|------|---------|---------|
| Prompt | `--prompt` | (required) | Descriptive text |
| Quality | `--quality` | `quality` | `quality` / `speed` |
| Audio | `--audio` | `true` | `true` / `false` |
| Resolution | `--size` | `1920x1080` | `1280x720`, `1920x1080`, `3840x2160` |
| Frame rate | `--fps` | `30` | `30` / `60` |
| Output dir | `--output-dir` | `.` | Any writable path |
| Poll interval | `--poll-interval` | `10` | Seconds |
| Max wait | `--max-wait` | `900` | Seconds (default raised for reliability) |

## Error Handling

- **Missing ZHIPU_API_KEY**: Ask user to set environment variable
- **Missing zai-sdk**: `pip install zai-sdk` (under anaconda)
- **Missing ffmpeg**: Required for frame extraction and concatenation
- **Task timeout**: Increase `--max-wait` or retry; check task status manually via API
- **Task failed**: Simplify the prompt and retry
- **File too large for Feishu**: Compress with ffmpeg (reduce resolution or increase CRF)
