---
name: "mochi-document-templates"
description: "Generate notices, certificates and business documents from DOCX, text or HTML templates, validate fields and retain Word run formatting. Use for Document Templates and Batch Output."
metadata: {"openclaw": {"requires": {"anyBins": ["python3", "python"]}, "homepage": "https://mochilab.bz", "version": "1.0.1"}}
---

# Document Templates and Batch Output

## Run a job

Use Python 3.10+ in the current agent workspace. Install scripts/requirements.txt into a dedicated virtual environment when it is nonempty. Credentials are private host configuration, not dependencies. Save the requested action as workspace-local JSON, then run:

```text
python3 "{baseDir}/scripts/run.py" --workspace "CURRENT_AGENT_WORKSPACE" --input "request.json"
```

Read the JSON ok/result receipt; a failed command is not a completed operation. Paths are workspace-relative except an explicitly supplied private connection profile. Agents have separate workspaces and separate state. Never use another agent's workspace just because it has a working account. Data and notifications persist under .mochilab. Do not upload those private state folders with a Skill package.

Use for deterministic user-supplied template filling and batch document output. inspect discovers {{field_name}} placeholders. render accepts one data object or up to 200 rows. Missing fields are reported before writing any documents. Field values are literal text, not expressions; no macros or template code executes. DOCX replacements span split runs and cover ordinary paragraphs, tables, headers and footers. Replacement text adopts the first token run's style while surrounding runs stay intact. Text in drawings, text boxes and embedded objects is outside this version's field scan: use ordinary paragraphs/tables for editable fields.

HTML values are escaped. Source files remain unchanged; outputs use new files and include SHA256. Use unique outputName values for rows. Validate a sample document visually in the user's document application before applying a new template to a large batch, especially if inserted values have very different lengths. This helper fills existing templates; it does not design a new layout or calculate spreadsheet formulas.

[User guide](README.md) · [Simplified Chinese guide](README.zh-CN.md)
