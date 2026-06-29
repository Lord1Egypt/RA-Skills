# llm-deploy-helper 🚀

**One-stop local LLM deployment assistant** — detect hardware, get recommendations, and generate Docker Compose / systemd configs.

## Installation

```bash
pip install llm-deploy-helper
```

Optional: install `psutil` for more accurate system detection (works without it too):

```bash
pip install llm-deploy-helper[full]
```

## Quick Start

### 1. Check system & get recommendations

```bash
$ llm-deploy-helper check
```

Example output:

```
╭─────────────────────── System Information ───────────────────────╮
│ Property      │ Value                                            │
├───────────────┼──────────────────────────────────────────────────┤
│ OS            │ linux                                            │
│ CPU Cores     │ 16                                               │
│ RAM           │ 64.0 GB                                          │
│ Free Disk     │ 200.0 GB                                         │
│ GPU Available │ ✅ Yes                                            │
│ GPU Name      │ NVIDIA GeForce RTX 4090                          │
│ GPU VRAM      │ 24.0 GB                                          │
│ CUDA Version  │ 12.4                                             │
╰──────────────────────────────────────────────────────────────────╯

╭─────────────────── 📋 Recommended Engines ───────────────────╮
│ Engine         │ Reason                           │ Score   │
├────────────────┼──────────────────────────────────┼─────────┤
│ ⭐ vLLM         │ Powerful GPU (24 GB VRAM)...    │ 10      │
│ ⭐ Ollama       │ GPU available (RTX 4090)...     │ 8       │
│ ⭐ llama.cpp    │ Abundant RAM (64 GB)...         │ 9       │
╰──────────────────────────────────────────────────────────────╯
```

### 2. Generate Docker Compose config

```bash
# Ollama (auto-uses GPU)
$ llm-deploy-helper generate --engine ollama --model llama3.1:8b

# vLLM (requires GPU)
$ llm-deploy-helper generate --engine vllm --model meta-llama/Llama-3.1-8B-Instruct

# llama.cpp (CPU/GPU)
$ llm-deploy-helper generate --engine llama.cpp --model llama3.1-8b-Q4_K_M.gguf --no-gpu --port 9090
```

Then start:

```bash
docker compose up -d
```

### 3. Generate systemd service

```bash
$ llm-deploy-helper systemd --engine ollama --model llama3.1:8b
```

Install:

```bash
sudo cp ollama-llm.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ollama-llm
```

### 4. List recommended models

```bash
$ llm-deploy-helper models --engine ollama
```

## Supported Engines

| Engine | Image | Default Port | Notes |
|--------|-------|-------------|-------|
| **Ollama** | `ollama/ollama:latest` | 11434 | Easy to use, CPU/GPU adaptive |
| **vLLM** | `vllm/vllm-openai:latest` | 8000 | High-throughput GPU inference |
| **llama.cpp** | `ghcr.io/ggerganov/llama.cpp:server` | 8080 | Lightweight, CPU-friendly, quantized models |

## System Requirements

| Model Size | Min VRAM | Min RAM | Recommended Engine |
|------------|----------|---------|-------------------|
| 7-8B (4-bit) | None (CPU) | 8 GB | llama.cpp, Ollama |
| 7-8B (FP16) | 16 GB | 22 GB | vLLM, Ollama |
| 13-16B (4-bit) | None (CPU) | 16 GB | llama.cpp, Ollama |
| 20B+ (FP16) | 24 GB+ | 32 GB+ | vLLM |

## Commands

| Command | Description |
|---------|-------------|
| `llm-deploy-helper check` | Detect hardware, show recommendations |
| `llm-deploy-helper generate` | Generate docker-compose.yml |
| `llm-deploy-helper systemd` | Generate systemd unit file |
| `llm-deploy-helper models` | List recommended models with requirements |

## Development

```bash
git clone https://github.com/minirr890112-byte/llm-deploy-helper.git
cd llm-deploy-helper
pip install -e ".[dev]"
```

## License

MIT
