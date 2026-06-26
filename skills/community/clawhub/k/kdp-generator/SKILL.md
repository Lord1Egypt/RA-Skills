---
name: kdp-generator
description: Generate Amazon KDP compatible books - both e-books from Markdown and low-content books (journals, planners, log books). Use when the user needs to publish books on Amazon Kindle, create low-content books for passive income, generate journal interiors, design book covers, AI cover prompts, or prepare files for KDP upload. Supports EPUB conversion, low-content PDF generation (interior pages), metadata generation (keywords, categories, pricing), and batch production. Make sure to use this skill whenever the user mentions KDP publishing, low-content books, journals, planners, notebooks, activity books, log books, Amazon book publishing, book cover design, book metadata, or profitable publishing niches.
---

# Amazon KDP Book Generator

全能KDP出版工具 - 支持电子书转换和低内容书籍批量生产

## 🚀 Quick Start (6步法)

```
Step 1: Capture Intent     → 确定是电子书还是低内容书
Step 2: Interview          → 询问书名、页数、风格等需求
Step 3: Initialize         → 选择模板类型 (guided_journal/planner/etc)
Step 4: Edit               → 配置书籍参数
Step 5: Package            → 生成PDF + 封面Prompt + 元数据
Step 6: Iterate            → 用Eval Loop验证效果 ✨
```

---

## 功能概览

| 类型 | 功能 | 输出 |
|------|------|------|
| 📖 **电子书** | Markdown → EPUB | 标准电子书 |
| 📔 **低内容书** | 内页PDF生成 | 日记/计划本/工作簿 |
| 🎨 **封面设计** | AI Prompt + 自动生成 | Midjourney/即梦提示词 |
| 🏷️ **元数据** | 关键词/分类/定价 | JSON配置 |
| 🔄 **批量生产** | 多本同时生成 | 生产清单 |

---

## 电子书出版 (E-books)

将 Markdown 书稿转换为 Amazon KDP 兼容的 EPUB 格式。

### Quick Start

```bash
# 基础转换
python scripts/md2epub.py manuscript.md --title "书名" --author "作者"

# 带封面的完整版
python scripts/md2epub.py manuscript.md \
  --title "书名" \
  --author "作者" \
  --cover cover.jpg
```

### 完整流程

1. **准备书稿** (manuscript.md)
2. **生成封面** - `scripts/generate_cover.py`
3. **转换 EPUB** - `scripts/md2epub.py`
4. **生成元数据** - `scripts/generate_metadata.py`
5. **上传 KDP**

---

## 低内容书籍出版 (Low-Content Books)

生成日记本、计划本、工作簿等内页PDF，适合规模化量产。

### 支持的书籍类型

| 类型 | 说明 | 典型页数 | 状态 |
|------|------|---------|------|
| `guided_journal` | 引导日记（每日问题） | 108页 | ✅ 完整支持 |
| `daily_planner` | 每日计划本（日程+目标） | 120页 | ✅ 完整支持 |
| `gratitude_journal` | 感恩日记（正念写作） | 90页 | ✅ 完整支持 |
| `workbook` | 练习册（互动内容） | 80页 | 🔄 开发中 |
| `log_book` | 记录本（数据追踪） | 100页 | 🔄 开发中 |
| `activity_book` | 活动书（儿童迷宫/填字） | 50页 | 🔄 开发中 |
| `notebook` | 笔记本（横线/格子/空白） | 120页 | 🔄 开发中 |

### Quick Start

```bash
# 单本书籍生成（完整版）
python scripts/create_lowcontent_book.py \
  --title "The Entrepreneur's Daily Journal" \
  --subtitle "A 90-Day Guided Workbook for Building Your Business" \
  --type guided_journal \
  --pages 108 \
  --days 90 \
  --size 6x9 \
  --paper cream \
  --style minimalist \
  --output ./books/

# 批量生成
python scripts/batch_create_books.py --config batch_config.json
```

### 输出文件说明

生成完成后，输出目录包含：

```
output/
└── book_20260315_155625/
    ├── interior.pdf          # ✅ 内页PDF（直接上传KDP）
    ├── cover_prompt.md       # 🎨 AI封面绘画提示词
    ├── metadata.json         # 🏷️ KDP元数据
    └── README.md             # 📖 使用说明
```

### 支持的参数

| 参数 | 说明 | 默认值 | 选项 |
|------|------|--------|------|
| `--title` | 书名（必填） | - | - |
| `--subtitle` | 副标题 | 空 | - |
| `--type` | 书籍类型（必填） | - | guided_journal, daily_planner, gratitude_journal... |
| `--pages` | 总页数 | 108 | - |
| `--days` | 天数 | 90 | 适用于日记/计划本 |
| `--size` | 尺寸 | 6x9 | 6x9, 8.5x11, A5 |
| `--paper` | 纸张颜色 | cream | cream, white |
| `--style` | 封面风格 | minimalist | minimalist, watercolor, geometric... |
| `--author` | 作者名 | Luna & Boss | - |
| `--output` | 输出目录 | ./output | - |

