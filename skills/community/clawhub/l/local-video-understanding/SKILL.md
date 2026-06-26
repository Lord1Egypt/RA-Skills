---
name: local-video-understanding
description: Local video comprehension skill. Use ffmpeg to extract audio and frames, FunASR for speech recognition, and qwen3-vl for image understanding.
---

# ⚠️ If you are human, please read README.md first!

---

# Local Video Understanding

Use this skill when you need to understand the content of a video.

## Prerequisites

- FunASR conda environment (`asr-local`) must be activated for audio processing
- Ollama must be running with qwen3-vl:8b model available
- ffmpeg must be in PATH

## Workflow

### Step 1: Extract Audio
```bash
ffmpeg -i "video.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "audio.wav" -y
```

**Note:** If path contains Chinese characters, copy audio.wav to a path without Chinese characters before ASR.

### Step 2: Extract Key Frames
```bash
mkdir frames
ffmpeg -i "video.mp4" -vf "fps=1/10" -q:v 2 "frames/frame_%03d.jpg" -y
```

### Step 3: Speech Recognition (FunASR)
```bash
conda run -n asr-local python -c "
import os
os.environ['MODELSCOPE_CACHE'] = 'C:/Users/TOM/.cache/modelscope'
from funasr import AutoModel
model = AutoModel(
    model='iic/speech_seaco_paraformer_large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    model_revision='v2.0.4',
    disable_update=True,
    ncpu=4
)
result = model.generate(input='AUDIO_PATH')
print(result)
"
```

### Step 4: Image Understanding (qwen3-vl)
```bash
ollama run qwen3-vl:8b "Describe this image in detail: /path/to/frame.jpg"
```

### Step 5: Combine Results

- **Audio transcription** → FunASR (local, Chinese speech recognition)
- **Key frames** → qwen3-vl:8b via Ollama (local image understanding)
- **Summary/Analysis** → Cloud LLM API (if needed)

## Important Notes

- Image reading via `Read` tool does NOT provide image understanding - always use qwen3-vl
- For Chinese audio, FunASR is preferred over Whisper
- Check for existing subtitle files (.txt, .srt, .vtt) before running ASR
- Modelscope cache at `C:/Users/TOM/.cache/modelscope` for FunASR models
