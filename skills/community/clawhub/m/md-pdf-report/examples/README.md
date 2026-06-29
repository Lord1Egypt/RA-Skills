# Examples

Real and synthetic Markdown files that demonstrate the skill's output.

| File | Pages | Purpose |
|------|-------|---------|
| `test_report.md` | 1 | Minimal feature test — covers headings, lists, tables, code, callouts, links |
| `Mike_Lynch_FactCheck.md` | 7 | Real-world 7-page fact-check report — 1,951 Chinese characters, 36 source links, 5 callout boxes |

## Regenerate the PDFs

```bash
cd /path/to/md-pdf-report
python3 md2pdf.py examples/test_report.md
python3 md2pdf.py examples/Mike_Lynch_FactCheck.md
```

Both will produce a same-name `.pdf` next to the `.md` file.

## Use as templates

Both files are structured for reuse:

- **`test_report.md`** — minimal scaffold covering every supported Markdown element
- **`Mike_Lynch_FactCheck.md`** — full structure for a "claim verification" report (recommended starting point for fact-checks)

For broader scaffolds, see [`../templates/`](../templates/) (fact-check, research-report, scheme).
