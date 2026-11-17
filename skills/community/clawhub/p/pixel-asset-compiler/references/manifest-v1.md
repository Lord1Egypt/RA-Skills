# Manifest v1

## Input Contract

Use one reference image and one source image per semantic action. Paths must stay inside the input directory.

```json
{
  "schemaVersion": "1.0",
  "assetName": "blue_knight",
  "assetType": "character",
  "reference": "reference.png",
  "actions": [
    {
      "id": "idle",
      "name": "Idle",
      "source": "actions/idle.png",
      "fps": 6,
      "loop": true,
      "direction": "right",
      "expectedFrames": 4
    }
  ],
  "processing": {
    "background": "auto",
    "pixelNormalize": false,
    "sequenceNormalize": false,
    "alignFrames": true,
    "preserveDetachedElements": true
  }
}
```

## Semantic Fields

- `assetName`: lowercase safe slug used for file names.
- `assetType`: normally `character`, but may be another explicit caller-provided type.
- `reference`: the sole identity baseline.
- `actions[].id`: lowercase safe slug and stable engine animation ID.
- `actions[].name`: human-readable action label.
- `actions[].source`: image containing only that action.
- `actions[].fps`: positive playback FPS supplied by the user or upstream generator.
- `actions[].loop`: explicit playback behavior.
- `actions[].direction`: optional explicit direction; never infer it silently.
- `actions[].expectedFrames`: recommended when the generator promised a frame count.

## Processing Defaults

Use fidelity-preserving defaults. `pixelNormalize=false` and `sequenceNormalize=false` preserve source resolution and colors. Enable them only when the user explicitly requests a reduced, shared pixel grid and palette.

Keep `alignFrames=true` for stable Canvas, Ground Line, and Pivot. Keep `preserveDetachedElements=true` for weapons, attack arcs, projectiles, particles, hair, and capes that are disconnected from the body.

Do not add manual background colors, crop rectangles, canvas dimensions, or pivots unless inspection explicitly requests a supported override.
