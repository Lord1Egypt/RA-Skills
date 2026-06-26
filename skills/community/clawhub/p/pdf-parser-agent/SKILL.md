# SKILL.md - pdf-parser-agent

## Purpose
Parses local PDF files into structured Markdown and JSON formats using the `opendataloader-pdf` library, providing deterministic, local data extraction that bypasses LLM context limits for document content ingestion.

## Core Technology Attribution
This skill is built upon `opendataloader-pdf`, originally developed by **bundolee** and **claude**.

## Dependencies
This skill requires Python packages installed system-wide or user-site-wide:
1. `opendataloader-pdf`

## Usage Example
The skill's execution script dynamically finds the correct user-site packages path, assuming the user has installed the dependency via `pip install --user opendataloader-pdf`.

```bash
# Assuming a PDF exists at 'Files for testing/sample-local-pdf.pdf'
openclaw skill pdf-parser-agent --run --args "Files for testing/sample-local-pdf.pdf"
```

## Implementation Notes
The underlying logic now uses `site.getusersitepackages()` to dynamically locate the installed package, maximizing portability across different OS/Python minor versions.
