---
name: manim-animation
description: "Create mathematical animations with synchronized voiceover narration and subtitles using Manim Community and manim-voiceover. Use when users want to create animated videos with narration, math animations with voice, educational videos with subtitles, or any request involving Manim scene generation with TTS voiceover. Trigger phrases include: manim animation, math animation, animated video with voice, manim voiceover, create animation video, or any request to generate narrated mathematical/educational animation videos."
required_tools:
  - name: manim
    install: "pip install manim"
  - name: ffmpeg
    install: "brew install ffmpeg (macOS) / apt install ffmpeg (Linux)"
    notes: "Must include libx264 encoder and libass (for subtitle burn-in)"
  - name: python3
    install: "Python 3.9+ required"
required_packages:
  - "manim"
  - "manim-voiceover[gtts]"
network_access:
  - service: "Google TTS (gTTS)"
    purpose: "Text-to-speech synthesis for voiceover narration"
    required: false
    notes: "Default TTS engine. Can be replaced with offline pyttsx3 if network is unavailable."
---

# Manim Animation: Animation + Voiceover + Subtitle Generator

**Author:** ericksun（孙自翔）

## Overview

This skill uses Manim Community to generate mathematical/educational animations, with manim-voiceover plugin integration for TTS voice narration and synchronized subtitles. All processing runs locally — no paid API required.

**Core Capabilities:**
- 🎬 **Animation Generation**: Create animations of math formulas, geometric shapes, charts, and more with Manim
- 🎙️ **Voice Narration**: Integrate TTS via manim-voiceover plugin with automatic animation-voice sync
- 📝 **Subtitle System**: In-scene subtitles (Manim Text) + SRT external subtitles (ffmpeg burn-in)
- 🔄 **One-Click Pipeline**: Describe requirements → Generate code → Render video → Burn subtitles

**TTS Engines (gTTS preferred):**
- **gTTS** (Recommended): Google free TTS, supports Chinese, no API Key needed
- **pyttsx3** (Fallback): Offline TTS, no network required
- **Azure/OpenAI/ElevenLabs** (High quality): Requires paid API Key

## Prerequisites

### 🔍 One-Click Environment Check

**Before first use, run the environment check script to verify all dependencies are ready:**

```bash
python3 {SKILL_DIR}/scripts/check_environment.py
```

This script checks:
- ✅ Manim Community installation (`manim` command)
- ✅ manim-voiceover + gTTS plugin
- ✅ FFmpeg + libx264 encoder (hardcoded Manim dependency, **required**)
- ✅ FFmpeg + libass (for SRT subtitle burn-in)
- ✅ Python dependencies
- ✅ Chinese font availability

### Required System Tools

