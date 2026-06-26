---
name: file-organizer
description: "File organization and batch operations for workspace management. Use when organizing files for: (1) Moving files to correct directories, (2) Batch renaming (patterns, numbering, dates), (3) Creating directory structures, (4) Organizing by type/extension, (5) Cleaning scattered files, (6) Project scaffolding, or (7) Restructuring project layouts."
---

# File Organizer

Manages file organization through safe, predictable batch operations.

## Core Workflows

### Directory Structure
Create standard project layouts:
```
project/
├── src/          - Source code
├── docs/         - Documentation
├── tests/        - Test files
├── assets/       - Images, fonts, media
├── scripts/      - Build scripts, utilities
└── config/       - Configuration files
```

### Moving Files
- `mv <source> <dest>` - Single file
- `find . -name "*.ext" -exec mv {} <dest>/ \;` - Batch by extension
- Always confirm destination exists

### Batch Renaming
**Patterns:**
- Sequential numbering: `file_{001..100}.txt`
- Date-based: `YYYY-MM-DD_description`
- Type-based: Group by extension

**Safe approach:**
1. `echo` commands first (dry run)
2. Review output
3. Remove `echo`, execute

### Organizing by Type
Group files by extension into folders:
```
mkdir -p images docs code
find . -name "*.png" -o -name "*.jpg" | xargs -I {} mv {} images/
find . -name "*.md" -o -name "*.txt" | xargs -I {} mv {} docs/
find . -name "*.py" -o -name "*.js" | xargs -I {} mv {} code/
```

### Finding Scattered Files
```
find . -type f -name "*.ext"    # Find by extension
find . -type f -mtime -7        # Modified in last 7 days
find . -type f -size +100M      # Large files
```

### Dry Runs First
Always preview batch operations:
```
echo "Would move these files:"
find . -name "*.ext"
# Review, then execute
```

## Safety Rules

1. **Never delete** without explicit permission (use `trash` if available)
2. **Dry run first** - Always echo/preview batch operations
3. **Check destinations** - Confirm target directories exist
4. **Backup before restructure** - Snapshot before major moves
5. **Respect workspace boundaries** - Only touch ~/openclaw

## When to Read references/patterns.md

Load when:
- Complex rename patterns needed
- Project structure templates required
- Advanced find commands for filtering
- Edge cases (symlinks, special characters)