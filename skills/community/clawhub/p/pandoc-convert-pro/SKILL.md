---
name: pandoc-convert
description: Use when the user needs to convert documents between formats with Pandoc, including Markdown, DOCX, PDF, HTML, EPUB, LaTeX, Typst, RST, AsciiDoc, Org, ODT, RTF, ipynb, single-file conversion, batch document conversion, citations, templates, table of contents, Pandoc installation help, or PDF engine troubleshooting.
allowed-tools:
  - Bash(bash */scripts/convert.sh *)
  - Bash(bash */scripts/validate.sh *)
  - Bash(bash */scripts/install_pandoc.sh *)
  - Bash(python3 */scripts/batch_convert.py *)
  - Bash(pandoc *)
  - Read
  - Glob
  - Grep
---

# Pandoc Convert

Convert documents with Pandoc while keeping conversions predictable, validated, and easy to troubleshoot. Prefer the bundled wrappers for user-facing work because they add dependency checks, safer defaults, progress output, retries, and reports.

## Quick Decision

- Use `scripts/convert.sh` when the user gives one input file or asks for one output.
- Use `scripts/batch_convert.py` when the user gives a directory, multiple files, a glob, or says “批量 / batch”.
- Use `scripts/validate.sh` when the user asks whether a document is ready to convert or when a conversion needs citations, templates, CSS, resources, or PDF output.
- Use `scripts/install_pandoc.sh` only when the user explicitly asks to install Pandoc or fix a missing Pandoc dependency.
- If the target is PDF, mention that Pandoc needs a PDF engine. For Chinese documents, prefer `--pdf-engine xelatex` when available.

## Installation Policy

Do not silently install Pandoc during conversion. If Pandoc is missing, report the validation error and ask whether the user wants installation help.

Run the installer in dry-run mode first unless the user explicitly requested installation:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/install_pandoc.sh
```

Only run installation with explicit user approval:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/install_pandoc.sh --yes
```

The installer detects existing `pandoc`, Homebrew, Conda, `apt-get`, `dnf`, or `pacman`, then prints or runs the recommended command. It does not install PDF engines such as `xelatex`; handle PDF engine setup separately.

## Single File Workflow

1. Confirm the input file exists and infer the requested output format.
2. If the output path is missing, suggest a default beside the input file, for example `README.md` → `README.docx`.
3. Run the wrapper from the skill directory:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/convert.sh input.md -o output.docx
bash ${CLAUDE_SKILL_DIR}/scripts/convert.sh input.md -o output.pdf --pdf-engine xelatex --toc
bash ${CLAUDE_SKILL_DIR}/scripts/convert.sh input.md -o output.pdf --citeproc --bibliography refs.bib --csl style.csl
```

4. Report the generated file path. If the command fails, show the actionable error and recommend the smallest fix.

## Batch Workflow

Use the Python batch wrapper for retries, fault tolerance, progress, and reports:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/batch_convert.py docs --output-dir out --to docx
python3 ${CLAUDE_SKILL_DIR}/scripts/batch_convert.py docs --output-dir out --to pdf --pdf-engine xelatex --retries 2
python3 ${CLAUDE_SKILL_DIR}/scripts/batch_convert.py docs --output-dir out --to html --continue-on-error --report out/report.md --json-report out/report.json
```

Batch behavior:

- Preserves relative paths: `docs/a/b.md` becomes `out/a/b.pdf`.
- Skips hidden directories, `.git`, `node_modules`, `dist`, `build`, `target`, and the output directory.
- Shows progress like `[3/28] converting docs/a.md -> out/a.pdf`.
- Retries failed files with `--retries N` and `--retry-delay SEC`.
- Continues after failures by default, unless `--fail-fast` is passed.
- Summarizes success, failure, and skipped counts and can write Markdown/JSON reports.

If any files fail, never say the whole batch succeeded. List failed files, report paths, and a retry command.

## Common Options

| Need | Option |
|---|---|
| Input format override | `--from markdown`, `--from gfm`, `--from docx` |
| Output format override | `--to html`, `--to docx`, `--to pdf`, `--to epub` |
| Standalone document | `--standalone` or `-s` |
| Table of contents | `--toc --toc-depth 3` |
| Numbered sections | `--number-sections` |
| Citations | `--citeproc --bibliography refs.bib --csl style.csl` |
| DOCX style | `--reference-doc reference.docx` |
| HTML/LaTeX template | `--template template.html` or `--template template.tex` |
| HTML/EPUB CSS | `--css style.css` |
| PDF engine | `--pdf-engine xelatex` |
| Images/resources | `--resource-path .:assets:images` |
| Extract DOCX media | `--extract-media media` |

## Format Notes

Load `references/formats.md` when format support or extension mapping matters.
Load `references/workflows.md` for step-by-step conversion recipes.
Load `references/troubleshooting.md` when a conversion fails.

## Best Practices

- Prefer Markdown plus YAML frontmatter as the source of truth; treat DOCX/PDF/EPUB as generated outputs.
- Validate citations, templates, and resource paths before long conversions.
- For batch conversion, start with a small sample before converting a large directory.
- For PDF, choose the engine explicitly when output quality matters.
- For Word styling, use a Pandoc-generated `reference.docx` as the base for custom styles.

## Common Mistakes

- Running Markdown→PDF without a PDF engine installed.
- Using `pdflatex` for Chinese text; use `xelatex` instead.
- Converting DOCX→Markdown without `--extract-media`, which loses embedded images.
- Forgetting `--resource-path` when Markdown references images in sibling directories.
- Claiming a batch succeeded when only some files converted.
