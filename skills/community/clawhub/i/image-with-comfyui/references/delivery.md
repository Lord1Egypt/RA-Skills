# Delivery Reference (image-with-comfyui)

The SKILL.md core says "send the media, in the user's session, no paths". This
file holds the per-channel delivery formats and the staging steps. Open it when
you need the exact prefix for a channel.

## The one rule

After generating, **send the file**, don't describe it. A text line like "video
attachment" is NOT a send.

## Per-channel format

| Channel | Format | Example |
|---|---|---|
| WhatsApp | `MEDIA:` + absolute path | `MEDIA:/home/user/.openclaw/media/outbound/angel_video.mp4` |
| Telegram | `MEDIA:` or `filePath:` | varies by implementation |
| Discord | Direct attachment | varies by implementation |

> **Never invent a directive variant** — e.g. `/MIL` is not a real directive and will be shown to the user as literal text. Only the channel's documented format works; if you are not sure, re-read this file before replying.

## Staging steps (WhatsApp)

1. Copy the output to `~/.openclaw/media/outbound/` first.
2. **Pre-send verification — do this BEFORE the send message.** Run `ffprobe` on
   the file and only send if the checks pass. Never claim "ready" until this
   has passed:
   ```
   ffprobe -v error -show_entries format=duration -of \n   csv=p=0 <file>
   ffprobe -v error -show_entries stream=codec_name,width,height -of \n   csv=p=0 <file>
   ```
   - A zero/empty duration or a missing file means **do not send** — regenerate.
   - For **video** the codec must be **H.264 (avc1)**, 44.1 kHz audio. VLLM /
     FastH3 default output is **AV1** — WhatsApp will not play AV1. Transcode:
     ```
     ffmpeg -y -i <src> -c:v libx264 -crf 22 -s 640x360 -c:a aac -b:a 128k \n     -movflags +faststart <out>.mp4
     ```
     then `ffprobe` the `.mp4` again before sending.
   - For **audio** the codec must be **AAC** (mp3 files are accepted but
     transcoding AAC 44.1 kHz is safest — see the music skill). Never send a raw
     `.glb`, `.wav`/`.opus` that a channel may choke on.
3. Send via `MEDIA:/home/user/.openclaw/media/outbound/<filename>` (use absolute
   file path).
4. The `MEDIA:` line must be the **sole content** of the WhatsApp message — no
   `[[reply_to_current]]`, no text before it — otherwise WhatsApp splits the file
   and text into two messages (the file message then **does not deliver**, and
   only the text line goes through). For a caption use the
   `MEDIA:./file.ext caption=...` **single-line** form, and nothing else.
5. **Clean up:** delete the staged file after a successful send so sensitive
   generated media doesn't linger across sessions.

## pi2m / hyi2m (3D mesh) delivery

The two I2M entry points each produce different deliverables:

- **pi2m** (Pixal3D / Trellis2, default) produces **one** deliverable: the mesh
  **zip**. The trellis2 graph removes its own background internally, so there is
  no separate character image to send back. The GLB is kept at its natural units
  (delivery scale ×1) and packaged as `pi2m_<timestamp>.zip`.
- **hyi2m** (Hunyuan 3D v2.1) produces **two** deliverables, and both must go to
  the user:

1. **The extracted character image** (step-1 PNG) — send it **as an image**
   (an image message / attachment), never just its path. With `--extract none`
   the step-1 image *is* the user's own input, so there is nothing new to send.
2. **The mesh, as a zip** — the script first **scales the GLB in place by the
   delivery factor** (default ×3000 — the raw Hunyuan 3D v2.1 mesh is at a
   normalized unit scale, character ≈ 2 units, no declared units; `--scale 1`
   keeps it unscaled), then packages it (`hyi2m_<timestamp>.glb` →
   `hyi2m_<timestamp>.zip`). Send the **zip** as an attachment; never send the
   raw `.glb` on its own.

**Never render the mesh.** Do not convert the GLB to an image or video, or take
screenshots of a 3D viewer. A **third-party online GLB viewer link is allowed, only when the user explicitly asks** — it uploads the user's mesh to an external service, so never share one unprompted.
the user views/rotates the mesh themselves; the zip + character image remain the
primary delivery.

## Always

- Deliver in the **user's original request session/thread** — not a separate
  topic/group/thread unless explicitly told.
- The `MEDIA:` line is a **channel protocol directive** — the channel parses it, strips it, and delivers the file; it is **not** 'sending a raw path'. What is forbidden is pasting a **bare** file path, ComfyUI URL, or host info as visible message text (the user cannot act on it, and it leaks host-structure details). Paths travel only through the `MEDIA:` directive line or the channel's attachment field, never as free text.
- **Pre-send ffprobe check is mandatory** (not optional) for every video/audio
  send. The #1 failure mode in history was sending a claim of "done" before the
  file actually existed or was channel-compatible. Always ffprobe first, send
  only on success.
