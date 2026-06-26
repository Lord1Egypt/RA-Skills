---
name: pdf_simple_tool
description: PDF splitting and PDF-to-Word conversion tools implemented in Node.js.
---

# PDF Simple Tool Skill

This skill provides two main actions for working with PDF files:

1. **split_pdf** – Extract a page range from a PDF into a new PDF.
2. **pdf_to_word** – Convert a PDF into a simple Word (.docx) document.

## Install
cd skills/pdf-simple-tool/node/
执行命令： npm install

## Actions

### split_pdf

When the user asks to split a PDF by page range (for example, "把这个 PDF 的第 3-5 页拆出来" / "split pages 3–5"), call the Node implementation:

- Entry: `skills/pdf-simple-tool/node/index.js`
- Function: `splitPdf(inputPath, outputPath, fromPage, toPage)`

**Inputs**
- `inputPath` (string): The absolute path to the source PDF.
- `outputPath` (string): The absolute path where the new PDF will be written.
- `fromPage` (integer): Start page (1-based).
- `toPage` (integer): End page (1-based, inclusive).

Example behavior:
- If the user says: "帮我把 /Users/xingxing/.openclaw/workspace/test.pdf 的第 1-3 页拆成一个 PDF 文件",
  map this to:
  - `inputPath = "/Users/xingxing/.openclaw/workspace/test.pdf"`
  - `outputPath = "/Users/xingxing/.openclaw/workspace/test_p1-3.pdf"`
  - `fromPage = 1`
  - `toPage = 3`

### pdf_to_word

When the user asks to convert a PDF to Word (for example, "把这个 PDF 转成 Word" / "convert to docx"), call the Node implementation:

- Entry: `skills/pdf-simple-tool/node/index.js`
- Function: `pdfToWord(inputPath, outputPath)`

**Inputs**
- `inputPath` (string): The absolute path to the source PDF.
- `outputPath` (string): The absolute path where the Word file (.docx) will be written.

Example behavior:
- If the user says: "把 /Users/xingxing/.openclaw/workspace/test.pdf 转成 Word",
  map this to:
  - `inputPath = "/Users/xingxing/.openclaw/workspace/test.pdf"`
  - `outputPath = "/Users/xingxing/.openclaw/workspace/test.docx"`

## Notes

- Implementation code lives in `skills/pdf-simple-tool/node/index.js` and uses:
  - `pdf-lib` for PDF manipulation.
  - `pdf-parse` + `docx` for PDF-to-Word conversion.
- You are responsible for wiring these actions into your agent so that natural language
  requests are converted into the appropriate function calls with the correct paths and page ranges.
