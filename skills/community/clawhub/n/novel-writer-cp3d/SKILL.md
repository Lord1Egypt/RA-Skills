---
name: novel-writing-assistant
description: Comprehensive novel writing assistant for creating, managing, and formatting novels. Use when the user needs help with (1) writing novel chapters, (2) managing novel structure and consistency, (3) checking chapter formatting, (4) continuing existing storylines, (5) converting novel formats (markdown to txt/epub/pdf), (6) managing characters and plot arcs, or any other novel writing tasks.
---

# Novel Writing Assistant

This skill helps with all aspects of novel writing, from creating new chapters to managing complex storylines and characters.

## Core Capabilities

### 1. Chapter Writing

When writing new chapters:
- Read existing chapters to understand the story context
- Maintain consistent tone, style, and character voices
- Follow the established chapter format (title, author, date, content sections)
- Use proper paragraph breaks and dialogue formatting
- Save chapters in the designated folder with consistent naming

### 2. Format Management

Standard chapter format:
```
# XX-第X章 章节标题.md

## 第X章：章节标题

## 作者：作者名

## 日期：YYYY年MM月DD日

## 日期说明（可选）

---

正文内容，使用正确的段落和对话格式

---

**第X天/章，结束。**

**关键信息总结**
**但……**

**后续预告/思考**
```

### 3. Format Checking

Check chapters for:
- Consistent frontmatter (title, author, date)
- Proper paragraph breaks (not too long or too short)
- Correct dialogue formatting
- Consistent section separators
- Missing or inconsistent information

### 4. Novel Continuation

When continuing a novel:
- Review the last 2-3 chapters for context
- Check the story's current status and unresolved plot points
- Maintain character consistency
- Advance the plot logically
- Match the existing writing style

### 5. Format Conversion

Convert novels between formats:
- Markdown → TXT (plain text)
- Markdown → EPUB (e-book)
- Markdown → PDF (document)

Use scripts in `scripts/` folder for conversions.

### 6. Character & Plot Management

Track and manage:
- Character profiles and development
- Plot arcs and storylines
- Timeline consistency
- World-building details

Store this information in `references/characters.md` and `references/plot.md`.

## File Organization

Standard novel folder structure:
```
NovelName/
├── 00-简介.md
├── 01-第一章 标题.md
├── 02-第二章 标题.md
├── ...
├── characters.md (character profiles)
├── plot.md (plot outline)
└── NovelName.txt (compiled text version)
```

## Best Practices

1. **Always read context** - Before writing, read existing chapters
2. **Maintain consistency** - Keep tone, style, and details consistent
3. **Use proper formatting** - Follow the established chapter format
4. **Save incrementally** - Save work frequently to avoid loss
5. **Check before converting** - Verify formatting before format conversion
6. **Track changes** - Keep notes on what was changed and why

## Available Scripts

- `scripts/md_to_txt.py` - Convert markdown chapters to plain text
- `scripts/check_format.py` - Check chapter formatting consistency
- `scripts/compile_novel.py` - Compile all chapters into single file

## Reference Files

- `references/characters.md` - Character profiles and tracking
- `references/plot.md` - Plot outline and story arcs
- `references/writing_guide.md` - Writing style and conventions

## Usage Examples

**Write a new chapter:**
"帮我写小说《觉醒之鬼》第二十五章，承接第二十四章的剧情"

**Check formatting:**
"检查一下小说所有章节的格式是否一致"

**Convert format:**
"把小说转换成txt格式"

**Continue story:**
"继续写下一章，主角遇到了新的挑战"

**Manage characters:**
"更新角色信息，添加新角色"
