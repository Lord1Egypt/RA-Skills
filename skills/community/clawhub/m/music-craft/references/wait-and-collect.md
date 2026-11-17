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

Add `--expected-seconds <audio_duration>` for any exact-duration job. The helper
treats empty `/query_result` data as pending, watches the cache for newly
written audio files, and with `--expected-seconds` only accepts a file whose
measured length (via `ffprobe`) is within `--tolerance` seconds (default 2) of
the request. Shorter in-progress files are reported under `rejected`. If
`ffprobe` is not installed it returns `succeeded_unverified`; measure the file
yourself before delivering it. The helper only accepts a loopback `--api-url`.

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

## Long Jobs: Recover, Do Not Re-fire

Field lessons from long local runs (requests of about 370 s and more, Apple
Silicon, 2026-08 to 2026-09). The server writes completed takes to the cache
whatever happens to the client, so a failure on the client side rarely means
the generation failed.

| Symptom | What it usually means | Do this |
|---|---|---|
| Delivered file is shorter than requested (e.g. 295 s for 371 s) | The API surfaced an in-progress intermediate | Reject it; keep waiting with `--expected-seconds` |
| Client hangs for a long time, or exits with a transient error, or leaves a 0-byte output | The server may already have saved the take | Check the cache before anything else (below) |
| Diffusion finished in the log but nothing is saved after ~15 min | Stuck in the tiled VAE decode | Restart the server and submit once more |
| `Connection refused`; log ends with an MPS `MTLCommandBuffer` assertion | The server crashed mid-diffusion | Restart the server (models reload on first request, about 2 min) and submit once more |
| Takes for long beds disappear at the 600 s mark | Server task timeout | Start the server with a larger `ACESTEP_GENERATION_TIMEOUT` (for example 5400) for anything over ~4 min |

Check the cache for a finished take:

```bash
python3 scripts/wait_for_acestep.py --scan-only \
  --cache-dir "${ACE_STEP_PATH:-$HOME/ACE-Step-1.5}/.cache/acestep/tmp/api_audio" \
  --expected-seconds <audio_duration>
```

Decision:

1. Submit a long job **once**.
2. If the client hangs or fails, run the scan above before resubmitting.
3. `found` → copy that take out of the cache, record the cache filename and why it was chosen next to the output, then verify it as usual.
4. `not_found` and the server log shows the job still running → keep waiting; do not submit a duplicate.
5. `not_found` and the server is stuck or dead → restart it and submit once more.

## Check The Start And End

A take can end in a fade: the last seconds drop below about −35 dB, which
leaves silence under the end of a mix. Listen to, or measure, the first and
last 10 seconds. To fix a fading end without regenerating, splice material from
the middle of the same take over the end with a crossfade. Example for a 435 s
take whose audible content stops around 427 s (415 + 25 − 5 = 435 s):

```bash
ffmpeg -i take.mp3 -filter_complex \
  "[0:a]atrim=0:415,asetpts=PTS-STARTPTS[a];[0:a]atrim=150:175,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=5:c1=tri:c2=tri[out]" \
  -map "[out]" -c:a libmp3lame -q:a 2 take-tailspliced.mp3
```

Write the result to a new file and note the splice next to it. A quiet opening
is fine under narration, but check it if the music plays alone.

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
