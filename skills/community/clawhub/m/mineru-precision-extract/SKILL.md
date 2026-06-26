---
name: mineru-precision-extract
description: >
  MinerU precision extract — high-accuracy document extraction with full feature set. Convert PDFs, scanned documents, images, Word (DOC/DOCX), PowerPoint (PPT/PPTX), and HTML files into Markdown, HTML, LaTeX, DOCX, or JSON with table recognition, formula recognition (LaTeX), and advanced OCR.
  Choose between vlm model for highest accuracy on complex layouts, academic papers, and intricate tables, or pipeline model for zero-hallucination reliable extraction. Supports batch processing of hundreds of files, web page crawling to Markdown, and multi-format output in a single command.
  Use this skill when you need to: extract tables from PDFs, recognize formulas in academic papers, convert PDF to HTML or LaTeX, batch process document files, OCR scanned documents with high precision, convert documents to DOCX format, crawl web pages to structured Markdown, or process documents with complex layouts.
  Supports 80+ languages across Latin, Arabic, Cyrillic, Devanagari, CJK, and more script families. Handles large files with no size or page limits, unlike quick extraction modes.
  Built for researchers, data engineers, academic institutions, and production document pipelines that demand accuracy and reliability. Works as a Claude Code skill, MCP tool, or standalone CLI.
  高精度PDF提取、表格识别、公式识别、PDF转HTML、PDF转LaTeX、PDF转DOCX、批量PDF处理、扫描件OCR、学术论文解析、多格式文档转换。支持VLM高精度模型和零幻觉Pipeline模型，80+语言支持，适用于学术研究、数据工程和生产环境文档处理。
read_when:
  - Extracting tables from documents
  - Converting PDF to HTML, LaTeX, or DOCX
  - Batch document processing
  - OCR on scanned documents
  - Crawling web pages to Markdown
  - High-precision document extraction
  - Formula recognition in documents
  - Multi-format document conversion
  - Converting documents with tables
  - Processing large PDF files
metadata: {"openclaw":{"emoji":"📄","homepage":"https://mineru.net","source":"https://github.com/MinerU-Extract/mineru-precision-extract","author":"OpenDataLab","requires":{"bins":["mineru-open-api"],"env":["MINERU_TOKEN"],"config":["~/.mineru/config.yaml"]},"install":[{"id":"npm","kind":"node","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via npm"},{"id":"go","kind":"go","package":"github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api","bins":["mineru-open-api"],"label":"Install via go install","os":["darwin","linux"]}]}}
allowed-tools: Bash(mineru-open-api:*)
---

# Precision Document Extraction with mineru-open-api

Full-featured document extraction with table/formula recognition, OCR, multi-format output, batch processing, and web crawling.

## Why use extract?

- **Table recognition** — accurately extracts tables from PDFs and images
- **Formula recognition** — preserves mathematical formulas as LaTeX
- **Multi-format output** — Markdown, HTML, LaTeX, DOCX, JSON
- **Model selection** — choose `vlm` for highest accuracy or `pipeline` for zero-hallucination
- **Batch processing** — process hundreds of files in one command
- **Web crawling** — convert web pages to structured Markdown
- **All file formats** — PDF, images, DOC, DOCX, PPT, PPTX, HTML
- **Higher limits** — much larger file size and page count than quick mode
- **80+ languages** — full language coverage across all script families

## Installation

```bash
npm install -g mineru-open-api
```

Or via Go (macOS/Linux):

```bash
go install github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api@latest
```

### Verify installation

```bash
mineru-open-api version
```

## Authentication

Create a token at https://mineru.net/apiManage/token, then configure:

```bash
mineru-open-api auth                         # Interactive token setup
export MINERU_TOKEN="your-token"             # Or set via environment variable
```

Token resolution order: `--token` flag > `MINERU_TOKEN` env > `~/.mineru/config.yaml`.

## Quick start

```bash
mineru-open-api extract report.pdf                         # Markdown to stdout
mineru-open-api extract report.pdf -o ./out/               # Save to directory
mineru-open-api extract report.pdf -f md,html,docx -o ./   # Multi-format
mineru-open-api extract report.pdf --model vlm -o ./out/   # High-accuracy mode
mineru-open-api extract *.pdf -o ./results/                # Batch extract
mineru-open-api crawl https://example.com/article          # Web page → Markdown
```

## Supported input formats

| Format | Supported |
|--------|:-:|
| PDF (`.pdf`) | Yes |
| Images (`.png`, `.jpg`, `.jpeg`, `.jp2`, `.webp`, `.gif`, `.bmp`) | Yes |
| Word (`.doc`, `.docx`) | Yes |
| PowerPoint (`.ppt`, `.pptx`) | Yes |
| HTML (`.html`) | Yes |
| URLs (remote files) | Yes |

## Commands

### extract — Precision extraction

```bash
mineru-open-api extract <file-or-url> [...] [flags]
```

#### Examples

