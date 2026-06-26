# kai-docx-generator

> Generate professional .docx documents from Markdown — 8 style presets for contracts, reports, dispatches, and more. Or fill data into existing .docx templates with `{{placeholder}}` variables.

A Claude Code skill that converts Markdown to Word documents with style-driven formatting, or fills data into .docx templates via XML-level scanning.

English | [简体中文](README.zh-CN.md)

---

## Features

### Markdown → .docx

| Feature | Input | Output |
|---------|-------|--------|
| Headings | `#`, `##`, `###` | Styled heading levels 1–3 |
| Tables | GFM tables | Full-width, zebra-striped, blue headers |
| Lists | `- item`, `1. item` | List Bullet / List Number styles |
| Code blocks | `` ```python `` | Monospace, gray background, language label |
| Callouts | `> text` | Color-coded info/warning/success boxes |
| Images | `![alt](path)` | Embedded with optional caption |
| Page break | `<!-- pagebreak -->` | Word page break |
| TOC | YAML front matter | Auto-generated table of contents |

### Style Presets
|-------|----------|------------|
| `standard` (default) | General documents | Blue headings, 11pt, 1.15 spacing |
| `contract` | Contracts & agreements | Formal, 12pt, tight spacing |
| `report` | Business reports | Blue headers, 10.5pt, professional |
| `meeting` | Meeting minutes | Compact, 10.5pt, action-item focus |
| `business_letter` | Business letters | Traditional letter format |
| `tech_spec` | Technical specifications | Monospace, dark-theme friendly |
| `dispatch` | Official dispatchs / 红头文件 | Red Heading 1, 28pt fixed spacing |
| `notice` | Official notices | Bold, 14pt, authoritative |

---

## Design Philosophy

### 1. Content-Style Separation

Markdown content never references colors, fonts, or sizes directly. It declares structure (`# heading`, `> quote`), and the style preset decides how it looks. Swap `--style report` to `--style contract` and the same Markdown produces a completely different document.

### 2. Style-Driven Architecture

Each style preset configures: heading colors/sizes, paragraph spacing, line spacing, font sizes. All presets share the same rendering engine — no duplicated code.

### 3. CJK Font Handling

Chinese/Japanese/Korean characters render correctly via `w:eastAsia` XML attributes on every run. Default font: Microsoft YaHei (Windows) / PingFang SC (macOS fallback).

### 4. Security by Default

| Threat | Mitigation |
|--------|------------|
| Path traversal in images | Rejects `..` and absolute paths |
| XML injection in templates | Escapes `&`, `<`, `>` |
| Input exhaustion | 200KB markdown, 20 images, 50×20 tables |

---

## Install

### Claude Code

Tell Claude: "Install kai-docx-generator"

Or manually:
```bash
pip install kai-docx-generator
```

### OpenClaw

```bash
# Via ClawHub (recommended)
clawhub install kai-docx-generator

# Or manually
git clone https://github.com/kaisersong/kai-docx-generator ~/.openclaw/skills/kai-docx-generator
```

> ClawHub page: https://clawhub.ai/kaisersong/kai-docx-generator

OpenClaw auto-installs all dependencies on first use.

---

## Usage

### Commands

```bash
# Basic: Markdown → .docx
kai-docx-generate input.md output.docx

# With style preset
kai-docx-generate --style report input.md output.docx

# Fill data into .docx template (JSON)
kai-docx-fill --data data.json --output output.docx template.docx

# Fill data from YAML front matter
kai-docx-fill --data frontmatter.md --output output.docx template.docx

# Validate .docx structure
kai-docx-validate file.docx
```

### Typical Workflows

**Generate a Business Report:**

```bash
# 1. Write report.md with YAML front matter
# 2. Convert with report style
kai-docx-generate --style report report.md report.docx
# → report.docx (blue headers, professional spacing)
```

**Fill a Contract Template:**

```bash
# 1. Prepare template.docx with {{party_a}}, {{amount}}, {{date}}
# 2. Fill with JSON data
kai-docx-fill --data contract-data.json --output signed.docx template.docx
# → signed.docx (all placeholders replaced)
```

**Generate with TOC and Header/Footer:**

```markdown
---
title: Q4 Technical Report
author: Engineering Team
date: 2026-04-10
header:
  text: CONFIDENTIAL
  alignment: center
footer:
  page_number: true
toc:
  max_level: 3
---

# Executive Summary
...
```

```bash
kai-docx-generate --style tech_spec report.md report.docx
# → report.docx (TOC, page numbers, "CONFIDENTIAL" header)
```

---

## Features

### Markdown Support

| Element | Syntax | Rendering |
|---------|--------|-----------|
| Headings (H1–H3) | `#`, `##`, `###` | Styled by preset, CJK fonts |
| Paragraphs | Text blocks | Standard spacing, rich text runs |
| Bold / Italic | `**bold**`, `*italic*` | Per-run formatting |
| Bullet lists | `- item` | List Bullet style |
| Numbered lists | `1. item` | List Number style |
| Tables | GFM pipe tables | 100% width, zebra stripes, blue headers |
| Code blocks | Triple backticks | Monospace, gray bg, language label |
| Blockquotes | `> text` | Color-coded callout box |
| Images | `![caption](path)` | Embedded, centered caption |
| Page break | `<!-- pagebreak -->` | Word page break |
| Horizontal rule | `---` | Bottom-border line |
| YAML front matter | `---\n...\n---` | Metadata, header, footer, TOC |

### Template Filling

- Scans `w:t` XML nodes in document body, headers, footers, comments, footnotes
- Replaces `{{placeholder}}` patterns with provided data
- Sanitizes values: removes control chars, escapes XML, truncates at 5000 chars
- Multi-call safe: each `fill()` call resets to original template state

### Input Limits

| Resource | Limit | Behavior on exceed |
|----------|-------|-------------------|
| Markdown size | 200 KB | Truncate to 200 KB |
| Images | 20 | Drop excess images |
| Table rows | 50 | Truncate to 50 rows |
| Table columns | 20 | Truncate to 20 cols |
| Template value | 5000 chars | Truncate per value |

---

## Requirements

| Dependency | Purpose | Auto-installed |
|------------|---------|----------------|
| Python >= 3.10 | Runtime | ❌ |
| `python-docx` >= 1.1.0 | Word document assembly | ✅ |
| `markdown-it-py` >= 3.0.0 | Markdown parsing (GFM-like) | ✅ |
| `lxml` >= 4.9.0 | XML processing | ✅ |
| `Pillow` >= 10.0.0 | Image validation | ✅ |
| `pyyaml` >= 6.0 | YAML front matter parsing | ✅ |

---

## Compatibility

| Platform | Version | Install path |
|----------|---------|--------------|
| Claude Code | any | `~/.claude/skills/kai-docx-generator/` |
| OpenClaw | ≥ 0.9 | `~/.openclaw/skills/kai-docx-generator/` |

**Works With:**

| Skill | Output | Consumed As |
|-------|--------|-------------|
| kai-report-creator | Markdown reports | → .docx via kai-docx-generate |
| Any Markdown source | .md files | → styled .docx |
| Existing .docx templates | `{{placeholder}}` patterns | → filled via kai-docx-fill |

---

## Version History

**v0.1.0** — Initial release: Markdown → .docx with 8 style presets, template filling with XML scanning, TOC insertion, input limits, security protections.
