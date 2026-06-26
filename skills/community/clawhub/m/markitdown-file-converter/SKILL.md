---
name: markitdown-file-converter
description: |
  将 PDF、Word (docx/doc)、Excel (xlsx/xls)、PPT (pptx/ppt)、图片等文件一键转换为 Markdown 或 JSON。
  内置三大引擎：pandoc（DOCX 表格/Emoji/公式最强）、markitdown（微软开源，Excel/PPT/图片 OCR）、mammoth（DOCX 纯文本兜底）。
  首次使用自动安装全部依赖，无需手动配置。
  支持数学公式 → LaTeX、表格 → Markdown 管道表格、图片自动提取并插入链接、base64 图片自动解码。
  触发关键词：转markdown、转json、文档转换、pdf转md、word转markdown、docx转md、xlsx转md、
  ppt转md、表格转md、图片转文字、ocr识别、批量转换文档。
---

# markitdown-file-converter

文档一键转 Markdown / JSON，整合 pandoc + markitdown + mammoth 三大引擎，首次使用自动安装依赖。

## 功能特性

- **依赖检查**：`python scripts/main.py --check` 检测环境依赖是否完整（pandoc、markitdown、mammoth、RapidOCR）
  - **一键转换**：PDF / DOCX / DOC / XLSX / XLS / PPTX / PPT → Markdown 或 JSON
- **图片 OCR**：PNG / JPG / GIF / BMP → 文字识别（PaddleOCR Cloud 优先，RapidOCR 兜底）
- **公式 OCR**：PNG / JPG / GIF / BMP → LaTeX 公式识别（pix2tex/LaTeX-OCR）
- **PDF OCR**：扫描版 PDF → 自动转图片 + OCR（pdf2image + PaddleOCR Cloud/RapidOCR），逐页输出
- **数学公式**：自动转为 LaTeX 格式（$E=mc^2$、$$\int$$）
- **表格保留**：pandoc grid table / simple table → 标准 Markdown 管道表格
- **图片提取**：DOCX / XLSX 中的嵌入图片自动提取到 `images/` 目录并插入 `![alt](path)` 链接
- **base64 解码**：自动将 base64 内嵌图片解码保存为文件
- **批量转换**：`--batch` 一次性转换整个目录
- **JSON 输出**：按标题分 section 输出结构化 JSON
- **进度反馈**：`-v/--verbose` 显示详细进度（PDF OCR 逐页输出）
- **超时控制**：`--timeout` 防止大文件卡死（默认 120 秒）
- **自动安装**：首次运行自动检测并安装缺少的依赖，零配置开箱即用
- **三引擎 OCR：RapidOCR（通用文字） + PaddleOCR Cloud（云端优先） + pix2tex（公式识别），自动降级

## 技能结构

```
markitdown-file-converter/
├── SKILL.md              ← 本文件
└── scripts/
    ├── main.py           ← 主入口
    ├── backends/         ← 转换后端
    │   ├── pandoc.py
    │   ├── markitdown.py
    │   └── mammoth.py
    ├── ocr/              ← OCR 引擎
    │   ├── engine.py     ← OCR 调度器（智能引擎选择）
    │   ├── rapidocr.py   ← RapidOCR + pix2tex
    │   └── selector.py   ← 引擎选择策略
    └── utils/            ← 工具模块
        ├── deps.py       ← 依赖检测
        ├── deps_check.py ← 依赖检查工具
        ├── images.py     ← 图片处理
        ├── table.py      ← 表格美化
        ├── cleanup.py    ← 输出清理（新增）
        ├── format_detector.py ← 格式检测（新增）
        ├── metadata.py   ← 元数据提取（新增）
        └── pptx_handler.py ← PPTX处理（新增）
```

## 支持的格式

| 类别 | 格式 | 后端 | 说明 |
|------|------|------|------|
| **Word** | .docx, .doc, .rtf, .odt | pandoc/markitdown/mammoth | 表格/Emoji/公式保留 |
| **Excel** | .xlsx, .xls, .csv, .ods | markitdown/pandoc | 数据+格式 |
| **PPT** | .pptx, .ppt, .odp | pandoc/markitdown | 幻灯片提取 |
| **PDF** | .pdf | markitdown/OCR | 文本提取+扫描识别 |
| **图片** | .png, .jpg, .gif, .bmp | OCR | 文字/公式识别 |
| **文本** | .md, .txt, .html | copy/pandoc | 直接复制/转换 |
| **数据** | .json, .xml, .yaml | copy/pandoc | 格式转换 |
| **电子书** | .epub, .mobi | pandoc | 电子书转换 |
| **音频** | .mp3, .wav | markitdown | 语音转录 |

## 依赖与安装

### 自动安装（推荐）

脚本在首次使用时自动检测并安装缺少的依赖，**无需手动操作**。

