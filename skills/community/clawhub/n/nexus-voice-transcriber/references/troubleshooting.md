# Troubleshooting Guide — Voice Transcriber

Common issues and how to fix them.

## Installation Issues

### `whisper` module not found
```bash
pip install openai-whisper
```
If that fails, try:
```bash
pip install git+https://github.com/openai/whisper.git
```

### `ffmpeg` not found
- **Windows**: Download from https://ffmpeg.org/download.html and add to PATH.
- **macOS**: `brew install ffmpeg`
- **Linux**: `apt install ffmpeg` (Ubuntu/Debian) or `yum install ffmpeg` (CentOS)

### Python version issues
Whisper requires Python 3.8+. Check:
```bash
python3 --version
```

## Transcription Errors

### `RuntimeError: CPU not supported` (Apple Silicon)
Use the ARM64 version of Python or install Rosetta 2.

### `HTTPError 429` (Deepgram rate limit)
You’ve hit the API rate limit. Wait a minute and retry, or switch to local Whisper:
```bash
python3 scripts/transcribe.py --file audio.wav --provider whisper
```

### `DEEPGRAM_API_KEY not set`
Set the environment variable:
```bash
export DEEPGRAM_API_KEY="your_key_here"
```
On Windows (PowerShell):
```powershell
$env:DEEPGRAM_API_KEY="your_key_here"
```

### Whisper model download fails
Manually download the model file and place it in `~/.cache/whisper/`:
- tiny: `tiny.pt`
- base: `base.pt`
- small: `small.pt`
- medium: `medium.pt`
- large: `large-v3.pt`

URL format: `https://openaipublic.azureedge.net/main/whisper/models/<hash>/<model>.pt`

## Audio/Format Issues

### `Invalid data found when processing input` (ffmpeg)
The file might be corrupted or in an unsupported format. Try converting first:
```bash
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 output.wav
```

### Transcript is empty
- Check if audio file has actual speech (not silence).
- Try a larger Whisper model:
  ```bash
  python3 scripts/transcribe.py --file audio.wav --provider whisper --model medium
  ```
- For Deepgram, check API key permissions.

### Wrong language detected
Force the language:
```bash
python3 scripts/transcribe.py --file audio.wav --provider whisper --language en
```

## Long Audio Problems

### Memory error / crash on large files
Split the file first:
```bash
python3 scripts/transcribe.py --file long.wav --provider whisper --split
```

### Transcript chunks out of order
This can happen with parallel processing. Our script processes sequentially, but if you manually split, ensure filenames sort correctly (`chunk_001.mp3`, `chunk_002.mp3`, …).

## Permission Issues

### Cannot write to output directory
```bash
# Create directory with proper permissions
mkdir -p ~/voice-transcriber/transcripts
chmod 755 ~/voice-transcriber/transcripts
```

### Script not executable (Linux/macOS)
```bash
chmod +x scripts/transcribe.py
```

## Getting Help

1. Check `whisper` GitHub issues: https://github.com/openai/whisper/issues
2. Deepgram docs: https://developers.deepgram.com/docs
3. OpenClaw skill support: `clawhub inspect voice-transcriber`
4. Run script with `--help` to see all options:
   ```bash
   python3 scripts/transcribe.py --help
   ```
