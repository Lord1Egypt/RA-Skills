# Quality Gates

## Structural Issues

- `NO_FRAMES`: the action contains no detectable frame. Regenerate or replace that action.
- `FRAME_COUNT_MISMATCH`: confirm `expectedFrames`; if correct, regenerate only that action.
- `AMBIGUOUS_FRAME_OWNERSHIP`: increase spacing between frames or clarify the source layout. Do not guess component ownership.

## Content Issues

- `EMPTY_FRAME`: regenerate the affected action with every requested frame populated.
- `REFERENCE_PALETTE_DRIFT`: regenerate the action using the same reference. Do not palette-map away identity drift by default.
- `ACTION_SCALE_DRIFT`: regenerate with matching camera distance and character scale. Do not resize each action from its bounding box.
- `GROUND_DRIFT`: regenerate unstable poses or review deliberate airborne actions before overriding.
- `PIXEL_GRID_DRIFT`: regenerate with one consistent source pixel scale, or explicitly enable normalization when reduction is intended.
- `BACKGROUND_RESIDUE`: retry deterministic cleanup; if residue remains, regenerate that action on a flat solid background.
- `TRANSPARENT_RGB`: treat as a processing/output failure and do not publish until cleared.

## Targeted Regeneration Prompt

Use the original reference image on every retry. Replace bracketed fields without changing passed actions:

```text
Regenerate only the [ACTION_ID] animation for this exact character.
Use the attached reference as the sole identity, costume, weapon, palette, and proportion baseline.
Produce [FRAME_COUNT] ordered frames at a consistent camera distance and character scale.
Action semantics: [ACTION_DESCRIPTION]. Direction: [DIRECTION]. Playback: [FPS] FPS, [LOOP_OR_ONCE].
Keep the full character, weapon, and detached effects inside each frame with clear spacing between frames.
Use one perfectly flat solid background color not present in the character. No labels, borders, shadows, gradients, texture, or extra characters.
Do not redesign or simplify any passed visual detail.
```

After replacement, run the complete inspect, compile, audit, validate, and export sequence again. Preserve all passed source files unchanged.
