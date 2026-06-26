# Error Policy

The runtime translates backend and transport failures into user-facing guidance:

- auth failures -> regenerate API key
- insufficient points -> subscription page
- missing image input for `image_to_image` -> ask for `--input-images`
- credit-rule mismatch -> remove custom params and retry defaults
- generated output violates explicit size / aspect-ratio constraints -> retry with the next compatible model or fail clearly
- timeout -> suggest lower size or quality

Raw backend payloads may still appear in debug logs, but they are not the primary user-facing explanation.
