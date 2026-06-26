# Meeting Summary Skill — Setup Guide

Complete installation guide. Follow these steps from top to bottom on a fresh machine.

## Prerequisites

- **Python 3.9+**
- **ffmpeg** (audio preprocessing)
- **macOS / Linux** (tested on macOS ARM64, should work on Linux x86_64)

---

## Step 1: Install System Dependencies

### ffmpeg

```bash
# macOS
brew install ffmpeg

# Or download static binary from https://evermeet.cx/ffmpeg/ (macOS)
# Linux (Ubuntu/Debian)
sudo apt install ffmpeg
```

Verify: `ffmpeg -version`

---

## Step 2: Python Dependencies (Main Scripts)

These are needed for the core pipeline (`meeting-summarize.py`, `voiceprint-manager.py`):

```bash
pip3 install numpy scipy soundfile onnxruntime
```

| Package | Purpose | Version Tested |
|---------|---------|----------------|
| `numpy` | Array operations, audio processing | 2.0.2 |
| `scipy` | Cosine similarity for voiceprint matching | 1.13.1 |
| `soundfile` | Audio file I/O (requires libsndfile) | 0.13.1 |
| `onnxruntime` | Speaker embedding model inference | 1.19.2 |

### libsndfile (if soundfile fails)

```bash
# macOS
brew install libsndfile

# Linux
sudo apt install libsndfile1
```

---

## Step 3: StepFun API Key (Required)

The skill uses StepFun's ASR and LLM models:

- **ASR 转写**：`step-asr` 模型（文件上传接口）
- **LLM**：`step-3.5-flash` 模型（说话人数估计 + 纪要生成）

### Get Your API Key

1. Go to **https://platform.stepfun.com/interface-key**
2. Sign up / Log in
3. Navigate to **API Keys** → **Create New Key**
4. Copy the key

### Save the Key

```bash
echo "your-api-key-here" > ~/.stepfun_api_key
chmod 600 ~/.stepfun_api_key
```

The scripts look for the key in this order:
1. `~/.stepfun_api_key`
2. `~/.step_api_key`
3. Environment variable `STEPFUN_API_KEY`

### What It's Used For

- **Step ASR** (`step-asr`): 通过文件上传接口做语音转文字
- **Step LLM** (`step-3.5-flash`): 估计说话人数、生成结构化会议纪要

---

## Step 4: Speaker Embedding Model (For Voiceprint Matching)

Download the wespeaker ResNet34 ONNX model (~25MB):

```bash
mkdir -p ~/.openclaw/workspace/models/speaker-embedding

# Download from wespeaker releases
curl -L "https://github.com/wenet-e2e/wespeaker/releases/download/v2.1/voxceleb_resnet34.onnx" \
  -o ~/.openclaw/workspace/models/speaker-embedding/speaker_model.onnx
```

