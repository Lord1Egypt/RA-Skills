# Wake Word Detection

Kiwi supports two wake word engines: **text-based fuzzy matching** (default) and **OpenWakeWord ML detection**.

## Text Engine (default)

The simplest approach — Kiwi runs Whisper STT continuously and checks the transcript for the wake word using fuzzy string matching.

```yaml
wake_word:
  engine: "text"
  keyword: "kiwi"
```

**How it works:**

1. Audio is captured and processed through Silero VAD (Voice Activity Detection)
2. Speech segments are transcribed by Faster Whisper
3. The transcript is checked for the wake word using Levenshtein distance
4. Common misspellings and phonetic variants are defined per-language in locale files

**Pros:** No extra model, works with any word, language-aware typo matching.

**Cons:** Higher CPU/GPU usage (Whisper runs on all speech), slightly higher latency.

## OpenWakeWord Engine (ML)

A dedicated ONNX model (~10MB) that listens to raw audio in real time — no Whisper needed for wake word detection.

```yaml
wake_word:
  engine: "openwakeword"
  model: "hey_jarvis"      # Built-in model name or path to .onnx file
  threshold: 0.5           # Detection sensitivity (0.0–1.0)
```

**Performance:** ~80ms latency, ~2% CPU usage.

### Built-in Models

| Model | Wake Phrase |
|-------|------------|
| `hey_jarvis` | "Hey Jarvis" |
| `alexa` | "Alexa" |
| `hey_mycroft` | "Hey Mycroft" |

### How it Works

1. Audio is captured at 16kHz
2. OpenWakeWord processes raw PCM frames through a small ONNX neural network
3. When confidence exceeds the threshold, wake word is detected
4. Only then does Whisper STT activate to transcribe the actual command
5. This saves significant compute — Whisper only runs when needed

!!! tip "Threshold tuning"
    Start with `0.5`. Lower values (0.3) increase sensitivity but may cause false activations. Higher values (0.7) reduce false positives but may miss some activations.

### Train a Custom Wake Word

You can train your own wake word (e.g., "Hey Kiwi") using Google Colab — no voice recordings needed:

```bash
python scripts/train_wake_word.py --phrase "hey kiwi"
```

This generates synthetic training data and trains an ONNX model. Place the resulting `.onnx` file in the project directory and reference it in config:

```yaml
wake_word:
  engine: "openwakeword"
  model: "path/to/hey_kiwi.onnx"
  threshold: 0.5
```

### Environment Overrides

```bash
KIWI_WAKE_ENGINE=openwakeword
KIWI_WAKE_MODEL=hey_jarvis
KIWI_WAKE_THRESHOLD=0.5
```

## Comparison

| | Text Engine | OpenWakeWord |
|---|---|---|
| CPU usage | Higher (Whisper always on) | ~2% |
| Latency | ~500ms–2s | ~80ms |
| Custom words | Any word, just change config | Needs model training |
| Extra model | No | ~10MB ONNX |
| Language support | All 15 languages | Language-independent |
