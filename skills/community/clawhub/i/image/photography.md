# Photography, Color, and Print

## Color Profiles

| Profile | Use For |
|---------|---------|
| `sRGB` | Web delivery, most marketplaces, social |
| `Adobe RGB` | Print workflows with wider gamut |
| `ProPhoto RGB` | High-end RAW editing and master files |

- Browsers and many upload pipelines effectively expect sRGB.
- Wide-gamut files exported for the web without conversion often look washed out or inconsistent.
- Embed the ICC profile when the destination respects color management.

## RAW and Non-Destructive Editing

- RAW files are source negatives; do not overwrite them.
- Keep edits in sidecars, catalogs, layered masters, or non-destructive instructions when possible.
- White balance corrections are safer in RAW than in JPEG.
- Different RAW converters can produce visibly different output from the same file.
- Keep at least one master export suitable for future edits before creating flattened delivery versions.
- Noise reduction, clarity, and sharpening should be balanced for the final destination; settings that feel dramatic on screen often print badly.

## Metadata and EXIF

Preserve when needed:
- Copyright and author data
- Editorial provenance
- Archive or legal context

Strip when appropriate:
- Public web publishing
- Sensitive location data
- Irrelevant camera metadata on lightweight delivery assets

GPS warning:
- Strip GPS before public delivery for homes, private locations, or sensitive subjects.

## Print Export Rules

| Setting | Web | Print |
|--------|-----|-------|
| Color space | sRGB | Adobe RGB or printer profile |
| Resolution | 72-150 PPI guidance | 300 PPI typical |
| Format | WebP/JPEG/PNG | TIFF or high-quality JPEG |
| Metadata | Minimal | Preserve if needed |

- Print work must care about physical size, bleed, sharpening target, and final output process.
- A web export that looks good on screen is not automatically print-safe.
- Ask whether the destination printer, lab, or publication has its own profile and export requirements before assuming a generic print preset.
- Soft-proofing or at least checking for gamut clipping is worth it when brand colors or skin tones must survive print.

## Retouching Traps

- Over-smoothing skin or texture until the file looks synthetic.
- Aggressive sharpening halos that only become obvious in print.
- Cropping too tightly and leaving no safe room for print trims or editorial layouts.

## Quality Control

Before delivery:

```
□ Orientation fixed
□ ICC profile intentional
□ No clipped highlights or blocked shadows
□ No obvious halos or oversharpening
□ Dust spots or sensor marks checked
□ Metadata decision made on purpose
```