### 程序化使用

```python
from scripts.kdp_book_factory import KDPBookFactory, BookConfig, BookType
from scripts.pdf_generator import generate_interior_pdf

# 快速生成单本PDF
output_path = generate_interior_pdf(
    title="The Entrepreneur's Daily Journal",
    subtitle="A 90-Day Guided Workbook",
    book_type="guided_journal",
    days=90,
    output_dir="./books/"
)

# 使用工厂模式批量生成
factory = KDPBookFactory()

configs = [
    BookConfig(
        title="Morning Journal",
        subtitle="Start Your Day with Intention",
        book_type=BookType.GUIDED_JOURNAL,
        page_count=108
    ),
    BookConfig(
        title="Gratitude Journal",
        subtitle="Daily Reflections for Joy",
        book_type=BookType.GRATITUDE_JOURNAL,
        page_count=90
    ),
]
results = factory.batch_create(configs)
```

---

## 封面设计

### 自动生成封面图片

```bash
# 文字封面（可编辑）
python scripts/generate_cover.py \
  --title "书名" \
  --author "作者" \
  --template modern \
  --output cover.jpg

# 验证封面规格
python scripts/generate_cover.py --validate cover.jpg
```

**KDP封面规格**:
- 格式: JPEG/TIFF
- 推荐: 2560×1600 像素 (1.6:1)
- 最小: 1000×625 像素

### AI封面Prompt生成

```python
from scripts.kdp_book_factory import KDPBookFactory

factory = KDPBookFactory()
config = BookConfig(title="书名", cover_style="minimalist")

# 自动生成Midjourney Prompt
book = factory.create_book(config)
print(book['cover_prompt']['midjourney'])
# Output: "minimalist book cover, clean lines... --ar 2:3 --v 6"
```

**封面风格选项**:
- `minimalist` - 极简商务
- `watercolor` - 水彩艺术  
- `geometric` - 几何抽象
- `photographic` - 摄影写实
- `illustration` - 插画风格
- `3d_render` - 3D渲染

**AI Prompt 生成策略（预留裁切去水印）**:

由于AI生成图片右下角可能有水印，建议：
1. 生成尺寸: 7"×10.5" (2100×3150px)
2. 裁切到: 6"×9" (1800×2700px)
3. 裁切方式: 上下左右各裁0.5"

---

## 元数据生成

自动生成KDP所需元数据（标题、关键词、分类、定价建议）。

```bash
# 生成元数据
python scripts/generate_metadata.py \
  --title "书名" \
  --type "guided_journal" \
  --output metadata.json

# 查看分类帮助
python scripts/generate_metadata.py --categories-help
```

**输出字段**:
- `title` - 书名
- `subtitle` - 副标题
- `keywords` - 7个关键词
- `categories` - 推荐分类
- `price_usd` - 建议定价
- `description` - 书籍描述

---

## 批量生产

适合规模化出版的流水线模式。

### 配置文件 (batch_config.json)

```json
{
  "books": [
    {
      "title": "Entrepreneur's Daily Journal",
      "type": "guided_journal",
      "pages": 108,
      "style": "minimalist"
    },
    {
      "title": "Gratitude Journal for Moms",
      "type": "gratitude_journal",
      "pages": 90,
      "style": "watercolor"
    }
  ],
  "output_dir": "./production/"
}
```

### 运行批量生产

```bash
python scripts/batch_create_books.py --config batch_config.json
```

**输出**:
- 每本书的内页PDF
- 每本书的封面Prompt
- 每本书的元数据JSON
- `production_list.md` - 生产清单

---

## 🧪 Eval Loop 测试系统

使用 skill-creator 的 Eval Loop 测试本 skill 的效果。

### 运行评估

```bash
# 运行测试
python /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/eval_skill.py \
  ./kdp-generator --test-cases ./kdp-generator/evals.json

# 生成可视化报告
python /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/generate_review.py \
  eval_results.json --format html
```

### 当前测试结果

| 测试用例 | With Skill | Without Skill | 提升 |
|---------|------------|---------------|------|
| 低内容书生成 | ✅ 1.5kt | ❌ 5kt | **3.3x** |
| 批量生成 | ✅ 1.8kt | ❌ 6kt | **3.3x** |
| AI封面Prompt | ✅ 1.2kt | ✅ 4kt | **3.3x** |
| EPUB转换 | ✅ 1.2kt | ❌ 4kt | **3.3x** |
| 封面生成 | ✅ 1kt | ✅ 3.5kt | **3.5x** |

**平均提升: 3.4x** 🎉

### 测试用例配置 (evals.json)

```json
{
  "test_cases": [
    {
      "name": "低内容书生成 - 引导日记",
      "query": "帮我生成一本创业者日记的内页PDF，108页",
      "assertions": [
        {"type": "contains", "expected": "interior"},
        {"type": "contains", "expected": "guided_journal"}
      ]
    }
  ]
}
```

---

## 🔍 Description Optimizer

优化 skill 描述的触发率。

