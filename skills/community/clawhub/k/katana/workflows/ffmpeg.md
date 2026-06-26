# ffmpeg Post-Processing Reference

**Load this file when the user asks to edit, join, trim, crop, add text, add effects, convert format, or otherwise post-process a generated video.**

---

## ⚠️ Delivering ffmpeg output

ffmpeg temp output may not be in your agent's allowed file paths. Copy the file to an appropriate location before sending.

**Example output directory:**

```bash
SKILL_OUTBOUND_DIR="${SKILL_OUTBOUND_DIR:-${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw}/media/outbound}"
mkdir -p "$SKILL_OUTBOUND_DIR"
cp ${TMPDIR:-/tmp}/output.mp4 "$SKILL_OUTBOUND_DIR/output.mp4"
```

Adapt the output directory to your agent framework's file delivery requirements.

---

## Detection

```bash
which ffmpeg 2>/dev/null
```

If not found, install for your platform:

| Platform | Command |
|---|---|
| Linux (Debian/Ubuntu) | `sudo apt install ffmpeg` |
| Linux (Fedora) | `sudo dnf install ffmpeg` |
| macOS | `brew install ffmpeg` |
| Windows | `winget install ffmpeg` or `choco install ffmpeg` |

ffmpeg CLI flags are identical across all platforms.

---

**Temp directory:** Examples use `$TMPDIR` for temp files (falls back to `/tmp` on POSIX, uses `%TEMP%` on Windows). Set `TMPDIR` if needed, or substitute your preferred temp directory.

**Windows users:** Shell commands in this file use POSIX (bash) syntax. For PowerShell/CMD: replace `${TMPDIR:-/tmp}` with `$env:TEMP`, use backtick `` ` `` for line continuation, and use `\` for path separators.

## ⚠️ MANDATORY: Output Compatibility (NON-NEGOTIABLE)

**ALL ffmpeg output videos MUST use these flags to ensure playback on Telegram, iOS, Android, and browsers:**

```bash
-c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart
```

**Why:** Without these flags, ffmpeg may default to:
- `High 4:4:4 Predictive` profile → unplayable on Telegram, iOS, most Android devices, and many browsers
- Non-standard pixel formats → blank thumbnails, no playback
- Missing `faststart` → video must fully download before playing

**For crossfade/xfade operations specifically:** Normalise BOTH source videos to the above format BEFORE applying filters, then re-encode the output with the same flags. The xfade filter can produce non-standard pixel formats if fed unnormalised input.

```bash
# Step 1: Normalise source 1
ffmpeg -y -i source1.mp4 \
  -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -crf 18 -preset medium \
  -c:a aac -b:a 192k -ar 44100 -ac 2 \
  -movflags +faststart ${TMPDIR:-/tmp}/src1_norm.mp4

# Step 2: Normalise source 2
ffmpeg -y -i source2.mp4 \
  -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -crf 18 -preset medium \
  -c:a aac -b:a 192k -ar 44100 -ac 2 \
  -movflags +faststart ${TMPDIR:-/tmp}/src2_norm.mp4

# Step 3: Apply filters on normalised sources, re-encode output with same flags
ffmpeg -y -i ${TMPDIR:-/tmp}/src1_norm.mp4 -i ${TMPDIR:-/tmp}/src2_norm.mp4 \
  -filter_complex "..." \
  -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -crf 18 -preset medium \
  -c:a aac -b:a 192k -ar 44100 -ac 2 \
  -movflags +faststart output.mp4
```

**Every command in this file that produces an output MP4 MUST include these flags.** No exceptions.

---

## Speed Guide

| Symbol | Meaning |
|--------|---------|
| ⚡ | Stream copy (`-c copy`) — fast, no re-encode. **Note:** preserves source codec settings — if playback issues occur, use full re-encode with mandatory compatibility flags instead |
| 🐢 | Re-encode required — slower, quality loss possible |
| 🔧 | Re-encode recommended for best results |

---

## 1. Concatenation / Joining

### Join with concat demuxer (⚡ for same codec/resolution)

Best for videos with identical codecs and resolution.

```bash
# Create a file list
printf "file 'video1.mp4'\nfile 'video2.mp4'\nfile 'video3.mp4'\n" > ${TMPDIR:-/tmp}/concat.txt

