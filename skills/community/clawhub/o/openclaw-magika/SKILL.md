---
name: openclaw-magika
description: "AI-powered file type detection. Detects file content types (200+ types, ~99% accuracy) using Google Magika deep learning model. Triggered when: (1) user asks to identify/check/detect file type, (2) analyzing uploaded files, (3) batch classifying files by content. Requires: magika CLI (pip install/pipx install/brew). Reads: no config files. No data sent to third parties; local inference only."
metadata: {"openclaw":{"emoji":"🔍","requires":{"anyBins":["magika"]}}}}
---

# openclaw-magika

> AI-powered file content type detection using Google Magika.

## Quick Use

```bash
# Single file — label output
magika -l /path/to/file

# MIME type output
magika -i /path/to/file

# Recursive directory scan
magika -r ./workspace/

# JSON output (for programmatic use)
magika --json /path/to/file

# Batch multiple files
magika -r --json ./uploads/
```

## Common Tasks

| Task | Command |
|------|---------|
| Identify single file | `magika -l <file>` |
| Get MIME type | `magika -i <file>` |
| Recursive scan | `magika -r <dir>` |
| Batch JSON | `magika --jsonl <files...>` |
| With confidence score | `magika -s -l <file>` |

## Output Labels

Magika identifies 200+ content types including: `markdown`, `json`, `python`, `javascript`, `pdf`, `zip`, `png`, `jpeg`, `html`, `xml`, `sql`, `csv`, `png`, `gif`, `mp3`, `mp4`, `exe`, `elf`, `wasm`, and many more.

High-confidence predictions are marked with `[HIGH]`. Low-confidence returns generic labels like `text` or `unknown binary data`.

## Install

```bash
# pipx (recommended)
pipx install magika

# pip
pip install magika

# brew
brew install magika

# curl script
curl -LsSf https://securityresearch.google/magika/install.sh | sh
```

## Notes

- **Fast**: ~5ms per file after model loads
- **Accurate**: 99% average precision on 200+ file types
- **Local**: All inference runs locally, no network needed
- **Size agnostic**: Only reads a subset of file content regardless of file size
