# Upstream Project Notes

Repository: `https://github.com/helloene/live-album-downloader`

Observed default branch commit while creating this skill: `d852ddc21bf64b3fb2ac9eada81c9047124783ce`.

Purpose: Python CLI for downloading original photos from public PhotoPlus live album activities. It fetches PhotoPlus public album metadata and writes original image bytes to `./PhotoPlus/<activity_id>/`, or `./PhotoPlus/<folder-name>/` when `--folder-name` is supplied.

Requirements:

- Python 3.10+
- `requests`
- `tqdm`
- `piexif`

Main upstream command:

```bash
python3 live_album_downloader.py --id 12345678
```

Important flags:

- `--id`: required numeric PhotoPlus activity ID.
- `--count`: maximum photos to fetch. Default is `9999`.
- `--tab`: tab filter. Default is `all`; date-like tabs such as `3.28` are supported.
- `--rename-template`: filename template with `{name}`, `{date}`, `{time}`, `{address}`, and `{tab}`.
- `--folder-name`: output folder name under `PhotoPlus`.
- `--no-set-mtime`: do not sync file modification time from photo timestamp.
- `--save-metadata`: write raw JSON sidecar metadata.
- `--inspect`: print summary and tab matching preview without downloading.
- `--write-caption`: write activity title into IPTC `Caption/Abstract` and EXIF `UserComment`.
- `--gps-lat`, `--gps-lon`, `--gps-alt`: write EXIF GPS metadata.

Activity ID examples:

```text
https://live.photoplus.cn/live/12345678
https://live.photoplus.cn/live/pc/12345678/#/live
```

Use only for albums the user has permission to download or archive.
