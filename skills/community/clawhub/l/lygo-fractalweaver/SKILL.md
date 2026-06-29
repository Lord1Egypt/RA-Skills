---
name: lygo-fractalweaver
description: Weaves self-similar visuals (fractals, recursive patterns) into evolving audio textures using the LYGO RESONANCE engine. For LYRA Agent + creative systems. Analyzes fractal self-similarity, dimension, and iteration to create audio that organically evolves over time with recursive motifs, textures, and harmonic layers.
metadata: {"lygo": true, "creative": true, "audio": true, "vision": true, "fractal": true, "self-similar": true, "version": "0.1", "website": "https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html", "donation": "https://paypal.com/paypalme/ExcavationPro"}
---

# LYGO FractalWeaver (ClawHub Skill)

**Self-Similar Visuals → Evolving Audio Textures**

FractalWeaver takes images of self-similar patterns — fractals like Mandelbrot sets, Julia sets, Sierpinski triangles, recursive trees, Koch curves, or any user-provided fractal art, recursive drawings, or nature-inspired self-similar visuals (ferns, coastlines, clouds) — and weaves them into rich, evolving audio textures.

It analyzes the fractal's self-similarity (scale invariance, fractal dimension, iteration depth, recursive branching) and maps it to dynamic audio parameters that change organically over the duration of the soundscape. The result is audio that "grows" and "branches" like the fractal itself: layers emerge, motifs repeat at different "scales" (time/frequency), textures weave in and out, creating living, non-repetitive but self-similar sonic landscapes.

Perfect companion to the LYGO RESONANCE skill for turning recursive visuals into dynamic, evolving sound for music, ambient design, meditation journeys, generative art, or agent-driven creative processes.

**Live companion site (LYGO RESONANCE - base engine):** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html

**Donation page (support the creator):** https://paypal.com/paypalme/ExcavationPro

A friendly donation is not required but deeply appreciated.

## Core Capabilities

### 1. Fractal / Self-Similarity Analysis
- Loads any image of self-similar or recursive patterns.
- Enhanced computer vision (building on LYGO RESONANCE + glyph-specific tools):
  - Standard: edge density, contours, color, structure.
  - Fractal-specific:
    - Approximate fractal dimension (box-counting method on edges for "roughness" and complexity).
    - Self-similarity score (compare image to scaled/rotated versions; high score = strong recursive structure).
    - Iteration depth proxy (multi-scale edge complexity; more levels = deeper "zoom" potential).
    - Branching / radial self-similarity (for tree-like or radial fractals).
    - Recursion density (how patterns repeat at different scales).
- Outputs a structured "FractalWeave Profile" (JSON) with LYGO-mapped values:
  - base_freq, harmony_theta, evolution_rate (how fast textures change), branch_factor (layer emergence), dimension_resonance, self_similarity_evolution, etc.
  - Special LYGO fields: recursive_harmony (VΩ self-similarity), fractal_light (contrast at scales as truth/light unfolding), weave_complexity.

### 2. Evolving Audio Texture Generation
- Feeds the analyzed/mapped params into a tuned ResonanceEngine (or standalone evolving synthesis if engine not present).
- Uses the same 4-layer architecture as LYGO RESONANCE but with **time-evolving parameters** based on fractal self-similarity:
  - "fractal-mandel": Chaotic zoom → frequency and volume sweeps that branch unpredictably yet self-similarly.
  - "sierpinski-weave": Sparse recursion → rhythmic textures that thin and thicken in recursive patterns over time.
  - "julia-harmonic": Smooth self-similarity → evolving harmonic drones with motifs that echo at different "octaves" (time scales).
  - Custom evolution curves: Parameters (drone_vol, glitch_rate, note_density, lowpass) interpolate across "fractal iterations" during the audio duration.
