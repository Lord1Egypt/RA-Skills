---
name: otterai-cli
description: Use when the user mentions Otter, Otter.ai, or wants to find, search, download, export, or manage meeting notes, transcripts, recordings, or audio from calls, standups, syncs, or interviews.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - otter
      env:
        - OTTERAI_USERNAME
        - OTTERAI_PASSWORD
    install: uv tool install otterai-cli
---

# Otter.ai CLI

CLI for interacting with Otter.ai meeting notes and transcripts via the `otter` command.

## Prerequisites

Install with:
```bash
uv tool install otterai-cli
```

Upgrade with:
```bash
uv tool upgrade otterai-cli
```

Authenticate with:
```bash
otter login
```

Credentials are stored in your OS keychain via keyring, with `~/.otterai/config.json` as fallback.

You can also use environment variables (`OTTERAI_USERNAME`, `OTTERAI_PASSWORD`), which take highest precedence.

## Commands

### Speeches (Meeting Notes)

```bash
otter speeches list                          # list all speeches
otter speeches list --days 7                 # last 7 days
otter speeches list --folder "Work"          # by folder name (case-insensitive)
otter speeches list --folder 123456          # by folder ID
otter speeches list --page-size 10           # limit results
otter speeches list --source owned           # only owned speeches (default)
otter speeches list --source shared          # only shared speeches
otter speeches list --source all             # all speeches
otter speeches list --json                   # JSON output

otter speeches get SPEECH_ID                 # get speech details + full transcript
otter speeches get SPEECH_ID --json

otter speeches search "keyword" SPEECH_ID    # search within a speech
otter speeches search "keyword" SPEECH_ID --size 100

otter speeches download SPEECH_ID -f txt     # formats: txt, pdf, mp3, docx, srt, md
otter speeches download SPEECH_ID -f pdf -o my_file
otter speeches download SPEECH_ID -f md      # markdown (generated locally from transcript data)
otter speeches download SPEECH_ID -f md -o meeting-notes
otter speeches download SPEECH_ID -f md --frontmatter-fields "title,summary,speakers"
otter speeches download SPEECH_ID -f md --frontmatter-fields none

otter speeches upload recording.mp4          # upload audio for transcription

otter speeches rename SPEECH_ID "New Title"
otter speeches trash SPEECH_ID               # move to trash
otter speeches trash SPEECH_ID --yes         # skip confirmation

otter speeches move SPEECH_ID --folder "Work"
otter speeches move ID1 ID2 ID3 --folder "Work"
otter speeches move SPEECH_ID --folder "New Folder" --create  # auto-create folder
```

### Speakers

```bash
otter speakers list
otter speakers list --json
otter speakers create "Speaker Name"
otter speakers tag SPEECH_ID SPEAKER_ID          # list segments, then tag
otter speakers tag SPEECH_ID SPEAKER_ID -t UUID  # tag specific segment
otter speakers tag SPEECH_ID SPEAKER_ID --all    # tag all segments
```

### Folders

```bash
otter folders list
otter folders list --json
otter folders create "My Folder"
otter folders create "My Folder" --json
otter folders rename FOLDER_ID "New Name"
```

### Groups

```bash
otter groups list
otter groups list --json
```

### Auth & Config

```bash
otter login                  # authenticate (saves to keyring)
otter user                   # show current user
otter logout                 # clear credentials
otter config show            # show config
otter config clear           # clear config
```

## Important: Speech IDs

Otter.ai speeches have two identifiers:
- **`speech_id`** (e.g. `7KR9X3VNPLQ8JTMS`) -- internal ID, does NOT work with API
- **`otid`** (e.g. `Xp4mRtK9wLs2vNcQjY7hBfA3eZd`) -- used in all CLI commands

All CLI commands expect the **otid**. Use `otter speeches list` to find them, or:
```bash
otter speeches list --json | jq '.speeches[].otid'
```

## Markdown Frontmatter

When downloading as `md`, YAML frontmatter is included by default. Customize with `--frontmatter-fields`:

```bash
# Use defaults
otter speeches download SPEECH_ID -f md

# Pick specific fields
otter speeches download SPEECH_ID -f md --frontmatter-fields "title,speech_id,summary"

# Disable frontmatter
otter speeches download SPEECH_ID -f md --frontmatter-fields none
```

Default fields: title, summary, speakers, start_time, end_time, duration_seconds, source, speech_id, folder, folder_id

All available fields: title, summary, speakers, start_time, end_time, duration_seconds, source, speech_id, folder, folder_id, otid, created_at, transcript_updated_at, language, transcript_count, process_status

Note: `speech_id` in frontmatter is the Otter internal speech_id; the `SPEECH_ID` argument in commands still expects the otid.

## Usage Examples

**List recent meetings:**
```bash
otter speeches list --days 7
```

**Get a transcript:**
```bash
otter speeches list --days 1           # find the speech ID
otter speeches get SPEECH_ID           # get full transcript
```

**Search for a topic across meetings:**
```bash
otter speeches list --days 30 --json   # find relevant speech IDs
otter speeches search "budget" SPEECH_ID
```

**Download as markdown:**
```bash
otter speeches list                    # find the speech ID
otter speeches download SPEECH_ID -f md
```

**Download as PDF:**
```bash
otter speeches list                    # find the speech ID
otter speeches download SPEECH_ID -f pdf
```

**Filter by folder:**
```bash
otter speeches list --folder "Work"
```

**Organize meetings into folders:**
```bash
otter folders create "Q1 Planning"
otter speeches move SPEECH_ID --folder "Q1 Planning"
```

**Upload a recording:**
```bash
otter speeches upload recording.mp4
```

## Notes

- Most commands support `--json` for machine-readable output. Prefer `--json` when you need to parse or extract specific data.
- When asked about a specific meeting, first list recent speeches to find the otid, then use `speeches get` to retrieve the transcript.
- For broad searches across meetings, list speeches first, then search within each relevant one.
- Download supports txt, pdf, mp3, docx, srt, and md formats. The `md` format is generated locally from transcript data and includes speaker labels with YAML frontmatter.
- Both `speeches list --folder` and `speeches move --folder` accept a **folder name** (case-insensitive) or a **numeric folder ID**. Use `otter folders list` to see available folders and their IDs.
- Use `-n` / `--page-size` to limit the number of results (not `--limit`).
- `--source` defaults to `owned`. Use `shared` or `all` to include shared speeches.
