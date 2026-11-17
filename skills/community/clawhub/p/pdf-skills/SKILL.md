---
name: pdf-skills
description: PDF知识提取技能。功能：(1)PDF文本提取为Markdown (2)CJK字符间距自动修复 (3)知识规则批量提取 (4)行业标准文档结构化处理。当用户需要处理PDF文件、提取知识内容、分析行业标准文档时使用此技能。
---

# PDF知识提取技能

> 技能版本：v1.0
> 训练日期：2026-05-16
> 依赖：Python 3.8+, requests, PyMuPDF

## 功能概述

将PDF文件转换为Markdown格式，支持：

- PDF文本提取（PyMuPDF）
- CJK字符间距自动修复
- YAML front matter 元数据
- 知识规则批量提取
- 行业标准文档自动分类

## 核心脚本

### 1. pdf2md.py - PDF转Markdown

```bash
# 指定输出路径
python scripts/pdf2md.py <pdf_url_or_path> <output.md>

# 自动命名（{序号}_{标准号}.md）
python scripts/pdf2md.py <pdf_url_or_path>
```

**输出文件名格式：** `{序号}_{标准号}.md`
- 示例：`03_CJJ36-2016.md`, `04_DGTJ08-92-2013.md`
- 序号从URL提取，标准号自动识别（CJJ/DG/GB/SHA等）

**YAML front matter 包含：**

| 字段 | 说明 |
|------|------|
| title | 文档标题 |
| standard_id | 标准编号 |
| category | 分类（道路养护/绿化养护/排水防汛/市容环卫等） |
| seq | 序号 |
| date | 提取日期 |
| source | 来源URL/路径 |
| doc_hash | 内容MD5哈希（前8位） |
| pages_total | 总页数 |
| pages_with_text | 有文本的页数 |
| pages_scanned | 扫描页数（无文本） |
| total_chars | 总字符数 |

### 2. extract_rules.py - 知识规则提取

```bash
python scripts/extract_rules.py <md_file>
```

提取7类知识规则：

| 类型 | 说明 | 示例 |
|------|------|------|
| frequency | 巡查/检测频率 | 每日一巡、二日一巡 |
| threshold | 技术阈值 | 平整度<=5mm、宽度>=X米 |
| grade | 等级分类 | 优/良/合格/不合格 |
| period | 周期要求 | 养护期>=7天、检测周期1-3年 |
| formula | 计算公式 | 合格率=(合格数/总数)*100% |
| material | 材料规格 | 水泥标号、沥青型号 |
| specification | 尺寸规格 | 直径、高度、间距 |

### 3. batch_pipeline.py - 批量处理

```bash
# 从 index.md 自动读取CDN URL，批量处理
python scripts/batch_pipeline.py -o output/

# 只列出可用URL，不执行转换
python scripts/batch_pipeline.py --list

# 指定范围（第1-10个）
python scripts/batch_pipeline.py -o output/ -s 1 -e 10

# 指定 index.md 路径
python scripts/batch_pipeline.py -i /path/to/00_index.md -o output/
```

## 已知限制

| 问题 | 原因 | 状态 |
|------|------|------|
| 表格格式丢失 | 双栏排版PDF无法还原行列结构 | 待优化 |
| 扫描页无文本 | PyMuPDF无法提取扫描图片 | 需OCR支持 |
| 字符间距 | PyMuPDF对CJK字符间加空格 | 已修复 |

**关于表格：** 行业标准PDF普遍采用双栏排版，PyMuPDF只能提取纯文本，无法自动还原表格的行列结构。如需表格，建议使用Adobe Acrobat等专业工具导出。

## 安装依赖

```bash
pip install requests pymupdf PyYAML
```

## 工作目录结构

```
pdf-skills/
├── SKILL.md                 # 技能说明（本文件）
├── README.md                # 用户文档
├── scripts/
│   ├── pdf2md.py            # 核心脚本
│   ├── extract_rules.py     # 规则提取
│   └── batch_pipeline.py    # 批量处理
└── output/                  # 输出目录（需创建）
```

## 训练测试记录

| 日期 | PDF | 页数 | MD大小 | 提取规则 |
|------|-----|------|--------|----------|
| 2026-05-16 | CJJ 36-2016 | 168 | 87.5KB | 99条 |

## 关键经验

1. **requests** 下载最稳定，自动处理URL编码
2. **PyMuPDF** 提取中文PDF文本最有效
3. **CJK间距修复** 必须做，否则中文语义被破坏
4. **双栏排版** 是行业标准PDF常见格式，表格无法自动还原
5. **YAML front matter** 方便后续检索和分类
