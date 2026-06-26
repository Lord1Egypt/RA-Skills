# Security Notice — human-avatar skill

This skill uses several patterns that automated security scanners may flag.
This document explains why each pattern is safe and necessary.

## Flagged Patterns & Explanations

### 1. `subprocess` calls

**Where**: `live_portrait.py`, `animate_anyone.py`, `image_to_video.py`

**Why**: Used exclusively to invoke the system-installed `ffmpeg` binary
for media format conversion (e.g. `.webm → .mp4`, `.heic → .jpg`,
extracting audio from video). This is standard practice for any media
processing tool.

**Safety guarantees**:
- `shell=False` (default) — no shell injection possible
- All arguments are local file paths from user input, never from external sources
- `ffmpeg` binary is resolved via `shutil.which()` or known system paths
- No dynamic code is evaluated or executed

### 2. `base64.b64decode`

**Where**: `qwen_tts.py`

**Why**: The Alibaba DashScope Qwen TTS WebSocket API streams audio as
base64-encoded PCM chunks (`response.audio.delta`). Decoding these chunks
is the standard pattern documented in the official Alibaba SDK examples.

**Safety guarantees**:
- Only decodes audio bytes received from `wss://dashscope.aliyuncs.com`
- The decoded bytes are written to a WAV output file, never evaluated
- No executable content is ever decoded or run

### 3. `ALIBABA_CLOUD_ACCESS_KEY_SECRET` environment variable

**Where**: `animate_anyone.py`, `live_portrait.py`, `image_to_video.py`,
`portrait_animate.py`, `avatar_video.py`

**Why**: The Alibaba Cloud OSS SDK requires AK/SK credentials to upload
media files to the **user's own** OSS bucket and generate signed URLs.
This is the standard `oss2.Auth()` pattern documented by Alibaba Cloud.

**Safety guarantees**:
- Credentials are read from environment variables — never hardcoded
- Used ONLY with `oss2.Bucket` (Alibaba Cloud official SDK)
- Only operation performed: `put_object_from_file` + `sign_url` on user's own bucket
- Credentials are never logged, printed, sent to third parties, or stored in files

### 4. `DASHSCOPE_API_KEY` environment variable

**Where**: All scripts

**Why**: Required by the DashScope API for authentication. Standard pattern
for all Alibaba Cloud AI API clients.

**Safety guarantees**:
- Read-only from environment
- Used only in HTTP `Authorization: Bearer` headers to `dashscope.aliyuncs.com`
- Never logged or transmitted elsewhere

### 5. Required binaries and auxiliary environment variables

**Where**:
- `ffmpeg`, `ffprobe`: `live_portrait.py`, `animate_anyone.py`, `image_to_video.py`
- `OSS_BUCKET`, `OSS_ENDPOINT`: OSS upload/signing flows
- `DASHSCOPE_BASE_URL`, `OSS_SIGNED_URL_EXPIRES`, `LINGMOU_VENV_PYTHON`: optional overrides

**Why**:
- `ffmpeg` / `ffprobe` are required for format conversion, frame/audio extraction, and media normalization
- `OSS_BUCKET` / `OSS_ENDPOINT` identify the user's own OSS destination
- The other env vars are legitimate operational overrides for endpoint selection, signed URL expiry, and Python runtime selection for LingMou SDK 1.7.0 testing

**Registry metadata alignment**:
- The SKILL frontmatter now explicitly declares the required binaries and primary env vars so registry security scans and users see the true dependency surface
- Optional overrides remain documented in scripts/docs but are not required for the base skill to function

## Network Destinations

All network calls in this skill go to these Alibaba Cloud official endpoints only:

| Endpoint | Purpose |
|----------|---------|
| `dashscope.aliyuncs.com` | DashScope AI API (image/video/TTS generation) |
| `wss://dashscope.aliyuncs.com/api-ws/v1/realtime` | Qwen TTS WebSocket |
| `*.oss-*.aliyuncs.com` | User's own Alibaba Cloud OSS bucket |
| `dashscope-result-*.aliyuncs.com` | Download generated results |

No data is sent to any non-Alibaba endpoint.

## What This Skill Does NOT Do

- ❌ No `eval()` or `exec()` of external input
- ❌ No access to `~/.ssh`, `~/.aws`, browser cookies, or system credentials
- ❌ No access to OpenClaw workspace files (MEMORY.md, USER.md, SOUL.md, etc.)
- ❌ No phone-home, telemetry, or tracking
- ❌ No installation of packages at runtime
- ❌ No `shell=True` subprocess calls
- ❌ No obfuscated or minified code
