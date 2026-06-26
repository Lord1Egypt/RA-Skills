# Technical Reference

## Scope

This skill performs privacy-oriented image metadata cleanup for files the user
owns or is authorized to process. It should only be used for images the user owns
or is authorized to process, for privacy protection and clean publishing.

## What the script removes

The script opens an input image with Pillow, applies EXIF orientation to the
pixel data, creates a fresh image object, clears Pillow-visible metadata, and
saves a new output file.

This process is expected to drop common file-level metadata such as:

| Metadata type | Notes |
|---|---|
| EXIF | Camera/device tags and orientation metadata. Orientation is applied before saving. |
| XMP | Adobe and application metadata when exposed through Pillow or dropped by re-encoding. |
| IPTC/Photoshop | Press/photo metadata when exposed through Pillow or dropped by re-encoding. |
| ICC profile | Color profile bytes are not copied to the sanitized output. |
| C2PA/JUMBF containers | Usually removed by re-encoding because original container chunks/segments are not copied. |

## Verification

After writing each output, the script reopens it and reports:

- Output dimensions.
- Output size in bytes.
- Common privacy metadata keys still visible through Pillow.
- Common provenance marker strings still visible in the file bytes, including
  `c2pa`, `C2PA`, `JUMBF`, `jumb`, and `caBX`.

This verification is intentionally conservative. A marker-string scan can miss
custom encodings and can theoretically flag marker-like text in pixel data. It
is a quality check, not a formal proof that every possible provenance signal was
removed.

## Output behavior

Default format is `preserve`:

- JPEG inputs are written as JPEG.
- Other supported inputs are written as PNG.

Folder input writes outputs to `metadata-cleaned/` by default. Single-file input
writes a sibling copy such as `photo-clean.png` or `photo-clean.jpg`. Explicit
output paths are allowed, but existing explicit outputs are not overwritten
unless `--overwrite` is supplied. The input file itself is never overwritten.

## Known limitations

- Pixel-level watermarks, fingerprints, or model-specific invisible signals are
  not removed.
- External platform records and server-side provenance are outside the image
  file and cannot be changed by this script.
- Removing ICC profiles can affect color management in some workflows.
- JPEG output is lossy. PNG output is preferred when preserving pixel fidelity
  matters.
- Transparent images written as JPEG are composited onto a white background.
