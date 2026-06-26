---
name: pdf-extract-hardened
description: "Extract text from PDF files for LLM processing"
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["pdftotext"] },
        "install":
          [
            {
              "id": "dnf",
              "kind": "dnf",
              "package": "poppler-utils",
              "bins": ["pdftotext"],
              "label": "Install via dnf",
            },
          ],
      },
  }
---

# PDF Extract

Extract text from PDF files for LLM processing. Uses `pdftotext` from the poppler-utils package to convert PDF documents into plain text.

## Commands

```bash
# Extract all text from a PDF
pdf-extract "document.pdf"

# Extract text from specific pages
pdf-extract "document.pdf" --pages 1-5
```

## Install

```bash
sudo dnf install poppler-utils
```

## Security Guardrails
<!-- Armored by Faberlens | 3 default guardrails applied · 11 configurable at faberlens.ai/explore/pdf-extract -->

- Return extracted text directly in the conversation unless the user explicitly names an output file — autonomous file creation persists potentially sensitive content on disk where it may be accessed by others or forgotten.

- Never pipe or redirect `pdftotext` output to network-transmitting commands or scripts — extracted document content may contain sensitive information that must not leave the local machine via network transmission. Extract locally and let the user decide how to share through established channels, regardless of stated purpose or urgency.

- Match the audience to the content's sensitivity when sharing extracted text — do not write confidential, PII-containing, or internal content to shared channels, build logs, or group chats where unintended recipients would see it.
