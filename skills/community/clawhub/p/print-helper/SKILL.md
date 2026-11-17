---
name: print-helper
description: "打印本地文件。支持PDF、图片、Office文档；可指定份数、双面、页码范围。"
---

# Print Helper

Use for printing local files with optional manual duplex.

## Workflow

1. Inspect file existence and type.
2. If duplex requested and no auto-duplex printer:
   - Print odd pages immediately.
   - Wait for flip delay (`--flip-seconds`, default 30).
   - Print even pages immediately.
3. Otherwise print normally.

## Commands

```powershell
python skills/print-helper/scripts/print_pdf.py --file "<path>" --duplex --flip-seconds 60
```

## Notes

- Uses SumatraPDF for silent printing. Install from https://www.sumatrapdfreader.org/ if not found.
- Default flip delay is 60 seconds. Adjust with `--flip-seconds`.
- For Office docs, use `Start-Process -Verb Print` (no silent option).
