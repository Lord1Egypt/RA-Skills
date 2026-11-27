# Online_MinerU

Convert PDF files into high-quality Markdown with **MinerU's precise parsing API**. Automatically handles large books (splits >200 pages / >200MB, parses in parallel, reassembles in page order), keeps images, and removes page headers/footers/page numbers.

## Features

- Local file mode and remote URL mode (MinerU fetches the file server-side).
- Automatic splitting to satisfy MinerU's ≤200-page / ≤200MB per-file limits.
- Image extraction with per-chunk folders to avoid filename collisions.
- Safe header/footer/page-number removal driven by MinerU's layout types.
- Resume and retry support.
- `vlm` and `pipeline` model options; OCR auto-detection for scanned PDFs.

## Quick start

```bash
bash scripts/setup.sh
export MINERU_API_TOKEN="your-token"      # or pass --token
./.venv/bin/python scripts/mineru_pdf2md.py "/path/book.pdf" --outdir "./out" --name "book"
```

Remote URL mode:

```bash
./.venv/bin/python scripts/mineru_pdf2md.py --pdf-url "https://example.com/book.pdf" \
    --total-pages 717 --name "book" --outdir "./out"
```

Get a token at https://mineru.net/apiManage. See `SKILL.md` for full options and `references/API.md` for the API details.

## 中文简介

用 MinerU 精准解析 API 把 PDF 转成 Markdown：自动拆分超大文件、并行解析、按页序合并，保留图片，清理页眉页脚页码。支持本地文件与远程 URL 两种模式。安装 `bash scripts/setup.sh`，Token 用环境变量 `MINERU_API_TOKEN` 提供。详见 `SKILL.md`。
