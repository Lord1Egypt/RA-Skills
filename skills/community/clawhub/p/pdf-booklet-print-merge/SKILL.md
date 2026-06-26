---
name: pdf-booklet-print-merge
description: 'Merge PDF files and create booklet-ready 2-up duplex output for saddle-stitch printing. Use for PDF merge, booklet imposition, short-edge duplex, center-fold reading, 小册子打印, 对折中缝翻页.'
argument-hint: '--input-dir data/input --output data/output/booklet_print.pdf --merged-output data/output/merged_source.pdf'
user-invocable: true
disable-model-invocation: false
---

# PDF Booklet Print Merge

## When To Use

- You need to merge multiple PDF files into one source file.
- You need a booklet print layout (2 pages per sheet, landscape, duplex).
- You want pages reordered for saddle stitch so the booklet can be folded at the center.
- You need Chinese-friendly use cases like `小册子打印`, `双面打印`, `中缝翻页`, `对折阅读`.

## Inputs

- `--input-dir`: source folder containing PDF files.
- `--output`: booklet-imposed output path.
- `--merged-output`: sequential merged output path (optional).
- `--no-merged-output`: skip sequential merged output.

## Procedure

1. Validate that the input directory exists and contains at least one PDF.
2. Sort PDF files by natural filename order.
3. Merge all pages sequentially into a source sequence.
4. Pad page count to a multiple of 4 with blanks for booklet signatures.
5. Reorder pages into saddle-stitch sheet order.
6. Place left/right pages on a single landscape sheet (2-up layout).
7. Write booklet output and optional merged source output.
8. Return print settings guidance: landscape + duplex + short-edge flip.

## Run Script

Run [booklet_merge.py](./scripts/booklet_merge.py) with your arguments.

Example:

```bash
/usr/bin/python3 ./.claude/skills/pdf-booklet-print-merge/scripts/booklet_merge.py --input-dir data/input
```

## References

- Publishing checklist: [publish-checklist.md](./references/publish-checklist.md)
