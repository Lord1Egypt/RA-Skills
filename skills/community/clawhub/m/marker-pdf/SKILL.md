---
name: marker-pdf
description: "Use when converting scanned PDFs or documents to markdown/JSON/HTML. Marker (Datalab) uses surya OCR for 90+ languages including Arabic."
version: 1.0.0
author: Hermes Agent
license: MIT-0
platforms: [linux, macos, windows]
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
  hermes:
    tags: [pdf, ocr, markdown, arabic, document-conversion, surya]
    category: mlops
    related_skills: [ocr-and-documents, llm-wiki]
---

# Marker PDF — Scanned Document to Markdown

Convert PDFs, images, DOCX, PPTX, HTML, EPUB into clean markdown, JSON, or HTML.
Uses [surya](https://github.com/VikParuchuri/surya) for OCR (90+ languages including Arabic)
and layout detection. Optionally uses an LLM for higher accuracy.

## When to Use

- Converting scanned PDFs (especially Arabic/multilingual) to searchable markdown
- Extracting tables, equations, code blocks from PDFs
- Preparing documents for LLM ingestion (wiki, RAG, knowledge base)
- Batch converting multiple PDFs to markdown

**Don't use for:** Native digital PDFs with good text (just extract text directly).
Don't use for single-page images (use `vision_analyze` instead).

## Installation (Bootc/Fedora Atomic — Container-Based)

On immutable systems (Bootc, Silverblue, etc.), use `uv` inside a container or a venv:

```bash
# Option A: uv tool install (isolated, best for CLI use)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install marker-pdf

# Option B: uv venv + pip (if you need Python API access)
uv venv ~/.venvs/marker && source ~/.venvs/marker/bin/activate
uv pip install marker-pdf

# Option C: Podman container (fully isolated)
podman run --rm -v ./pdfs:/data -it python:3.12-slim \
  bash -c "pip install marker-pdf && marker_single /data/input.pdf -o /data/output/"
```

First run downloads ~1GB of ML models to `~/.cache/marker/`.

## CLI Usage

### Single file

```bash
marker_single /path/to/file.pdf -o /path/to/output/
```

Key flags:
- `--output_format [markdown|json|html|chunks]` — default: markdown
- `--force_ocr` — force OCR on all pages (use for scanned PDFs)
- `--strip_existing_ocr` — remove existing OCR text, re-OCR with surya
- `--page_range "0,5-10,20"` — process specific pages
- `--use_llm` — boost accuracy with an LLM (needs API key)
- `--disable_image_extraction` — skip image extraction
- `--paginate_output` — add page number markers
- `--debug` — save debug images with layout overlays

### Batch conversion

```bash
marker /path/to/input/folder/ -o /path/to/output/ --workers 4
```

### Arabic / RTL documents

```bash
# Force OCR (recommended for scanned Arabic PDFs)
marker_single arabic.pdf -o ./output/ --force_ocr

# With LLM boost for better accuracy
marker_single arabic.pdf -o ./output/ --force_ocr --use_llm \
  --llm_service marker.services.gemini.GoogleGeminiService \
  --gemini_api_key YOUR_KEY
```

Surya OCR supports Arabic natively. For scanned documents, always use `--force_ocr`.

### Table extraction only

```bash
marker_single file.pdf -o ./output/ \
  --converter_cls marker.converters.table.TableConverter \
  --output_format json
```

## Python API

```python
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

converter = PdfConverter(artifact_dict=create_model_dict())
rendered = converter("input.pdf")
text, _, images = text_from_rendered(rendered)
# text is markdown string
```

### With custom config

```python
from marker.config.parser import ConfigParser

config = {"output_format": "json", "force_ocr": True}
config_parser = ConfigParser(config)
converter = PdfConverter(
    config=config_parser.generate_config_dict(),
    artifact_dict=create_model_dict(),
    processor_list=config_parser.get_processors(),
    renderer=config_parser.get_renderer(),
)
rendered = converter("input.pdf")
```

## Output Formats

| Format | Contents |
|--------|----------|
| **Markdown** | Text + images (saved separately) + tables + LaTeX equations + code blocks |
| **JSON** | Tree of blocks with types, bounding boxes, HTML, images (base64) |
| **HTML** | Full HTML with img tags, math tags, pre tags |
| **Chunks** | Flattened list of top-level blocks with full HTML (for RAG) |

## LLM Services (for `--use_llm`)

| Service | Flag | Key needed |
|---------|------|------------|
| Gemini (default) | `--gemini_api_key` | GOOGLE_API_KEY env or flag |
| Ollama | `--llm_service marker.services.ollama.OllamaService` | `--ollama_base_url`, `--ollama_model` |
| Claude | `--llm_service marker.services.claude.ClaudeService` | `--claude_api_key` |
| OpenAI | `--llm_service marker.services.openai.OpenAIService` | `--openai_api_key`, `--openai_model` |

### Performance Notes

- GPU: ~0.18s/page (H100), ~1-3s/page (CPU)
- VRAM: ~3.5GB average per worker, 5GB peak
- 60-page PDF on CPU: expect 2-5 minutes (after models cached)
- Reduce `--workers` if running out of memory

## Common Pitfalls

1. **Garbled output on scanned PDFs** — always use `--force_ocr` for scanned documents
2. **Out of memory** — decrease `--workers` or split the PDF into smaller chunks
3. **Missing Arabic text** — surya supports Arabic natively; if results are poor, try `--strip_existing_ocr --force_ocr`
4. **Large model download on first run** — ~1.35GB `model.safetensors` downloaded from `models.datalab.to` to `~/.cache/datalab/models/layout/<date>/`. The connection may break mid-download (BrokenPipeError) — marker retries 3 times automatically. On slow connections, run as a background process (`notify_on_complete=true`) with a high foreground timeout (600s) so the retry mechanism has room. See `references/model-download-pitfalls.md`.
5. **Python 3.10+ required** — check with `python3 --version`
6. **No GPU?** — works on CPU, just slower. Set `TORCH_DEVICE=cpu` if auto-detect fails
7. **License** — model weights: OpenRAIL-M (free for research/personal/startups <$2M). Code: GPL-3.0

## Post-OCR Cleanup

Marker output for Arabic scanned PDFs typically has ~85% readable text quality. Common issues:

- **Letter substitution:** ب↔ج, ت↔ث, etc. — tolerable, meaning still clear
- **Repetition tails:** Lines where OCR hallucinates the same word 10+ times at the end (e.g., "المسافرة المسافرة المسافرة...")
- **Pure garbage:** English gobbledygook from corrupted table cells ("ASS NO. 10" x 40, "second second second...")
- **Fine-print mangling:** Table of contents, formulas, very small fonts get heavy noise

Run this cleanup AFTER marker_single output. The key patterns to detect and fix:

1. **Page markers** `{N}----------------` and **table separators** `|---|---|` — PRESERVE these, they are structural
2. **English-only garbage** — "ASS NO" / "second second" / "STATE OF THE STATE" repeated 5+ times with no Arabic characters → REMOVE the line
3. **Arabic repetition tails** — "الله الله الله الله" or "المسافرة المسافرة" repeated 4+ times at the end of a line that starts valid → TRUNCATE before the repetition
4. **Line-wide repetition** — a single word repeated 8+ times forming the entire line → REMOVE

For the full reusable cleanup script with all patterns, see `references/arabic-ocr-cleanup.md`.

## Pipeline: OCR → Wiki

End-to-end workflow for scanned Arabic PDFs into an LLM wiki (see also `llm-wiki` skill):

### Step 1 — OCR (this skill)
```bash
marker_single "/path/to/document.pdf" \
  --output_dir /tmp/marker-output \
  --force_ocr \
  --paginate_output \
  --output_format markdown
```
Run in **background** with `notify_on_complete=true` — model downloads ~1.5GB on first run and can take 10+ minutes.

### Step 2 — Clean
Apply the cleanup approach above (or the full script in references/). Save cleaned output to `raw/papers/` in the wiki:
```bash
cp /tmp/marker-output/cleaned-document.md ~/wiki/raw/papers/<subject>.md
```
### Step 3 — Ingest (via `llm-wiki` skill)

Ingest to the target wiki. For a main wiki:

```bash
cp /tmp/marker-output/cleaned-document.md ~/wiki/raw/papers/<subject>.md
```

For a **sub-wiki** (e.g., academic study wiki under `~/wiki/study/` — see
llm-wiki skill's Multi-Wiki section):

```bash
cp /tmp/marker-output/cleaned-document.md ~/wiki/study/raw/papers/<subject>.md
```

Then:
1. Create a `concepts/` page summarizing the document's topics with `sources:` frontmatter linked to the raw file — in the **same wiki** as the raw file
2. Extend SCHEMA.md tags if the content introduces a new domain (sub-wiki's SCHEMA.md, not the parent's)
3. Update `index.md` with a new section link and page count (sub-wiki's index.md)
4. Append to `log.md` with full pipeline description (sub-wiki's log.md)

## Verification

- [ ] Check output markdown has correct Arabic text (no garbled characters)
- [ ] Tables are properly formatted (markdown table syntax)
- [ ] Equations are in LaTeX format ($$...$$)
- [ ] Page count matches input PDF
- [ ] Images extracted to output directory (if applicable)
- [ ] **Cleanup pass complete** — repetition tails removed, English-only garbage purged, page markers preserved
- [ ] **Wiki integration verified** — raw file in raw/papers/, concept page created, index.md updated, log.md appended
