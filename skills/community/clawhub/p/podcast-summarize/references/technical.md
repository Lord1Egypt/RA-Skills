# Podcast Summarize - Technical Reference

## Dependencies

### Required Tools
- `ffmpeg` - Audio conversion and processing (installed at /usr/bin/ffmpeg)
- `yt-dlp` - YouTube/audio extraction (need to install)
- `whisper` - Transcription (need to install)

### Installation Commands

```bash
# Install yt-dlp
pip install yt-dlp

# Install Whisper
pip install openai-whisper

# Or use the CLI version
pip install whisper
```

## Supported Formats

### Input Audio
- MP3, M4A, WAV, OGG, FLAC
- YouTube videos (via yt-dlp)
- Direct URL links

### Transcription
- whisper.cpp (local, fast)
- OpenAI Whisper API (accurate)
- HuggingFace Transformers (offline option)

## API Keys (if needed)

### OpenAI Whisper API
- Set OPENAI_API_KEY environment variable
- Or use local whisper.cpp for offline

## Output Formats

### Summary Structure
1. Title & Metadata
2. Key Points (3-5 bullets)
3. Detailed Summary (2-3 paragraphs)
4. Actionable Insights
5. Timestamps for key moments

### Optional Additions
- Guest/Host information
- Episode highlights
- Quotes from episode
- Related resources mentioned
- Follow-up episode suggestions
