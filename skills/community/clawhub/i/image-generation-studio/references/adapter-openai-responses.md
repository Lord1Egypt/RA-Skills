# OpenAI Responses adapter

Use this reference when the selected provider uses `adapter: "openai_responses"`, or when the user mentions OpenAI Responses, `/v1/responses`, the `image_generation` tool, or image generation through a Responses-compatible proxy.

The implementation lives in `{baseDir}/scripts/generate.py` under `openai_responses_generate`.

## Request shape

The adapter uses stdlib HTTP JSON calls:

- endpoint: `POST {base}/v1/responses`
- base URL: `--api-url` / provider `api_url`, defaulting to `https://api.openai.com`
- authorization: `Authorization: Bearer <api_key>`
- payload includes `model`, `input`, and `tools: [{"type": "image_generation", "action": ..., "size": ..., "background": ...}]`

The prompt is sent as the top-level `input` string for text-to-image. When `-i / --input` images are provided, the adapter sends Responses content blocks with `input_text` followed by `input_image` data URLs. If a system prompt is configured, it is prepended to the user prompt with a blank line.

## Supported operations

- Text-to-image generation through the Responses API image generation tool.
- Image editing/redraw with one or more `-i / --input` images sent as `input_image` content.
- Action control through the image generation tool's `action` field.
- Size control through the image generation tool's `size` field.
- Quality and moderation control through the image generation tool's `quality` and `moderation` fields.
- Output format control through the tool's `output_format` field.
- Background control through the image generation tool's `background` field.
- Optional local JPEG/WebP saved-file quality control via `--output-compression`; this is not sent to the Responses API.
- Flexible image extraction from several possible response shapes.

## Unsupported operations in this wrapper

- Streaming is not implemented for this adapter.
- Search grounding and thinking flags are not implemented for this adapter.
- `--aspect-ratio` is not sent; use `--size` for shape control.
- OpenAI Images-specific fields other than `--size`, `--quality`, `--moderation`, and `--output-format` are not sent.

## Relevant CLI options

| Option | Behavior |
| --- | --- |
| `--provider` | Selects a config provider whose adapter is `openai_responses`. |
| `-m`, `--model` | Model ID or alias for the Responses-compatible provider. |
| `-p`, `--prompt` | Required prompt. |
| `-f`, `--filename` | Required output path. Extension controls final saved format; parent directories are created automatically. |
| `-i`, `--input` | Repeatable input image path. Sends each image as an `input_image` data URL and defaults action to `edit`. |
| `--action` | Sent into the image generation tool as `action`; values: `auto`, `generate`, `edit`. Defaults to `edit` with inputs, otherwise `generate`. |
| `-r`, `--resolution` | Maps to tool `size` when `--size` is not provided: `1K` → `1920x1088`, `1K-portrait` → `1088x1920`, `2K` → `2560x1440`, `2K-portrait` → `1440x2560`, `4K` → `3840x2160`, `4K-portrait` → `2160x3840`. |
| `--size` | Overrides resolution mapping. Examples: `auto`, `1920x1088`, `1088x1920`, `2560x1440`, `1440x2560`, `3840x2160`, `2160x3840`. |
| `--quality` | Sent into the image generation tool as `quality`; values: `auto`, `low`, `medium`, `high`. |
| `--moderation` | Sent into the image generation tool as `moderation`; values: `auto`, `low`. |
| `--background` | Sent into the image generation tool as `background`; values: `auto`, `transparent`, `opaque`. |
| `--output-format` | Sent as `output_format`; defaults from `-f` extension when possible (`jpg` becomes `jpeg`). |
| `--output-compression` | Not sent to the Responses API. When saving as JPEG/WebP, used locally as Pillow output quality. |
| `--system-prompt`, `--system` | Prepended to the prompt with a blank line. |

## Ignored or irrelevant options

The script warns and ignores `-n / --number`, `--aspect-ratio`, `--response-format`, `--search`, `--thinking`, and `--stream` for this adapter. Use `--size` for exact shape control. Use `--action auto` only when you want the model to decide between generation and editing from the prompt and inputs.

## Response handling

The adapter searches the JSON response recursively for image data. It first looks for an output item like:

```json
{
  "type": "image_generation_call",
  "result": "<base64 image>"
}
```

It also accepts common keys such as `b64_json`, `image_base64`, `base64`, `result`, or image-like objects with base64 `data`.

If no image data is found, the script exits with `OpenAI Responses returned no image data` and includes the first part of the raw response.

## Good command patterns

Text-to-image:

```bash
uv run {baseDir}/scripts/generate.py --provider my-responses -p "minimal product photo of a matte black lamp" -f outputs/lamp.webp -r 2K-portrait --quality high --moderation low --background opaque --output-compression 85
```

Edit with an input image:

```bash
uv run {baseDir}/scripts/generate.py --provider my-responses -p "change the jacket to black" -f outputs/edit.png -i person.png --action edit --quality high
```

With a model alias:

```bash
uv run {baseDir}/scripts/generate.py -m my-responses-image -p "wide cinematic desert road at night" -f outputs/road.webp -r 4K
```

## Common failure causes

- Provider/proxy exposes OpenAI Images endpoints but not `/v1/responses`.
- Selected model does not support the Responses `image_generation` tool.
- User tries a provider/model that accepts text-to-image but rejects Responses `input_image` editing.
- Provider ignores or rejects the requested `size`, `action`, or output fields inside the tool object.
- Response shape lacks extractable base64 image data.
