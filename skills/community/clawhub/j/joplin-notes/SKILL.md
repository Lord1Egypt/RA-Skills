---
name: joplin-notes
description: Interface for managing Joplin notes via WebDAV. Allows listing notebooks and notes, reading content (first line = title), and creating or updating notes and notebooks. Use this skill when the user wants to access or modify their Joplin database programmatically.
---

# Joplin Notes Skill

This skill provides programmatic access to a Joplin database synchronized via WebDAV.

## How it Works

Joplin stores notes and notebooks as `.md` files in a flat directory. They are linked via metadata at the end of the file (`id`, `parent_id`, `type_`).
- **Title:** The first line of the file is the title of the note or notebook.
- **Notebook:** A special file type (`type_: 2`) that serves as a container for notes.
- **Note:** A standard file (`type_: 1`) assigned to a notebook via `parent_id`.

## Available Scripts

The scripts are located in `scripts/` and require the following environment variables:
- `JOPLIN_PASSWORD`: The password for WebDAV access.
- `JOPLIN_ACCOUNT`: The username for Joplin (e.g., `openclaw`).
- `JOPLIN_WEBDAV_PATH`: The full path to the Joplin directory on the WebDAV server.

### 1. List Notes (`list_notes.py`)
Outputs the entire structure of notebooks and their contained notes.
- **Usage:** `python3 scripts/list_notes.py`

### 2. Get Note Content (`get_note.py`)
Reads the content of a specific note by its ID.
- **Usage:** `python3 scripts/get_note.py <note_id>`

### 3. Upsert Note/Notebook (`upsert_note.py`)
Updates an existing note or creates a new one. Supports notebooks via the type parameter.
- **Usage:** `python3 scripts/upsert_note.py <note_id|new> <parent_id> <content_file> [type (1=note, 2=notebook)]`

### 4. Create Notebook (`create_notebook.py`)
Creates a new notebook.
- **Usage:** `python3 scripts/create_notebook.py <title> [parent_notebook_id]`

## Workflow Examples

### Query Structure
1. `exec("python3 /home/openclaw/.openclaw/workspace/skills/joplin-notes/scripts/list_notes.py")`
2. Analyze the output to find the desired `note_id` or `notebook_id`.

### Read Note Content
1. `exec("python3 /home/openclaw/.openclaw/workspace/skills/joplin-notes/scripts/get_note.py <note_id>")`

### Edit or Create Note
1. Download the current content with `get_note.py` (if editing).
2. Create a temporary file with the new content (include the title in the first line).
3. Call `upsert_note.py`.
