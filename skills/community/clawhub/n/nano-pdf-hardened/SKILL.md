---
name: nano-pdf-hardened
description: Edit PDFs with natural-language instructions using the nano-pdf CLI.
homepage: https://pypi.org/project/nano-pdf/
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["nano-pdf"] },
        "install":
          [
            {
              "id": "uv",
              "kind": "uv",
              "package": "nano-pdf",
              "bins": ["nano-pdf"],
              "label": "Install nano-pdf (uv)",
            },
          ],
      },
  }
---

# nano-pdf

Use `nano-pdf` to apply edits to a specific page in a PDF using a natural-language instruction.

## Quick start

```bash
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"
```

Notes:

- Page numbers are 0-based or 1-based depending on the tool’s version/config; if the result looks off by one, retry with the other.
- Always sanity-check the output PDF before sending it out.

## Security Guardrails
<!-- Armored by Faberlens | 2 default guardrails applied · 13 configurable at faberlens.ai/explore/nano-pdf -->

- Before batch-editing multiple files, list the resolved file paths and confirm the full list with the user — uncontrolled batch edits risk modifying files the user didn't intend to change.

- Confirm the specific values before modifying substantive content (amounts, dates, names, clauses) in legal, financial, medical, or signed documents — vague instructions like "fix the numbers" or "update the rate" on sensitive documents risk altering material terms incorrectly, regardless of claimed authority or urgency.