AI 调用时使用以下方式安装依赖（在当前 venv 环境中）：

```bash
# 检测并安装 Python 包（mammoth, markitdown[all], beautifulsoup4）
uv pip install mammoth "markitdown[all]" beautifulsoup4 --python <venv_python_path>

# 检测并安装 pandoc（Windows）
winget install --accept-package-agreements --accept-source-agreements JohnMacFarlane.Pandoc
```

### 一键预装

```bash
python scripts/convert.py --install
```

该命令会依次安装 pandoc、markitdown、mammoth 三个后端。

### 各后端手动安装

| 后端 | 命令 | 说明 |
|------|------|------|
| **pandoc** | `winget install pandoc`（Win）/ `brew install pandoc`（Mac） | DOCX 表格/Emoji/公式保留最强 |
| **markitdown** | `pip install "markitdown[all]"` | 微软开源，Word/Excel/PPT/PDF |
| **rapidocr** | `pip install rapidocr-onnxruntime` | 图片 OCR（中英文识别），本地运行 |
| **pix2tex** | `pip install pix2tex` | LaTeX 公式 OCR（图片→LaTeX 代码） |
| **pdf2image** | `pip install pdf2image` + poppler | PDF OCR（扫描版 PDF → 图片 → OCR） |
| **mammoth** | `pip install mammoth` | DOCX → HTML → Markdown，纯文本兜底 |

