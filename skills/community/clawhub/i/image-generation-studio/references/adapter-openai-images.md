# OpenAI Images-compatible adapter

Use this reference when the selected provider uses `adapter: "openai_images"`, or when the user mentions OpenAI Images, `/v1/images/generations`, `/v1/images/edits`, `gpt-image-*`, Grok Imagine, xAI image generation, image edits through OpenAI-style endpoints, `response_format`, or temporary image URLs.

The implementation lives in `{baseDir}/scripts/generate.py` under `openai_images_generate`.

## Request shape

The adapter uses stdlib HTTP calls to OpenAI Images-compatible endpoints:

- text-to-image: `POST {base}/v1/images/generations` with JSON
- image edit: `POST {base}/v1/images/edits` with multipart form data
- base URL: `--api-url` / provider `api_url`, defaulting to `https://api.openai.com`
- authorization: `Authorization: Bearer <api_key>`

For edits, each input is sent as a repeated multipart field named `image[]`.

## Supported operations

- Text-to-image generation.
- Image editing when one or more `-i / --input` images are provided.
- Multiple edit input images at the wrapper level, although provider/model support varies.
- OpenAI Images-style size, quality, output format, moderation, compression, response format, and image count fields.
- URL image download with browser-like headers. Provider API credentials are only sent to API endpoints, never to returned image URLs.

## Relevant CLI options

| Option | Behavior |
| --- | --- |
| `--provider` | Selects a config provider whose adapter is `openai_images`. |
| `-m`, `--model` | Model ID or alias. |
| `-p`, `--prompt` | Required prompt or edit instruction. |
| `-f`, `--filename` | Required output path. Extension controls final saved format; parent directories are created automatically. |
| `-i`, `--input` | Switches from generations to edits and sends each input as `image[]`. |
| `-n`, `--number` | Sent as `n`; defaults to `1`. Multiple response images are saved as `file`, `file-2`, `file-3`, etc. |
| `-r`, `--resolution` | Maps to sizes when `--size` is not provided: `1K` → `1920x1088`, `1K-portrait` → `1088x1920`, `2K` → `2560x1440`, `2K-portrait` → `1440x2560`, `4K` → `3840x2160`, `4K-portrait` → `2160x3840`. |
| `--size` | Overrides resolution mapping. Examples: `auto`, `1920x1088`, `1088x1920`, `2560x1440`, `1440x2560`, `3840x2160`, `2160x3840`. |
| `--quality` | Sent as `quality`; values: `auto`, `low`, `medium`, `high`. |
| `--output-format` | Sent as `output_format`; defaults from `-f` extension when possible (`jpg` becomes `jpeg`). |
| `--output-compression` | Sent only when output format is not `png`. |
| `--moderation` | Sent as `moderation`; values: `auto`, `low`. |
| `--response-format` | Sent as `response_format`; values: `url`, `b64_json`. |
| `--system-prompt`, `--system` | Prepended to the user prompt with a blank line, because OpenAI Images has no system role. |

## Ignored or irrelevant options

The script warns and ignores `--aspect-ratio`, `--background`, `--action`, `--search`, `--thinking`, and `--stream` for this adapter. Use `--size` for exact shape control; generation vs edit is selected by whether `-i / --input` is provided.

## Response handling

The adapter expects `data[0]` to contain one of:

- `b64_json`: decoded directly and saved
- `url`: downloaded, then saved

If a provider supports it, prefer `--response-format b64_json` because URL downloads can fail when temporary URLs require browser cookies, auth, or short-lived access.

`revised_prompt` is printed when returned by the provider.

## Output handling

Provider image bytes are opened with Pillow and re-encoded according to the `-f` extension:

- `.png` → PNG
- `.jpg` / `.jpeg` → JPEG, flattening alpha onto white
- `.webp` → WEBP
- unknown extension → PNG

This means the upstream provider may return JPEG while the saved file is PNG or WEBP.

## Good command patterns

Text-to-image:

```bash
uv run {baseDir}/scripts/generate.py --provider my-images -p "studio product photo of a ceramic mug" -f outputs/mug.png --size 1536x1024 --quality high
```

Edit with base64 response:

```bash
uv run {baseDir}/scripts/generate.py --provider my-images -p "add neon rain reflections" -f outputs/edit.png -i source.png --response-format b64_json
```

xAI/Grok-style alias:

```bash
uv run {baseDir}/scripts/generate.py -m grok -p "surreal city skyline at dusk" -f outputs/grok.jpg -r 2K
```

## Common failure causes

- Provider or proxy exposes chat/responses endpoints but not `/v1/images/generations`.
- Selected model supports generation but not `/v1/images/edits`.
- Provider accepts only one edit input even though the wrapper sends repeated `image[]` fields.
- Temporary image URL cannot be downloaded; retry with `--response-format b64_json` when supported.
- Unsupported `size`, `quality`, `output_format`, or `moderation` value at the provider/model layer.
