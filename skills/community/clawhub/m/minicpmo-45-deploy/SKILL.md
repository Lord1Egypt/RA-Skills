---
name: minicpmo-45-deploy
description: >-
  Deploy MiniCPM-o 4.5 multimodal model via Web Demo, vLLM Serve, or
  llamacpp-omni. Use when the user asks to deploy, start, configure, or
  troubleshoot MiniCPM-o 4.5 services, or mentions deployment, serving,
  inference, or demo setup.
---

# MiniCPM-o 4.5 Deployment Guide

This skill guides the Agent through deploying MiniCPM-o 4.5. Choose the appropriate section based on your deployment method.

## Step 0: Check Your Device and Choose a Deployment Method

Before deploying, check your device type and resources. Follow this decision tree:

```
What is your device?
│
├─ NVIDIA GPU
│   ├─ VRAM >= 28GB (A100 / H100 / RTX A6000)
│   │   └─→ Web Demo (full bf16) ✅
│   │
│   ├─ VRAM 12-24GB (RTX 3060 12G / RTX 4070 / RTX 4090)
│   │   └─→ Web Demo (AWQ/BNB int4 quantized) ✅
│   │
│   └─ VRAM < 12GB
│       └─→ ⚠ Not yet supported (llamacpp-omni / vLLM planned)
│
├─ Apple Silicon (M1/M2/M3/M4/M5 Mac)
│   └─→ ⚠ Not yet supported (llamacpp-omni planned, stay tuned)
│
├─ CPU only (no GPU)
│   └─→ ⚠ Not yet supported (llamacpp-omni planned, stay tuned)
│
└─ Other platforms (AMD GPU / Intel Arc / Ascend NPU, etc.)
    └─→ ⚠ Not tested and not yet supported
```

> **Agent guideline:** Only NVIDIA GPUs with VRAM >= 12GB are currently supported (Web Demo).
> For all other devices — **Apple Silicon, CPU-only, NVIDIA < 12GB, AMD, Intel Arc, Ascend NPU, etc.** — inform the user:
> "This device is not yet supported for MiniCPM-o 4.5 deployment. Support for Apple Silicon and low-resource devices via llamacpp-omni is planned. Please stay tuned for updates."
> **Do NOT attempt to guide the user through any deployment steps for unsupported devices.**

## Deployment Methods Overview

