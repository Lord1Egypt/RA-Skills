---
name: obsidian-cli-tool
description: Interact with Obsidian vaults using the Obsidian CLI to read, create, search, and manage notes, tasks, properties, and more. Also supports plugin and theme development with commands to reload plugins, run JavaScript, capture errors, take screenshots, and inspect the DOM. Use when the user asks to interact with their Obsidian vault, manage notes, search vault content, perform vault operations from the command line, or develop and debug Obsidian plugins and themes.
---

# Obsidian CLI

Use the `obsidian` CLI to interact with a running Obsidian instance. Requires Obsidian to be open.

## Command reference

### Vault operations
- `obsidian list vaults` — List all vaults
- `obsidian open <vault>` — Open a vault by name
- `obsidian open <note>` — Open a note in the default vault
- `obsidian search "query"` — Fuzzy search for notes
- `obsidian search-content "term"` — Search within note contents

### Note operations
- `obsidian create --name "Title" --content "Body text"` — Create a new note
- `obsidian print <note>` — Print note contents
- `obsidian move <source> <target>` — Move or rename a note
- `obsidian delete <note>` — Delete a note
- `obsidian daily` — Open or create today's daily note

### Properties (frontmatter)
- `obsidian frontmatter get <note> <key>` — Get a property value
- `obsidian frontmatter set <note> <key> <value>` — Set a property value
- `obsidian frontmatter remove <note> <key>` — Remove a property

### Plugin development
- `obsidian plugin reload` — Reload the current plugin
- `obsidian plugin eval '<code>'` — Run JavaScript in Obsidian
- `obsidian plugin screenshot` — Take a screenshot of Obsidian
- `obsidian plugin dom` — Inspect the DOM structure

## Usage examples

```bash
# Create a note
obsidian create --name "Meeting Notes" --content "# Standup\n\n- Task A done\n- Task B in progress"

# Search for a note
obsidian search "project roadmap"

# Read a note
obsidian print "Projects/Website Redesign"

# Update frontmatter
obsidian frontmatter set "Todo List" status "in-progress"

# Open daily note
obsidian daily
```

## Requirements

- Obsidian must be running
- The Obsidian CLI plugin must be installed and enabled
- For plugin development commands, the workspace must be an Obsidian plugin project
