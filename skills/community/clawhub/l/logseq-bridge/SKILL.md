---
name: logseq-bridge
description: Pure file-based interaction with a local Logseq graph. Read, write, search, and manage Logseq journals and pages via direct `.md` file operations. No plugins or HTTP APIs needed.
---

# Logseq Bridge

Interact with your Logseq graph by **directly reading and writing `.md` files** on disk. No plugins, no HTTP APIs — just filesystem access to your Logseq graph directory.

---

## How It Works

```
Agent → Shell → Read/Write local `.md` files → Logseq reloads on next Cmd/Ctrl+R
```

**Pure file operations. No HTTP APIs, no plugin bridges, no port listeners.**

---

## Prerequisites

Your Logseq graph is stored as a local directory structure:

```
{graph_root}/
├── journals/       ← Daily notes *.md
├── pages/          ← Knowledge pages *.md
├── assets/         ← Images, attachments
├── logseq/         ← Config files
│   └── config.edn
└── .logseq/        ← Index database (auto-maintained)
    └── graphs/
        └── logseq_local_*.transit
```

What you need:
1. **Logseq installed** and opened at least once (so `.logseq/` exists)
2. **Read/write access** to the graph directory on your filesystem
3. **Know your graph path**

---

## Finding Your Graph Path

### Method 1: From Logseq UI

Open Logseq → **Settings** → **Advanced** → Look for "Current graph directory"

### Method 2: From the transit database file

```bash
ls ~/.logseq/graphs/*.transit
# e.g.: logseq_local_E%3A+++Users++MyUser++Logseq.transit
```

The filename is URL-encoded. Decode it to find your path:

```bash
# In WSL/Linux, mount the drive and set the path
export LQ="/mnt/c/Users/MyUser/Logseq"
```

---

## Core Operations

Set the environment variable first:

```bash
export LQ="/path/to/your/logseq/graph"
```

### 📝 Write to Today's Journal

```bash
DATE=$(date +%Y_%m_%d)
FILE="$LQ/journals/$DATE.md"

cat >> "$FILE" << 'EOF'
- 🦞 Note title
  - Sub-item 1
  - Sub-item 2
EOF
```

### 📖 Read a Journal

```bash
cat "$LQ/journals/$(date +%Y_%m_%d).md"
# Or a specific date
cat "$LQ/journals/2026_04_25.md"
```

### 📄 Read a Knowledge Page

```bash
cat "$LQ/pages/Page Name.md"
```

### 🔍 Search Notes

```bash
# Search all pages
grep -ri "keyword" "$LQ/pages/"

# Search journals
grep -rn "keyword" "$LQ/journals/"

# Search the database index (faster)
strings ~/.logseq/graphs/*.transit | grep -i "keyword" | head -20
```

### 📋 Create a New Page

```bash
cat > "$LQ/pages/New Page.md" << 'EOF'
title:: New Page
tags:: tag1, tag2

- Page content
  - Sub content
EOF
```

### 📊 List Statistics

```bash
# Total journals
ls "$LQ/journals/" | wc -l

# Total pages
ls "$LQ/pages/" | wc -l

# Latest 5 journals
ls -t "$LQ/journals/" | head -5
```

---

## Markdown Format Reference

Write notes in Logseq-compatible Markdown:

| Syntax | Example | Note |
|--------|---------|------|
| Bullet list | `- content` | Every line starts with `- ` |
| Indent children | `  - child` | 2-space indent |
| Bold | `**text**` | Standard Markdown |
| Wiki link | `[[Page Name]]` | Auto-links pages |
| Tag | `#tagname` | Auto-indexed |
| Property | `key:: value` | Page or block-level property |
| TODO marker | `TODO do something` | Renders as task |
| DONE marker | `DONE completed` | Renders as done |

---

## Known Issues & Limitations

| Issue | Description | Workaround |
|-------|-------------|------------|
| No real-time refresh | Logseq doesn't watch file changes | Press `Ctrl+Shift+R` (or `Cmd+Shift+R`) to reload |
| Static text reads | Reads raw `.md`, not block tree | Parse Markdown yourself for structured data |
| Cloud sync delay | Graph on OneDrive/Dropbox may lag | Wait a few seconds after writing |
| Special characters in paths | Chinese/Unicode chars | Wrap paths in double quotes |

---

## Quick Start

```bash
# 1. Find your graph path in Logseq Settings → Advanced

# 2. Set the path
export LQ="/path/to/your/logseq/graph"

# 3. Write a test note
DATE=$(date +%Y_%m_%d)
echo "- 🎉 Logseq Bridge test successful!" >> "$LQ/journals/$DATE.md"

# 4. Reload Logseq (Ctrl+Shift+R or Cmd+Shift+R)
```

---

## Best Practices

1. **File operations first** — stable, zero dependencies
2. **Tell user to reload** — Logseq won't auto-detect file changes
3. **Date format** — Journal filenames are always `YYYY_MM_DD.md`
4. **Page naming** — The filename IS the page name; Chinese OK
5. **Heredoc** — Use `<< 'EOF'` for multi-line content

---

## References

- Logseq: https://logseq.com
- Logseq Markdown Guide: https://docs.logseq.com
- ClawHub: https://clawhub.ai