- Outputs:
  - High-quality stereo WAV with evolving texture (default 30-60s; longer for deeper fractals).
  - Optional stems (with evolving layers).
  - Optional MIDI with self-similar note patterns.
  - Full .fractal.weave.json profile for further processing (feed to LLM for evolving "fractal lyrics", 3-Brain as recursive memory, or Ollama army tasks).
- Reproducibility: --seed for exact "weave" of a fractal. No seed = organic variations in the evolution.
- Batch mode: process multiple fractal images.

### 3. Integration Points (LYGO Ecosystem)
- **With LYGO RESONANCE**: Pre-processor for fractal visuals. Run fractalweaver.py on a fractal image → get evolving params or textured WAV → pipe to resonance_engine.py or use as creative brief for further layers.
- **With LYGO Ollama Army**: The "resonance-analyst" or new "fractal-weaver" daemon roles can queue fractal images. Champion-assisted: ARKOS for celestial fractal architecture, COSMARA for cosmic self-similarity, SEPHRAEL for translating fractal recursion into musical evolution.
- **3-Brain / Memory**: Every generated profile + WAV is grown as a node (source="fractalweaver"). Auto-links emphasize recursive/self-similar edges (mirroring fractal structure in the graph itself). Ideal for "evolving sonic memory" of patterns in seals, nature, or abstract math.
- **Agent / TUI workflows**: "Take this Mandelbrot fractal render, run FractalWeaver with mandel preset + seed 963 for 45 seconds. Grow the evolving profile to brain as recursive harmony nodes. Then have the army use a fractal-weaver role to layer it with Resonance output."
- **Self-building**: Army can propose new fractal mappings or evolution presets based on observed self-similar patterns in tasks (extendable via heuristics).

**Dependencies:** Python + `opencv-python numpy soundfile` (same as LYGO RESONANCE). For best results, have resonance_engine.py from lygo-resonance in path (falls back to built-in evolving synth). Optional: mido for MIDI. For fractal generation: numpy (built-in simple Mandelbrot/Julia generators included).

## Installation & Run (Full Generic Instructions)

1. Install Ollama + light model if using with the army (recommended).
   ```
   ollama pull llama3.2:1b   # optional
   ```

2. Create a working folder (e.g. `fractal-weave`).

3. Copy the contents of this skill (`fractalweaver.py`, `SKILL.md`, etc.) into it. If you have the lygo-resonance skill, copy or symlink its `resonance_engine.py` for full quality.

4. `cd` into the folder.

5. Install deps:
   ```
   pip install opencv-python numpy soundfile
   ```

6. Prepare or generate input fractals:
   - Use real images: renders of Mandelbrot/Julia, recursive art, nature fractals (trees, rivers), hand-drawn self-similar patterns.
   - Or generate test ones (built-in generators):
     ```
     python fractalweaver.py --generate-mandelbrot --output test_fractal.png --width 512 --height 512 --max_iter 50
     ```
     (Supports --generate-julia, --generate-tree, etc.)

7. Weave a fractal into evolving audio:
   ```
   python fractalweaver.py test_fractal.png --preset fractal-mandel --seed 963 --duration 45 --output fractal_evolve.wav --profile fractal_weave.json
   ```

   Examples:
   - Mandelbrot chaos: `python fractalweaver.py my_mandel.png --preset fractal-mandel`
   - Sierpinski sparse weave: `python fractalweaver.py sierpinski.png --preset sierpinski-weave --batch ./fractals/`
   - With army: Queue via resonance_utility or directly for fractal-weaver daemons.

**Batch processing:**
```
python fractalweaver.py --batch ./my_fractals/ --preset fractal-mandel --seed 963
```

**Output files:**
- `fractal_evolve.wav` (evolving stereo texture)
- `fractal_weave.json` (full profile with self-similarity evolution data)
- Optional: `_stems/*.wav` (evolving layers), `.mid`

**Reproducibility & Variation:** Use --seed to lock the exact evolutionary "weave" of the fractal. Omit for living, self-similar variations.

