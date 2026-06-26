---
name: minimax-cp
description: 使用 MiniMax Coding Plan API 进行网页搜索和图像理解。当用户要求搜索信息、查找资料、或者询问实时内容时使用搜索功能；当用户要求识图、分析图片、描述图片内容时使用 understand_image 功能。触发词：搜索、查找、search、look up、识图、分析图片、图片里是什么
---

# MiniMax Web Search & Vision

使用 MiniMax Coding Plan MCP 进行网页搜索和图像理解。

## 搜索

```bash
python3 scripts/mmsearch.py "<搜索关键词>"
```

## 识图

```bash
python3 scripts/mmvision.py "<提示词>" "<图片路径或URL>"
```

**支持的图片格式**：JPEG, PNG, WebP

**示例：**
```bash
# 描述图片内容
python3 scripts/mmvision.py "描述这张图片" /path/to/image.png

# 提取图片中的文字
python3 scripts/mmvision.py "提取图片中的所有文字" https://example.com/image.jpg

# 分析图片内容
python3 scripts/mmvision.py "这张图片里有什么？" image.jpg
```

## 脚本说明

- `scripts/mmsearch.py` — 调用 `web_search` 工具
- `scripts/mmvision.py` — 调用 `understand_image` 工具

**依赖：**
- `uvx` (Python 包运行器)
- `minimax-coding-plan-mcp`
- `MINIMAX_API_KEY` 环境变量（已内置在脚本中）
