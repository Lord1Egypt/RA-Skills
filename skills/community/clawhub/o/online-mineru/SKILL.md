---
name: online-mineru
description: "Convert PDFs to Markdown with MinerU's precise parsing API. Splits and reassembles files over the 200-page/200MB limit, keeps images, cleans headers/footers. Works with local files or a remote URL."
---

# Online_MinerU

Convert a PDF into Markdown (`.md` + `images/`) using **MinerU's precise parsing API**. Large documents that exceed MinerU's per-file limits (≤200 pages, ≤200MB) are split, parsed in parallel, and merged back in page order. Images are preserved; page headers/footers/page numbers are removed.

## Requirements

- Python 3.9+ and pip.
- A MinerU API token from https://mineru.net/apiManage (precise parsing API). Tokens can expire, renew when needed.
- Install dependencies (creates `.venv` with `pypdf` + `requests`):

```bash
bash scripts/setup.sh
```

Run everything with `./.venv/bin/python` after that.

## Token

Provide the token by any of: `--token`, environment variable `MINERU_API_TOKEN`, a `MINERU_API_TOKEN=...` line in `~/.openclaw/.env`, or a `.secrets/mineru_token` file in the skill folder. Never commit the token.

**Token expiry:** MinerU API keys are valid for at most about **90 days**. If parsing starts failing with an auth / HTTP 401/403 error, the key has likely expired — renew it at https://mineru.net/apiManage and update `MINERU_API_TOKEN`.

## Usage

### A. Local PDF

```bash
./.venv/bin/python scripts/mineru_pdf2md.py "/path/book.pdf" --outdir "/path/out" --name "book"
```

Optional tuning:

```bash
... --ocr auto|on|off --model vlm|pipeline --language ch
```

### B. Remote PDF by URL (recommended when the file is not local)

Give MinerU a publicly reachable, China-friendly URL and MinerU fetches it server-side — no large download to your machine. For files over 200 pages pass the total page count so the script splits by page ranges:

```bash
./.venv/bin/python scripts/mineru_pdf2md.py --pdf-url "https://example.com/book.pdf" \
    --total-pages 717 --name "book" --outdir "/path/out"
```

- ≤200 pages: omit `--total-pages`.
- Scanned PDF: add `--ocr on`.
- The URL must be reachable by MinerU (GitHub/AWS and some foreign URLs time out; a domestic/China URL is best).

### OpenList/AList direct-link helper

If the file lives on OpenList/AList, resolve a direct link automatically (also fixes the port):

```bash
./.venv/bin/python scripts/openlist_url.py --base https://host:8443 \
    --username USER --password PASS --path "/dir/book.pdf"
```

The printed URL can be passed straight to `--pdf-url`.

## Options (key)

- `--ocr auto|on|off` — `auto` samples the text layer to detect scanned PDFs.
- `--model vlm|pipeline` — default `vlm` (higher accuracy).
- `--no-clean-hf` — disable header/footer/page-number removal.
- `--no-formula`, `--no-table` — disable formula/table recognition.
- `--resume` — reuse `.mineru_work/<job>/state.json` to retry without re-uploading.
- `--allow-partial` — merge successful chunks even if some failed.
- `--pdf-url`, `--total-pages` — URL mode.
- `--dry-run` — only split and print chunks, no API calls.

## Output

```
<outdir>/<name>/
├── <name>.md
├── images/chunk_0001/...
└── manifest.json
```

## How it works

1. Split to ≤200 pages; re-split any chunk >200MB by halving pages.
2. Apply batch upload URLs (≤50 per request) → PUT upload (no Content-Type) → MinerU auto-submits.
3. Poll `extract-results/batch/{batch_id}` until `done`.
4. Download each zip (`full.md`, `images/`, `*_content_list.json`), drop header/footer/page_number blocks by type, rewrite image paths per chunk, and concatenate in page order.

## Limitations

- A table/paragraph crossing a split boundary may break there.
- MinerU already drops most headers/footers; content_list-based cleaning is a safe fallback.
- MinerU accounts have ~1000 highest-priority pages/day; beyond that is lower priority (slower).
- PDF only for now.
- Encrypted PDFs must be decrypted; scanned PDFs rely on OCR.

API reference: `references/API.md`.

---

## 中文说明

用 **MinerU 精准解析 API** 把 PDF 转成 Markdown（md + images 目录）。超过单文件限制（≤200 页 / ≤200MB）时会自动拆分、并行解析、按页序合并；保留图片，清理页眉/页脚/页码。

安装：`bash scripts/setup.sh`。Token 用环境变量 `MINERU_API_TOKEN` 或 `--token` 提供。

**Token 有效期**：MinerU 的 Key 最长约 **90 天**；若解析报鉴权失败 / HTTP 401/403，多半是 Key 过期，请到 https://mineru.net/apiManage 更换并更新 `MINERU_API_TOKEN`。

本地文件：

```bash
./.venv/bin/python scripts/mineru_pdf2md.py "/路径/书.pdf" --outdir "/输出" --name "书名"
```

URL 模式（文件不在本机时推荐，由 MinerU 服务器侧拉取，无需下载大文件）：

```bash
./.venv/bin/python scripts/mineru_pdf2md.py --pdf-url "https://example.com/book.pdf" \
    --total-pages 717 --name "书名" --outdir "/输出"
```

- ≤200 页不用加 `--total-pages`；扫描件加 `--ocr on`。
- URL 必须 MinerU 能访问（国外链接可能超时，国内直链最佳）。
- OpenList/AList 可用 `scripts/openlist_url.py` 自动取直链并修正端口。

输出：`<outdir>/<书名>/<书名>.md` + `images/` + `manifest.json`，图片引用形如 `images/chunk_0001/xxx.jpg`。详见 `references/API.md`。
