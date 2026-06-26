---
name: macos-contacts
description: Access and search Apple Contacts on macOS using AppleScript. Use when the user asks to look up a contact, find a phone number or email, search contacts by name, or get details about someone in their address book. macOS only.
---

# Apple Contacts (AppleScript)

Uses `osascript` to query the macOS Contacts app. **macOS only.** Requires Contacts permission on first run — macOS will show a prompt, click Allow.

## Setup

No installation required. Just ensure the skill's `scripts/` directory is intact after installing.

## Usage

```bash
# List all contacts
osascript <skill_dir>/scripts/contacts.applescript list

# Search by name (case-insensitive)
osascript <skill_dir>/scripts/contacts.applescript search "Alice"

# Get full details for a contact
osascript <skill_dir>/scripts/contacts.applescript get "Alice Smith"
```

Replace `<skill_dir>` with the absolute path to this skill's directory (use `pwd` inside the skill folder if unsure).

## Output format

- `list` / `search`: one line per match → `Name | Phone | Email`
- `get`: full details (all phones, emails, birthday, notes), contacts separated by `---`

## Notes

- First run may trigger a macOS Contacts permission dialog — user must click Allow
- If no contacts found, returns a descriptive message instead of empty output
- Script supports partial name matching (e.g. "Ali" matches "Alice Smith")
