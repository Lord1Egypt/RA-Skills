---
name: mineru-fast
description: >
  MinerU fast extract — zero-setup, instant document extraction. Convert PDFs, images, Word (DOCX), and PowerPoint (PPTX) to Markdown with no login, no token, no API key, no configuration required. Just install and run.
  Powered by the MinerU flash-extract engine with built-in OCR, table recognition, and formula extraction (LaTeX). Handles scanned documents, photos of text, academic papers, contracts, invoices, resumes, and slides out of the box.
  Use this skill when you need to: quickly extract text from a PDF, convert a document to Markdown without signing up, read a scanned PDF, turn a Word file into Markdown, parse a PowerPoint presentation, OCR an image, extract content from a PDF file, or get a fast document conversion with no setup.
  Supports 80+ languages including Chinese, English, Japanese, Korean, Arabic, Hindi, French, German, Spanish, Russian, and many more. Works with local files and remote URLs.
  Ideal for developers, researchers, students, and anyone who wants instant document parsing without accounts or API tokens. Use as a Claude Code skill, agent tool, or standalone CLI.
  PDF提取、文档转Markdown、免登录PDF转换、快速文档提取、扫描件OCR、图片转文字、Word转Markdown、PPT转Markdown、PDF解析、零配置文档转换。无需注册、无需Token，安装即用，一键提取PDF、Word、PPT、图片中的文字内容。
read_when:
  - Extracting text from PDF documents
  - Converting documents to Markdown
  - Parsing document content
  - Reading PDF files
  - Converting Word documents
  - Quick document parsing without login
  - OCR on scanned documents
  - Fast document conversion
  - Extracting tables from documents
  - Extracting formulas from documents
  - Converting LaTeX formulas from PDF
metadata: {"openclaw":{"emoji":"⚡","homepage":"https://mineru.net","source":"https://github.com/MinerU-Extract/mineru-fast-extract","author":"OpenDataLab","requires":{"bins":["mineru-open-api"]},"install":[{"id":"npm","kind":"node","package":"mineru-open-api","bins":["mineru-open-api"],"label":"Install via npm"},{"id":"go","kind":"go","package":"github.com/opendatalab/MinerU-Ecosystem/cli/mineru-open-api","bins":["mineru-open-api"],"label":"Install via go install","os":["darwin","linux"]}]}}
allowed-tools: Bash(mineru-open-api:*)
---

# Fast Document Extraction with mineru-open-api

Zero-setup, instant document parsing — no login, no token, no configuration needed. Supports tables and formulas (LaTeX).

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

## Quick start

```bash
mineru-open-api flash-extract report.pdf                     # PDF → Markdown (instant!)
mineru-open-api flash-extract report.pdf -o ./out/           # Save to file
mineru-open-api flash-extract resume.docx                    # Word → Markdown
mineru-open-api flash-extract slides.pptx                    # PowerPoint → Markdown
mineru-open-api flash-extract photo.png                      # Image → Markdown (OCR)
mineru-open-api flash-extract https://example.com/doc.pdf    # URL → Markdown
```

## Supported input formats

| Format | Supported |
|--------|:-:|
| PDF (`.pdf`) | Yes |
| Images (`.png`, `.jpg`, `.jpeg`, `.jp2`, `.webp`, `.gif`, `.bmp`) | Yes |
| Word (`.docx`) | Yes |
| PowerPoint (`.pptx`) | Yes |
| URLs (remote files) | Yes |

## Command: flash-extract

```bash
mineru-open-api flash-extract <file-or-url> [flags]
```

### Flags

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--output` | `-o` | _(stdout)_ | Output path (file or directory) |
| `--language` | | `ch` | Document language |
| `--pages` | | _(all)_ | Page range, e.g. `1-10` |
| `--timeout` | | `900` | Timeout in seconds |

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

## Examples

```bash
mineru-open-api flash-extract report.pdf
mineru-open-api flash-extract report.pdf -o ./out/
mineru-open-api flash-extract report.pdf --language en
mineru-open-api flash-extract report.pdf --language latin
mineru-open-api flash-extract report.pdf --pages "1-5"
mineru-open-api flash-extract contract.docx -o ./out/
mineru-open-api flash-extract presentation.pptx -o ./out/
mineru-open-api flash-extract scan.jpg --language ch
```

## Output behavior

- **No `-o` flag**: result goes to stdout; status/progress messages go to stderr
- **With `-o` flag**: result saved to file/directory; progress messages on stderr
- Markdown output includes extracted images saved alongside the `.md` file
- **Tables** are converted to Markdown tables
- **Formulas** are converted to LaTeX format (inline `$...$` and block `$$...$$`)

## Agent guidelines

When using this skill on behalf of the user:

- **Always use `flash-extract`** for any input — whether it's a local file or a URL (e.g. `https://cdn-mineru.openxlab.org.cn/demo/example.pdf`). Do NOT assume a URL means "web page". `flash-extract` handles URLs to document files directly.
- **Quote file paths** that contain spaces or special characters with double quotes. Example: `mineru-open-api flash-extract "report 01.pdf"`.
- **Don't run commands blindly on errors** — explain the exit code and troubleshooting steps instead of re-running the command.
- **Installation questions** ("mineru 怎么安装") should be answered with the install instructions above.

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
| 4 | File too large or page limit exceeded | Try a smaller file or fewer pages |
| 5 | Extraction failed | Document may be corrupted or unsupported |
| 6 | Timeout | Increase with `--timeout` |

## Troubleshooting

- **Timeout on large files**: Increase with `--timeout 1600`
- **Extraction quality is poor**: Try specifying `--language` to match the document language
- **HTTP 429**: Rate limit hit. Wait a few minutes and retry.