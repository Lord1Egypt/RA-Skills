# local-file-processor

Process local files with common operations: batch rename, format conversion, organization, duplicate detection, and metadata management.

## Installation

```bash
brew install exiftool imagemagick ffmpeg
chmod +x ~/.openclaw/workspace/skills/local-file-processor/local-file-processor
```

## Global Safety Flags

These flags work for all commands:

- `--dry-run` — Preview changes, no files modified/deleted
- `--overwrite` — Allow replacing existing target files (default is no overwrite)
- `--force` — Skip confirmation prompts for destructive actions
- `--verbose` — Verbose output

## Commands

### rename

```bash
local-file-processor rename <pattern> <replacement> [--dir <path>] [--recursive]
```

Examples:

```bash
local-file-processor rename "IMG_" "Photo_" --dir ~/Pictures --dry-run
local-file-processor rename "old" "new" --dir ~/Files
local-file-processor rename "*.jpg" "vacation_{seq}.jpg" --dir ~/Photos
```

Special replacement tokens:
- `{seq}` sequence number (001, 002, ...)
- `{date}` current date (YYYY-MM-DD)
- `{time}` current time (HH-MM-SS)

---

### convert

```bash
local-file-processor convert <format> --input <path-or-glob> [--output <dir>] [--quality <1-100>]
```

Examples:

```bash
local-file-processor convert jpg --input "~/Photos/*.png" --dry-run
local-file-processor convert mp3 --input "~/Audio/*.wav" --output ~/converted
local-file-processor convert mp4 --input ./clip.mov --overwrite
```

Supported formats:
- Images: `jpg, jpeg, png, gif, webp, tiff, bmp`
- Audio: `mp3, m4a, wav, flac, aac, ogg`
- Video: `mp4, mov, avi, mkv, webm`

---

### organize

```bash
local-file-processor organize <date|type|metadata> [--dir <path>] [--key <metadataTag>]
```

Examples:

```bash
local-file-processor organize date --dir ~/Downloads --dry-run
local-file-processor organize type --dir ~/Documents
local-file-processor organize metadata --dir ~/Photos --key Model
```

Notes:
- `metadata` strategy requires `--key`.
- Metadata-derived folder names are sanitized to prevent traversal/unsafe paths.

---

### duplicates

```bash
local-file-processor duplicates [--dir <path>] [--recursive] [--action list|delete|move] [--dest <dir>]
```

Examples:

```bash
local-file-processor duplicates --dir ~/Downloads
local-file-processor duplicates --dir ~/Files --action delete --dry-run
local-file-processor duplicates --dir ~/Files --action delete --force
local-file-processor duplicates --dir ~/Photos --action move --dest ~/Duplicates
```

Notes:
- `delete` asks for confirmation unless `--force` is used.
- `move` requires `--dest`.

---

### metadata

```bash
local-file-processor metadata <file-or-glob> [--get <key> | --set <k=v>... | --remove <key>... | --all]
```

Examples:

```bash
local-file-processor metadata photo.jpg --get DateTimeOriginal
local-file-processor metadata "~/Photos/*.jpg" --set "Artist=Jane Doe" --dry-run
local-file-processor metadata photo.jpg --remove Copyright --force
```

Notes:
- Metadata keys are validated (safe charset only).
- Write/delete metadata operations require confirmation unless `--force`.

## Safety Model

- **No overwrite by default** for move/convert operations.
- Use `--overwrite` to explicitly replace existing files.
- Destructive operations require confirmation unless `--force`.
- `--dry-run` works for all write/delete operations.
- File scanning uses null-delimited handling for safer filenames.

## Troubleshooting

**Missing exiftool**
```bash
brew install exiftool
```

**Missing convert (ImageMagick)**
```bash
brew install imagemagick
```

**Missing ffmpeg**
```bash
brew install ffmpeg
```
