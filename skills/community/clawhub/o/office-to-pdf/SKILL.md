---
name: office-to-pdf
description: "Convert office files to pdf"
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["libreoffice"] },
        "install":
          [
            {
              "id": "apt",
              "kind": "apt",
              "package": "libreoffice",
              "bins": ["libreoffice"],
              "label": "Install via apt",
            },
          ],
      },
  }
---

# convert office files to pdf

Convert one or more LibreOffice-supported documents to PDF with LibreOffice in headless mode.
Use this skill when an OpenClaw workflow needs to normalize office files such as:

- Presentations: `.ppt`, `.pptx`, `.odp`
- Documents: `.doc`, `.docx`, `.odt`, `.rtf`
- Spreadsheets: `.xls`, `.xlsx`, `.ods`

to pdf.

## Command Patterns

Convert one file:

```bash
libreoffice --headless --convert-to pdf --outdir ./out ./input.pptx
```

Convert multiple files:

```bash
libreoffice --headless --convert-to pdf --outdir ./out ./a.docx ./b.pptx ./c.xlsx
```

## Install

```bash
sudo apt install libreoffice
```