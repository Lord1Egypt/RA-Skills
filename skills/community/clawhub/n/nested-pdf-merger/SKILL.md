---
name: nested-pdf-merger
description: Use this skill when the task is to merge PDFs from a nested directory tree into a single PDF with hierarchical bookmarks by invoking the external `nestedpdfmerger` CLI. This skill depends on the `nestedpdfmerger` binary being installed and available on PATH.
metadata: {"openclaw":{"requires":{"bins":["nestedpdfmerger"]},"homepage":"https://github.com/Lyutenant/nested-pdf-merger"}}
---

# Nested PDF Merger

This repository wraps the external `nestedpdfmerger` CLI.

Do not implement PDF merging logic in this repository.
Do not modify anything under `reference/`.

## Requirements

This skill requires the `nestedpdfmerger` command to be installed and available on `PATH`.

Expected installation command:

```bash
pip install nestedpdfmerger
```

Expected CLI entrypoint:

```bash
nestedpdfmerger INPUT_DIR -o OUTPUT.pdf [options]
```

Alternative module invocation:

```bash
python -m nestedpdfmerger INPUT_DIR -o OUTPUT.pdf [options]
```

## When to use

Use this skill when the user wants to:

- Merge PDF files from a folder tree into one output PDF.
- Preserve the folder hierarchy as PDF bookmarks.
- Preview merge order with `--dry-run`.
- Exclude directories, change sort order, or disable bookmarks.

## Workflow

1. Confirm the input directory and desired output path.
2. Prefer `--dry-run` first when the user wants to validate merge order.
3. Run the CLI with the smallest set of flags needed.
4. If the command fails because the binary is missing, tell the user to install it with `pip install nestedpdfmerger`.

## Supported flags

- `-o, --output PATH`
- `--sort {natural,alpha,mtime}`
- `--reverse`
- `--exclude NAME [NAME ...]`
- `--exclude-hidden`
- `--no-bookmarks`
- `--dry-run`
- `--strict`
- `--verbose`
- `--quiet`
- `--version`

## Examples

Preview merge order:

```bash
nestedpdfmerger ./reports --dry-run
```

Merge with explicit output:

```bash
nestedpdfmerger ./reports --output merged.pdf
```

Merge while excluding folders:

```bash
nestedpdfmerger ./reports --output merged.pdf --exclude Backup Data
```
