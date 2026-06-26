---
name: premium-pdf
description: Generate premium enterprise-style PDFs from markdown content, with automatic de-AI text humanization (removes em dashes, AI filler phrases, overly formal language) and a professional Navy + Gold design system.
version: 1.0.0
emoji: "📄"
homepage: https://github.com/andreasozzo/SkillsAI
metadata: {"openclaw": {"requires": {"bins": ["python3"]}, "os": ["macos", "linux"], "skillKey": "premium-pdf", "always": false}}
user-invocable: true
---

# Premium Enterprise PDF Generator

Generate high-quality, enterprise-grade PDF documents from markdown input. This skill applies a **de-AI humanization pipeline** to make LLM-generated text sound more natural, then renders it into a **premium PDF** with a professional Navy + Gold design system (marketing agency quality).

---

## When to Use This Skill

Invoke this skill when the user:
- Asks to create a PDF from markdown or text content
- Wants to generate a professional report, proposal, or document
- Needs to export content as a visually polished enterprise document
- Says phrases like: "create a PDF", "generate a report PDF", "export as enterprise PDF", "make a premium PDF"

---

## How to Invoke

### Basic usage (markdown string)

```bash
python3 premium-pdf/generate_pdf.py \
  --input "# Report Title

Your markdown content here..." \
  --output output.pdf \
  --title "Document Title"
```

### From a markdown file

```bash
python3 premium-pdf/generate_pdf.py \
  --input path/to/document.md \
  --output output.pdf \
  --title "Document Title"
```

### With a company logo in the header

```bash
python3 premium-pdf/generate_pdf.py \
  --input path/to/document.md \
  --output output.pdf \
  --title "Quarterly Report" \
  --logo path/to/company-logo.png
```

---

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--input` or `-i` | Yes | Markdown text (string) or path to a `.md` file |
| `--output` or `-o` | Yes | Output PDF file path (e.g., `report.pdf`) |
| `--title` or `-t` | No | Document title shown in the header (default: "Enterprise Report") |
| `--logo` | No | Path to a PNG or JPG logo image to display in the header |

---

## What the Skill Does

### 1. De-AI Text Humanization

Before rendering, the skill automatically applies text transformations:

- **Em dashes** (`—`) → replaced with `, ` (natural comma-based flow)
- **En dashes** (`–`) → replaced with ` - `
- **Formal AI phrases** removed: "It is important to note", "Furthermore", "Moreover", "Additionally", "In conclusion", "In order to"
- **AI buzzwords** replaced: "utilize" → "use", "leverage" → "use", "delve into" → "explore", "comprehensive" → "complete", "robust" → "solid", "seamlessly" → "smoothly"
- **Unnecessary qualifiers** stripped: "basically", "literally", "actually", "quite"
- **Double spaces** normalized

### 2. Premium PDF Design (Navy + Gold)

The generated PDF features:

- **Color palette**: 60% white/light gray, 30% deep navy (#1A2B4A), 10% gold (#C9A84C)
- **Typography hierarchy**: H1 28pt → H2 20pt → H3 16pt → H4 13pt → Body 11pt
- **Professional header**: Navy background with white title + date (optional logo support)
- **Gold accent lines**: Under H2 headings and above the footer
- **Page numbers**: Centered footer with page count
- **Justified body text** for professional document appearance

### 3. Markdown Elements Supported

- Headings: `#`, `##`, `###`, `####`
- **Bold** and *italic* and ***bold-italic*** text
- Inline `code` and fenced code blocks
- Unordered lists (`-`, `*`, `+`) and ordered lists (`1.`, `2.`)
- Nested list items
- Blockquotes (`>`)
- Horizontal rules (`---`)
- Hyperlinks (rendered as bold text)

---

## Setup (First Time)

Install Python dependencies:

```bash
pip3 install -r premium-pdf/requirements.txt
```

Or install directly:

```bash
pip3 install "reportlab>=4.0.0" "Pillow>=9.0.0"
```

---

## Example Interaction

**User**: "Create a PDF from this markdown report and save it as quarterly-report.pdf"

**Agent action**:
```bash
python3 premium-pdf/generate_pdf.py \
  --input "[user's markdown content]" \
  --output quarterly-report.pdf \
  --title "Quarterly Report Q1 2026"
```

**Output**: `PDF generated successfully: /absolute/path/to/quarterly-report.pdf`

After running, inform the user of the output path so they can open the file.

---

## Error Handling

If the script returns an error:
1. Check that `reportlab` is installed: `pip3 install reportlab`
2. Verify the input markdown is not empty
3. Ensure the output directory is writable
4. Check that the logo file path exists (if `--logo` is used)
