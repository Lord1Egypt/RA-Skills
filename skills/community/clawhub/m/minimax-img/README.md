# MiniMax Image Generation Skill

Generate images from text prompts using MiniMax's `image-01` model.

## Setup

1. Install:
   ```bash
   clawhub install minimax-image
   ```

2. Set your API key:
   ```bash
   export MINIMAX_API_KEY=your_key_here
   ```

3. Get your API key at: https://platform.minimax.io

## Usage

```bash
python scripts/minimax_media.py image "A futuristic city at sunset"
```

Returns the local PNG file path and a URL to the generated image.

## Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| MINIMAX_API_KEY | Yes | - |
| MINIMAX_BASE_URL | No | https://api.minimax.io |

## License

MIT
