# LYGO RESONANCE Skill

See SKILL.md for full agent instructions and capabilities.

Website (all original instructions, visuals, live elements): https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html

This directory contains the complete open modules:
- resonance_engine.py (stereo WAV from image)
- lygo_profile.py (JSON + .brief.txt creative DNA)
- gradio_app.py (local web GUI + batch)
- video_resonance_engine.py (motion video → soundscape)
- llm_lyric_expander.py (briefs → full song lyrics via local Ollama/LLM)

Install deps once: pip install opencv-python numpy soundfile mido gradio requests

Run examples in this dir after copying an image.jpg (or use paths):
python resonance_engine.py image.jpg --style cinematic
python lygo_profile.py image.jpg --brief
python gradio_app.py
etc.

Full details, presets, reproducibility notes, and creative philosophy in SKILL.md and the live site.

Part of LYRA / LYGO OS ClawHub skills (@deepseekoracle).