| Method | Use Case | Model Format | Section |
|--------|----------|-------------|---------|
| **Web Demo** | Interactive experience (chat / voice / full-duplex) | bf16 / AWQ / BNB | [Web Demo Deployment](#web-demo-deployment) |
| **vLLM Serve** | High-throughput API serving | bf16 / AWQ | [vLLM Serve Deployment](#vllm-serve-deployment) |
| **llamacpp-omni** | Low-resource / Apple / CPU inference | GGUF | [llamacpp-omni Deployment](#llamacpp-omni-deployment) |

---

## References

- **Documentation**: https://minicpm-o.readthedocs.io/
- **HuggingFace**: https://huggingface.co/openbmb/MiniCPM-o-4_5
- **ModelScope**: https://modelscope.cn/models/OpenBMB/MiniCPM-o-4_5

### Hardware Requirements

| Variant | Precision | Model Size | Inference VRAM | Recommended Device |
|---------|-----------|-----------|---------------|-------------------|
| Full (bfloat16) | bf16 | ~18GB | ~21.5GB | NVIDIA >= 28GB (A100 / H100 / RTX A6000) |
| AWQ quantized (int4) | W4A16 | ~6GB | ~11GB | NVIDIA >= 12GB (RTX 3060 12G / RTX 4070) |
| BNB quantized (int4) | NF4 | ~6GB | ~11GB | NVIDIA >= 12GB (RTX 3060 12G / RTX 4070) |
| GGUF (llama.cpp) | Q4_K_M | ~6GB | ~12GB VRAM or 16GB RAM | NVIDIA >= 12GB / Apple M3+ >= 16GB / CPU only |

- Pre-quantized AWQ model: [openbmb/MiniCPM-o-4_5-awq](https://huggingface.co/openbmb/MiniCPM-o-4_5-awq)
- llama.cpp-omni full-duplex requires Apple M4 Max >= 24GB RAM or NVIDIA >= 12GB

---

## Web Demo Deployment

### Step 1: Environment Setup

**1.1 Python 3.10+**

Skip if Python 3.10+ is already available. Otherwise, install Miniconda:

```bash
mkdir -p ./miniconda3_install_tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_25.11.1-1-Linux-x86_64.sh \
    -O ./miniconda3_install_tmp/miniconda.sh
bash ./miniconda3_install_tmp/miniconda.sh -b -u -p ./miniconda3
source ./miniconda3/bin/activate
```

`install.sh` defaults to `python3.10`. Use `PYTHON=python3.11 bash install.sh` to specify another version.

**1.2 FFmpeg**

```bash
sudo apt update && sudo apt install -y ffmpeg
```

**1.3 Clone Repository and Install Dependencies**

```bash
git clone https://github.com/OpenBMB/MiniCPM-o-Demo.git
cd MiniCPM-o-Demo
bash ./install.sh
```

`install.sh` automatically: creates `.venv/base` virtual environment -> installs PyTorch 2.8.0 -> installs `requirements.txt` dependencies -> verifies the environment.

Manual installation alternative:

```bash
python -m venv .venv/base && source .venv/base/bin/activate
pip install "torch==2.8.0" "torchaudio==2.8.0"
pip install -r requirements.txt
```

### Step 2: Model Download

Model size is ~18GB. Use the auto-source script to benchmark and pick the fastest source via SDK:

```bash
# Auto-benchmark sources (downloads config.json from HuggingFace / ModelScope via SDK)
python scripts/download_model.py --local-dir ./model/MiniCPM-o-4_5

# Manually specify source: huggingface / modelscope
python scripts/download_model.py --source modelscope --local-dir ./model/MiniCPM-o-4_5
```

The script automatically verifies the model after download. If the user already has a model, verify it separately:

```bash
# Verify a local model directory
python scripts/download_model.py --verify /path/to/MiniCPM-o-4_5

# Verify a HuggingFace Hub ID (downloads config.json to check)
python scripts/download_model.py --verify openbmb/MiniCPM-o-4_5
```

Checks: `model_type == "minicpmo"`, `architectures` contains `"MiniCPMO"`, `version == "4.5"`.

> Script is at `scripts/download_model.py`. Can also be imported: `from download_model import verify_model`

Manual download alternatives:

```bash
# HuggingFace CLI
huggingface-cli download openbmb/MiniCPM-o-4_5 --local-dir /path/to/MiniCPM-o-4_5

# ModelScope
modelscope download --model OpenBMB/MiniCPM-o-4_5 --local_dir /path/to/MiniCPM-o-4_5
```

You can also skip manual download — the model will be automatically downloaded from HuggingFace Hub on first launch (requires stable network).

> **Agent guideline:** When the user provides a custom model path, run `python scripts/download_model.py --verify <model_path>` to confirm the model is valid before proceeding to configuration.

### Step 3: Configuration

```bash
cp config.example.json config.json
```

**Minimal configuration** (no changes needed when using auto-download):

```json
{
  "model": { "model_path": "openbmb/MiniCPM-o-4_5" }
}
```

**Local model configuration**:

```json
{
  "model": { "model_path": "/path/to/MiniCPM-o-4_5" }
}
```

Configuration priority: CLI arguments > config.json > defaults. See [web-demo-reference.md](references/web-demo-reference.md) for all configuration fields.

### Step 4: Generate SSL Certificate

Browser microphone/camera APIs require HTTPS. SSL certificate is mandatory:

```bash
mkdir -p certs
openssl req -x509 -newkey rsa:2048 \
    -keyout certs/key.pem -out certs/cert.pem \
    -days 365 -nodes -subj '/CN=dev'
```

Self-signed certificates trigger a browser security warning — click "Proceed" to continue. Replace files under `certs/` when you have a proper certificate.

### Step 5: Start the Service

```bash
# Single GPU
CUDA_VISIBLE_DEVICES=0 bash start_all.sh

# Multi-GPU (one Worker per GPU, parallel request processing)
CUDA_VISIBLE_DEVICES=0,1,2,3 bash start_all.sh

# HTTP mode (microphone/camera unavailable, not recommended)
bash start_all.sh --http
```

The startup script automatically: detects GPUs -> launches Workers (one per GPU) -> waits for model loading (~30-90s) -> starts Gateway -> prints access URLs.

### Step 6: Verify and Use

Successful startup output:

```
Service is running!
Chat Demo:  https://localhost:8006
Admin:      https://localhost:8006/admin
API Docs:   https://localhost:8006/docs
```

Verify with curl:

```bash
curl -k https://localhost:8006/health
```

**Four interaction modes:**

| Mode | URL | Description |
|------|-----|-------------|
| Turn-based Chat | `/` | Text/image/audio/video input, streaming text + voice output |
| Half-Duplex Audio | `/half_duplex` | Server-side VAD, auto-detects speech start/end |
| Omnimodal Full-Duplex | `/omni` | Simultaneous audio + video input, model decides when to respond |
| Audio Full-Duplex | `/audio_duplex` | Real-time bidirectional voice conversation |
| Admin | `/admin` | Worker status / queue / session management |

### Stop the Service

```bash
kill $(cat tmp/*.pid 2>/dev/null) 2>/dev/null
# or
pkill -f "gateway.py|worker.py"
```

### Advanced: torch.compile Acceleration

Set `"service": { "compile": true }` in `config.json`.

Pre-compile (recommended to avoid ~15min cold compilation on first run):

```bash
CUDA_VISIBLE_DEVICES=0 TORCHINDUCTOR_CACHE_DIR=./torch_compile_cache \
    .venv/base/bin/python precompile.py
```

With cache, startup overhead drops to ~5min. Omni Full-Duplex per-unit latency decreases from ~0.9s to ~0.5s (A100).

### Troubleshooting

See [web-demo-reference.md](references/web-demo-reference.md) for detailed troubleshooting. Quick reference:

| Issue | Resolution |
|-------|-----------|
| OOM | Confirm VRAM >= 28GB, check usage with `nvidia-smi` |
| Microphone/camera unavailable | Confirm HTTPS mode and certificates exist |
| Slow model download | Use `--source modelscope` or ModelScope CLI |
| Worker fails to start | Check `tmp/worker_*.log`, verify CUDA driver / model path / port conflicts |

---

## vLLM Serve Deployment

> **⚠ Not Yet Available** — The vLLM Serve deployment is under development and not ready for use.

> **Agent guideline:** When the user selects or is directed to the vLLM Serve method, respond directly:
> "The vLLM Serve deployment is not yet available. Please use the Web Demo method as an alternative for now. We will support vLLM Serve soon — stay tuned for updates."
> **Do NOT attempt to guide the user through vLLM deployment steps.**

### Planned Content Outline (In Development)

1. Environment setup and vLLM installation
2. Model loading configuration
3. Starting the vLLM server
4. API call examples (OpenAI-compatible format)
5. Multimodal input (image / audio / video)
6. Performance tuning (tensor parallel / quantization / prefix caching)
7. Troubleshooting

---

## llamacpp-omni Deployment

> **⚠ Not Yet Available** — The llamacpp-omni deployment is under development and not ready for use.

> **Agent guideline:** When the user selects or is directed to llamacpp-omni (including Apple devices, low-VRAM NVIDIA, CPU-only, or other platforms), respond directly:
> "The llamacpp-omni deployment is not yet available. If you have an NVIDIA GPU (VRAM >= 12GB), you can use the Web Demo method (int4 quantized) for now. We will support llamacpp-omni soon — stay tuned for updates."
> **Do NOT attempt to guide the user through llamacpp-omni deployment steps.**

### Planned Content Outline (In Development)

1. Environment setup and llama.cpp compilation
2. GGUF model conversion and download
3. Starting the inference service
4. API call examples
5. Multimodal input support
6. Quantization precision and performance comparison
7. Troubleshooting
