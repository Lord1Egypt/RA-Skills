---
name: minimax-pdf-analysis
description: Analyze PDF files using MiniMax API. Supports text extraction, keyword search, and image-based VLM analysis (converts PDF pages to images first). Requires MiniMax Coding Plan API key (sk-cp-*).
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["python","node"],"env":["MINIMAX_API_KEY"]}}}
---

# MiniMax PDF Analysis

使用 MiniMax API 分析 PDF，支援三種模式。

## 三種分析模式

### 1. 萃取文字 `extract`
```bash
python scripts/analyze_pdf.py extract input.pdf
python scripts/analyze_pdf.py extract input.pdf --output out.txt
python scripts/analyze_pdf.py extract input.pdf --pages 1-3
```

### 2. 搜尋關鍵字 `search`
```bash
python scripts/analyze_pdf.py search input.pdf "PID"
python scripts/analyze_pdf.py search input.pdf "error" --ignore-case
python scripts/analyze_pdf.py search input.pdf "regex.*pattern" --regex
```

### 3. VLM 圖片分析 `vision`
```bash
# 需要 MINIMAX_API_KEY 環境變數
export MINIMAX_API_KEY=sk-cp-xxx

# 分析整份 PDF（每頁轉圖片後分析）
python scripts/analyze_pdf.py vision input.pdf "摘要這張投影片的內容"

# 只分析特定頁面
python scripts/analyze_pdf.py vision input.pdf "摘要" --pages 1-3 --dpi 200
```

## 環境需求

| 套件 | 安裝方式 |
|------|---------|
| PyMuPDF | `pip install pymupdf` |
| MiniMax API Key | `MINIMAX_API_KEY=sk-cp-xxx` |
