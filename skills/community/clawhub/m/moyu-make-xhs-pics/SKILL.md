---
name: moyu-make-xhs-pics
description: 将Markdown文章转换为小红书风格的封面图、插图和配图。支持阿里百炼和MiniMax API，4种风格（fresh/warm/notion/cute），4种布局（balanced/list/comparison/flow）。
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/paulforcoding/make-xhs-pics
  env:
    required:
      - DASHSCOPE_API_KEY    # 阿里百炼 API Key（推荐）
      - MINIMAX_API_KEY      # MiniMax API Key（不推荐）
    primary: DASHSCOPE_API_KEY
    note: 推荐使用阿里百炼，DASHSCOPE_API_KEY
---

# moyu-make-xhs-pics - 小红书图片生成器

将 Markdown 文章自动转换为小红书风格的图片。

## 功能

- 🖼️ **三种图片类型**
  - 封面图：文章内容的高度提炼
  - 插图：完整表达文章内容 + 布局
  - 配图：随机章节的内容概括
- 🤖 **双 Provider**：MiniMax + 阿里百炼
- 🎨 **4 种风格**：fresh / warm / notion / cute
- 📐 **4 种布局**：balanced / list / comparison / flow
- 💧 **水印支持**：自动添加"AI 生成"

## 安装

```bash
pip install -r requirements.txt
```

## 环境变量

```bash
# MiniMax
export MINIMAX_API_KEY="your-key"

# 阿里百炼
export DASHSCOPE_API_KEY="your-key"
```

## 使用方法

```python
from src import generate_article_images

result = generate_article_images(
    article_path="path/to/article.md",
    cover_count=1,
    illustration_count=1,
    decoration_count=2,
    style="fresh",
    layout="auto",
    provider="dashscope"
)

if result["success"]:
    print(f"生成成功: {result['total']} 张图片")
    print(f"封面图: {result['covers']}")
    print(f"插图: {result['illustrations']}")
    print(f"配图: {result['decorations']}")
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| cover_count | 1 | 封面图数量 |
| illustration_count | 1 | 插图数量 |
| decoration_count | 2 | 配图数量 |
| style | fresh | 风格 (fresh/warm/notion/cute) |
| layout | auto | 布局 (balanced/list/comparison/flow/auto) |
| provider | minimax | API (minimax/dashscope) |

## License

GPL v3 - See LICENSE file

## 参考

提示词逻辑参照 [baoyu-skills](https://github.com/JimLiu/baoyu-skills)