- **Manim Community**: `pip install manim`
- **FFmpeg (with libx264 + libass)**: Manim hardcodes the `libx264` encoder for video rendering; subtitle burn-in requires `libass`
  - macOS (Homebrew): `brew install ffmpeg` (includes x264 and libass by default)
  - macOS (Conda): `conda install x264 -c conda-forge` (**⚠️ conda's ffmpeg does not include libx264 by default**)
  - Linux: `sudo apt install ffmpeg libx264-dev libass-dev`
- **Python 3.9+** and pip

### Required Python Packages

```bash
# Core
pip install manim

# Voiceover + TTS
pip install "manim-voiceover[gtts]"
```

### Optional (Enhanced Features)

- **pyttsx3**: Offline TTS (`pip install "manim-voiceover[pyttsx3]"`)

### ⚡ Quick Install

```bash
pip install manim "manim-voiceover[gtts]"

# macOS (Homebrew) — Recommended, includes libx264 + libass
brew install ffmpeg

# macOS (Conda) — Requires additional x264 install, otherwise Manim render will fail with UnknownCodecError: libx264
conda install x264 -c conda-forge

# Verify ffmpeg supports libx264 and libass
ffmpeg -codecs 2>&1 | grep libx264     # Should show: encoders: libx264
ffmpeg -filters 2>&1 | grep subtitles  # Should show: subtitles filter
```

## Workflow

### Quick Start — One-Click Run

After the user describes their requirements, use the pipeline script for one-click execution:

```bash
python3 {SKILL_DIR}/scripts/run_pipeline.py \
    --scene_file <scene_file.py> \
    --scene_name <SceneName> \
    --quality high \
    --burn_subtitles
```

**Common Options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--scene_file` | Required | Manim scene Python file |
| `--scene_name` | Required | Scene class name |
| `--quality` | `high` | Render quality: `low`/`medium`/`high`/`production` |
| `--burn_subtitles` | False | Whether to burn SRT subtitles with ffmpeg |
| `--speed` | `1.35` | Playback speed multiplier (e.g., 1.35 means 1.35x speed; set to 1.0 to disable) |
| `--preview` | False | Auto-open preview after rendering |
| `--output_dir` | `./output` | Output directory |

### Complete Workflow (4 Steps)

#### Step 1: Understand User Requirements and Generate Manim Scene Code

Based on the user's description, generate a Manim scene Python file. Scene code should follow these patterns:

**No-voiceover mode** (animation only):

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        title = Text("Title", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(1)
```

**Voiceover mode** (animation + voice + subtitles):

```python
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class MyScene(VoiceoverScene):
    def _make_subtitle(self, text_str):
        """Create subtitle with dark background at bottom of screen."""
        sub = Text(text_str, font_size=22, color=WHITE, weight=BOLD)
        # Prevent subtitle from overflowing left/right edges
        max_width = config.frame_width - 1.0  # 0.5 margin each side
        if sub.width > max_width:
            sub.scale_to_fit_width(max_width)
        sub.to_edge(DOWN, buff=0.4)
        bg = BackgroundRectangle(sub, color=BLACK, fill_opacity=0.6, buff=0.15)
        return VGroup(bg, sub)

    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))

        sub_text = "Welcome to the demo"
        with self.voiceover(text=sub_text) as tracker:
            sub = self._make_subtitle(sub_text)
            title = Text("Demo", font_size=48)
            self.play(Write(title), FadeIn(sub), run_time=tracker.duration)

        self.play(FadeOut(sub))
        self.wait(0.3)
```

**Key Pattern — voiceover context manager:**

```python
with self.voiceover(text="Speech text") as tracker:
    # tracker.duration = TTS speech duration (seconds)
    # Animations within this block auto-sync with voice
    self.play(SomeAnimation(), run_time=tracker.duration)
```

`with self.voiceover(text=...) as tracker` does three things:
1. Calls the TTS engine to generate speech audio
2. Automatically calculates speech duration
3. Provides `tracker.duration` to sync animations with voice

**Subtitle Best Practices:**
- In-scene subtitles: Use the `_make_subtitle()` helper to display white bold text with dark background at the bottom of the screen
- **Overflow prevention**: `_make_subtitle()` auto-detects subtitle width and scales proportionally (`scale_to_fit_width`) when exceeding frame bounds; uses `font_size=22` for long text
- **Subtitle sync**: `FadeIn(sub)` in the **first** `self.play()` within the voiceover block ensures subtitles appear in sync with voice — do not delay
- FadeIn subtitle at the start of each voiceover block, FadeOut after it ends
- Subtitle text should match the voiceover text

**⚠️ Avoid Double Subtitles:** If the scene code already uses `_make_subtitle()` to render in-scene subtitles, **do not** also use `--burn_subtitles` to burn SRT subtitles, otherwise two overlapping subtitle layers will appear. Choose only one approach:
- Option A (Recommended): Render subtitles in code with `_make_subtitle()`, do not burn SRT
- Option B: Do not render subtitles in code, burn SRT via `--burn_subtitles`

#### Step 2: Configure Rendering Parameters

Create `manim.cfg` in the same directory as the scene file:

```ini
[CLI]
quality = high_quality
preview = False

[ffmpeg]
video_codec = h264
```

**Quality Reference Table:**

| Quality | Flag | Resolution | FPS | manim.cfg Value |
|---------|------|------------|-----|-----------------|
| Low | -ql | 480p | 15 | low_quality |
| Medium | -qm | 720p | 30 | medium_quality |
| High | -qh | 1080p | 60 | high_quality |
| Production | -qp | 2160p | 60 | production_quality |

#### Step 3: Render Video

```bash
manim render <scene_file.py> <SceneName>
```

Output path pattern: `media/videos/<file>/<resolution>/<SceneName>.mp4`

#### Step 4: Burn SRT Subtitles (Optional)

manim-voiceover automatically generates `.srt` subtitle files in the same directory as the video. Burn with ffmpeg:

```bash
ffmpeg -y -i <video.mp4> \
    -vf "subtitles=<subtitle.srt>:force_style='FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,BackColour=&H80000000,BorderStyle=4,MarginV=30'" \
    -c:a copy \
    <output_subtitled.mp4>
```

**⚠️ Double Subtitle Pitfall**: If the scene Python code already renders in-scene subtitles with `_make_subtitle()`, **do not** also burn SRT subtitles, otherwise two overlapping subtitle layers will appear.

**Note**: ffmpeg requires libass support. On macOS, `brew install ffmpeg` typically includes it. Conda environments may require `conda install x264 -c conda-forge`.

#### Step 5: Speed Up Video (Optional)

Use ffmpeg to speed up the video, default 1.35x:

```bash
SPEED=1.35
ffmpeg -y -i <input.mp4> \
    -filter_complex "[0:v]setpts=PTS/${SPEED}[v];[0:a]atempo=${SPEED}[a]" \
    -map "[v]" -map "[a]" \
    <output_fast.mp4>
```

**Note**: Speed-up should be the final output step. If the scene code has in-scene subtitles (`_make_subtitle`), the speed-up input should use the original video (not the SRT-burned version) to avoid double subtitles. The `run_pipeline.py` `--speed` parameter handles this logic automatically.

## Manim Common Animation Reference

### Create/Display Animations
- `Write(text)` — Write text
- `Create(mobject)` — Draw shapes
- `FadeIn(mobject)` / `FadeOut(mobject)` — Fade in/out
- `DrawBorderThenFill(mobject)` — Draw border then fill

### Transform Animations
- `Transform(source, target)` — Morph
- `ReplacementTransform(source, target)` — Replacement morph
- `TransformMatchingShapes(source, target)` — Shape-matching morph

### Move/Scale
- `mobject.animate.to_edge(UP)` — Move to edge
- `mobject.animate.shift(RIGHT * 2)` — Translate
- `mobject.animate.scale(2)` — Scale
- `Rotate(mobject, angle=PI)` — Rotate

### Common Objects
- `Text("Text", font_size=48, color=BLUE)` — Text
- `MathTex(r"e^{i\pi}+1=0")` — LaTeX formula
- `Circle(radius=1, color=RED)` — Circle
- `Square(side_length=2, color=GREEN)` — Square
- `Arrow(start, end)` — Arrow
- `NumberPlane()` — Coordinate plane
- `Axes(x_range, y_range)` — Axes

### Grouping and Layout
- `VGroup(obj1, obj2)` — Vertical group
- `group.arrange(RIGHT, buff=0.5)` — Horizontal arrangement
- `BackgroundRectangle(obj, color=BLACK, fill_opacity=0.6)` — Background rectangle

## Known Issues and Solutions

### ⚠️ Missing libx264 Codec (Most Common Issue)

**Symptom**: `UnknownCodecError: libx264`

**Root Cause**: Manim hardcodes the `libx264` encoder in `scene_file_writer.py` (cannot be overridden via config/cfg), but conda environment's ffmpeg is compiled with `--disable-gpl` and does not include the GPL-licensed libx264.

**Solution**:
```bash
# Conda environment (most common scenario)
conda install x264 -c conda-forge
# After installation, conda-forge's ffmpeg will auto-relink the x264 library

# Verify
ffmpeg -codecs 2>&1 | grep libx264
# Output should include: encoders: libx264 libx264rgb
```

**Note**: `brew install ffmpeg` installs ffmpeg with built-in x264, but conda environments prioritize their own ffmpeg and will not use the Homebrew version.

### setuptools Compatibility
`manim-voiceover` depends on `pkg_resources`, which may fail on Python 3.12+:
```bash
pip install "setuptools>=69.0,<72.0"
```

### ffmpeg Missing libass
SRT subtitle burn-in requires libass. macOS:
```bash
brew install ffmpeg
# Verify
ffmpeg -filters 2>&1 | grep subtitles
```

Linux:
```bash
sudo apt install libass-dev
# May need to recompile ffmpeg
```

### gTTS Network Issues
gTTS requires access to Google TTS service. If network is unavailable, switch to pyttsx3 offline engine:
```python
from manim_voiceover.services.pyttsx3 import Pyttsx3Service
self.set_speech_service(Pyttsx3Service())
```

### Chinese Fonts
Manim uses system fonts to render `Text` objects. Ensure Chinese fonts are available:
- macOS: PingFang SC (built-in)
- Linux: `sudo apt install fonts-noto-cjk`
- Specify font: `Text("Text", font="PingFang SC")`

## Related Resources

- **GitHub Repository**: https://github.com/hzsunzixiang/manim-animation-skill
- **Manim Technical Guide**: `references/manim_guide.md` — Detailed Manim + voiceover + subtitle technical documentation
- **Environment Check Script**: `scripts/check_environment.py` — One-click dependency check
- **Render Pipeline Script**: `scripts/run_pipeline.py` — One-click render + subtitle burn-in
