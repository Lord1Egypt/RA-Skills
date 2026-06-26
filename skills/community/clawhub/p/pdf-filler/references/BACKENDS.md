# Backend fallback chain

The orchestrator tries backends in this order. Each is skipped if its dependency isn't installed. The first backend that fills every requested field "wins" and its output becomes the final PDF.

| # | Backend  | Dependency                                  | Strengths                                                                 | Caveats                                                  |
|---|----------|---------------------------------------------|---------------------------------------------------------------------------|----------------------------------------------------------|
| 1 | pypdf    | `pip install pypdf` (required)              | Pure Python, broadest install base, handles most AcroForms                | Needs `/NeedAppearances` for some viewers to redraw text |
| 2 | pdfrw    | `pip install pdfrw` (extra `[pdfrw]`)       | Fine-grained control over annotation dicts, useful for unusual layouts   | Older project, not all PDF features supported            |
| 3 | PyMuPDF  | `pip install PyMuPDF` (extra `[pymupdf]`)   | Robust appearance regeneration, native checkbox/radio handling, flatten   | Larger native dependency (MuPDF)                          |
| 4 | pdftk    | System binary `pdftk` on PATH               | Last-resort, handles many quirky PDFs via FDF; supports `--flatten`       | Not bundled, install via package manager                 |

## Forcing a specific backend

```bash
python scripts/fill.py form.pdf values.json -o out.pdf --backend pymupdf
```

Use this when:

- The auto-winner produces a PDF that displays blank in a particular viewer (try `pymupdf` or `pdftk` -- they regenerate appearances reliably).
- You want consistent output across runs regardless of which optional dependencies are installed.

## Best-effort chaining

```bash
python scripts/fill.py form.pdf values.json -o out.pdf --best-effort
```

Each backend processes only the fields the previous backends couldn't handle, and the partial PDF is fed forward. Useful when one backend handles text but stumbles on checkboxes (or vice versa).

## Listing what's available locally

```bash
python scripts/list_backends.py
```

Prints a JSON object showing which backends are installed and the order they'd be tried.

## Installing pdftk

- macOS: `brew install pdftk-java`
- Debian/Ubuntu: `apt install pdftk-java`
- Windows: download a pdftk port and ensure `pdftk.exe` is on PATH

## When all backends fail

1. Run `extract.py --include-values` on the input -- confirm the field names you're filling actually exist (case + spaces matter).
2. Try `--backend pymupdf` and inspect the output PDF in a different viewer; some viewers cache form appearances aggressively.
3. Check whether the PDF is encrypted (`pypdf` will surface this error). Decrypt with the document password and retry.
4. As a final fallback, install `pdftk-java` and retry; pdftk handles many edge cases the Python libraries miss.
