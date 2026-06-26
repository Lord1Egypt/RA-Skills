---
name: maxqda-timecode
description: Convert transcript timecodes from MM:SS format to MAXQDA-compatible [hh:mm:ss] format for qualitative research data import.
version: 1.0.0
author: @Kiriny1999
---

# MAXQDA Timecode Converter

Convert transcript timecodes from `MM:SS` format to MAXQDA-compatible `[hh:mm:ss]` format, with timecodes placed before speaker identity.

## Usage

When the user asks to convert interview transcripts for MAXQDA import:

```
Convert timecodes in [path] for MAXQDA
把 [路径] 的时间码转成 MAXQDA 格式
```

## What It Does

1. Removes the first line (title/header)
2. Converts timecodes and repositions them:
   - Input: `提问者 00:02` (Speaker MM:SS)
   - Output: `[00:00:02]提问者` ([hh:mm:ss]Speaker, no space)
3. Handles hours correctly when minutes exceed 60 (e.g., `65:30` → `[01:05:30]提问者`)
4. Overwrites the original file

## One-Step Conversion Script

```bash
perl -ne '
    next if $. == 1;  # Skip first line (title)
    # Remove BOM if present
    s/^\x{FEFF}//;
    # Convert: Speaker MM:SS -> [hh:mm:ss]Speaker (no space)
    if (/^(\S+)\s+(\d{2}):(\d{2})/) {
        $speaker = $1;
        $mm = $2;
        $ss = $3;
        $hh = int($mm / 60);
        $mm = $mm % 60;
        s/^(\S+)\s+(\d{2}):(\d{2})/sprintf("[%02d:%02d:%02d]%s", $hh, $mm, $ss, $speaker)/e;
    }
    print;
' "$INPUT_FILE" > "$TEMP_FILE" && mv "$TEMP_FILE" "$INPUT_FILE"
```

## Batch Processing

To process all `.txt` files in a directory:

```bash
for f in "/path/to/directory/"*.txt; do
    perl -ne '
        next if $. == 1;
        s/^\x{FEFF}//;
        if (/^(\S+)\s+(\d{2}):(\d{2})/) {
            $speaker = $1;
            $mm = $2;
            $ss = $3;
            $hh = int($mm / 60);
            $mm = $mm % 60;
            s/^(\S+)\s+(\d{2}):(\d{2})/sprintf("[%02d:%02d:%02d]%s", $hh, $mm, $ss, $speaker)/e;
        }
        print;
    ' "$f" > "${f}.tmp" && mv "${f}.tmp" "$f"
done
```

## Format Examples

| Input | Output |
|-------|--------|
| `提问者 00:02` | `[00:00:02]提问者` |
| `回答者 01:30` | `[00:01:30]回答者` |
| `提问者2 65:45` | `[01:05:45]提问者2` |

## Notes

- Original filename is preserved
- First line (title) is removed
- Handles UTF-8 BOM automatically
- Input format: `Speaker MM:SS`
- Output format: `[hh:mm:ss]Speaker` (no space between `]` and speaker)