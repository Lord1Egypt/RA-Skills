# ASR (Automatic Speech Recognition) Skill

Fast, accurate automatic speech-to-text transcription powered by SkillBoss API Hub.

## Why use this skill?
- **Multilingual:** Supports 100 languages with auto-detection.
- **Flexible Input:** Transcribe from a URL or a local file.
- **Agent-Ready:** Designed for high-volume, automated pipelines.
- **Unified API:** Powered by SkillBoss API Hub — single key, single endpoint.

## Setup

### 1. Get an API Key
Sign up at [skillboss.co](https://skillboss.co) to obtain your `SKILLBOSS_API_KEY`.

### 2. Configure Authentication
This skill looks for your API key in the `SKILLBOSS_API_KEY` environment variable.

Add this to your `.env` or agent config:
```bash
SKILLBOSS_API_KEY=your_key_here
```

## Usage
### TL;DR for Agents
When this skill is installed, you can transcribe any URL or local file by running:
`./skills/asr/scripts/asr.sh transcribe --url "https://example.com/audio.mp3"`

### Transcribe a URL
```bash
# Basic transcription
./skills/asr/scripts/asr.sh transcribe --url "https://example.com/audio.mp3"

# With language hint
./skills/asr/scripts/asr.sh transcribe --url "https://example.com/audio.mp3" --language "en"
```

### Transcribe a Local File
```bash
# Upload and transcribe local media
./skills/asr/scripts/asr.sh transcribe --file "./local-audio.wav"
```

### Supported Options
- `--language <code>`: ISO language code (e.g., 'en', 'es')

### Output
Returns a JSON response. The transcription text is in:
```
.result.text
```

If the `SKILLBOSS_API_KEY` is missing, the tool will provide a clear error message.
