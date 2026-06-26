# Post-Processing Workflow

**Load this file when the user asks to edit, join, trim, crop, add text, add effects, convert format, or otherwise post-process a generated image or video.**

For detailed ffmpeg commands and flags, see `{baseDir}/workflows/ffmpeg.md`.

---

## ⚠️ Audio Preservation (MANDATORY)

**ALWAYS preserve audio tracks from source videos unless the user explicitly asks to remove or replace audio.**

When source video has audio (check with `ffprobe`), ffmpeg commands MUST include audio mapping and encoding:
- Map audio: `-map 0:a` (or appropriate stream index)
- Encode audio: `-c:a aac -b:a 192k -ar 44100 -ac 2`
- For crossfades: use `acrossfade` filter alongside video `xfade`
- Never use `-an` (strips audio) unless explicitly requested

Many video models (e.g. `seedance-2-0`) generate audio alongside video. Stripping it silently is a data loss bug.

---

## Detection

```bash
which ffmpeg 2>/dev/null
```

If not found, tell the user: "ffmpeg is not installed. Install it for enhanced post-processing features (joining, trimming, effects, text overlays, format conversion)." See `{baseDir}/workflows/ffmpeg.md` for platform-specific installation instructions.

---

## ⚠️ Output Compatibility & Delivery

Apply **mandatory output compatibility flags** and **delivery steps** as documented in `{baseDir}/workflows/ffmpeg.md` (sections: "MANDATORY: Output Compatibility" and "Delivering ffmpeg output").

---

## Workflow

1. **Identify the post-processing task** (trim, join, crop, text overlay, effects, format conversion, etc.)
2. **Check ffmpeg availability**
3. **Load `{baseDir}/workflows/ffmpeg.md`** for detailed commands for the specific operation
4. **Apply mandatory output compatibility flags** from `{baseDir}/workflows/ffmpeg.md` to every output MP4
5. **Copy output** per `{baseDir}/workflows/ffmpeg.md` delivery instructions
6. **Deliver** the processed file to the user

---

## Common Operations

| Task | Reference |
|------|-----------|
| Join/concatenate videos | workflows/ffmpeg.md §1 |
| Trim/cut | workflows/ffmpeg.md §2 |
| Crop/resize | workflows/ffmpeg.md §3 |
| Effects (fade, speed, reverse, B&W, blur) | workflows/ffmpeg.md §4 |
| Text overlays / watermarks | workflows/ffmpeg.md §5 |
| Audio (add, replace, extract, adjust) | workflows/ffmpeg.md §6 |
| Format conversion (MP4, WebM, GIF) | workflows/ffmpeg.md §7 |
| Advanced (PIP, split screen, slideshow) | workflows/ffmpeg.md §8 |
| Hardware acceleration | workflows/ffmpeg.md §10 |

---

## Media Allowlist Handling

When delivering post-processed media:
- Images: PNG, JPEG, WebP
- Videos: MP4 (H.264 + AAC), GIF
- Ensure output format is in the allowlist before attempting delivery

---

## Delivery

Follow the delivery pattern defined in `{baseDir}/SKILL.md`. Deliver the post-processed file to the user with a description of the operation performed.

---

## Error Handling

- If ffmpeg fails, report the exact error output to the user
- Do not retry with different parameters without user approval
- If a format is unsupported, suggest alternatives

---

*Part of the Katana skill. See SKILL.md for routing and general configuration.*
