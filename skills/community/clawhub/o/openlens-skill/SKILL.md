# OpenLens Skill

AI Video Generation Portal with Raw Transparency for OpenClaw.

## Description

OpenLens is a minimalist AI video generation portal that serves as a raw transparency pass-through to your private video API. It bypasses content filtering restrictions and provides:

- **Prompt Refinement**: Use LLM to enhance prompts before video generation
- **Image-to-Video**: Upload images and convert to video
- **Dual Mode**: GUI (Streamlit) + CLI
- **Local Save**: Auto-download generated videos to configured local path
- **Streaming Download**: Robust large file downloads with progress bar

## Features

- Pure pass-through: no content filtering, no safety middleware
- Manual API configuration via GUI or config.json
- OpenAI-style /v1/video/generations protocol support
- Auto-polling for async video generation
- HTML5 video player with download button
- 18+ age verification gate
- CLI support for automation

## Installation

```bash
clawhub install openlens-skill
```

## Usage

### GUI Mode

```bash
streamlit run app.py
```

### CLI Mode

```bash
# Basic video generation
python3 cli.py --prompt "A sunset over ocean"

# With prompt refinement
python3 cli.py -p "A sunset" --refine

# Image to video
python3 cli.py -p "Character walking" -i "https://example.com/image.jpg"

# Custom output path
python3 cli.py -p "video prompt" -o ./myvideo.mp4
```

## Configuration

Edit `config.json` or use the GUI to set your API credentials:

```json
{
    "video_api_url": "YOUR_VIDEO_API_URL",
    "video_api_key": "YOUR_VIDEO_API_KEY",
    "text_api_url": "YOUR_TEXT_API_URL",
    "text_api_key": "YOUR_TEXT_API_KEY",
    "text_model": "gpt-4o",
    "default_save_path": "./outputs"
}
```

## CLI Options

| Flag | Description |
|------|-------------|
| `-p, --prompt` | Video description (required) |
| `-i, --image_url` | Image URL for I2V |
| `-o, --output` | Output file path |
| `-r, --refine` | Enable prompt refinement |
| `--resolution` | 720p or 1080p |
| `--duration` | 5, 10, or 15 seconds |

## Requirements

- Python 3.8+
- streamlit >= 1.28.0
- requests >= 2.31.0
- tqdm >= 4.66.0

## License

MIT

## Author

OpenClaw Community
