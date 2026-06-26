---
name: kai-docx-generator
description: >-
  Generate professional .docx documents from Markdown text or fill data into .docx templates.
  Use when: converting markdown to Word, generating reports/contracts/proposals as .docx,
  filling template variables in Word documents, validating .docx structure.
  Triggers: "生成word", "转成docx", "markdown转word", "生成文档", "填充模板",
  "fill template", "generate docx", "convert markdown to word".
version: 1.1.0
metadata:
  openclaw:
    emoji: "📝"
    os:
      - darwin
      - linux
      - windows
    requires:
      bins:
        - python3
    install:
      - id: python-docx
        kind: uv
        package: python-docx
        label: "python-docx (core)"
      - id: markdown-it-py
        kind: uv
        package: markdown-it-py
        label: "markdown-it-py (parser)"
      - id: lxml
        kind: uv
        package: lxml
        label: "lxml (XML)"
      - id: Pillow
        kind: uv
        package: Pillow
        label: "Pillow (images)"
      - id: pyyaml
        kind: uv
        package: pyyaml
        label: "pyyaml (YAML)"
---

# kai-docx-generator

Generate professional .docx documents from Markdown, or fill data into .docx templates.

## Core Principles

1. **Zero Fabrication** — Never invent content. If data is missing, use placeholder text (`[待填写]`) or ask the user.
2. **Template Filling is XML-level** — `{{variable_name}}` patterns are matched at the `w:t` XML node level inside the .docx. Values are sanitized to escape `& < > " '` and remove control characters.
3. **Security: Path Validation** — Image paths must be relative or within the current working directory. Absolute paths (e.g. `/tmp/...`) and path traversal (`..`) are rejected.
4. **Auto-Truncation** — Exceeding input limits (200KB, 20 images, 50 table rows, 20 table columns) triggers automatic truncation without error.
5. **Template Strictness** — `--strict` mode on `fill_template.py` returns exit code 1 when any placeholder remains unreplaced, enabling CI/CD gate usage.

## Commands

| Command | What it does |
|---------|-------------|
| `python3 <skill-path>/scripts/generate.py <input.md> <output.docx>` | Convert Markdown to .docx |
| `python3 <skill-path>/scripts/generate.py --style <style> <input.md> <output.docx>` | Convert with a specific style |
| `python3 <skill-path>/scripts/fill_template.py --data <data.json|frontmatter.md> --output <out.docx> <template.docx>` | Fill template with data |
| `python3 <skill-path>/scripts/fill_template.py --strict --data <data.json> --output <out.docx> <template.docx>` | Fill template, fail if placeholders remain |
| `python3 <skill-path>/scripts/validate.py <file.docx>` | Validate .docx file structure |

## Markdown → .docx

```bash
python3 <skill-path>/scripts/generate.py input.md output.docx
python3 <skill-path>/scripts/generate.py --style report input.md output.docx
```

### Content-Type → Style Routing

When no `--style` is specified, recommend a style based on topic keywords:

| Topic keywords | Recommended style | Use case |
|---------------|-------------------|---------|
| 合同、协议、条款、contract, agreement | `contract` | Contracts & legal documents |
| 报告、分析、数据、KPI、report, analysis, dashboard | `report` | Business reports (blue headers) |
| 会议纪要、meeting minutes, 讨论 | `meeting` | Meeting minutes (compact layout) |
| 红头文件、通知、通报、dispatch, official notice | `dispatch` | Official dispatchs (red header) |
| 技术、API、架构、代码、spec, architecture | `tech_spec` | Technical specs (monospace body) |
| 公函、商务信、letter | `business_letter` | Business letters |
| 公告、公告通知、notice, announcement | `notice` | Official notices (large bold text) |
| 其他 / general | `standard` | General documents |

When routing, announce: *"推荐使用 `[style]` 样式 ([description])，可用 `--style` 覆盖。"*

### Default Output Filename

If the user does not specify an output filename, derive it from the input file:
- `<input>.md` → `<input>.docx` (same basename, replace extension)
- For generated content (no input file), use: `doc-<YYYY-MM-DD>-<slug>.docx`
- **Slug rule:** lowercase the title/topic, replace spaces and non-ASCII with hyphens, keep only alphanumeric ASCII and hyphens, max 30 chars.