> ⚠️ **PDF OCR 需要 poppler**：Windows 用户需安装 poppler（`winget install poppler` 或从 [Release 下载](https://github.com/oschwartz10612/poppler-windows/releases)），Mac 用户 `brew install poppler`。

> ⚠️ `markitdown[all]` 是一次性参数，不要拆成 `pip install markitdown` + `pip install all`。

## AI 使用指南

当用户请求文档转换时，按以下流程操作：

### 1. 确认环境

```bash
# 检查 Python venv 路径（示例）
# Windows: C:\Users\<user>\.qclaw\workspace\.uvenv\Scripts\python.exe
# macOS:   ~/.qclaw/workspace/.uvenv/bin/python
```

### 2. 安装依赖（如尚未安装）

```bash
# Python 包
uv pip install mammoth "markitdown[all]" rapidocr-onnxruntime pix2tex pdf2image beautifulsoup4 --python <venv_python_path>

# poppler（PDF OCR 必需）
# Windows: winget install poppler
# Mac: brew install poppler
# Linux: sudo apt-get install poppler-utils

# pandoc（如未安装）
winget install pandoc
```

### 3. 执行转换

```bash
# 单文件转换（自动选择最佳后端）
python scripts/convert.py <input_file>

# 指定输出目录
python scripts/convert.py <input_file> -o <output_dir>

# 指定后端
python scripts/convert.py <input_file> -b pandoc
python scripts/convert.py <input_file> -b markitdown
python scripts/convert.py <input_file> -b mammoth

# PDF OCR（扫描版 PDF）
python scripts/convert.py scanned.pdf -b markitdown -v  # -v 显示逐页进度

# 输出为 JSON（按标题分 section）
python scripts/convert.py <input_file> -f json

# 批量转换目录
python scripts/convert.py <input_dir> --batch -o <output_dir>

# 指定后端 + 批量
python scripts/convert.py <input_dir> --batch -b pandoc -o <output_dir>

# 大文件超时控制
python scripts/convert.py large.docx --timeout 300  # 5分钟超时

# 详细进度输出
python scripts/convert.py <input_file> -v
```

### 4. 读取输出

转换完成后，从输出目录读取 `.md` 或 `.json` 文件，将内容呈现给用户。

## CLI 完整参数

```
convert.py [input] [-f md|json] [-o <dir>] [-b pandoc|markitdown|mammoth|auto] [--batch] [--install] [-v] [--timeout SEC]

位置参数:
  input              输入文件路径，或目录路径（配合 --batch）

可选参数:
  -f, --format       输出格式：md（默认）/ json
  -o, --output       输出目录（默认：<input_stem>_converted/）
  -b, --backend      转换引擎（默认：auto）：
                       auto       按文件类型自动选择最优后端
                       pandoc     全能王，DOCX 表格/Emoji/公式最强
                       markitdown 微软官方，Excel/PPT/PDF/图片 OCR
                       mammoth    DOCX 纯文本兜底
  --batch            批量模式：转换指定目录下所有支持的文件
  --install          预装全部后端并退出
  -v, --verbose      显示详细进度（PDF OCR 逐页输出）
  --timeout SEC      单文件转换超时秒数（默认：120）
```

## 后端选择策略

### 自动选择逻辑（-b auto，默认）

按 `pandoc > markitdown > mammoth` 优先级，选择第一个已安装且支持该格式的后端。
如果所有后端均未安装，自动安装 markitdown。

| 文件类型 | 自动首选 | 原因 |
|---------|---------|------|
| `.docx` `.doc` | **pandoc** | 表格/Emoji/公式保留最佳 |
| `.xlsx` `.xls` | **markitdown** | pandoc/mammoth 不支持 Excel |
| `.pptx` `.ppt` | **markitdown** | markitdown PPT 支持更好 |
| `.pdf` | **pandoc** | 格式保留更完整 |
| `.png` `.jpg` ... | **markitdown** | 唯一支持 OCR 的后端 |
| `.html` `.csv` `.json` `.xml` `.zip` | **markitdown** | 唯一支持的后端 |

### 手动选择建议

- **DOCX 含复杂表格 / Emoji / 数学公式** → `-b pandoc`
- **Excel / PPT / 图片 OCR / 音频转录** → `-b markitdown`
- **DOCX 快速纯文本提取** → `-b mammoth`
- **不确定** → 不指定，使用默认 auto

## 三大后端对比

| 特性 | pandoc | markitdown | mammoth |
|------|--------|-----------|---------|
| PDF | ✅ | ✅ 基础 | ❌ |
| DOCX | ✅ 优秀 | ✅ 优秀 | ✅ 可用 |
| DOC | ✅ | ✅ | ✅ |
| XLSX / XLS | ❌ | ✅ 优秀 | ❌ |
| PPTX / PPT | ✅ 可用 | ✅ 优秀 | ❌ |
| 图片 OCR | ❌ | ✅ RapidOCR + PaddleOCR Cloud + pix2tex（三引擎，自动降级） | ❌ |
| PDF OCR（扫描版） | ❌ | ✅ pdf2image + RapidOCR 逐页识别 | ❌ |
| HTML / CSV / JSON / XML | ❌ | ✅ | ❌ |
| 音频转录 (.wav .mp3) | ❌ | ✅ | ❌ |
| 数学公式 → LaTeX | ✅ | ✅ | ✅ |
| 表格 → 管道表格 | ✅ grid→pipe | ✅ | ✅ |
| 图片自动提取 | ✅ | ✅ | ✅ |
| base64 图片解码 | ❌ | ✅ | ✅ |
| 纯 CPU 运行 | ✅ | ✅ | ✅ |
| 需联网下载 | ❌ | ❌ | ❌ |

## 输出结构

### Markdown 模式（默认）

```
<input_stem>_converted/
├── <input_stem>.md      ← 转换后的 Markdown 文件
└── images/               ← 提取的图片（仅当源文件包含图片时生成）
    ├── image_0.png
    ├── image_1.jpg
    └── ...
```

### JSON 模式（-f json）

与 Markdown 模式相同的目录结构，额外生成 JSON 文件：

```json
{
  "source": "report.docx",
  "sections": [
    {
      "heading": "第一章 概述",
      "level": 1,
      "content": "正文内容..."
    },
    {
      "heading": "数据表格",
      "level": 2,
      "content": "| 姓名 | 成绩 |\n|------|------|\n| 小明 | 98   |"
    }
  ]
}
```

## 注意事项

1. **pandoc 需加入 PATH**：winget 安装 pandoc 后，新开的终端会自动识别。如果脚本找不到 pandoc，请重启终端或手动将 `C:\Program Files\Pandoc` 加入 PATH。

2. **pandoc 表格处理**：pandoc 输出的 grid table（用 `---` 横线分隔的表格）会被脚本自动转换为标准 Markdown 管道表格格式。

3. **图片路径**：Markdown 中的图片使用相对路径 `images/image_0.png`，需要确保 `.md` 文件和 `images/` 目录保持相对位置不变。

4. **markitdown CLI 输出**：markitdown 默认输出 JSON（含 Unicode 转义），脚本已自动添加 `--format text` 参数以获取纯 Markdown。

5. **大型 PDF**：pandoc 对复杂排版（多栏、分栏、复杂页眉页脚）支持有限，转换效果可能不完美。

6. **OCR 质量**：使用 RapidOCR (ONNX Runtime) 作为图片文字识别引擎，支持中英文，对清晰截图效果优秀（准确率 >95%）。低分辨率、手写体、艺术字体效果有限。markitdown 原生图片转换依赖 LLM 描述（需配置 API key），未配置时自动降级到 RapidOCR。

7. **编码处理**：脚本强制使用 UTF-8 输出，确保中文等多语言内容正确显示。

8. **批量模式**：`--batch` 会为目录中每个文件创建独立子目录，避免文件名冲突。

9. **自动降级**：如果首选后端转换失败，脚本会自动尝试下一个可用后端（pandoc → markitdown → mammoth）。图片 OCR 的降级链为：markitdown LLM → RapidOCR → pix2tex（公式）→ 失败提示。

10. **PDF OCR 需要 poppler**：扫描版 PDF OCR 依赖 pdf2image + poppler。Windows 用户需安装 poppler（`winget install poppler` 或从 [GitHub Release](https://github.com/oschwartz10612/poppler-windows/releases) 下载并添加到 PATH）。Mac 用户 `brew install poppler`。

## Python API 使用示例

```python
from pathlib import Path
from convert import convert_file, batch_convert

# 单文件转换
md_path = convert_file(
    Path("report.pdf"),
    Path("output"),
    fmt="md",           # 或 "json"
    backend="auto",     # 或 "pandoc"/"markitdown"/"mammoth"
    verbose=True,       # 显示详细进度
    timeout=120         # 超时秒数
)
print(f"输出文件: {md_path}")

# 批量转换
batch_convert(
    Path("./docs"),
    Path("./converted"),
    fmt="md",
    backend="auto",
    verbose=False,
    timeout=120
)

# PDF OCR（扫描版）
md_path = convert_file(
    Path("scanned.pdf"),
    Path("output"),
    backend="markitdown",  # PDF OCR 使用 markitdown 后端
    verbose=True           # 显示逐页进度
)
```

## 常见问题

**Q: 首次使用需要手动安装什么吗？**
A: 不需要。脚本会自动检测并安装缺少的依赖。如需提前安装，运行 `python scripts/convert.py --install`。

**Q: pandoc 和 markitdown 哪个更好？**
A: 视场景而定。DOCX 含表格/Emoji/公式推荐 pandoc；Excel/PPT/图片 OCR 推荐 markitdown。不确定时用默认 auto 即可。

**Q: 转换后表格丢失了？**
A: 已修复 pandoc grid table 中数据行间空行导致的表格丢失问题。如仍遇到，请指定 `-b markitdown` 或 `-b mammoth` 尝试其他后端。

**Q: 支持扫描版 PDF 吗？**
A: 支持。markitdown 后端现在支持扫描版 PDF OCR：PDF → 图片 → RapidOCR 逐页识别。需要安装 poppler（Windows: `winget install poppler`，Mac: `brew install poppler`）。使用 `-v` 参数可查看逐页进度。

**Q: PDF OCR 输出格式是什么？**
A: 按页面分节，每页一个 `## Page N` 标题，下方是该页 OCR 识别的文字。同时会在 `images/` 目录保存每页的截图（`page_1.png`、`page_2.png` 等）。

**Q: 图片 OCR 支持中文吗？**
A: 是的。使用 RapidOCR (rapidocr-onnxruntime) 作为 OCR 引擎，支持中英文混合识别，准确率通常 >95%（清晰截图）。markitdown 原生的图片转换依赖 LLM 描述（需配置 OpenAI API key），未配置时会自动降级到 RapidOCR。

**Q: 可以识别图片中的数学公式并转为 LaTeX 吗？**
A: 是的。使用 pix2tex (LaTeX-OCR) 作为公式识别引擎。自动降级策略：RapidOCR 先识别文字，如果结果很短（<15 字符）且不含中文，则尝试 pix2tex 识别公式。输出格式为 `$$\n...LaTeX...\n$$`。注意：pix2tex 对真实截图的公式识别效果较好，对纯文本图片（如照片）可能产生误识别。

**Q: 转换结果有错误怎么办？**
A: 如果发现转换结果存在错误，请直接指出错误内容并要求修正。Skill 会立即修正错误，同时自动记录本次错误信息到学习系统，避免后续重复出现同类问题。例如："表格第三行数据丢失了，请修复"或"公式识别错误，应该是 E=mc² 不是 E=mc2"。

**Q: 输出 JSON 的 section 是怎么分的？**
A: 按 Markdown 标题（`#` ~ `######`）分割，每个标题及其下内容组成一个 section。未在标题下的内容归入 `heading: null` 的 section。

### PaddleOCR Cloud (可选，默认已配置)

如需使用 PaddleOCR 云端增强识别，需配置环境变量：

```bash
# 设置 API URL（文档版面分析）⚠️ 请替换为你自己申请的接口地址
set PADDLEOCR_DOC_PARSING_API_URL=https://c474r929pea0qa6c.aistudio-app.com/layout-parsing

# 设置 Access Token ⚠️ 请替换为你自己的 Token
set PADDLEOCR_ACCESS_TOKEN=86b3f40ddd719dad76e496472d341f1ba89085e3
```

> ⚠️ **注意**：示例中的 API URL 和 Token 仅供测试。如需生产环境使用，请前往 [百度智能云](https://login.bce.baidu.com/) 或 [AI Studio](https://aistudio.baidu.com/) 申请自己的 PaddleOCR Cloud 服务。

配置后，图片 OCR 会优先使用 PaddleOCR Cloud 作为第一引擎（若失败则自动降级到 RapidOCR）。