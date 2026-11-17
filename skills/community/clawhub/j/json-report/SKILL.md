---
name: json-report
description: "Convert JSON data into clean Markdown tables and reports. Use for pasted JSON, API or log output, or any batch of JSON records."
version: 1.0.0
slug: json-report
homepage: https://clawhub.ai/example/json-report
changelog: Initial release of the JSON-to-Markdown report skill.
user-invocable: true
metadata: {"clawdbot":{"emoji":"📊","os":["linux","darwin","win32"]},"openclaw":{"requires":{"anyBins":["python3","python"]}}}
---

## When to Use

Use when the main artifact is a readable Markdown report derived from JSON data, for example:

- The user pastes JSON and asks for a table, summary, or readable report.
- API responses, logs, or exports need to be turned into documentation.
- A batch of JSON records should become a single `.md` document.

## Core Rules

### 1. Prefer the helper script over hand-built tables

- Run `{baseDir}/scripts/json_to_md.py` with the `exec` tool instead of writing tables by hand.
- The script handles escaping, column detection, and multi-table inputs.
- Fall back to manual conversion only when Python is unavailable or the input needs special handling the script does not cover.

### 2. Preserve data fidelity

- Never round or truncate numbers, dates, or strings when converting.
- Escape `|` characters in cell content so tables do not break.
- Keep field names exactly as they appear in the source JSON.

### 3. Choose the right output shape

- A top-level array of flat objects becomes one Markdown table.
- A top-level object whose values are arrays becomes one table per key.
- A single object becomes a two-column key/value table.

## Usage

```bash
python {baseDir}/scripts/json_to_md.py input.json --title "My Report" --out report.md
```

## Common Traps

- Multi-line cell values silently break table rows; the script converts newlines to `<br>`.
- JSON with mixed record shapes can produce sparse tables; confirm the columns before delivery.
- Large inputs may produce very wide tables; prefer key/value layout for deeply nested objects.

## Output Format

Output is Markdown: an optional `# Title` heading followed by one or more GitHub-style tables. Always deliver the result as a `.md` file or markdown text block.
