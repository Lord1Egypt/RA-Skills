---
name: meeting-transcription
description: "Private local meeting transcription for OpenClaw: convert audio recordings into timestamped transcripts, SRT/VTT subtitles, and structured Markdown notes with deterministic action-item extraction. Use for meetings, interviews, calls, lectures, and voice notes when audio should remain local."
license: MIT-0
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins: ["python3"]
      pip: ["openai-whisper"]
    version: "0.1.0"
---
# Private local meeting transcription

Use `meeting.py` to transcribe a user-selected audio/video file with local Whisper and produce reusable transcript artifacts. The workflow does not call a cloud transcription API. Whisper model files may be downloaded the first time a model is used; disclose that setup network requirement and keep later processing local.

## Quick start

```bash
python3 meeting.py --input meeting.m4a --model base --output-dir meeting-output
```

This writes:

- `transcript.json` with transcript text, language, duration, and timestamped segments;
- `transcript.srt` with subtitle timing;
- `notes.md` with a readable transcript and deterministic action-item candidates.

## Formats and models

- Use `--format all` (default), `json`, `srt`, or `markdown`.
- Use Whisper models `tiny`, `base`, `small`, `medium`, `large`, or `turbo`.
- Use `--language en` when the language is known; omit it for automatic detection.
- Use `--include-word-timestamps` only when detailed timing is required; it costs more compute.

## Privacy and safety

- The input must resolve inside the current workspace; symlink escapes are rejected.
- Output is written only to the requested output directory inside the workspace.
- The script performs local transcription through Whisper and makes no runtime network request.
- Initial model acquisition can require network access through Whisper's normal model cache. Use a pre-downloaded model in restricted environments.
- Do not place confidential recordings, credentials, or private transcripts in public issue reports.

## Agent workflow

1. Confirm the user has permission to process the recording.
2. Check local capacity before large jobs with the Local System Info skill.
3. Choose `base` for a practical default; use `small` or larger when accuracy matters and resources allow.
4. Run the script and inspect `transcript.json` before summarizing.
5. Cite timestamps when extracting decisions or action items.

## Example

```bash
python3 meeting.py \
  --input interview.wav \
  --model small \
  --language en \
  --output-dir interview-output \
  --format all
```

Source: https://github.com/iyeque/openclaw-skills/tree/main/skills/meeting-transcription

Report bugs and security concerns through the repository issue guidance.