If the URL changes, search the [wespeaker GitHub releases](https://github.com/wenet-e2e/wespeaker/releases) for the latest ONNX model.

**Model specs**: ResNet34, 256-dim embeddings, ~25MB, runs on CPU via onnxruntime.

---

## Step 5: pyannote Speaker Diarization (Optional but Recommended)

pyannote provides much better speaker turn detection than the lightweight fallback. It requires a **separate Python virtual environment** because it pulls in PyTorch (~2GB).

### 5a: Accept the Model License

1. Go to **https://huggingface.co/pyannote/speaker-diarization-community-1**
2. **Log in** to your Hugging Face account
3. **Accept the usage agreement** (required to download the model)

### 5b: Create a Dedicated Virtual Environment

```bash
python3 -m venv ~/.venv-pyannote
source ~/.venv-pyannote/bin/activate

pip install pyannote.audio huggingface_hub soundfile torch
```

### 5c: Download the Model Locally

```bash
# Still in the venv
python3 -c "
from huggingface_hub import snapshot_download
snapshot_download('pyannote/speaker-diarization-community-1',
                  local_dir='$HOME/.openclaw/workspace/models/pyannote-community-1')
"
```

Or using git:
```bash
git lfs install
git clone https://huggingface.co/pyannote/speaker-diarization-community-1 \
  ~/.openclaw/workspace/models/pyannote-community-1
```

### 5d: Set the Environment Variable

Tell the meeting-summary script where to find the pyannote Python:

```bash
export MEETING_SUMMARY_PYANNOTE_PYTHON="$HOME/.venv-pyannote/bin/python"
```

Add this to your `~/.zshrc` or `~/.bashrc` to persist.

### 5e: Test pyannote

```bash
~/.venv-pyannote/bin/python scripts/pyannote-diarize.py \
  --audio /path/to/short-test.wav \
  --num-speakers 2
```

Expected output: JSON with `segments` array containing `start_time`, `end_time`, `speaker_hint`.

**⚠️ Performance Note**: pyannote on CPU is slow (~1x realtime for short audio, slower for long recordings). The skill mitigates this with chunked selective diarization and caching. GPU/MPS acceleration is supported by PyTorch but not required.

---

## Step 6: Verify Installation

```bash
# Test ASR
python3 scripts/transcribe.py --audio /path/to/short-audio.wav

# Test voiceprint
python3 scripts/voiceprint-manager.py list

# Test full pipeline (short audio)
python3 scripts/meeting-summarize.py \
  --audio /path/to/short-meeting.wav \
  --out /tmp/test-summary.json \
  --minutes-out /tmp/test-summary.md
```

---

## Environment Variables Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| `MEETING_SUMMARY_PYANNOTE_PYTHON` | (none) | Path to pyannote venv python binary |
| `MEETING_SUMMARY_LLM_URL` | `https://api.stepfun.com/v1/chat/completions` | LLM API endpoint |
| `MEETING_SUMMARY_LLM_MODEL` | `step-3.5-flash` | LLM model for speaker estimation & summary |
| `STEPFUN_API_KEY` | (reads from `~/.stepfun_api_key`) | StepFun API key |
| `PYANNOTE_PIPELINE_PATH` | `~/.openclaw/workspace/models/pyannote-community-1` | Local pyannote model path |
| `HF_TOKEN` | (none) | Hugging Face token (alternative to local model) |

---

## Directory Structure After Setup

```
~/.openclaw/workspace/
├── models/
│   ├── speaker-embedding/
│   │   └── speaker_model.onnx          # wespeaker ResNet34 (25MB)
│   └── pyannote-community-1/           # pyannote diarization model
│       ├── config.yaml
│       ├── embedding/
│       ├── segmentation/
│       └── plda/
├── memory/
│   └── voiceprints/                    # Enrolled speaker voiceprints
│       ├── Alice.json
│       └── Bob.json
├── cache/
│   └── meeting-summary/               # ASR + diarization cache
│       ├── <hash>--asr--zh.json
│       └── <hash>--chunk-diarization--*.json
└── skills/
    └── meeting-summary/
        ├── SKILL.md
        ├── scripts/
        │   ├── meeting-summarize.py
        │   ├── pyannote-diarize.py
        │   ├── voiceprint-manager.py
        │   └── transcribe.py
        └── references/
            └── setup-guide.md
```

---

## Troubleshooting

### "No StepFun API key found"
→ Create `~/.stepfun_api_key` with your key, or set `STEPFUN_API_KEY` env var.

### "Audio preprocessing failed"
→ Ensure ffmpeg is installed and in PATH: `which ffmpeg`

### "pyannote pipeline is not available locally"
→ Set `MEETING_SUMMARY_PYANNOTE_PYTHON` to your venv python path, and ensure the model is downloaded to `models/pyannote-community-1/`.

### pyannote runs too slow
→ Use `--max-new-chunks 2` to limit diarization to only the most important chunks. Use the cache — subsequent runs skip already-processed chunks.

### soundfile import error
→ Install libsndfile: `brew install libsndfile` (macOS) or `apt install libsndfile1` (Linux).

### ONNX model not found
→ Download to `models/speaker-embedding/speaker_model.onnx`. See Step 4 above.
