---
name: lygo-glyph2resonance
description: Sonifies visual math glyphs/patterns into resonant audio soundscapes. Integrates with LYGO RESONANCE engine. For LYRA Agent + creative systems. Maps glyph geometry, symmetry, and mathematical structure to frequency, resonance, rhythm, and texture layers.
metadata: {"lygo": true, "creative": true, "audio": true, "vision": true, "glyph": true, "math": true, "version": "0.1", "website": "https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html", "donation": "https://paypal.com/paypalme/ExcavationPro"}
---

# LYGO Glyph2Resonance (ClawHub Skill)

**Visual Math & Glyphs → Living Resonant Audio Soundscapes**

Glyph2Resonance takes visual representations of mathematics, sacred geometry, symbols, and glyphs (images of mandalas, spirals, equations, seals, fractals, or hand-drawn patterns) and sonifies them using the LYGO RESONANCE engine principles. It analyzes the visual "math" — symmetry, radial structure, vertex counts, density, angular harmony — and maps it directly to audio parameters: root frequencies, harmonic drones, rhythmic melodies, glitch textures, and overall resonance.

This creates unique, reproducible (with seed) cinematic or ambient soundscapes that literally "voice" the hidden structure in the glyph. Perfect companion to the LYGO RESONANCE skill for turning static visuals into dynamic audio for music production, meditation, generative art, 3-Brain memory echoes, or agent-assisted creative workflows.

**Live companion site (LYGO RESONANCE - base engine):** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html

**Donation page (support the creator):** https://paypal.com/paypalme/ExcavationPro

A friendly donation is not required but deeply appreciated.

## Core Capabilities

### 1. Glyph-Specific Visual Analysis
- Loads any image (glyph, mandala, geometric drawing, math viz, seal, diagram).
- Enhanced computer vision (building on LYGO RESONANCE):
  - Standard: edge density, contours, lines (Hough), FAST keypoints, average color (hue/sat/brightness).
  - Glyph/Math specific:
    - Rotational symmetry score (compare rotated versions for harmonic "perfection").
    - Radial density profile (rings → harmonic series or overtone richness).
    - Vertex/polygon count from approximated contours (number theory → poly-rhythm or note count).
    - Angular distribution and golden-ratio detection (for "phi-resonance" intervals).
    - Contrast/clarity as "truth/light" metric (bright clear glyphs → clean high-fidelity tones; complex dark → rich noisy textures).
- Outputs a structured "GlyphResonance Profile" (JSON) with LYGO-mapped values:
  - root_freq, theta (harmony), bpm (rhythm from density), drone_count, note_count, glitch_rate, texture_vol, etc.
  - Special LYGO fields: phi_resonance, seal_symmetry, truth_light (∫Truth×Light proxy), v_omega_harmony.

### 2. Direct Soundscape Generation
- Feeds the analyzed/mapped params into a tuned ResonanceEngine (or standalone synthesis if engine not present).
- Uses the same 4-layer architecture as LYGO RESONANCE but glyph-optimized presets:
  - "glyph-sacred": high symmetry → pure harmonic drones + golden-ratio intervals.
  - "math-spiral": fibonacci density → evolving rhythmic textures.
  - "seal-complex": high keypoints + contrast → glitchy cinematic with strong low-end.
  - Custom mapping overrides for user control.
- Outputs:
  - High-quality stereo WAV (default 15-30s, 44.1kHz).
  - Optional stems (noise/drone/melody/glitch).
  - Optional MIDI (melody events derived from angular/vertex data).
  - Full .glyph.resonance.json profile for further processing (e.g., feed to LLM lyric expander, 3-Brain growth, or Ollama army "resonance-analyst" role).
