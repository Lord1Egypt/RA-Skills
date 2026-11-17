---
name: pdfparse
description: >-
  High-quality PDF → clean Markdown conversion for text-layer (digital) academic PDFs —
  journal articles, book chapters, guidelines, reports. Handles single files AND large
  batches. Use this skill whenever the user wants PDFs turned into markdown/fulltext for
  reading, quoting, summarising or analysis: "şu PDF'leri markdown'a çevir / parse et",
  "PDF'den metin çıkar / fulltext çıkar", "makaleleri md yap", "bu 70 PDF'i işle",
  "PDF to markdown", "convert this PDF", "extract full text from these papers",
  "parse these PDFs into readable text files". Also reach for it when a batch of
  downloaded reference PDFs (e.g. from pdf-downloader) needs to become readable,
  searchable text for a literature review or book chapter. Handles double-column journal
  layouts with correct reading order (full left column then right, full-width figures
  respected), rejoins Springer-style split figure captions, names outputs by paper title
  (`--keep-names` keeps PDF filenames instead, for numbered reference collections), and
  extracts figures numbered to match the paper's own Figure N. It is the
  parser of choice for text-layer PDFs; do NOT route scanned/image-only PDFs here — that
  is image-ocr's job — and do not confuse it with pdf-downloader (fetching PDFs),
  paper-vault (carding papers) or opencite (search/metadata): those skills fetch or file
  papers, pdfparse converts local PDF files into clean markdown.
---

# PDF Parse — Academic PDF → Clean Markdown

Turns text-layer PDFs into clean, readable, sentence-flowing Markdown — the format you
want before summarising, quoting, or synthesising sources. Validated on a 72-paper
double-column journal corpus: 72/72 parsed in ~2 minutes with zero failures.

## Why this parser instead of simple extraction

- **Correct double-column reading order** — the FULL left column is emitted first (top to
  bottom), then the FULL right column. This mirrors how a human reads a two-column page and
  keeps paragraphs that start at the bottom of the left column and continue at the top of
  the right column intact. (An earlier row-by-row merge of left/right by y-coordinate broke
  exactly this case — it put the right column's continuation before the left column's
  paragraph start.) Mixed first pages (single-column title/abstract → double-column body)
  are handled too.
- **Full-width figure regions are respected.** When a page has a spanning figure with body
  text above it, the body text above is read first (left → right), then the figure, then
  the text below the figure. A figure in the middle of the page never gets pulled out of
  order. (An earlier pass silently dropped spanning blocks on pages where the figure was at
  the top — that lost the image entirely.)
- **Split figure captions are rejoined.** Springer-style layouts split a `Fig. N` caption
  into two blocks at the same vertical band: the left starts with `Fig. N ...`, the right
  continues the same sentence. The parser merges them into one caption so the right half
  doesn't leak into the body text as if it were a new paragraph. The merge only fires when
  there is real sentence continuity — the left part ends with a connector (`,`, `;`, `:-`,
  or a dangling `and`/`of`/`the`/`with`...) or the right part opens with `(`. Section
  headings and body paragraphs that merely sit at the same height (e.g. `Proteome
  Analysis Identifies Pathways...` or `lack of hemodynamic...`) are correctly rejected.
