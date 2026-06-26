---
name: pdf2word-skills
description: Convert scanned PDF documents into Word text documents using a free, local OCR engine or remote api.
---

# PDF to Word Converter

[🇨🇳 简体中文 / Simplified Chinese](README_zh.md)

A skill to extract text from scanned PDF documents and convert them into reusable Word (`.docx`) files using the free, local `docr` OCR engine.

## Prerequisites

1. Initialize the OCR engine by downloading the binaries:
   ```bash
   bash scripts/install.sh
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r scripts/requirements.txt
   ```

## Usage

Run the Python script passing the input PDF file and the desired output `.docx` file path. You can also append any additional standard `docr` arguments (such as engine preferences).

```bash
python scripts/pdf2word.py <input.pdf> <output.docx> [docr_args...]
```

### Examples

Convert a single file with the default local engine:
```bash
python scripts/pdf2word.py sample.pdf sample_output.docx
```

### Using Other API Engines

By default, the script uses the local `RapidOCR` engine. The underlying `docr` tool also supports other engines like the Google Gemini API for potentially higher recognition accuracy on complex layouts.

To use Gemini, first configure your API key:
```bash
mkdir -p ~/.ocr
echo "gemini_api_key=your_gemini_key" > ~/.ocr/config
```

Then pass the `-engine gemini` argument to the script:
```bash
python scripts/pdf2word.py sample.pdf sample_output.docx -engine gemini
```

If your document has **tables**, you can force Gemini to output them in Markdown format so the script can parse them into native Word tables:
```bash
python scripts/pdf2word.py sample.pdf sample_output.docx -engine gemini -prompt "Extract all text and preserve tables in Markdown format using | symbols."
```

### How it Works
1. The script calls `docr`, which uses the specified OCR model (RapidOCR by default) to read text from the scanned PDF.
2. The extracted text is temporarily stored.
3. The `python-docx` library is used to read the temporary text and construct a formatted Word document.
4. Temporary files are cleaned up automatically.
