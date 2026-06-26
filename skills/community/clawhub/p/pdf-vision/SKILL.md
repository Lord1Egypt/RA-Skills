---
name: pdf-vision
description: Extract text content from image-based/scanned PDFs using multiple vision APIs with automatic fallback. Supports Xflow (qwen3-vl-plus) and ZhipuAI (GLM-4.6V-Flash, GLM-5) vision models. This skill converts PDF pages to images and uses AI vision capabilities to extract structured text, tables, and content from scanned documents that cannot be processed with traditional text extraction methods.
license: MIT
---

# PDF Vision Extraction Skill (Enhanced)

## Overview

This skill handles **image-based or scanned PDFs** that contain no selectable text. It supports **multiple vision APIs** with automatic fallback:

### Primary Models
- **Xflow**: `qwen3-vl-plus` (your primary vision model)
- **ZhipuAI**: `glm-4.6v-flash` (free vision model with fallback support)
- **Fallback**: `glm-5` (text-only, but may work with some image prompts)

Unlike traditional PDF text extraction tools (`pdftotext`, `pdfplumber`) which only work on text-based PDFs, this skill can process:
- Scanned documents
- Image-only PDFs  
- Photographed documents
- Handwritten notes (with limitations)
- Complex layouts with tables and formatting

## Supported Models

### Vision-Capable Models
| Provider | Model | Type | Context | Free |
|----------|-------|------|---------|------|
| Xflow | `qwen3-vl-plus` | Vision + Text | 131K | ❌ |
| ZhipuAI | `glm-4.6v-flash` | Vision + Text | 32K | ✅ |
| ZhipuAI | `glm-5` | Text-only* | 128K | ❌ |

### Additional Text Models (for fallback)
| Provider | Model | Context | Free |
|----------|-------|---------|------|
| ZhipuAI | `glm-4-flash-250414` | 128K | ✅ |
| ZhipuAI | `cogview-3-flash` | 32K | ✅ |

*Note: `glm-5` is primarily text-only but may handle image prompts in some cases.

## Prerequisites

### 1. API Configuration
Your OpenClaw must be configured with both providers:

**Xflow Configuration** (already set up):
- `models.providers.openai.baseUrl`: `https://apis.iflow.cn/v1`
- `models.providers.openai.apiKey`: Your Xflow API key

**ZhipuAI Configuration** (update token):
- `models.providers.zhipuai.baseUrl`: `https://open.bigmodel.cn/api/paas/v4`
- `models.providers.zhipuai.apiKey`: Your ZhipuAI API token

### 2. Required System Tools
- `pypdfium2` Python library (for PDF to image conversion)
- `curl` (for API calls)
- `base64` (for image encoding)

### 3. Python Libraries (already installed)
```bash
pypdfium2
```

## Usage

### Automatic Fallback Mode (Default)
Uses Xflow first, falls back to ZhipuAI if needed:
```bash
./scripts/pdf_vision.py --pdf-path /path/to/document.pdf
```

### Specific Model Selection
Force a specific model for cost or performance reasons:
```bash
# Use free GLM-4.6V-Flash model
./scripts/pdf_vision.py --pdf-path document.pdf --model zhipuai/glm-4.6v-flash

# Use specific Xflow model  
./scripts/pdf_vision.py --pdf-path document.pdf --model openai/qwen3-vl-plus

# Short form (auto-detects provider)
./scripts/pdf_vision.py --pdf-path document.pdf --model glm-4.6v-flash
```

### Structured Data Extraction
```bash
./scripts/pdf_vision.py --pdf-path invoice.pdf --prompt "Extract as JSON: vendor, date, total" --model glm-4.6v-flash
```

### Multi-page PDF Handling
```bash
# Process page 3 specifically
./scripts/pdf_vision.py --pdf-path book.pdf --page 3 --output page3.txt
```

## Configuration

### Environment Variables
The skill reads configuration from your OpenClaw config file (`~/.openclaw/openclaw.json`):
- `models.providers.openai.baseUrl` & `apiKey`
- `models.providers.zhipuai.baseUrl` & `apiKey`

### Output Format
Returns extracted text content as a string. For structured data requests, the AI model will format output according to your prompt instructions.

## Examples

### Cost-Optimized Extraction (Free Model)
**Command:** `--model glm-4.6v-flash`
**Use case:** When you want to use free vision capabilities
**Result:** Good quality extraction at no cost

### High-Quality Extraction (Premium Model)  
**Command:** `--model qwen3-vl-plus`
**Use case:** When you need maximum accuracy and complex layout understanding
**Result:** Best possible extraction quality

### Automatic Fallback (Recommended)
**Command:** No `--model` flag
**Use case:** Production environments where reliability is key
**Result:** Uses best available model, falls back gracefully

## Model Comparison

### GLM-4.6V-Flash (Free)
- ✅ Completely free
- ✅ Good Chinese text recognition  
- ✅ Decent table structure preservation
- ⚠️ Lower context window (32K vs 131K)
- ⚠️ May struggle with very complex layouts

### Qwen3-VL-Plus (Premium)
- ✅ Superior image understanding
- ✅ Excellent table and structure recognition
- ✅ Larger context window (131K)
- ✅ Better handling of mixed languages
- ❌ Requires paid API access

## Limitations

- **Single page processing**: Currently processes one page at a time
- **Image quality**: Better results with higher resolution scans
- **Complex layouts**: May struggle with very dense or overlapping text
- **Handwriting**: Limited accuracy with handwritten content
- **File size**: Large PDFs may exceed API token limits

## Technical Implementation

The skill follows this workflow:
1. **PDF to Image**: Converts specified PDF page to PNG using `pypdfium2`
2. **Model Selection**: Chooses model based on user preference or fallback logic
3. **API Call**: Sends image + prompt to selected vision API endpoint
4. **Response Parsing**: Extracts and returns the AI-generated text content
5. **Fallback**: If primary model fails, tries alternative models

For debugging, temporary files are created in `/tmp/`:
- `/tmp/pdf_vision_page.png` - converted image
- `/tmp/pdf_vision_payload_*.json` - API request payload  
- `/tmp/pdf_vision_response_*.json` - API response

## Integration Notes

This skill complements the standard `pdf` skill:
- Use `pdf` skill for **text-based PDFs** (faster, no API cost)
- Use `pdf-vision` skill for **image-based/scanned PDFs** (requires vision API)

Both skills can be used together in a fallback pattern:
1. Try `pdf` skill first
2. If no text extracted, fall back to `pdf-vision` skill

## Cost Optimization Tips

1. **Use GLM-4.6V-Flash for routine tasks** - it's free and quite capable
2. **Reserve Qwen3-VL-Plus for complex documents** - when you need maximum accuracy
3. **Test both models on your document types** - choose based on your quality requirements
4. **Monitor API usage** - track which models you're using most

## Update Your GLM API Token

Replace the placeholder token in your config:
```bash
# Replace YOUR_ACTUAL_GLM_TOKEN with your real token
sed -i 's/YOUR_GLM_API_TOKEN_HERE/YOUR_ACTUAL_GLM_TOKEN/g' ~/.openclaw/openclaw.json
```