# Concat without re-encoding (fastest — requires same codec, resolution, frame rate)
ffmpeg -f concat -safe 0 -i ${TMPDIR:-/tmp}/concat.txt -c copy output.mp4
```

**Gotcha:** All inputs must have identical codecs, resolution, and frame rate. If they differ, use the concat filter or normalise first.

### Join with concat filter (🐢 — handles different properties)

```bash
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex \
  "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v0]; \
   [1:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v1]; \
   [v0][0:a][v1][1:a]concat=n=2:v=1:a=1[outv][outa]" \
  -map "[outv]" -map "[outa]" output.mp4
```

**Note:** Normalises all inputs to 1080p/30fps before joining.

### Join with crossfade transition (🐢)

```bash
# 1-second crossfade between two videos
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex \
  "[0:v]trim=0:5,setpts=PTS-STARTPTS[v0]; \
   [1:v]trim=0:5,setpts=PTS-STARTPTS[v1]; \
   [v0][v1]xfade=transition=fade:duration=1:offset=4[outv]; \
   [0:a]atrim=0:5,asetpts=PTS-STARTPTS[a0]; \
   [1:a]atrim=0:5,asetpts=PTS-STARTPTS[a1]; \
   [a0][a1]acrossfade=d=1[outa]" \
  -map "[outv]" -map "[outa]" output.mp4
```

**Gotcha:** `offset` = duration of first video minus transition duration. Available transitions: `fade`, `wipeleft`, `wiperight`, `dissolve`, `slidedown`, `slideup`, `circleopen`, `circleclose`, etc.

---

## 2. Trimming / Cutting

### Trim by timestamp without re-encoding (⚡)

```bash
ffmpeg -i input.mp4 -ss 00:00:05 -to 00:00:15 -c copy output.mp4
```

**Gotcha:** Cuts at nearest keyframe — may not be frame-accurate. Put `-ss` before `-i` for faster seek (less accurate).

### Trim with re-encoding for precise cuts (🐢)

```bash
ffmpeg -i input.mp4 -ss 00:00:05.123 -to 00:00:15.456 -c:v libx264 -c:a aac output.mp4
```

**Note:** Frame-accurate but requires full re-encode.

### Trim to duration (⚡ or 🐢)

```bash
# Fast (stream copy)
ffmpeg -i input.mp4 -t 10 -c copy output.mp4

# Precise (re-encode)
ffmpeg -i input.mp4 -t 10 -c:v libx264 -c:a aac output.mp4
```

---

## 3. Cropping & Resizing

### Crop to specific dimensions (🐢)

```bash
# Crop 1920x1080 to 1080x1080 (centred)
ffmpeg -i input.mp4 -filter:v "crop=1080:1080:(1920-1080)/2:0" -c:a copy output.mp4
```

**Formula:** `crop=W:H:X:Y` where X,Y is top-left corner of crop region.

### Crop to aspect ratio (🐢)

```bash
# Crop to 1:1 (square)
ffmpeg -i input.mp4 -filter:v "crop=ih:ih:(iw-ih)/2:0" -c:a copy output.mp4

# Crop to 9:16 (vertical from landscape)
ffmpeg -i input.mp4 -filter:v "crop=ih*9/16:ih:(iw-ih*9/16)/2:0" -c:a copy output.mp4
```

### Resize / scale (🐢)

```bash
# Scale to 1080p (preserve aspect ratio)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:a copy output.mp4

# Scale to exact size (may distort)
ffmpeg -i input.mp4 -vf "scale=1280:720" -c:a copy output.mp4