```bash
mineru-open-api extract report.pdf                         # Markdown to stdout
mineru-open-api extract report.pdf -f html                 # HTML to stdout
mineru-open-api extract report.pdf -o ./out/               # Save to directory
mineru-open-api extract report.pdf -o ./out/ -f md,docx    # Multiple formats
mineru-open-api extract report.pdf -f latex -o ./out/      # LaTeX output
mineru-open-api extract report.pdf --model vlm -o ./out/   # High-accuracy mode
mineru-open-api extract report.pdf --ocr -o ./out/         # OCR for scanned docs
mineru-open-api extract report.pdf --language en -o ./out/ # Specify language
mineru-open-api extract report.pdf --pages "1-10" -o ./out/  # Page range
mineru-open-api extract *.pdf -o ./results/                # Batch extract
mineru-open-api extract --list files.txt -o ./results/     # Batch from file list
mineru-open-api extract https://example.com/doc.pdf        # Extract from URL
cat doc.pdf | mineru-open-api extract --stdin -o ./out/    # From stdin
```

#### extract flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | _(stdout)_ | Output path (file or directory) |
| `--format` | `-f` | `md` | Output formats: `md`, `json`, `html`, `latex`, `docx` (comma-separated) |
| `--model` | | _(auto)_ | Model: `vlm`, `pipeline`, `html` (see below) |
| `--ocr` | | `false` | Enable OCR for scanned documents |
| `--formula` | | `true` | Enable/disable formula recognition |
| `--table` | | `true` | Enable/disable table recognition |
| `--language` | | `ch` | Document language |
| `--pages` | | _(all)_ | Page range, e.g. `1-10,15` |
| `--timeout` | | `900`/`1800` | Timeout in seconds (single/batch) |
| `--list` | | | Read input list from file (one path per line) |
| `--concurrency` | | `0` | Batch concurrency (0 = server default) |

#### Model comparison: vlm vs pipeline

| | `vlm` | `pipeline` |
|---|---|---|
| Parsing accuracy | Higher — better at complex layouts, mixed content | Standard |
| Hallucination risk | May produce hallucinated text in rare cases | **No hallucination** — biggest advantage |
| Best for | Academic papers, complex tables, intricate layouts | General documents where fidelity matters most |

When the user values accuracy and the document has complex formatting, suggest `--model vlm`. When the user prioritizes reliability and no-hallucination guarantee, suggest `--model pipeline` (or omit `--model` to use auto).

### crawl — Web page extraction

Fetch web pages and convert to structured Markdown.

```bash
mineru-open-api crawl https://example.com/article              # Markdown to stdout
mineru-open-api crawl https://example.com/article -f html      # HTML to stdout
mineru-open-api crawl https://example.com/article -o ./out/    # Save to file
mineru-open-api crawl url1 url2 -o ./pages/                    # Batch crawl
mineru-open-api crawl --list urls.txt -o ./pages/              # Batch from file list
```

#### crawl flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | _(stdout)_ | Output path |
| `--format` | `-f` | `md` | Output formats: `md`, `json`, `html` (comma-separated) |
| `--timeout` | | `900`/`1800` | Timeout in seconds (single/batch) |
| `--list` | | | Read URL list from file (one per line) |
| `--stdin-list` | | `false` | Read URL list from stdin |
| `--concurrency` | | `0` | Batch concurrency |

### auth — Authentication management

```bash
mineru-open-api auth              # Interactive token setup
mineru-open-api auth --verify     # Verify current token is valid
mineru-open-api auth --show       # Show current token source and masked value
```

## Supported `--language` values

Values are organized by script/language family — each value covers all languages in its group.

### Standalone language packs

| Value | Included languages | 说明 |
|-------|-------------------|------|
| `ch` | Chinese, English, Chinese Traditional | 中英文（默认值） |
| `ch_server` | Chinese, English, Chinese Traditional, Japanese | 繁体、手写体 |
| `en` | English | 纯英文 |
| `japan` | Chinese, English, Chinese Traditional, Japanese | 日文为主 |
| `korean` | Korean, English | 韩文 |
| `chinese_cht` | Chinese, English, Chinese Traditional, Japanese | 繁体中文为主 |
| `ta` | Tamil, English | 泰米尔文 |
| `te` | Telugu, English | 泰卢固文 |
| `ka` | Kannada | 卡纳达文 |
| `el` | Greek, English | 希腊文 |
| `th` | Thai, English | 泰文 |

### Language family packs

