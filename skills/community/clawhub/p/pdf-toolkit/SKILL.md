---
name: pdf-toolkit
description: "Run a local script to work with PDF files, DOCX documents, OCR, and text-to-speech. Use the read tool to load this SKILL.md, then exec the uv run command inside it. Do NOT use sessions_spawn. Triggers: read pdf, extract text from pdf, merge pdfs, split pdf, rotate pdf, ocr pdf, read docx, create docx, text to speech, convert to mp3, pdf info, pdf pages."
homepage: https://pypdf.readthedocs.io
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["uv"]}}}
---

## System Dependencies
- `uv` must already be installed because this skill is executed with `uv run`, and `uv` installs the Python dependencies declared in `src/main.py`.
- `ffmpeg` is needed for `tts` because the speech output is normalized and written as an `.mp3` file through `ffmpeg`.
- `tesseract` is needed for `ocr` because it performs the actual optical character recognition on scanned page images.
- `pdfimages` is also needed for `ocr` because it extracts page images from PDFs before those images are passed to `tesseract`; `pdfimages` comes from `poppler`.
- `pandoc` is optional for `convert` because it can convert between many document formats when text-based conversion is possible.
- `libreoffice` is an optional alternative to `pandoc` for `convert` because it can handle document conversions that `pandoc` may not support well.

## File Access And Network Behavior
- This skill operates on the file paths provided by the caller. It can read from and write to any host path the caller supplies; it is not limited to the OpenClaw workspace.
- The `/root/.openclaw/workspace/...` paths in the command examples show where the skill entrypoint lives. They do not restrict which files the skill can access.
- The `tts` command uses `edge-tts`, which sends the input text to an external text-to-speech service over the network to generate audio.
- Do not use `tts` with sensitive or private text unless you are comfortable sending that text off-host.
- All other commands run locally on the host, subject to the optional local binaries documented below.

# Skill: PDF Toolkit

## When to use
- User wants to extract text, tables, or images from a PDF.
- User wants to get metadata or page count from a PDF.
- User wants to merge, split, or rotate a PDF.
- User wants to create a new PDF from plain text or Markdown.
- User wants to read or write a DOCX file.
- User wants to OCR a scanned PDF (requires `tesseract` on host).
- User wants to convert text or a document to an MP3 audio file (requires `ffmpeg` on host).
- User wants to convert between document formats (requires `pandoc` or `libreoffice` on host).
- User wants to check which optional system tools are available.

## When NOT to use
- User wants to view or render a PDF visually — use a PDF viewer.
- User wants to fill in PDF form fields — this skill does not support AcroForms.
- User wants to edit an existing PDF's text in-place — use a dedicated PDF editor.

## Commands

### Check available tools
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py doctor
```

### Get PDF metadata and page count
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py info <pdf_path>
```

### Extract text from a PDF
```bash
# All pages
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py extract-text <pdf_path>

# Specific pages (1-indexed, comma-separated or ranges)
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py extract-text <pdf_path> --pages 1,3,5-8
```

### Extract tables from a PDF
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py extract-tables <pdf_path>
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py extract-tables <pdf_path> --pages 2-4
```

### Extract images from a PDF
```bash
# Saves images to current directory by default
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py extract-images <pdf_path>
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py extract-images <pdf_path> --output-dir /path/to/output
```

### Merge PDFs
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py merge <pdf1> <pdf2> [<pdf3> ...] --output merged.pdf
```

### Split a PDF
```bash
# Split into individual pages
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py split <pdf_path> --output-dir /path/to/output

# Extract a page range into a new PDF
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py split <pdf_path> --pages 2-5 --output extracted.pdf
```

### Rotate pages in a PDF
```bash
# Rotate all pages 90 degrees clockwise
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py rotate <pdf_path> --degrees 90 --output rotated.pdf

# Rotate specific pages
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py rotate <pdf_path> --degrees 180 --pages 1,3 --output rotated.pdf
```

### Create a PDF from text
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py create-pdf --text "Hello, world!" --output hello.pdf
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py create-pdf --file input.txt --output document.pdf
```

### Read a DOCX file
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py read-docx <docx_path>
```

### Write a DOCX file
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py write-docx --text "Content here" --output document.docx
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py write-docx --file input.txt --output document.docx
```

### OCR a scanned PDF (requires tesseract)
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py ocr <pdf_path>
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py ocr <pdf_path> --pages 1-3 --lang eng
```

### Convert text or document to speech (requires ffmpeg)
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py tts --text "Hello, world!" --output speech.mp3
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py tts --file input.txt --output speech.mp3
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py tts --file document.pdf --output speech.mp3
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py tts --text "Hello" --voice en-GB-SoniaNeural --output speech.mp3
```

### Convert document formats (requires pandoc or libreoffice)
```bash
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py convert <input_path> --output <output_path>
```

### Examples

```bash
# Inspect a PDF
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py info report.pdf

# Pull text from pages 1–3
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py extract-text report.pdf --pages 1-3

# Merge two PDFs
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py merge a.pdf b.pdf --output combined.pdf

# OCR a scanned document
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py ocr scan.pdf

# Read a Word document
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py read-docx report.docx

# Text to MP3
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py tts --text "Welcome to the future." --output welcome.mp3

# Check what is available on this host
uv run /root/.openclaw/workspace/skills/pdf-toolkit/src/main.py doctor
```

## Chat Delivery
- When this skill is used in a chat interface that supports file attachments, such as Telegram, any generated output file should be sent back to the user as an attachment after successful creation or conversion.
- This applies to commands that create files, including `create-pdf`, `write-docx`, `extract-images`, `merge`, `split`, `rotate`, `tts`, and `convert`.
- If a temporary output file is created in the Claw runtime temporary folder for delivery, delete that temporary file immediately after the file has been sent successfully to the user.
- Do not delete files that were written to a user-requested destination outside the Claw temporary folder.
- If the chat environment cannot send file attachments, report the output path clearly instead of claiming the file was delivered.

## Output
- Plain text with labeled sections separated by blank lines.
- Errors are prefixed with `Error:`.
- The `doctor` command shows a table of available and missing tools.

## Notes
- `uv run` reads the inline `# /// script` dependency block in `main.py` and auto-installs Python packages in an isolated environment — no pip install or venv setup needed.
- **Core features** (info, extract-text, extract-tables, merge, split, rotate, create-pdf, read-docx, write-docx) work with `uv` alone — no system binaries required.
- **OCR** requires `tesseract` installed on the host (`brew install tesseract` / `apt install tesseract-ocr`). Also needs `pdfimages` from poppler (`brew install poppler`).
- **TTS** requires `ffmpeg` installed on the host (`brew install ffmpeg` / `apt install ffmpeg`).
- **Document conversion** requires `pandoc` or `libreoffice` on the host.
- Run `doctor` first if you are unsure which features are available.
