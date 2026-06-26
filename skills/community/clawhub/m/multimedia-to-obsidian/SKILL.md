---
name: multimedia-to-obsidian
description: 将任意多媒体文档导入 Obsidian 知识库。支持 PPT、PDF、DOCX、图片等格式，自动提取每一页/每一张图片，使用多模态模型理解内容，生成文字描述后存入 OB。适用于：(1) 整理培训课件 (2) 迁移笔记到 OB (3) 将图片资料转为结构化知识。
---

# 多媒体导入 Obsidian

将 PPT、PDF、DOCX、图片等多媒体文档导入 Obsidian，每页/每张图片自动生成文字描述。

## 功能特点

- 支持多种格式：PPT、PDF、DOCX、图片（PNG、JPG 等）
- 自动提取媒体文件
- 调用多模态模型理解内容
- 自动分类到 OB 仓库

## 使用方法

### 前提条件

1. 安装依赖：
```bash
brew install pandoc poppler
pip install python-pptx pillow
```

2. 设置环境变量（至少一个）：
```bash
# MiniMax
export MINIMAX_API_KEY="your-key"
export MINIMAX_API_HOST="https://api.minimaxi.com"

# OpenAI
export OPENAI_API_KEY="your-key"

# Anthropic
export ANTHROPIC_API_KEY="your-key"
```

### 调用脚本

```bash
python3 <skill>/scripts/media_to_obsidian.py <源文件/目录> <输出OB目录> [options]
```

**参数：**
- 源文件/目录：单个文件或包含多媒体文件的目录
- 输出目录：Obsidian 仓库路径
- 选项：
  - `--format ppt|pdf|docx|image|all` : 指定格式，默认 all
  - `--model minimax|openai|anthropic` : 指定模型，默认 minimax
  - `--category 分类名` : 指定输出分类目录

### 示例

```bash
# 导入 PPT 课件
python3 ~/.openclaw/workspace/skills/multimedia-to-obsidian/scripts/media_to_obsidian.py \
  /path/to/培训课件.pptx \
  /path/to/Obsidian \
  --format ppt --category 培训

# 导入图片到 OB
python3 ~/.openclaw/workspace/skills/multimedia-to-obsidian/scripts/media_to_obsidian.py \
  /path/to/images/ \
  /path/to/Obsidian \
  --format image --category 素材

# 批量导入目录下的所有文档
python3 ~/.openclaw/workspace/skills/multimedia-to-obsidian/scripts/media_to_obsidian.py \
  /path/to/documents/ \
  /path/to/Obsidian
```

## 输出结构

```
Obsidian仓库/
├── 培训/
│   └── 培训课件.md (含每页图片理解)
├── 素材/
│   └── 图片1.md
│   └── 图片2.md
└── 导入/
    └── 文档名.md
```

## 工作流程

1. **提取媒体**：从 PPT/PDF/DOCX 提取每一页为图片
2. **理解内容**：调用多模态模型理解每张图片
3. **生成描述**：将图片描述写入 Markdown
4. **分类存储**：按指定分类存入 OB
