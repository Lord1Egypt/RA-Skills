# ODT File Manager — Reference

Detailed `odfdo` API patterns for complex local document operations.

> For downloading/uploading ODT files to NextCloud, use `nextcloud-aio-oc` → `python3 scripts/files_binary.py`.

## Opening & Saving

```python
from odfdo import Document

doc = Document("existing.odt")   # open existing
doc = Document("text")           # new blank text document
doc.save("output.odt")
doc.save("output.odt", pretty=True)  # human-readable XML (slightly larger file)
```

---

## Paragraphs & Headings

```python
from odfdo import Document, Header, Paragraph

doc = Document("file.odt")
body = doc.body

# Append plain paragraph
body.append(Paragraph("Hello, world!"))

# Append heading — use Header class (creates text:h element)
body.append(Header(1, "Chapter Title"))   # <-- correct for headings
body.append(Header(2, "Subsection"))

# Append styled paragraph
body.append(Paragraph("Highlighted text", style="Text Body"))

# Read all content in document order (paragraphs + headings)
from odfdo import Header, Paragraph
for child in body.children:
    if isinstance(child, Header):
        print(f"H{child.level}: {child.inner_text}")
    elif isinstance(child, Paragraph):
        text = child.inner_text
        if text and text.strip():
            print(f"P[{child.style}]: {text}")

# Read only paragraphs (text:p) — excludes headings
for para in body.paragraphs:
    print(para.style, "→", para.inner_text)

# Read only headings (text:h)
for h in body.headers:
    print(f"H{h.level}: {h.inner_text}")

# Insert at specific position
body.insert(Paragraph("Inserted text"), position=2)
```

---

## Spans (inline formatting)

```python
from odfdo import Span

# Bold text within a paragraph
para = Paragraph("")
para.append(Span("bold text", style="Bold"))
para.append(" normal text")
body.append(para)
```

---

## Tables

```python
from odfdo import Table, Row, Cell

# Create a new table
table = Table("MyTable")
for r in range(3):
    row = Row()
    for c in range(4):
        cell = Cell(f"R{r}C{c}")
        row.append(cell)
    table.append(row)
body.append(table)

# Read an existing table
table = body.get_table_by_name("MyTable")   # by name
table = body.tables[0]                       # by index

rows, cols = table.nrows, table.ncols

# Get/set cell by (row, col) — zero-indexed
cell = table.get_cell(0, 0)
value = cell.value           # numeric value if set
text  = cell.text_recursive  # text content

table.set_value(1, 2, "New value")  # set by (row, col, value)

# Append a new row
new_row = Row()
new_row.append(Cell("A"))
new_row.append(Cell("B"))
table.append(new_row)
```

---

## Metadata

```python
meta = doc.meta

# Read
print(meta.title)
print(meta.creator)
print(meta.creation_date)    # datetime or None
print(meta.description)
print(meta.subject)
print(meta.language)

# Write
meta.title = "My Document"
meta.subject = "Project Notes"
meta.description = "Weekly status update"
meta.language = "en-US"
```

---

## Finding & Replacing Text

`el.replace(pattern, new)` treats `pattern` as a regex and returns the match count.

### Plain text replacement (all elements)

```python
import re

for el in list(body.paragraphs) + list(body.headers):
    el.replace(re.escape("old text"), "new text")
```

### Regex replacement

```python
for el in list(body.paragraphs) + list(body.headers):
    el.replace(r"\b\d{4}\b", "YEAR")   # replace 4-digit years
```

### Using the built-in odfdo-replace utility (CLI)

```bash
odfdo-replace --input file.odt --pattern "old text" --replacement "new text" --output out.odt
```

---

## Extracting All Text

```python
from odfdo import Header, Paragraph

# Full document text in order (paragraphs + headings)
lines = []
for child in body.children:
    if isinstance(child, (Header, Paragraph)):
        text = child.inner_text or ""
        if text.strip():
            lines.append(text)
full_text = "\n".join(lines)
```

Or use the CLI utility:
```bash
odfdo-show file.odt           # shows all text to stdout
odfdo-markdown file.odt       # converts to Markdown
```

---

## Font & Outline Control

### Set font across the whole document (programmatic)

ODT stores font at four independent layers. Changing only the `default-style` leaves
named paragraph styles (e.g. the `Heading` style sets `Liberation Sans`) and inline
automatic styles unchanged — they win over the default. The correct fix is to walk
**all** `style:text-properties` nodes in both `styles.xml` and `content.xml`.

