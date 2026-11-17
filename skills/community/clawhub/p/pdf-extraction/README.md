# pdf-extract

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

簡易 PDF 擷取指令：自動判斷每一頁是**可選取文字**還是**掃描圖**，並選擇正確工具取出內容。

| 頁面類型 | 使用工具 |
|---------|---------|
| 原生文字 PDF | `pdfplumber` 文字 / 表格擷取 |
| 掃描 / 圖片型 PDF | PyMuPDF + Tesseract OCR |

使用者不必自己判斷內容類型。

## 安裝

### 系統需求

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)（掃描頁需要）

```bash
# Ubuntu / Debian
sudo apt install tesseract-ocr tesseract-ocr-eng
# 繁中可選：
# sudo apt install tesseract-ocr-chi-tra

# macOS
# brew install tesseract
```

### 用 pip 從 GitHub 安裝（推薦）

```bash
# 最新 main
pip install "git+https://github.com/alex-ht/pdf-extraction.git"

# 指定版本 tag
pip install "git+https://github.com/alex-ht/pdf-extraction.git@v1.0.0"
```

安裝後會提供 `pdf-extract` 指令：

```bash
pdf-extract --help
```

### 從 ClawHub 安裝（OpenClaw skill）

```bash
# OpenClaw
openclaw skills install @alex-ht/pdf-extraction

# 或 ClawHub CLI
clawhub install pdf-extraction
# 然後在 skill 目錄：pip install -e .
# 或直接：pip install "git+https://github.com/alex-ht/pdf-extraction.git"
```

Skill 頁面：https://clawhub.ai/alex-ht/pdf-extraction
### 從原始碼安裝（開發）

```bash
git clone https://github.com/alex-ht/pdf-extraction.git
cd pdf-extraction
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 使用方式

```bash
# 最簡單：自動判斷，輸出文字到終端
pdf-extract document.pdf

# 寫入檔案
pdf-extract document.pdf -o out.txt

# JSON（含每頁使用的 mode）
pdf-extract document.pdf --format json -o out.json

# Markdown + 表格
pdf-extract document.pdf --tables --format markdown -o out.md

# 只看某一頁會走 text 還是 ocr
pdf-extract document.pdf --analyze-only

# 強制整份用 OCR / 純文字
pdf-extract scan.pdf --mode ocr --ocr-lang eng
pdf-extract text.pdf --mode text

# 指定頁面
pdf-extract doc.pdf --pages 1-3,5

# 含 metadata
pdf-extract doc.pdf --meta --format markdown
```

也可：

```bash
python -m pdf_extract document.pdf
```

## 自動判斷邏輯（`--mode auto`）

對每一頁：

1. 用 pdfplumber 試抽文字、統計字元數與嵌入圖片數
2. 字元夠多且密度夠高 → **text**
3. 字元很少（預設 < 40）或幾乎是圖 → **ocr**

可用 `--min-text-chars` 調整門檻。

## 輸出格式

- `text`（預設）：純文字，含頁碼與 mode 標記
- `json`：結構化結果
- `markdown`：便於閱讀 / 文件化

## CLI 參數

| 旗標 | 說明 |
|------|------|
| `-o`, `--output` | 寫入檔案（預設 stdout） |
| `-f`, `--format` | `text` \| `json` \| `markdown` |
| `--mode` | `auto` \| `text` \| `ocr` |
| `--pages` | 例如 `1-3,5` |
| `--tables` | 在文字頁擷取表格 |
| `--layout` | 保留原生文字排版 |
| `--meta` | 包含 PDF metadata |
| `--ocr-lang` | Tesseract 語言（預設 `eng`） |
| `--ocr-dpi` | OCR 渲染 DPI（預設 `200`） |
| `--analyze-only` | 只輸出分類結果 JSON |
| `-q`, `--quiet` | 不在 stderr 顯示進度 |

## 依賴

- `pdfplumber` — 文字、表格、結構
- `pymupdf` — 頁面渲染 + 呼叫 Tesseract OCR
- `Pillow` — 影像支援
- 系統 `tesseract` — OCR 引擎

## 授權

[MIT](LICENSE)
