# Markdown to Rich HTML

AI coding workflows often generate long Markdown files for technical plans, design notes, implementation proposals, and review documents. These files are convenient for agents to write, but they are often too long and too flat for humans to read comfortably.

This Codex skill reads and understands the content of a Markdown file or folder, then presents it as an appropriate self-contained HTML page. Instead of mechanically converting Markdown tags to HTML tags, it chooses a layout and visual structure that fit the document's purpose, making the result easier to scan, compare, and use.

## Install

Use `$skill-installer` in Codex:

```text
$skill-installer install https://github.com/441126098/md-to-rich-html
```

Restart Codex after installation so the skill can be discovered.

## Usage

```text
Use $md-to-rich-html to convert this Markdown technical plan into a readable HTML page.
```

## License

MIT
