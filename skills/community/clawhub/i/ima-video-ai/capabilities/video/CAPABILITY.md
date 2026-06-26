# Video Capability

## Responsibility

This capability owns all shipped media generation in this repo:

- `text_to_video`
- `image_to_video`
- `first_last_frame_to_video`
- `reference_image_to_video`

## Owning Code

- `scripts/ima_runtime/capabilities/video/routes.py`
- `scripts/ima_runtime/capabilities/video/models.py`
- `scripts/ima_runtime/capabilities/video/params.py`
- `scripts/ima_runtime/capabilities/video/executor.py`

It depends on shared catalog, client, input, config, and error modules, but it is the only capability package in the current repo.

## Read Order

1. `references/scenarios.md`
2. `references/routing.md`
3. `references/models.md`
4. `references/params.md`
5. `references/parameter-tuning.md`

## Boundary

- capability code decides video task type, model binding, video-only param shaping, and execution
- shared code owns product-list fetch, create/poll HTTP calls, input upload, prefs, and error translation
- non-video features are out of scope for this repo
