# Photo Editing Reference

## Color Theory for Film Look

- **Teal/Orange**: The most common Hollywood color grade. Shadows shift teal (cyan+blue), highlights shift warm orange. Creates pleasing skin tones + environmental contrast.
- **S-Curve**: Lift blacks slightly (not pure black), roll off highlights (not pure white), increase midtone contrast. Creates "film-like" response curve vs digital's linear response.
- **Film Grain**: Subtle noise in shadows mimics film stock. Use sparingly (σ=0.005-0.02).
- **Vignette**: Darkening edges draws eye to center. Classic cinema look uses subtle falloff.

## Effect Details

### Dehaze (Clarity)
Local contrast enhancement: Gaussian blur extracts low-frequency (haze/atmosphere) component. Subtracting it from original reveals detail hidden by haze. Boosting these mid-frequency details = clarity. Blur radius ~1/20 of image width works well for landscape/flowers.

### Vibrance vs Saturation
- **Saturation**: Uniform multiplier on all pixels. Can clip already-saturated areas.
- **Vibrance**: Per-pixel adaptive. Compute per-pixel saturation (max-min of RGB). Boost less saturated pixels more. Preserves skin tones and already-vibrant areas.

### Levels Adjustment
Similar to Photoshop's levels tool:
1. `shadows` — Set black point (clip or offset)
2. `highlights` — Set white point
3. `midtones` (gamma) — Power function: output = input^(1/gamma)
   - gamma > 1: brighten midtones
   - gamma < 1: darken midtones

### Split Toning
Apply different color casts to shadows and highlights separately:
1. Compute luminance mask
2. For each pixel, weight = how shadow/highlight it is
3. Add/subtract RGB per channel with weight

## Image Handling

- HEIC: Use `pillow-heif` → register opener → PIL loads natively
- Large images: Resize to 3840px max dim for processing (saves ~10x compute time)
- Quality: JPEG 95% is near-lossless for web use
- Format conversion: HEIC → JPEG loses EXIF data; use `piexif` if EXIF preservation needed

## Pipeline Design

Effects are composable pipeline stages. Order matters:

```
dehaze → grade → saturation → light → sharpen
```

Rationale: Dehaze first (clean the canvas), color grade second (set the mood), adjust saturation third (fine-tune), light effects fourth (atmosphere), sharpen last (final polish).
