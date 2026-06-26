# PDF Vision Skill for OpenClaw

![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)

Extract text content from **image-based/scanned PDFs** using multiple vision APIs with automatic fallback. This skill converts PDF pages to images and uses AI vision capabilities to extract structured text, tables, and content from scanned documents that cannot be processed with traditional text extraction methods.

## 🚀 Features

- **Multi-model support**: Xflow (Qwen3-VL-Plus) + ZhipuAI (GLM-4.6V-Flash)
- **Automatic fallback**: Seamlessly switches between models if one fails
- **Free tier available**: GLM-4.6V-Flash provides free vision capabilities
- **Table structure preservation**: Maintains formatting and layout
- **Multi-language support**: Excellent Chinese and English text recognition
- **Cost optimization**: Use free models for routine tasks, premium for complex documents

## 📋 Prerequisites

### API Configuration
Add your API credentials to `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://apis.iflow.cn/v1",
        "apiKey": "your-xflow-api-key"
      },
      "zhipuai": {
        "baseUrl": "https://open.bigmodel.cn/api/paas/v4", 
        "apiKey": "your-zhipuai-api-key"
      }
    }
  }
}
```

### Python Dependencies
```bash
pip3 install pypdfium2
```

### System Tools
- `curl` (for API calls)
- `base64` (for image encoding)

## 🛠️ Installation

### Method 1: Git Clone (Recommended)
```bash
git clone https://github.com/your-username/pdf-vision-skill.git ~/.openclaw/workspace/skills/pdf-vision
```

### Method 2: Manual Download
1. Download the repository as ZIP
2. Extract to `~/.openclaw/workspace/skills/pdf-vision`

## 🎯 Usage

### Basic Usage
```bash
cd ~/.openclaw/workspace/skills/pdf-vision/scripts
./pdf_vision.py --pdf-path /path/to/document.pdf
```

### Specific Model Selection
```bash
# Use free GLM-4.6V-Flash model
./pdf_vision.py --pdf-path document.pdf --model glm-4.6v-flash

# Use premium Qwen3-VL-Plus model  
./pdf_vision.py --pdf-path document.pdf --model qwen3-vl-plus
```

### Custom Prompts
```bash
./pdf_vision.py --pdf-path invoice.pdf --prompt "Extract vendor, date, and total as JSON"
```

### Multi-page Documents
```bash
# Process page 3 specifically
./pdf_vision.py --pdf-path book.pdf --page 3 --output page3.txt
```

## 🔧 Configuration

The skill automatically reads your OpenClaw configuration from `~/.openclaw/openclaw.json` and extracts:
- Xflow API credentials (`models.providers.openai`)
- ZhipuAI API credentials (`models.providers.zhipuai`)

## 📊 Model Comparison

| Model | Provider | Cost | Context | Best For |
|-------|----------|------|---------|----------|
| `qwen3-vl-plus` | Xflow | Premium | 131K | Complex layouts, maximum accuracy |
| `glm-4.6v-flash` | ZhipuAI | Free | 32K | Routine tasks, cost optimization |

## 🔄 Automatic Fallback

The skill uses intelligent fallback logic:
1. **Primary**: Try Xflow Qwen3-VL-Plus first
2. **Fallback**: If Xflow fails, try ZhipuAI GLM-4.6V-Flash
3. **Manual override**: Force specific model with `--model` flag

## 📝 Examples

### Class Schedule Extraction
```bash
./pdf_vision.py --pdf-path class_schedule.pdf --prompt "Extract all courses, times, and locations as a table"
```

### Invoice Processing
```bash
./pdf_vision.py --pdf-path invoice.pdf --prompt "Extract as JSON: vendor_name, invoice_date, total_amount, line_items"
```

### Document Summarization
```bash
./pdf_vision.py --pdf-path research_paper.pdf --prompt "Summarize the main findings in 3 bullet points"
```

## 🐛 Troubleshooting

### Common Issues

**"API configuration error"**
- Verify your OpenClaw config has valid API keys
- Check that both Xflow and ZhipuAI providers are configured

**"No text extracted"**
- Try adjusting the prompt for better results
- Check image quality of scanned documents

**"Page number invalid"**
- PDF page numbers are 1-indexed in command line
- Use `--page 0` for first page or omit for default

## 📜 License

MIT License - Free to use, modify, and distribute.

## 🙏 Acknowledgments

Built for [OpenClaw](https://openclaw.ai) - The open-source AI assistant platform.

---

**Note**: Replace `your-username` in the git clone URL with your actual GitHub username when you create the repository.