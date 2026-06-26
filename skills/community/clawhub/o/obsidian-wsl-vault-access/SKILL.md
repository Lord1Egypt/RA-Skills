---
name: obsidian-wsl-vault
description: Work with an Obsidian vault stored on Windows and accessed from WSL. Read, search, create, and edit markdown notes directly through mounted paths such as /mnt/c, /mnt/d, or other /mnt/<drive> locations. Use when the user wants note operations against a Windows-hosted Obsidian vault from WSL.
---

# Obsidian Vault (WSL)

Use this skill when the vault lives on Windows but is being accessed from WSL through `/mnt/<drive>`.

## Workflow

1. Identify the vault root from the user-provided path before doing broad searches or edits.
2. Operate on the filesystem path directly; Obsidian does not require a special API for normal note work.
3. Preserve existing frontmatter, wiki-links, embeds, headings, and folder structure unless the user asks to change them.

## Vault Location

Do not assume a fixed vault path.

Common patterns:

- Windows: `C:\Users\<user>\Documents\<vault>\`
- Windows: `D:\Notes\<vault>\`
- WSL: `/mnt/c/Users/<user>/Documents/<vault>/`
- WSL: `/mnt/d/Notes/<vault>/`

Treat the vault root as the directory containing the Obsidian note tree.

## Path Translation

```text
Windows -> WSL: C:\path\to\file -> /mnt/c/path/to/file
Windows -> WSL: D:\path\to\file -> /mnt/d/path/to/file
WSL -> Windows: /mnt/c/path     -> C:/path
WSL -> Windows: /mnt/d/path     -> D:/path
```

Replace backslashes with forward slashes and lowercase the drive letter under `/mnt/<drive>`.

## Common Operations

### Read a note

```bash
cat "/mnt/<drive>/<vault>/<path>/<filename>.md"
```

### Search the vault

Prefer `rg` for speed:

```bash
rg "search term" "/mnt/<drive>/<vault>/"
```

### Edit a note

Edit the markdown file in place with targeted changes instead of rewriting the whole note when possible.

### Create a new note

Use a minimal template when metadata is needed:

```markdown
---
title: Note Title
tags: []
---

# Note Title
```

## Obsidian Conventions

- Notes are markdown files ending in `.md`
- YAML frontmatter is commonly used for metadata such as `title`, `tags`, and `aliases`
- Internal links use `[[Note Name]]`
- Embeds use `![[Note Name]]`
- Callouts use `> [!type]`

## Working Rules

- Confirm the vault root before making broad searches or bulk changes
- Prefer targeted edits over full-file rewrites
- Keep filenames, wiki-links, and folder structure consistent with the existing vault
