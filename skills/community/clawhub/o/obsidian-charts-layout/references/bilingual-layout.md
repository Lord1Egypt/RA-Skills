# Bilingual Layout Reference

> Core rules for Chinese-English bilingual Markdown notes in Obsidian → PDF output.
> Used by AI daily report generation agents.

## 1. CN/EN Line Structure

Each info unit = **one bold Chinese line** + next line **italic English**.

```
**中文内容**
*English content*
```

**Strictly prohibited:** Mixing CN/EN on the same line, or using commas/colons to separate CN/EN in the same paragraph.

## 2. Inline Break vs Paragraph

- **Same logical unit** → trailing double-space (renders as `<br>`)
- **Between different units** → blank line (renders as paragraph break)

```
**中文标题**  ← 2 trailing spaces
*English title*  ← 2 trailing spaces
**中文详情**  ← 2 trailing spaces
*English detail*
```

## 3. List Format (Critical)

**? Correct:** Use `- ` lists, group related items inside one `<li>`.
**? Wrong:** Use paragraphs or `---` separators.

```markdown
- **中文项目**  
  *English item*  
  **中文详情**  
  *English detail*
```

## 4. Section Format Spec

| Section | Format |
|---------|--------|
| TL;DR | `> **中文**` + next line `> *English*` (no `[!note]`) |
| Price changes | `> [!info]` callout + list (Obsidian only; strip `[!info]` for PDF) |
| New model release | `**中文**` + `*English*` + `| table |` |
| Hot apps | `- **中文**` + next line `  *English*` |
| Industry news | `- **中文**` + `  *English*` (multi-line inside list) |
| Overseas analysis | Table with `**中文**<br>*English*` |

## 5. Common Pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Using `---` separator for industry items | `<p>` inline flattening | Use `<li>` list format |
| Empty lines inside list | List breaks into independent paragraphs | Remove blank lines, use trailing double-space |
| Obsidian `[!abstract]` callout | PDF renders garbled | Strip `[!something]`, keep `> **Content**` |
| PowerShell HTML Replace for PDF | Tables/lists break | Use Python `markdown` library |
| Inconsistent indentation | List formatting corrupted | Always use 2-space indent |

## 6. PDF Generation Flow

```python
import markdown
html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
# Edge headless print
msedge --headless --print-to-pdf=output.pdf --no-margins input.html
```

## 7. Summary

> **All CN/EN paired content: `- ` list + trailing double-space `<br>`, never paragraphs, separators, or other formats.**
