# Supported Media Formats (Read-Only Reference)

This file describes the media formats recognized by Mallary's public media path. It intentionally contains no upload or publishing commands. Reading a format table is not authorization to transmit a local file or publish content.

## Agent Safety Boundary

Selecting local media for a later Mallary action can send the file bytes outside the local machine to Mallary storage, the Mallary CDN, and supporting hosting providers. The media can then be hosted at a public Mallary file URL.

- Start with read-only Mallary discovery.
- Do not use an upload as a format test or smoke test.
- Do not inspect or transmit more local file data than the user requested.
- Never transmit sensitive, regulated, customer, private, secret-bearing, or unrelated files.
- Before any transfer, make sure the local paths, target Dashboard profile, connected account, platform, message, timing, and expected result belong to a clear user request.
- Ask only when one of those material details is missing or ambiguous. Do not ask for a second confirmation after a clear publishing request.
- Execute the requested transfer once and never retry it automatically when the result is uncertain.

Executable upload and publishing syntax is intentionally omitted from this agent-facing reference.

## MIME Type Detection

Mallary infers the media type from the local filename extension. Renaming a file does not convert its contents and can cause a MIME mismatch. Keep the extension aligned with the file's real format.

## Supported Image Formats

| Extension       | MIME type    | Public media path |
| --------------- | ------------ | ----------------- |
| `.png`          | `image/png`  | Supported         |
| `.jpg`, `.jpeg` | `image/jpeg` | Supported         |
| `.webp`         | `image/webp` | Supported         |
| `.gif`          | `image/gif`  | Supported         |
| `.bmp`          | `image/bmp`  | Supported         |

Platform rules can be narrower than Mallary's accepted input formats. Check the selected destination's current limits before uploading media for the requested post.

## Supported Video Formats

| Extension       | MIME type          | Public media path |
| --------------- | ------------------ | ----------------- |
| `.mp4`          | `video/mp4`        | Supported         |
| `.mov`          | `video/quicktime`  | Supported         |
| `.webm`         | `video/webm`       | Supported         |
| `.mkv`          | `video/x-matroska` | Supported         |
| `.avi`          | `video/x-msvideo`  | Supported         |
| `.mpeg`, `.mpg` | `video/mpeg`       | Supported         |

## Unsupported Public Upload Targets

### Audio

| Extension | Detected fallback          | Public media path |
| --------- | -------------------------- | ----------------- |
| `.mp3`    | `application/octet-stream` | Not supported     |
| `.wav`    | `application/octet-stream` | Not supported     |
| `.ogg`    | `application/octet-stream` | Not supported     |
| `.m4a`    | `application/octet-stream` | Not supported     |

### Documents

| Extension | Detected fallback          | Public media path |
| --------- | -------------------------- | ----------------- |
| `.pdf`    | `application/octet-stream` | Not supported     |
| `.doc`    | `application/octet-stream` | Not supported     |
| `.docx`   | `application/octet-stream` | Not supported     |

Unknown extensions also fall back to `application/octet-stream` and are not normal public media targets. Convert an unsupported asset locally into a real image or video format only when the user requests that separate local change.

## Platform-Specific Media Notes

These are compatibility notes, not a user request to post.

### TikTok

- Video posts require exactly one video.
- Photo posts support up to 35 `jpg`, `jpeg`, or `webp` images.
- TikTok photo posts do not accept `png` images.

### YouTube

- A post requires exactly one video.
- Regular-video custom thumbnails can use `jpg`, `jpeg`, or `png` up to 50 MB.
- The recommended regular-video thumbnail dimensions are `1280x720` with a 16:9 ratio.
- For YouTube Shorts, YouTube may store the thumbnail but show a video frame instead. Mallary returns a warning because the YouTube API cannot confirm the cover viewers will see.

### Instagram

- Stories use exactly one image or video and do not support captions or follow-up comments.
- Reels use exactly one video.
- Carousels use 2 to 10 image or video items.
- Video and Reel covers can use a separate thumbnail.

### Facebook

- Video thumbnails can use `jpg`, `jpeg`, or `png` up to 10 MB.

### X

- A post supports up to 4 images, or 1 video, or 1 GIF.

### LinkedIn

- The current public path supports text-only posts or one image attachment.

### Bluesky

- A post can use up to four `jpg`, `jpeg`, `png`, or `webp` images, up to 2 MB each.
- A video post uses one `mp4` file, up to 300 MB.
- Do not mix images and video in one Bluesky post.
- Media items can include alt text for accessibility.

## Size and Provider Limits

Mallary's media path accepts files up to 5 GB. Each social platform applies separate type, duration, dimension, and size limits. A format accepted by Mallary can still be rejected by the destination platform.

## Read-Only Troubleshooting

- **Unsupported file type:** confirm the real extension and compare it with the tables above.
- **MIME mismatch:** verify that the extension matches the actual file contents; do not fix this by renaming alone.
- **File not found:** verify the path locally without transmitting the file.
- **No permission:** confirm that the current user can read the file without changing broad filesystem permissions.
- **Authentication error:** ask the user to restore the API key outside chat; never request or print the key.
- **Uncertain remote result:** inspect existing Mallary state and do not repeat the transfer automatically.

## Explicit Request Handoff

When the user clearly requests a media transfer or publish action, follow the request-handling rules in `SKILL.md`. Ask only for missing material details and do not require another confirmation. This file does not authorize or supply an executable state-changing workflow.
