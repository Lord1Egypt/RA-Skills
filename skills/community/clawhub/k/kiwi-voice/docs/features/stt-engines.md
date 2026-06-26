# STT Engines

Kiwi supports three speech-to-text engines. Switch between them in `config.yaml` or via environment variable.

## Comparison

| Engine | Quality | Latency | Cost | Local | GPU |
|--------|---------|---------|------|-------|-----|
| **Faster Whisper** | Excellent | ~1–3s | Free | Yes | Optional (CUDA) |
| **ElevenLabs** | Excellent | ~0.3–0.5s | ~$0.018/min | No | No |
| **MLX Whisper** | Excellent | ~0.5–1s | Free | Yes | Apple Silicon |

## Faster Whisper

<span class="badge badge-free">FREE</span> <span class="badge badge-new">DEFAULT</span>

Local STT using CTranslate2-optimized Whisper models. Works on CPU or CUDA GPU.

```yaml
stt:
  engine: "faster-whisper"
  model: "small"             # tiny, base, small, medium, large
  device: "cuda"             # cuda or cpu
  compute_type: "float16"    # float16 (GPU) or int8 (CPU)
  language: "ru"
```

!!! tip "Model size tradeoff"
    `small` is the sweet spot — fast with good accuracy. Use `large` for best accuracy (slower startup), `tiny` for minimal resources.

## ElevenLabs

<span class="badge badge-paid">PAID</span> <span class="badge badge-cloud">CLOUD</span>

Cloud-based STT via WebSocket (Scribe v2 model). Lowest latency, no local resources needed. Uses the same API key as ElevenLabs TTS.

```yaml
stt:
  engine: "elevenlabs"
  elevenlabs:
    model_id: "scribe_v2"
    language_code: ""        # auto-detect if empty; or "ru", "en", etc.
```

```bash
# .env — same key for both TTS and STT
KIWI_ELEVENLABS_API_KEY=sk-...
```

!!! info "How it works"
    Kiwi collects audio using the same VAD pipeline (energy + Silero), then sends the full buffer to ElevenLabs via WebSocket for transcription. All existing hallucination filtering and wake word detection still applies.

!!! note "Pricing"
    ElevenLabs STT costs ~$0.018/min (~$1.05/hr). With typical voice assistant usage (a few minutes of speech per hour), the cost is minimal.

## MLX Whisper

<span class="badge badge-free">FREE</span> <span class="badge badge-gpu">APPLE SILICON</span>

Local STT optimized for Apple Silicon using Lightning Whisper MLX. ~10x faster than standard Whisper on M-series chips.

```yaml
stt:
  engine: "mlx-whisper"
  model: "distil-medium.en"
  mlx_batch_size: 12
```

Requires `lightning-whisper-mlx` — only available on macOS with Apple Silicon (M1/M2/M3/M4).

## Switching Engines

### Via config.yaml

```yaml
stt:
  engine: "elevenlabs"   # faster-whisper, elevenlabs, mlx-whisper
```

### Via environment variable

```bash
KIWI_STT_ENGINE=elevenlabs python -m kiwi
```

### Engine aliases

For convenience, these aliases are also accepted:

| Alias | Resolves to |
|-------|-------------|
| `whisper` | `faster-whisper` |
| `eleven` | `elevenlabs` |
| `11labs` | `elevenlabs` |
