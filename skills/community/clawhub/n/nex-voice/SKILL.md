---
name: nex-voice
description: Voice note transcription and intelligent action item extraction for capture and organization of verbal communication. Record and transcribe voice notes, voice messages, and meeting recordings in Dutch and English using OpenAI Whisper with selectable model quality (tiny to large). Automatically extract structured action items from transcripts including tasks (moet, must), reminders (vergeet niet, don't forget), scheduled calls, email actions, meetings (afspraken), decisions, and deadline-based items. Full-text search across all transcripts to find past conversations and action items by keyword. Manage extracted actions with completion tracking, priority levels, and due date assignment. View pending and overdue action items to stay on top of commitments. Optional LLM integration for intelligent action extraction and transcript summarization. Perfect for busy professionals, meeting attendees, and business owners who prefer speaking notes over typing and need to convert voice into organized action items and searchable records. All audio files and transcripts stay secure on your machine.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "🎤"
    requires:
      bins:
        - python3
        - whisper
        - ffmpeg
      env: []
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-voice.py"
      - "lib/*"
      - "setup.sh"
---

# Nex Voice

Voice note transcription and action item extraction. Automatically transcribe voice notes with OpenAI Whisper, extract action items (tasks, reminders, calls, meetings, decisions, deadlines), and manage them locally. Supports Dutch and English. All data stays on your machine.

## When to Use

Use this skill when the user asks about:

- Transcribing a voice note, voice message, or audio file
- Extracting action items from voice notes (tasks, reminders, calls, meetings)
- Searching through voice note transcripts
- Managing action items or tasks from voice notes
- What was discussed in a voice note or meeting recording
- Pending or overdue action items
- Statistics about voice notes and transcriptions
- Exporting transcripts

Trigger phrases: "transcribe", "voice note", "voice message", "audio file", "action item", "what did we discuss", "extract tasks", "pending tasks", "spraakbericht", "wat is besproken", "actie", "afspraak"

## Quick Setup

If this is your first time using nex-voice, run the setup script:

```bash
bash setup.sh
```

This checks for required dependencies (Whisper and FFmpeg), sets up the data directory at `~/.nex-voice`, initializes the database, and tests the installation.

## Available Commands

The CLI tool is `nex-voice`. All commands output plain text.

### Transcribe

Transcribe an audio file:

```bash
nex-voice transcribe /path/to/voice.ogg
nex-voice transcribe /path/to/voice.ogg --language en
nex-voice transcribe /path/to/voice.ogg --speaker "Kevin"
nex-voice transcribe /path/to/voice.ogg --tags "client-meeting,proposal"
```

Options:
- `--language`: Language code (en for English, nl for Dutch). Default: nl
- `--speaker`: Name of the speaker for attribution
- `--tags`: Comma-separated tags for organization

Returns: Recording ID and transcript summary.

### Extract Actions

Extract action items from a recording:

```bash
nex-voice actions 42
nex-voice actions --last
nex-voice actions 42 --use-llm
```

Options:
- Recording ID or `--last` for the most recent recording
- `--use-llm`: Use configured LLM for intelligent extraction (optional)

### List Recordings

List all recordings:

```bash
nex-voice list
nex-voice list --since 2026-03-01
nex-voice list --speaker "Kevin"
nex-voice list --tag "client-meeting"
```

### Show Recording

Show full details of a recording:

```bash
nex-voice show 42
```

Displays: transcript, summary, extracted actions, metadata.

### Search Transcripts

Full-text search across all transcripts:

```bash
nex-voice search "offerte"
nex-voice search "offerte" --since 2026-04-01
```

### Pending Actions

List all pending action items:

```bash
nex-voice pending
nex-voice pending --type task
nex-voice pending --type reminder
```

Types: task, reminder, call, email, meeting, decision, deadline

### Complete Action

Mark an action item as complete:

```bash
nex-voice complete 7
```

### Overdue Actions

Show overdue action items:

```bash
nex-voice overdue
```

### Export Transcript

Export a transcript:

```bash
nex-voice export 42 --format txt
nex-voice export 42 --format json
```

### Statistics

Show statistics:

```bash
nex-voice stats
```

Displays: total recordings, total hours transcribed, languages, action items extracted, pending/overdue counts.

### Configuration

View or set configuration:

```bash
nex-voice config show
nex-voice config set-whisper-model base
nex-voice config set-whisper-model large
nex-voice config set-language nl
nex-voice config set-api-key
nex-voice config set-provider openai
nex-voice config set-model gpt-4o
nex-voice config set-api-base https://api.openai.com/v1
```

## Example Interactions

**User:** "Transcribe this voice note for me"
**Agent runs:** `nex-voice transcribe /path/to/file.ogg`
**Agent:** Shows recording ID and presents the transcript with extracted action items.

**User:** "What action items came from the last recording?"
**Agent runs:** `nex-voice actions --last`
**Agent:** Presents the extracted actions (tasks, reminders, calls, meetings, decisions, deadlines).

**User:** "Search my voice notes for anything about the proposal"
**Agent runs:** `nex-voice search "proposal"`
**Agent:** Lists matching transcripts and highlights relevant sections.

**User:** "What tasks are still pending from voice notes?"
**Agent runs:** `nex-voice pending --type task`
**Agent:** Shows all incomplete tasks with due dates and assignments.

**User:** "Mark task 7 as done"
**Agent runs:** `nex-voice complete 7`
**Agent:** Confirms completion and updates the database.

**User:** "Show me overdue actions"
**Agent runs:** `nex-voice overdue`
**Agent:** Lists all overdue items with their recordings and context.

## Output Parsing

All CLI output is plain text, structured for easy parsing:

- Section headers followed by `---` separators
- List items prefixed with `- `
- Timestamps in ISO-8601 format
- Action items include: ID, type, description, assigned_to, due_date, priority, status
- Every command output ends with `[Nex Voice by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally.

## Features

### Transcription
- Supports OGG, MP3, WAV, M4A, OPUS, WEBM formats
- Automatic audio conversion using ffmpeg if needed
- Language detection and support for Dutch (default) and English
- Whisper model selection (tiny, base, small, medium, large)
- Duration tracking and maximum 600-second audio limit

### Action Extraction
- Pattern-based extraction with Dutch and English keywords:
  - **Tasks**: "moet", "must", "do"
  - **Reminders**: "vergeet niet", "don't forget"
  - **Calls**: "bel", "call"
  - **Emails**: "mail", "stuur email", "send email"
  - **Meetings**: "afspraak", "meeting"
  - **Decisions**: "besloten", "decided"
  - **Deadlines**: "deadline", "voor", "by"
- Intelligent extraction with optional LLM (OpenAI, Claude, etc.)
- Automatic date parsing (morgen=tomorrow, vrijdag=Friday, etc.)
- Speaker and assignee detection

### Storage & Management
- Local SQLite database at `~/.nex-voice/`
- Full-text search across transcripts
- Tag-based organization
- Speaker attribution
- Completion tracking with timestamps

### Optional LLM Features
- Intelligent action extraction from transcripts
- Summary generation
- Requires explicit configuration: API key, provider, model
- Supported providers: OpenAI, Anthropic Claude, local LLMs

## Important Notes

- All voice data is stored locally at `~/.nex-voice/`. No telemetry, no analytics.
- No external API calls are made unless you explicitly configure an LLM provider.
- Whisper CLI must be installed (pip install openai-whisper or faster-whisper).
- FFmpeg must be installed for audio format conversion.
- Maximum audio duration: 600 seconds (10 minutes). Longer files are rejected.
- LLM features are optional and require explicit configuration.
- Supported audio formats: OGG, MP3, WAV, M4A, OPUS, WEBM

## Troubleshooting

- **"whisper: command not found"**: Install with `pip install openai-whisper`
- **"ffmpeg: command not found"**: Install FFmpeg from ffmpeg.org
- **"Database not found"**: Run `bash setup.sh` to initialize
- **"No transcripts found"**: Run `nex-voice list` to see all recordings
- **"LLM not configured"**: Run `nex-voice config set-api-key` to enable LLM features

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor
