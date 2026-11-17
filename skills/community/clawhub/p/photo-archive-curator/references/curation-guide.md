# Photo Archive Curation — Full Reference

## 1. Taxonomy of photo mess
| Kind | Signature | Tool response |
|---|---|---|
| Exact duplicate | identical bytes (sha256) | auto-detect, safe cull (keep one) |
| Near duplicate | re-encoded/resized/compressed copy | perceptual hash hamming ≤ 6 |
| Burst series | ≥2 shots within ≤2s, same exposure family | keep sharpest (Laplacian var), quarantine rest |
| Screenshot-of-screenshot | huge near-dup cluster of PNGs | near-dup grouping reveals them |
| Name collisions | same name from different devices | rename by EXIF datetime + suffix |
| Undated | no EXIF (messenger saves, old scans) | mtime fallback, `~` prefix |

## 2. Perceptual hashing (why and how)
Goal: a fingerprint of what the image *looks like*, stable under JPEG re-encode,
resolution change, mild crop, and brightness filters — the transformations messaging
apps and export pipelines apply.

- **aHash (average)**: downsample to 8×8 grayscale, threshold each pixel vs the mean
  → 64 bits. Fast, brightness-sensitive.
- **dHash (gradient)**: 9×8 → 8×8 horizontal differences → 64 bits. Robust to global
  brightness shifts, cheap. Default here.
- **pHash (DCT)**: 32×32 → DCT → top-left 8×8 low frequencies → 64 bits. Most robust
  to compression/crop; needs Pillow (or any DCT implementation).

Combined score: near-dup if `min(dist_a, dist_d) ≤ 6`; similar (burst candidate) if
`≤ 12`. Hamming distance on 64 bits: random unrelated images average ~32.

## 3. Blur detection
Laplacian variance on the grayscale image (or its 8×8-derived luminance grid when
running pure-stdlib): sharp edges → high variance. Thresholds are *relative*: the
curator computes the archive's median variance and flags images below
`median × factor`. Absolute thresholds fail across devices — a phone night shot is
softer than a DSLR daylight shot by default. Burst-keeper selection always uses
relative ranking within the group (sharpest wins), which is device-independent.

## 4. EXIF rules
- `DateTimeOriginal` (tag 36867) > `CreateDate` (36868) > file mtime (mark `~`).
- Formats: JPEG (EXIF in APP1), HEIC (EXIF in `meta` box — needs Pillow/exifread),
  TIFF, PNG (rarely has EXIF; `eXIf` chunk since 2017 spec).
- Sidecars: `.jpg+.mov` (Apple Live Photo), `.dng+.jpg`, Samsung `MotionPhoto`
  (the motion is embedded in the JPEG's trailer — XMP `MicroVideo` offset; copy the
  file whole, never strip).
- GPS coordinates survive copying but not social-upload re-encoding; if the user asks
  for privacy scrubbing, EXIF wipe is a separate operation (`--strip-exif` deletes
  all metadata after the dated rename — the date is already in the filename).

## 5. Directory layout contract
```
<root>/2023/2023-07/20230712-143015.jpg
<root>/2023/2023-07/20230712-143015-2.jpg    (collision suffix)
<root>/2023/2023-07/20230712-143016~.jpg     (undated: mtime used)
<root>/_cull/near/…                          (quarantined near-dupes)
<root>/_cull/burst/…                         (non-keeper burst shots)
<root>/_cull/blur/…                          (blur candidates, review)
```
Rules: never overwrite; never cross filesystems silently (rename within root only);
operations logged to `<root>/_curate_log.jsonl` (every planned+applied action,
replayable and auditable).

## 6. Performance notes
- Hashing 10k photos: sha256 exact-dup pass ~1–2 min (I/O bound).
- Perceptual pass decodes thumbnails: with Pillow, use `Image.draft()` / decode at
  ≤256px; pure-stdlib path decodes JPEG via `imghdr`-style parsing only for size —
  for real pixels without Pillow the script limits itself to exact+dHash on
  Pillow-decoded data and says so clearly if Pillow is missing.
- All-pairs near-dup search is O(n²) on 64-bit ints — 10k files = 50M comparisons ≈
  seconds in C-speed ints, but the script buckets by hash prefix (16 buckets) to cut
  it further; unbucketed comparison remains the fallback.

## 7. Privacy & safety
- 100% local: no network calls, no telemetry, no uploads — verifiable by reading the
  script (stdlib imports only).
- Dry-run default; `--apply` required for any filesystem mutation.
- Deletion is two-stage: quarantine (`_cull/`) then explicit delete of quarantine.
- The log (`_curate_log.jsonl`) is itself metadata — offer to delete it after a
  verified clean run.
