# MiniMax Media Skill

Image generation and text-to-speech using MiniMax API.

## Features

- **Image Generation**: `image-01` model → PNG images
- **Text-to-Speech**: `speech-2.8-hd` model → MP3 audio

## Setup

1. Install the skill:
   ```bash
   clawhub install minimax-media
   ```

2. Set your API key:
   ```bash
   export MINIMAX_API_KEY=your_key_here
   ```

   Or add to your shell profile (~/.bashrc, ~/.zshrc, etc.)

3. Get your API key at: https://platform.minimax.io

## Usage

### Image Generation

```bash
python scripts/minimax_media.py image "A futuristic city at sunset"
```

Returns the local file path and URL of the generated image.

### Text-to-Speech

```bash
python scripts/minimax_media.py tts "Hello world" --voice female-tianmei
```

Available voices:

| Voice ID | Language | Gender |
|----------|----------|--------|
| female-tianmei | Chinese | Female |
| male-qn-qingse | Chinese | Male |
| male-qn-jianbin | Chinese | Male |
| English_expressive_narrator | English | Male |

Speed: `--speed 0.5` to `--speed 2.0` (default: 1.0)

## Environment Variables

| Variable | Required | Default |
|----------|----------|---------|
| MINIMAX_API_KEY | Yes | - |
| MINIMAX_BASE_URL | No | https://api.minimax.io |

## License

MIT
