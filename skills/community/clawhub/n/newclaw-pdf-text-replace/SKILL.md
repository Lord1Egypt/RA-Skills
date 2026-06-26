---
name: pdf-text-replace
description: "Replace text in PDF files while preserving visual fidelity. Handles custom font encodings, embedded subsets, encrypted PDFs, image-based scans (OCR), variable-length replacements, and style changes. Use when user wants to change/replace/modify specific text in any PDF."
version: 2.1.4

metadata:
  openclaw:
    emoji: "\U0001F4C4"
    homepage: "https://clawhub.ai/skills/newclaw-pdf-text-replace"
    os: [macos, linux]
    requires:
      bins: [python3]
    install:
      pip: [pypdf, pdfplumber, fonttools, pdf2image, Pillow]
      brew: [poppler]
---

# PDF Text Replace v2.0 - PDF 文字精准替换

在不破坏原始视觉效果的前提下，替换 PDF 中的指定文字。自动检测 PDF 类型并选择最优替换策略，支持加密 PDF、扫描件、样式修改等高级场景。

## 适用场景

- 修改证书、合同上的日期、姓名、数字
- 修正已导出 PDF 中的错别字（原始文件已丢失）
- 更新加密 PDF 中的内容（需提供密码）
- 对扫描版 PDF（纯图片）进行 OCR 识别后替换
- 修改替换文字的颜色、字号、加粗、下划线

## 安装

```bash
# OpenClaw 一键安装
clawhub install newclaw-pdf-text-replace

# 核心依赖（必须）
pip3 install pypdf pdfplumber fonttools pdf2image Pillow
brew install poppler    # macOS

# 可选依赖（按需启用高级功能）
pip3 install pikepdf           # L6: 解密加密 PDF
pip3 install paddleocr         # L5: OCR 扫描件替换（首选）
pip3 install opencv-python     # L5: OCR 图像预处理
pip3 install pymupdf           # L4: 样式修改（颜色/字号/粗体）
```

## 六级能力体系

| 级别 | 能力 | 依赖 | 状态 |
|------|------|------|------|
| L1 | 等长直接字节码替换 | 核心依赖 | 内置 |
| L2 | 变长替换（Tz 缩放 / 重排） | 核心依赖 | 内置 |
| L3 | 跨 Tj 操作符多段文本替换 | 核心依赖 | 内置 |
| L4 | 样式修改（颜色/字号/粗体/下划线） | pymupdf | 可选 |
| L5 | 图像型 PDF OCR 替换 | paddleocr + opencv | 可选 |
| L6 | 加密 PDF 解密替换 | pikepdf | 可选 |

缺少可选依赖时，工具自动降级到已安装的级别，不会崩溃。

## 使用方法

### 命令行

```bash
# 基础替换
python3 scripts/pdf_text_replace.py input.pdf "旧文字" "新文字"

# 指定输出路径
python3 scripts/pdf_text_replace.py input.pdf "2025" "2026" output.pdf

# L4: 修改颜色（红色）
python3 scripts/pdf_text_replace.py input.pdf "草稿" "正式" --color 1,0,0

# L4: 修改字号 + 加粗 + 下划线
python3 scripts/pdf_text_replace.py input.pdf "标题" "新标题" --size 18 --bold --underline

# L5: 强制 OCR 模式（扫描件）
python3 scripts/pdf_text_replace.py scan.pdf "旧" "新" --force-ocr

# L6: 加密 PDF
python3 scripts/pdf_text_replace.py secret.pdf "旧" "新" --password mypassword

# 指定页码（从 0 开始）
python3 scripts/pdf_text_replace.py multi.pdf "旧" "新" --page 2
```

### AI 自然语言（OpenClaw / Claude Code）

> "把这个 PDF 里的'比赛时间：2025年'改成'2026年'"
> "把加密 PDF（密码 abc123）里的'Draft'改成'Final'，并标红"
> "这个扫描版证书，把日期从 01/01/2024 改成 01/01/2025"

### Python API

```python
from scripts.pdf_text_replace import replace_text

# 基础用法
replace_text("input.pdf", "2025", "2026", "output.pdf")

# 带样式（L4）
replace_text(
    "input.pdf", "Draft", "Final", "output.pdf",
    color=(1, 0, 0),    # 红色
    font_size=14,
    underline=True,
)

# 加密 PDF（L6）
replace_text("secret.pdf", "old", "new", password="mypassword")

# 扫描件（L5）
replace_text("scan.pdf", "old", "new", force_ocr=True)
```

## 自动策略选择流程

```
输入 PDF
  ├─ 是否加密？ → L6 解密
  ├─ 是否图像型？ → L5 OCR
  ├─ 文字是否在字体内？
  │     ├─ 等长 → L1 直接字节码替换
  │     ├─ 变长 → L2 Tz 缩放/重排
  │     └─ 多段分布 → L3 跨 Tj 替换
  └─ 有样式要求？ → L4 叠加样式层
```

## 核心难点：为什么 PDF 文字替换很难？

大多数 PDF 使用**内嵌字体子集** + 自定义字节编码（CMap）。`"2025"` 在 PDF 内部是字形代码如 `0x25 0x24 0x25 0x26`，不是 ASCII。必须：解析 CMap → 反向编码目标字符 → 在字节流中精确替换，缺失字符还需嵌入新字体子集。

## 踩坑规则

| 规则 | 原因 |
|------|------|
| 不用 fontTools 改后重嵌原字体 | 会损坏字形渲染 |
| 缺失字符新建独立字体资源 | 不碰原始字体 |
| 用 pdfplumber 获取精确坐标 | 每字符 x0/top/x1/bottom |
| 视觉样式必须匹配系统字体 | Cambria Bold → Georgia Bold |
| 同时验证文本提取 + 视觉渲染 | 两者可能不一致 |

## 文件结构

```
pdf-text-replace/
├── SKILL.md
├── scripts/
│   ├── pdf_text_replace.py    # v2.0 统一入口（本文件）
│   ├── v2_l2_varlen.py        # L2: 变长替换
│   ├── v2_l3_multitj.py       # L3: 跨 Tj 替换
│   ├── v2_l4_style.py         # L4: 样式修改
│   ├── v2_l5_ocr.py           # L5: OCR 扫描件
│   └── v2_l6_decrypt.py       # L6: 加密解密
└── references/
    └── cmap-encoding-guide.md
```
