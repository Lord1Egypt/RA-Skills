# macOS Workflow

Use this when running the workflow in Terminal or iTerm on macOS.

## 1. Install dependencies

```bash
python3 -m pip install --upgrade pymupdf python-docx
```

## 2. Create a clean working folder

```bash
mkdir -p ./work ./output
```

## 3. Export the revised draft to PDF if needed

If AI has just edited a DOCX, Markdown, or text draft, first obtain a revised PDF. This skill annotates the revised PDF, not the editable source.

## 4. Extract the source text and PDF block map

```bash
python3 ./scripts/build_outline_diff_outputs.py extract \
  --new-pdf "/Users/you/path/new-outline.pdf" \
  --old-source "/Users/you/path/old-outline.docx" \
  --output-dir "./work"
```

This creates:

- `./work/new_pdf_full_text.txt`
- `./work/new_pdf_blocks.json`
- `./work/old_source_full_text.txt`

The old baseline can be `.docx`, `.pdf`, `.txt`, or `.md`.

## 5. Compare the two versions

Read the extracted files and manually create:

- `./work/compare_report.md`
- `./work/annotation_manifest.json`

Manifest format: [manifest-schema.md](manifest-schema.md)

## 6. Render the deliverables

```bash
python3 ./scripts/build_outline_diff_outputs.py render \
  --new-pdf "/Users/you/path/new-outline.pdf" \
  --old-source "/Users/you/path/old-outline.docx" \
  --manifest-json "./work/annotation_manifest.json" \
  --report-md "./work/compare_report.md" \
  --output-dir "./output"
```

## 7. Auto-follow hook after AI edits

If the agent itself has just revised an outline, script, treatment, beat sheet, season map, or character bio:

- do not wait for a second user reminder
- obtain or export the revised PDF
- reuse the previous version as `--old-source`
- regenerate the annotated comparison PDF and reports

If no baseline or revised PDF exists, report the blocker explicitly.

## 8. Verify the PDF

Open the output PDF and check:

- visible yellow note boxes show Chinese correctly
- only structural changes are marked
- note boxes are outside the source text area

## macOS Notes

- A committed `.py` file is still safer than ad hoc pasted code.
- If Chinese text does not render, install or point the script at a CJK system font.
- If Preview.app caches an older PDF, close and reopen the file after regeneration.
