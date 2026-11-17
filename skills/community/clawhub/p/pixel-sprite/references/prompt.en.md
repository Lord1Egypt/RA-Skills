# Pixel Sprite · Generation Prompt Template (English)

Replace `[SUBJECT]` with the subject feature card. Adjust `32x32`, `6-8 colors` and `pure white background` to the user's parameters. Keep every other constraint verbatim.

```text
Convert the [SUBJECT] in the reference image into a low-resolution pixel illustration (Low Resolution Pixel Sprite).

Keep the subject's original design from the reference image exactly: overall shape, proportions, silhouette, structure, pose, color characteristics and identifying elements must all stay the same. Do not redesign the subject and do not change its design language; only convert the medium of expression into classic handmade pixel art.

Produce a retro-game-style pixel icon (Pixel Icon / Sprite Asset).

Use a 32x32 Pixel Sprite specification drawn on a strict 1-pixel grid. Every pixel is a uniform square; use nearest-neighbor upscaling so the result keeps crisp, hard-edged pixels. Avoid blurry pixels, anti-aliasing, gradient transitions, pixel filters and automatic pixelation effects.

Simplify the subject into a clean pixel structure with a clear silhouette and high readability. Express form through clean, continuous pixel clusters; avoid stray pixels and complex detail.

Use a limited palette of no more than 6-8 main colors. Show volume with flat color blocks and a simple one- or two-step light/shadow relationship; no complex lighting, no gradients.

Follow the classic 8-bit / 16-bit game sprite design language: cute, warm, nostalgic, comfortable and lively.

Output a single [SUBJECT] in pixel style, centered composition, pure white background, no text, no logo, no border, no extra decoration, no environment elements.
```

## Subject feature card example

```text
[SUBJECT]:
Category: an orange short-haired cat
Shape & proportions: round face, head about 1/2 of the body, body curled into a roughly horizontal oval
Pose & facing: lying down facing front, both front paws together in front, tail wrapping around from the right
Main colors: orange (#F2A03D), cream (belly and muzzle)
Secondary colors & shading: dark orange (#C9732A) for stripes and shadow, small pink nose
Identifying elements: dark M-shaped stripe on the forehead, small notch in the left ear, green eyes
Must keep: M stripe, left-ear notch, curled-up pose
```

## Parameter quick reference

| User asks for | Replace with |
|---|---|
| "smaller / favicon" | `16x16 Pixel Sprite`, palette down to 4-6 colors |
| "bigger / more detail" | `64x64 Pixel Sprite`, palette up to 10-12 colors |
| "transparent background" | `pure white background` → `transparent background (PNG alpha)`; keep white and say so if the host cannot do alpha |
| "dark / brand-color background" | `pure white background` → `solid <color name> background`, still no environment |
| "a set / several" | one image per subject, one feature card each, shared technical constraints |