# Scale by factor (half size)
ffmpeg -i input.mp4 -vf "scale=iw/2:ih/2" -c:a copy output.mp4
```

**Note:** Use even dimensions — ffmpeg requires widths/heights divisible by 2 for most codecs.

### Pad / letterbox to different aspect ratio (🐢)

```bash
# Letterbox 16:9 to 4:3 with black bars
ffmpeg -i input.mp4 -vf "pad=ih*4/3:ih:(ow-iw)/2:(oh-ih)/2:black" -c:a copy output.mp4
```

---

## 4. Effects

### Fade in / fade out — video (🐢)

```bash
# 1-second fade in, 1-second fade out on a 10-second video
ffmpeg -i input.mp4 -filter:v \
  "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" -c:a copy output.mp4
```

### Fade in / fade out — audio (🐢)

```bash
ffmpeg -i input.mp4 -filter:a \
  "afade=t=in:st=0:d=1,afade=t=out:st=9:d=1" -c:v copy output.mp4
```

### Combined video + audio fade (🐢)

```bash
ffmpeg -i input.mp4 -filter_complex \
  "[0:v]fade=t=in:st=0:d=1,fade=t=out:st=9:d=1[v]; \
   [0:a]afade=t=in:st=0:d=1,afade=t=out:st=9:d=1[a]" \
  -map "[v]" -map "[a]" output.mp4
```

### Speed up / slow down (🔧)

```bash
# 2x speed (fast forward)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output.mp4

# 0.5x speed (slow motion)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" output.mp4
```

**Gotcha:** `atempo` range is 0.5–2.0. For >2x or <0.5x, chain multiple: `atempo=2.0,atempo=2.0` for 4x.

### Reverse video (🐢)

```bash
# Reverse video and audio
ffmpeg -i input.mp4 -vf reverse -af areverse output.mp4
```

**Gotcha:** Entire file is loaded into memory. For long videos, trim first.

### Black and white / grayscale (🐢)

```bash
ffmpeg -i input.mp4 -vf "hue=s=0" -c:a copy output.mp4
# Alternative:
ffmpeg -i input.mp4 -vf "colorchannelmixer=.3:.6:.1:0:.3:.6:.1:0:.3:.6:.1" -c:a copy output.mp4
```

### Brightness / contrast / saturation (🐢)

```bash
# Increase brightness +0.1, contrast 1.5x, saturation 1.2x
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:contrast=1.5:saturation=1.2" -c:a copy output.mp4
```

### Blur (🐢)

```bash
# Full video Gaussian blur
ffmpeg -i input.mp4 -vf "gblur=sigma=5" -c:a copy output.mp4

# Box blur
ffmpeg -i input.mp4 -vf "boxblur=5:1" -c:a copy output.mp4

# Selective blur (region only) — blur top-right quarter
ffmpeg -i input.mp4 -filter_complex \
  "[0:v]crop=iw/2:ih/2:iw/2:0,boxblur=10[blur]; \
   [0:v][blur]overlay=iw/2:0" -c:a copy output.mp4
```

---

## 5. Text / Overlays

### Basic text overlay (🐢)

```bash
ffmpeg -i input.mp4 -vf \
  "drawtext=text='Hello World':fontcolor=white:fontsize=48:x=50:y=50" \
  -c:a copy output.mp4
```

### Styled text with font, colour, background box (🐢)

ffmpeg uses a built-in default font. To use a custom font, provide `fontfile=` with a platform-specific path.

| Platform | Common font path |
|---|---|
| Linux | `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf` |
| macOS | `/System/Library/Fonts/Helvetica.ttc` |
| Windows | `C:/Windows/Fonts/arial.ttf` |

```bash
ffmpeg -i input.mp4 -vf \
  "drawtext=text='Hello World':fontcolor=white:fontsize=64:box=1:boxcolor=black@0.5:boxborderw=10:x=(w-text_w)/2:y=(h-text_h)/2" \
  -c:a copy output.mp4