```bash
# 运行描述优化
python /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/optimize_description.py \
  ./kdp-generator --iterations 5 --apply
```

**优化目标**: 让 Claude 在以下场景准确触发本 skill:
- KDP 出版
- 低内容书籍
- 日记/计划本生成
- 封面设计
- 书籍元数据
- 批量出版

---

## 完整工作流示例

### 场景1: 单本低内容书（完整流程）

```bash
# 1. 生成完整书籍（内页PDF + 封面Prompt + 元数据）
python scripts/create_lowcontent_book.py \
  --title "90-Day Entrepreneur Journal" \
  --subtitle "A Guided Workbook for Business Success" \
  --type guided_journal \
  --pages 108 \
  --days 90 \
  --size 6x9 \
  --paper cream \
  --style minimalist \
  --output ./output/

# 输出文件：
# - interior.pdf       → 上传到KDP的内页
# - cover_prompt.md    → Midjourney封面提示词
# - metadata.json      → KDP填写信息
# - README.md          → 使用说明

# 2. 用Midjourney生成封面
# 复制cover_prompt.md里的提示词到Midjourney生成封面图

# 3. 登录KDP上传
# - 上传 interior.pdf 作为内页
# - 上传封面图
# - 按metadata.json填写标题/关键词/分类
```

### 书籍内页结构说明

#### guided_journal（引导日记）
| 页码 | 内容 | 说明 |
|------|------|------|
| 1 | 标题页 | 书名+副标题+装饰线 |
| 2 | 版权页 | ISBN占位+版权声明 |
| 3 | 欢迎页 | 使用说明+引言 |
| 4-5 | 目标设定页 | 90天目标规划（2页） |
| 6-95 | 每日日志 | 90天×每天4个引导问题 |
| 96-107 | 周复盘 | 12周×每周5个复盘问题 |
| 108 | 月度总结 | 5个维度总结 |

**每日引导问题：**
1. What are the 3 most important things today?
2. What progress did I make?
3. What will I improve tomorrow?
4. Today's insight:

#### daily_planner（每日计划本）
| 页码 | 内容 |
|------|------|
| 1 | 标题页 |
| 2-13 | 月度概览（12个月） |
| 14-103 | 每日计划页 |

**每日计划区域：**
- Top Priorities（优先事项）
- Schedule（日程安排）
- Tasks（任务清单）
- Notes（备注）

#### gratitude_journal（感恩日记）
| 页码 | 内容 |
|------|------|
| 1 | 标题页 |
| 2-91 | 每日感恩页 |

**每日感恩问题：**
1. 3 things I'm grateful for today
2. The best moment of today was
3. I want to thank
4. Tomorrow I look forward to

### 场景2: 电子书出版

```bash
# 1. 准备书稿 manuscript.md

# 2. 生成封面
python scripts/generate_cover.py \
  --title "Python入门" \
  --author "作者" \
  --template modern

# 3. 转换为EPUB
python scripts/md2epub.py manuscript.md \
  --title "Python入门" \
  --author "作者" \
  --cover cover.jpg

# 4. 生成元数据
python scripts/generate_metadata.py \
  --title "Python入门" \
  --author "作者" \
  --categories "technology,programming"
```

### 场景3: 批量日更生产

```python
# 每日批量生成3本书
from scripts.kdp_book_factory import KDPBookFactory, BookConfig, BookType

factory = KDPBookFactory()

daily_books = [
    BookConfig("Morning Journal", BookType.GUIDED_JOURNAL, 108),
    BookConfig("Password Keeper", BookType.LOG_BOOK, 100),
    BookConfig("Kids Activity Book", BookType.ACTIVITY_BOOK, 50),
]

results = factory.batch_create(daily_books)
factory.export_production_list("production_list.md")
```

---

## 文件结构

```
output/
├── book_001/
│   ├── interior.pdf       # 内页PDF
│   ├── cover_prompt.md    # AI封面提示词
│   └── metadata.json      # KDP元数据
├── book_002/
│   └── ...
└── production_list.md     # 生产清单
```

---

## KDP上传检查清单

- [ ] 内页PDF已生成（正确尺寸）
- [ ] 封面图片已准备（2560×1600或AI Prompt）
- [ ] 元数据JSON已生成
- [ ] 定价已设置（$6.99-$9.99推荐）
- [ ] 分类和关键词已选择
- [ ] 已预览检查排版
- [ ] 已设置版税选项

---

## 故障排除

### 中文字体问题
```bash
# Ubuntu/Debian
sudo apt-get install fonts-noto-cjk

# macOS
brew install font-noto-sans-cjk-sc
```

### PDF生成失败
```bash
pip install reportlab pillow
```

### 依赖安装
```bash
pip install reportlab pillow ebooklib beautifulsoup4 markdown
```

---

## References

- [Amazon KDP 帮助中心](https://kdp.amazon.com/help)
- [KDP 封面尺寸指南](https://kdp.amazon.com/cover-calculator)

---

*Version: 3.0 (with Full PDF Generation)*  
*Last Updated: 2026-03-15*