# API notes

This skill targets image APIs that expose only image routes.

## Supported endpoints

- `POST /v1/images/generations`
- `POST /v1/images/edits`

## Authentication

Pass credentials through environment variables and attach them as a bearer token in requests.

Recommended variables:

- `IMAGE_API_BASE_URL`
- `IMAGE_API_KEY`

## Generation request

Typical JSON body:

```json
{
  "prompt": "a cute robot making tea",
  "size": "1024x1024",
  "n": 1
}
```

## Edit request

Typical multipart fields:

- `image`: source image file
- `mask`: optional mask file
- `prompt`: edit instruction
- `size`: optional size
- `n`: optional count

## Output behavior

The helper script prefers saving images locally.

- If the API returns `data[0].b64_json`, it decodes and writes a local file.
- If the API returns `data[0].url`, it downloads the file locally by default.
- Use `--keep-url` if a workflow explicitly prefers the remote URL.

Default output root:

- `output/grok-images/`

## Presets

Style presets:

- `anime`
- `cute`
- `photoreal`
- `cyberpunk`

Size presets:

- `square` → `1024x1024`
- `portrait` → `1024x1536`
- `landscape` → `1536x1024`

## Practical reminders

- Do not assume chat completions exist.
- Do not hardcode secrets into committed files.
- Prefer environment variables.
- If the target channel can send local images, prefer the downloaded local file.
