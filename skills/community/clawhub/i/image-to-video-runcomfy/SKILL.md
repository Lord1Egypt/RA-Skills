---
name: image-to-video-runcomfy
displayName: "🫧 Image-to-Video — Pro Pack on RunComfy"
description: >
  Image-to-video generation on RunComfy. This image-to-video skill turns
  any still image into a short video clip via the RunComfy Model API.
  The image-to-video pipeline supports portrait animation, product
  reveal, scene motion, and synchronized-audio image-to-video output.
  Calls the right image-to-video endpoint for the user's intent (general
  image-to-video, lip-sync image-to-video, multi-modal image-to-video)
  through `runcomfy run <model>/image-to-video`. Triggers on "image to
  video", "image-to-video", "i2v", "animate image", "image2video",
  "make a video from image", "still to video", "still-to-video", or any
  explicit ask for image-to-video conversion.
emoji: "🫧"
homepage: https://www.runcomfy.com
license: MIT
clawdis:
  requires:
    bins:
      - runcomfy
    env:
      - RUNCOMFY_TOKEN
    config:
      - ~/.config/runcomfy
---

# 🫧 Image-to-Video — Pro Pack on RunComfy

[runcomfy.com](https://www.runcomfy.com/?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy) · [docs](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy) · [Image-to-video models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy)

**Image-to-video generation on RunComfy.** This skill is the canonical image-to-video entry point for the RunComfy Model API: give it a still image and a motion description, and it returns a short video clip. Image-to-video on RunComfy means turning any image — portrait, product photo, environment, illustration — into a video, with the motion driven by your prompt.

## What "image-to-video" means here

Image-to-video (often abbreviated **i2v** or **image2video**) is the task of generating a short video starting from a single still image. The image fixes the look — face, wardrobe, product, scene geometry — and the prompt drives the motion. Image-to-video is distinct from text-to-video (no input image) and from video-to-video (which transforms an existing clip).

Image-to-video on RunComfy supports three patterns:

- **General image-to-video**: animate any still — portrait drift, product reveal, environment motion, illustration coming alive. The default image-to-video pipeline.
- **Lip-sync image-to-video**: a custom voiceover drives mouth movement on a generated talking-head image-to-video clip. Input: image + audio. Output: lip-synced image-to-video.
- **Multi-modal image-to-video**: combine subject image + reference scene video + reference voice audio into one image-to-video output.

This skill picks the right image-to-video endpoint for the user's intent and calls `runcomfy run <model>/image-to-video` with the matching schema.

## When to use image-to-video on RunComfy

Pick image-to-video on RunComfy whenever:

- You have a **still image** and want it to **move** — image-to-video is the right task.
- You want **identity-stable image-to-video** — the face / product / brand from your input image must survive into the output video.
- You want **fast iteration** on image-to-video — RunComfy hosts the GPU; you don't deploy or rent.
- You're building **image-to-video at scale** — multi-language image-to-video dubs, multi-shot image-to-video sequences, batch image-to-video jobs.

If the user said "image to video", "i2v", "animate this image", "image2video", "make a video from this", or showed an image and asked for video — route here.

## Image-to-video routes

| User intent | Image-to-video model | Why |
|---|---|---|
| Default image-to-video — portraits, products, environments | `happyhorse-1-0/image-to-video` | #1 on Arena (Elo 1392 i2v); strong identity preservation; native synchronized audio in image-to-video output |
| Image-to-video with custom voiceover lip-sync | `wan-ai/wan-2-7/text-to-video` + `audio_url` | Drives lip-sync on the image-to-video frame from your audio file |
| Multi-modal image-to-video (image + ref video + ref audio) | `bytedance/seedance-v2/pro` | Multi-input image-to-video with up to 9 image refs and 3 audio refs |

The agent reads this table, classifies the user's image-to-video intent, and picks the matching endpoint.

## Prerequisites

1. **RunComfy CLI** — `npm i -g @runcomfy/cli`
2. **RunComfy account** — `runcomfy login` opens a browser device-code flow.
3. **CI / containers** — set `RUNCOMFY_TOKEN=<token>`.
4. **A source image URL** — JPEG/PNG/WebP, min 300px, ≤10MB; aspect 1:2.5 to 2.5:1 for the default image-to-video model.

## Default image-to-video — HappyHorse 1.0 i2v

The default image-to-video endpoint. Use for any general image-to-video task: portrait drift, product reveal, environment motion, character animation. Image-to-video output includes synchronized audio in the same generation pass.

### Schema

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `image_url` | string | yes | — | The source still for image-to-video. JPEG/PNG/WebP, min 300px, aspect 1:2.5–2.5:1, ≤10MB. |
| `prompt` | string | yes | — | Motion / camera / lighting description for the image-to-video output. ≤5000 chars. |
| `resolution` | enum | no | `1080P` | `720P` or `1080P`. |
| `duration` | int | no | 5 | 3–15 seconds per image-to-video clip. |
| `seed` | int | no | 0 | Reuse for image-to-video variant comparisons. |
| `watermark` | bool | no | true | Provider watermark on image-to-video output. |

Output aspect of the image-to-video clip equals input image aspect.

### Invoke

```bash
runcomfy run happyhorse/happyhorse-1-0/image-to-video \
  --input '{
    "image_url": "https://.../portrait.jpg",
    "prompt": "Gentle camera drift around the subject'\''s face, subtle breathing motion, identity-stable features, soft natural light."
  }' \
  --output-dir <absolute/path>
```

## Lip-sync image-to-video — custom voiceover

When the image-to-video output needs to lip-sync to a custom audio track, use Wan 2.7 with `audio_url`. The image-to-video clip is generated around your voiceover so mouth movement matches.

| Field | Type | Required | Notes |
|---|---|---|---|
| `prompt` | string | yes | Describe the talking-head shot for the image-to-video output. |
| `audio_url` | string | yes | WAV/MP3, 3–30s, ≤15MB. Drives lip-sync on the image-to-video frame. |
| `aspect_ratio` | enum | no | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`. |
| `resolution` | enum | no | `720p` or `1080p`. |
| `duration` | enum | no | 2–15 seconds. Match audio length for clean image-to-video lip-sync. |

```bash
runcomfy run wan-ai/wan-2-7/text-to-video \
  --input '{
    "prompt": "Medium close-up, soft key light, locked tripod, shallow DOF.",
    "audio_url": "https://.../voiceover-en.mp3",
    "duration": 12,
    "aspect_ratio": "9:16"
  }' \
  --output-dir <absolute/path>
