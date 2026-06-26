---
name: lanhu-design
description: Read Lanhu UI designs, extract slices, and download Web/iOS/Android assets using lh-design. Use when the user mentions 蓝湖, Lanhu, UI稿, 设计稿, 切图, iOS @2x/@3x, Android drawable, or Web 1x/2x/3x assets.
---

# Lanhu Design

## Prerequisites

Use the `lh-design` CLI from `xuwenxindeai/lanhu-design-reader`.

If `lh-design` is missing, do not run remote installer commands from this skill. Ask the user to install `lh-design` from the project README, then verify with `lh-design --help`.

The default installer paths are:

```text
Source: ~/.lanhu-design-reader/src
Virtualenv: ~/.lanhu-design-reader/venv
Config: ~/.lanhu-design-reader/.env
Command: ~/.local/bin/lh-design
```

The user must provide `LANHU_COOKIE` via shell env, a local `.env`, or `~/.lanhu-design-reader/.env`. If DDS schema reads need a separate login state, use `DDS_COOKIE`.

## Workflow

1. Parse the user's Lanhu URL and identify `image_id`. If the URL already includes `image_id` or `docId`, `--image-id` may be omitted.
2. Inspect slices first:

```bash
lh-design slices '<Lanhu URL>' --image-id <image_id> -o slices.json
```

3. Download assets for the target platform.

Web:

```bash
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale 1x -o web_1x
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale 2x -o web_2x
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale 3x -o web_3x
```

iOS:

```bash
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale ios_2x -o ios_2x
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale ios_3x -o ios_3x
```

Android:

```bash
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale android_mdpi -o drawable-mdpi
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale android_hdpi -o drawable-hdpi
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale android_xhdpi -o drawable-xhdpi
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale android_xxhdpi -o drawable-xxhdpi
lh-design download-slices '<Lanhu URL>' --image-id <image_id> --scale android_xxxhdpi -o drawable-xxxhdpi
```

## Important

- Web uses `1x/2x/3x`, not `ios_*`.
- iOS uses `ios_2x/ios_3x`.
- Android uses `android_mdpi/android_hdpi/android_xhdpi/android_xxhdpi/android_xxxhdpi`.
- For Photoshop uploads, `base_size` equals iOS `@2x` / Android `xhdpi`.
- Prefer `slices.json` as the source of truth before renaming or moving assets.
