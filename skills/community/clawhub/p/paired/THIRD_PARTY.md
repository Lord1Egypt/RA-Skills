# Third-party software in paired v2.0.0

paired uses or depends on the following open-source projects. Every component listed here is downloaded by the user at build/install time — none of their source code is bundled with this skill.

## Voice synthesis engines

### VoxCPM2 — primary voice-cloning engine
* Project: https://github.com/OpenBMB/VoxCPM
* Paper: https://arxiv.org/abs/2509.24650
* Authors: Zhou, Zeng, Liu et al. (OpenBMB)
* License: Apache-2.0
* Used for: 48kHz studio-quality voice cloning, 30-language multilingual synthesis
* Cited in source: `skill/voice/paired-voice-synth.py`, `skill/engines/voxcpm-server.py`

### coqui-tts (XTTS v2) — fallback voice-cloning engine
* Project: https://github.com/idiap/coqui-ai-TTS (active fork after Coqui shutdown)
* License: Apache-2.0
* Used for: 24kHz voice cloning when VoxCPM2 unavailable
* Cited in source: `skill/engines/xtts.Dockerfile`

### piper — generic neural TTS fallback
* Project: https://github.com/rhasspy/piper
* License: MIT
* Used for: voice synthesis when no cloning engine is available
* Cited in source: `skill/voice/paired-voice-synth.py` (fallback_piper)

### espeak-ng — last-resort TTS
* Project: https://github.com/espeak-ng/espeak-ng
* License: GPL-3.0
* Used for: final fallback when all neural engines fail
* Cited in source: `skill/voice/paired-voice-synth.py` (fallback_espeak)

## Audio infrastructure

### ffmpeg
* Project: https://ffmpeg.org/
* License: LGPL-2.1+ (or GPL-2.1+ depending on build options)
* Used for: audio resampling, concatenation, format conversion, silence trimming
* Cited in source: throughout `skill/voice/` and `skill/setup/`

### alsa-utils (arecord)
* Project: https://alsa-project.org/
* License: GPL-2.0
* Used for: capturing user microphone input during setup
* Cited in source: `skill/setup/paired-voice-setup.py`

## Phone control

### BlueZ
* Project: http://www.bluez.org/
* License: LGPL-2.1+
* Used for: Bluetooth pairing, HFP/A2DP profiles, OBEX file transfer
* Cited in source: `skill/bin/bt-*.py` throughout

### Android Debug Bridge (adb)
* Project: https://developer.android.com/tools/adb
* License: Apache-2.0
* Used for: ADB-over-Wi-Fi phone control, SMS sending, notification reading
* Cited in source: `skill/bin/bt-adb-*.py`

## Python libraries

### FastAPI + uvicorn
* https://github.com/tiangolo/fastapi (MIT)
* https://github.com/encode/uvicorn (BSD-3-Clause)
* Used for: HTTP server inside the voice-cloning Docker containers

### PyTorch + CUDA
* https://github.com/pytorch/pytorch (BSD-style)
* Used as the deep-learning runtime for VoxCPM2 and XTTS

### soundfile, numpy
* https://github.com/bastibe/python-soundfile (BSD-3-Clause)
* https://github.com/numpy/numpy (BSD-3-Clause)
* Used for: audio I/O and array math

## Models (downloaded at runtime, not bundled)

### openbmb/VoxCPM2
* HuggingFace: https://huggingface.co/openbmb/VoxCPM2
* License: Apache-2.0
* Size: ~5GB
* Downloaded automatically on first container start

### tts_models/multilingual/multi-dataset/xtts_v2
* HuggingFace: https://huggingface.co/coqui/XTTS-v2
* License: Coqui Public Model License (CPML) — non-commercial
* Downloaded automatically by coqui-tts on first use
* **Note:** If you intend commercial use, use VoxCPM2 only (paired falls back automatically)

## Agent framework

### OpenClaw
* Project: https://openclaw.ai
* The paired skill is published to ClawHub and runs inside OpenClaw agents.

