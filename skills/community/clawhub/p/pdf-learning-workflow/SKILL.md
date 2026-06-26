---
name: pdf-learning-workflow
description: "扫描版PDF书籍 → OCR识别 → 章节分割 → 学习优化笔记"
homepage: https://github.com/adoresever/graph-memory
metadata:
  openclaw:
    emoji: 📚
  security:
    credentials_usage: |
      This skill requires a GLM-OCR API key from ZhipuAI (bigmodel.cn).
      The API key is only sent to api.bigmodel.cn as HTTP Authorization header.
      No credentials are logged, stored in files, or transmitted to any other destination.
    allowed_domains:
      - bigmodel.cn
      - cdn.bigmodel.cn
---

# 📚 PDF 学习工作流

将扫描版 PDF 书籍转为学习优化笔记。支持中英文、公式、表格识别。

## ⛔ 前置检查

### Credential Check

!`test -f ~/.config/glm-ocr/api_key && echo "✅ GLM-OCR key configured" || echo "⚠️ NO GLM-OCR KEY — setup required"`

**If ⚠️ NO KEY:** Guide user through setup before any API call:

1. 去 https://bigmodel.cn/ 注册并获取 GLM-OCR API Key
2. `mkdir -p ~/.config/glm-ocr && echo "your-api-key" > ~/.config/glm-ocr/api_key`

### 环境检查

- Python: `python3`（需安装 `zai-sdk`, `pymupdf`, `Pillow`）
- 依赖: `zai-sdk`, `pymupdf`, `Pillow`（首次运行自动安装）

---

## 工作流（按顺序执行）

### 阶段 1：PDF 拆页

```bash
SKILL_DIR=$(dirname "${BASH_SOURCE[0]:-$0}")
WORK_DIR=~/projects/pdf-learning-workflow
PDF_PATH="$1"
BOOK_NAME=$(basename "$PDF_PATH" .pdf)

OUT_DIR="$WORK_DIR/output/$BOOK_NAME"
mkdir -p "$OUT_DIR/raw_chunks" "$OUT_DIR/learning" "$OUT_DIR/pages"

$SKILL_DIR/scripts/extract_pages.py "$PDF_PATH" "$OUT_DIR/pages"
```

### 阶段 2：OCR 识别（分批）

每 5 页一批调用 GLM-OCR。每页转为 base64 data URL 后调用 API。失败重试 1 次，跳过继续。

```python
import os, base64, time
from zai import ZhipuAiClient
api_key = open(os.path.expanduser("~/.config/glm-ocr/api_key")).read().strip()
client = ZhipuAiClient(api_key=api_key)
with open(page_path, 'rb') as f:
    data_url = "data:image/png;base64," + base64.b64encode(f.read()).decode()
response = client.layout_parsing.create(model="glm-ocr", file=data_url)
markdown = response.md_results
```

保存为 `raw_chunks/chunk_XXX.md`，页码标题用 `## Page X`。

### 阶段 3：合并全文

所有 chunk 按页码合并为 `$OUT_DIR/$BOOK_NAME.md`。

### 阶段 4：后处理

```bash
$SKILL_DIR/scripts/postprocess.py "$OUT_DIR/$BOOK_NAME.md" --pages "$OUT_DIR/pages"
```

功能：
- **公式清洗：** `$ y = x $` → `$y = x$`，`$$ E = mc^2 $$` → `$$E = mc^2$$`
- **代码块检测：** 自动识别 C++/Fortran/python 代码，包裹 `````cpp` 围栏
- **图片裁剪：** 根据 OCR `![](page=0,bbox=[...])` 标记，从对应页 PNG 裁剪图片到 `assets/`

### 阶段 5：生成导读

`$OUT_DIR/${BOOK_NAME}-guide.md`：全书概览 + 每章 2-3 句简介 + 阅读建议

### 阶段 6：章节分割

读取合并全文，识别标题层级，输出到 `chapter_structure.md`。

### 阶段 7：学习重构（全部章节）

对每一章生成 `learning/chapter_XXX_标题.md`。使用诱导式结构：

> **⚠️ Markdown 精确性要求（非常重要）：**
> - 公式 `$...$` 和 `$$...$$` 前后不能有空格，否则 KaTeX 不识别
> - 表格必须用标准 Markdown 表格语法 `| col1 | col2 |`，不能混入 HTML `<table>` 标签
> - 代码块用 `````cpp` 等围栏包裹，不要用缩进代替
> - 列表保持一致的缩进层级
> - 不要混用 HTML 标签和 Markdown 语法在同一段落

```
## 🎯 学习目标

## 💡 为什么要学

## 📖 核心内容（逐步引导）

## 📐 公式与定义（LaTeX: $E=mc^2$）

## ✍️ 例题与解析

## ⚠️ 常见误解

## 📝 本章小结

## 🧪 自测题
```

### 阶段 8：生成 HTML 版本

将每章 MD 转为带 KaTeX 渲染的 HTML：

```bash
# 逐章转 HTML
for md in "$OUT_DIR/learning"/*.md; do
    $SKILL_DIR/scripts/md2html.py "$md"
done

# 生成导航页
$SKILL_DIR/scripts/gen_index.py "$OUT_DIR"
```

### 阶段 9：用户交互

- 章节分割后展示结构，确认后再继续
- 每章重构后询问是否继续下一章
- 允许调整学习风格（详细/简洁）

---

## 最终目录结构

```
output/<BookName>/
├── index.html                ← 📖 导航页（所有资源的入口）
├── <BookName>.md             ← 合并全文
├── <BookName>-guide.md       ← 导读
├── chapter_structure.md      ← 章节结构
├── assets/                   ← 裁剪图片 (fig_001.png...)
├── raw_chunks/               ← OCR 中间产物
└── learning/
    ├── chapter_001_标题.md    ← Markdown 源文件
    ├── chapter_001_标题.html  ← HTML 渲染版（含 KaTeX）
    └── ...
```

## 快速开始

```
用户: 把这本 PDF 转成学习笔记
你: 检查凭证 → 执行工作流 → 输出结果
```