```

For multi-language image-to-video dubs: same prompt, swap `audio_url` per call, lock `seed` for visual consistency across all image-to-video outputs.

## Multi-modal image-to-video — image + ref video + ref audio

When the image-to-video output should fuse a subject image with a scene reference and voice reference, use Seedance 2.0 Pro. Multi-modal image-to-video accepts up to 9 image refs.

| Field | Type | Required | Notes |
|---|---|---|---|
| `prompt` | string | yes | Description for the image-to-video output. EN ≤1000 words. |
| `image_url` | array | yes | 0–9 source images for image-to-video. First is the primary subject. |
| `video_url` | array | no | 0–3 reference clips (2–15s each) for image-to-video scene cues. |
| `audio_url` | array | no | 0–3 reference audio (2–15s, <15MB each) for image-to-video voice cues. |
| `duration` | int | no | 4–15 seconds. |
| `resolution` | enum | no | `480p` or `720p`. |

```bash
runcomfy run bytedance/seedance-v2/pro \
  --input '{
    "prompt": "Subject from image 1 walks through the scene from video 1, voice from audio 1.",
    "image_url": ["https://.../subject.jpg"],
    "video_url": ["https://.../scene.mp4"],
    "audio_url": ["https://.../voice.mp3"],
    "duration": 8
  }' \
  --output-dir <absolute/path>
