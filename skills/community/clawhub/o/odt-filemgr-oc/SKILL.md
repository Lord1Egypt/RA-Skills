---
name: odt-filemgr-oc
description: Create, parse, and edit ODT (OpenDocument Text) files locally using Python and odfdo. Use when the user asks to create, edit, read, update, append to, inspect, or manipulate any ODT file. Works with the nextcloud-aio-oc skill for NextCloud integration — that skill handles downloading and uploading the binary file; this skill handles all document-level editing.
license: MIT
compatibility: Requires Python 3.10+.
required-binaries:
  - python3>=3.10
---

# ODT File Manager

Local ODT document creation and editing powered by `odfdo`.

**Library**: `odfdo` v3.20+ — actively maintained, single dep (`lxml`), full ODF support.

## Required Setup

```bash
pip install odfdo
```

## Skill Boundaries

This skill is **purely local** — it has no network access and knows nothing about NextCloud.

For NextCloud workflows, pair with `nextcloud-aio-oc`:

| Step | Skill |
|------|-------|
| Find file on NextCloud | `nextcloud-aio-oc` → `node scripts/nextcloud.js files search` |
| Download binary ODT | `nextcloud-aio-oc` → `python3 scripts/files_binary.py download` |
| **Edit / create ODT** | **`odt-filemgr-oc`** → `python3 scripts/odt_tool.py ...` |
| Upload binary ODT | `nextcloud-aio-oc` → `python3 scripts/files_binary.py upload` |

Scripts live at: `~/.openclaw/skills/odt-filemgr-oc/scripts/`

---

## Workflows

### Edit an existing ODT (NextCloud)

```bash
NC=~/.openclaw/skills/nextcloud-aio-oc/scripts
ODT=~/.openclaw/skills/odt-filemgr-oc/scripts

# 1. Download
python3 $NC/files_binary.py download "/Documents/MyDoc.odt" /tmp/MyDoc.odt

# 2. Inspect
python3 $ODT/odt_tool.py inspect /tmp/MyDoc.odt

# 3. Edit
python3 $ODT/odt_tool.py append /tmp/MyDoc.odt --text "New Section" --heading 2
python3 $ODT/odt_tool.py append /tmp/MyDoc.odt --text "Section content here."

# 4. Upload back
python3 $NC/files_binary.py upload /tmp/MyDoc.odt "/Documents/MyDoc.odt"
```

### Create a new ODT and push to NextCloud

```bash
# 1. Create locally
python3 $ODT/odt_tool.py create /tmp/NewDoc.odt --title "Q1 Report"

# 2. Add content
python3 $ODT/odt_tool.py append /tmp/NewDoc.odt --text "Summary" --heading 2
python3 $ODT/odt_tool.py append /tmp/NewDoc.odt --text "Results were positive across all metrics."

# 3. Push to NextCloud
python3 $NC/files_binary.py upload /tmp/NewDoc.odt "/Documents/Q1 Report.odt"
```

### Edit a local ODT (no NextCloud)

```bash
python3 $ODT/odt_tool.py inspect   myfile.odt
python3 $ODT/odt_tool.py to-text   myfile.odt
python3 $ODT/odt_tool.py append    myfile.odt --text "Added paragraph."
python3 $ODT/odt_tool.py replace   myfile.odt --find "draft" --sub "final"
python3 $ODT/odt_tool.py set-meta  myfile.odt --title "Final Report"
```

---

## odt_tool.py Commands

| Command | Description |
|---------|-------------|
| `inspect <file>` | Show metadata + paragraph/heading/table structure |
| `to-text <file>` | Extract all text content in document order |
| `create <file> [--title T]` | Create blank ODT (optional H1 title) |
| `append <file> --text T [--heading N] [--style S]` | Append heading (N=1–6) or paragraph |
| `replace <file> --find F --sub S [--regex]` | Find and replace text |
| `set-meta <file> [--title T] [--subject S] [--description D]` | Update metadata |
| `set-font <file> --font F [--size N] [--no-preserve-mono]` | Set font across all style layers (default + all named/inline overrides) |
| `set-outline <file> --numbered \| --plain` | Toggle heading numbering (1.1.1 or none) |
| `merge-styles <file> --template T` | Apply all styles from a template ODT |

---

## Custom Python Edits

For table edits, style changes, or multi-step operations, write inline Python:

```python
from odfdo import Document, Header, Paragraph

doc = Document("/tmp/file.odt")
body = doc.body

# Read all content in order
for child in body.children:
    if isinstance(child, Header):
        print(f"H{child.level}: {child.inner_text}")
    elif isinstance(child, Paragraph) and child.inner_text.strip():
        print(f"[{child.style}]: {child.inner_text}")

# Add content
body.append(Header(2, "New Section"))
body.append(Paragraph("Content here."))

# Table edit
table = body.get_table_by_name("MyTable")
table.set_value(0, 0, "Updated cell")

doc.save("/tmp/file.odt", pretty=True)
```

For the full odfdo API (tables, lists, spans, styles, metadata), see [REFERENCE.md](REFERENCE.md).

---

## Key Rules

1. **Always inspect before editing** a file you haven't seen.
2. **Temp files**: use `/tmp/` for working files; clean up after upload.
3. **Styles**: for complex style systems (colors, spacing, borders), use `merge-styles` with a template rather than generating styles from scratch. `set-font` and `set-outline` work safely on any document without a template.

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: odfdo` | `pip install odfdo` |
| `zipfile.BadZipFile` | File corrupted or not a real ODT — re-download |
| Heading doesn't appear as H1 | Use `Header(1, "text")`, not `Paragraph("text", style="Heading 1")` |
| Font still shows as Liberation in Collabora | ODT has 6 font attributes per style rule. Old approach only set 3 (`style:font-name-*`). Collabora renders from `fo:font-family` — now all 6 are set. Re-run `set-font`. |
| Font name must match exactly | LibreOffice/Collabora font names are case-sensitive: `"Noto Sans"` not `"noto sans"` |
| `set-outline` changes not visible | Some documents override numbering via paragraph styles — use `merge-styles` with a clean template instead |
