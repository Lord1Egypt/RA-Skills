---
name: ini-align
version: 1.0.0
description: >
  INI file section and key-value alignment tool. Reorders sections and keys in a target INI file
  to match the order in a source (reference) INI file. Target-only sections/keys preserved at end
  with full content, source-only sections listed as comments. Use when user requests "INI section
  reorder", "INI key alignment", "align INI sections", "reorder INI config", or similar needs.
---

# INI File Alignment

## Overview

Align a target INI file's section order and key order to match a source (reference) INI file.

## Usage

Run the script directly:

```bash
python scripts/ini_align.py <source.ini> <target.ini> <output.ini>
```

## Input/Output Convention

- **source.ini**: Reference file, never modified
- **target.ini**: File to be reordered, never modified
- **output.ini**: Output file with aligned result. Never overwrite source or target.

## Alignment Rules

The script will:

1. **Common sections**: Sections present in both files are reordered to match source order. Keys within each section are also reordered to match source key order.
2. **Target-only keys**: Keys in target but not in source are appended at the end of that section.
3. **Source-only sections**: Sections only in source are listed as comments (`; [SectionName]`) at the end of output.
4. **Target-only sections**: Sections only in target are preserved with full content at the end of output.
5. **Duplicate sections**: If source has duplicate section names, the first occurrence determines position.

## Pre-execution Confirmation

Before running the script, confirm with the user:

- Full paths to source and target files
- Output file path (suggest naming: `<original>-aligned.ini`)
- Confirm original files will not be overwritten

## Post-execution Summary

After running, output statistics:

- Source section count
- Target section count
- Common section count
- Source-only and target-only section counts
- Any duplicate section warnings
