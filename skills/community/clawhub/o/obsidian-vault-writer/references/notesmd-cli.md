# notesmd-cli Reference

`notesmd-cli` interacts with Obsidian vaults from the terminal. **Obsidian does not need to be running.** Designed for server, VPS, and headless environments.

Source: https://github.com/Yakitrak/notesmd-cli

---

## Install

**macOS / Linux (Homebrew):**
```bash
brew tap yakitrak/yakitrak
brew install yakitrak/yakitrak/notesmd-cli
```

**Build from source (Go 1.19+):**
```bash
git clone https://github.com/yakitrak/notesmd-cli.git
cd notesmd-cli
go build -o notesmd-cli .
sudo install -m 755 notesmd-cli /usr/local/bin/
```

**Verify:**
```bash
notesmd-cli --version
```

---

## Vault Management

```bash
# Register a vault (headless / no Obsidian installed)
notesmd-cli add-vault /path/to/vault
notesmd-cli add-vault /path/to/vault --set-default

# List vaults (default marked)
notesmd-cli list-vaults
notesmd-cli list-vaults --default --path-only   # just the default vault path

# Set default vault
notesmd-cli set-default-vault "{vault-name}"

# Remove a vault registration (does not delete files)
notesmd-cli remove-vault "{vault-name}"
```

---

## Daily Note

Reads `.obsidian/daily-notes.json` for folder, date format, and template automatically.

```bash
notesmd-cli daily
notesmd-cli daily --content "text to append"
notesmd-cli daily --vault "{vault-name}"
notesmd-cli daily --content "text" --vault "{vault-name}"
```

---

## Create / Update Note

```bash
# Create (leaves existing note unchanged if no flag)
notesmd-cli create "{note-path}" --content "..."

# Append to existing note
notesmd-cli create "{note-path}" --content "..." --append

# Overwrite existing note
notesmd-cli create "{note-path}" --content "..." --overwrite

# Target a specific vault
notesmd-cli create "{note-path}" --content "..." --vault "{vault-name}"
```

Intermediate directories are created automatically. If `{note-path}` has no `/`, the vault's configured default folder is used.

---

## Read / Print Note

```bash
notesmd-cli print "{note-name}"
notesmd-cli print "{note-path}"
notesmd-cli print "{note-name}" --vault "{vault-name}"
```

---

## Search

```bash
# Fuzzy search by note name (interactive)
notesmd-cli search --vault "{vault-name}"

# Search note content (non-interactive, for scripting)
notesmd-cli search-content "term" --no-interactive
notesmd-cli search-content "term" --format json
notesmd-cli search-content "term" --format json --vault "{vault-name}"
```

---

## List, Move, Delete

```bash
# List vault contents
notesmd-cli list
notesmd-cli list "folder/subfolder"

# Move / rename (also updates internal links)
notesmd-cli move "{current-path}" "{new-path}"
notesmd-cli move "{current-path}" "{new-path}" --vault "{vault-name}"

# Delete
notesmd-cli delete "{note-path}"
notesmd-cli delete "{note-path}" --vault "{vault-name}"
```

---

## Frontmatter

```bash
# Print frontmatter
notesmd-cli frontmatter "{note-name}" --print

# Edit a field (creates if absent)
notesmd-cli frontmatter "{note-name}" --edit --key "status" --value "done"

# Delete a field
notesmd-cli frontmatter "{note-name}" --delete --key "draft"

# Target a specific vault
notesmd-cli frontmatter "{note-name}" --print --vault "{vault-name}"
```
