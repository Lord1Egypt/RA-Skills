# Podcastfy Skill for OpenClaw

> Transform content into engaging AI-generated podcasts using Podcastfy.

## Overview

Podcastfy is an open-source Python package that transforms multi-modal content (text, images, websites, PDFs, YouTube videos) into engaging, multi-lingual audio conversations using GenAI.

It's like NotebookLM's podcast feature but open-source and programmatic.

## Prerequisites

### 1. Install Podcastfy

```bash
pip install podcastfy
```

### 2. Install FFmpeg (required for audio processing)

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### 3. Configure API Keys

Create a `.env` file with your API keys:

```bash
# Required: At least one LLM + one TTS
GEMINI_API_KEY=your_gemini_api_key    # Default: transcript generation
OPENAI_API_KEY=your_openai_api_key    # Default: TTS

# Optional (for other TTS models)
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

**Supported TTS Models:**
| Model | Quality | API Key Required |
|:---|:---|:---|
| OpenAI (default) | Good | Yes |
| ElevenLabs | Great (customizable) | Yes |
| Google (gemini/geminimulti) | Best (English only) | Yes |
| Edge | Basic | No |

**Recommended Setup:**
- Transcript: Gemini (free tier available)
- TTS: OpenAI or ElevenLabs

## Usage

### Basic Examples

#### From URLs (websites, articles)

```bash
python -m podcastfy.client --url https://example.com/article1 --url https://example.com/article2
```

#### From YouTube Video

```bash
python -m podcastfy.client --url https://youtube.com/watch?v=xxx
```

#### From PDF

```bash
python -m podcastfy.client --file path/to/document.pdf
```

#### From Images

```bash
python -m podcastfy.client --image path/to/image1.jpg --image path/to/image2.png
```

#### From Text

```bash
python -m podcastfy.client --text "Your raw text content here"
```

#### Longform (30+ minutes)

```bash
python -m podcastfy.client --url https://example.com/article --longform
```

#### Only Generate Transcript (no audio)

```bash
python -m podcastfy.client --url https://example.com/article --transcript-only
```

### Python API Usage

```python
from podcastfy.client import generate_podcast

# From URLs
audio_file = generate_podcast(
    urls=["https://example.com/article1", "https://example.com/article2"]
)

# From local files
audio_file = generate_podcast(
    file="path/to/urls.txt"
)

# From images
audio_file = generate_podcast(
    image=["path/to/image1.jpg", "path/to/image2.png"]
)

# Longform
audio_file = generate_podcast(
    urls=["https://example.com/article"],
    longform=True
)
```

### Advanced Options

```bash
# Custom conversation config
python -m podcastfy.client --url https://example.com/article --conversation-config config.yaml

# Use specific TTS model
python -m podcastfy.client --url https://example.com/article --tts-model elevenlabs

# Use local LLM for privacy
python -m podcastfy.client --url https://example.com/article --transcript-only --local

# Output to specific directory
python -m podcastfy.client --url https://example.com/article --output-dir ./my-podcasts
```

## Integration with OpenClaw

### Method 1: Direct CLI Execution

Use OpenClaw's exec tool:

```bash
python -m podcastfy.client --url https://example.com/article
```

### Method 2: Python Script Generation

Generate a Python script and run it:

```python
# Script will be created by the skill
from podcastfy.client import generate_podcast

audio = generate_podcast(
    urls=["<user_provided_url>"],
    output_dir="./podcasts"
)
```

## Use Cases for Dental/Medical Content

### Transform Articles into Podcasts

```bash
# Convert dental research articles to audio
python -m podcastfy.client --url https://www.dental.com/research/article
```

### Convert Course Materials

```bash
# Turn course PDFs into listenable content
python -m podcastfy.client --file ./dental-course/lecture1.pdf
```

### Create Patient Education

```bash
# Transform patient info sheets to audio
python -m podcastfy.client --text "Dental implant procedure explained..."
```

### Summarize YouTube Dental Videos

```bash
# Turn dental education videos into podcasts
python -m podcastfy.client --url https://youtube.com/watch?v=dental-education-video
```

## Output

- Audio file: MP3 format
- Transcript: TXT file (if `--transcript-only` or alongside audio)
- Default output directory: `./podcastfy_output/`

## Troubleshooting

### "ffmpeg not found"

```bash
# Install ffmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Linux
```

### "API key not found"

Make sure your `.env` file is in the correct directory and API keys are set.

### "Multi-speaker voices not available"

Google's multi-speaker TTS requires allowlisting. Use OpenAI or ElevenLabs instead.

## Resources

- [GitHub](https://github.com/souzatharsis/podcastfy)
- [Documentation](https://podcastfy.readthedocs.io/)
- [Web App](https://openpod.fly.dev/)
- [PyPI](https://pypi.org/project/podcastfy/)

---

**Note**: Requires Python 3.11+ and FFmpeg.