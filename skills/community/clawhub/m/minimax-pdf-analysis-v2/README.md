# MiniMax PDF Analysis Skill

Analyze PDF files using MiniMax Coding Plan API — supports text extraction, keyword search, and VLM image-based analysis.

## Features

- **Extract** — pull readable text out of any PDF
- **Search** — find keyword snippets inside PDF pages
- **Vision** — convert PDF pages to images, then analyze with MiniMax VLM (great for scanned/image-based PDFs)

## Setup

```bash
# Install dependencies
pip install pymupdf

# Set API key
export MINIMAX_API_KEY=sk-cp-xxx
```

Get your Coding Plan API key at: https://platform.minimaxi.com

## Usage

```bash
# Extract text
python scripts/analyze_pdf.py extract report.pdf --output text.txt

# Search inside PDF
python scripts/analyze_pdf.py search report.pdf "revenue" --ignore-case

# VLM image analysis (converts pages to PNG first)
python scripts/analyze_pdf.py vision report.pdf "請摘要這張投影片的內容"
python scripts/analyze_pdf.py vision report.pdf "分析這份文件的結構" --pages 1-5 --dpi 200
```

## How Vision Mode Works

```
PDF → PyMuPDF → PNG images → MiniMax VLM API → Text analysis
```

Works even on scanned/image-only PDFs that have no extractable text.

## License

MIT
