---
name: markdown-to-word
description: Convert a Markdown file or raw Markdown string into a polished Word DOCX document. Supports custom Word template files, includes built-in DOCX templates, and is the right skill when the user asks to export Markdown to Word, generate a .docx report from Markdown, or restyle Markdown content with a reference DOCX.
---

# Markdown To Word

Use this skill when the user wants a Markdown file or Markdown string converted into a Word `.docx` document.

## What this skill provides

- Deterministic conversion through `pandoc`
- Input from either a Markdown file or a raw Markdown string
- Custom template support through `--template /path/to/reference.docx`
- Built-in template pack in `assets/templates/`
- Optional table of contents, numbered sections, metadata, and resource-path support

## Quick workflow

1. Choose the input source.
   File input: pass `--input-file /abs/path/file.md`
   Raw string input: pass `--markdown '...'`
2. Choose the template.
   Custom template wins when the user provides one.
   Otherwise use a built-in template with `--builtin-template`.
3. Set output path with `--output /abs/path/result.docx`.
4. For long reports, prefer `--toc` and `--number-sections`.

## Built-in templates

- `modern-blue`: clean report style, safe default
- `executive-serif`: formal memo / proposal style
- `warm-notebook`: softer editorial style
- `minimal-gray`: restrained documentation style

List them at runtime with:

```bash
python3 scripts/markdown_to_docx.py --list-templates
```

## Main command

```bash
python3 scripts/markdown_to_docx.py \
  --input-file /abs/path/source.md \
  --output /abs/path/output.docx \
  --builtin-template modern-blue \
  --toc \
  --number-sections
```

## Raw string example

```bash
python3 scripts/markdown_to_docx.py \
  --markdown '# Weekly Report\n\n- Finished template system\n- Integrated pandoc' \
  --output /abs/path/weekly-report.docx \
  --builtin-template executive-serif \
  --title 'Weekly Report'
```

## Template rules

- Prefer `--template` when the user already has a branded `.docx` reference file.
- Use `--builtin-template` when no custom template is provided.
- If both are passed, the script uses the custom template.

## Metadata and assets

- Pass `--title`, `--author`, `--date`, or `--metadata-file`
- Use `--resource-path` when Markdown references local images outside the Markdown file directory
- Example templates and a sample Markdown file live under `assets/`

## Bundled files

- Converter: `scripts/markdown_to_docx.py`
- Built-in template generator: `scripts/build_builtin_templates.py`
- Built-in templates: `assets/templates/*.docx`

## Notes

- This skill expects `pandoc` to be installed and available on `PATH`
- Generated DOCX styling depends on the selected reference DOCX, so for brand fidelity a custom reference file is still the best option
