---
name: photoplus-album-downloader
description: Download PhotoPlus / 谱时图片直播 albums from a URL or activity ID; use to inspect metadata, filter date tabs, save JSON, or write caption/GPS metadata.
version: 1.0.0
dependencies: python>=3.10, requests, tqdm, piexif
metadata:
  openclaw:
    requires:
      bins:
        - python3
    skillKey: photoplus-album-downloader
    homepage: https://github.com/helloene/live-album-downloader
---

# PhotoPlus Album Downloader

## Overview

Use the upstream Python project `helloene/live-album-downloader` to download original images from public PhotoPlus live albums. Always confirm the user has permission to download/store the album contents when the album is not clearly theirs.

## Quick Workflow

1. Extract the activity ID from the user input. PhotoPlus IDs are numeric and usually appear in:

```text
https://live.photoplus.cn/live/12345678
https://live.photoplus.cn/live/pc/12345678/#/live
```

2. Prefer the bundled wrapper because it accepts either a URL or ID and can clone/download the upstream project if needed:

```bash
python3 /path/to/photoplus-album-downloader/scripts/download_photoplus_album.py \
  "https://live.photoplus.cn/live/12345678" \
  --workdir /path/to/output-root \
  --install-deps
```

3. If dependencies are already installed and the upstream repo is already present, call the upstream script directly:

```bash
python3 live_album_downloader.py --id 12345678
```

4. Report the output folder. The upstream project writes to `./PhotoPlus/<activity_id>/` from the command working directory, or `./PhotoPlus/<folder-name>/` when `--folder-name` is used.

## Common Commands

Inspect album metadata and tab names before downloading:

```bash
python3 scripts/download_photoplus_album.py 12345678 --inspect --install-deps
```

Download only a date-like tab:

```bash
python3 scripts/download_photoplus_album.py 12345678 --tab 3.29 --folder-name "event-3.29"
```

Save metadata sidecars and preserve useful filenames:

```bash
python3 scripts/download_photoplus_album.py 12345678 \
  --save-metadata \
  --rename-template "{date}_{time}_{name}"
```

Write album title caption and GPS EXIF/IPTC metadata:

```bash
python3 scripts/download_photoplus_album.py 12345678 \
  --write-caption \
  --gps-lat 31.2304 \
  --gps-lon 121.4737
```

## Options

- Use `--count N` for test runs or partial downloads.
- Use `--tab all` for all photos; date tabs such as `3.28` are matched from photo timestamp metadata by the upstream project.
- Use `--folder-name NAME` to avoid numeric output folders.
- Use `--dry-run` on the wrapper to print the resolved upstream command without network or download work.
- Use `--repo-dir PATH` when an existing clone of `helloene/live-album-downloader` should be reused.
- Use `--install-deps` when `requests`, `tqdm`, or `piexif` are missing.

## Troubleshooting

- If the upstream script prints `Wrong ID`, re-check that the number came from `/live/<id>` or `/live/pc/<id>`, and that the album is public/available.
- If dependency installation fails in a sandbox, request approval to run the same `pip`/network command with escalation.
- If the album has many photos, first run with `--inspect` or `--count 10`.
- If filenames collide, the upstream project auto-adds suffixes such as `_2`.

## References

- Read `references/upstream-project.md` for the exact upstream repository URL, pinned commit observed while creating this skill, and supported CLI flags.
- Use `scripts/download_photoplus_album.py` as the low-friction command wrapper.