```

**Parameters:**
- `box=1:boxcolor=black@0.5` — semi-transparent background
- `boxborderw=10` — padding around text
- `x=(w-text_w)/2:y=(h-text_h)/2` — centre alignment

### Moving / animated text (🐢)

```bash
# Scroll text from right to left
ffmpeg -i input.mp4 -vf \
  "drawtext=text='Breaking News':fontcolor=white:fontsize=48:x=w-mod(w*t*100\,w+text_w):y=h-60" \
  -c:a copy output.mp4

# Fade in text (appears at 2s, fully visible at 3s)
ffmpeg -i input.mp4 -vf \
  "drawtext=text='Hello':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2:enable='between(t,2,10)':alpha=if(lt(t,3)\,(t-2)/1\,1)" \
  -c:a copy output.mp4
```

### Timestamp / watermark overlay (🐢)

```bash
# Burn in timestamp
ffmpeg -i input.mp4 -vf \
  "drawtext=text='%{localtime\:%Y-%m-%d %H\\\\\:%M\\\\\:%S}':fontcolor=white:fontsize=24:x=10:y=10:box=1:boxcolor=black@0.5" \
  -c:a copy output.mp4
```

### Image overlay — picture-in-picture / watermark logo (🐢)

```bash
# Logo watermark in bottom-right corner (10% of width, with 10px padding)
ffmpeg -i input.mp4 -i logo.png -filter_complex \
  "[1:v]scale=iw*0.1:-1[logo];[0:v][logo]overlay=W-w-10:H-h-10" \
  -c:a copy output.mp4
```

### Subtitle file overlay (🐢)

```bash
# Burn in SRT subtitles
ffmpeg -i input.mp4 -vf "subtitles=subtitles.srt" -c:a copy output.mp4

# ASS subtitles (preserves styling)
ffmpeg -i input.mp4 -vf "subtitles=subtitles.ass" -c:a copy output.mp4
```

**Gotcha:** `subtitles` filter requires ffmpeg compiled with `--enable-libass`. On most systems this is included. If not, use `-c:s mov_text` to embed (soft subs) instead of burning in.

---

## 6. Audio

### Add / replace audio track (⚡ or 🐢)

```bash
# Replace audio (re-encode video)
ffmpeg -i input_video.mp4 -i audio.mp3 -c:v libx264 -c:a aac -map 0:v:0 -map 1:a:0 -shortest output.mp4

# Replace audio without re-encoding video (if codecs compatible)
ffmpeg -i input_video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest output.mp4
```

### Extract audio from video (⚡)

```bash
ffmpeg -i input.mp4 -vn -c:a copy output.aac
# Or convert to mp3
ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 output.mp3
```

### Remove audio (⚡)

```bash
ffmpeg -i input.mp4 -an -c:v copy output.mp4
```

### Adjust volume (🐢)

```bash
# Double volume
ffmpeg -i input.mp4 -filter:a "volume=2.0" -c:v copy output.mp4

# Half volume
ffmpeg -i input.mp4 -filter:a "volume=0.5" -c:v copy output.mp4

# Normalise audio (loudnorm — two-pass for best results)
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:v copy output.mp4
```

### Mix multiple audio tracks (🐢)

```bash
ffmpeg -i input.mp4 -i bg_music.mp3 -filter_complex \
  "[0:a][1:a]amix=inputs=2:duration=longest:dropout_transition=2[a]" \
  -map 0:v -map "[a]" -c:v copy output.mp4
```

**Gotcha:** Use `weights` to balance: `amix=inputs=2:weights=1 0.3` for 70% reduction on second track.

### Fade audio in / out (🐢)

```bash
# 2s fade in, 3s fade out (on 30s video)
ffmpeg -i input.mp4 -af "afade=t=in:st=0:d=2,afade=t=out:st=27:d=3" -c:v copy output.mp4
```

### Audio delay / offset (🐢)

```bash
# Delay audio by 500ms
ffmpeg -i input.mp4 -filter_complex "[0:a]adelay=500|500[a]" -map 0:v -map "[a]" -c:v copy output.mp4
```

---

## 7. Format Conversion

### Common format conversions (🐢 unless same codec)

```bash
# MP4 to WebM (VP9 + Opus — best quality for web)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm

