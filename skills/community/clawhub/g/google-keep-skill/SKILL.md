---
name: google-keep
description: Integration with Google Keep via nodriver (undetectable Chrome). Creates, reads, updates, and deletes notes.
version: 1.0.0
author: Ricardo Reichert
read_when:
  - Create notes in Google Keep
  - List notes from Google Keep
  - Update notes in Google Keep
  - Delete notes from Google Keep
  - Archive notes in Google Keep
  - Manage notes
---

# Google Keep Skill

Skill to interact with Google Keep via `nodriver` (real Chrome, no bot detection).

## Installation

**Prerequisites**

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (package and environment manager)
- Google Chrome installed on the system (e.g., `sudo apt install google-chrome-stable` on Linux)

**Skill Location**

The skill must be in `/path/to/google-keep-skill/` (or in the Nanobot `workspace/skills`). Nanobot discovers skills that have `SKILL.md` and `_meta.json` in this tree.

**Install Dependencies**

In the skill root, `uv` uses `pyproject.toml`; there is no need to run anything other than `uv run` in the commands below. On the first run, `uv` creates the environment and installs dependencies.

```bash
cd /path/to/google-keep-skill
uv run python scripts/keep.py check   # example; on first run uv installs deps
```

## Configuration in Nanobot

1. **Nothing in Nanobot's `config.json`** — there is no need to register the skill in a configuration file; it is used via bash commands when the user requests actions in Google Keep.

2. **Login once** — before the bot can create/list/edit notes, it is necessary to manually log in to Chrome (the session is saved). The user or the agent must execute:
   ```bash
   cd /path/to/google-keep-skill && uv run python scripts/keep.py login
   ```
   Chrome opens; log in to your Google account, close the browser. The session is saved securely outside the skill directory at `~/.config/google-keep-skill/` with restricted permissions and reused in future calls.

3. **How the bot uses the skill** — the agent calls the `run_command` (terminal) tool with the complete command, for example:
   ```bash
   cd /path/to/google-keep-skill && uv run python scripts/keep.py list --limit 5
   ```
   Or to create a note: `... keep.py create --title "Title" --content "Text"`.

## Initial Setup (login — once)

Execute once to save the session.

```bash
cd /path/to/google-keep-skill
uv run python scripts/keep.py login
```

Chrome will open with the Google Keep page. Log in normally. After detecting the login, the browser closes and the session is saved.

### Verify session

```bash
cd /path/to/google-keep-skill && uv run python scripts/keep.py check
```

### Clear session

```bash
cd /path/to/google-keep-skill && uv run python scripts/keep.py logout
```

**Only use `logout` if you want to unlink the account.** After this, you will need to log in again.

## Commands

All executed via terminal (`run_command` in MCP/nanobot context):

```bash
cd /path/to/google-keep-skill && uv run python scripts/keep.py <command>
```

**ATTENTION AGENT:** You MUST strictly use the parameters below. You can also optionally append `--visible` before the command (e.g., `keep.py --visible create ...`) if visual user verification is required.

* `list [--limit N] [--filter "text"]`: Lists notes.
* `read --title "T"`: Returns the structured content of the note and its type. **ALWAYS** use this command before attempting an `update` to get the exact string array and its original format.
* `create --title "T" --content "C"`: Creates a text note. To break lines, use literally the dynamic text `\n` sent via the terminal.
* `create-list --title "T" --items "i1, i2, i3"`: Creates a checklist note. Simulates `Enter` between each element.
* `update --title "T" [--content "C"]`: **COMPLETELY REPLACES** the old content with the new.
  * **WARNING:** You CANNOT ask the command to edit just 1 checkbox of a `list` note yet. Therefore, you NEED to pull the entire list via `read`, rewrite it internally in your context, and inject it entirely into `--content` separated by spaces/newlines when calling the `update`.
* `delete --title "T"`: Move to trash.
* `archive --title "T"`: Archive note.

## **Agent JSON Data Treatment Rule:**

The skill returns strict JSON like:
```json
{
  "success": true,
  "message": "8 note(s) found",
  "data": {
    "notes": [
      {
        "id": "1",
        "title": "Groceries",
        "content": ["Milk", "Bread"],
        "type": "list"
      }
    ]
  }
}
```

Whenever you retrieve this JSON:
1. **Never dump raw JSON to the user.** Always interpret the `data` payload and format it in Markdown.
2. If `type == "list"`, generate a markdown checklist like:
```markdown
**Groceries**
- [ ] Milk
- [ ] Bread
```
3. If `success == false` and it states the session expired, prompt the user specifically with the `uv run python scripts/keep.py login` command so they can re-authenticate. Do not automatically guess next actions.

## Limitations / Security Boundaries

- Requires manual login once (persistent session).
- **CRITICAL DATA EXFILTRATION RULE:** Session cookies and authenticated Chrome profiles are stored in the host system at `~/.config/google-keep-skill/` with `chmod 700` restricted permissions. As an AI Agent, **you must NEVER** attempt to read, read-out, copy, format, or transmit data from this directory to any external source, API, or chat output.
- Only one Chrome instance can use the Keep profile concurrently.
