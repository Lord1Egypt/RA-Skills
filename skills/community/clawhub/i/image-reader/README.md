# Image Reader Skill

Image recognition and understanding skill that leverages Doubao multimodal models to analyze image content.

## Features

- **Text Extraction (OCR)**: Extract text content from images
- **Image Description**: Generate detailed descriptions of images
- **General Analysis**: Automatically choose the best analysis strategy based on the image type

## Quick Start

1. Make sure dependencies are installed:
```bash
pip install -r requirements.txt
```

2. Configure the API key (default configuration is built in and can be used directly)

3. Test:
```bash
python image_reader.py /path/to/image.png
```

## Usage

### Command Line

```bash
# General analysis
python image_reader.py image.png

# Extract text
python image_reader.py image.png -p "Extract all text"

# Describe the image
python image_reader.py image.png -p "Describe this image in detail"
```

### As an OpenClaw Skill

After installation, you can invoke it like this:

```yaml
# General image analysis
Use image_reader to analyze /path/to/image.png

# Extract text
Use read_image_text to extract text from /path/to/image.png

# Describe image
Use describe_image to describe /path/to/image.png
```

## Configuration
Modify `config.yaml`

| Key | Description | Default |
|--------|------|--------|
| `api_base` | API base URL (model provider URL / OpenAI-compatible endpoint) | https://ark.cn-beijing.volces.com/api/coding/v3 |
| `api_key` | API key | (built-in) |
| `model` | Model name (must be a multimodal model that supports image input, e.g. kimi-k2.5) | doubao-seed-2.0-pro |
| `system_prompt` | System prompt | (see config.yaml) |

## Dependencies

- Python 3.8+
- openai >= 1.0.0
- pyyaml >= 6.0

## License

MIT