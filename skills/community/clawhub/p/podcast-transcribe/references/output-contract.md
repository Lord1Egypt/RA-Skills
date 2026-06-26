# Output Contract

Prefer machine-readable output:

```bash
npx podcast-helper transcribe <input> --output-dir <dir> --json
```

Add `--progress jsonl` when you want machine-readable progress events and terminal failure events on `stderr`.

## Artifacts

The command writes:

- the original audio file
- a `.srt` subtitle file
- a `.txt` transcript file

Always report these artifact paths back to the user.

## Success Envelope

```json
{
  "ok": true,
  "command": "transcribe",
  "input": "https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3",
  "source": "remote-audio-url",
  "language": "eng",
  "artifacts": {
    "audio": "/abs/path/nicole.mp3",
    "srt": "/abs/path/nicole.srt",
    "txt": "/abs/path/nicole.txt"
  }
}
```

## Failure Envelope

```json
{
  "ok": false,
  "command": "transcribe",
  "error": {
    "code": "SOURCE_RESOLUTION_FAILED",
    "category": "source",
    "message": "Could not extract podcast audio from the provided page.",
    "hints": [
      "Pass the original episode page URL, a direct audio URL, or a local audio file.",
      "If this site hides audio metadata, download the audio separately and rerun `transcribe` with the file path."
    ]
  }
}
```

## Operational Notes

- Progress logs are emitted on `stderr`.
- Final success payloads are emitted as JSON on `stdout`.
- Structured failures are emitted as JSON on `stderr`.
- The local workflow uses a request-scoped temp workspace and cleans it up unless `--keep-temp` is set.
