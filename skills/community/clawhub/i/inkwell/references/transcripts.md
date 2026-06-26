# Transcript Verification System

A two-layer approach for voice note accuracy: inline echo for immediate verification, local storage for reference.

## Table of Contents

- [Why Verify Transcripts](#why-verify-transcripts)
- [Layer 1: Inline Echo](#layer-1-inline-echo)
- [Layer 2: Local Storage](#layer-2-local-storage)
- [Setup Instructions](#setup-instructions)
- [File Format](#file-format)

## Why Verify Transcripts

Voice-to-text transcription is imperfect. Names, technical terms, and context-dependent phrases are often misheard. Without verification:
- Decisions get recorded incorrectly
- Action items get wrong details
- Knowledge base accumulates errors over time

The two-layer approach catches errors early and creates an audit trail.

## Layer 1: Inline Echo

When receiving a voice note, immediately echo the raw transcript back so the human can verify:

**Format:**
```
> [Raw transcript text displayed in blockquote]

[Your response based on the transcript]
```

**Example:**
```
> Hey Vesper, can you check if the Stripe webhook is configured for the
> new endpoint at api dot example dot com slash hooks

Checking the Stripe webhook configuration for api.example.com/hooks...
```

The human sees what was transcribed and can correct errors before you act on bad data.

### When to Echo

- **Always echo** voice notes that contain: names, URLs, numbers, technical terms, commands
- **Skip echo** for simple conversational messages where intent is obvious ("hey, what's up?")
- **When in doubt, echo** — it's cheap and prevents costly mistakes

## Layer 2: Local Storage

Store transcripts locally for reference, debugging, and pattern analysis.

**Location:** `transcripts/` directory in workspace root (created by the setup script).

**Important:** Transcripts are gitignored and must never be committed to version control. They may contain sensitive voice data.

### Storage Rules

- One file per day: `YYYY-MM-DD.md`
- Append-only within a day (never overwrite)
- Include timestamp, source channel, and raw text
- Optionally include confidence indicators or correction notes

## Setup Instructions

Add the following guidance to your AGENTS.md or system prompt:

```markdown
### Voice Transcript Handling

When receiving voice notes:
1. **Echo the transcript** in a blockquote before responding
2. **Store the transcript** in `transcripts/YYYY-MM-DD.md` with timestamp
3. **Note corrections** if the human corrects the transcript

Format for storage:
- File: `transcripts/YYYY-MM-DD.md`
- Each entry: timestamp, channel, raw text, any corrections
```

The setup script creates the `transcripts/` directory with a `.gitignore` that excludes all files except the `.gitignore` itself.

## File Format

### Daily Transcript File (`transcripts/YYYY-MM-DD.md`)

```markdown
# Transcripts — 2026-04-07

## 14:32 UTC — Telegram Voice
> Hey Vesper, schedule a meeting with the API team for Thursday at 2 PM.

## 15:10 UTC — Discord Voice
> Can you check the deployment status of the auth service?
**Correction:** Human clarified "auth service" = "oauth-proxy" service specifically.

## 16:45 UTC — Telegram Voice
> Move the stripe integration project to archive, we decided to use LemonSqueezy instead.
```

### Key Elements

| Element | Purpose |
|---------|---------|
| Timestamp | When the voice note was received |
| Channel | Which platform it came from |
| Blockquote | The raw transcript text |
| Correction | Human-provided fixes (optional) |

## Maintenance

- Transcripts accumulate over time. Periodically review and delete old files (30+ days).
- If transcription quality degrades, check the audio provider configuration.
- Patterns of frequent corrections indicate terms to watch for (names, jargon, etc.).
