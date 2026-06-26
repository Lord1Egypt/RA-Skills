---
name: parser
version: "3.0.2"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [parser, tool, utility]
description: "Parse JSON, CSV, XML, and logs into structured output. Use when converting formats, validating structure, extracting fields, analyzing nested data."
---

# parser

Parse and extract data from various file formats.

## Commands

### `json`

Parse JSON files (uses jq if available, else built-in)

```bash
scripts/script.sh json
```

### `csv`

Parse CSV files, optionally extract a column by name or number

```bash
scripts/script.sh csv
```

### `xml`

Parse XML files with optional XPath (requires python3)

```bash
scripts/script.sh xml
```

### `yaml`

Parse YAML files with optional key path (requires python3)

```bash
scripts/script.sh yaml
```

### `lines`

Filter lines by pattern (grep-like, with context)

```bash
scripts/script.sh lines
```

### `split`

Split file content by delimiter

```bash
scripts/script.sh split
```

### `extract`

Extract text matching a regex pattern

```bash
scripts/script.sh extract
```

### `stats`

Show file statistics (lines, words, chars, encoding)

```bash
scripts/script.sh stats
```

## Requirements

- python3
- jq (optional)

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*

## Data Storage

Parse results can be cached in `~/.local/share/parser/`.
