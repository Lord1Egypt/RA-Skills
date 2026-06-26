# GPU & Apple Silicon

Kiwi Voice auto-detects GPU availability and falls back to CPU when no GPU is found.

## NVIDIA CUDA

For GPU-accelerated STT and local TTS:

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Verify:

```bash
python -c "import torch; print(torch.cuda.is_available())"
```

Configure in `config.yaml`:

```yaml
stt:
  device: "cuda"
  compute_type: "float16"
```

!!! tip
    Even without a GPU, Kiwi works well — Faster Whisper runs on CPU with `int8` quantization, and Kokoro ONNX / Piper don't need a GPU at all.

## Apple Silicon (MLX)

On M-series Macs, you can use **Lightning Whisper MLX** for ~10x faster STT:

```bash
pip install lightning-whisper-mlx
```

Configure:

```yaml
stt:
  engine: "mlx-whisper"
  model: "small"          # or large, medium, etc.
```

MLX Whisper is auto-detected on Apple Silicon. On non-Apple hardware, it falls back to Faster Whisper.

## CPU-Only Setup

Kiwi runs fully on CPU with these settings:

```yaml
stt:
  device: "cpu"
  compute_type: "int8"
  model: "small"          # Use small for better CPU performance

tts:
  provider: "kokoro"      # or piper — both are CPU-only
```

No CUDA, no GPU drivers needed. This is the lightest configuration.

## VRAM Requirements

Approximate VRAM usage for GPU components:

| Component | Model | VRAM |
|-----------|-------|------|
| Faster Whisper | `small` | ~1 GB |
| Faster Whisper | `large` | ~3 GB |
| Qwen3-TTS | 0.6B | ~2 GB |
| Qwen3-TTS | 1.7B | ~4 GB |
| pyannote (Speaker ID) | — | ~0.5 GB |

Kokoro ONNX and Piper run on CPU and don't use VRAM.