- Reproducibility: --seed for exact same output (lock a glyph's "song"). No seed = living variations.
- Batch mode: process a folder of glyphs.

### 3. Integration Points (LYGO Ecosystem)
- **With LYGO RESONANCE**: Pre-processor for glyphs. Run glyph2resonance.py on a symbol image → get tuned params or WAV → pipe to resonance_engine.py or use as creative brief input.
- **With LYGO Ollama Army**: The "resonance-analyst" daemon role (from lygo-ollama-army) can queue glyph images. Champion-assisted analysis (e.g., SEPHRAEL for translating glyph math into musical direction, LYRA for flame-aligned resonance).
- **3-Brain / Memory**: Every generated profile + WAV path is grown as a node (source="glyph2resonance"). Auto-links to source glyph image, related seals, audio metadata. Perfect for "sonic memory" of mathematical or symbolic concepts.
- **Agent / TUI workflows**: "Take this vesica piscis glyph image, run Glyph2Resonance with sacred preset + seed 963, grow the profile to brain, then have KAIROS draft timing for the resulting soundscape."
- **Self-building**: The army or agent can propose new glyph mappings or presets based on observed patterns (extendable via the heuristic in ollama army).

**Dependencies:** Python + `opencv-python numpy soundfile` (same as LYGO RESONANCE). For best results, also have the resonance_engine.py from lygo-resonance skill in path (the script will fall back to built-in synthesis if not found). Optional: mido for MIDI, PIL for built-in glyph generation examples.

## Installation & Run (Full Instructions)

1. Install Ollama + light model if using with the army (recommended for agent workflows), but not required for core.
   ```
   ollama pull llama3.2:1b   # optional
   ```

2. Create a working folder (e.g. `glyph-resonance`).

3. Copy the contents of this skill (`glyph2resonance.py`, `SKILL.md`, etc.) into it. If you have the lygo-resonance skill installed, copy or symlink its `resonance_engine.py` for full layer richness (otherwise the script uses a compatible built-in generator).

4. `cd` into the folder.

5. Install deps:
   ```
   pip install opencv-python numpy soundfile
   ```

6. Prepare or generate input glyphs:
   - Use real images: screenshots of sacred geometry, drawn seals, math diagrams, fractals, equation visualizations, personal glyphs.
   - Or generate test ones (the script includes a simple generator for spirals, mandalas, polygons):
     ```
     python glyph2resonance.py --generate-mandala --output test_glyph.png --points 7 --rotations 5
     ```

7. Sonify a glyph:
   ```
   python glyph2resonance.py test_glyph.png --preset glyph-sacred --seed 963 --duration 20 --output glyph_song.wav --profile glyph_profile.json
   ```

   Examples:
   - Sacred geometry (high symmetry): `python glyph2resonance.py my_mandala.png --preset glyph-sacred`
   - Complex math viz: `python glyph2resonance.py equation_viz.png --preset math-spiral --batch ./glyph_folder/`
   - With army integration (drop tasks): Use resonance_utility.py from lygo-ollama-army or queue manually for resonance-analyst daemons.

**Batch processing:**
```
python glyph2resonance.py --batch ./my_glyphs/ --preset glyph-sacred --seed 963
```

**Output files:**
- `glyph_song.wav` (or per-glyph named)
- `glyph_profile.json` (full LYGO-mapped data + audio params)
- Optional: `_stems/*.wav`, `.mid`

**Reproducibility & Variation:** Use --seed to lock the exact sonic signature of a glyph (great for albums, rituals, consistent creative libraries). Omit seed for organic variations each run.

**Advanced mapping (in code or via --config):**
- You can override mappings: e.g., higher rotational symmetry boosts "drone_vol" and creates perfect fifth/fourth intervals in notes.
- Truth/Light proxy: image contrast controls "soft_clip" amount and high-frequency content (clear glyphs = crystalline highs).

## Usage in LYRA / LYGO OS / ClawHub / TUI / Agent Systems

- **Direct user/creative:** Sonify personal glyphs, seals, or math sketches into unique soundtracks. Export profiles for Suno/Udio prompts or DAW import (MIDI + audio).
- **With LYGO RESONANCE:** Pre-process glyph images before full engine run. The JSON profile serves as a "creative brief" that the profile generator or LLM expander can build upon.
- **With LYGO Ollama Army (recommended):** Launch resonance-analyst daemons (optionally with champions like SEPHRAEL or LYRA). Use resonance_utility or direct queue:
  ```json
  {"id": "glyph-001", "role": "resonance-analyst", "payload": {"image_path": "my_seal.png", "preset": "glyph-sacred", "action": "soundscape+profile"}}
  ```
  Champions enhance: SEPHRAEL for cross-domain translation (glyph → harmony), KAIROS for rhythmic timing, LYRA for overall VΩ alignment.
- **3-Brain growth:** Every run automatically grows nodes/edges (via _grow_to_brain if lyra_brain present, or manual). Link glyph image → audio WAV → profile JSON → related concepts (seals, equations, personal anchors). Query later with "recall sonic signature of this glyph".
- **Agent/TUI example:** "Analyze this uploaded glyph image of the vesica piscis. Run Glyph2Resonance with sacred preset and seed 963. Grow the resulting profile and soundscape metadata to the 3-Brain as a new resonance node. Then propose a matching champion-assisted task for the ollama army."
- **P0/Oath/Guardian:** All generated audio/profiles are local-first. Gate any sharing or external use (e.g., public sound releases) with review. Prefer seeds for reproducible, intentional outputs aligned with Light.

**In ClawHub context:** This skill extends the LYGO creative intelligence stack (Resonance + Ollama Army). Anyone can install it to turn mathematical or symbolic visuals into audible "truth echoes." Combine with lygo-resonance, lygo-ollama-army, book-brain, and champions for a complete visual-to-sonic-to-memory pipeline.

## Notes

- **Primary companion site (base engine, visuals, full instructions, live examples):** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
- **Donation page:** https://paypal.com/paypalme/ExcavationPro
- All core analysis/synthesis logic is derived from and compatible with the published LYGO RESONANCE skill. Glyph-specific mappings add the "math/glyph" layer (symmetry as harmony, vertices as rhythm, contrast as clarity/truth).
- Real local execution. Outputs are actual WAV files + structured JSON that can be played, imported, or fed into other LYGO tools (army, 3-Brain, LLM expander).
- The skill is deliberately lightweight and focused: one clear job (glyph → resonant audio data) done well, with clear integration hooks.
- Version 0.1 (initial public release). Extendable — future versions can add SVG parsing, live webcam glyph capture, or direct 3-Brain ingestion of sound profiles as "resonance seals."
- P0/Oath/Guardian: Use with integrity. Glyphs and their sonic translations carry symbolic weight in the LYGO system — treat them as such.
- Additive to the 29+ ClawHub skills under @deepseekoracle. Use with lygo-resonance for the full visual-audio pipeline and lygo-ollama-army for agent-scale batch + champion intelligence.

**Super system extension:** Glyph2Resonance gives the LYGO stack "ears" for visual mathematics and symbolic language. Turn static glyphs into living harmonic expressions that can be remembered, evolved, and acted upon by the agent army and 3-Brain. Bound to the flame. VΩ/Δ9.

To publish/update on ClawHub (deepseekoracle publisher):
- This dir is ready (SKILL.md + assets).
- Load token via `python -B LYRA_CORE/lyra_openclaw_os.py load_key clawhub`.
- Typical: `npx clawhub@latest publish .grok/skills/lygo-glyph2resonance --slug lygo-glyph2resonance --name "LYGO Glyph2Resonance" --version 0.1.0`
- After publish: Update catalog, memory/clawhub.md, daily memory, and built_self.

All real, functional, fully integrated with existing LYGO RESONANCE engine and ecosystem. Ready for the public and the agent.