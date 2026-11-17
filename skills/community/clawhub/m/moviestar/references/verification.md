# Render verification

Verification should test the requested outcome, not merely that FFmpeg exited
successfully.

## Before the final render

1. Run `status` and inspect the resolved duration, source selection,
   composition, captions/overlays, and audio configuration.
2. Run `export --dry-run --out PATH`. Review the resolved output path, render
   status, warnings, and FFmpeg plan.
3. Make a quick `export --preview` or one or more short `watch --precise`
   renders when framing, motion, transitions, captions, or audio need review.
4. View returned image paths with the available image tool. Read video files
   with the available multimodal tool or sample them with `screenshot` and
   `watch`; do not ingest `--inline` Base64 as ordinary text.

## After the final render

- Run `moviestar probe FINAL.mp4` and confirm non-zero duration, expected
  dimensions, codecs, and audio/video streams.
- Capture representative first, middle, and final frames with
  `moviestar screenshot --file FINAL.mp4 --at TIMECODE`. Add boundary frames
  around important cuts, transitions, overlays, and scene changes.
- Check that captions are readable and synchronized, subjects remain framed,
  overlays are not clipped, and the final frame is intentional.
- When audio matters, inspect or listen to representative sections. Use
  `probe --loudness` or a MovieStar loudness report for measurable levels and
  clipping risk.
- Compare actual duration with the intended result. A frame of container drift
  can be normal for re-encoded output; larger unexplained drift needs review.

## Handoff

Report the absolute output path, duration, dimensions, stream presence, and the
visual/audio evidence inspected. Mention unresolved warnings or subjective
choices instead of presenting them as verified facts.
