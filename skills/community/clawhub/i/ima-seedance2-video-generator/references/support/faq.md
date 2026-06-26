# FAQ

## What does this skill do?

It generates Seedance 2.0 videos from text prompts and reference media. Supported reference inputs include images, videos, and audio files.

## Does `audio=true` mean I can get voiceover narration?

No. `audio=true` requests AI-generated ambient audio or sound effects. It does not guarantee human narration, voiceover, or preservation of an uploaded MP3 as the final soundtrack.

## Can I provide my own image, video, or audio file?

Yes. The skill supports:

- `--input-images` for general media input
- `--reference-image` for explicit image reference
- `--reference-video` for explicit video reference
- `--reference-audio` for explicit audio reference

## Do all input media need compliance verification?

Yes.

- Images: compliance verification enabled
- Videos: compliance verification enabled
- Audio: compliance verification enabled

Images, videos, and audio references all also go through strict preflight validation before task creation.

## When should I use `first_last_frame_to_video`?

Only when the user explicitly wants a first-frame / last-frame transition. If multiple media items are provided without explicit first-last-frame intent, the skill defaults to `reference_image_to_video`.

## Why does the skill default to `reference_image_to_video` for multiple media files?

Because multiple media items usually imply reference conditioning or consistency guidance, not a strict first-last-frame transition constraint.

## What is the recommended stdout mode for OpenClaw and IM integrations?

Use:

```bash
IMA_STDOUT_MODE=events
```

This keeps stdout reserved for structured JSON events.