# MP4 to MOV
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mov

# MOV to MP4 (stream copy if possible)
ffmpeg -i input.mov -c copy output.mp4

# Any to MKV
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mkv

# AV1 encoding (slow but excellent compression)
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 30 -c:a libopus output.mp4
```

### Convert to GIF (🐢)

```bash
# Optimised GIF with palette generation (best quality)
ffmpeg -i input.mp4 -filter_complex \
  "[0:v]fps=15,scale=480:-1:flags=lanczos,palettegen[pal]; \
   [0:v]fps=15,scale=480:-1:flags=lanczos[x]; \
   [x][pal]paletteuse=dither=bayer:bayer_scale=5" \
  output.gif
```

**Note:** Two-pass palette generation gives much better colour. Adjust `fps` and `scale` for file size.

### Extract frames as images (⚡)

```bash
# Extract all frames as PNG
ffmpeg -i input.mp4 frame_%05d.png

# Extract 1 frame per second
ffmpeg -i input.mp4 -vf fps=1 frame_%05d.png

# Extract specific range
ffmpeg -i input.mp4 -vf "select=between(n\,0\,100)" -vsync vff frame_%05d.png
```

### Create video from image sequence (🐢)

```bash
# 30fps from numbered images
ffmpeg -framerate 30 -i frame_%05d.png -c:v libx264 -pix_fmt yuv420p output.mp4
```

### Extract single frame / thumbnail (⚡)

```bash
# Frame at 5 seconds
ffmpeg -i input.mp4 -ss 00:00:05 -frames:v 1 -q:v 2 thumbnail.jpg

# Best quality thumbnail at specific time
ffmpeg -i input.mp4 -ss 00:00:05 -frames:v 1 -q:v 1 thumbnail.png
```

---

## 8. Advanced

### Picture-in-picture (PIP) (🐢)

```bash
# Small video overlaid on main video (bottom-right, 25% size)
ffmpeg -i main.mp4 -i pip.mp4 -filter_complex \
  "[1:v]scale=iw*0.25:-1[pip];[0:v][pip]overlay=W-w-20:H-h-20" \
  -c:a copy output.mp4
```

### Side-by-side / split screen (🐢)

```bash
# Horizontal split (two videos side by side)
ffmpeg -i left.mp4 -i right.mp4 -filter_complex \
  "[0:v]scale=960:1080:force_original_aspect_ratio=decrease,pad=960:1080:(ow-iw)/2:(oh-ih)/2[left]; \
   [1:v]scale=960:1080:force_original_aspect_ratio=decrease,pad=960:1080:(ow-iw)/2:(oh-ih)/2[right]; \
   [left][right]hstack=inputs=2[v]" \
  -map "[v]" -map 0:a output.mp4
```

### Split video into segments (⚡)

```bash
# Split into 30-second segments
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 30 -f segment -reset_timestamps 1 segment_%03d.mp4
```

### Slideshow from images with transitions (🐢)

```bash
# Simple slideshow (5 seconds per image, crossfade)
ffmpeg -framerate 1/5 -i img%03d.jpg -c:v libx264 -vf "fps=30,format=yuv420p" output.mp4

# With crossfade between images (requires explicit filter per image pair)
# For N images, create a concat with xfade between each:
ffmpeg -loop 1 -t 5 -i img001.jpg -loop 1 -t 5 -i img002.jpg -loop 1 -t 5 -i img003.jpg \
  -filter_complex \
  "[0:v]fps=30[v0];[1:v]fps=30[v1];[2:v]fps=30[v2]; \
   [v0][v1]xfade=transition=fade:duration=1:offset=4[x01]; \
   [x01][v2]xfade=transition=fade:duration=1:offset=8[outv]" \
  -map "[outv]" -c:v libx264 output.mp4