- **Header/footer/page-number removal** via position + fingerprinting — checks a block's
  bottom edge against the footer zone and fingerprints even very short footers (e.g.
  Springer's `1 3` volume/issue page marks), so they don't leak into the text.
- **Drop-cap and decorative-element filtering**.
- **Sentence reconstruction across page breaks** — de-hyphenation, mid-sentence cuts.
- **Reference-section pruning** (`References`, `Bibliography`, and Turkish
  `Kaynakça` / `Kaynaklar`). Pass `--keep-references` when the bibliography itself is
  the point (citation extraction, reference tracing); the metadata block then reports
  `REFERENCES: kept` instead of `REFERENCES: stripped`.
- **Optional page markers** (`--page-markers`) — a `<!-- page N -->` line between pages, so
  the output can be quoted with a page number ("p. 12") and parse order can be debugged
  page by page. Off by default. A marker is omitted at a boundary that was healed across
  pages, because inserting it there would split the rejoined word.
- **Paragraph reconstruction** from PDF line-breaks.
- **Optional figure extraction** as PNGs with markdown image markers.
- Fast: plain PyMuPDF (`fitz`), no LLM calls. (pymupdf4llm once hung for minutes on a
  73-page FELASA document; this parser finished it in seconds.)

Requirements: Python **3.10+** and PyMuPDF. **Always invoke the scripts through
`scripts/run.sh`** — it picks an interpreter that is new enough and actually has PyMuPDF,
skipping ones that don't. Plain `python3` is often the system interpreter, which usually
lacks PyMuPDF. Override the choice with `PYTHON=/path/to/python3`.

## Single PDF

```bash
"<skill_dir>/scripts/run.sh" "<skill_dir>/scripts/pdf_to_clean_md.py" <input.pdf> <output_dir> [--no-figures] [--slug SLUG] [--figure-dpi 200] [--keep-embedded] [--keep-references] [--page-markers] [--json] [--quiet]
```

- Writes `<output_dir>/fulltext.md`; with figures also `<output_dir>/figures/<slug>_fig_N.png`.
- Prints machine-readable metadata to stdout:
  `TITLE:`, `AUTHOR:`, `PAGES:`, `FIGURES:`, `OUTPUT_DIR:`, `REFERENCES:` — use it to confirm
  what was parsed.
- `--no-figures` skips figure extraction (recommended for pure text corpora — the 72-PDF
  chapter run used it).
- `--keep-embedded` also extracts uncaptioned embedded images (journal logos/badges). Off by
  default so figure numbers stay aligned with the paper.
- `--quiet` suppresses the per-file metadata block (FULLTEXT/TITLE/…/figure crosscheck) —
  useful when driving the parser programmatically.
- **Every output's first line is a version stamp** `<!-- pdfparse vX.Y.Z -->`. A `.md` that
  lacks this line (or shows an older version) was produced by a different parser version —
  worth re-parsing.
- **Slug defaults to the paper's real title** (slugified, e.g.
  `age-associated-resilience-against-ischemic-injury`), NOT the PDF filename — resolved from
  PDF metadata title, falling back to the **largest-font text block on page 1** (a title is
  almost always set in a clearly larger font than the body — 26pt vs 10pt in
  Nature-family journals — so even a multi-line title whose first line is short is captured
  in full), then to the filename. Override with `--slug` when you want a custom name (figure
  names follow the slug). Because the slug is title-derived, renaming the PDF afterwards
  never changes the output or figure names, and the same paper parsed from different
  filenames yields identical names.
- **Image markers stay on their own line.** Whitespace normalisation (paragraph joining,
  punctuation cleanup) never glues a `![fig_N](...)` marker into a neighbouring paragraph —
  markers are protected and restored as standalone lines. This keeps a figure marker right
  before (or after) the caption it belongs to, consistently.
- **Figure numbers match the paper.** Each extracted figure is labelled by the real number
  from its `Fig. N` caption (not a running counter), and uncaptioned images (logos/badges)
  are skipped. Images and captions are paired across the whole document, so a figure whose
  image sits at the bottom of one page and whose caption is at the top of the next still
  matches. Split captions are merged (see above) so the caption text stays whole. `fig_3.png`
  is genuinely the article's Figure 3.
- **Crosscheck output** (stdout): `FIG_CAPTIONS:` (numbers seen in captions), `FIG_EXTRACTED:`
  (numbers actually saved), `FIG_MISSING:` (captioned but no image → investigate), and
  `EMBEDDED_SKIPPED:` (logos/badges skipped). Aim for `FIG_MISSING: none` and
  `FIG_CAPTIONS == FIG_EXTRACTED`. A non-empty `FIG_MISSING` usually means a caption-only
  figure (e.g. a vector graphic drawn as text) — inspect and, if needed, fall back to the
  original PDF.
- **Verification tip:** after a parse, spot-check that every `Fig. N` caption in the
  markdown reads as one continuous paragraph (no body text wedged between its two halves),
  and that the `![fig_N]` marker appears right before its caption.

## Batch of PDFs

```bash
"<skill_dir>/scripts/run.sh" "<skill_dir>/scripts/parse_many.py" -o <output_root> \
    [--no-figures] [--keep-names] [--skip-existing] [--figure-dpi 200] [--quiet] \
    [--keep-references] [--page-markers] [--json] \
    <pdf1> <pdf2> ... <pdfN>
```

- One flat markdown file per PDF: `<output_root>/<title-slug>.md` (no nested folders).
- Figures (unless `--no-figures`) are pooled in `<output_root>/figures/`; filenames embed
  the title slug, so nothing collides and the markdown image links resolve correctly.
- **`--keep-names`** names each output after its **PDF filename** instead of the title slug
  (`03_Eskandarani_2023_Ammonia_IVC.pdf` → `03_Eskandarani_2023_Ammonia_IVC.md`). Use it when
  the input filenames are a deliberate numbering scheme that must stay aligned with an
  external reference list — e.g. a numbered bibliography where PDF #N ↔ reference #N, so
  `parsed_md/03_...md` is unambiguously reference 3. Trade-off: renaming a PDF later changes
  its output name, and duplicate filenames collide. Without the flag (default), names are
  title-derived and stable against renames.
