# Wait And Collect

Operational workflow for local ACE-Step batches where each song gets multiple
versions, such as M1 faithful/local-best and M2 local-contrast.

## Rule

Run local ACE-Step jobs sequentially:

1. Submit M1 and capture `TASK_ID`.
2. Watch the server log until the saved-audio line appears.
3. Copy or move the new MP3 files out of the cache directory.
4. Verify file size and duration.
5. Submit M2 only after M1 collection is finished.

The API can queue work, but the practical operator pattern is one job at a
time. It avoids ambiguous cache files and makes duration verification cheaper.

## Watch Progress

`GET /v1/stats` is useful only for top-level state such as queued/running counts.
It does not expose LM, DiT, or VAE sub-stage progress. For long local jobs, the
server log is the source of truth:

```bash
tail -f /tmp/acestep-api.log
```

Useful progress markers include DiT diffusion counters, CFG batch generation,
VAE decode, and saved-audio lines.

If `scripts/wait_for_acestep.py` is available, use it as the default wait helper:

```bash
python3 scripts/wait_for_acestep.py "$TASK_ID" \
  --api-url http://127.0.0.1:8001 \
  --cache-dir "${ACE_STEP_PATH:-$HOME/ACE-Step-1.5}/.cache/acestep/tmp/api_audio" \
  --poll-seconds 10 \
  --timeout-seconds 3600
```

The helper treats empty `/query_result` data as pending and also watches the
cache for newly written audio files. This avoids falsely classifying a running
job as failed.

## Find New Cache Files

ACE-Step writes generated audio under the API cache directory inside the
ACE-Step checkout:

```bash
find "${ACE_STEP_PATH:-$HOME/ACE-Step-1.5}/.cache/acestep/tmp/api_audio" \
  -type f -name '*.mp3' -mmin -30 -ls
```

If the local install lives somewhere else, use the `ACE_STEP_PATH` chosen during
pre-flight. Do not hardcode a user-specific path in published guidance.

## Verify Duration

```bash
ffprobe -v error \
  -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  "$output_file"
```

For exact-duration work, compare this value against the requested
`audio_duration`. Local ACE-Step should hit the requested duration exactly; if
it does not, record the discrepancy and inspect the server log before retrying.

## Cache Hygiene

The cache directory grows over time. Clean old files deliberately:

```bash
find "${ACE_STEP_PATH:-$HOME/ACE-Step-1.5}/.cache/acestep/tmp/api_audio" \
  -type f -name '*.mp3' -mtime +7 -print
```

Review the printed files first. To delete after review, replace `-print` with
`-delete`.

## No Cancel Endpoint

There is no documented cancel endpoint for a queued or running ACE-Step job.
Lint the prompt and lyrics before submitting long jobs, especially anything
over three minutes.

## Wall-Time Planning

Observed 2026-06-12 local run on Apple Silicon M3, 24 GB, standard tier,
`inference_steps: 8`:

| Requested duration | Typical wall time |
|---|---|
| 159-200 s | about 9-10 min |
| 239 s | about 12 min |
| 302 s | about 14-15 min |

Use this as a planning estimate, not a universal benchmark. Hardware, model
tier, timeout settings, and system load can change the timings.
