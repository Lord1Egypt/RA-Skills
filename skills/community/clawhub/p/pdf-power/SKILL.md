---
name: "pdf-power"
description: "PDF toolkit: extract, merge, split, compress, convert, watermark, and protect PDFs."
metadata:
  - pdf
  - document
  - conversion
  - productivity
allowed-tools:
  - read
  - write
  - exec
user-invocable: true
---

# PDF Power 🦁

Complete PDF toolkit. Extract text, merge documents, split pages, compress files, convert formats, add watermarks, and protect with passwords.

## Dependencies

The skill uses Python with `pypdf` + `PyMuPDF` (fitz). Install on first use:

```bash
pip install pypdf PyMuPDF Pillow
```

## Operations

### 📄 Extract Text
Read all text from a PDF. Clean output, preserves paragraph structure.

### 🔗 Merge PDFs
Combine multiple PDFs into one file. Maintains page order.

### ✂️ Split PDF
Split a PDF by page ranges or extract specific pages.

### 📦 Compress PDF
Reduce file size. Offers two levels: light (fast, minimal loss) and heavy (smaller, may reduce quality).

### 🖼️ Convert PDF to Images
Convert each page to PNG/JPEG image. Useful for previews or presentations.

### 🖼️ Extract Images
Extract embedded images from PDF pages. Saves to output folder.

### 💧 Watermark
Add text or image watermark to every page. Configurable opacity and position.

### 🔒 Protect / Unprotect
Add or remove password protection on PDF files.

## Usage Pattern

1. Identify the PDF path and desired operation.
2. Run the appropriate Python script.
3. Output file is saved beside the input file (or in specified output path).
4. Confirm result with the user.

## Output

- Text extraction → clean text content
- Merge/Split/Compress/Protect → PDF file
- Convert to images → folder of image files
- Extract images → folder of image files
- Watermark → watermarked PDF

## Critical Rules

- Never overwrite the original file unless user explicitly asks. Append `_output` to output filename.
- For large PDFs (>100 pages), warn the user and ask before proceeding.
- Validate PDF is not corrupted before processing.
- For password-protected PDFs, ask for the password upfront.
- Use `pypdf` for simple operations (merge, split, compress). Use `PyMuPDF` for rendering and image extraction.
- Compress only when user asks — don't compress silently.

---
⭐ *Gostou desta skill?* Deixe uma estrela no [ClawHub](https://clawhub.ai) para ajudar outros a encontrá-la!
