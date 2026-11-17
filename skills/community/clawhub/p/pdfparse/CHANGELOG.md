# Changelog

## 2.0.0 — 2026-10-30

First public release.

**Parsing**
- Double-column reading order (full left column, then full right column)
- Full-width figure regions respected; split figure captions rejoined
- Header/footer/page-number stripping, drop-cap filtering
- Sentence repair across page breaks (de-hyphenation, mid-sentence cuts)
- Optional page markers (`--page-markers`) for page-accurate citation
- Reference pruning, or `--keep-references` to keep the bibliography
- Figure extraction with numbers matched to the paper's own `Fig. N` captions, plus a
  caption/extraction crosscheck

**Tooling**
- `scripts/run.sh` — resolves a Python 3.10+ interpreter that has PyMuPDF
- `--json` machine-readable summary for single files and batches
- Batch wrapper: `--keep-names`, `--skip-existing`, tolerant of per-file failures
- Version stamp in every output (`<!-- pdfparse vX.Y.Z -->`)

**Tests**
- `scripts/self_test.py`: 11 checks covering the version stamp, naming, empty/scanned
  detection, `--skip-existing`, missing files, `--keep-references`, `--page-markers`
  and `--json`
