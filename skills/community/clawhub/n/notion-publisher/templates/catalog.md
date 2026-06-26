---
name: notion-publisher-template-catalog
description: Local article templates for the notion-publisher skill.
---

# Notion Publisher Template Catalog

These templates are original Notion-flavored Markdown layouts bundled with the skill. They are inspired by common public Notion template categories such as blog posts, editorial calendars, knowledge bases, and technical notes, but do not copy third-party template content.

When publishing an article, ask the user to choose one:

| ID | Name | File | Best for |
|---|---|---|---|
| 1 | Clean Essay | `templates/clean-essay.md` | 思考、观点、方法论文章 |
| 2 | Technical Deep Dive | `templates/technical-deep-dive.md` | 工具、代码、架构、实现原理 |
| 3 | Product Update | `templates/product-update.md` | 功能发布、版本更新、项目复盘 |
| 4 | Knowledge Note | `templates/knowledge-note.md` | 学习笔记、概念整理、教程 |
| 5 | Minimal Blog | `templates/minimal-blog.md` | 短文、随笔、轻量记录 |
| 6 | No Template | none | 直接写正文，不套模板 |

Selection guidance:
- For articles about a skill/tool implementation, default to Technical Deep Dive.
- For reflective writing, default to Clean Essay.
- For release notes or project announcements, default to Product Update.
- For tutorials or structured notes, default to Knowledge Note.
- For very short posts, default to Minimal Blog.

Placeholder convention:
- Replace `{{title}}`, `{{summary}}`, `{{intro}}`, `{{body}}`, `{{conclusion}}`, and other placeholders with generated article content.
- Remove any section that is not relevant to the article.
- Keep Notion-flavored Markdown valid: use tabs for child blocks inside callouts, toggles, and columns.
