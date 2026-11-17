## v1.1.1 — 2026-10-18

The 1.1.0 release shipped install commands that still pinned `packet-audit@1.0.0`, and the
self-check rule meant to catch that had been reading a version key the frontmatter does not
have, so it passed while the docs named the previous release. Both fixed:

- `references`/`SKILL.md`/`README.md` install lines pin the current version.
- `RC5` reads `metadata.version` (the same place `RC1` reads it), fails loudly when the version
  cannot be read, and names the stale pin and the expected version instead of a generic
  "unpinned" line.

## v1.1.0 — 2026-10-17

PDF reading without a dependency, measured against two reference extractors.

- `scripts/pdftext.py`: standard-library PDF text extraction (objects and `/ObjStm` streams,
  `FlateDecode`/`ASCIIHexDecode`/`ASCII85Decode`, page order from the page tree, `Tj`/`TJ`/`'`/`"`
  with per-font `/ToUnicode` CMaps, and word gaps reconstructed from `/Widths`). Encrypted
  files, scans and malformed files raise a named reason the report prints verbatim.
- PDFs are now read by default instead of only when `pypdf` happened to be installed, so the
  same packet gets the same audit on every machine. `pypdf` remains a fallback.
- Word-level validation against `pdftotext` on real documents: 0.94–1.00 recall, 0.92–1.00
  precision across a two-column research paper, tax forms, contracts and a 53-page book.
  A glyph-positioned page ("TD Canada Trust" written one `Td` per character) went from
  0.24 recall and 0.06 precision to 0.99/0.97.
- 14 new fixtures in `tests/test_pdftext.py` (page-tree order, object streams, ToUnicode,
  glyph-per-`Td` spacing, encrypted, image-only, non-PDF, packet-level PDF checks) and a
  guard that the reader imports only the standard library. 40 tests total.
- A PDF that cannot be read is a cited `PA-R01` warning carrying the exact reason, so an
  encrypted or scanned document can never be mistaken for a clean one.

## v1.0.0 — 2026-10-17

First release.

- Deterministic packet audit: classify every file in a folder, extract the fields that must
  agree, and report missing, expired, and inconsistent documents with file and page citations.
- Three bundled profiles: `rental-us`, `schengen-visa`, `insurance-claim-property`.
- Finding codes `PA-E01`, `PA-X01`, `PA-X02`, `PA-C01`, `PA-C02`, `PA-C03`, `PA-F01`, `PA-R01`,
  `PA-D01`, `PA-U01` with severity-driven verdict and exit codes (0/1/2/3).
- Outputs `packet-report.md`, `packet-report.json` (`packet-audit/report/1`), and
  `packet-manifest.json` with SHA-256 per file.
- Standard-library extraction for `.txt`, `.md`, `.csv`, `.json` and `.docx`; optional `pypdf`
  for PDFs; sidecar `<name>.pdf.txt` support; images reported as unreadable instead of guessed.
- 26 fixture-driven tests (clean packet, seeded mismatches, missing documents, extraction,
  profiles, CLI) and a ten-rule self-check.
- Offline: no network imports, no subprocess, no model calls, writes only to `--out`.
