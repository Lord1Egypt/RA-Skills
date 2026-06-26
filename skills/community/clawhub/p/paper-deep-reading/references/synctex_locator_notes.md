# SyncTeX Locator Notes

This bundle does not require SyncTeX for every run, but the reader and artifact contract are designed to use it whenever available.

## Recommended workflow

1. Compile the paper with SyncTeX enabled, for example:
   - `latexmk -pdf -synctex=1 main.tex`
2. Keep:
   - the compiled PDF
   - the generated `.synctex.gz`
3. Preserve `source_path`, `line_start`, and `line_end` in `latex_paragraphs.json`
4. During bundle enrichment, convert line anchors to PDF page / bbox coordinates
5. Store the result under each evidence item, for example:

```json
"synctex": {
  "pdf": "paper.pdf",
  "page": 3,
  "bbox": [70, 120, 480, 170]
}
```

## Localization priority

1. explicit SyncTeX page + bbox
2. explicit PDF page + bbox already stored in manifest
3. source path + line span
4. text-search fallback
