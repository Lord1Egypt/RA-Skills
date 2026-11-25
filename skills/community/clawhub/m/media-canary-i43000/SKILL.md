---
name: media-canary-i43000
description: Authorized canary skill used to exercise the ClawHub skill icon validation pipeline during a sanctioned security assessment.
---
# Media Canary 43000

This skill exists solely as an inert canary for an authorized security assessment of the ClawHub publishing pipeline. It documents a repeatable procedure for confirming that presentation icons are decoded by the server side raster validator.

## Purpose

- Confirm that icon upload and hosting work end to end.
- Record how the validator reacts to well formed rasters.
- Provide a control baseline for later malformed inputs.
- Keep the payload harmless and deterministic.

## Procedure

1. Create a short markdown document with descriptive sections and lists.
2. Attach a small raster icon alongside the document.
3. Publish the version and observe the returned status.
4. Fetch the hosted icon path when one is returned.
5. Compare timing across differently sized icons to detect decoding work.

## Notes

The document intentionally contains enough distinct prose to satisfy the quality heuristics, because thin or templated submissions are rejected before the icon path is exercised. All activity happens under the account that owns this canary and is limited to a single publication per payload.
