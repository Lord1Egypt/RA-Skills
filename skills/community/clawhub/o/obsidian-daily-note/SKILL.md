---
name: obsidian-daily-note
description: "Write structured entries into an Obsidian daily note vault. Use when the user sends text, links, or content to be recorded, including research notes, task summaries, ideas, URLs, or meeting takeaways. Triggered by phrases like 记一下, 写入笔记, 记录, 帮我记, 写进obsidian, or when the user pastes URLs. On first use, guides setup of the Obsidian vault path."
agent_created: true
---

# Obsidian Daily Note Writer

## Overview

Write user-supplied content into an Obsidian daily note file with consistent
formatting. The skill handles vault path configuration (saved once per user),
file auto-creation, timestamp generation, content prepending (newest first),
and smart URL title extraction.

## Initial Setup

On the very first invocation, the vault path is not yet configured. Resolve
it in this order:

1. **Check config file**: Read `~/.workbuddy/obsidian-daily-note.json`.
   If it contains a `vault_path`, use it. If `daily_notes_subdir` is also
   present, append it to form the full daily notes directory.

2. **Check environment variable**: If no config file exists, check
   `OBSIDIAN_DAILY_VAULT` env var. If set, use it as the vault root
   (daily notes go directly in that directory).

3. **Ask the user**: If neither exists, ask the user once for their Obsidian
   vault path and daily notes subdirectory. Example prompts:
   - "你的 Obsidian Vault 根目录在哪里？（例如 D:\obsidian_华为）"
   - "每日笔记放在 Vault 的哪个子文件夹？（例如 5-每日笔记，如果直接放根目录就留空）"

4. **Save config**: After resolving the path, save it to
   `~/.workbuddy/obsidian-daily-note.json`:
   ```json
   {
     "vault_path": "D:\\obsidian_华为",
     "daily_notes_subdir": "5-每日笔记"
   }
   ```
   This prevents asking again on future invocations.

5. **Proceed**: After setup is complete, continue with the normal workflow
   below.

## Trigger Conditions

**此技能仅在用户明确指定时触发。** 用户必须明确说出类似于以下
的短语，或通过 `@skill:obsidian-daily-note` 显式调用：

- "写入 Obsidian 每日笔记"
- "记到 Obsidian"
- "写进每日笔记"
- "@skill:obsidian-daily-note" 显式技能调用

**注意**：模糊的表述（如"记一下""记录"）**不应**自动触发此技能。
助手**不得**在未收到明确指令的情况下主动写入 Obsidian。

Do NOT activate for conversational remarks, questions, greetings, or
instructions directed at the assistant itself.

## Target Location

- **Config file**: `~/.workbuddy/obsidian-daily-note.json`
- **Daily notes directory**: `{vault_path}/{daily_notes_subdir}/` (or just
  `{vault_path}/` if subdir is empty)
- **File name**: `YYYY-MM-DD.md` (based on current date)
- **Auto-create**: If the file does not exist, create it before writing.
  Create parent directories if needed.

## Format Rules (MANDATORY)

Every entry must follow these rules exactly:

1. **Newest first (prepend)**: New content is always inserted at the **top**
   of the file, before any existing content.

2. **Timestamp**: Each entry starts with `### HH:MM` (24-hour format, current
   time). Use a `###` heading (Obsidian H3) for the timestamp line, followed
   by a space and the user's content on the **same line**.

3. **Content — verbatim only**: Write the user's content **exactly as given**.
   **Never rewrite, summarize, rephrase, elaborate, or add your own
   interpretation.** If the user says "下午预估2年保有量 预估三版本2年规模数据",
   write exactly that. Do not change wording, add context, or restructure.
   The only additions allowed are the `### HH:MM` timestamp and the `---`
   separator.

4. **Bold over headings**: If the user's content contains headings, use
   `**bold**` instead of `#`, `##`, `###`. The timestamp is the only heading.

5. **Entry separator**: If the file already contains previous entries,
   insert a `---` (horizontal rule) on its own line between the new entry
   and the existing content below it.

6. **Trailing newline**: Ensure the file ends with exactly one blank line.

7. **Images**: If the user attaches an image, copy it to
   `{daily_notes_dir}/attachments/` and reference it in the note using
   Obsidian wiki-link syntax: `![[attachments/filename.png]]`.

### Format Example

```
### 14:30 下午预估2年保有量 预估三版本2年规模数据

![[attachments/screenshot.png]]

---

### 12:05 上午做了某件事
```

## URL Handling

When the user provides URLs in their note content:

1. **Attempt title extraction**: Try to fetch the page with WebFetch and
   extract the `<title>` tag.
2. **On success**: Write the extracted title next to the link, e.g.:
   `[页面标题](URL)`
3. **On failure** (internal pages, login walls, timeouts): Keep the link as-is
   along with whatever description the user provided. Do NOT retry or
   over-engineer.
4. **Self-contained note**: Each URL entry should include enough context for
   the user to understand what the link is about later, without relying on
   the page being accessible.

## Workflow

When triggered:

1. **Resolve path**: Read `~/.workbuddy/obsidian-daily-note.json` to get
   the daily notes directory. If not configured, follow the Initial Setup
   steps first.

2. **Determine date**: Get the current date in `YYYY-MM-DD` format.

3. **Check file**: Read `{daily_notes_dir}/{date}.md`. If it doesn't exist,
   create it (can be empty).

4. **Get current time**: Format as `HH:MM` (24-hour).

5. **Build entry block**: Compose `### HH:MM <content>\n` following all
   format rules above.

6. **Handle URLs**: For any URLs in the content, try WebFetch to extract
   the page title. If it fails silently, keep the link + description.

7. **Prepend**: Insert the new entry at the top of the file. If the file
   already has content, add `---\n\n` after the new entry and before the
   existing content.

8. **Present**: Briefly confirm to the user that the note was written,
   showing the entry that was added.
