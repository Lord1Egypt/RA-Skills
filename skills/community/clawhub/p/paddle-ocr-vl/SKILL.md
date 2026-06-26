---
name: paddle-ocr-vl
description: GPU-accelerated document parsing and OCR via PaddleOCR-VL. Detects layout, recognizes Chinese/English text, tables, charts, and seals in images. Use when the user asks to OCR an image, extract text from a document, parse a screenshot, or recognize text in photos. Supports vertical classical Chinese text, modern newspaper layouts, and mixed-content documents.
version: 1.0.0
metadata:
  clawdbot:
    requires:
      env:
        - (none)
      bins:
        - docker
        - python3
        - nvidia-smi
    emoji: "🔍"
    homepage: https://github.com/user/paddle-ocr-vl-skill
    skills:
      - mcp-server
      - ocr
      - document-parsing
---

# PaddleOCR-VL Skill

GPU-accelerated document OCR using the PaddleOCR-VL model running inside an
ephemeral Docker container. Auto-detects NVIDIA GPU architecture (Blackwell
SM120 vs. standard) and selects the correct official image.

## When to Use

- User provides an image path and asks to "read", "OCR", or "extract text" from it
- User wants to parse a document screenshot, newspaper page, or classical text
- User asks about the content of an image file

## Architecture

This skill includes an **MCP server** (`server.py`) that exposes three tools:

| Tool | Purpose |
|---|---|
| `run_ocr` | OCR any image — provide an absolute path |
| `check_environment` | Verify Docker, GPU drivers, and image are ready |
| `run_demo` | Run OCR on bundled demo images to test the setup |

## Setup

### 1. Install the MCP Server

Add to `~/.config/Claude/claude_desktop_config.json` (Claude Desktop)
or `~/.claude/settings.json` (Claude Code):

```json
{
  "mcpServers": {
    "paddle-ocr-vl": {
      "command": "python3",
      "args": ["<INSTALL_DIR>/server.py"]
    }
  }
}
```

### 2. Pull the Docker Image (one-time)

```bash
# Blackwell GPU (RTX 50xx, B100/B200 — compute capability >= 12.0):
docker pull ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddleocr-vl:latest-nvidia-gpu-sm120

# Other NVIDIA GPU:
docker pull ccr-2vdh3abv-pub.cnc.bj.baidubce.com/paddlepaddle/paddleocr-vl:latest-nvidia-gpu
```

### 3. Verify

Call `check_environment` to verify everything is set up, then `run_demo` to
test on the bundled sample images.

## Bundled Demo Images

| File | Content |
|---|---|
| `demo/newspaper.png` | People's Daily article about China-Eritrea relations |
| `demo/classical_text.png` | Records of the Three Kingdoms, vertical classical Chinese |

## Requirements

- Docker with `nvidia-container-toolkit`
- NVIDIA GPU with drivers installed
- Python 3.10+ with `mcp` SDK (`pip install mcp`)

## Security & Privacy

- Images are processed inside an ephemeral Docker container (`--rm` flag)
- The container has no network access beyond `--network host` (needed for GPU)
- No data leaves the host machine
- The container is destroyed immediately after each OCR run

## External Endpoints

None. All processing is local.

## Official References

- PaddleOCR-VL docs: https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PaddleOCR-VL.html
- Blackwell-specific: https://www.paddleocr.ai/latest/version3.x/pipeline_usage/PaddleOCR-VL-NVIDIA-Blackwell.html
