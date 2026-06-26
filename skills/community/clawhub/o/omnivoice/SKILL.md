---
name: omnivoice
description: "All-in-one voice identity toolkit: speaker identification, voice library management, voice cloning, and speech-to-text. The only OpenClaw skill with speaker identification — recognize WHO is speaking, not just WHAT they said. 10 operations: identify speakers, manage a voice library (CRUD), clone voices, transcribe audio, voice swap, and persona voice replies. Activate when user sends voice/audio, asks to identify a speaker, manage a voice library, clone someone's voice, transcribe audio, or wants voice-based Q&A in a specific person's voice. Triggers: voice, audio, transcribe, 转文字, 语音, identify speaker, who is speaking, 这是谁的声音, 声纹识别, voice clone, 克隆声音, 模仿声音, voice library, 声音库, voice swap, 声音换皮."
---

# OmniVoice

Ten operations across four capabilities: **identify** (认) · **manage** (存) · **transcribe** (听) · **clone** (说).

## Dependencies

| Component | Install | Purpose |
|-----------|---------|---------|
| Whisper | `pip install openai-whisper` | Speech-to-text |
| Speaker ID | `pip install transformers librosa` | Speaker identification (UniSpeech-SAT) |
| CosyVoice2 | SiliconFlow API (`SF_API_KEY`) | Voice cloning |
| ffmpeg | System package | Audio conversion |

Voice references are stored in `voice-refs/` at workspace root.
Metadata lives in `TOOLS.md` under a "Voice Library" section.
See [references/voice-library-format.md](references/voice-library-format.md) for format spec.

## Operations

### Op 1 · Speaker Identification (声纹查询)

Input: audio → Output: who is speaking (or "unknown")

```bash
python3 scripts/voice_identify.py <audio_file> [--threshold 0.75]
```

Compares audio against all `voice-refs/*-ref*.*` using UniSpeech-SAT x-vector embeddings.
First run downloads model (~360MB) to `/tmp/hf_models/`.

**Accuracy:** Reliably separates male/female voices. Same-gender speakers need ≥5s audio for best results. Threshold 0.75 is default; raise to 0.85 for stricter matching.

### Op 2 · Add Voice to Library (声音入库)

Input: audio + speaker name → stores in voice library

1. Copy audio to `voice-refs/<name>-ref1.<ext>`
2. Transcribe to get reference text: `whisper <audio> --model small --output_format txt --output_dir /tmp`
3. Add entry to `TOOLS.md` (see format in references/)
4. Register speaker in `voice_identify.py` `SPEAKER_MAP`

**Good reference audio:** 10-15s clear speech, minimal noise, natural pace. 5s minimum.

### Op 3 · Voice Library CRUD (声音库管理)

- **List:** Check `TOOLS.md` voice library section + `ls voice-refs/`
- **Add:** See Op 2
- **Update:** Replace file in `voice-refs/`, update `TOOLS.md` entry
- **Delete:** Remove file from `voice-refs/`, remove `TOOLS.md` entry, remove from `SPEAKER_MAP`

### Op 4 · Voice Clone (声音克隆)

Input: text + library speaker → Output: audio in that speaker's voice

```bash
set -a; source <env_file_with_SF_API_KEY>; set +a

python3 scripts/cosyvoice_clone.py \
  --text "Text to speak" \
  --ref voice-refs/<speaker>-ref1.<ext> \
  --ref-text "What is said in reference audio" \
  --output /tmp/clone_output.wav
```

Long reference (>15s): truncate first with `ffmpeg -y -i <ref> -t 15 -ar 24000 -ac 1 /tmp/ref_trimmed.wav`.

### Op 5 · Transcribe (纯转文字)

Input: audio → Output: text

```bash
whisper <audio_file> --model small --output_format txt --output_dir /tmp --language <lang>
```

Languages: `zh` (Chinese), `en` (English), `ja` (Japanese). Omit for auto-detect.

### Op 6 · Transcribe + Identify (转文字+识别)

Input: audio → Output: who said what

Run Op 5 and Op 1 in parallel, report both results together.

### Op 7 · Speaker Verification (声纹验证)

Input: two audio files → Output: same person or not

```bash
python3 scripts/voice_identify.py <audio_1> --threshold 0.75
python3 scripts/voice_identify.py <audio_2> --threshold 0.75
```

Compare the top-ranked speaker from both runs. If they match → same person.
For direct pairwise comparison without a library, extract embeddings and compute cosine similarity (see voice_identify.py internals).

### Op 8 · Voice Swap (声音换皮)

Input: audio + library speaker → Output: same words, different voice

1. Transcribe input audio (Op 5)
2. Clone with target speaker's voice (Op 4), using transcribed text

### Op 9 · Persona Voice Reply — from Audio (人格化语音回复·语音版)

Input: audio question + library speaker → Output: AI answer in that speaker's voice

1. Transcribe the question (Op 5)
2. Generate answer text via LLM
3. Clone answer with target speaker's voice (Op 4)

### Op 10 · Persona Voice Reply — from Text (人格化语音回复·文字版)

Input: text question + library speaker → Output: AI answer in that speaker's voice

1. Generate answer text via LLM
2. Clone answer with target speaker's voice (Op 4)

## Send Audio (Feishu)

```bash
set -a; source <env_file>; set +a
bash scripts/feishu_send_audio.sh <wav_file> <receive_id>
```

Converts wav → opus, uploads, sends as voice message.
Requires `FEISHU_APP_ID` + `FEISHU_APP_SECRET` env vars.

## Extract Audio from Video

```bash
ffmpeg -y -i <video_file> -vn -ar 24000 -ac 1 /tmp/extracted_audio.wav
```
