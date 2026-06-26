---
name: video-bgm
description: Analyze a video's mood and add AI-generated BGM. Optionally speed up/slow down. Uses Gemini for video analysis and fal.ai Lyria2 for music generation. Triggers on "add bgm", "add music to video", "video bgm", or any request to add background music to a video file.
homepage: https://canlah.ai
metadata: {"openclaw": {"emoji": "🎵", "os": ["darwin", "linux"]}}
---

# Video BGM Skill

Analyze a video's content and mood, generate matching BGM via AI, and mix it in.

---

## Pipeline

```
Input Video → Gemini Analysis → Lyria2 BGM → FFmpeg Mix → Output
                (mood/style)     (generate)    (speed + volume + fade)
```

## Dependencies

- **Python**: `python3` (or activate your project venv if available)
- **Gemini API**: `GOOGLE_GENAI_API_KEY` (video understanding)
- **fal.ai**: `FAL_API_KEY` (Lyria2 music generation)
- **FFmpeg**: system install

## Setup

```bash
# Install required packages
pip install google-generativeai httpx

# Set API keys via environment variables
export GOOGLE_GENAI_API_KEY="your_google_api_key"
export FAL_API_KEY="your_fal_api_key"
```

## Usage

```
/video-bgm <path-to-video>
/video-bgm <path-to-video> --speed 1.1
/video-bgm <path-to-video> --speed 1.1 --volume 5
/video-bgm <path-to-video> --style "lo-fi chill"
```

## Arguments

| Arg | Default | Description |
|-----|---------|-------------|
| `path` | (required) | Path to input video file |
| `--speed` | `1.0` | Speed multiplier (e.g. 1.1 = 10% faster) |
| `--volume` | `5.0` | BGM volume multiplier (Lyria2 output is quiet) |
| `--fade-in` | `1.5` | Fade in duration in seconds |
| `--fade-out` | `3.0` | Fade out duration in seconds |
| `--style` | (auto) | Override music style (skip Gemini analysis) |

## Step-by-Step Process

### Step 1: Analyze Video with Gemini

Upload video to Gemini 2.0 Flash and get deep mood analysis.

```python
import google.generativeai as genai
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_GENAI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
```

Use this analysis prompt (acts as music supervisor, not generic):

```
Watch this video very carefully. You are a music supervisor for commercials.

Tell me:
1. What BRAND POSITIONING does this video convey? (luxury? affordable? aspirational?)
2. What is the EMOTIONAL JOURNEY of the viewer? Be specific at each moment.
3. What REAL commercial music references would fit? Name specific ad styles
   (Four Seasons resort? Apple reveal? Volvo? Pottery Barn? Nike?)
4. What is the ENERGY LEVEL? Contemplative/still or forward momentum?
5. What tempo, instruments, and production style would ACTUALLY work?
   Be honest - classical piano is often too stuffy. Consider modern alternatives.

Then provide a SINGLE music generation prompt (2-3 sentences) that captures
the ideal BGM. Focus on: instruments, tempo BPM, mood adjectives, production style.
Format: MUSIC_PROMPT: <your prompt here>
```

### Step 2: Extract the MUSIC_PROMPT

Parse the Gemini response to find the `MUSIC_PROMPT:` line. This becomes the Lyria2 prompt.

Always APPEND these constraints to any Lyria2 prompt:
```
No vocals, no drums, no percussion hits, no sound effects.
```

### Step 3: Generate BGM via fal.ai Lyria2

```python
import httpx
import os

FAL_API_KEY = os.environ.get("FAL_API_KEY")

resp = httpx.post(
    "https://fal.run/fal-ai/lyria2",
    headers={
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json",
    },
    json={"prompt": music_prompt},
    timeout=120.0,
)
audio_url = resp.json()["audio"]["url"]
```

Lyria2 generates ~32s of audio. Output is WAV, 48kHz stereo.

### Step 4: FFmpeg — Speed + Strip Audio + Mix BGM

```bash
# Step 4a: Speed up video (if requested) and strip any existing audio
ffmpeg -y -i INPUT.mp4 \
  -filter:v "setpts=PTS/{speed}" \
  -an \
  -c:v libx264 -preset medium -crf 18 \
  OUTPUT_speedup.mp4

# Step 4b: Get sped-up duration
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 OUTPUT_speedup.mp4)

# Step 4c: Mix BGM with volume boost, fade in/out, trim to video length
ffmpeg -y \
  -i OUTPUT_speedup.mp4 \
  -i bgm.wav \
  -filter_complex "[1:a]volume={volume},atrim=0:{duration},afade=t=in:st=0:d={fade_in},afade=t=out:st={duration-fade_out}:d={fade_out}[a]" \
  -map 0:v -map "[a]" \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  OUTPUT_final.mp4
```

### Step 5: Open Result

Open the final video for user review. Also open the BGM separately so they can evaluate the music alone.

## Key Learnings

- **Lyria2 output is VERY QUIET** — always use volume multiplier (default 5.0)
- **Don't over-specify the Lyria2 prompt** — "three acts" style prompts produce chaotic results. Keep it to instruments + tempo + mood + style reference.
- **Let Gemini act as music supervisor** — it gives much better style recommendations than generic "relaxing piano" defaults
- **Always strip existing audio first** (`-an`) — some videos have unwanted audio tracks
- **Classical piano is usually wrong** — for luxury/lifestyle, modern minimalist (Rhodes, guitar, cello) works better

## Output Files

All files are saved next to the input video:
```
input_video.mp4          → original
input_video_speedup.mp4  → sped up, no audio
input_video_bgm.wav      → generated BGM
input_video_final.mp4    → final output with BGM
```

## Examples

```bash
# Basic: analyze and add BGM
/video-bgm ~/Desktop/product_video.mp4

# Speed up 10% and add BGM
/video-bgm ~/Desktop/product_video.mp4 --speed 1.1

# Override style (skip Gemini analysis)
/video-bgm ~/Desktop/ad.mp4 --style "upbeat modern pop, synth pads, 100 BPM"

# Adjust volume
/video-bgm ~/Desktop/quiet_video.mp4 --volume 8
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