- **`--skip-existing`** skips a PDF whose output `.md` already exists (and is a real parse,
  not a near-empty stub), so re-running a large batch only processes missing/new files. It is
  a size check, NOT a version check — after a parser upgrade, re-parse without this flag (or
  delete the outputs first).
- **`--quiet`** suppresses the per-file metadata block, leaving one `OK:`/`SKIP:`/`EMPTY:`/
  `FAIL:` status line per file plus the final `DONE:` summary — the cleanest choice for 50+
  PDF runs.
- **Scanned/empty detection:** a PDF with no text layer (a scan without OCR) yields no real
  text and is reported `EMPTY:` and treated as a failure (exit ≠ 0) — never silently `OK:`.
  If you see `EMPTY:`, hand that PDF to the `image-ocr` skill instead.
- Error-tolerant: a failing PDF is reported and skipped, the batch continues. Exit code 0
  only if ALL files succeeded.
- Runs a file per ~1–2 s; for 50+ PDFs run as a background task and check the final
  `DONE: N ok, S skipped, E empty, F failed` line. Do NOT use `pkill`/`kill` patterns that could match the
  script's own command line when stopping such a task.
- Identical filenames in different folders would overwrite each other — rename first if that
  is a risk (this applies regardless of `--keep-names`).

## Machine-readable output

`--json` replaces the human-readable metadata block with a single JSON object on stdout. Use
it whenever a program (paper-vault, a script, another agent) consumes the result:

```json
{
  "status": "ok", "version": "2.0.0",
  "pdf": "/abs/paper.pdf", "slug": "renal-ischemia-in-rats",
  "title": "...", "authors": "...",
  "pages": 12, "figures": 3,
  "output_dir": "/abs/out", "output_path": "/abs/out/fulltext.md",
  "references": "stripped", "page_markers": false, "text_chars": 41234,
  "fig_captions": [1, 2], "fig_extracted": [1, 2], "fig_missing": [], "embedded_skipped": 0
}
```

- A missing input file yields `{"status": "error", "error": "PDF not found: ..."}` and exit 1.
- Batch mode prints totals plus a `results` array:
  `{"ok": 5, "skipped": 0, "empty": 1, "failed": 0, "results": [{"status": "ok", "pdf": "...", "output": "..."}]}`
- `--json` suppresses the per-file metadata, so stdout stays parseable; diagnostics keep going
  to stderr.

## Known artifacts (accept, don't chase)

- A drop-cap (large decorative first letter) occasionally swallows the first letter:
  "Housing" → "ousing". Cosmetic; usually obvious in headings.
- A first-page watermark combined with metadata text can survive footer filtering (e.g.
  `Vol.:(0123456789)` merged with an abbreviations list). Single occurrence, cosmetic —
  delete by hand if it bothers you.
- On rare pages, a figure whose image and caption are separated by hand because the caption
  is stored as vector art rather than a text block may report `FIG_MISSING`. The crosscheck
  flags it — check the original PDF if it matters.
- Reference sections are pruned by default — if the user needs bibliography text verbatim,
  re-run that file with `--keep-references` rather than re-extracting by hand.

## Workflow guidance

1. Confirm scope: single file or batch; whether figures matter (usually not for
   literature/text corpora → `--no-figures`).
2. For batches, sanity-check the first 1–2 outputs before launching the rest.
3. When done, report: number converted, output location, notable artifacts (drop-caps),
   and any FAILs with reasons. Offer to re-run failed files individually for better errors.
4. Scanned/image-only PDFs (no text layer) are auto-detected and reported `EMPTY:` — hand
   those to the image-ocr skill instead of retrying here.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/run.sh` | Interpreter wrapper: runs a script here with a Python that has PyMuPDF. Call every script through this. |
| `scripts/pdf_to_clean_md.py` | Core parser: one PDF → `fulltext.md` (+ figures). Class `AcademicPDFCleaner`. |
| `scripts/parse_many.py` | Batch wrapper: many PDFs → one `.md` each under `-o`, pooled figures, tolerant of failures. `--keep-names` preserves PDF filenames; also `--skip-existing`, `--quiet`, and empty/scanned detection. |
| `scripts/self_test.py` | Self-test: builds synthetic PDFs and checks version stamp, `--keep-names`, empty detection, `--skip-existing`, and missing-file failure. Run `scripts/run.sh scripts/self_test.py`. |

## Related skills (do not confuse)

- `image-ocr` — scanned PDFs / images without a text layer (this skill needs a text layer).
- `pdf-downloader` — fetching PDFs from DOIs/URLs, not converting them.
- `paper-vault` — persistence/card layer; uses `pdf_to_md.py` for quick extractions and may
  point here when clean output matters.
