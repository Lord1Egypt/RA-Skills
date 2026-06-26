---
name: obsidian-vault-writer
description: Use when saving content to an Obsidian vault, appending to daily notes, or writing structured output from another skill into a vault. Designed for VPS and headless server environments using notesmd-cli (no Obsidian desktop app required).
metadata: {
      "openclaw":{
         "emoji":"💎",
         "requires":{
            "bins":["notesmd-cli"]
         },
         "install":[
            {
               "id":"brew",
               "kind":"brew",
               "formula":"yakitrak/yakitrak/notesmd-cli",
               "bins":["notesmd-cli"],
               "label":"Install notesmd-cli (brew)"
            }
         ]
      }
   }
---

# Obsidian Vault Writer

Append and write content to Obsidian vaults using `notesmd-cli`. Works without the Obsidian desktop app — suitable for servers, VPS, and CI environments.

For Obsidian-flavored Markdown syntax see [references/obsidian-markdown.md](references/obsidian-markdown.md). For Canvas files see [references/obsidian-canvas.md](references/obsidian-canvas.md). For Bases files see [references/obsidian-bases.md](references/obsidian-bases.md). For full notesmd-cli command reference see [references/notesmd-cli.md](references/notesmd-cli.md).

---

## Step 1 — Check Vault Setup

```bash
notesmd-cli list-vaults --default --path-only
```

- **Output is a path** → vault is registered; use it for this session.
- **Empty output** → vault is not registered. Suggest a default and ask:
  > "No vault registered. Recommended path: `~/vaults/obsidian`. Use this, or enter a different absolute path?"
  Then register with the confirmed path:

```bash
notesmd-cli add-vault /path/to/vault --set-default
```

Confirm the vault name with:

```bash
notesmd-cli list-vaults --default
```

---

## Step 2 — Append to Daily Note

```bash
notesmd-cli daily --content "<formatted-content>"
```

To target a specific vault by name:

```bash
notesmd-cli daily --content "<formatted-content>" --vault "{vault-name}"
```

`notesmd-cli` reads `.obsidian/daily-notes.json` from the vault automatically for folder, date format, and template. No manual path resolution is needed.

For multiline content, use `\n` for newlines.

---

## Step 3 — Create or Update Notes

```bash
# Create a new note (leaves existing notes unchanged if no flag)
notesmd-cli create "{note-path}" --content "..." --vault "{vault-name}"

# Append to an existing note
notesmd-cli create "{note-path}" --content "..." --append --vault "{vault-name}"

# Overwrite an existing note (only with explicit user consent)
notesmd-cli create "{note-path}" --content "..." --overwrite --vault "{vault-name}"
```

Intermediate directories are created automatically. When `{note-path}` contains no `/`, the vault's configured default folder (from `.obsidian/app.json`) is used; otherwise the path is relative to the vault root.

---

## Safety Rules

- Confirm the vault at least once per session before writing.
- Never write to a vault not confirmed in this session.
- Never overwrite an existing note without explicit user consent.
- Never store vault credentials or sync tokens in the conversation.

---

## Feedback

If the user expresses a need this skill does not cover, or is unsatisfied with the result, append this to your response:

> "This skill may not fully cover your situation. Suggestions for improvement are welcome — [open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues)."

Do not include this message in normal interactions.
