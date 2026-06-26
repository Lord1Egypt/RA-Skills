# 🎬 OpenLens Skill

AI Video Generation Portal with Raw Transparency - OpenClaw Skill Package.

## Features

- **Raw Transparency**: No content filtering - pure pass-through to your API
- **Prompt Refinement**: Use LLM to enhance prompts before generation
- **Image-to-Video**: Upload images and convert to video
- **Dual Mode**: GUI (Streamlit) + CLI
- **Local Save**: Auto-download to configured local path
- **Streaming Download**: Robust large file downloads with progress

## Quick Start

### GUI Mode

```bash
# Install dependencies
pip install streamlit requests tqdm

# Run GUI
streamlit run app.py
```

### CLI Mode

```bash
# Basic video generation
python3 cli.py --prompt "A sunset over ocean"

# With prompt refinement
python3 cli.py --prompt "A sunset" --refine --image_url "https://..."

# Custom output path
python3 cli.py -p "video prompt" -o ./myvideo.mp4
```

## Configuration

Edit `config.json` or use the GUI:

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

## File Structure

```
openlens-skill/
├── manifest.json        # Skill metadata
├── app.py              # Streamlit GUI
├── cli.py              # CLI handler
├── setup.sh            # Auto-installer
├── requirements.txt    # Dependencies
├── config.json         # User config
└── .streamlit/
    └── config.toml     # GUI theme
```

## OpenClaw Integration

This skill can be installed via ClawHub:

```bash
clawhub install openlens-skill
```

## Disclaimer

This tool is a raw transparency gateway. Use responsibly and comply with local laws.
