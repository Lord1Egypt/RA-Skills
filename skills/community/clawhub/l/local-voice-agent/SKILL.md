---
name: local-voice-agent
description: Complete offline voice-to-voice AI assistant for OpenClaw (Whisper.cpp STT + Pocket-TTS). 100% local processing, no cloud APIs, no costs. Use for hands-free operation, voice commands, accessibility, or custom voice cloning.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎤",
        "requires": { "bins": ["whisper-cli", "python3", "ffmpeg"], "env": [] },
        "install":
          [
            {
              "id": "whisper-cpp",
              "kind": "git",
              "repo": "https://github.com/ggerganov/whisper.cpp",
              "target": "~/.local/whisper.cpp",
              "build": "make -j4",
              "bins": ["build/bin/whisper-cli"],
              "label": "Install Whisper.cpp (STT)",
            },
            {
              "id": "pocket-tts-server",
              "kind": "manual",
              "label": "Start Pocket-TTS server (see README)",
            },
          ],
      },
  }
---

# Voice Agent - OpenClaw Skill

Complete voice-to-voice AI assistant for hands-free operation.

## Architecture

```
User Voice → Whisper STT → Text → OpenClaw AI → Text → Pocket-TTS → Voice Response
```

## Prerequisites

### 1. Whisper.cpp (Speech-to-Text)

```bash
# Clone and build
git clone https://github.com/ggerganov/whisper.cpp ~/.local/whisper.cpp
cd ~/.local/whisper.cpp
make -j4

# Download tiny model (fast, low-resource)
bash ./models/download-ggml-model.sh tiny
```

**Test:**
```bash
./build/bin/whisper-cli -m models/ggml-tiny.bin -f samples/jfk.wav
```

### 2. Pocket-TTS (Text-to-Speech)

**Option A: Use existing server**
```bash
export POCKET_TTS_URL="http://localhost:5000"
```

**Option B: Install locally**
```bash
# Clone your Pocket-TTS server
cd /path/to/pockettts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m app.main --host 0.0.0.0 --port 5000
```

### 3. FFmpeg (Audio Conversion)

```bash
sudo apt-get install -y ffmpeg
```

## Quick Start

### Voice Command (One-shot)

```bash
# Record → Transcribe → Process → Speak
./bin/voice-agent "What's the weather today?"
```

### Interactive Mode

```bash
# Continuous voice conversation
./bin/voice-agent --interactive
```

### Voice File Processing

```bash
# Transcribe existing audio file
./bin/voice-to-text recording.wav

# Generate voice from text
./bin/text-to-voice "Hello world!" output.wav
```

## Configuration

Edit `config/voices.yaml`:

```yaml
# Default voices
stt:
  model: tiny  # tiny, small, medium (larger = more accurate, slower)
  language: en  # en, ne, hi, etc.

tts:
  url: http://localhost:5000
  voice: peter voice  # Your custom voice
  format: wav  # wav, mp3

# Performance
performance:
  threads: 4  # CPU threads for Whisper
  realtime: true  # Faster-than-realtime processing
```

## API Endpoints

### POST /v1/voice/command

Voice command processing:

```bash
curl -X POST "http://localhost:5000/v1/voice/command" \
  -F "audio=@recording.wav" \
  -F "action=openclaw"
```

Response:
```json
{
  "transcription": "What's the weather today?",
  "response_text": "The weather in Kathmandu is partly cloudy, 22 degrees Celsius.",
  "audio_response": "/tmp/response.wav"
}
```

### GET /v1/voices

List available TTS voices:

```bash
curl http://localhost:5000/v1/voices
```

## Use Cases

### 1. Daily Briefings (Voice)

```bash
./bin/voice-agent "Give me my morning briefing"
```

### 2. Voice Notes

```bash
./bin/voice-agent "Remind me to call Peter at 3 PM"
```

### 3. Hands-Free Coding

```bash
./bin/voice-agent "Show me the status of my git repository"
```

### 4. Accessibility

Perfect for users who prefer voice interaction or have mobility constraints.

## Scripts

### bin/voice-to-text

Convert speech to text:

```bash
./bin/voice-to-text input.wav
./bin/voice-to-text input.ogg  # Auto-converts with ffmpeg
./bin/voice-to-text input.mp4  # Extracts audio from video
```

### bin/text-to-voice

Convert text to speech:

```bash
./bin/text-to-voice "Hello world!" output.wav
./bin/text-to-voice --voice "usha lama" "Namaste!" greeting.wav
```

### bin/voice-agent

Full voice pipeline:

```bash
./bin/voice-agent "What time is it?"
./bin/voice-agent --interactive  # Conversation mode
./bin/voice-agent --file recording.wav  # Process file
```

## Troubleshooting

### Whisper.cpp Errors

**"failed to read audio file"**
- Convert to WAV first: `ffmpeg -i input.ogg -ar 16000 -ac 1 output.wav`

**"model not found"**
- Download model: `bash models/download-ggml-model.sh tiny`

### Pocket-TTS Errors

**"Connection refused"**
- Start TTS server: `python3 -m app.main`
- Check URL: `export POCKET_TTS_URL="http://localhost:5000"`

**"Voice not found"**
- List voices: `curl http://localhost:5000/v1/voices`
- Clone custom voice if needed

### Performance Issues

**Slow transcription**
- Use smaller model: `tiny` instead of `small`
- Reduce audio sample rate: `ffmpeg -i input.wav -ar 16000 output.wav`

**Slow TTS**
- Use shorter text
- Generate in background

## Examples

See `examples/` directory for:
- `morning-briefing.sh` - Automated voice briefing
- `voice-reminder.sh` - Voice-based reminders
- `conversation-mode.sh` - Interactive voice chat

## Performance

| Model | RAM | Speed (1 min audio) | Accuracy |
|-------|-----|---------------------|----------|
| **tiny** | 500MB | ~30 sec | ~90% |
| **small** | 1GB | ~60 sec | ~95% |
| **medium** | 2GB | ~120 sec | ~98% |

**Recommendation:** Start with `tiny`, upgrade to `small` if needed.

## License

MIT License - See LICENSE file

## Credits

- **Whisper.cpp** by Georgi Gerganov (ggerganov/whisper.cpp)
- **Pocket-TTS** by Kyutai Labs (kyutai-labs/pocket-tts)
- **OpenClaw** by OpenClaw Team (openclaw/openclaw)

## Support

- GitHub Issues: [Your Repo Link]
- OpenClaw Discord: https://discord.com/invite/clawd
- Documentation: [Your Docs Link]