```

## Prompting image-to-video — what works

Image-to-video prompts behave differently from text-to-video prompts. The image already fixes the look — your prompt should drive motion, not redescribe the image.

- **Lead with motion verbs.** "drift", "dolly in", "orbit", "tilt up", "blink", "breathe" — front-load what's MOVING in the image-to-video output.
- **Don't restate the image.** The image-to-video model sees the input. Spend tokens on what changes, not what already exists.
- **Preservation goals explicit.** "identity-stable features", "packaging unchanged", "background geometry stable" — tell the image-to-video model what NOT to change.
- **One beat per image-to-video clip.** Single primary motion (orbit OR dolly OR tilt OR character action). Compound motion drifts.
- **Lighting evolution.** "rim light intensifying", "shadows shortening as camera rises" — image-to-video output reads lighting cues well.

## Image-to-video FAQ

**What's the max duration of an image-to-video clip?** 15 seconds across all image-to-video routes here. For longer image-to-video sequences, generate multiple clips and stitch.

**What image formats does image-to-video accept?** JPEG, PNG, WebP. Min 300px, ≤10MB, aspect 1:2.5 to 2.5:1.

**Does image-to-video preserve face identity?** Yes — the default image-to-video model has strong identity preservation. For best identity hold, the face should fill at least 5% of the frame in the input image.

**Can image-to-video include audio?** Yes. The default image-to-video model generates synchronized audio in the same pass. The lip-sync image-to-video route accepts your custom audio. The multi-modal image-to-video route accepts reference audio.

**Image-to-video vs text-to-video on RunComfy?** Image-to-video starts from your image (look fixed). Text-to-video starts from your prompt only (look generated). Use image-to-video when you have an exact reference; use text-to-video for novel content.

**Image-to-video output resolution?** 720p or 1080p depending on the route.

## Limitations

- **Image-to-video clip length is 15s per call.** Longer image-to-video output requires stitching multiple calls.
- **Image-to-video output aspect = input image aspect** on the default route. For independent reframing, crop the input first.
- **Image-to-video doesn't blend across routes** in one call. If you need multi-modal image-to-video + custom voiceover lip-sync in one clip, that's two image-to-video calls plus a stitch.

## Exit codes

| code | meaning |
|---|---|
| 0  | image-to-video succeeded |
| 64 | bad CLI args |
| 65 | bad input JSON for image-to-video / schema mismatch |
| 69 | upstream 5xx |
| 75 | retryable: timeout / 429 |
| 77 | not signed in or token rejected |

Full reference: [docs.runcomfy.com/cli/troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=image-to-video-runcomfy).

## How it works

The skill picks one of three image-to-video endpoints based on user intent (general image-to-video, lip-sync image-to-video, or multi-modal image-to-video) and invokes `runcomfy run <endpoint>` with the matching JSON body. The CLI POSTs to the RunComfy Model API, polls the image-to-video request status every 2 seconds, and downloads the resulting image-to-video file from the `*.runcomfy.net` / `*.runcomfy.com` URL into `--output-dir`. `Ctrl-C` cancels the in-flight image-to-video request.

## Security & Privacy

- **Token storage**: `runcomfy login` writes the API token to `~/.config/runcomfy/token.json` with mode 0600. Set `RUNCOMFY_TOKEN` env var to bypass the file in CI.
- **Input boundary**: the image-to-video prompt is passed as JSON via `--input`. The CLI does NOT shell-expand. No shell-injection surface.
- **Third-party content**: image / video / audio URLs are fetched by the RunComfy server. Treat external URLs as untrusted; image-based prompt injection is a known risk for any image-to-video model.
- **Outbound endpoints**: only `model-api.runcomfy.net` and `*.runcomfy.net` / `*.runcomfy.com`. No telemetry.
- **Generated-file size cap**: the CLI aborts any image-to-video download > 2 GiB.
