# MiniMax Image Skill Reference

## Setup

### 1. Get a MiniMax API Key

1. Go to MiniMax Dashboard or your Coding Plan settings
2. Find your API key for image generation
3. Copy the API key

### 2. Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:MINIMAX_API_KEY = "your-api-key-here"

# To persist across sessions, add to your PowerShell profile:
Add-Content $PROFILE "`n`$env:MINIMAX_API_KEY = 'your-api-key-here'"
```

**Windows (CMD):**
```cmd
set MINIMAX_API_KEY=your-api-key-here

# To persist, use System Properties > Environment Variables
```

**macOS/Linux:**
```bash
export MINIMAX_API_KEY="your-api-key-here"

# Add to ~/.zshrc or ~/.bashrc to persist
echo 'export MINIMAX_API_KEY="your-api-key-here"' >> ~/.zshrc
```

## API Reference

### Model

- **Model ID**: `image-01` (MiniMax's image generation model)
- **Endpoint**: `https://api.minimaxi.com/v1/image_generation`

### Image Sizes

| Size | Description |
|------|-------------|
| `1K` | 1024x1024 pixels - Default, balanced quality/speed |
| `2K` | 2048x2048 pixels - High resolution |
| `4K` | 4096x4096 pixels - Ultra high resolution |

### Aspect Ratios

| Ratio | Description |
|-------|-------------|
| `1:1` | Square - Default |
| `16:9` | Wide - Suitable for banners, hero images |
| `9:16` | Portrait - Suitable for mobile content |
| `3:4` | Portrait - Standard photo ratio |
| `4:3` | Landscape - Classic photo ratio |

## Script Parameters

### Python Script (Cross-Platform)

```bash
python scripts/generate_image.py <prompt> [output_path] [--size SIZE] [--aspect RATIO]
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `prompt` | Yes | - | Text description of desired image |
| `output_path` | No | `./generated-image.png` | Where to save the image |
| `--size` | No | `1K` | Image size (1K, 2K, or 4K) |
| `--aspect` | No | `1:1` | Aspect ratio (1:1, 16:9, 9:16, 3:4, 4:3) |

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MINIMAX_API_KEY` | Yes | - | Your MiniMax API key |
| `IMAGE_SIZE` | No | `1K` | Image size (1K, 2K, or 4K) |
| `IMAGEAspectRatio` | No | `1:1` | Aspect ratio (1:1, 16:9, 9:16, 3:4, 4:3) |

## Usage Examples

### Basic Generation

```bash
python scripts/generate_image.py "A serene mountain landscape at dawn"
```

### Custom Output Path

```bash
python scripts/generate_image.py "Minimalist logo design" "./assets/logo.png"
```

### High Resolution

```bash
python scripts/generate_image.py --size 2K "Detailed portrait" "./high-res.png"
```

### Wide Banner

```bash
python scripts/generate_image.py --size 2K --aspect 16:9 "Product banner" "./banner.png"
```

### Mobile Wallpaper

```bash
python scripts/generate_image.py --size 2K --aspect 9:16 "Mobile wallpaper" "./phone-bg.png"
```

## Prompt Tips

### For Best Results

1. **Be specific**: "A red sports car" vs "A cherry red 1967 Mustang convertible"
2. **Include style**: "in watercolor style", "photorealistic", "minimalist flat design"
3. **Mention lighting**: "golden hour lighting", "soft diffused light", "dramatic shadows"
4. **Specify composition**: "close-up", "wide angle", "from above", "centered"

### Advanced Prompting Techniques

These techniques produce significantly better results:

#### Lighting & Atmosphere
- "golden hour lighting with warm tones"
- "dramatic studio lighting with soft shadows"
- "ethereal glow with cool undertones"

#### Style References
- "in the style of minimalist flat design"
- "photorealistic with shallow depth of field"
- "abstract digital art with geometric shapes"
- "vintage film photography aesthetic"

#### Composition
- "centered subject with symmetric composition"
- "rule of thirds placement"
- "leading lines converging on subject"

## Troubleshooting

### "MINIMAX_API_KEY not set"
Ensure the environment variable is set in your current shell:

**Windows (PowerShell):**
```powershell
echo $env:MINIMAX_API_KEY  # Should show your key
```

**macOS/Linux:**
```bash
echo $MINIMAX_API_KEY  # Should show your key
```

### "API request failed with HTTP status 400"
- Check your prompt for special characters that may break JSON
- Ensure the prompt isn't empty
- Verify API key is valid

### "API request failed with HTTP status 429"
- Rate limited - wait a moment and retry
- Consider upgrading your API quota

### "No image data found in response"
- The model may have refused the prompt (content policy)
- Try rephrasing the prompt
- Check if the model returned an error message in the response

### Image is corrupted/won't open
- Ensure Python 3.6+ is installed
- Check if the full response was received (network issues)
- Verify output path is writable

### Windows-specific issues
- Make sure Python is in your PATH
- Use forward slashes or escaped backslashes in paths

## API Costs

Check MiniMax pricing for your plan. Image generation typically costs more than text generation.

## Limitations

- Maximum prompt length varies
- Some content types may be restricted by content policy
- Generated images are subject to MiniMax's terms of service
- Rate limits apply based on your API tier
