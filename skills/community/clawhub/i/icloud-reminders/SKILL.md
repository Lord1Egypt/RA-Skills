---
name: icloud-reminders
description: Manage Apple iCloud Reminders via CloudKit API. Use for listing, adding, completing, deleting reminders, managing lists, and hierarchical subtasks. Works with 2FA-protected accounts via cached sessions.
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - reminders
    install:
      - kind: brew
        tap: tarekbecker/tap
        formula: icloud-reminders
        bins: [reminders]
    emoji: "✅"
    homepage: https://github.com/tarekbecker/icloud-reminders-cli
---

# iCloud Reminders

Access and manage Apple iCloud Reminders via CloudKit API. Full CRUD with hierarchical subtask support.

**Pure Go — no Python or pyicloud required.** Authentication, 2FA, session management and CloudKit API calls are all implemented natively in Go.

## Installation

### Homebrew (Recommended)

```bash
brew tap tarekbecker/tap
brew install icloud-reminders
```

Upgrade to the latest version:
```bash
brew upgrade icloud-reminders
```

## Setup

1. **Authenticate** (interactive — required on first run):
   ```bash
   reminders auth
   ```

   Credentials are resolved in this order:
   1. `ICLOUD_USERNAME` / `ICLOUD_PASSWORD` environment variables
   2. `~/.config/icloud-reminders/credentials` file (export KEY=value format)
   3. Interactive prompt (fallback)

2. **Session file** (`~/.config/icloud-reminders/session.json`) is created automatically and reused. Run `reminders auth` again when the session expires.

## Commands

```bash
# First-time setup / force re-auth
reminders auth
reminders auth --force

# List all active reminders (hierarchical)
reminders list

# Filter by list name
reminders list -l "🛒 Groceries"

# Include completed
reminders list --all          # or: -a

# Show only children of a parent reminder (by name or short ID)
reminders list --parent "Supermarket"
reminders list --parent ABC123DE

# Search by title
reminders search "milk"

# Search including completed
reminders search "milk" --all   # or: -a

# Show all lists (with active counts and short IDs)
reminders lists

# Add reminder (-l is REQUIRED)
reminders add "Buy milk" -l "Groceries"

# Add with due date and priority
reminders add "Call mom" -l "Groceries" --due 2026-02-25 --priority high

# Add with notes
reminders add "Buy milk" -l "Groceries" --notes "Get the organic 2% stuff"

# Add as subtask (-l is REQUIRED even for subtasks)
reminders add "Butter" -l "🛒 Groceries" --parent ABC123DE

# Add multiple at once (batch; -l is REQUIRED)
reminders add-batch "Butter" "Cheese" "Milch" -l "Groceries"

# Add multiple as subtasks
reminders add-batch "Butter" "Cheese" -l "Groceries" --parent ABC123DE

# Edit a reminder (update title, due date, notes, or priority)
reminders edit abc123 --title "New title"
reminders edit abc123 --due 2026-03-01 --priority high
reminders edit abc123 --notes "Updated notes"
reminders edit abc123 --priority none

# Complete reminder
reminders complete abc123

# Delete reminder
reminders delete abc123

# Export as JSON
reminders json

# Force full resync
reminders sync

# Export session cookies (share without password)
reminders export-session session.tar.gz

# Import session from export
reminders import-session session.tar.gz

# Verbose output (any command)
reminders list -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "not authenticated" | Run `reminders auth` |
| "invalid Apple ID or password" | Check credentials file |
| "2FA failed" | Re-run `auth`, enter a fresh code |
| "Missing change tag" | Run `reminders sync` |
| "List not found" | Check name with `reminders lists` |
| Binary not found | Run `bash scripts/build.sh` or check your PATH |
