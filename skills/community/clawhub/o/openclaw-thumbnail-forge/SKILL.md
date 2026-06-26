---
name: openclaw-thumbnail-forge
description: Local thumbnail generator for videos. Picks the best candidate frames using brightness, sharpness, and scene-change scores, composes professional thumbnails with text overlays, gradient bars, and watermarks, and ranks A/B variants on objective click-likelihood metrics. Exports at YouTube, Shorts, Instagram, X, and LinkedIn sizes. Pure ffmpeg + Pillow, no AI APIs, no remote calls.
license: MIT
metadata: {"openclaw":{"requires":{"bins":["ffmpeg","ffprobe","python3"]},"primaryEnv":null,"homepage":"https://clawhub.ai/gopendrasharma89-tech/openclaw-thumbnail-forge"}}
---

# openclaw-thumbnail-forge

v0.3.0

A practical thumbnail generator for videos. Builds the kind of professional-looking thumbnails creators normally make in Photoshop or Canva, but as a local CLI workflow with no API keys, no online services, and no AI dependencies.

## What this skill does

- `scripts/check_deps.sh` — verify `ffmpeg`, `ffprobe`, `python3` (and the `Pillow` Python package) are installed.
- `scripts/pick_frames.py` — extract candidate frames from a video and rank them by a composite score combining sharpness, brightness, contrast, and ffmpeg scene-change scores. Outputs the top-N frames as PNG files plus a JSON report.
- `scripts/compose_thumbnail.py` — turn one source frame into a finished thumbnail with bold title text, subtitle, gradient bar, optional logo overlay, and auto contrast boost. Supports custom fonts and color schemes.
- `scripts/export_sizes.py` — re-export a finished thumbnail to all common platform sizes in one command (YouTube, Shorts, Instagram square, X/Twitter, LinkedIn).
- `scripts/make_variants.py` — generate four A/B-testable variants of the same thumbnail (different color schemes, text placements, contrast levels) for split-testing. NEW in v0.3.0: pass `--auto-pick` to immediately score the four variants with `score_thumbnail.py`, copy the winner to `<output_dir>/winner.png`, and write a `winner.json` with the full ranking. One command, one decision.
- `scripts/score_thumbnail.py` (NEW in v0.2.0) — score one or more finished thumbnails on six objective visual metrics and pick the most likely click-winner. Gives a numeric click-likelihood score (0-100) per thumbnail and an explanation of which metrics drove the result.

## What this skill does not do

To set expectations honestly:

- It does not use AI subject detection or face recognition. Frame ranking and click-likelihood scoring are statistical, not semantic.
- It does not download fonts, stock photos, or any remote asset. You provide your own font path or use the system default.
- It does not perform OCR, transcription, or generative editing.
- It does not write outside the directory you provide.
- The click-likelihood scorer is a deterministic heuristic, not a real ML CTR model. It captures widely-cited thumbnail design rules (punch, focal pop, color punch, text band, brightness, edge density). Treat its output as a tie-breaker, not a guarantee.

## Required dependencies

```bash
bash scripts/check_deps.sh
```

Verifies `ffmpeg`, `ffprobe`, `python3`, and that `PIL` (Pillow) is importable. Pillow is the only Python dependency:

```bash
pip install Pillow
```

## Workflows

### 1. Pick the best candidate frames from a video

```bash
python3 scripts/pick_frames.py input.mp4 ./frames/ \
  --top 10 --interval 2.0
```

Extracts a frame every 2 seconds, scores each one, and writes the top 10 as `frames/frame_001.png` through `frames/frame_010.png` plus a `frames/report.json` with per-frame scores.

Tunable flags:
- `--interval <seconds>` — sampling interval (default 2.0)
- `--top <N>` — how many top frames to keep (default 10)
- `--min-brightness <0-255>` / `--max-brightness <0-255>` — reject frames that are too dark or blown out
- `--min-sharpness <float>` — reject blurry frames
- `--relax-on-empty` (NEW in v0.2.0) — if no frame passes the filters (very short clip, very dark video, single-subject still), retry once with very loose thresholds so you still get at least one candidate

For a video shorter than `2 * interval`, the script now automatically falls back to 3 evenly-spaced samples instead of returning zero candidates.

### 2. Compose a finished thumbnail from a frame

```bash
python3 scripts/compose_thumbnail.py frames/frame_003.png thumb.png \
  --title "10 ffmpeg Tricks I Wish I Knew Sooner" \
  --subtitle "A practical tour" \
  --color-scheme bold-yellow \
  --position bottom
```

Color schemes shipped: `bold-yellow`, `clean-white`, `red-alert`, `cool-blue`, `tech-green`. Each scheme defines title color, outline color, shadow, and gradient bar opacity.

Position options: `top`, `bottom`, `center`. The script auto-fits the title size to the available width and adds a readable gradient bar behind the text so the thumbnail reads at small sizes too.

Optional logo overlay:

```bash
python3 scripts/compose_thumbnail.py frames/frame_003.png thumb.png \
  --title "Your Title" \
  --logo logo.png --logo-corner top-right --logo-scale 0.12
```

In v0.2.0, the script now rejects an empty `--title ""` (instead of silently producing a textless thumbnail) and prints a clean error if the input image is corrupt or unreadable (instead of leaking a Python traceback).

### 3. Export to all platform sizes at once

```bash
python3 scripts/export_sizes.py thumb.png ./out/
```

Writes:
- `out/youtube_1280x720.png`
- `out/shorts_1080x1920.png`
- `out/instagram_1080x1080.png`
- `out/x_1200x675.png`
- `out/linkedin_1200x627.png`

### 4. Generate A/B variants

