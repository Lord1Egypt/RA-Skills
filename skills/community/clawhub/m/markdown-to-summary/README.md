# Markdown To Summary

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Distills long markdown documents into concise summaries — preserves key facts, removes filler

## What Problem This Solves

Long README, article, or doc needs to be understood in minutes, not hours. This skill identifies the document type (technical doc, article, meeting notes, changelog) and extracts the essential points while preserving technical accuracy.

**When triggered:** Markdown text + summary/condense/tl;dr intent.

## Features

- **Document type detection** — automatically identifies README, article, meeting notes, or changelog and adapts strategy
- **Preserves technical accuracy** — keeps exact version numbers, commands, paths, and URLs
- **Length control** — outputs 20-40% of original length unless user specifies otherwise
- **Structured output options** — prose paragraphs, bullet lists, or single-sentence tl;dr

## Quick Start

```bash
# Via ClawHub
clawhub install markdown-to-summary

# Or manually
cp -r markdown-to-summary ~/.openclaw/skills/
```

### Usage

```
/markdown-to-summary
```

Paste markdown and ask to summarize.

```
/markdown-to-summary/bullet
```

Outputs key points as a quick-scan bullet list.

```
/markdown-to-summary/tl-dr
```

Single sentence + one paragraph maximum.

## Modes

| Mode | Description |
|------|-------------|
| `/markdown-to-summary` | Concise prose summary, ~20-30% of original |
| `/markdown-to-summary/bullet` | Key points as structured bullets |
| `/markdown-to-summary/tl-dr` | Absolute shortest: 1 sentence + 1 paragraph |

## Examples

| Input | Output |
|-------|--------|
| 2000-word README | Preserves: prerequisites, key commands, architecture. Drops: installation chatter |
| Changelog with 20 entries | Groups: 3 features, 5 fixes, 1 breaking change |
| API doc with code examples | Code block kept as reference, surrounding text summarized |
| Article with digression | Skips tangent, keeps main argument and evidence |

## Directory Structure

```
markdown-to-summary/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # Document type taxonomies, length guidelines
└── tests/
```

## License

MIT License — see [LICENSE](LICENSE).