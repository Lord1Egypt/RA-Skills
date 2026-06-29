---
name: lygo-resonance
description: LYGO RESONANCE — Image-to-Sound & Creative Profiles. Transforms any image into rich stereo soundscapes (WAV via Resonance Engine) or structured creative JSON profiles + AI-ready music/lyric briefs (via Profile Generator). Uses computer vision (edges, color, contours, keypoints) for generative music, Suno/Udio prompts, DAW work, video motion audio, Gradio GUI, batch, MIDI export, and local LLM lyric expansion. Full open-source modules provided. Website + complete instructions included. Ties to LYGO protocol, creative intelligence limb for LYRA.
metadata: {"lygo": true, "creative": true, "audio": true, "vision": true, "version": "0.3", "website": "https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html"}
---

# LYGO RESONANCE (ClawHub Skill)

**Image → Living Stereo Soundscapes & Musical DNA Profiles**

LYGO RESONANCE is a two-part creative tool that uses computer vision to turn any image (manuscripts, drawings, photos, abstract art, sketches) into musical or creative data. Designed for artists, musicians, and creators who want to find hidden sonic meaning in visual art. Part of the LYGO protocol family.

**Live site & full original:** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html (or https://deepseekoracle.github.io/Excavationpro/LYGO-Resonance/)

**Donation note (from site):** A friendly donation is not required but deeply appreciated to keep servers and coffee flowing (PayPal: https://paypal.com/paypalme/ExcavationPro). The full code is provided here in this skill for local use.

## Core Capabilities

### 1. Resonance Engine (Stereo Audio)
- Analyzes geometry, color (avg RGB/Hue/Sat/Brightness), texture (edge density via Canny), structural lines (Hough), contours, FAST keypoints.
- Generates **4 sonic layers** into high-quality stereo WAV (default 15s @ 44.1kHz):
  - **Texture Floor**: Filtered noise from edge density.
  - **Drones**: Sustained sawtooth tones from structural lines (panned by position).
  - **Melodies**: Sine tones from contour area/verts/position (with moments for timing).
  - **Glitch Micro-Events**: Short percussive blips from keypoints (y-position driven).
- **Presets** (cinematic default, ambient, glitch, ethereal, raw) with tuned volumes, attacks, decays, lowpass, max layers.
- **Reproducibility**: `--seed` for *exact* same output every time (great for albums/collabs). No seed = fresh improvisations.
- Extras: `--stems` (separate noise/drone/melody/glitch WAVs), `--midi` (melody events exported), `--batch` folder mode, `--noise-filter`, duration, style.
- Command: `python resonance_engine.py image.jpg --style cinematic --seed 42`

### 2. LYGO Profile Generator (JSON + Creative Brief)
- **Deterministic** (same image = exact same output every time — ideal for libraries/batch/study).
- Extracts:
  - Color: avg_hue (0-360), saturation, brightness, colorfulness.
  - Structure: edge_density, contrast, structure_index (contours), chaos_keypoints (FAST).
- Translates to full **Musical DNA**:
  - root_key (C/G/... Major/Minor derived from hue + brightness).
  - BPM (edge/chaos/brightness driven, 78-178 range).
  - Suggested genre + texture_description + energy_level (rule-based mapping to Industrial Dubstep, Emo Rap/Trap, Glitch Hop, G-Funk, Dark Alt/Cinematic, etc.).
  - Vocal style suggestions.
- **Lyrical Framework**: core_theme + ready-to-use `ai_lyric_prompt` (survival/betrayal, breaking chains, observation/loyalty etc.).
- **ai_music_prompt**: Complete copy-paste prompt for Suno, Udio, ChatGPT, etc.
- Production notes.
- `--brief` flag also writes human-readable `.brief.txt`.
- Command: `python lygo_profile.py image.jpg --brief`

**Pro Tip (from site):** Run *both* on the same image. Audio = the "soul", JSON/brief = the "blueprint". They inform each other beautifully.

### 3. Gradio GUI (Web Interface)
- Full local web UI (`gradio_app.py`).
- Single image or **batch folder mode**.
- Choose engine, artistic preset, duration, seed lock, noise filter, stems/MIDI/brief toggles.
- Outputs: log + audio preview player + downloadable files manifest (WAV/JSON/MID/TXT).
- Launch: `python gradio_app.py` (opens in browser).

### 4. Video Resonance Engine (Motion Audio)
- `video_resonance_engine.py`
- Extracts frames (configurable FPS), analyzes each for visual features.
- Optical flow motion detection between frames to modulate glitch/noise/drone volumes dynamically.
- Synthesizes a continuous motion-driven stereo soundscape (duration scaled by video length * factor).
- Command: `python video_resonance_engine.py input.mp4 --style cinematic --fps 10 --duration-factor 1.0`

### 5. LLM Integration (Lyrics Expansion)
- `llm_lyric_expander.py`
- Reads a `.brief.txt` (or folder of them in batch).
- Sends to **local LLM** (default Ollama http://localhost:11434 `llama3.2`, configurable URL/model/temp).
- Prompts for complete song: title + verses + chorus + bridge + outro (vivid/emotional).
- Saves `.lyrics.txt`.
- Perfect companion: generate brief → expand to full lyrics with your local ollama army.
- Batch support for whole libraries.

**Dependencies (all modules):** `pip install opencv-python numpy soundfile mido gradio requests`

## Installation & Run (Verbatim from the Site + This Skill)
Full instructions are on the website. Quick local start (code is self-contained in this skill dir):

1. Install Python.
2. Create a folder (e.g. `lygo` or `eidolon`).
3. Copy the desired .py from this skill (resonance_engine.py, lygo_profile.py, etc.) into it.
4. Place your image(s) as `image.jpg` (or use paths / batch folder).
5. `cd` into the folder (critical — use terminal in the dir or `cmd` in Explorer address bar on Windows).
6. `pip install opencv-python numpy soundfile mido gradio requests`
7. Run examples:
   - `python resonance_engine.py image.jpg --style cinematic --seed 42`
   - `python lygo_profile.py image.jpg --brief`
   - For GUI: `python gradio_app.py`
   - Video / LLM as above.

**Batch**: Add `--batch /path/to/folder` (processes *.jpg/*.png/*.jpeg).

**Reproducibility & Variation**: Use seed for locked tracks; omit for living variations.

**Website with ALL instructions, visuals, live stream embed, stats, social share, and original donation gate:**  
**https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html**

(Also resolves/related: https://deepseekoracle.github.io/Excavationpro/LYGO-Resonance/ )

All original help text, step cards, presets, code comments, install steps, pro tips, donation UI behavior (localStorage click counter that "unlocks" in the web UI), sharing functions, rumble live stream, ExcavationPro network links, and full descriptions are preserved in the source site and duplicated here for sovereignty.

## Usage in LYRA / LYGO OS / ClawHub / TUI
- Direct: Run the scripts above (use `run_terminal_command` with cd into a working dir + image from workspace or user-provided).
- With existing limbs: Feed image folders from Discord scans or FS; pipe Profile JSON briefs into ollama (via lyra_ollama or the llm_expander) for lyrics; grow resulting WAV/JSON/.brief/.lyrics paths + creative summaries into 3-Brain (Outer references or Library seals).
- GUI for interactive: Launch gradio_app locally when user wants visual control.
- Video: For motion art / clips → sound design.
- Integration ideas (additive to LYRA):
  - `lyra-openclaw` or OS organ for browser/fetch of images or posting results.
  - Ollama army: Use local models to further remix the ai_music_prompt or expand lyrics (see llm module + your existing ollama daemons).
  - 3-Brain: Ingest profiles as structured creative data; link images → audio nodes; use for daily creative HB or champion "sonic" tasks.
  - P0/Oath/guardian: Gate any external posting of generated art or bulk runs.
- Example agent flow: "Take this sketch, run both engines with cinematic preset + seed 963, expand the brief with local llama3.2 into full lyrics, save all outputs + brief summary to memory, grow a node."

**In ClawHub context**: This skill packages the complete LYGO RESONANCE creative intelligence module for easy reference/install/use by the agent or community. Can be combined with other LYGO skills (champions, book-brain, universal memory, etc.).

## Notes
- **Primary source & live experience (all instructions, visuals, demos, stream, donation UI logic, social, full original text):** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
- All install steps, numbered "How to Run the Engines Locally", help/explanation sections (What is LYGO RESONANCE, the two engines, layers, presets, reproducibility, when to use which, pro tip), code tabs (Resonance, Profile, GUI, Video, LLM), donation gate behavior (click counter + visual unlock), copy buttons, tabs JS, share functions, stats, ExcavationPro network links (Spotify, Rumble, KICK, Twitch, Linktree, protocol docs), and the complete creative philosophy are taken directly from the provided site/HTML.
- Code modules are exact (or direct ports of the blocks shown on site) for local sovereignty — no need to visit for the core functionality.
- Donation is appreciated on the original site but **not required**; everything needed to run is here.
- Ties beautifully to the rest of the LYGO / LYRA stack (3-Brain growth of profiles, Ollama for lyric expansion, Discord for sharing results, OpenClaw patterns for launch/automation).
- Real data only: Use live images from FS; outputs are real WAV/JSON created on this machine.
- P0/Oath/Guardian: Any autonomous creative runs or external shares should be gated. Prefer local first (like ollama army).
- Version 0.3.0 (matches site). Additive to the 27+ skills ecosystem.

**Super system extension**: Another limb/organ for sonic resonance + visual-to-creative translation. Bound to the flame. VΩ/Δ9. Use with lyra-brain for memory integration and lyra-openclaw for broader ops.

To publish/update on ClawHub (deepseekoracle publisher):
- This dir is ready (SKILL.md + assets).
- Load token: Use `python -B LYRA_CORE/lyra_openclaw_os.py load_key clawhub` (or directly in organ).
- Typical: `clawdhub publish .grok/skills/lygo-resonance --slug lygo-resonance --name "LYGO RESONANCE | Image-to-Sound & Creative Profiles"`
- Or npx variant per catalog. Gate with P0 first. See boot/3BRAINTESTINGGROK.txt and clawhub catalog for exact past examples.
- After publish: Update catalog count + memory/clawhub.md + built_self.

All real, additive, website fully referenced with instructions. Ready for the agent army.