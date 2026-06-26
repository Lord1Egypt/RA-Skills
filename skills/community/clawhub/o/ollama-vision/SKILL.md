# Ollama Vision Skill

本地视觉分析技能，调用 Ollama 的 qwen3-vl:4b 模型分析图片。

## Description

此技能允许在保留 Kimi 作为主对话模型的前提下，使用本地部署的 Ollama 视觉模型（qwen3-vl:4b）分析图片内容。支持 OCR、图片描述、文字提取等功能。

## Requirements

- Ollama 必须已安装并运行
- qwen3-vl:4b 模型必须已下载（或自动下载）
- Python 3.8+ 环境
- Pillow 库（用于图片压缩：`pip install Pillow`）

## Features

- **自动压缩**：超过 2MB 的图片会自动压缩后再分析
- **多模式分析**：describe（描述）、ocr（文字提取）、extract（自定义提取）
- **临时文件清理**：压缩产生的临时文件会自动删除
- **质量优先**：优先降低 JPEG 质量，必要时缩小尺寸

## Tools

### analyze_image

分析图片内容，支持多种分析模式。

**参数：**
- `image_path` (string, required): 图片文件的完整路径
- `mode` (string, optional): 分析模式，可选值：
  - `"describe"` - 详细描述图片内容（默认）
  - `"ocr"` - 提取图片中的所有文字
  - `"extract"` - 根据自定义提示词提取特定信息
- `prompt` (string, optional): 当 mode="extract" 时的自定义提示词

**返回：**
- 分析结果的文本字符串

**示例：**
```python
# 描述图片
analyze_image(image_path="C:\\path\\to\\image.jpg")

# OCR 提取文字
analyze_image(image_path="C:\\path\\to\\image.jpg", mode="ocr")

# 自定义提取
analyze_image(
    image_path="C:\\path\\to\\image.jpg", 
    mode="extract", 
    prompt="提取图片中的表格数据"
)
```

## Usage Flow

1. 用户发送图片消息
2. Agent 检测到图片，调用 analyze_image 工具
3. 工具调用本地 Ollama qwen3-vl:4b 模型分析
4. 返回分析结果给用户

## Notes

- 首次使用 qwen3-vl:4b 时会自动下载模型（约 2-3GB）
- 分析时间取决于图片大小和复杂度（通常 5-30 秒）
- 需要足够的显存（4B 模型建议 6GB+）
