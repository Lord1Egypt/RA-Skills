# gpt-image-2-generation

> Generate images from text prompts using the **gpt-image-2** model on [WellAPI](https://wellapi.ai).

A ClawHub / OpenClaw-compatible agent skill that turns natural-language prompts into images by calling `POST https://wellapi.ai/v1/images/generations`, decoding the returned base64 image, and saving it to disk.

## Features

- Single-call text-to-image generation with `gpt-image-2`
- Configurable `size`, `quality`, `format`, `n`
- Secure local storage of the API key (`~/.config/gpt-image-2-generation/config.json`, mode `0600`)
- Friendly first-run onboarding that points the user to a free API key
- Pure-Python implementation, no third-party dependencies

## Get a free API key

Register at **https://wellapi.ai/register?channel=c_qqn3vdvc** to obtain a free WellAPI API key, then either:

```bash
export WELLAPI_API_KEY="sk-..."
```

or run the interactive helper which will save it for you:

```bash
python3 scripts/setup_api_key.py
```

## Usage

```bash
python3 scripts/generate_image.py --prompt "大海"
python3 scripts/generate_image.py \
  --prompt "A futuristic city skyline at dusk, cyberpunk style" \
  --size 1024x1024 \
  --quality high \
  --format png \
  --output ./city.png
```

The saved file path is printed on stdout.

## Request shape

```json
{
  "model": "gpt-image-2",
  "prompt": "大海",
  "n": 1,
  "size": "1024x1024",
  "quality": "low",
  "format": "jpeg"
}
```

Sent with `Authorization: Bearer <API_KEY>`.

## Response shape

```json
{
  "data": [{ "b64_json": "..." }],
  "output_format": "png",
  "size": "1024x1024",
  "quality": "low"
}
```

The skill writes the decoded bytes to the path given by `--output` (or an auto-generated one based on the timestamp).

## Requirements

- Python 3.7+
- Network access to `https://wellapi.ai`

## License

MIT
