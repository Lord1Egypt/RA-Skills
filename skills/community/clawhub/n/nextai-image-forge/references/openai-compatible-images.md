# OpenAI-Compatible Image APIs

This open-source NextAI edition of ImageForge uses the fixed NextAI Code API base and the OpenAI-compatible image endpoints used by this skill:

- `POST /v1/images/generations`
- `POST /v1/images/edits`

The API URL is fixed to `https://www.nextai-code.com/v1`. ImageForge appends `/images/generations` or `/images/edits`. Any configured URL outside `https://www.nextai-code.com` / `https://www.nextai-code.com/v1` is rejected before use.

ImageForge has deterministic/unit and local skill discovery validation so far. Do not report a live provider as validated until generation or editing has been tested against that provider.

## Authentication

Requests use bearer token authentication:

```text
Authorization: Bearer <API key>
```

The API key must come from the user secret file or `IMAGE_FORGE_API_KEY`. Never place keys in the skill folder, Git, logs, or replies.

## Generation request

After the Image Brief Gate is approved, run:

```bash
python3 "$IMAGE_FORGE_SCRIPT" generate --brief '<approved brief>' --prompt '<prompt>'
```

The helper rejects generation without either `--brief '<approved brief>'` or `--direct`.

Payload basics:

```json
{
  "model": "gpt-image-2",
  "prompt": "<prompt>",
  "size": "1024x1024",
  "n": 1
}
```

Optional generation fields supported by the helper:

- `--model`: per-command model override.
- `--size`: output size, default `1024x1024`.
- `--quality`: forwarded when provided.
- `--n`: number of images requested, default `1`.
- `--output-dir` and `--output-name`: local output controls.

## Edit request

After the Image Brief Gate is approved, run:

```bash
python3 "$IMAGE_FORGE_SCRIPT" edit --brief '<approved brief>' --image '<path>' --prompt '<instruction>'
```

The helper rejects edits without either `--brief '<approved brief>'` or `--direct`.

Image edits use `multipart/form-data` with these fields:

- `model`: default `gpt-image-2`, unless configured differently.
- `prompt`: text instruction.
- `size`: default `1024x1024`.
- `image`: one uploaded image file; repeated `--image` values are sent as repeated `image` fields.

Optional edit fields supported by the helper:

- `--model`: per-command model override.
- `--size`: output size, default `1024x1024`.
- `--output-dir` and `--output-name`: local output controls.

## Response expectation

ImageForge expects JSON responses with base64 image data:

```json
{
  "data": [
    {"b64_json": "<base64 PNG bytes>"}
  ]
}
```

Each `data[].b64_json` item is decoded and written as a `.png` file directly in the project root by default. ImageForge does not create output sidecar `.json` files. URL-only image responses are treated as `protocol_error` by this helper.

## Supported configuration

Default model is `gpt-image-2`, but it must still be written during setup before generation or editing can proceed. Users can change only the model/key with:

- the first-use local setup page started by `python3 "$IMAGE_FORGE_SCRIPT" ensure-ready`
- CLI fallback setup through `python3 "$IMAGE_FORGE_SCRIPT" setup`
- `IMAGE_FORGE_MODEL=<model>`

Other configuration sources:

- `IMAGE_FORGE_API_URL`: overrides the project API URL.
- `IMAGE_FORGE_API_KEY`: overrides the user secret file.
- `.image-forge/config.json`: stores non-secret project config such as locked `apiUrl`, `defaultModel`, and optional `outputDir`; default output directory is the project root.
- `~/.config/image-forge/secrets.json`: stores the user API key with restricted file permissions.

## Edit limitations

The safest supported edit mode is one source image plus one text instruction. ImageForge accepts repeated `--image` values and passes them through as repeated form fields, but provider support for multi-image edits is not guaranteed.

If a provider rejects a multi-image edit with a provider or protocol error, ImageForge reports `multi_image_unsupported` and the user should retry with one `--image`.
