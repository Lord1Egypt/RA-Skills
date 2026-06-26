---
name: happyhorse-video-gen-edit
description: Video Generation and Editing with HappyHorse models. Supports text2video, image2video (first-frame based), reference2video (multi-image character fusion), and video editing capabilities.
homepage: https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market
metadata: {"clawdbot":{"emoji":"🐴","requires":{"bins":["python3"],"env":["DASHSCOPE_API_KEY"]},"primaryEnv":"DASHSCOPE_API_KEY"},"author":"KrisYe"}
---

# HappyHorse Video Models

HappyHorse Video Models, created by Alibaba Group, are video generation and editing models. This skill integrates with HappyHorse Model APIs on ModelStudio (Bailian-Alibaba Model Service Platform).

## Model Overview

| Model | Capabilities | Resolution | Duration |
| --- | --- | --- | --- |
| happyhorse-1.0-t2v | Text to Video | 720P, 1080P | 3-15s |
| happyhorse-1.0-i2v | First-frame Image to Video | 720P, 1080P | 3-15s |
| happyhorse-1.0-r2v | Reference images to video, Multi-character fusion | 720P, 1080P | 3-15s |
| happyhorse-1.0-video-edit | Video editing, Style transfer, Reference-based edit | 720P, 1080P | 3-15s (output) |

## Text to Video Generation (happyhorse-1.0-t2v)

Generate videos from text prompts.

### text2video task-submit
```bash
python3 {baseDir}/scripts/happyhorse-magic.py text2video-gen --prompt "一座由硬纸板和瓶盖搭建的微型城市，在夜晚焕发出生机" --resolution "720P" --ratio "16:9" --duration 5
python3 {baseDir}/scripts/happyhorse-magic.py text2video-gen --prompt "一只可爱的小猫将军站在悬崖上，远处是壮丽的雪山" --resolution "1080P" --ratio "16:9" --duration 10
python3 {baseDir}/scripts/happyhorse-magic.py text2video-gen --prompt "海浪拍打岩石的慢镜头" --resolution "720P" --ratio "9:16" --duration 8 --no-watermark
```

### Options
- `--prompt`: Text prompt for video generation (required, max 5000 non-Chinese chars or 2500 Chinese chars)
- `--resolution`: Video resolution - `720P` or `1080P` (default: 1080P)
- `--ratio`: Aspect ratio - `16:9`, `9:16`, `1:1`, `4:3`, `3:4` (default: 16:9)
- `--duration`: Video duration in seconds, 3-15 (default: 5)
- `--no-watermark`: Disable "Happy Horse" watermark (default: enabled)
- `--seed`: Random seed for reproducibility [0, 2147483647]

### text2video tasks-get (round-robin)
```bash
python3 {baseDir}/scripts/happyhorse-magic.py text2video-get --task-id "<TASK_ID_FROM_VIDEO_GEN>"
```

## Image to Video Generation (happyhorse-1.0-i2v)

Generate video from a first-frame image. Output aspect ratio automatically follows the input image.

### First-frame to Video
```bash
python3 {baseDir}/scripts/happyhorse-magic.py image2video-gen --prompt "一只猫在草地上奔跑" --first-frame "https://example.com/cat.png" --resolution "720P" --duration 5
python3 {baseDir}/scripts/happyhorse-magic.py image2video-gen --first-frame "https://example.com/landscape.jpg" --resolution "1080P" --duration 10
python3 {baseDir}/scripts/happyhorse-magic.py image2video-gen --prompt "花朵缓缓绽放" --first-frame "https://example.com/flower.png" --duration 8 --no-watermark
```

### Options
- `--prompt`: Text prompt for video generation (optional but recommended)
- `--first-frame`: First frame image URL (required). Format: JPEG/JPG/PNG/WEBP, min 300px per side, max 10MB.
- `--resolution`: Video resolution - `720P` or `1080P` (default: 1080P). Output ratio follows input image.
- `--duration`: Video duration in seconds, 3-15 (default: 5)
- `--no-watermark`: Disable "Happy Horse" watermark (default: enabled)
- `--seed`: Random seed for reproducibility [0, 2147483647]

Note: There is no `--ratio` parameter. The output video aspect ratio automatically follows the input first-frame image.

### image2video tasks-get (round-robin)
```bash
python3 {baseDir}/scripts/happyhorse-magic.py image2video-get --task-id "<TASK_ID_FROM_VIDEO_GEN>"
```

## Reference to Video Generation (happyhorse-1.0-r2v)

Generate video from reference images as character/object sources. Use "character1", "character2", etc. in the prompt to reference images by their array order.