| Value | Script/Family | Included languages |
|-------|--------------|-------------------|
| `latin` | Latin script (拉丁语系) | French, German, Afrikaans, Italian, Spanish, Bosnian, Portuguese, Czech, Welsh, Danish, Estonian, Irish, Croatian, Uzbek, Hungarian, Serbian (Latin), Indonesian, Occitan, Icelandic, Lithuanian, Maori, Malay, Dutch, Norwegian, Polish, Slovak, Slovenian, Albanian, Swedish, Swahili, Tagalog, Turkish, Latin, Azerbaijani, Kurdish, Latvian, Maltese, Pali, Romanian, Vietnamese, Finnish, Basque, Galician, Luxembourgish, Romansh, Catalan, Quechua |
| `arabic` | Arabic script (阿拉伯语系) | Arabic, Persian, Uyghur, Urdu, Pashto, Kurdish, Sindhi, Balochi, English |
| `cyrillic` | Cyrillic script (西里尔语系) | Russian, Belarusian, Ukrainian, Serbian (Cyrillic), Bulgarian, Mongolian, Abkhazian, Adyghe, Kabardian, Avar, Dargin, Ingush, Chechen, Lak, Lezgin, Tabasaran, Kazakh, Kyrgyz, Tajik, Macedonian, Tatar, Chuvash, Bashkir, Malian, Moldovan, Udmurt, Komi, Ossetian, Buryat, Kalmyk, Tuvan, Sakha, Karakalpak, English |
| `east_slavic` | East Slavic (东斯拉夫语系) | Russian, Belarusian, Ukrainian, English |
| `devanagari` | Devanagari script (天城文语系) | Hindi, Marathi, Nepali, Bihari, Maithili, Angika, Bhojpuri, Magahi, Santali, Newari, Konkani, Sanskrit, Haryanvi, English |

## Global flags

| Flag | Short | Description |
|------|-------|-------------|
| `--token` | | API token (overrides env and config) |
| `--base-url` | | API base URL (for private deployments) |
| `--verbose` | `-v` | Verbose mode, print HTTP details |

## Output behavior

- **No `-o` flag**: result goes to stdout; status/progress messages go to stderr
- **With `-o` flag**: result saved to file/directory; progress messages on stderr
- **Batch mode** (`extract`/`crawl`): requires `-o` to specify output directory
- **Binary formats** (`docx`): cannot output to stdout, must use `-o`
- Markdown output includes extracted images saved alongside the `.md` file

## Agent guidelines

When using this skill on behalf of the user:

- **Quote file paths** that contain spaces or special characters with double quotes. Example: `mineru-open-api extract "report 01.pdf"`.
- **Don't run commands blindly on errors** — explain the exit code and troubleshooting steps.
- **Installation questions** ("mineru 怎么安装") should be answered with the install instructions above.
- For **stdout mode** (no `-o`), only one text format can be output at a time. If the user wants multiple formats, suggest adding `-o`.
- If the user hasn't authenticated yet, guide them to create a token at https://mineru.net/apiManage/token and run `mineru-open-api auth`.

### Default output directory

When the user does NOT specify `-o`, generate a default output directory:

```
~/MinerU-Skill/<name>_<hash>/
```

- `<name>`: derived from the source, then **sanitized** (replace spaces and shell-unsafe characters with `_`, collapse consecutive `_`).
  - For URLs: last path segment (e.g. `https://arxiv.org/pdf/2509.22186` → `2509.22186`)
  - For local files: filename without extension (e.g. `report.pdf` → `report`)
- `<hash>`: first 6 characters of MD5 hash of the full original source.

```bash
echo -n "source" | md5sum | cut -c1-6   # Linux
echo -n "source" | md5 | cut -c1-6      # macOS
```

When the user specifies `-o`: use the user's path as-is.

### Skill upgrade = CLI upgrade

When the user asks to upgrade this skill, re-install the CLI first:

```bash
npm install -g mineru-open-api@latest
```

## Exit codes

| Code | Meaning | Recovery |
|------|---------|----------|
| 0 | Success | — |
| 1 | General API or unknown error | Check network; retry; use `--verbose` |
| 2 | Invalid parameters / usage error | Check command syntax and flag values |
| 3 | Authentication error | Create or refresh token at https://mineru.net/apiManage/token, then run `mineru-open-api auth` |
| 4 | File too large or page limit exceeded | Split the file or use `--pages` |
| 5 | Extraction failed | Document may be corrupted; try a different `--model` |
| 6 | Timeout | Increase with `--timeout`; large files may need 1600+ seconds |

## Troubleshooting

- **"no API token found"**: Run `mineru-open-api auth` or set `MINERU_TOKEN` env variable. Create token at https://mineru.net/apiManage/token.
- **Timeout on large files**: Increase with `--timeout 1600`
- **Batch fails partially**: Check stderr for per-file status; succeeded files are still saved
- **Binary format to stdout**: Use `-o` flag; `docx` cannot stream to stdout
- **Private deployment**: Use `--base-url https://your-server.com/api`
- **Extraction quality is poor**: Try `--model vlm` for complex layouts, or `--ocr` for scanned documents
- **Tables not extracted correctly**: Try `--model vlm` for better table recognition

## Reporting Issues

- Skill issues: Open an issue at https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli
- CLI issues: Open an issue at https://github.com/MinerU-Extract/mineru-document-extractor