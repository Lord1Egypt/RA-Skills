# Markdown to Word Example

This is a sample document to verify the `markdown-to-word` skill.

## Features

- Supports Markdown file input
- Supports Markdown string input
- Supports custom `reference.docx` templates
- Built-in multiple style templates

## Table

| Template | Style | Use Case |
| --- | --- | --- |
| modern-blue | Clear & Professional | Reports, Proposals, Weekly updates |
| executive-serif | Formal & Steady | Proposals, Contract attachments, Memos |
| warm-notebook | Soft Editorial | Articles, Sharing notes, Reading notes |
| minimal-gray | Restrained & Simple | Tech docs, Internal guides |

## Code

```bash
python3 scripts/markdown_to_docx.py \
  --input-file sample.md \
  --output sample.docx \
  --builtin-template modern-blue \
  --toc
```
