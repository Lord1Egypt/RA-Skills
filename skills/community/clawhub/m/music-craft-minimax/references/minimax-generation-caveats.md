# MiniMax Generation Caveats

Execution constraints and known behaviors that affect how MiniMax generations are run and delivered. Load this reference before multi-output or long-duration MiniMax workflows.

## Sequential runs only

MiniMax generation is not re-entrant from the same working directory. Run one generation to completion before starting the next. Parallel or overlapping invocations risk output collisions or silent failures.

**Rule:** never launch a second `mmx music generate` (or `generate_with_retry.py`) while one is still running in the same session.

## Output-file handling

The `mmx music generate --out` flag is mandatory when using
`generate_with_retry.py --output-path`. The wrapper output path is a preservation
and verification destination; it does not replace the CLI's `--out` argument.
The CLI may still write to a different internal path and rely on the caller to
move the file, so do not assume the file appears at the requested path without
verification.

In the 2026-06-12 field run, 6/18 cloud jobs ended with SIGTERM/SIGKILL after
the MP3 had already been saved. Treat the file as the source of truth:

1. Check that the expected file exists.
2. Check file size is non-zero and plausibly above 100 KB.
3. Run `ffprobe` to verify duration and format.
4. Rerun only when the file is missing or invalid.

**Safe pattern — always verify after each run:**

```bash
# Use a wrapper that moves the file to the requested output path after success
python3 scripts/generate_with_retry.py \
  --output-path "$target_dir/M1_song.mp3" \
  -- music generate --prompt "..." --model music-2.6 --out "$target_dir/M1_song.mp3"

# Verify the file exists where expected before proceeding
test -f "$target_dir/M1_song.mp3" || {
  echo "ERROR: output not found at $target_dir/M1_song.mp3"
  exit 1
}
```

If calling `mmx` directly without a wrapper, check the CLI stdout for the `saved:` line and move the file accordingly.

If the process exits non-zero but the expected output is fresh and passes
verification, accept the file and record the signal as a transport/session
caveat rather than a generation failure. The retry wrapper promotes signal
recoveries after `ffprobe` can read a positive duration, or after a minimal MP3
header check when `ffprobe` is unavailable.

## Duration is a target, not a guarantee

`--length` (milliseconds) is a hint, not a contract. Observed behavior:

- In the 2026-06-12 field run, cloud outputs ranged from **57-135%** of the requested duration.
- 12/18 were truncated below 90% of requested duration.
- 3/18 were close, within 90-110% of requested duration.
- 3/18 were extended above 110% of requested duration.
- Cloud can undershoot and overshoot; do not frame the risk as truncation only.
- The `music-2.6` model is the right choice for vocal quality; `ACE-Step` is the right choice when exact duration is a hard requirement.

**Before generation:** warn the user if the prompt is lyric-heavy and the requested length exceeds ~150s.

**After generation:** always check the actual duration with `ffprobe` or equivalent and report it to the user.

### Local vs Cloud Duration Data

Verified 2026-06-12 paired run:

| Requested | Local ACE-Step | MiniMax cloud examples |
|---|---|---|
| 159 s | 159.000 s | 97.0 s (61%), 139.3 s (88%) |
| 170 s | 170.000 s | 165.7 s (97%), 194.4 s (114%), 169.9 s (100%), 154.6 s (91%) |
| 187 s | 187.000 s | 252.8 s (135%), 224.9 s (120%) |
| 195 s | 195.000 s | 204.8 s (105%), 146.0 s (75%) |
| 200 s | 200.000 s | 125.9 s (63%), 138.9 s (69%) |
| 239 s | 239.000 s | 182.9 s (77%), 205.0 s (86%) |
| 302 s | 302.000 s | 195.6 s (65%), 171.8 s (57%) |

Summary: use local ACE-Step when duration is a hard requirement. Use MiniMax
when fast iteration, cover/mashup workflows, lyrics API, or exact `mmx` flags
matter more than final duration.

## Prompt Budget

Keep standard cloud prompts under about 500 characters when possible. Longer
prompts still work below the hard byte limit, but the field run found that
shorter prompts were less likely to run into shell termination friction.

For compact patterns, see [`short-prompt-recipes.md`](short-prompt-recipes.md).

## References Flag

Treat `--references` as optional. During batch work, inline concise references
inside the prompt text instead of depending on a separate flag:

```text
Heavy cinematic post-rock in the spirit of Mogwai and Russian Circles...
```

If `--references` works in a single run, it is fine to use. If jobs are getting
killed or timing out, remove the flag and inline the reference.

## Output Format

Observed MiniMax cloud outputs in the 2026-06-12 run were:

- MP3
- stereo
- 44.1 kHz
- about 256 kbps

There are no documented `mmx music generate` flags for FLAC, 48 kHz, or bitrate
selection.

## Batch, Preview, And Quota

- No documented `mmx music batch` mode exists. Run versions sequentially.
- No documented low-cost preview/draft mode exists.
- If the CLI does not expose usage/quota, check the MiniMax web dashboard before
  large batches.

## Delivery caveats to report

When delivering MiniMax output, include these caveats in the delivery note:

| Caveat | What to say |
|---|---|
| Duration variance | "MiniMax output length is approximate. Actual duration was X:XX vs requested Y:YY." |
| Sequential only | "Multiple versions were generated sequentially; parallel generation was not attempted." |
| Output path verified | "Output file was verified to exist at the requested path before delivery." |
| Short lyric-heavy output | "This lyric-heavy prompt returned a shorter-than-requested track (~120-150s). If exact3:00+ length is needed, a re-gen with a shorter structure or a switch to ACE-Step is recommended." |

Keep delivery notes factual and machine-independent. Do not reference internal temp paths or machine-specific directories.
