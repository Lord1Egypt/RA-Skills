# Image Capability

## Responsibility

This capability owns all image generation in this repo:

- `text_to_image`
- `image_to_image`

## Owning Code

- `scripts/ima_runtime/capabilities/image/routes.py`
- `scripts/ima_runtime/capabilities/image/models.py`
- `scripts/ima_runtime/capabilities/image/params.py`
- `scripts/ima_runtime/capabilities/image/executor.py`

## Boundary

- image capability code decides task routing, model binding, image-only param shaping, and execution
- shared code owns product-list fetch, upload flow, create/poll HTTP calls, prefs, and error translation
- non-image features are out of scope for this repo