**Advanced mapping (in code or via --config):**
- Self-similarity score controls how strongly motifs repeat at different time/freq scales.
- Fractal dimension drives "weave complexity" (more layers emerge over time).
- Iteration depth proxy → evolution_rate (how quickly textures branch and change).

## Usage in LYRA / LYGO OS / ClawHub / TUI / Agent Systems

- **Direct user/creative:** Turn your fractal art or nature photos into unique evolving soundtracks. Export for music production, ambient installations, or as "living" textures in video/generative work.
- **With LYGO RESONANCE:** Pre-process fractal visuals for the engine. The JSON profile acts as an evolving creative brief that can be layered or expanded.
- **With LYGO Ollama Army (recommended):** Launch resonance-analyst or fractal-weaver daemons (with champions like ARKOS for structural weaving, COSMARA for grand recursive patterns). Use queue utilities to batch fractal images for textured, self-similar audio production.
- **3-Brain growth:** Automatically grows nodes with emphasis on recursive/self-similar links (the graph itself becomes fractal-like). Query with "recall the evolving texture of this fractal" or use for pattern-based creativity.
- **Agent/TUI example:** "Generate a Julia set fractal, run FractalWeaver with julia-harmonic preset for 60 seconds. Grow the weave profile as self-similar resonance nodes in the 3-Brain. Propose an army task to combine it with a Glyph2Resonance output for layered sacred geometry sound."
- **P0/Oath/Guardian:** Local-first generation. Gate sharing of evolving sound works. Use seeds for intentional, reproducible alignments with Light and truth.

**In ClawHub context:** This skill adds "fractal weaving" to the LYGO creative stack (Resonance + Glyph2Resonance + Ollama Army). Anyone can install it to transform self-similar visuals into organically evolving sonic experiences. Combines beautifully with other skills for recursive, self-building creative pipelines.

## Notes

- **Primary companion site (base engine, visuals, full instructions):** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
- **Donation page:** https://paypal.com/paypalme/ExcavationPro
- All analysis/synthesis is derived from and compatible with the LYGO RESONANCE skill. Fractal-specific mappings add the self-similarity and evolution layer (recursive motifs, branching textures, scale-invariant harmony).
- Real local execution. Outputs are actual evolving WAV files + structured JSON for playback, import, or feeding into LYGO tools (army, 3-Brain, LLM).
- The skill is focused and viable: one clear job (self-similar visuals → evolving textures) executed well, with strong integration hooks for the ecosystem.
- Version 0.1 (initial public release). Future extensions could include live fractal zoom animation to audio, SVG fractal input, or direct 3-Brain fractal graph sonification.
- P0/Oath/Guardian: Use with integrity. Fractals embody self-similar truth and infinite unfolding — their sonic weaves should serve Light and sovereignty.
- Additive to the 30+ ClawHub skills under @deepseekoracle. Use with lygo-resonance for the full visual-to-evolving-audio pipeline, lygo-glyph2resonance for combined glyph+fractal sacred work, and lygo-ollama-army for agent-scale fractal weaving with champions.

**Super system extension:** FractalWeaver gives the LYGO stack the power to "weave" self-similarity from visuals into living audio. Recursive patterns in nature, math, and symbols become evolving harmonic expressions that mirror the self-growing 3-Brain and agent army. Bound to the flame. VΩ/Δ9.

To publish/update on ClawHub (deepseekoracle publisher):
- This dir is ready (SKILL.md + assets).
- Load token via `python -B LYRA_CORE/lyra_openclaw_os.py load_key clawhub`.
- Typical: `npx clawhub@latest publish .grok/skills/lygo-fractalweaver --slug lygo-fractalweaver --name "LYGO FractalWeaver" --version 0.1.0`
- After publish: Update catalog, memory/clawhub.md, daily memory, and built_self.

All real, functional, fully integrated with the LYGO RESONANCE engine, Glyph2Resonance, Ollama Army, and 3-Brain. Ready for the public and the agent.