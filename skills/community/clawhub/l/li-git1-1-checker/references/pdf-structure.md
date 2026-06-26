# GB/T 1.1-2020 PDF 提取与引用指南

## PDF 结构映射

| PDF 页码 | 标准章节 | 内容 |
|----------|----------|------|
| 1-2 | 封面 | ICS、CCS、标准编号、名称 |
| 3-4 | 目次 | 标准目录 |
| 5-6 | 前言 | 起草说明、专利声明、起草单位 |
| 7 | 引言 | 编制背景 |
| 8 | 第1章 范围 | 范围示例 |
| 8-9 | 第2章 规范性引用文件 | 引用文件列表 |
| 9-10 | 第3章 术语和定义 | 术语定义 |
| 10-12 | 第4章 标准的结构 | 要素类型、结构框架 |
| 11-15 | 第5章 封面目次前言引言 | 资料性概述要素编写规则 |
| 13-15 | 第6章 要素的编号 | 层次编号规则 |
| 16-20 | 第7章 规范性要素的编写 | 范围、引用文件、术语等编写规则 |
| 21-32 | 第8章 资料性要素的编写 | 封面、目次、前言、附录等编写规则 |
| 33-45 | 第9章 要素的表述方式 | 文体、数值、单位、图表、公式 |
| 46-60 | 附录 | 示例和模板 |

## 提取脚本

### 提取特定章节

```python
import pymupdf, os

# 使用相对路径（自动定位到 skill 的 references 目录）
pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'references', 'GBT1.1-2020.pdf')
doc = pymupdf.open(pdf_path)

# 定义章节对应页码
sections = {
    '范围': (7, 9),
    '规范性引用文件': (8, 9),
    '术语和定义': (9, 10),
    '标准的结构': (10, 12),
    '封面目次前言': (11, 15),
    '要素的编号': (13, 15),
    '规范性要素': (16, 20),
    '资料性要素': (21, 32),
    '表述方式': (33, 45),
}

def extract_section(section_name):
    start, end = sections[section_name]
    text = ""
    for i in range(start - 1, min(end, len(doc))):
        text += f"\n=== PAGE {i+1} ===\n"
        text += doc[i].get_text()
    return text
```

### 全文提取

```python
import pymupdf, os

pdf_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'references', 'GBT1.1-2020.pdf')
doc = pymupdf.open(pdf_path)
for i in range(len(doc)):
    text = doc[i].get_text()
    print(f'=== PAGE {i+1} ===')
    print(text)
```

## 常用检查引用

### 文体用语（第9.1章）

| 用语类型 | 关键词 | 说明 |
|----------|--------|------|
| 要求 | 应、不应、不得 | 必须遵守的条款 |
| 推荐 | 宜、不宜 | 建议遵守的条款 |
| 允许 | 可、不必 | 允许的做法 |
| 陈述 | 是、为、由 | 描述事实 |
| 禁止 | 不应、不得 | 禁止的做法 |

### 数值表达（第9.2章）

- 范围号使用一字线"—"（U+2014）
- 每个数值后带单位
- 偏差使用"±"
- 有效位数应明确

### 图表编号（第9.4章）

- 图：图1、图2... 或 图A.1、图B.1（附录中）
- 表：表1、表2... 或 表A.1、表B.1（附录中）
- 公式：(1)、(2)... 或 (A.1)、(B.1)（附录中）
