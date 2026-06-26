---
name: hitpaw-image-enhancer
description: Enhance images and videos using HitPaw's AI enhancement API
version: "1.0.3"
author: Nova (HitPaw-Official)
type: cli
entry: dist/cli.js
repository: https://github.com/HitPaw-Official/openclaw-skill-hitpaw-enhancer
keywords:
  - image
  - video
  - enhancement
  - upscale
  - hitpaw
  - ai
license: MIT
capabilities:
  - image_enhancement
  - image_upscaling
  - photo_enhance
  - video_enhancement
  - video_upscaling
requirements:
  node: ">=18"
  packages:
    - axios
    - commander
    - ora
    - chalk
    - fs-extra
environment:
  variables:
    - name: HITPAW_API_KEY
      description: Your HitPaw API key
      required: true
---

# HitPaw Image & Video Enhancer Skill

A powerful OpenClaw skill that integrates HitPaw's state-of-the-art AI enhancement technology for both **images** and **videos**. Enhance, upscale, restore, and denoise with multiple AI models.

---

## 🎯 Features

Based on the official [HitPaw API Documentation](https://developer.hitpaw.com/image/Introduction), this skill leverages industrial-grade AI models developed in-house by HitPaw's expert R&D team.

### Core Strengths

- **Quality**: Industry-defining quality fit for professional use cases, from commercial photography to archival restoration
- **Fidelity**: Preserves the original details and identities in the source images, ensuring the output remains true to the input
- **Efficiency**: Optimized for low latency and high throughput, capable of processing distinct enhancement tasks at scale

---

## 📸 Image Enhancement

According to the [Image API Introduction](https://developer.hitpaw.com/image/Introduction), our image processing services offer world-class capabilities designed to handle a wide variety of restoration scenarios:

### Key Capabilities

- **Upscale**: Output high-resolution images from low-resolution input files using standard or high-fidelity models
- **Face Recovery**: Ensure high-quality facial details, offering both "Clear" (soft/beauty) and "Natural" (textured/realistic) restoration options
- **Sharpen & Denoise**: Bring images into focus by removing blur and sensor noise while preserving the original structure
- **Generative Restoration**: Leverage Diffusion technology to reconstruct details in severely degraded portraits or general images

### Model Classes

The Image API offers two classes of AI models to suit different needs:

- **Standard Models**: Fast and efficient, prioritizing preserving original fidelity and details. Recommended for most professional and general restoration use cases
- **Generative Models**: Utilize Stable Diffusion to produce the highest quality outputs, capable of "imagining" missing details. Ideal for extremely low-quality inputs where traditional upscaling fails

#### Standard Models

As detailed in the [Available Models](https://developer.hitpaw.com/image/available-models) documentation:

| Model | Multiplier | Description | Best For |
|-------|------------|-------------|----------|
| `general_2x` / `general_4x` | 2x / 4x | General Enhance Model | General photos, landscapes |
| `face_2x` / `face_4x` | 2x / 4x | Portrait Model (Clear) | Soft/beauty style portrait enhancement |
| `face_v2_2x` / `face_v2_4x` | 2x / 4x | Portrait Model (Natural) | Natural/realistic portrait enhancement |
| `high_fidelity_2x` / `high_fidelity_4x` | 2x / 4x | High Fidelity Model | Professional photography, conservatively upscaling high-quality sources |
| `sharpen_denoise_1x` | 1x | Sharp Denoise Model | Aggressive denoising with sharpening |
| `detail_denoise_1x` | 1x | Detail Denoise Model | Gentle denoising with texture preservation |

#### Generative Models

Powered by Stable Diffusion technology:

| Model | Multiplier | Description | Best For |
|-------|------------|-------------|----------|
| `generative_portrait_1x/2x/4x` | 1x/2x/4x | Generative Portrait Model | Extremely low-quality portraits, "re-imagines" details |
| `generative_1x/2x/4x` | 1x/2x/4x | Generative Enhance Model | Heavily compressed or very low-resolution general images |

**Technical Highlights**:
- Generative models excel at texture generation and sharpening
- They can fill in missing details that traditional upscalers cannot recover
- Ideal for restoration tasks where source data is severely degraded

#### Example Image Use Cases

```bash
# General photo upscaling (landscape, architecture)
enhance-image -u landscape.jpg -m general_4x -o hd_landscape.jpg

# Portrait beautification (soft skin)
enhance-image -u selfie.jpg -m face_4x -o portrait_beautified.jpg

# Professional archival restoration (natural look)
enhance-image -u old_photo.png -m face_v2_2x -o restored.png --keep-exif

# Denoise grainy low-light photo
enhance-image -u night_photo.jpg -m sharpen_denoise_1x -o clean.jpg

# Generative reconstruction for severely degraded image
enhance-image -u blurry_face.jpg -m generative_portrait_2x -o ai_face.jpg
```

---

## 🎬 Video Enhancement

According to the [Video API Introduction](https://developer.hitpaw.com/video/Introduction), our video processing services provide industrial-grade solutions for restoring and upscaling video content:

### Key Capabilities

- **Video Upscale**: Convert SD or HD footage to 4K Ultra HD clarity using deep convolution and feature learning technologies
- **Portrait Restoration**: Specialized models to detect, stabilize, and enhance faces in video streams, removing motion blur and noise while maintaining identity
- **General Restoration**: A comprehensive solution based on GAN technology to de-noise, de-blur, and enhance details in general video content
- **Generative Reconstruction**: Utilizing Stable Diffusion for video to reconstruct textures and details in extremely low-quality footage

### Core Pillars

- **Temporal Stability**: Unlike image-only models, our video engines ensure smooth transitions between frames, eliminating flickering and jitter
- **Clarity**: Recovering fine details and removing compression artifacts common in streaming or legacy media
- **Performance**: Optimized inference times to handle heavy video processing workloads efficiently

### Model Classes

- **Restoration & Upscale (Standard)**: Models like Ultra HD and General Restore focus on cleaning up the footage and increasing resolution without altering the fundamental content. They rely on pixel-perfect accuracy and temporal consistency
- **Generative Video**: Uses advanced logic-based reconstruction. Designed for "impossible" restoration tasks where the source video lacks sufficient data, generating realistic textures and details to fill the gaps

#### Available Video Models

From the [Video Models Documentation](https://developer.hitpaw.com/video/available-models):

| Model | Description | Use Case |
|-------|-------------|----------|
| `ultrahd_restore_2x` | Ultra HD Model | High-definition upscale; natural-looking 1080p→4K |
| `general_restore_1x` / `2x` / `4x` | General Restore Model | General video restoration, de-noising, de-blurring |
| `portrait_restore_1x` / `2x` | Portrait Restore Model | Multi-face restoration with temporal stability |
| `face_soft_2x` | Video Face Soft Model | Facial beautification with consistent appearance |
| `generative_1x` | Generative Video Model | Extreme restoration of heavily degraded footage |

**Technical Highlights**:
- Generates realistic textures and eliminates flickering via multi-frame SD architecture
- Handles heavy compression, high-ISO noise, and complex motion blur
- Maintains identity consistency across frames

#### Example Video Use Cases

```bash
# Convert old 720p footage to 4K
enhance-video -u old_clip.mp4 -m ultrahd_restore_2x -r 3840x2160 -o 4k_remastered.mp4

# Restore grainy, noisy home video
enhance-video -u home_movie.avi -m general_restore_2x -r 1920x1080 -o cleaned.mp4

# Beautify faces in vlog/interview
enhance-video -u interview.mp4 -m face_soft_2x -r 1920x1080 -o soft_faces.mp4

# Stabilize and restore old family footage with multiple faces
enhance-video -u family_reunion.mov -m portrait_restore_2x -r 1920x1080 -o restored.mp4

# Generative AI restoration for severely degraded source
enhance-video -u heavily_compressed.mp4 -m generative_1x -r 1920x1080 -o regenerated.mp4
```

---

## 🚀 Why Choose HitPaw API?

**Industry-Leading Quality**: Professional-grade output suitable for commercial photography, archival restoration, and broadcast-quality video remastering

**Unparalleled Fidelity**: Strictly retains original details and subject identity, ensuring outputs remain true to inputs

**Comprehensive Model Catalog**: 16 specialized models covering virtually every restoration scenario

**Scalable Performance**: Optimized for low-latency, high-throughput workloads

---

## 📊 Quick Reference

### Image Model Selection Guide

| Scenario | Recommended Model |
|----------|-------------------|
| General photo upscale | `general_2x` or `general_4x` |
| Portrait beautification | `face_2x` or `face_4x` |
| Portrait natural look | `face_v2_2x` or `face_v2_4x` |
| Professional archival | `high_fidelity_2x` / `high_fidelity_4x` |
| Grainy low-light | `sharpen_denoise_1x` |
| Subtle denoise | `detail_denoise_1x` |
| Severely degraded | `generative_portrait_*` or `generative_*` |

### Video Model Selection Guide

| Scenario | Recommended Model |
|----------|-------------------|
| SD → 4K upscale | `ultrahd_restore_2x` |
| General cleanup | `general_restore_2x` |
| Interview/vlog beautification | `face_soft_2x` |
| Old home movies (multiple faces) | `portrait_restore_2x` |
| Severely compressed/ degraded | `generative_1x` |

---

## Installation

```bash
clawhub install hitpaw-image-enhancer
```

## Configuration

Set your HitPaw API key:

```bash
export HITPAW_API_KEY="your_api_key_here"
```

Or create a `.env` file in your OpenClaw workspace:

```
HITPAW_API_KEY=your_api_key_here
```

Get your API key at: https://playground.hitpaw.com/

Test the API directly in the browser: [HitPaw Playground →](https://playground.hitpaw.com/)

---

## 📸 Examples & Gallery

> **Note**: All screenshots below are from official HitPaw website (hitpaw.com), showcasing real enhancement results. Place additional examples in the `images/` folder.

### Image Enhancement Examples

#### General Upscale (2x/4x)

From official HitPaw documentation:

| Before | After |
|--------|-------|
| ![Before](images/image-official-before.jpg) | ![After](images/image-official-after.jpg) |

*Demonstrates general image enhancement and upscaling capabilities*

**Use case**: Landscape photos, architecture, general photography

#### Unblur / Motion Blur Removal

| Before | After |
|--------|-------|
| ![Blurry](images/unblur-official-before.jpg) | ![Sharp](images/unblur-official-after.jpg) |

*Shows blur removal and sharpening effects*

**Use case**: Action shots, low-light photos, camera shake recovery

---

## 🎬 Video Enhancement Gallery

> Video screenshots coming soon. Currently using placeholder references.

| Scenario | Original Frame | Enhanced Frame |
|----------|----------------|----------------|
| General Upscale (1080p → 4K) | ![Original](images/video-original.jpg) | ![Enhanced](images/video-enhanced.jpg) |
| Portrait Restoration | ![Before](images/portrait-video-before.jpg) | ![After](images/portrait-video-after.jpg) |
| Denoise & Cleanup | ![Noisy](images/video-noisy.jpg) | ![Clean](images/video-clean.jpg) |

See [images/README.md](images/README.md) for screenshot guidelines and recommended sources.

---

## 📊 Model Comparison Examples

### Face Enhancement: Clear vs Natural

| Clear (Soft/Beauty) | Natural (Realistic) |
|---------------------|---------------------|
| ![Face Clear](images/face-clear.jpg) | ![Face Natural](images/face-natural.jpg) |

- **Face Clear Model**: Soft skin, beautification style
- **Face Natural Model**: Preserves natural texture and pores

### Generative vs Standard Models

| Standard (general_4x) | Generative (generative_portrait_2x) |
|-----------------------|------------------------------------|
| ![Standard](images/general-upscale.jpg) | ![Generative](images/generative-portrait.jpg) |

- **Standard models**: Fast, preserves original details
- **Generative models**: Reconstructs missing details, ideal for severely degraded inputs

---

# IMAGE COMMAND

## Usage: `enhance-image`

### Command Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--url`, `-u` | string | **required** | URL of the image to enhance |
| `--output`, `-o` | string | `output.jpg` | Output file path |
| `--model`, `-m` | string | `general_2x` | Image model (see below) |
| `--extension`, `-e` | string | `.jpg` | Output extension (`.jpg`, `.png`, `.webp`) |
| `--dpi` | number | original | Target DPI for metadata |
| `--keep-exif` | boolean | false | Preserve EXIF data from original |
| `--poll-interval` | number | 5 | Polling interval in seconds |
| `--timeout` | number | 300 | Maximum wait time in seconds |

#### Available Image Models

| Model | Multiplier | Best For | DPI Support |
|-------|------------|----------|-------------|
| `general_2x` / `general_4x` | 2x / 4x | General photos, landscapes | ✅ |
| `face_2x` / `face_4x` | 2x / 4x | Portrait & face enhancement | ✅ |
| `face_v2_2x` / `face_v2_4x` | 2x / 4x | Improved face model | ✅ |
| `high_fidelity_2x` / `high_fidelity_4x` | 2x / 4x | High quality preservation | ✅ |
| `sharpen_denoise_1x` | 1x | Denoise & sharpen | ✅ |
| `detail_denoise_1x` | 1x | Detail preservation | ✅ |
| `generative_1x/2x/4x` | — | Generative Enhance Model | ❌ |

#### Examples

```bash
# Simple 2x upscale with general model
enhance-image -u photo.jpg -o enhanced.jpg -m general_2x

# Face enhancement 4x
enhance-image -u portrait.jpg -m face_4x -o portrait_4x.jpg --keep-exif

# High fidelity with custom DPI
enhance-image -u old-photo.png -m high_fidelity_2x -dpi 300 -o hd.png

# Batch processing
for img in *.jpg; do
  enhance-image -u "$img" -o "upscaled/$img" -m general_4x
done
```

---

# VIDEO COMMAND

## Usage: `enhance-video`

### ⚠️ Important Notes

- **Resolution is required** (`--resolution` or `-r`). Must be in `WIDTHxHEIGHT` format (e.g., `1920x1080`).
- Ensure target resolution does **not exceed max output resolution** (36 MP total pixels) per API limits.
- Video processing can take **minutes to hours** depending on length. Use `--timeout` to extend if needed.
- Input video must be at a **publicly accessible URL** (local files not directly supported).

### Command Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--url`, `-u` | string | **required** | URL of the video to enhance |
| `--output`, `-o` | string | `output.mp4` | Output file path |
| `--model`, `-m` | string | `general_restore_2x` | Video model (see below) |
| `--resolution`, `-r` | string | **required** | Target resolution in WxH (e.g., `1920x1080`) |
| `--original-resolution` | string | — | Original resolution (e.g., `1280x720`) - optional |
| `--extension`, `-e` | string | `.mp4` | Output extension (`.mp4`, `.mov`, `.avi`) |
| `--fps` | number | — | Target FPS (preserves original if omitted) |
| `--keep-audio` | boolean | true | Preserve audio track |
| `--poll-interval` | number | 10 | Polling interval in seconds |
| `--timeout` | number | 600 | Maximum wait time in seconds |

#### Available Video Models

| Model | Description | Use Case |
|-------|-------------|----------|
| `general_restore_1x` / `2x` / `4x` | General video restoration | General upscaling |
| `face_soft_2x` | Face-softening enhancement | Portrait videos |
| `portrait_restore_1x` / `2x` | Portrait restoration | Face-focused content |
| `ultrahd_restore_2x` | Ultra HD upscaling | Highest quality upscale |
| `generative_1x` | Generative fill | AI-powered restoration |

#### Examples

```bash
# Upscale to 1080p using general_restore_2x
enhance-video -u input.mp4 -o output_1080p.mp4 -m general_restore_2x -r 1920x1080

# Upscale to 4K with specific original resolution
enhance-video -u clip.mov -o 4k.mov -m general_restore_4x -r 3840x2160 --original-resolution 1920x1080

# Denoise with portrait model
enhance-video -u portrait_video.avi -m portrait_restore_2x -r 1920x1080 -o clean_portrait.mp4

# Add color to B&W (if generative model supports)
enhance-video -u bw_vintage.mp4 -m generative_1x -r 1920x1080 -o colorized.mp4
```

---

## Coin Consumption

### Image Enhancement
- 2x/4x models: **~75 coins** per image
- 1x models: **~50 coins** per image
- Generative models: **~100+ coins** per image

### Video Enhancement
Coin costs depend on video length, model, and resolution. Approximate rates:
- Upscale models: **~200-400 coins** per minute
- Restoration models: **~150-300 coins** per minute

**Always check current rates** at: https://playground.hitpaw.com/

---

## Error Handling

Common errors and solutions:

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid API key` | Wrong or expired key | Update `HITPAW_API_KEY` |
| `Insufficient coins` | Account balance too low | Top up at HitPaw Playground |
| `Unsupported model` | Model name typo or not available | Check model table above |
| `Invalid extension` | Output format not supported | Use `.jpg/.png/.webp` for images; `.mp4/.mov/.avi` for videos |
| `Invalid video URL` | URL not publicly accessible | Ensure video is reachable via HTTPS |
| `Input/target resolution over limit` | Exceeds 36 MP total pixels (e.g., 7680x4320 = ~33 MP) | Reduce resolution |
| `Video duration over limit` | Video longer than 1 hour | Trim video first |
| `Rate limit exceeded` | Too many requests | Wait and retry with exponential backoff |
| `Video processing failed` | Corrupt video or unsupported codec | Try different input format or re-encode |

---

## Error Codes

The API returns structured error codes. Always check both HTTP status and the `error_code` field.

### General Errors

| error_code | HTTP Status | Message |
|------------|-------------|---------|
| 100400000 | 400 | No access |
| 100400001 | 400 | Invalid URL |
| 100400002 | 400 | Bad Request |
| 100401000 | 401 | Token is expired |
| 100403000 | 403 | Invalid request parameters |
| 100403001 | 403 | Access denied |
| 100403002 | 403 | You don't have permission to access this resource |
| 100429000 | 429 | Too many requests, please try again later |
| 100500000 | 500 | Internal error |
| 100500001 | 500 | Database error |
| 100500002 | 500 | Cache error |
| 100500003 | 500 | Failed to create file |
| 100500004 | 500 | Signature verification failed |
| 100500005 | 500 | Configuration error |
| 100500006 | 500 | Unknown error |
| 100500007 | 500 | Operation timeout |

### API-Specific Errors

| error_code | HTTP Status | Message |
|------------|-------------|---------|
| 110400000 | 400 | api_key is not valid |
| 110400002 | 400 | The task does not exist |
| 110400003 | 400 | The task failed, please try again |
| 110400005 | 400 | The model is not supported, please try again |
| 110400007 | 400 | The extension is not valid |
| 110400008 | 400 | The video URL is not valid |
| 110400009 | 400 | The input resolution is over limit |
| 110400010 | 400 | The target resolution is over limit |
| 110400011 | 400 | The video duration is over limit |
| 110402000 | 402 | The coins are not enough |
| 110402001 | 402 | The coins are not enough |
| 110402004 | 402 | The Demo try times exceeded |

### Error Response Format

```json
{
  "error_code": 110400000,
  "message": "api_key is not valid"
}
```

## Rate Limiting

- The API implements rate limiting to ensure fair usage
- Error code `100429000` will be returned if you exceed the rate limit
- Implement **exponential backoff** in your retry logic

## Best Practices

### Polling for Job Status
- Poll the `/api/task-status` endpoint at reasonable intervals (recommended: every 5–10 seconds)
- Implement exponential backoff for failed requests
- Set a maximum number of polling attempts to avoid infinite loops
- Check status values: `CONVERTING` (keep polling), `COMPLETED` (success), `ERROR` (failed)

### Error Handling
- Always check the HTTP status code AND `error_code` in the response
- Implement retry logic for transient errors (5xx errors)
- Do NOT retry 4xx client errors without first fixing the request
- Log error responses for debugging

### Resource Limits
- **Images**: Max input resolution 70 MP (Enhancement/Denoise) / 34 MP (Generative); Max output 432 MP (Enhancement/Denoise)
- **Videos**: Max output 36 MP total pixels; Duration 0.5s – 1 hour
- Verify file extension validity before submitting

### API Key Management
- Store API keys securely using environment variables
- Never commit API keys to version control
- Rotate API keys periodically

### File URL Requirements
- Ensure image and video URLs are publicly accessible
- Use HTTPS URLs
- Use **Pre-sign OSS Upload** for unreliable URLs: https://developer.hitpaw.com/common/oss-presign-put-api

## Technical Details

### API Compatibility

This skill implements the official HitPaw API as documented:
- **Base URL**: `https://api-base.hitpaw.com`
- **Image endpoint**: `POST /api/photo-enhancer`
- **Video endpoint**: `POST /api/video-enhancer`
- **Status endpoint**: `POST /api/task-status`

Both endpoints return a `job_id`. Use the status endpoint to poll until `COMPLETED`, then download from `res_url`.

### Polling Strategy

- **Images**: default poll every 5s, timeout 300s (5 min)
- **Videos**: default poll every 10s, timeout 600s (10 min)
- Implement **exponential backoff** when encountering 5xx errors or rate limit (429)

For longer videos, increase `--timeout` as needed (e.g., `--timeout 3600` for 1 hour).

### Resolution & Format Limits

**Image Model Specs**:

| Model Category | DPI Support | Max Input | Max Output | Formats |
|----------------|-----------|----------|----------|--------|
| Enhancement & Denoise (`general_*`, `face_*`, `high_fidelity_*`, `*_denoise_*`) | ✅ | 70 MP | 432 MP | bmp, jpeg, jpg, png, jfif, tga, tiff, webp, heif |
| Generative (`generative_*`, `generative_portrait_*`) | ❌ | 34 MP | 34 MP | Same formats |

**Video Model Specs**:

| Property | Limit |
|----------|-------|
| Max Input Resolution | No limit |
| Max Output | 36 MP total pixels |
| Duration | 0.5 seconds – 1 hour |
| Input Formats | dv, mlv, m2ts, m2t, m2v, nut, ser, 3g2, 3gp, asf, avi, divx, f4v, flv, h261, h263, m4v, mkv, mov, mp4, mpeg, mpeg4, mpg, mxf, ogv, rm, rmvb, webm, wmv, gif |
| Output Formats | mp4, mov, mkv, m4v, avi, gif |

**Examples**: 3840×2160 = 8.3 MP ✅, 7680×4320 = 33.2 MP ✅, 8192×4608 = 37.7 MP ❌

For videos, `resolution` is **required**. Choose based on your needs:
- Keep original size? Set `resolution` to original dimensions (use `--original-resolution` for better quality).
- Upscale? Multiply original width/height by factor (2x, 4x).
- Downscale? Rare but possible; just specify smaller dimensions.

### Audio Preservation

By default, `enhance-video` keeps the audio track (`--keep-audio`, default true). Use `--no-keep-audio` to strip audio.

---

## Support

- Image API Docs: https://developer.hitpaw.com/image/API-reference
- Video API Docs: https://developer.hitpaw.com/video/API-reference
- Playground: https://playground.hitpaw.com/
- Contact: support@hitpaw.com

This skill is an **unofficial integration** with HitPaw API. You must have a valid API key and comply with HitPaw's terms. The skill author is not responsible for any charges incurred.

## License

MIT © HitPaw-Official
