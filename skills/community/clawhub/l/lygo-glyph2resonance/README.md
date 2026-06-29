# LYGO Glyph2Resonance

Sonifies visual math glyphs, sacred geometry, seals, and mathematical patterns into rich resonant audio soundscapes.

**Core job:** Analyze a glyph image → extract geometry, symmetry, phi proportions, radial structure, vertex density, contrast → map to LYGO RESONANCE audio parameters → produce a real stereo WAV + structured .glyph.resonance.json profile.

Completely compatible with the published LYGO RESONANCE engine (lygo-resonance skill) and the LYGO Ollama Army (lygo-ollama-army).

## Quick Start
```bash
pip install opencv-python numpy soundfile

# Generate a test sacred geometry glyph
python glyph2resonance.py --generate-mandala --points 7 --rotations 5

# Sonify it
python glyph2resonance.py generated_glyph_mandala.png --preset glyph-sacred --seed 963 --duration 22
```

See SKILL.md for full instructions, integration with the army/champions/3-Brain, batch usage, and how it extends the LYGO RESONANCE pipeline.

**Website & base engine:** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
**Donation:** https://paypal.com/paypalme/ExcavationPro

Part of the LYGO creative intelligence stack under @deepseekoracle on ClawHub.