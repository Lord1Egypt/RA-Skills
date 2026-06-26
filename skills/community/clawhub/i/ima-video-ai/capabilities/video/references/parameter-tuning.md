# Video Parameter Tuning

This guide covers user-facing tuning for the current video runtime.

## First-Pass Defaults

Use these when you want the fastest path to a stable first result:

- `text_to_video`: `ima-pro-fast`, `duration=5`, `resolution=480p`
- `image_to_video`: `ima-pro-fast`, `duration=5`, `resolution=480p`
- `first_last_frame_to_video`: `ima-pro-fast`, `duration=5`, `resolution=480p`
- `reference_image_to_video`: `ima-pro-fast`, `duration=5`, `resolution=480p`

For Seedance reference mode, start with one reference image before adding video/audio references.

## Duration

Use shorter clips for first-pass validation and troubleshooting:

- `5` seconds: fastest and cheapest
- `10` seconds: better for motion beats and short product demos
- `15` seconds: only after the shorter pass is stable

Example:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_video \
  --model-id ima-pro-fast \
  --extra-params '{"duration":10}' \
  --prompt "camera dolly through a quiet museum hall" \
  --output-json
```

## Resolution

Use lower resolution first when you are debugging prompt, motion, or account budget:

- `480p`: cheapest first pass
- `720p`: standard review pass
- `1080P` / `1080p`: only when the selected model and live credit rules support it

Example:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type image_to_video \
  --model-id ima-pro-fast \
  --input-images ./product.jpg \
  --extra-params '{"resolution":"720p"}' \
  --prompt "slow product pedestal rotation" \
  --output-json
```

## Aspect Ratio

Aspect ratio is usually not part of the credit-rule selector, but it still has to match backend-supported values. Pass the exact catalog value.

Common values:

- `1:1`
- `4:3`
- `3:4`
- `16:9`
- `9:16`
- `21:9`
- `adaptive` or `auto` for some Seedance product leaves

Example:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type first_last_frame_to_video \
  --model-id ima-pro \
  --input-images ./first.png ./last.png \
  --extra-params '{"aspect_ratio":"9:16"}' \
  --prompt "vertical transition between these states" \
  --output-json
```

## Audio Generation Toggle

Seedance leaves expose an audio toggle in live catalog form config. Keep it enabled when you want generated sound, disable it when you want silent output.

Example:

```bash
python3 scripts/ima_runtime_cli.py \
  --task-type text_to_video \
  --model-id ima-pro-fast \
  --extra-params '{"audio":false}' \
  --prompt "silent motion graphic logo reveal" \
  --output-json
```

If the current model leaf uses `generate_audio` instead of `audio`, trust the live catalog and pass the exact field name it exposes.

## Reference Media Tuning For Seedance

This applies only to `ima-pro` / `ima-pro-fast` on `reference_image_to_video`.

Recommended progression:

1. one reference image only
2. one reference image + one short reference video
3. one reference image + one short reference audio
4. image + video + audio only after the simpler cases succeed

When troubleshooting:

- remove reference video first if motion conflicts with the prompt
- remove reference audio first if timing or compliance checks start failing
- reduce all reference clips to `2~8s` before trying the `10~15s` edge

## Rule-Matching Parameters

The current runtime normalizes user values only where the live credit rules require canonical values.

In practice, this matters most for:

- `duration`
- `resolution`
- model-specific fields like `mode`

If a request fails with `6009` / `6010`, rerun with only:

- `--model-id`
- `--prompt`
- the minimum necessary media inputs

Then add one custom parameter back at a time.

## Cost-Aware Tuning Order

When a request is unstable or too expensive, reduce in this order:

1. `duration`
2. `resolution`
3. reference media count
4. audio generation toggle

Do not tune all four at once if you are trying to isolate a failure.
