# Web Demo Deployment Reference

This document supplements SKILL_EN.md with complete configuration details, advanced deployment options, and troubleshooting.

## Complete Configuration Fields

`config.json` contains the following groups. Priority: CLI arguments > config.json > defaults.

```json
{
  "model": {
    "model_path": "openbmb/MiniCPM-o-4_5",
    "pt_path": null,
    "attn_implementation": "auto"
  },
  "audio": {
    "ref_audio_path": "assets/ref_audio/ref_minicpm_signature.wav",
    "playback_delay_ms": 200,
    "chat_vocoder": "token2wav"
  },
  "service": {
    "gateway_port": 8006,
    "worker_base_port": 22400,
    "max_queue_size": 1000,
    "request_timeout": 300.0,
    "compile": false,
    "data_dir": "data"
  },
  "duplex": {
    "pause_timeout": 60.0
  }
}
```

### Field Reference

| Group | Field | Default | Description |
|-------|-------|---------|-------------|
| **model** | `model_path` | `openbmb/MiniCPM-o-4_5` | HuggingFace model directory or Hub ID |
| model | `pt_path` | null | Optional additional .pt weight override path |
| model | `attn_implementation` | `"auto"` | Attention implementation (auto / flash\_attention\_2 / sdpa / eager) |
| **audio** | `ref_audio_path` | `assets/ref_audio/ref_minicpm_signature.wav` | TTS reference audio path |
| audio | `playback_delay_ms` | 200 | Frontend audio playback delay (ms), range 0-2000 |
| audio | `chat_vocoder` | `"token2wav"` | Vocoder: token2wav (lightweight, default) / cosyvoice2 (requires extra dependencies) |
| **service** | `gateway_port` | 8006 | Gateway listening port |
| service | `worker_base_port` | 22400 | Worker base port (Worker N = base + N) |
| service | `max_queue_size` | 1000 | Maximum queued requests |
| service | `request_timeout` | 300.0 | Request timeout (seconds) |
| service | `compile` | false | Enable torch.compile acceleration |
| service | `data_dir` | `"data"` | Data storage directory |
| **duplex** | `pause_timeout` | 60.0 | Duplex pause timeout (seconds), releases Worker when exceeded |

## Attention Backend Selection

| Value | Behavior | Use Case |
|-------|----------|----------|
| `"auto"` (default) | Detects flash-attn -> flash\_attention\_2, otherwise -> sdpa | Recommended, compatible with all environments |
| `"flash_attention_2"` | Forces Flash Attention 2 | flash-attn package installed |
| `"sdpa"` | PyTorch built-in SDPA | Cannot compile flash-attn |
| `"eager"` | Naive Attention | Debug only |

Performance on A100: flash\_attention\_2 is ~5-15% faster than sdpa; sdpa is several times faster than eager.

## Multi-GPU Deployment

Gateway + Worker Pool architecture, one Worker per GPU.

- **Turn-based / Half-Duplex**: Request-level load balancing
- **Full-Duplex**: Session affinity (entire session bound to one Worker)

```bash
CUDA_VISIBLE_DEVICES=0,1,2,3 bash start_all.sh
```

4 Workers run on ports 22400-22403; Gateway exposes port 8006.

## Manual Startup (Advanced)

Start Worker and Gateway separately for finer-grained control:

```bash
# Worker (one terminal per GPU)
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=. .venv/base/bin/python worker.py \
    --port 22400 --gpu-id 0 --worker-index 0

# Gateway (another terminal)
PYTHONPATH=. .venv/base/bin/python gateway.py \
    --port 8006 --workers localhost:22400
```

## torch.compile Performance Comparison

| Metric | Without Compile | With Compile |
|--------|----------------|--------------|
| Omni Full-Duplex per-unit latency (A100) | ~0.9s | ~0.5s |
| First startup overhead (cold compile) | — | ~15 min |
| First startup overhead (cached) | — | ~5 min |
| VRAM usage | ~21.5 GB | ~21.5 GB |

## Troubleshooting

### Out of Memory (OOM)

Loading in bfloat16 requires ~21.5GB VRAM. Recommended GPU VRAM >= 28GB.

Steps:
1. Check VRAM usage with `nvidia-smi`
2. Confirm no other processes are consuming VRAM
3. Verify multiple Workers are not assigned to the same GPU

### Microphone / Camera Unavailable

Browser security policies require HTTPS.

Steps:
1. Confirm the service was not started with `--http`
2. Verify `key.pem` and `cert.pem` exist under `certs/`
3. Click "Proceed" on browser security warning page

### Slow Model Download

```bash
# Use hf-mirror
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download openbmb/MiniCPM-o-4_5 --local-dir /path/to/model

# Or use ModelScope
modelscope download --model OpenBMB/MiniCPM-o-4_5 --local_dir /path/to/model
```

After download, point `model_path` in `config.json` to the local path.

### Worker Fails to Start

```bash
cat tmp/worker_0.log
```

Common causes:
- CUDA driver version incompatible with PyTorch 2.8.0
- Incorrect `model_path` in `config.json`
- Port conflict — change `worker_base_port` or `gateway_port`

### API Documentation

After starting the service, visit `https://localhost:8006/docs` for the interactive Swagger UI API documentation.
