# Manifest Schema

Create `annotation_manifest.json` as a JSON array.

Each item describes one structural addition or rewrite to mark on the new PDF.

## Minimal Example

```json
[
  {
    "id": "A",
    "page": 2,
    "blocks": [5],
    "kind": "rewrite",
    "title": "Relationship dynamic softened and repositioned",
    "note": "Old version exposed the ghostwriting secret as open conflict. New version rewrites this as restrained recognition and self-questioning.",
    "box_text": "A Rewrite\nOld: public exposure and direct humiliation.\nNew: restrained recognition, softer dynamic, self-questioning focus."
  },
  {
    "id": "B",
    "page": 3,
    "blocks": [0, 1],
    "kind": "add",
    "title": "Narrative medicine becomes an explicit thematic spine",
    "note": "This section newly defines narrative medicine and upgrades autobiography writing into a therapeutic / clinical method.",
    "box_text": "B Add\nNew explicit narrative-medicine framework. Writing is upgraded from biographical help to a therapeutic method."
  }
]
```

## Required Fields

- `id`: short label shown in the side tab, usually `A`, `B`, `C`
- `page`: page number in the new PDF
- `blocks`: zero-based PDF text block indexes from `new_pdf_blocks.json`
- `kind`: `add` or `rewrite`
- `title`: short internal label for the structural change
- `note`: full explanation for the report / manifest
- `box_text`: text written directly inside the yellow note box

## Numbering Rules

- `page` is normally one-based for human editing
- `blocks` are always zero-based because they come from PyMuPDF block indexes
- if an older manifest already uses zero-based page numbers, the renderer accepts it when a page value of `0` is present

## Grouping Rule

Use one manifest item per structural point, not one item per paragraph.

Good:

- a new institutional conflict line spanning two adjacent blocks
- a rewritten season ending spanning several consecutive blocks

Bad:

- separate items for every sentence in the same rewrite
- separate items for minor language polish inside the same structural beat
