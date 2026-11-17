---
name: my-content-organizer
description: "Organize workspace files by type, extension, and date. Use when: workspace is cluttered, need to sort downloads, clean up screenshots, organize media files, or prepare files for archival/backup."
metadata:
  {
    "openclaw":
      {
        "emoji": "📁",
        "requires": { "bins": ["mkdir", "mv", "find"] }
      }
  }
---

# Content Organizer Skill

Sort and organize workspace files into clean category folders.

## When to Use

✅ **USE this skill when:**
- "Organize my workspace" / "清理工作区"
- "Sort these files by type"
- "Where did my screenshots go?"
- Preparing files for backup or upload
- Downloads folder is a mess

## Category Rules

| Folder       | File Types                                    |
|--------------|-----------------------------------------------|
| images/      | jpg, jpeg, png, gif, webp, svg, bmp, tiff     |
| documents/   | pdf, doc, docx, txt, md, rtf, odt, xps        |
| spreadsheets/ | xls, xlsx, csv, tsv, ods                    |
| archives/    | zip, tar, gz, bz2, 7z, rar                   |
| code/        | py, js, ts, html, css, json, yaml, sh, rb    |
| media/       | mp3, mp4, wav, flac, mkv, mov, avi            |
| other/       | anything else                                 |

## Basic Steps

### 1. Scan & Report
```bash
find . -maxdepth 2 -type f 2>/dev/null | head -50
```

### 2. Create Category Folders
```bash
mkdir -p images documents spreadsheets archives code media other
```

### 3. Move Files (dry run first!)
```bash
# Dry run — shows what would move
find . -maxdepth 1 -type f | while read f; do
  ext="${f##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  case "$ext" in
    jpg|jpeg|png|gif|webp|svg|bmp|tiff) echo "Would move $f -> images/";;
    pdf|doc|docx|txt|md|rtf|odt|xps) echo "Would move $f -> documents/";;
    xls|xlsx|csv|tsv|ods) echo "Would move $f -> spreadsheets/";;
    zip|tar|gz|bz2|7z|rar) echo "Would move $f -> archives/";;
    py|js|ts|html|css|json|yaml|yml|sh|rb) echo "Would move $f -> code/";;
    mp3|mp4|wav|flac|mkv|mov|avi) echo "Would move $f -> media/";;
    *) echo "Would move $f -> other/";;
  esac
done
```

### 4. Execute the Move
```bash
find . -maxdepth 1 -type f | while read f; do
  [ "$f" = "./SKILL.md" ] && continue
  ext="${f##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  case "$ext" in
    jpg|jpeg|png|gif|webp|svg|bmp|tiff) mv "$f" images/ 2>/dev/null;;
    pdf|doc|docx|txt|md|rtf|odt|xps) mv "$f" documents/ 2>/dev/null;;
    xls|xlsx|csv|tsv|ods) mv "$f" spreadsheets/ 2>/dev/null;;
    zip|tar|gz|bz2|7z|rar) mv "$f" archives/ 2>/dev/null;;
    py|js|ts|html|css|json|yaml|yml|sh|rb) mv "$f" code/ 2>/dev/null;;
    mp3|mp4|wav|flac|mkv|mov|avi) mv "$f" media/ 2>/dev/null;;
    *) mv "$f" other/ 2>/dev/null;;
  esac
done
```

### 5. Verify
```bash
echo "=== Organized workspace ==="
ls -la */ 2>/dev/null
```

## Notes
- **Always dry run first** — never skip the preview step
- Files with no extension go to `other/`
- Hidden files (starting with `.`) are skipped
- Run from the directory you want to organize
