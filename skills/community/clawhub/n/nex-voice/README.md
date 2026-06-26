# Nex Voice

**Voice Note Transcription & Action Item Extraction**

Automatically transcribe voice notes with OpenAI Whisper, extract action items (tasks, reminders, calls, meetings, decisions, deadlines), and manage them locally. Supports Dutch and English. All data stays on your machine.

## Features

- **Audio Transcription** - Convert voice notes to text using Whisper
- **Action Extraction** - Automatically identify tasks, reminders, calls, meetings, decisions, and deadlines
- **Multi-language Support** - Dutch (default) and English
- **Local Storage** - All data stored in `~/.nex-voice/`, no cloud uploads
- **Full-text Search** - Search across all transcripts
- **Action Management** - Track, complete, and manage action items
- **Optional LLM Integration** - Use AI for smarter action extraction (optional)
- **Export** - Export transcripts as text or JSON

## Quick Start

### Installation

1. Ensure Python 3.9+ is installed
2. Install dependencies:
   ```bash
   pip install openai-whisper
   # or for faster alternative:
   pip install faster-whisper
   ```
3. Install FFmpeg:
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: `scoop install ffmpeg` or `choco install ffmpeg`

4. Run setup:
   ```bash
   bash setup.sh
   ```

### First Transcription

```bash
nex-voice transcribe /path/to/voice.ogg
```

This will:
1. Transcribe the audio file
2. Extract action items automatically
3. Store everything in the local database
4. Display results in your terminal

## Commands

### Transcribe
```bash
nex-voice transcribe /path/to/audio.ogg
nex-voice transcribe /path/to/audio.ogg --language en --speaker "Kevin"
```

### List Recordings
```bash
nex-voice list
nex-voice list --since 2026-04-01 --speaker "Kevin"
```

### Show Details
```bash
nex-voice show 42
```

### Search
```bash
nex-voice search "proposal"
```

### Extract Actions
```bash
nex-voice actions --last
nex-voice actions 42
```

### Manage Actions
```bash
nex-voice pending              # List pending actions
nex-voice overdue              # List overdue actions
nex-voice complete 7           # Mark action 7 as complete
```

### Export
```bash
nex-voice export 42 --format txt
nex-voice export 42 --format json --output transcript.json
```

### Statistics
```bash
nex-voice stats
```

### Configuration
```bash
nex-voice config show
nex-voice config set-whisper-model large
nex-voice config set-whisper-language en
nex-voice config set-api-key  # For LLM features
```

## Supported Audio Formats

- OGG
- MP3
- WAV
- M4A
- OPUS
- WEBM

## Action Extraction

The skill automatically recognizes these patterns:

### Dutch Examples
- "Moet nog de offerte sturen naar Bakkerij Peeters" → Task
- "Vergeet niet: demo met ECHO Management donderdag 14u" → Reminder
- "Besloten: we gaan voor het premium pakket" → Decision
- "Bel Silvia morgen terug" → Call
- "Deadline proposal vrijdag" → Deadline

### English Examples
- "Kevin said he'll send the quote by Friday" → Task
- "Don't forget: meeting with John tomorrow" → Reminder
- "We decided to go with the premium package" → Decision
- "Call Sarah tomorrow" → Call

## Configuration

All settings are stored in `~/.nex-voice/config.json`:

```json
{
  "whisper_model": "base",
  "whisper_language": "nl",
  "api_key": "your-api-key",
  "api_base": "https://api.openai.com/v1",
  "api_model": "gpt-4o"
}
```

### Whisper Models

- **tiny** - Fastest, least accurate (39M)
- **base** - Good balance (140M) - Default
- **small** - Better accuracy (244M)
- **medium** - High accuracy (769M)
- **large** - Highest accuracy (1.5B)

Larger models are slower but more accurate.

## Optional: LLM Integration

For intelligent action extraction with Claude, OpenAI, or other LLMs:

```bash
nex-voice config set-api-key
# Enter your API key
nex-voice config set-api-model gpt-4o
# Or: claude-opus-4-1, your-local-model, etc.
```

Then use LLM extraction:
```bash
nex-voice actions --last --use-llm
```

## Data Storage

All data is stored locally at `~/.nex-voice/`:

```
~/.nex-voice/
├── nex_voice.db          # SQLite database
├── config.json           # Configuration
├── recordings/           # Audio files
└── exports/              # Exported transcripts
```

No data is sent to external servers unless you explicitly configure LLM features.

## Troubleshooting

### "whisper: command not found"
```bash
pip install openai-whisper
# or
pip install faster-whisper
```

### "ffmpeg: command not found"
Install FFmpeg from https://ffmpeg.org

### "Database not found"
```bash
bash setup.sh
```

### "No results found for: X"
Try:
```bash
nex-voice list
nex-voice stats
```

## Requirements

- Python 3.9+
- OpenAI Whisper or Faster Whisper
- FFmpeg
- SQLite3 (included with Python)

## License

MIT-0 License - See LICENSE.txt

## Built by Nex AI

[nex-ai.be](https://nex-ai.be) - Digital transformation for Belgian SMEs

Author: Kevin Blancaflor
