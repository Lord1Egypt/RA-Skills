---
name: pdf-filler
description: Extract and fill PDF AcroForm fields with a multi-backend fallback chain. Reads field schemas (text inputs, checkboxes, radio buttons, dropdowns, multi-line text) from any AcroForm PDF and fills them using user-provided JSON values. Tries pypdf, pdfrw, PyMuPDF, and pdftk in order so it works on PDFs that defeat any single library. Use when the user wants to inspect, populate, batch-fill, or programmatically complete PDF forms, or asks about extracting form field names from a PDF, filling out a PDF, generating a filled PDF, or AcroForm processing.
license: MIT
compatibility: Requires Python 3.10+ on the agent host. Optional system dependency `pdftk` enables a last-resort backend; optional Python packages `pdfrw` and `PyMuPDF` expand the fallback chain.
metadata:
  author: qubit999
  version: "0.1.5"
  homepage: https://github.com/qubit999/oc-pdf-filler
---

# pdf-filler

Operate on PDF AcroForms: list every field with its type and current value, then fill the PDF with values supplied as JSON. The skill calls a small Python package (`oc-pdf-filler`) that wraps a fallback chain of PDF libraries, so a single recalcitrant PDF doesn't block the workflow.

## Workspace rules (read this first)

Many agent hosts run inside a sandbox that only allows reads/writes inside a
specific workspace folder. Files written outside that folder show up as
"Unavailable / Outside allowed folders" and the user can't download them.

The CLI enforces this for you:

- The "workspace" is resolved from the first set environment variable in this list,
  falling back to the current working directory:
  `OC_PDF_FILLER_WORKSPACE`, `OPENCLAW_WORKSPACE`, `CLAWHUB_WORKSPACE`,
  `AGENT_WORKSPACE`, `SKILL_WORKSPACE`, `WORKSPACE`.
- All output paths (schema JSON and filled PDF) are resolved **relative to the workspace**.
- If you pass an absolute `--output` that points outside the workspace, the CLI
  rewrites it to the same basename inside the workspace (and prints a warning to
  stderr).
- You can override the workspace explicitly with `--workspace DIR`.

In practice: pass relative paths (e.g. `-o form_done.pdf`), or omit `--output`
entirely. The default is `<input-stem>_done.pdf` inside the workspace.

## When to use

Trigger this skill when the user:

- Asks to inspect, list, or extract the form fields of a PDF
- Wants to fill out / populate / complete a PDF form programmatically
- Mentions AcroForm, checkbox, radio button, or dropdown handling in a PDF
- Has a batch of PDFs to fill from structured data (JSON)

## Setup (once per workspace)

The skill scripts call the `oc-pdf-filler` Python package. Install it first:

```bash
pip install "oc-pdf-filler[all]"
# or, if working from the source repo: pip install -e ".[all]"
```

The `[all]` extra pulls in `pdfrw` and `PyMuPDF` for the full fallback chain. Install `pdftk` from your package manager for the last-resort backend (optional, but useful for stubborn PDFs).

Verify which backends are active:

```bash
python scripts/list_backends.py
```

## Step 1: Extract the field schema

Always extract first so you know the exact field names and types before constructing the JSON values file. Use a workspace-relative path for the output (the CLI confines it to the workspace automatically).

```bash
python scripts/extract.py /path/to/form.pdf --output schema.json --include-values
```

Each entry in the resulting JSON has:

- `name`: the AcroForm field name (use this verbatim as the key when filling)
- `type`: one of `text`, `checkbox`, `radio`, `choice`, `signature`, `pushbutton`, `unknown`
- `options`: for radios and checkboxes, the accepted export values; for choices, the dropdown options
- `value`: current value if the form is partially filled (only when `--include-values` is set)
- `max_length`, `multiline`, `required`, `read_only`: hints for validation

See `references/FIELD_TYPES.md` for the value contract per field type.

## Step 2: Build a values JSON file

The fill input is a flat JSON object `{ "FieldName": value }`. Example:

```json
{
  "Name Verantwortlicher": "ACME GmbH",
  "Postleitzahl Verantwortlicher": "10115",
  "Beschäftigte": true,
  "Verarbeitungstyp": "Automatisiert"
}
```

A starter template is included at `assets/values.example.json`.

