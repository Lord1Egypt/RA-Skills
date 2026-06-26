name: northbase
description: Tool for reading and writing persistent notes and workspace files via the Northbase CLI. Use when the user explicitly asks to read, write, list, or sync their stored notes or workspace files. Examples: "Open my ideas note", "Update tasks/today.md", "Add this idea to my notes", "List my files". Do NOT use automatically — only when the user requests file interaction.
---

# System Context

Northbase is part of a system that includes:

- a mobile application used by the user
- the Northbase CLI used by local agents
- a remote storage service that synchronizes files

The mobile app and CLI both interact with the same workspace files.  
Agents use the CLI so that all file operations go through a consistent interface with proper caching and synchronization.

# Requirements

This skill requires the `northbase` CLI to already be installed and available on the system.

Verify installation with:

northbase --help

If the CLI is unavailable, tell the user that Northbase must be installed before this skill can be used.

---

# Northbase Skill

Northbase provides a command-line interface for accessing persistent notes and workspace files that are shared between the user, the mobile app, and the agent. These files are stored remotely but mirrored locally through the Northbase CLI.

This skill allows the agent to read, write, list, and sync those files when the user explicitly asks for it or clearly intends to interact with their notes or stored workspace content.

Northbase should **not** be used automatically or implicitly. Only use it when the user explicitly asks to interact with their files or notes.

---

# Capabilities

Northbase can:

- List available files
- Read file contents
- Create or update files
- Sync the local mirror with the server

All file interactions must be performed through the `northbase` CLI.

---

# When to Use Northbase

Use Northbase only when the user:

- asks to read or open a note
- references a specific file (e.g. `ideas.md`)
- asks to view their stored notes
- asks to update or create a file
- asks to add content to their notes
- asks to list files
- asks to sync their workspace
- explicitly asks you to use Northbase

Examples:

- "Open my ideas note"
- "Update tasks/today.md"
- "What's in memory/2026-02-23.md?"
- "Add this idea to my notes"
- "List my files"

If the user does **not** ask for file interaction, do **not** use Northbase.

---

# Important Rules

- Always interact with stored notes through the `northbase` CLI.
- Never read `~/.mybot/files` or `~/.northbase/files` directly.
- Never query Supabase or the database directly.
- Never bypass the CLI caching or synchronization logic.
- Treat the local mirror as an implementation detail.

The **northbase CLI is the single source of truth** for interacting with persistent files.

---

# Safety Guidelines

- Do **not overwrite existing files** unless the user clearly intends to replace the entire file.
- When modifying an existing file:
  1. Read it first using `northbase get`
  2. Modify the content
  3. Write the updated content back with `northbase put`

This prevents accidental loss of existing notes.

---

# Commands

## Sync files

Sync the local mirror with the server when freshness is required (for example if the user may have edited files from another device).

Command:
northbase pull

Sync only a specific folder prefix:
northbase pull memory/

---

## List files

List all available files:
northbase list

List files within a folder:
northbase list memory/
northbase list tasks/

---

## Read a file

Retrieve the contents of a file:
northbase get ideas.md
northbase get memory/2026-02-23.md

The contents will be printed to stdout.

---

## Write or update a file

Write content to a file using stdin.

Example:
printf "new idea\n" | northbase put ideas.md

For multi-line content:
cat <<'EOF' | northbase put tasks/today.md
# Today
- [ ] Finish draft
- [ ] Review notes
EOF

---

# Typical Workflow

When interacting with Northbase:

1. Run `northbase pull` if the local mirror may be outdated.
2. Run `northbase list` to discover available files.
3. Run `northbase get <path>` to read a file.
4. Modify the content if needed.
5. Run `northbase put <path>` to update or create the file.

---

# File Path Conventions

Northbase uses path-based folders within file paths.

Examples:
ideas.md
tasks/today.md
memory/2026-02-23.md

Folders are prefixes in the file path rather than separate objects.

---

# Error Handling

If Northbase reports that the user is not logged in:
northbase login

If a file cannot be found:

1. Run `northbase list` to discover available files.
2. If appropriate, create a new file using `northbase put`.

If the `northbase` command is missing, stop and tell the user that the Northbase CLI is not installed on this system.Do not attempt to install it automatically.

---
# Authentication

Northbase requires the user to be logged in.

If the CLI reports that the user is not authenticated, run:

northbase login

---

# Summary

Northbase is a tool for interacting with persistent notes and workspace files shared between the user, the mobile app, and the agent.

Use it **only when the user intends to interact with their stored files**, and always perform file operations through the `northbase` CLI.
