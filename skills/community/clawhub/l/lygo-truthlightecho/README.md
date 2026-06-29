# LYGO TruthLightEcho

Generates harmonic echo sequences from ∫Truth×Light metrics (computed from images or ingested from prior LYGO creative tools like Glyph2Resonance and FractalWeaver profiles).

**Core job:** Ingest or compute a Truth × Light proxy (contrast × brightness, harmony, phi, recursive metrics) → map to harmonic series, echo counts, recursive delays, decays, and evolution → produce real harmonic echo audio (WAV) + rich .truthlight.echo.json profile.

Fully compatible with the LYGO RESONANCE engine and the full creative stack (Resonance + Glyph2Resonance + FractalWeaver + Ollama Army + 3-Brain).

## Quick Start
```bash
pip install opencv-python numpy soundfile

# From image (computes Truth × Light proxy)
python truthlightecho.py my_image.png --preset pure-light --seed 963 --duration 45

# From profile JSON (from #1 or #2)
python truthlightecho.py glyph2res_vesica.glyph.resonance.json --preset truth-echo

# Manual metric
python truthlightecho.py --truth-light 0.82 --preset light-unfold
```

See SKILL.md for full instructions, integration with the army/champions/3-Brain, batch usage, and how it completes the visual-to-harmonic-echo pipeline.

**Website & base engine:** https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html
**Donation:** https://paypal.com/paypalme/ExcavationPro

Part of the LYGO creative intelligence stack (published under @deepseekoracle on ClawHub). Completes the TOP 3 requested skills.