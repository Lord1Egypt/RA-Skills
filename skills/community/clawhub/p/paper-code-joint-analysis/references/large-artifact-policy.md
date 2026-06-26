# Large Artifact Policy

This skill must not try to exceed model or API hard limits. There is no reliable way to bypass a model context window or a hard API payload limit.

Chunking is not the default for every file. Prefer file-based single artifacts when the file is modest in size and the active model/API can handle it. Chunking is a fallback for construction, transport, or tool limits, especially Windows command-line length limits, not a replacement for the stable final files.

For example, if a PDF text extract or Markdown report is under about 1 MB and can be read from disk by Codex, keep it as one file and pass the path. Do not paste the whole file into a PowerShell command, `python -c`, JSON argument, or here-string. The safe pattern is "short command + file path", not "long command + embedded content".

## Rules

- Do not put long narrative reports inside `analysis_bundle.json`.
- Keep `analysis_bundle.json` structured and compact.
- Put long narrative content in Markdown files.
- For normal-size reports, write one fixed Markdown file directly.
- For very long reports or tool-call-limited outputs, generate section chunks first, then merge them into the fixed final filename.
- The final reader-facing filenames remain stable, especially `paper_reading_report.md`.
- Use chunking as an intermediate build technique, not as a reason to change page code for one paper.

## Recommended Chunk Layout

```text
analysis_dir/
  _parts/
    paper_reading_report/
      01_problem.md
      02_symbols.md
      03_method.md
      04_experiments.md
      05_code_questions.md
      manifest.json
  paper_reading_report.md
```

`manifest.json` should be:

```json
{
  "title": "paper_reading_report",
  "parts": [
    "01_problem.md",
    "02_symbols.md",
    "03_method.md",
    "04_experiments.md",
    "05_code_questions.md"
  ]
}
```

Merge with:

```bash
python scripts/merge_markdown_parts.py analysis_dir/_parts/paper_reading_report analysis_dir/paper_reading_report.md
```

## When To Use

Use this pattern when:

- a generated report section is too long for one tool call;
- Windows command-line length limits would be hit by an attempted inline script or inline content argument;
- the model response would otherwise truncate;
- the page must show a complete report but the analysis is too large to construct safely in one step.

Do not use this pattern when:

- the artifact is below the model/API practical payload limit and can be read from disk as a file;
- the only issue is that a shell command was written poorly with huge inline text;
- a short command can pass a path to an existing file.

## What This Does Not Solve

Chunking does not let the model reason over more information than its context window at one moment. It only lets Codex build and persist long outputs safely over multiple steps. Use indexes, section summaries, and source references when the input corpus itself is larger than the active context.
