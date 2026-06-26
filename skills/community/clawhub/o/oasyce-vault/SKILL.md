---
name: datavault
description: >
  Local-first data asset manager — scan, classify, and report on your data before deciding what to share.
  Use when user mentions scanning files, classifying data, data inventory, or organizing digital assets.
---

# DataVault

Know what you have before you decide what to share. Local-first data asset scanner and classifier.

## Prerequisites

```bash
pip install datavault
```

Verify: `datavault version` should print `0.1.0+`.

## Commands

### Scan a directory

```bash
datavault scan [path] [--no-recursive]
```

Scans a directory and categorizes all files (60+ formats recognized):
- Documents, spreadsheets, images, audio, video
- Code, data files, archives, databases

Default: scans current directory recursively.

### Classify a single file

```bash
datavault classify <file>
```

Returns category, MIME type, and file size.

### Generate a report

```bash
datavault report [path] [--format text|json]
```

Produces a summary report of all data assets found. JSON format available for programmatic use.

## When to use this skill

- User wants to know what data they have
- User asks to scan/inventory files or directories
- User wants a data asset report
- User is preparing to register assets on Oasyce (scan first, register later)

## When NOT to use this skill

- User wants to register/trade data rights (use oasyce-data-rights)
- User wants to move/delete/organize files (use standard file tools)

## Works with Oasyce

DataVault is standalone. When paired with [Oasyce](https://pypi.org/project/oasyce/), scanned assets can be registered on the decentralized network:

```bash
pip install datavault[oasyce]
datavault scan ~/Documents        # See what you have
oasyce register ~/Documents/report.pdf  # Register what matters
```
