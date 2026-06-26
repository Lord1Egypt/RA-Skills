# TTS Providers

Kiwi supports five text-to-speech providers. Switch between them in `config.yaml` or via environment variable.

## Comparison

| Provider | Quality | Latency | Cost | Local GPU | Languages |
|----------|---------|---------|------|-----------|-----------|
| **ElevenLabs** | Excellent | ~0.3s | ~$0.30/1K chars | No | 29 |
| **Qwen3-TTS (local)** | Excellent | ~1–3s | Free | Yes (CUDA) | Many |
| **Qwen3-TTS (RunPod)** | Excellent | ~2–5s | ~$0.0003/sec | No | Many |
| **Kokoro ONNX** | High | <0.5s | Free | No | 8 |
| **Piper** | Good | <0.5s | Free | No | 30+ |

## Kokoro ONNX

<span class="badge badge-free">FREE</span> <span class="badge badge-new">RECOMMENDED</span>

Fully local TTS with 14 voices at 24kHz. Models auto-download on first use (~340MB). No GPU needed.

```yaml
tts:
  provider: "kokoro"
  kokoro:
    voice: "af_heart"
    speed: 1.0
```

Supports English, Japanese, Chinese, Korean, and several European languages. Russian is not yet supported — use Piper or ElevenLabs for Russian.

## Piper

<span class="badge badge-free">FREE</span>

Fast local TTS using ONNX models. Wide language support including Russian.

```yaml
tts:
  provider: "piper"
  piper:
    model: "en_US-lessac-medium"
```

Models are downloaded automatically. See the [Piper voices list](https://github.com/rhasspy/piper#voices) for available models.

## ElevenLabs

<span class="badge badge-paid">PAID</span>

Cloud-based TTS with the lowest latency and highest voice quality. Requires an API key.

```yaml
tts:
  provider: "elevenlabs"
  elevenlabs:
    voice_id: "aEO01A4wXwd1O8GPgGlF"
    model_id: "eleven_multilingual_v2"
    stability: 0.45
    similarity_boost: 0.75
    speed: 1.0
```

```bash
# .env
KIWI_ELEVENLABS_API_KEY=sk-...
```

## Qwen3-TTS (Local)

<span class="badge badge-free">FREE</span> <span class="badge badge-gpu">GPU REQUIRED</span>

High-quality local TTS using the Qwen3-TTS model. Requires a CUDA GPU with sufficient VRAM.

```yaml
tts:
  provider: "qwen3"
  qwen3:
    backend: "local"
```

## Qwen3-TTS (RunPod)

<span class="badge badge-paid">PAY-PER-USE</span>

Same Qwen3-TTS quality, but running on RunPod serverless GPUs. No local GPU needed.

```yaml
tts:
  provider: "qwen3"
  qwen3:
    backend: "runpod"
```

```bash
# .env
RUNPOD_API_KEY=...
RUNPOD_TTS_ENDPOINT_ID=...
```

## Switching Providers

### Via config.yaml

```yaml
tts:
  provider: "kokoro"   # kokoro, piper, qwen3, elevenlabs
```

### Via environment variable

```bash
KIWI_TTS_PROVIDER=kokoro python -m kiwi
```

### Via REST API

Test TTS without changing config:

```bash
curl -X POST http://localhost:7789/api/tts/test \
  -d '{"text": "Hello, I am Kiwi!"}'
```
