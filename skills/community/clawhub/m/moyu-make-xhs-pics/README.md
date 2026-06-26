# moyu-make-xhs-pics

小红书图片生成器 - OpenClaw Skill

## 简介

输入一篇 Markdown 文章的本地路径
运行本 skill 讲自动该文件生成为小红书风格的1张封面图、1张插图和2张配图。

**提示词逻辑参照 [baoyu-skills](https://github.com/JimLiu/baoyu-skills)**

## 功能特性

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
# MiniMax-不太推荐，效果不太好
export MINIMAX_API_KEY="your-key"

# 阿里百炼-推荐
export DASHSCOPE_API_KEY="your-key"
```

## 使用方法

### Python API

```python
from src import generate_article_images

result = generate_article_images(
    article_path="path/to/article.md",
    cover_count=1,
    illustration_count=1,
    decoration_count=2,
    style="fresh",
    layout="auto",
    provider="minimax"
)

if result["success"]:
    print(f"生成成功: {result['total']} 张图片")
    print(f"封面图: {result['covers']}")
    print(f"插图: {result['illustrations']}")
    print(f"配图: {result['decorations']}")
```

### 命令行

```bash
python scripts/generate.py article.md \
    --cover 1 \
    --illustration 1 \
    --decoration 2 \
    --style fresh \
    --layout auto \
    --provider minimax
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

## 项目结构

```
moyu-make-xhs-pics/
├── src/
│   ├── __init__.py          # 主入口
│   ├── article_parser.py    # 文章解析
│   ├── prompt_engine.py     # 提示词引擎
│   ├── image_generator.py  # 图片生成
│   ├── watermark.py         # 水印
│   ├── layout_selector.py   # 布局选择
│   └── types.py             # 类型定义
├── scripts/
│   └── generate.py          # 命令行入口
├── tests/                   # 测试
├── data/
│   └── sample.md            # 示例文章
└── requirements.txt
```

## 测试

```bash
pytest tests/ -v
```

## License

GPL v3 - See [LICENSE](LICENSE) file
