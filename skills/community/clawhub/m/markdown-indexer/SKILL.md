---
name: markdown-indexer
description: Scan a directory of Markdown files, extract titles/headings/frontmatter, build a searchable index JSON, and output a concise summary report. Use when you need to inventory, catalog, or make a folder of .md files discoverable without reading each file individually.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["jq"] },
        "install":
          [
            {
              "id": "jq",
              "kind": "system",
              "label": "Install jq (apt install jq or brew install jq)",
            },
          ],
      },
    "emoji": "📑"
  }
---

# Markdown Indexer

Scan Markdown files in a directory and produce a structured index.

## When to use it

- You have a folder of `.md` files (notes, docs, wikis) and need to know what's in them at a glance.
- Before uploading or publishing a collection of documents, you want a catalog.
- You need a JSON index for downstream search or automation.

## Prerequisites

- `jq` is installed (used for JSON formatting)
- Files must be UTF-8 encoded Markdown

## Usage

### Step 1: Scan a directory

```bash
# Basic scan — outputs index.json in current directory
find ./docs -name "*.md" -print0 | while IFS= read -r -d '' f; do
  title=$(grep -m1 '^# ' "$f" | sed 's/^# //' | tr '\n' ' ')
  [ -z "$title" ] && title=$(basename "$f" .md)
  headings=$(grep -c '^#' "$f" 2>/dev/null || echo 0)
  lines=$(wc -l < "$f")
  frontmatter=$(head -20 "$f" | grep -c '^---$' || echo 0)
  echo "{\"file\":\"$f\",\"title\":\"$title\",\"headings_count\":$headings,\"lines\":$lines,\"has_frontmatter\":$frontmatter}"
done | jq -s '.' > index.json
```

### Step 2: View summary

```bash
jq 'length' index.json          # total files
jq 'sort_by(-.lines)[:5]' index.json  # top 5 longest
jq '[.[] | select(.has_frontmatter >= 2)] | length' index.json  # files with YAML frontmatter
```

### Step 3: Generate a Markdown report

```bash
jq -r '.[] | "- **\(.title)** — `\(.file)` (\(.lines) lines, \(.headings_count) headings)"' index.md > catalog.md
```

## Output

- `index.json`: Array of objects with `file`, `title`, `headings_count`, `lines`, `has_frontmatter`
- `catalog.md` (optional): Human-readable Markdown table of contents

## Example: Pipeline with other tools

```bash
# 1. Index the docs folder
bash scan.sh ./docs

# 2. Filter out files without headings
jq '[.[] | select(.headings_count > 0)]' index.json > valid-index.json

# 3. Upload to your knowledge base
curl -X POST https://api.example.com/import -d @valid-index.json
```