### Supported Markdown Features

| Feature | Syntax |
|---------|--------|
| Headings (H1-H3) | `#`, `##`, `###` |
| Paragraphs | Text blocks |
| Bold / Italic | `**bold**`, `*italic*` |
| Bullet / Numbered lists | `-`, `1.` |
| Tables | Standard GFM tables |
| Code blocks | Triple backticks, with optional language |
| Blockquotes (callout) | `> text` → info box |
| Images | `![caption](path)` |
| Page break | `<!-- pagebreak -->` |
| Horizontal rule | `---` |
| YAML front matter | `---\ntitle: ...\n---` |

### Style Presets

| Style | Use case |
|-------|----------|
| `standard` (default) | General documents |
| `contract` | Contracts & agreements (formal, 12pt) |
| `report` | Business reports (blue headers, 10.5pt) |
| `meeting` | Meeting minutes (compact, 10.5pt) |
| `business_letter` | Business letters (traditional format) |
| `tech_spec` | Technical specifications (monospace, dark theme) |
| `dispatch` | Official dispatchs / 红头文件 (red header) |
| `notice` | Official notices (bold, 14pt) |

### YAML Front Matter

```yaml
---
title: Document Title          # 写入 docx core_properties.title
author: Author Name            # 写入 docx core_properties.author
date: 2026-04-10               # 写入 docx core_properties.created
lang: zh                       # 可选: zh | en, 影响默认文本
header:
  text: CONFIDENTIAL           # 页眉文字
  alignment: center            # left | center | right
footer:
  page_number: true            # 显示页码
toc:
  max_level: 3                 # TOC 包含的最大标题级别 (1-3)
---
```

All fields are optional. `title`, `author`, and `date` are written to the .docx core properties (visible in Word → File → Info).

## Template Filling

```bash
# With JSON data
python3 <skill-path>/scripts/fill_template.py --data data.json --output output.docx template.docx

# With Markdown front matter as data
python3 <skill-path>/scripts/fill_template.py --data frontmatter.md --output output.docx template.docx

# Strict mode: fail if any placeholder remains unreplaced
python3 <skill-path>/scripts/fill_template.py --strict --data data.json --output output.docx template.docx
```

Data format (JSON):
```json
{
  "company_name": "Acme Corp",
  "amount": "¥1,000,000",
  "date": "2026-04-10"
}
```

Template placeholders are `{{variable_name}}` patterns in the .docx text (matched at `w:t` XML node level). Values are automatically sanitized to escape XML special characters and remove control characters. Long values are truncated to prevent layout breakage.

### --strict Mode

When `--strict` is passed, the script exits with code 1 if any `{{placeholder}}` remains unreplaced after filling. This enables CI/CD gating: all placeholders must have corresponding data keys.

### Input Limits

- Markdown size: 200KB max
- Images: 20 max
- Table rows: 50 max
- Table columns: 20 max

Exceeding limits triggers automatic truncation with no error.

## QA Process

After generating a .docx, run these checks:

**Automated checks** (run `validate.py` on the output):
1. File is valid ZIP with required structure (`word/document.xml`, `[Content_Types].xml`, `word/_rels/document.xml.rels`)
2. XML is parseable (no malformed tags)
3. File size is reasonable (> 50KB warning, > 50MB warning)
4. No unreplaced `{{placeholders}}` detected

**Visual checks** (open in Word/WPS):
5. **Style conformance** — headings use the correct style preset colors and fonts (see `references/style-presets.md` for exact values)
6. **Spacing** — callouts have proper spacing from surrounding elements
7. **Tables** — column widths are reasonable, no emoji overlap
8. **Code blocks** — monospace font + gray background rendering
9. **TOC** — if requested, TOC field code is present (requires Word to update fields)
10. **Images** — embedded images render at correct size, no broken links

**Template filling checks:**
11. All `{{placeholders}}` with matching data keys are replaced
12. No XML corruption — the output opens without error
13. Long values are truncated appropriately (no layout breakage)

Use `--validate` flag with `generate.py` to run automated checks automatically after generation.

## Works with

- **kai-report-creator** — generate .docx reports from markdown output
- Any Markdown content (reports, specs, meeting notes, contracts)
- Existing .docx templates with `{{placeholder}}` variables
