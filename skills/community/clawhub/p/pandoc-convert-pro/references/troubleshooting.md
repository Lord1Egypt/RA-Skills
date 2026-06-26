# Pandoc Troubleshooting

## `pandoc is not installed`

Use the optional installer helper. It is dry-run by default and only prints the recommended command:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/install_pandoc.sh
```

After the user explicitly approves installation, run:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/install_pandoc.sh --yes
```

The helper detects an existing Pandoc installation and exits without reinstalling. It can recommend Homebrew, Conda, `apt-get`, `dnf`, or `pacman` when those package managers are available. If no supported package manager is detected, use Pandoc's official installer or tarball from https://pandoc.org/installing.html.

Manual macOS install example:

```bash
brew install pandoc
pandoc --version
```

PDF output may still need a separate PDF engine; installing Pandoc alone is not always enough for PDF conversion.

## PDF engine not found

Pandoc needs an external PDF engine for PDF output. Install one or choose another engine:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/convert.sh input.md -o output.pdf --pdf-engine xelatex
```

For macOS, BasicTeX or TinyTeX is usually lighter than full MacTeX. For Linux, TeX Live is the common choice.

## Chinese or Unicode text breaks in PDF

Use `xelatex`:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/convert.sh input.md -o output.pdf --pdf-engine xelatex
```

If fonts are missing, install appropriate CJK fonts and configure the document metadata or template.

## Images are missing

Check that image paths are relative to the working directory or pass resource paths:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/convert.sh input.md -o output.html --resource-path .:assets:images
```

For DOCX to Markdown, use `--extract-media media`.

## Citations do not render

Check all of these:

- `--citeproc` is present.
- The bibliography file exists.
- The CSL file exists when specified.
- Citation keys in Markdown match keys in the bibliography.

Example:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/convert.sh thesis.md -o thesis.pdf --citeproc --bibliography refs.bib --csl ieee.csl
```

## DOCX styling does not match expectations

Use a reference document:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/convert.sh report.md -o report.docx --reference-doc reference.docx
```

The content of `reference.docx` is ignored; its styles, margins, headers, footers, and document properties are used.

## Batch conversion partially fails

This is expected in tolerant batch mode. Read the summary and report:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/batch_convert.py docs --output-dir out --to html --retries 2 --report out/report.md --json-report out/report.json
```

Then retry only the failed files after fixing the reported errors. Use `--fail-fast` when partial results are not useful.
