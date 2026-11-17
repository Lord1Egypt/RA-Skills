# photo-archive-curator

Offline curator for messy photo archives: finds exact and near-duplicates, flags
blurry shots, picks burst keepers, and renames everything into a dated
`YYYY/YYYY-MM/` tree from EXIF — entirely on your machine, no uploads, dry-run by
default.

## The real-world problem
A decade of phone exports looks like this: `IMG_4711.JPG`, `photo(3).jpg`,
`2019-03-12 14.55.11.jpg` — 30–40% of it burst series, WhatsApp re-compressions and
plain duplicates. Cloud "cleanup" tools want to upload your entire camera roll to do
it. Merging two phones' libraries creates name collisions. Nobody can find anything,
and nobody dares delete anything.

## What it does
`scripts/curate.py` (stdlib core; Pillow optional and recommended for the
perceptual pass):

- **Exact duplicates** — sha256, safe to cull
- **Near duplicates** — dHash/aHash perceptual hashes, hamming distance ≤ 6 survives
  re-encoding, resizing, WhatsApp compression
- **Blur candidates** — relative variance test against the archive median
- **Burst series** — shots within 2 s grouped; keeper = sharpest → largest → earliest
- **Dated rename** — EXIF DateTimeOriginal → `YYYYMMDD-HHMMSS` in `YYYY/YYYY-MM/`,
  collision suffixes, `~` marker when only mtime exists, sidecar `.mov/.dng` moved
  with their stills
- **Safety** — dry-run by default, `--apply` to act, quarantine concept (`_cull/`),
  full audit log `_curate_log.jsonl`

```
$ python3 scripts/curate.py --root ~/Photos --scan
Photos: 12400
Exact duplicates: 812 files (1.9 GB)
Near duplicates (dist<=6): 1204 pairs
Blur candidates (var < 10% of archive median): 143
Burst groups (>=3 shots within 2s): 96 (531 files, 345 cull candidates)

$ python3 scripts/curate.py --root ~/Photos --organize --apply
Plan: 11062 moves ... Applied. Log: ~/Photos/_curate_log.jsonl
```

## Files
- `SKILL.md` — triggers, workflow, keeper rules, pitfalls
- `references/curation-guide.md` — hash theory, EXIF rules, layout contract, privacy
- `scripts/curate.py` — the curator (run `--scan` first, always)

Local-only by design. Backup before any delete. Pillow improves the perceptual pass
(`uv pip install pillow` or system package).
