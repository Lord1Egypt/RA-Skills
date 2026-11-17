# pdfparse

**Fast, deterministic academic PDF → clean Markdown.** No LLMs, no models, no cloud calls.

`pdfparse` converts text-layer journal PDFs into sentence-flowing Markdown that is actually
pleasant to read, quote and summarise: correct double-column reading order, header/footer
stripping, figure extraction with matching caption numbers, page-break healing and optional
page markers for citations.

It runs in seconds per file on a laptop CPU, and the same PDF always produces the same output.

## Why another PDF converter?

Most PDF tooling falls into two camps: heavy ML pipelines that download models and need a GPU,
or one-line `pdftotext` calls that scramble two-column journal layouts. This sits in between:

- **No models, no network** — plain PyMuPDF, ~1–2 s per file
- **Built for academic layouts** — two-column reading order, Springer-style split captions,
  full-width figures, drop caps, footers
- **Verifiable** — every output starts with a `<!-- pdfparse vX.Y.Z -->` stamp, and the run
  reports a figure crosscheck (`FIG_CAPTIONS` vs `FIG_EXTRACTED`, `FIG_MISSING`)
- **Batch-friendly** — parse a whole collection in one command, tolerant of individual failures
- **Machine-readable** — `--json` gives a stable summary instead of human-oriented text

## Requirements

- **Python 3.10+**
- **[PyMuPDF](https://pymupdf.readthedocs.io/)** — note that PyMuPDF is licensed **AGPL-3.0**
- macOS or Linux (the wrapper is bash; on Windows use WSL or Git Bash)

```bash
pip install -r requirements.txt
```

## Install

Copy this folder into your skills directory:

- **Cherry Studio** — `…/CherryStudio/Data/Skills/pdfparse/`
- **Claude Code** — `~/.claude/skills/pdfparse/`

Or install it in Claude Code as a plugin — this repository is also a plugin marketplace:

```
/plugin marketplace add ogzhnbygl/pdfparse
/plugin install pdfparse@ogzhnbygl
```

Always invoke the scripts through the bundled wrapper:

```bash
scripts/run.sh scripts/pdf_to_clean_md.py --help
```

`run.sh` picks a Python that is 3.10+ *and* has PyMuPDF — on many machines plain `python3` is
the system interpreter, which has neither. Override with `PYTHON=/path/to/python3`.

## Updating

An installed skill is a **copy** — new commits in this repository do not reach an existing
installation. There is no background update check.

- **Cherry Studio** — Settings → Skills → Add Skill → GitHub → paste this repository's
  `SKILL.md` URL again. Re-installing overwrites the existing copy.
- **Claude Code** — re-run the install, or if installed as a plugin,
  `claude plugin update pdfparse` (this only works when the version was bumped).
- **claude.ai** — upload the new zip under Settings → Capabilities → Skills.

To see which version you have, check the first line of any output
(`<!-- pdfparse v2.0.0 -->`) or the `"version"` field of `--json`.

## Usage

### Single PDF

```bash
scripts/run.sh scripts/pdf_to_clean_md.py paper.pdf out/ --no-figures
```

Writes `out/fulltext.md`. Without `--no-figures`, figures are rendered to `out/figures/` and
linked from the Markdown, numbered to match the paper's own `Fig. N` captions.

Machine-readable summary:

```bash
scripts/run.sh scripts/pdf_to_clean_md.py paper.pdf out/ --json
```

### Batch

```bash
scripts/run.sh scripts/parse_many.py -o parsed/ --no-figures --keep-names *.pdf
```

One `.md` per PDF, figures pooled in `parsed/figures/`. A failing file is reported and skipped;
the batch continues.

## Options

| Flag | Effect |
| --- | --- |
| `--no-figures` | Skip figure extraction (faster, text only) |
| `--slug SLUG` | Override the title-derived output slug |
| `--figure-dpi N` | Figure render DPI (default 200) |
| `--keep-embedded` | Also extract uncaptioned images (logos/badges) |
| `--keep-references` | Keep the bibliography instead of pruning it |
| `--page-markers` | Emit `<!-- page N -->` lines so output can be cited by page |
| `--json` | One JSON summary on stdout |
| `--quiet` | Suppress per-file metadata |

Batch-only: `-o/--output-dir`, `--keep-names`, `--skip-existing`, plus all of the above.

## Output

```markdown
<!-- pdfparse v2.0.0 -->

<!-- page 1 -->

# Results

Body text, reflowed into paragraphs...
```

Scanned PDFs (no text layer) are reported as `EMPTY:` and treated as failures rather than
silently producing an empty file. Run OCR on those separately.

## Known limitations

- Requires a **text layer**. Image-only scans are detected and rejected, not OCR'd.
- **Tables are kept as text**, not parsed into cells — column alignment can suffer on wide
  tables with merged cells.
- Reference pruning is heuristic. If it cuts too much or too little, use `--keep-references`
  and inspect the tail; markers are transparent to the detection.
- Layout heuristics are tuned on one- and two-column scientific journals (English/Turkish).
  Three-column magazines, posters and preprints with unusual layouts are untested.
- Page markers are omitted at page boundaries that were healed across pages, because inserting
  a marker there would split the rejoined word.

## Tests

```bash
scripts/run.sh scripts/self_test.py
```

Builds synthetic PDFs and checks the version stamp, `--keep-names`, empty/scanned detection,
`--skip-existing`, missing-file handling, `--keep-references`, `--page-markers` and `--json`.

## Releasing (maintainers)

1. Bump `__version__` in `scripts/pdf_to_clean_md.py`
2. Bump the same version in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
   — Claude Code only replaces files when the computed version changes
3. Add a `CHANGELOG.md` entry under the new version
4. Run `scripts/run.sh scripts/self_test.py`
5. Commit, tag `vX.Y.Z`, push; confirm CI is green

The version string is how users and update tooling detect a release — a commit without a
version bump is invisible to them.

## License

This skill's own code is MIT licensed — see [LICENSE](LICENSE).

It depends on **PyMuPDF**, which is licensed **AGPL-3.0**. Installing PyMuPDF yourself and
importing it does not change this project's license, but if you redistribute PyMuPDF with your
application, AGPL terms apply to that distribution.
