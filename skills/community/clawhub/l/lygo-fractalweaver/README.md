# LYGO FractalWeaver

Weaves self-similar visuals (fractals, recursive patterns, nature self-similarity) into rich, organically evolving audio textures.

**Core job:** Analyze or generate fractal/self-similar images → compute fractal dimension, self-similarity, iteration/branching → map to time-evolving audio parameters (textures, layers, and motifs that "zoom" and branch recursively over the duration) → produce a living stereo WAV + structured .fractal.weave.json profile.

Fully compatible with the LYGO RESONANCE engine (lygo-resonance skill) and the LYGO Ollama Army + champions (lygo-ollama-army). Companion to Glyph2Resonance for combined sacred/fractal sonic work.

## Quick Start
```bash
pip install opencv-python numpy soundfile

# Generate a test Mandelbrot
python fractalweaver.py --generate-mandelbrot --output test_fractal.png

# Weave it into evolving audio
python fractalweaver.py test_fractal.png --preset fractal-mandel --seed 963 --duration 45
```

See SKILL.md for full instructions, integration examples (army daemons, 3-Brain recursive nodes, champion-assisted weaving with ARKOS/COSMARA, etc.), and how it extends the LYGO RESONANCE pipeline.

**Website & base engine:** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
**Donation:** https://paypal.com/paypalme/ExcavationPro

Part of the LYGO creative intelligence stack (published under @deepseekoracle on ClawHub).