### Critical: include every checkbox and radio explicitly

LLMs tend to omit fields they're unsure about, which silently leaves checkboxes unchecked in the output PDF. Don't do that. For every field in the schema:

- **Checkbox** (`type: checkbox`): set `true` or `false`. If the user didn't mention it, default to `false` rather than omitting the key.
- **Radio** (`type: radio`): set the exact export string from `options`. If the user didn't pick one, leave it out only if it's truly optional; otherwise ask the user or pick the most plausible value.
- **Text / choice / signature**: omit only if the field is genuinely blank.

If you are unsure for a checkbox, choose `false`, not omission. The CLI's `unset_checkboxes` and `unset_radios` summary fields tell you which fields were left out so you can self-correct on the next pass. As safety nets you can pass:

- `--default-unset-checkboxes off` to force every untouched checkbox to false in one go.
- `--default-unset-radios first` to pick the first available option for every untouched radio group.

## Step 3: Fill the PDF

Omit `--output` to get the recommended default `<input-stem>_done.pdf` inside the workspace, or pass a workspace-relative filename. Absolute paths outside the workspace are automatically rewritten into it (the host's sandbox would reject them otherwise).

```bash
# preferred: keep the original name with _done suffix, in the workspace
python scripts/fill.py /path/to/form.pdf values.json
# or pass an explicit relative path
python scripts/fill.py /path/to/form.pdf values.json --output form_done.pdf
```

By default the orchestrator uses `--backend auto`, walking the chain `pypdf -> pdfrw -> PyMuPDF -> pdftk` and stopping at the first backend that fills every field.

Useful flags:

- `--backend pymupdf` -- force a specific backend (e.g. when the auto winner produces a PDF that doesn't render correctly in your viewer)
- `--best-effort` -- chain backends so partial fills accumulate (use when no single backend handles every field)
- `--flatten` -- bake values into the PDF so they can't be edited (best support: PyMuPDF, pdftk)
- `--strict` -- exit non-zero if any requested field is missing or unfillable

The script prints a JSON summary including `winning_backend`, `workspace`, `output_path` (absolute path of the resulting PDF, always inside the workspace), `filled`, `missing`, `failed`, `unset_checkboxes`, `unset_radios`, and per-attempt details. If filling fails, see `references/BACKENDS.md` for backend-specific troubleshooting tips.

## Delivering the result to the user

**Send the file back automatically as soon as the fill succeeds. Do not wait for the user to ask.** Users on chat platforms (Telegram, Slack, Discord, Teams, the ClawHub web client, etc.) expect the finished PDF to arrive in the conversation as an attachment immediately after you announce success.

Procedure:

1. Read `output_path` from the fill summary. It is guaranteed to be inside the workspace, so the host can attach it.
2. Use whatever attachment / file-return mechanism the host provides — Telegram bot `sendDocument`, Slack `files.upload`, the agent runtime's own `attach_file` / `send_file` tool, or simply emit it as a workspace artifact. Do not ask the user "do you want me to send it?"; just send it.
3. In the same turn, briefly confirm what was sent (filename + filled-field count). The user shouldn't have to ask twice.
4. If you genuinely cannot find an attachment channel, surface the workspace-relative path so the user can fetch it manually — but treat that as a last resort.

Never write the PDF outside the workspace (e.g. `/tmp`, `/var`, your home directory). Sandboxed hosts will mark it as "Unavailable / Outside allowed folders".

## End-to-end example

```bash
python scripts/extract.py form.pdf -o schema.json
# ... agent inspects schema.json, builds values.json based on user input ...
python scripts/fill.py form.pdf values.json
# writes <workspace>/form_done.pdf
```

After filling, re-run `extract.py --include-values form_done.pdf` and confirm the values stuck before delivering the PDF to the user.

## Notes and edge cases

- Field names may contain spaces, German umlauts, or punctuation. Always copy them verbatim from `extract.py` output.
- For radio groups, set the value to the export name of the chosen option (one of the strings in `options`), not a boolean.
- Signature fields (`type: signature`) are reported but not auto-filled.
- Encrypted PDFs are out of scope; the tool will surface the underlying library error.
- Some PDF viewers cache appearance streams; if a viewer shows blank fields after filling, try opening with a different viewer or use `--flatten`.
