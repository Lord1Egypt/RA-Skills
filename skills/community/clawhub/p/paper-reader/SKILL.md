---
name: paper-reader
description: Comprehensive PDF paper reader for academic research. Extracts text, figures, tables, and structured content from research papers with support for multimodal analysis.
metadata:
  {
    "openclaw":
      {
        "emoji": "📑",
        "requires": { "python": ["pdfplumber", "pymupdf", "PIL"] },
      },
  }
---

# Paper Reader Skill

专为学术论文阅读设计的多功能PDF提取工具。

## 功能特性

- 📄 **文本提取**: 完整提取论文文本，保留章节结构
- 🖼️ **图片提取**: 自动提取论文中的图表、实验结果图
- 📊 **表格提取**: 提取实验数据表格为结构化格式
- 📋 **元数据读取**: 标题、作者、摘要、关键词
- 🔍 **章节识别**: 自动识别Introduction、Methods、Results等章节
- 📑 **批量处理**: 支持整个论文文件夹批量处理

## 依赖安装

```bash
pip install pdfplumber pymupdf Pillow
```

## 使用方法

### 命令行工具

```bash
# 完整提取论文（文本+图片+表格）
python3 ~/.openclaw/skills/paper-reader/read_paper.py paper.pdf --full

# 仅提取文本
python3 ~/.openclaw/skills/paper-reader/read_paper.py paper.pdf --text

# 提取图片到指定文件夹
python3 ~/.openclaw/skills/paper-reader/read_paper.py paper.pdf --images --img-dir ./figures

# 提取表格为CSV
python3 ~/.openclaw/skills/paper-reader/read_paper.py paper.pdf --tables --csv-dir ./tables

# 提取前3页（通常包含摘要和引言）
python3 ~/.openclaw/skills/paper-reader/read_paper.py paper.pdf --pages 1-3
```

### Python API

```python
from paper_reader import PaperReader

reader = PaperReader("paper.pdf")

# 获取元数据
metadata = reader.get_metadata()

# 提取全文
text = reader.extract_text()

# 提取特定章节
abstract = reader.extract_section("Abstract")
methods = reader.extract_section("Methods")

# 提取图片
figures = reader.extract_images(output_dir="./figures")

# 提取表格
tables = reader.extract_tables()
```

## 输出结构

```
paper_output/
├── paper.txt              # 完整文本
├── metadata.json          # 论文元数据
├── abstract.txt           # 摘要
├── sections/              # 分章节文本
│   ├── 01_Introduction.txt
│   ├── 02_Related_Work.txt
│   ├── 03_Methods.txt
│   ├── 04_Experiments.txt
│   └── 05_Conclusion.txt
├── figures/               # 提取的图片
│   ├── fig_1.png
│   ├── fig_2_table.png
│   └── fig_3_chart.png
└── tables/                # 提取的表格
    ├── table_1.csv
    └── table_2.csv
```

## 学术论文专用功能

### 1. 实验数据提取
自动识别并提取：
- 实验结果表格
- 性能对比图表
- 消融实验数据

### 2. 方法章节结构化
识别Methods章节中的：
- 网络架构描述
- 损失函数公式
- 训练参数设置

### 3. 参考文献提取
提取参考文献列表，支持BibTeX格式导出。
