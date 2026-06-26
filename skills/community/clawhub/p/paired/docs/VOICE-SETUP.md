# Voice Cloning Setup for paired v2.0.0

`paired` v2.0.0 introduces optional voice cloning so the agent can speak with your own voice — for SMS-to-voice dictation, voice notes on Telegram, and live phone replies through your paired device.

## Privacy first

- **Your voice never leaves your hardware.** All synthesis runs locally on your GPU (or CPU fallback).
- **Nothing is bundled with this skill.** The reference WAV and splice clips you record stay in `~/.config/paired/voice/`.
- **No cloud calls.** Models are downloaded once from HuggingFace, then run offline.
- **No training data is shipped upstream.**

## Hardware

| Setup | Quality | Speed |
|-------|---------|-------|
| High-end consumer GPU (16GB+ VRAM, recommended) | 48kHz studio (VoxCPM2) | 5-10s per minute of speech |
| Mid-range GPU (8-12GB VRAM) | 48kHz studio (VoxCPM2) | 10-20s per minute |
| Entry GPU (4-6GB VRAM) | 24kHz (XTTS only) | 5-15s per minute |
| CPU only | 24kHz (XTTS) | 1-5 minutes per minute (slow) |
| No model server | Generic neural (piper) | <1s — no cloning |

## Quick start (assuming Docker + NVIDIA GPU)

### 1. Build and run the VoxCPM2 service

```bash
cd skill/engines
docker build -t paired-voxcpm:latest -f voxcpm.Dockerfile .

mkdir -p ~/.config/paired/voice/word-clips

docker run -d \
  --name paired-voxcpm \
  --gpus all \
  --restart unless-stopped \
  -p 8056:8056 \
  -v ~/.config/paired/voice:/refs \
  -v paired-hf-cache:/root/.cache/huggingface \
  paired-voxcpm:latest
```

First run downloads ~5GB of model weights from HuggingFace (one-time).

### 2. Record your reference voice

```bash
python3 skill/setup/paired-voice-setup.py reference
```

You will be prompted to read 6 phrases. Takes about 5 minutes. Quiet room, same mic distance for every phrase.

### 3. (Optional) Record splice clips for tricky words

If you have an unusual name or word the model mispronounces, record it yourself:

```bash
python3 skill/setup/paired-voice-setup.py word myname
```

The clip lives in `~/.config/paired/voice/word-clips/myname.wav`. The synth wrapper splices it whenever the text contains "myname" (case-insensitive, whole-word).

You can add as many splice words as you like.

### 4. Test

```bash
python3 skill/voice/paired-voice-synth.py "Hello, this is my cloned voice." /tmp/test.wav
mpg123 /tmp/test.wav   # or aplay
```

### 5. Wire into paired

Edit `~/.config/paired/voice.conf` to confirm paths. The paired-respond wrapper picks up the config automatically.

## CPU fallback (no GPU)

The same Docker container runs on CPU. Expect 1-5 minutes generation per minute of audio. Useful for offline / low-power setups.

## Multilingual

VoxCPM2 auto-detects language from input text across 30 languages:

> Arabic, Burmese, Chinese, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew, Hindi, Indonesian, Italian, Japanese, Khmer, Korean, Lao, Malay, Norwegian, Polish, Portuguese, Russian, Spanish, Swahili, Swedish, Tagalog, Thai, Turkish, Vietnamese.

Pass any of these in `text` and you will hear your cloned voice speaking that language.

## Troubleshooting

**Model not loading.** First run takes 2-4 minutes (model download + warmup). Watch `docker logs -f paired-voxcpm`.

**Generation timeout.** VoxCPM2 has a 400-character soft limit per call. `paired-voice-synth.py` chunks long text automatically at sentence boundaries.

**Sounds like the wrong language.** Make sure you are using `reference_wav_path` mode, not `prompt_wav_path + prompt_text`. The synth wrapper does this correctly by default.

**OOM on GPU.** Restart the container — `docker restart paired-voxcpm`. Reduce `inference_timesteps` in the synth config if it keeps happening.

