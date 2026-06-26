---
name: music-composer
description: Music composition assistant. Accepts natural language input, guides the user through multi-turn interaction to define genre, mood, theme, tempo, and other musical elements, generates structured prompts for Suno/Udio, and saves the output to a user-specified path.
---

# Music Composer

This skill helps users go from a single natural language description to a finished music file, through a structured multi-turn conversation.

## When to Use

Trigger this skill when the user:
- Says "create a song", "generate some music", "I want a track that..."
- Describes a mood, scene, or use case (e.g. "something for working out", "a sad piano piece")
- Wants to use Suno or Udio but doesn't know how to write a prompt

## Workflow

### Step 1: Understand Intent

Parse the user's initial input. Extract any elements already mentioned, identify what's missing.

**Core music elements:**

| Element | Description | Examples |
|---------|-------------|---------|
| Genre | Style of music | Pop, Jazz, Lo-fi, Classical, EDM, Folk |
| Mood | Emotional tone | Upbeat, melancholic, energetic, calm, mysterious |
| Theme | Subject or scene | Heartbreak, travel, morning, city at night |
| Tempo | Speed | Slow 60bpm / Medium 120bpm / Fast 160bpm |
| Instruments | Main sounds | Piano, guitar, synth, strings, drum machine |
| Duration | Target length | 30s / 1 minute / full song (3-4 min) |
| Vocals | Voice presence | Instrumental / male / female / choir |
| Language | Lyric language (if vocals) | English / Chinese / no lyrics |

### Step 2: Multi-Turn Interaction

Ask about missing elements in batches — max 2-3 questions per round. Wait for the user's reply before moving to the next round.

**Interaction rules:**
- Offer 3-4 labeled options per element, plus a "custom" option
- If the user says "up to you" or "whatever", pick recommended defaults and move on
- Keep the tone conversational and light

**Round 1 — Genre + Mood:**
```
Got it! Let me help you build this track. A couple of quick questions:

1. Genre preference?
   A. Lo-fi Hip-hop (relaxed, study vibes)
   B. Pop (catchy, accessible)
   C. EDM (high energy, driving beat)
   D. Classical / Neo-classical (instrumental, refined)
   E. Custom: ___

2. Overall mood?
   A. Upbeat and happy
   B. Melancholic
   C. Motivating / energetic
   D. Calm and meditative
```

**Round 2 — Tempo + Instruments:**
```
Got it! Two more:

1. Tempo?
   A. Slow (60-80 BPM — relaxing, sleep)
   B. Medium (90-120 BPM — everyday background)
   C. Fast (130-160 BPM — workout, focus)

2. Main instruments? (pick multiple)
   Piano / Guitar / Synth / Strings / Drum machine / Bass / Custom
```

**Round 3 — Vocals + Duration + Output path:**
```
Almost there:

1. Vocals?
   A. Instrumental only
   B. Female vocals
   C. Male vocals

2. Duration?
   A. Short clip (30s)
   B. 1 minute
   C. Full track (3-4 min)

3. Where should the file be saved? (enter a folder path)
```

### Step 3: Generate Prompt Options

Once all elements are collected, present **2-3 style variants** for the user to choose from. Each variant includes:
- A name and style description
- A complete English prompt ready for Suno or Udio

**Format:**
```
Option A — "Midnight Drive"
Style: Dark, cinematic lo-fi with a slow groove

Prompt:
lo-fi hip hop, melancholic, late night city drive, slow tempo 75bpm,
piano melody, vinyl crackle, soft drums, bass guitar,
instrumental, 2 minutes, atmospheric, nostalgic

Option B — "Neon Glow" (City Pop flavor)
Style: 80s-inspired City Pop, warm synths, nostalgic

Prompt:
city pop, 1980s inspired, nostalgic, upbeat 110bpm,
electric piano, synthesizer, bass, light drums,
instrumental, dreamy, 3 minutes
```

### Step 4: API Setup Guidance

Before generating, check whether the user has API access configured. If not, explain the options:

#### Option 1: Web interface (no setup required)
```
The easiest way — paste the prompt directly into the web app:
- Suno: https://suno.com
- Udio: https://www.udio.com

Download the result manually and save it to your chosen folder.
```

#### Option 2: Self-hosted API (automated)
```
Suno and Udio do not have official public APIs.
Community-maintained wrappers are available on GitHub:
- Suno: https://github.com/gcui-art/suno-api
- Udio: https://github.com/udioapi/udio-api

These require your account session credentials.
Store credentials in a local .env file — never hardcode them in scripts.
Refer to each project's README for setup instructions.
```

### Step 5: Generate and Save

Once the user confirms a prompt and has API access ready, run the generation script:

```python
import requests
import os

def generate_music(prompt: str, output_path: str):
    """
    Call the local Suno API and save the result to output_path.
    Requires SUNO_API_URL set in environment (e.g. http://localhost:3000).
    Credentials must be configured in the API service, not passed here.
    """
    api_url = os.getenv("SUNO_API_URL")
    if not api_url:
        raise EnvironmentError("SUNO_API_URL is not set in environment variables.")

    response = requests.post(f"{api_url}/api/generate", json={
        "prompt": prompt,
        "make_instrumental": True,
        "wait_audio": True
    })

    if response.status_code != 200:
        raise RuntimeError(f"API request failed: {response.status_code}")

    data = response.json()

    os.makedirs(output_path, exist_ok=True)
    saved = []
    for i, item in enumerate(data):
        audio_url = item.get("audio_url")
        if audio_url:
            audio_data = requests.get(audio_url).content
            filepath = os.path.join(output_path, f"track_{i+1}.mp3")
            with open(filepath, "wb") as f:
                f.write(audio_data)
            saved.append(filepath)

    return saved
```

After generation, report to the user:
```
Music saved to: [output path]/track_1.mp3

Details:
- Duration: ~3 minutes
- Format: MP3
- Prompt used: [prompt text]

Want to regenerate or adjust the style?
```

## Notes

- Music generated via Suno/Udio is subject to each platform's terms of service — verify before commercial use
- Community API wrappers may break when platforms update — check the respective GitHub repos for status
- If the API is unavailable, output the full prompt so the user can generate manually via the web interface
- The output directory will be created automatically if it does not exist
