# macOS mlx_audio Reference

**Privacy-First | Local Processing | Optimized for Apple Silicon**

This guide covers using Qwen3-TTS on macOS with Apple Silicon (M1/M2/M3/M4) using the `mlx_audio` library.

## Why Local TTS on macOS?

### Privacy Benefits

Using `mlx_audio` on macOS ensures:

- **100% Offline Processing** - No internet required after model download
- **Zero Data Transmission** - Your text never leaves your Mac
- **No Cloud Dependencies** - No API keys, no external services
- **Apple Silicon Optimization** - Leverages Neural Engine and GPU

### Security Advantages

| Feature | Cloud TTS | mlx_audio (Local) |
|---------|-----------|-------------------|
| Network Required | Yes | No (after download) |
| Data Leaves Device | Yes | Never |
| API Keys | Required | Not needed |
| Audit Trail | External | You control |

## Installation

### Requirements
- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.8+
- ffmpeg

### Install

```bash
pip install mlx-audio
brew install ffmpeg
```

## Command Structure

```bash
python -m mlx_audio.tts.generate [OPTIONS]
```

## All Parameters

### Required

| Parameter | Description |
|-----------|-------------|
| `--text` | Text to synthesize |
| `--model` | Model identifier (e.g., `mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit`) |

### Optional

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--output` / `-o` | Output file path | Auto-generated |
| `--voice` | Preset voice (CustomVoice only) | None |
| `--instruct` | Voice description (VoiceDesign only) | None |
| `--ref_audio` | Reference audio for cloning | None |
| `--ref_text` | Reference text for cloning | None |
| `--speed` | Speaking speed (0.5-2.0) | 1.0 |
| `--gender` | Voice gender | None |
| `--pitch` | Voice pitch (0.5-2.0) | 1.0 |
| `--lang_code` | Language code | en-US |
| `--temperature` | Sampling temperature | 0.7 |
| `--top_p` | Top-p sampling | 0.9 |
| `--repetition_penalty` | Repetition penalty | 1.0 |

## Model Identifiers

All models use 8bit quantization for efficiency.

### 1.7B Models (Best Quality)

```
mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit
mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit
mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit
```

### 0.6B Models (Faster)

```
mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit
mlx-community/Qwen3-TTS-12Hz-0.6B-VoiceDesign-8bit
mlx-community/Qwen3-TTS-12Hz-0.6B-CustomVoice-8bit
```

## Preset Voices (CustomVoice)

The CustomVoice model includes **9 premium preset voices** (Open Source Version):

1. **Chelsie** - Female, English (American) - Gentle, breathy, empathetic
2. **Serena** - Female, English - Warm, gentle young female
3. **Ono Anna** - Female, Japanese - Playful Japanese female voice
4. **Sohee** - Female, Korean - Warm Korean female voice
5. **Aiden** - Male, English (American) - Sunny American male voice
6. **Dylan** - Male, English - English male voice
7. **Eric** - Male, English - English male voice
8. **Ryan** - Male, English - English male voice
9. **Uncle Fu** - Male, Chinese (Beijing) - Youthful Beijing male voice

**Recommended Natural/Real Voices:**
- **Natural Female:** `Chelsie` (gentle, empathetic) or `Serena` (warm)
- **Real Male:** `Aiden` (sunny, American) or `Ryan` (natural English)

**Note:** Use `model.get_supported_speakers()` to list available voices programmatically.

## Language Codes

| Code | Language |
|------|----------|
| `en-US` | American English |
| `en-GB` | British English |
| `zh-CN` | Mandarin Chinese (Simplified) |
| `zh-TW` | Mandarin Chinese (Traditional) |
| `ja` | Japanese |
| `ko` | Korean |
| `de` | German |
| `fr` | French |
| `ru` | Russian |
| `pt` | Portuguese |
| `es` | Spanish |
| `it` | Italian |
| `auto` | Auto-detect |

## Usage Examples

### Basic TTS

```bash
python -m mlx_audio.tts.generate \
    --text "Hello world" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit \
    --output hello.wav
```

### CustomVoice with Female Voice (Natural, Real)

```bash
python -m mlx_audio.tts.generate \
    --text "Welcome to our service" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
    --voice Chelsie \
    --speed 1.1 \
    --lang_code en-US \
    --output welcome.wav
```

### CustomVoice with Male Voice (Natural, Real)

```bash
python -m mlx_audio.tts.generate \
    --text "Thank you for calling" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
    --voice Aiden \
    --speed 0.9 \
    --lang_code en-US \
    --output thankyou.wav
```

### VoiceDesign

```bash
python -m mlx_audio.tts.generate \
    --text "I am your AI assistant" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit \
    --instruct "A professional female voice, calm and clear" \
    --speed 1.0 \
    --lang_code en-US \
    --output assistant.wav
```

### Voice Cloning

```bash
python -m mlx_audio.tts.generate \
    --text "This is my cloned voice speaking" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit \
    --ref_audio /path/to/reference.wav \
    --ref_text "The reference audio transcript" \
    --output cloned.wav
```

### Chinese TTS

```bash
python -m mlx_audio.tts.generate \
    --text "" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
    --voice Aiden \
    --lang_code zh-CN \
    --output chinese.wav
```

## Advanced Parameters

### Temperature and Top-p

Control the randomness and diversity of the generated speech:

```bash
python -m mlx_audio.tts.generate \
    --text "Hello" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit \
    --temperature 0.8 \
    --top_p 0.95
```

- **Temperature**: Higher values (e.g., 0.9) produce more varied output, lower values (e.g., 0.5) produce more deterministic output
- **Top-p**: Nucleus sampling parameter (0.0-1.0)

### Repetition Penalty

Prevent repetitive patterns:

```bash
python -m mlx_audio.tts.generate \
    --text "Hello hello hello" \
    --model mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit \
    --repetition_penalty 1.2
```

## Performance Tips

1. **Use 0.6B models** for faster generation with slight quality trade-off
2. **First run downloads models** - subsequent runs are faster
3. **Apple Silicon optimization** - runs efficiently on M-series chips
4. **Memory usage** - 1.7B models use ~4GB RAM, 0.6B models use ~2GB

## Troubleshooting

### Model Download Issues

If models fail to auto-download:

```bash
# Manually download with huggingface-cli
pip install huggingface-hub
huggingface-cli download mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit
```

### Audio Format Issues

Ensure ffmpeg is installed:

```bash
brew install ffmpeg
which ffmpeg  # Should return /opt/homebrew/bin/ffmpeg
```

### Out of Memory

Use smaller models:

```bash
# Use 0.6B instead of 1.7B
--model mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit
```

### Slow Generation

- Close other memory-intensive applications
- Use 0.6B models for faster inference
- Ensure you're on Apple Silicon (Intel Macs will be slower)
