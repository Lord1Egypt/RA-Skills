---
name: kindle2md
description: Convert Kindle HTML notebook exports to Obsidian Markdown format. Use this when the user wants to convert a Kindle book notes HTML file (exported from the Kindle app) into a Markdown file suitable for Obsidian. Trigger when user mentions "kindle", "读书笔记", "Kindle笔记", "笔记本.html", or wants to convert book highlights to markdown.
---

# Kindle to Markdown

Use this skill to convert Kindle HTML notebook exports to Obsidian Markdown format.

## Setup (First Time Only)

Before using, configure the output directory by editing `references/config.md`.

**Read `references/config.md`** to get the `output_dir` value. If the value is still "CHANGE_TO_YOUR_OBSIDIAN_BOOKS_PATH", remind the user to configure it first.

## Input

The user will provide an HTML file path, for example:
- `/kindle2md "下载/动物农场.html"`
- `/kindle2md "C:/Users/Downloads/动物农场 (Z-Library) - 笔记本.html"`

Extract the book title from the HTML filename:
- Remove path and extension
- Remove metadata like "[英]作者", "(Z-Library)", " - 笔记本"

## Output

**Output directory**: Read from `references/config.md` → `output_dir`

**Output filename**: `{书名}.md`

Example: for input file `动物农场 ([英]乔治·奥威尔) (Z-Library) - 笔记本.html`, output should be `动物农场.md`

If file already exists, overwrite it.

## Runtime

Run the conversion script from the scripts folder:

```bash
python "<skill_path>/scripts/kindle_notes_to_md.py" --override -o "<output_dir>/<书名>.md" "<用户提供的HTML路径>"
```

Where:
- `<skill_path>` is the path to this skill folder
- `<output_dir>` is read from `references/config.md`

## Success

Report to the user:
- "转换完成！文件已保存到: {output_path}"

## Errors

If the HTML file doesn't exist or is invalid, report the error to the user clearly.
