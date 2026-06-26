# nano-gpt-cli

CLI and ClawHub/OpenClaw skill package for the NanoGPT API.

NanoGPT is an API for text, image, and video generation. According to the official docs, its text generation interface generally matches OpenAI standards, while the wider platform also exposes image, video, speech, and related endpoints. This repository is specifically for working with the NanoGPT API from the command line and from OpenClaw/ClawHub skill workflows.

Official docs: <https://docs.nano-gpt.com/>

## What’s here

- `cli/`: TypeScript CLI published as `nano-gpt-cli`
- `scripts/`: wrapper scripts for skill-driven workflows
- `SKILL.md`: root skill definition for OpenClaw/ClawHub
- `references/`: concise command and workflow docs

## Install

```bash
npm install
npm run build
cd cli
npm link
```

## Configure

Set your NanoGPT API token with an environment variable:

```bash
export NANO_GPT_API_KEY=YOUR_NANO_GPT_TOKEN
```

Or store it once in the local CLI config:

```bash
nano-gpt config set api-key YOUR_API_KEY
```

Optional overrides:

```bash
export NANO_GPT_MODEL=moonshotai/kimi-k2.5
export NANO_GPT_IMAGE_MODEL=qwen-image
export NANO_GPT_VIDEO_MODEL=kling-video-v2
export NANO_GPT_BASE_URL=https://nano-gpt.com
export NANO_GPT_OUTPUT_FORMAT=text
```

## Usage

```bash
nano-gpt prompt "Write one sentence proving this CLI is working."
nano-gpt chat
nano-gpt models --json
nano-gpt image "A red panda coding at a laptop" --output /tmp/red-panda.jpg
nano-gpt image "Turn this product photo into a watercolor ad" --image ./product.png --output /tmp/product-watercolor.png
nano-gpt video "A cinematic drone flyover of a neon coastal city at dusk" --duration 5 --output /tmp/neon-city.mp4
nano-gpt video "Animate this concept frame with subtle camera motion" --image ./concept.png --output /tmp/concept-shot.mp4
```

## Security

This CLI sends prompts and any explicitly provided `--image` or `--video` inputs to the NanoGPT API at the configured base URL, which defaults to `https://nano-gpt.com`.

If you run `nano-gpt config set api-key ...`, the token is stored locally in the per-user `nano-gpt-cli` config directory. You can avoid local storage by using `NANO_GPT_API_KEY` instead.

Do not pass sensitive local files unless you intend to upload them to NanoGPT. Image and video generation commands will read the local media paths you provide and transmit that data to the configured API endpoint.

## Development

```bash
npm run build
npm test
```

The CLI defaults to `moonshotai/kimi-k2.5` for text and `qwen-image` for image generation.

## License

MIT. See `LICENSE`.