```

### Add metadata (⚡)

```bash
ffmpeg -i input.mp4 -metadata title="My Video" -metadata artist="imgnAI" -metadata comment="Generated video" -c copy output.mp4
```

---

## 9. Common Pipelines

### Generate → trim → add text → fade in/out

```bash
# Step 1: Trim generated video
ffmpeg -i generated.mp4 -ss 1 -to 8 -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart trimmed.mp4

# Step 2: Add text overlay and fades
ffmpeg -i trimmed.mp4 -filter_complex \
  "[0:v]fade=t=in:st=0:d=1,fade=t=out:st=6:d=1,drawtext=text='Generated by imgnAI':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=h-60[v]; \
   [0:a]afade=t=in:st=0:d=1,afade=t=out:st=6:d=1[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart final.mp4
```

### Join two generated videos with crossfade

**Note:** For crossfade operations, normalise both source videos first (see MANDATORY section above).

```bash
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex \
  "[0:v]scale=1920:1080,setsar=1,fps=30[v0]; \
   [1:v]scale=1920:1080,setsar=1,fps=30[v1]; \
   [v0][v1]xfade=transition=fade:duration=1:offset=4[outv]; \
   [0:a]asetpts=PTS-STARTPTS[a0]; \
   [1:a]asetpts=PTS-STARTPTS[a1]; \
   [a0][a1]acrossfade=d=1[outa]" \
  -map "[outv]" -map "[outa]" -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -crf 18 -preset medium -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart merged.mp4
```

### Add audio to a silent generated video

```bash
ffmpeg -i generated_video.mp4 -i music.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest video_with_audio.mp4
```

### Full pipeline: generate → crop 9:16 → add text → convert to GIF

```bash
# Crop to vertical 9:16
ffmpeg -i generated.mp4 -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0" -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart cropped.mp4

# Add text
ffmpeg -i cropped.mp4 -vf "drawtext=text='Made with imgnAI':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=h-50" -c:v libx264 -profile:v high -level 4.0 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 44100 -ac 2 -movflags +faststart text_overlay.mp4

# Convert to GIF
ffmpeg -i text_overlay.mp4 -filter_complex \
  "[0:v]fps=12,scale=360:-1:flags=lanczos,palettegen[pal]; \
   [0:v]fps=12,scale=360:-1:flags=lanczos[x]; \
   [x][pal]paletteuse" output.gif
```

---

## 10. Hardware Acceleration

### NVENC (NVIDIA)

```bash
# Encode with NVENC (much faster than software x264)
ffmpeg -i input.mp4 -c:v h264_nvenc -preset p4 -cq 23 -c:a aac output.mp4

# HEVC (H.265) with NVENC
ffmpeg -i input.mp4 -c:v hevc_nvenc -preset p4 -cq 28 -c:a aac output.mp4
```

**Check availability:**
```bash
ffmpeg -hide_banner -encoders | grep nvenc
```

### Quick Sync (Intel)

```bash
ffmpeg -i input.mp4 -c:v h264_qsv -preset medium -c:a aac output.mp4
```

### VAAPI (Linux AMD/Intel)

```bash
ffmpeg -i input.mp4 -c:v h264_vaapi -vaapi_device /dev/dri/renderD128 -c:a aac output.mp4
```

**Note:** Hardware encoders are faster but may produce slightly lower quality than `libx264` at equivalent bitrates. Use `-cq` (constant quality) mode for best quality/size tradeoff.

---

## 11. Quick Reference: Codec Flags

| Codec | Encode flag | Typical use |
|-------|------------|-------------|
| H.264 | `-c:v libx264` | Maximum compatibility |
| H.265/HEVC | `-c:v libx265` | Better compression, slower |
| VP9 | `-c:v libvpx-vp9` | WebM / web |
| AV1 | `-c:v libaom-av1` | Best compression, very slow |
| AAC | `-c:a aac` | Standard audio for MP4 |
| Opus | `-c:a libopus` | Best audio quality |
| MP3 | `-c:a libmp3lame` | Universal audio |

---

