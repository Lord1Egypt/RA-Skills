# KDP Generator

Amazon KDP 书籍生成器 - 支持电子书转换和低内容书籍批量生产。

## Features

- 📖 **电子书出版**: Markdown → EPUB 转换
- 📔 **低内容书籍**: 日记/计划本/工作簿内页PDF生成
- 🎨 **封面设计**: AI Prompt 生成 + 自动封面生成
- 🏷️ **元数据生成**: 关键词/分类/定价建议
- 🔄 **批量生产**: 多本同时生成

## Installation

```bash
openclaw skill install kdp-generator
```

## Quick Start

### 生成低内容书籍
```bash
python scripts/create_lowcontent_book.py \
  --title "My Journal" \
  --type guided_journal \
  --pages 108 \
  --output ./output/
```

### Markdown 转 EPUB
```bash
python scripts/md2epub.py manuscript.md \
  --title "My Book" \
  --author "Author Name"
```

### 批量生成
```bash
python scripts/batch_create_books.py --config batch_config.json
```

## Supported Book Types

| Type | Description | Status |
|------|-------------|--------|
| guided_journal | 引导日记 | ✅ Ready |
| daily_planner | 每日计划本 | ✅ Ready |
| gratitude_journal | 感恩日记 | ✅ Ready |
| log_book | 记录本 | 🔄 WIP |
| activity_book | 活动书 | 🔄 WIP |

## Dependencies

```bash
pip install reportlab pillow ebooklib beautifulsoup4 markdown
```

## License

MIT