### Multi-character Reference
```bash
python3 {baseDir}/scripts/happyhorse-magic.py reference2video-gen --prompt "身着红色旗袍的女性character1，镜头以侧面中景勾勒旗袍修身剪裁" --reference-images "https://example.com/girl.jpg" --resolution "720P" --ratio "16:9" --duration 5
python3 {baseDir}/scripts/happyhorse-magic.py reference2video-gen --prompt "身着红色旗袍的女性character1，轻抬玉手展开折扇character2时流苏耳坠character3随头部转动轻盈摆动" --reference-images "https://example.com/girl.jpg" "https://example.com/fan.jpg" "https://example.com/earrings.jpg" --resolution "720P" --ratio "16:9" --duration 5
python3 {baseDir}/scripts/happyhorse-magic.py reference2video-gen --prompt "character1在海边散步，阳光洒在沙滩上" --reference-images "https://example.com/person.png" --resolution "1080P" --ratio "16:9" --duration 10
```

### Options
- `--prompt`: Text prompt with character references (required, max 5000 non-Chinese chars). Use "character1/character2/..." to reference images in array order.
- `--reference-images`: Reference image URLs (required, 1-9 images). The 1st image = character1, 2nd = character2, etc.
- `--resolution`: Video resolution - `720P` or `1080P` (default: 1080P)
- `--ratio`: Aspect ratio - `16:9`, `9:16`, `1:1`, `4:3`, `3:4` (default: 16:9)
- `--duration`: Video duration in seconds, 3-15 (default: 5)
- `--no-watermark`: Disable "Happy Horse" watermark (default: enabled)
- `--seed`: Random seed for reproducibility [0, 2147483647]

Note: Reference images should have short side >= 400px. Avoid low-resolution, blurry, or heavily compressed images.

### reference2video tasks-get (round-robin)
```bash
python3 {baseDir}/scripts/happyhorse-magic.py reference2video-get --task-id "<TASK_ID_FROM_VIDEO_GEN>"
```

## Video Editing (happyhorse-1.0-video-edit)

Edit existing videos with text instructions and optional reference images. Supports style transfer, local replacement, and other editing tasks.

### Instruction-based Editing
```bash
python3 {baseDir}/scripts/happyhorse-magic.py video-edit --prompt "将场景变成夜晚，添加霓虹灯效果" --video "https://example.com/video.mp4" --resolution "720P"
python3 {baseDir}/scripts/happyhorse-magic.py video-edit --prompt "为人物换上酷闪的衣服" --video "https://example.com/original.mp4"
```

### Reference Image-based Editing
```bash
python3 {baseDir}/scripts/happyhorse-magic.py video-edit --prompt "让视频中的角色穿上图片中的条纹毛衣" --video "https://example.com/video.mp4" --reference-images "https://example.com/clothes.webp"
python3 {baseDir}/scripts/happyhorse-magic.py video-edit --prompt "将背景替换为参考图中的场景" --video "https://example.com/video.mp4" --reference-images "https://example.com/bg.jpg" --resolution "720P"
```

### Options
- `--prompt`: Editing instruction (required, max 5000 non-Chinese chars)
- `--video`: Input video URL to edit (required, mp4/mov, 3-60s input, output max 15s)
- `--reference-images`: Reference image URLs for editing (optional, 0-5 images)
- `--resolution`: Output resolution - `720P` or `1080P` (default: 1080P)
- `--audio-setting`: Audio handling - `auto` (default) or `origin` (keep original audio)
- `--no-watermark`: Disable "Happy Horse" watermark (default: enabled)
- `--seed`: Random seed for reproducibility [0, 2147483647]

Note: Output aspect ratio and duration follow the input video. No `--ratio` or `--duration` parameters. If input video > 15s, system auto-truncates to first 15s.

### video-edit tasks-get (round-robin)
```bash
python3 {baseDir}/scripts/happyhorse-magic.py video-edit-get --task-id "<TASK_ID_FROM_VIDEO_EDIT>"
```

## Key Differences from Wan 2.7

| Feature | HappyHorse | Wan 2.7 |
| --- | --- | --- |
| Watermark default | Enabled ("Happy Horse") | Disabled ("AI Generated") |
| prompt_extend | Not supported | Supported |
| negative_prompt | Not supported | Supported |
| seed parameter | Supported (all models) | Supported (all models) |
| I2V modes | First-frame only | First-frame, First+Last-frame, Video continuation |
| R2V reference type | Images only (character1/2) | Videos + Images (视频1/图片1) |
| R2V reference count | 1-9 images | Max 3 videos + 5 images |
| Video Edit input | 3-60s, output max 15s | 2-10s |
| Video Edit prompt | Required | Optional |

## Important Notes

- **Task ID Validity**: Task IDs are valid for 24 hours
- **Video URL Validity**: Generated video URLs are valid for 24 hours, download immediately
- **Content Review**: Both input and output are subject to content safety review
- **Billing**: Based on resolution (1080P > 720P) × duration (seconds)
- **Watermark**: Default enabled with "Happy Horse" text; use `--no-watermark` to disable
