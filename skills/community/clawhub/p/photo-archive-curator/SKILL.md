---
name: photo-archive-curator
description: "Use when a phone or folder of thousands of photos needs culling, deduplication, and organization. Detects exact and near-duplicates (perceptual hashing), finds blurry shots, builds a burst-series keeper picker, and renames files into a dated folder tree using EXIF — no cloud, no uploads."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [photos, dedupe, exif, perceptual-hash, organization, privacy]
---

# Photo Archive Curator

## Overview
Camera rolls accumulate thousands of files: burst shots, near-identical takes, WhatsApp
duplicates, screenshots of screenshots, and name-mangled exports (`IMG_4711.JPG` next
to `2019-03-12 14.55.11.jpg` next to `photo(3).jpg`). Cloud services offer to "clean"
this by uploading everything — a privacy trade many don't want. This skill curates a
photo archive **entirely offline**, in-place:

- **Exact duplicates** by file hash, then **near-duplicates** by perceptual hash
  (8×8 DCT average hash — survives re-encoding, resizing, WhatsApp compression)
- **Blur detection** via Laplacian-variance on the decoded image (stdlib-decodable
  formats or Pillow when present)
- **Burst grouping**: consecutive shots within 2s of each other → keep the sharpest /
  largest, list the rest as cull candidates
- **Dated rename**: `EXIF DateTimeOriginal` → `YYYYMMDD-HHMMSS` with collision suffixes,
  into `YYYY/YYYY-MM/` folders; non-EXIF files fall back to mtime with a `~` marker
- **Dry-run by default**: writes nothing until `--apply`; every planned action is
  reviewable first; originals are never deleted without `--apply delete-dupes`

## When to Use
- "My phone/camera export is a mess, organize it" (10k+ files)
- Freeing space: burst series and near-dupes are typically 20–40% of a camera roll
- Merging photo libraries from two phones/laptops (collision-safe renaming)
- Pre-migration cleanup before moving photos into any cloud or NAS
- **Don't use for:** editing/rating workflows (no UI), videos (pass-through only),
  RAW-format culling quality judging (hash/dedupe still works; blur scores are less
  meaningful on unprocessed RAW).

## Steps
1. **Always start with a scan (dry run):**
   ```bash
   python3 scripts/curate.py --root ~/Photos --scan
   ```
   Output: exact dupes, near-dupes (hamming distance ≤ 6), blurry candidates,
   burst groups with keeper recommendation, undated files count.
2. Review the cull list. Keepers chosen as: sharpest in burst → tie-break largest
   file → tie-break earliest name (stable, explainable rule).
3. **Apply the plan** (still non-destructive by default):
   ```bash
   python3 scripts/curate.py --root ~/Photos --organize --apply
   python3 scripts/curate.py --root ~/Photos --apply delete-dupes   # after backup!
   ```
4. Deletion policy: exact dupes are safe after the scan output is reviewed; near-dupes
   move to a `_cull/` quarantine folder (recoverable) unless `--apply delete-dupes`
   is explicitly passed. Recommend a backup before any delete.
5. Re-run `--scan` to verify: zero exact dupes, zero collisions, dated tree coverage.

## How Perceptual Hashing Works (summary)
Each image → grayscale 8×8 → DCT-ish average → 64-bit hash. Two photos with hamming
distance ≤ 6 are visually the same (re-compressed, slightly cropped, filtered).
Distance 7–12 = "similar, review" (burst candidates). The implementation uses a pure-
stdlib 8×8 downsample + a DCT-free aHash/dHash pair (horizontal gradient hash) — robust
to brightness shifts and cheap on ARM. With Pillow present, quality improves (real DCT).

## Worked Example
`~/Photos` — 12,400 files from three phones merged:
```
EXACT dupes:        812 files (1.9 GB)   — same sha256, different names/paths
NEAR dupes:       1,204 pairs (2.8 GB)   — hamming ≤ 6 (WhatsApp re-compressions)
Burst groups:        96 groups, 531 files — 2s-window series; keep sharpest → 186 keep
Blurry candidates:   143 files            — Laplacian var below threshold
Undated:            208 files             — no EXIF, mtime used, marked with ~
Plan: 12,400 → 10,241 files, dated tree YYYY/YYYY-MM/, unique names guaranteed.
```
User reviews the `_cull/` quarantine for an evening, deletes it, reclaims ~5 GB.

## Common Pitfalls
1. **Deleting before reviewing.** Near-dupes at distance ≤ 6 are *usually* redundant,
   not always — quarantine first (`_cull/`), delete the quarantine after a look.
2. **Trusting filenames.** `IMG_1234` resets across devices; EXIF
   DateTimeOriginal is the only reliable timestamp; the `~` prefix marks files where
   EXIF was missing and mtime was used (often wrong for migrated/copied files).
3. **Live Photos / paired files**: `.jpg` + `.mov` sidecars and Samsung `MotionPhoto`
   share a stem — the curator renames sidecars together with their stills; never
   cull a `.mov` sidecar whose still is a keeper.
4. **Timezone drift**: cameras with wrong clocks produce wrong folders — scan output
   shows a year histogram; a 2020 folder with 3 photos screams clock reset.
5. **Case-insensitive filesystems**: `img.jpg` vs `IMG.JPG` collide after rename —
   collision suffix `-2`, `-3` is appended deterministically.
6. **Running against a live camera roll** (phone still connected): files change during
   scan — run against a stable copy/export.

## Verification Checklist
- [ ] Dry-run scan reviewed BEFORE any --apply
- [ ] Exact dupes: same hash verified; near-dupes quarantined to _cull/, not deleted
- [ ] Burst keepers: rule stated (sharpest → largest → earliest name)
- [ ] Renamed tree: no collisions, sidecar .mov moved with stills
- [ ] Undated files visibly marked (~ prefix), count reported
- [ ] Re-scan after apply: 0 exact dupes, 0 collision errors