```bash
python3 scripts/make_variants.py frames/frame_003.png ./variants/ \
  --title "10 ffmpeg Tricks" \
  --subtitle "A practical tour"
```

Writes 4 variants with different color schemes and positions, ideal for click-rate split testing.

NEW in v0.3.0 — add `--auto-pick` to produce the variants AND immediately pick the winner in one command:

```bash
python3 scripts/make_variants.py frames/frame_003.png ./variants/ \
  --title "10 ffmpeg Tricks" \
  --subtitle "A practical tour" \
  --auto-pick
```

This writes the 4 variants plus a copy of the highest-scoring variant as `./variants/winner.png` and a `./variants/winner.json` with the full ranking. The original four `variant_*.png` files are preserved so you can still pick a different one if you disagree with the score.

### 5. Score finished thumbnails on click-likelihood (NEW in v0.2.0)

```bash
python3 scripts/score_thumbnail.py variants/*.png
```

Scores every thumbnail on six objective metrics and prints a ranked list with the winner highlighted:

| Sub-score | What it measures |
|---|---|
| `punch` | Global luminance contrast |
| `focal_pop` | Variance of per-tile mean luminance — high when there is one obvious focal area |
| `color_punch` | Saturation mean + saturation stddev (combined) |
| `text_band` | Presence of a high-contrast horizontal text band (long run of high-edge-density rows) |
| `brightness` | Distance from the optimal mid-tone (penalty for too dark or washed-out) |
| `edge_density` | Mean edge magnitude — peaks at mid values, penalised at extremes |

Each sub-score is normalised to `[0, 100]` and combined with weights `0.18 / 0.22 / 0.15 / 0.20 / 0.12 / 0.13`. Final `click_score` is in `[0, 100]`.

When given two or more thumbnails, the script also prints an explanation: which metric drove the gap, by how much, for each pairwise comparison vs the winner.

JSON mode:

```bash
python3 scripts/score_thumbnail.py variants/*.png --output ranking.json --json
```

## Full pipeline example

```bash
# 1) Find the best candidate frames
python3 scripts/pick_frames.py my_video.mp4 ./frames/ --top 5 --interval 1.5

# 2) Generate four variants from the top frame
python3 scripts/make_variants.py frames/frame_001.png ./variants/ \
  --title "Your Title Here" --subtitle "Optional subtitle"

# 3) Score the variants and pick the click-winner
python3 scripts/score_thumbnail.py variants/*.png --output ranking.json

# 4) Export the chosen variant to every platform size
python3 scripts/export_sizes.py variants/variant_b_clean_white_top.png ./out/
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success |
| 1 | partial failure (no frames passed filters; no scorable images among inputs) |
| 2 | error (bad arguments, unsafe path, missing or corrupt input, ffmpeg/ffprobe failure) |

## Safety properties

- All Python helpers use `subprocess.run` with argument lists (never `shell=True`) and reject input/output paths containing shell metacharacters via a strict regex allowlist.
- The skill never reads or writes outside the input/output paths the user provides.
- No environment variables are read for credentials. No tokens, secrets, or API keys are required.
- No remote calls of any kind. The skill only invokes locally installed `ffmpeg` and the Python `Pillow` library.

## Known limitations

- Frame scoring and thumbnail click-likelihood scoring are heuristic, not AI-based. They are not aware of "is the subject's face visible" — they maximise objective image-quality signals and proxies for visual hierarchy.
- Default font is the system default if `--font` is not provided. If no usable font is found, the script falls back to Pillow's bitmap font, which looks plain. Pass `--font` for nice typography.
- `compose_thumbnail.py` does not do automatic background removal. If you want isolated subjects, do the subject-cutout step in a different tool first.

## v0.3.0 changes

- `scripts/make_variants.py` now accepts `--auto-pick`. After producing the four A/B variants, it runs `scripts/score_thumbnail.py` on them, copies the highest-scoring variant to `<output_dir>/winner.png`, and writes `<output_dir>/winner.json` with the full ranking and reasoning. Removes the manual second step in the typical workflow.
- Robustly parses the scorer's nested `winner` block (`winner.winner_file`, `winner.ranked[]`) and falls back to the raw `results[]` array if the structure changes in future scorer versions.
- No changes to existing CLI flags; `--auto-pick` is purely additive. The four variant filenames (`variant_a_...png`, `variant_b_...png`, `variant_c_...png`, `variant_d_...png`) are unchanged.

## v0.2.0 changes

**New feature**

- `scripts/score_thumbnail.py` — deterministic local click-likelihood scorer. Scores one or more finished thumbnails on six visual metrics (punch, focal pop, color punch, text band, brightness, edge density) and ranks them. Pure Pillow + standard library, no ML, no remote calls.

**Bug fixes**

- `compose_thumbnail.py` and `make_variants.py` now reject empty `--title ""` with a clear error instead of silently producing a textless thumbnail.
- `compose_thumbnail.py` now catches `PIL.UnidentifiedImageError` on a corrupt or non-image input and prints a clean one-line error instead of leaking a Python traceback.
- `pick_frames.py` now correctly returns exit code 2 (not 0) when `ffprobe` fails on a non-video input, when the video duration is zero, or when the input path contains shell metacharacters. Pipelines that key off exit codes will work correctly now.
- `pick_frames.py` no longer silently produces zero frames on a very short clip (`< 2 * interval`). It now falls back to 3 evenly-spaced samples for short clips, and the new `--relax-on-empty` flag retries once with very loose thresholds when even the loose default produces no candidates.
- Removed a redundant double-ffprobe call in `probe_duration`.

**No breaking changes**: existing CLI flags, output filenames, scoring formulas, and verdict thresholds are unchanged. v0.1.0 scripts and pipelines continue to work.

## License

MIT. See `LICENSE`.