```python
from odfdo import Document
from odfdo.element import Element

MONO_STYLES = {"Preformatted_20_Text", "Example", "Teletype", "Source_20_Code"}

def set_doc_font(path: str, font: str, size: str | None = None) -> None:
    doc = Document(path)
    pt = (size if size.endswith("pt") else f"{size}pt") if size else None

    # Declare font face
    existing = {s.get_attribute("style:name") for s in doc.get_styles() if s.tag == "style:font-face"}
    if font not in existing:
        face = Element.from_tag("style:font-face")
        face.set_attribute("style:name", font)
        face.set_attribute("svg:font-family", font)
        doc.insert_style(face, automatic=False)

    font_family = f"'{font}'" if " " in font else font  # ODF requires quoted names with spaces

    def apply(tp, name=""):
        if name in MONO_STYLES:
            return
        # Logical name (links to font-face declaration)
        tp.set_attribute("style:font-name", font)
        tp.set_attribute("style:font-name-asian", font)
        tp.set_attribute("style:font-name-complex", font)
        # Actual family used by Collabora/LibreOffice for rendering — must also be set
        tp.set_attribute("fo:font-family", font_family)
        tp.set_attribute("style:font-family-asian", font_family)
        tp.set_attribute("style:font-family-complex", font_family)
        if pt:
            tp.set_attribute("fo:font-size", pt)
            tp.set_attribute("style:font-size-asian", pt)
            tp.set_attribute("style:font-size-complex", pt)

    # Layer 1 & 2: default-style + named styles (styles.xml)
    for s in doc.get_styles():
        for tp in s.get_elements("style:text-properties"):
            apply(tp, s.get_attribute("style:name") or "")

    # Layer 3 & 4: automatic styles on individual elements (content.xml)
    for section in doc.content.get_elements("office:automatic-styles"):
        for s in section.children:
            for tp in s.get_elements("style:text-properties"):
                apply(tp, s.get_attribute("style:name") or "")

    doc.save(path, pretty=True)
```

### Suppress heading numbering

```python
for lvl in doc.styles.xpath("//text:outline-level-style"):
    lvl.set_attribute("style:num-format", "")
    lvl.set_attribute("style:num-suffix", "")
    try:
        lvl.del_attribute("text:display-levels")
    except (KeyError, AttributeError):
        pass
```

### Enable hierarchical heading numbers (1. / 1.1 / 1.1.1)

```python
for lvl in doc.styles.xpath("//text:outline-level-style"):
    level = int(lvl.get_attribute("text:level") or 1)
    lvl.set_attribute("style:num-format", "1")
    lvl.set_attribute("style:num-suffix", ".")
    if level > 1:
        lvl.set_attribute("text:display-levels", str(level))
```

---

## Template Styles

The recommended approach is to reuse styles from a template:

```python
from odfdo import Document

template = Document("template.odt")
target   = Document("new.odt")

# Merge styles from template into target
target.merge_styles_from(template)

# Now styles from template are available in target
body.append(Paragraph("Styled text", style="MyCustomStyle"))
```

Available built-in named styles (always present):
- `Heading 1` through `Heading 6`
- `Text Body`
- `List Paragraph`
- `Bold` (span style)
- `Italic` (span style)

---

## Lists

```python
from odfdo import List, ListItem, Paragraph

lst = List()
for item_text in ["First item", "Second item", "Third item"]:
    item = ListItem()
    item.append(Paragraph(item_text))
    lst.append(item)
body.append(lst)
```

---

## Working with Headers/TOC (inspection)

```python
# Get just the headings (for outline)
headings = [
    (para.style_name, para.text_recursive)
    for para in body.paragraphs
    if para.style_name and para.style_name.startswith("Heading")
]
for style, text in headings:
    print(style, ":", text)
```

---

## Common End-to-End Pattern (with NextCloud)

This skill handles step 2 only. Steps 1 and 3 are handled by `nextcloud-aio-oc`.

```python
#!/usr/bin/env python3
"""Append a new section to an existing ODT and re-upload to NextCloud."""
import subprocess

NC_PATH  = "/Documents/MyReport.odt"
LOCAL    = "/tmp/MyReport.odt"
NC_SKILL = "/home/olorin/.openclaw/skills/nextcloud-aio-oc/scripts"

# 1. Download (nextcloud-aio-oc)
subprocess.run(["python3", f"{NC_SKILL}/files_binary.py", "download", NC_PATH, LOCAL], check=True)

# 2. Edit (odt-filemgr-oc)
from odfdo import Document, Header, Paragraph
doc = Document(LOCAL)
doc.body.append(Header(2, "Weekly Update"))
doc.body.append(Paragraph("All tasks completed on schedule."))
doc.save(LOCAL, pretty=True)

# 3. Upload (nextcloud-aio-oc)
subprocess.run(["python3", f"{NC_SKILL}/files_binary.py", "upload", LOCAL, NC_PATH], check=True)
print("Done.")
```

---

## odfdo CLI Utilities (quick reference)

| Command | Purpose |
|---------|---------|
| `odfdo-show file.odt` | Print all text content to stdout |
| `odfdo-markdown file.odt` | Convert ODT to Markdown |
| `odfdo-headers file.odt` | Show heading outline |
| `odfdo-replace --input f.odt --pattern X --replacement Y --output g.odt` | Find/replace |
| `odfdo-meta-print file.odt` | Print metadata fields |
| `odfdo-meta-update file.odt --json meta.json` | Merge metadata from JSON |
| `odfdo-diff a.odt b.odt` | Text diff between two ODT files |
| `odfdo-styles file.odt` | List styles in document |
