---
name: google-doc-format
description: Create professionally formatted Google Docs from markdown using gog docs create. Produces clean documents with proper heading hierarchy, real Google Docs tables (not tab-separated text), bold text, bullet lists, numbered lists, and clickable hyperlinks. Use when creating or recreating Google Docs that need proper formatting, especially documents with data tables, link indexes, or structured reports. Triggers on: format google doc, create formatted doc, fix google doc tables, google doc formatting, format doc for client, create master index, create deliverable doc, format audit report.
---

# Google Doc Format Skill

Create professionally formatted Google Docs from markdown using `gog docs create --file`. The key insight: markdown tables and formatting render properly as native Google Docs elements when passed through the `--file` flag.

## Core Method

Always use `gog docs create` with `--file` to import markdown. Never use `gog docs write` or `gog docs insert` for full documents — those don't parse markdown tables.

```bash
gog docs create "Doc Title" --file source.md --parent "FOLDER_ID" --pageless --force --no-input
```

Flags:
- `--file` — Import markdown file (required for proper table rendering)
- `--parent` — Google Drive folder ID
- `--pageless` — Use pageless layout (recommended for reports/audits)
- `--force` — Skip confirmations

## Markdown → Google Docs Mapping

| Markdown | Google Docs Element |
|----------|-------------------|
| `# Heading 1` | HEADING_1 |
| `## Heading 2` | HEADING_2 |
| `### Heading 3` | HEADING_3 |
| `**bold text**` | Bold text |
| `*italic text*` | Italic text |
| `- item` or `* item` | Bullet list |
| `1. item` | Numbered list |
| `\| col1 \| col2 \|` | Native TABLE element |
| `[link text](url)` | Clickable hyperlink |
| `---` | Horizontal rule |
| `> blockquote` | Indented text |

## Table Formatting Rules

Markdown pipe tables render as **native Google Docs tables** — this is the main value of this skill. Tables are the element most likely to break when creating docs any other way.

**Correct format:**
```markdown
| # | Document | Link |
|---|----------|------|
| 01 | Technical SEO Audit | [Open doc](https://docs.google.com/document/d/DOC_ID/edit) |
| 02 | On-Page SEO Audit | [Open doc](https://docs.google.com/document/d/DOC_ID/edit) |
```

**What NOT to do:**
- ❌ Tab-separated values (no `\t` between columns)
- ❌ Plain text pretending to be a table
- ❌ Using `gog docs write` with raw text (doesn't parse markdown)
- ❌ Putting tables inside code blocks (won't render as tables)

## Document Templates

### Master Index / Link Index Doc

```markdown
# Project Name — Deliverables Master Index

*Last updated: DATE*

---

## 📋 Section Name

### Subsection

| # | Document | Link |
|---|----------|------|
| 01 | Document Name | [Open doc](https://docs.google.com/document/d/DOC_ID/edit) |
| 02 | Document Name | [Open doc](https://docs.google.com/document/d/DOC_ID/edit) |

---

## 🎨 Another Section

### Subsection

| # | Document | Link |
|---|----------|------|
| 01 | Document Name | [Open doc](https://docs.google.com/document/d/DOC_ID/edit) |

---

## 📂 Folder Structure

- **Root:** Folder Name
  - **Subfolder**
    - Document 1
    - Document 2
```

### Audit/Report Doc

```markdown
# Report Title: Descriptive Subtitle

**URL:** /page-slug/
**Target Keywords:** keyword1, keyword2, keyword3
**Meta Title:** SEO Title (60 chars)
**Meta Description:** Meta description (155 chars)

---

## Section Heading

Body paragraph with **bold key terms** and normal text.

### Subsection

| Metric | 2024 | 2023 | Change |
|--------|------|------|--------|
| Value 1 | 232 | 274 | -15% |

**Key takeaway:** Summary sentence after the table.

### Another Subsection

- **Bold label** — Description text
- **Bold label** — Description text
```

## Workflow

1. **Write markdown to temp file** — `cat > /tmp/doc_name.md << 'EOF'`
2. **Create doc** — `gog docs create "Title" --file /tmp/doc_name.md --parent FOLDER_ID --pageless --force --no-input`
3. **Verify structure** — `gog docs structure DOC_ID --no-input | grep -i table`
4. **Verify content** — `gog docs cat DOC_ID --no-input | head -20`

## Verification Checklist

After creating, verify:
- [ ] `gog docs structure` shows TABLE elements (not just NORMAL_TEXT with pipe characters)
- [ ] Table row counts match expected dimensions (e.g., `[table 6x3]`)
- [ ] Links are clickable: `[Open doc](url)` renders as hyperlinks
- [ ] Heading hierarchy is correct (H1 > H2 > H3)
- [ ] Bold text renders (check structure output for inline formatting)

## Replacing an Existing Doc

To replace a badly formatted doc:
1. Create new doc with `--file` flag
2. Verify formatting on the new doc
3. Rename new doc to match old name: `gog drive rename NEW_ID "Original Name" --force --no-input`
4. Delete old doc: `gog drive delete OLD_ID --force --no-input`
5. Move new doc to correct folder if needed: `gog drive move NEW_ID --parent FOLDER_ID --force --no-input`

## Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| Tables show as pipe-separated text | Used `gog docs write` instead of `--file` | Recreate with `gog docs create --file` |
| Links not clickable | Used plain URLs, not markdown link syntax | Use `[text](url)` format |
| No headings | Used underline-style headings | Use `#` prefix headings |
| Missing bold | Used HTML `<b>` tags | Use `**text**` markdown |
| Rate limit (429) | Too many API calls in short time | Add `sleep 3` between operations |

## Rate Limiting

Google Docs API has per-minute write quotas. When creating multiple docs:
- Add `sleep 3` between create operations
- If you get 429 errors, wait 60 seconds and retry
- For large batches (5+ docs), add `sleep 5` between each

## Getting Doc IDs for Link Tables

To build a link index:
1. List folder contents: `gog drive ls --parent FOLDER_ID --json --no-input`
2. Extract IDs and names with: `python3 -c "import json,sys; data=json.load(sys.stdin); [print(f'{f[\"name\"]} | {f[\"id\"]}') for f in data.get('files',[])]"`
3. Build Google Doc URLs: `https://docs.google.com/document/d/DOC_ID/edit`