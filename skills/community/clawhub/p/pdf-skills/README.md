# PDF知识提取技能

将PDF文件转换为Markdown格式，并提取知识规则。

## 功能特性

- PDF文本提取（PyMuPDF引擎）
- CJK字符间距自动修复
- YAML元数据（标准编号、分类、来源）
- 知识规则批量提取
- 行业标准文档自动分类

## 快速开始

### 1. 安装依赖

```bash
pip install requests pymupdf PyYAML
```

### 2. 单文件转换

```bash
# 指定输出路径
python scripts/pdf2md.py input.pdf output.md

# 自动命名
python scripts/pdf2md.py https://example.com/doc.pdf

# 指定CDN URL
python scripts/pdf2md.py https://linlan.net/cdn/zhishi/yanghu/03_xxx.pdf
```

### 3. 批量处理

```bash
# 批量转换全部19个标准
python scripts/batch_pipeline.py -o output/

# 指定范围
python scripts/batch_pipeline.py -o output/ -s 1 -e 5

# 查看可用标准列表
python scripts/batch_pipeline.py -l
```

### 4. 知识规则提取

```bash
python scripts/extract_rules.py output/03_CJJ36-2016.md
```

## 目录结构

```
pdf-skills/
├── SKILL.md                 # 技能定义（AI使用）
├── README.md                # 用户文档（本文）
├── scripts/
│   ├── pdf2md.py           # PDF转Markdown核心脚本
│   ├── extract_rules.py     # 知识规则提取
│   └── batch_pipeline.py    # 批量处理
└── output/                  # 输出目录（需手动创建）
```

## 输出示例

```markdown
---
title: "城镇道路养护技术规范 CJJ 36 2016"
standard_id: "CJJ-36-2016"
category: "道路养护"
seq: "03"
date: "2026-05-16"
source: "https://linlan.net/cdn/zhishi/yanghu/03_xxx.pdf"
doc_hash: "df52b3ad"
pages_total: 168
pages_with_text: 164
pages_scanned: 5
total_chars: 87506
---

# 城镇道路养护技术规范 CJJ 36 2016

## Metadata

| Item | Value |
|-----|-----|
| Total Pages | 168 |
| Pages with Text | 164 |
...

## Content
## Page 2

中华人民共和国行业标准
城镇道路养护技术规范
...
```

## 知识规则类型

| 类型 | 说明 | 示例 |
|------|------|------|
| frequency | 巡查/检测频率 | 每日一巡、二日一巡 |
| threshold | 技术阈值 | 平整度<=5mm |
| grade | 等级分类 | 优/良/合格/不合格 |
| period | 周期要求 | 养护期>=7天 |
| formula | 计算公式 | 合格率=(合格数/总数)*100% |
| material | 材料规格 | 水泥标号、沥青型号 |
| specification | 尺寸规格 | 直径、高度、间距 |

## 已知限制

- **表格格式**：双栏排版PDF无法自动还原表格结构
- **扫描页**：PyMuPDF无法提取扫描图片中的文本
- **字符间距**：CJK间距问题已自动修复

## 相关项目

- [ioc-kms-dataset](https://gitee.com/linlannet/ioc-kms-dataset) - 市政养护知识库数据集
