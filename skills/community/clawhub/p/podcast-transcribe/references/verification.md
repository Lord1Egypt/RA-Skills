# Verification

Use a small public sample for low-cost verification:

```text
https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3
```

## Smoke Test

```bash
npx podcast-helper transcribe https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3 --output-dir ./out/smoke --json
```

## What to Verify

- the command exits successfully
- the success envelope includes `audio`, `srt`, and `txt` artifact paths
- the `.txt` transcript is non-empty
- the `.srt` file contains timestamped subtitle blocks

## Local Runtime Debugging

If local `mlx-whisper` is failing:

```bash
podcast-helper doctor
podcast-helper setup mlx-whisper
```

When debugging progress or chunking behavior, rerun with `--progress jsonl`.
