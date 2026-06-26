---
name: minimax-image-understanding
description: 使用多模态大模型理解图片内容，生成业务含义描述。支持多种模型：(1) MiniMax VLM (2) OpenAI GPT-4V (3) Claude Vision。用于理解截图、图表、文档照片等，生成精准的文字描述。
---

# 图片理解

调用多模态大模型理解图片，生成精准的业务描述。

## 支持的模型

| 模型 | 环境变量 | 说明 |
|------|----------|------|
| MiniMax VLM | `MINIMAX_API_KEY`, `MINIMAX_API_HOST` | 默认，推荐用于中文理解 |
| OpenAI | `OPENAI_API_KEY` | GPT-4V |
| Anthropic | `ANTHROPIC_API_KEY` | Claude Vision |

## 使用方法

### 前提条件

设置对应模型的环境变量（至少一个）：

```bash
# MiniMax（默认）
export MINIMAX_API_KEY="your-minimax-key"
export MINIMAX_API_HOST="https://api.minimaxi.com"

# 或 OpenAI
export OPENAI_API_KEY="your-openai-key"

# 或 Anthropic
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### 调用脚本

```bash
python3 <skill>/scripts/understand_image.py <图片路径> [model] [prompt]
```

**参数：**
- 图片路径：本地图片文件（PNG、JPG、JPEG、GIF、WebP）
- model（可选）：`minimax`（默认）、`openai`、`anthropic`
- prompt（可选）：自定义提示词

### 示例

```bash
# 使用默认（MiniMax）
python3 ~/.openclaw/workspace/skills/minimax-image-understanding/scripts/understand_image.py /path/to/image.png

# 指定模型
python3 ~/.openclaw/workspace/skills/minimax-image-understanding/scripts/understand_image.py /path/to/image.png openai

# 自定义提示词
python3 ~/.openclaw/workspace/skills/minimax-image-understanding/scripts/understand_image.py /path/to/image.png minimax "描述图表中的数据趋势"
```

## 输出

直接输出图片的业务含义描述，不再罗列元素位置，聚焦数据内容和业务逻辑。
