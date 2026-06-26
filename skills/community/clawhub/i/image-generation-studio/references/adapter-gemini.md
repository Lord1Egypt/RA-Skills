# Gemini adapter

Use this reference when the selected provider uses `adapter: "gemini"`, or when the user mentions Gemini, Google GenAI, Nano Banana, `gemini-*` image models, search grounding, thinking, streaming, or multi-image composition.

The implementation lives in `{baseDir}/scripts/generate.py` under `gemini_generate`.

## Request shape

The adapter uses the Google GenAI SDK:

- client: `google.genai.Client`
- method: `client.models.generate_content(...)` or `generate_content_stream(...)`
- custom endpoint: `--api-url` / provider `api_url` is passed as `types.HttpOptions(base_url=..., api_version="v1beta")`
- API key: required through `--api-key`, env var, or provider config

For text-to-image, `contents` is the prompt string. For edits/composition, `contents` is all input images followed by the prompt.

## Supported operations

- Text-to-image generation.
- Image editing with input images.
- Multi-image composition with up to 14 input images.
- Native aspect ratio control.
- Native image size control via `1K`, `2K`, `4K`.
- Optional streaming text output.
- Nano 2-only search grounding and thinking controls.

## Relevant CLI options

| Option | Behavior |
| --- | --- |
| `--provider` | Selects a config provider whose adapter is `gemini`. |
| `-m`, `--model` | Gemini model ID or user-defined alias from `config.json`. |
| `-p`, `--prompt` | Required prompt or edit instruction. |
| `-f`, `--filename` | Required output path. Extension controls final file format; parent directories are created automatically. |
| `-i`, `--input` | Repeatable input image path. Up to 14 images. Enables edit/composition. |
| `-r`, `--resolution` | Passed as native `image_size`; valid values are `1K`, `2K`, `4K`. |
| `--aspect-ratio` | Passed as native image aspect ratio. |
| `--system-prompt`, `--system` | Passed as native `system_instruction`. |
| `--search` | Nano 2 only. Adds Google Search grounding. Values: `web`, `image`, `both`. |
| `--thinking` | Nano 2 only. `minimal` maps to thinking budget `0`; `high` maps to `-1`. |
| `--stream` | Uses `generate_content_stream`; prints text chunks live, saves image at the end. |

## Ignored or irrelevant options

The script warns and ignores OpenAI-compatible image fields for this adapter: `--size`, `--number`, `--quality`, `--output-format`, `--output-compression`, `--background`, `--moderation`, `--response-format`, and `--action`.

Do not recommend them for Gemini unless the user is intentionally passing provider-specific flags through a custom wrapper, which this script does not do.

## Advanced features (search and thinking)

`--search` and `--thinking` require the model alias to declare the corresponding capabilities in `config.json`:

```json
{
  "models": {
    "my-nano2": {
      "provider": "gemini",
      "model": "gemini-3.1-flash-image-preview",
      "capabilities": ["search", "thinking"]
    }
  }
}
```

If the user requests search grounding or thinking without declared capabilities, the script warns and ignores those flags. These features are currently supported by models like `gemini-3.1-flash-image-preview` (Nano 2).

## Output handling

The adapter scans returned parts for text and image inline data:

- text parts are printed as `Model: ...` in non-streaming mode, or streamed live with `--stream`
- inline image data is base64-decoded if needed
- image bytes are saved through the common output helper

The common output helper opens provider bytes with Pillow and re-encodes according to the `-f` extension; unknown extensions save as PNG.

If no image data appears, the script exits with `Gemini returned no image data.`

## Good command patterns

Text-to-image:

```bash
uv run {baseDir}/scripts/generate.py --provider my-gemini -p "cinematic mountain village at sunrise" -f outputs/village.png -r 2K --aspect-ratio 16:9
```

Edit or composition:

```bash
uv run {baseDir}/scripts/generate.py --provider my-gemini -p "place the product on the marble table" -f outputs/composite.png -i product.png -i table.jpg
```

Nano 2 with search and thinking (requires capabilities declared in config.json):

```bash
uv run {baseDir}/scripts/generate.py -m my-nano2 -p "poster for a real 2026 Tokyo jazz festival mood" -f outputs/poster.png --search web --thinking high --stream
```

Where `my-nano2` is a user-defined alias in `config.json`:
```json
{
  "models": {
    "my-nano2": {
      "provider": "gemini",
      "model": "gemini-3.1-flash-image-preview",
      "capabilities": ["search", "thinking"]
    }
  }
}
```

## Common failure causes

- Missing API key for the selected provider.
- Input image path does not exist or cannot be opened by Pillow.
- More than 14 input images.
- Asking for `--search` / `--thinking` on a model other than Nano 2.
- Custom `api_url` does not expose the Google GenAI `v1beta` API shape.
