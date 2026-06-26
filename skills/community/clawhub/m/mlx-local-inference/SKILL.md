---
name: mlx-local-inference
description: >
  Use when calling local AI on this Mac — text generation, embeddings,
  speech-to-text, OCR, or image understanding. LLM/VLM via oMLX gateway at
  localhost:8000/v1. Embedding/ASR/OCR via Python libraries (mlx-lm, mlx-vlm, mlx-audio).
  Works offline. Use instead of cloud APIs for privacy or low latency.
metadata: { "openclaw": { "os": ["darwin"], "requires": { "anyBins": ["uv"] } } }
---

# MLX Local Inference Stack

Local AI inference on Apple Silicon. **oMLX** handles LLM/VLM with continuous batching.
Python libraries handle Embedding/ASR/OCR directly via `uv`.

## Architecture

```
┌─────────────────────────────────────┐
│  oMLX (localhost:8000/v1)           │
│  - LLM (Qwen3.5-35B, etc.)          │
│  - VLM (vision-language models)     │
│  - Continuous batching + SSD cache  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Python Libraries (via uv run)      │
│  - mlx-lm: Embedding                │
│  - mlx-vlm: OCR (PaddleOCR-VL)      │
│  - mlx-audio: ASR (Qwen3-ASR)       │
└─────────────────────────────────────┘
```

## Models

| Capability | Implementation | Model | Size |
|-----------|---------------|-------|------|
| 💬 LLM | oMLX API | `Qwen3.5-35B-A3B-4bit` | ~20 GB |
| 👁️ VLM | oMLX API | Any mlx-vlm model | varies |
| 📐 Embed | mlx-lm (uv) | `Qwen3-Embedding-0.6B-4bit-DWQ` | ~1 GB |
| 🎤 ASR | mlx-audio (uv) | `Qwen3-ASR-1.7B-8bit` | ~1.5 GB |
| 👁️ OCR | mlx-vlm (uv) | `PaddleOCR-VL-1.5-6bit` | ~3.3 GB |

## Usage

### LLM / Vision-Language (via oMLX API)

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8000/v1", api_key="local")

# Text generation
resp = client.chat.completions.create(
    model="Qwen3.5-35B-A3B-4bit",
    messages=[{"role": "user", "content": "Hello"}]
)
print(resp.choices[0].message.content)
```

---

### Embeddings (via mlx-lm + uv)

```bash
uv run --with mlx-lm python -c "
from mlx_lm import load
model, tokenizer = load('~/models/Qwen3-Embedding-0.6B-4bit-DWQ')
text = 'text to embed'
inputs = tokenizer(text, return_tensors='np')
embeddings = model(**inputs).last_hidden_state.mean(axis=1)
print(embeddings.shape)
"
```

---

### ASR — Speech-to-Text (via mlx-audio + uv)

> **Important:** Must run with `--python 3.11` to avoid OpenMP threading issues (`SIGSEGV`).

```bash
uv run --python 3.11 --with mlx-audio python -m mlx_audio.stt.generate \
  --model ~/models/Qwen3-ASR-1.7B-8bit \
  --audio "audio.wav" \
  --output-path /tmp/asr_result \
  --format txt \
  --language zh \
  --verbose
```

---

### OCR (via mlx-vlm + uv)

> **Important:** The `generate` function parameter order must be `(model, processor, prompt, image)`.

```bash
cat << 'PY_EOF' > run_ocr.py
import os
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template

model_path = os.path.expanduser("~/models/PaddleOCR-VL-1.5-6bit")
model, processor = load(model_path)
prompt = apply_chat_template(processor, config=model.config, prompt="OCR:", num_images=1)

output = generate(model, processor, prompt, "document.jpg", max_tokens=512, temp=0.0)
print(output.text)
PY_EOF

uv run --python 3.11 --with mlx-vlm python run_ocr.py
```

---

## Service Management (oMLX only)

```bash
# Check running models
curl http://localhost:8000/v1/models

# Restart oMLX
launchctl kickstart -k gui/$(id -u)/com.omlx-server
```

## Model Storage Strategy

**All models stored in `~/models/` using oMLX-compatible structure:**

```
~/models/
├── Qwen3-Embedding-0.6B-4bit-DWQ/
├── Qwen3-ASR-1.7B-8bit/
├── PaddleOCR-VL-1.5-6bit/
└── Qwen3.5-35B-A3B-4bit/
```

## Requirements

- Apple Silicon Mac (M1/M2/M3/M4)
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
