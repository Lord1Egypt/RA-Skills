---
name: manual-qztc
description: 仅供QZTC内部使用。教学工作手册生成工具 v5.3。Generator+Reviewer双模式，支持Pipeline一键生成+审查。
---

# 教学工作手册生成工具 v5.3

> 🎯 **设计模式**: Generator + Reviewer + Pipeline + Tool Wrapper
> 📁 **代码文件**: `manual_generator.py`
> 🔍 **审查脚本**: `scripts/review_document.py`
> 📖 **规则参考**: `references/grading-formula.md`

---

## 🚀 快速开始

### Pipeline 一键执行（推荐）

```bash
# 生成 + 审查
python3 manual_generator.py <Excel文件> --pipeline
```

### 单独使用

```bash
# 生成
python3 manual_generator.py 数据可视化-23级计算机.xls

# 审查
python3 scripts/review_document.py 教学工作手册.docx
```

---

## 📁 目录结构

```
manual-qztc/
├── SKILL.md                      # 本文件
├── manual_generator.py             # 主生成器（Generator模式）
├── scripts/
│   └── review_document.py        # 质量审查（Reviewer模式）v1.0
└── references/
    └── grading-formula.md        # 工具规则（Tool Wrapper）
```

---

## 🔄 Pipeline 工作流

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: 生成 (Generator)                                  │
│  python3 manual_generator.py <Excel> --pipeline             │
│       ↓                                                    │
│  ✅ CHECKPOINT 1: 文件生成成功？                             │
│       ↓                                                    │
│  STEP 2: 审查 (Reviewer)                                   │
│  python3 scripts/review_document.py <输出.docx>             │
│       ↓                                                    │
│  ✅ CHECKPOINT 2: 所有检查项通过？                          │
│       ↓                                                     │
│  STEP 3: 交付                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 测试数据

```bash
# C#程序设计（48学生，软工）
python3 manual_generator.py "~/Documents/QZTC/2026/C#程序设计-23级软工.xls" --pipeline

# 数据可视化（52学生，计算机）
python3 manual_generator.py "~/Documents/QZTC/2026/数据可视化-23级计算机.xls" --pipeline
```

---

## 📋 表格结构

### 作业表（学生作业登记表）
| 列 | 内容 |
|----|------|
| cells[0] | 学号 |
| cells[1] | 姓名 |
| cells[2-14] | 作业1-13（填√或空） |

### 成绩表（学生课程成绩登记表）
| 列 | 内容 |
|----|------|
| cells[0] | 学号 |
| cells[1] | 姓名 |
| cells[8] | 平时成绩 |
| cells[9] | 期中成绩 |
| cells[10] | 期末成绩 |
| cells[11] | 总评 |

### 分页
- 每表21行（1表头+20数据）
- 不足20学生时多余行留空

---

## 🔧 审查检查项

| 检查项 | 说明 |
|--------|------|
| ✅ placeholders | 所有{*}占位符已替换 |
| ✅ homework_tables | 作业表结构正确 |
| ✅ grade_tables | 成绩表结构正确 |

---

## 📐 占位符规则

| 占位符 | 含义 | 示例 |
|--------|------|------|
| `{as}` | 学年 | `2025 - 2026` |
| `{ay}` | 学年学期 | `2025-2026-2` |
| `{sm}` | 学期 | `二` |
| `{g}` | 年级 | `23` |
| `{mj}` | 专业 | `软工` |
| `{g}{mj}` | 复合 | `23软工` |
| `{tot}` | 总人数 | `48` |
| `{v}` | 平均成绩 | `78.5` |
| `{y}` `{m}` `{d}` | 年/月/日 | `2026` / `4` / `9` |
| `{c}` | 班号 | `1` |

---

## 📦 依赖

```python
import pandas as pd
from docx import Document
```

---

## 🔄 更新日志

| 版本 | 日期 | 内容 |
|------|------|------|
| **v5.1** | 2026-04-09 | 全面切换至{* }占位符格式 | |
| v4.6 | 2026-03-28 | 文本替换格式、居中、分页 |

---

*v5.1 - 2026-04-09 - Generator + Reviewer + Pipeline + Tool Wrapper*
