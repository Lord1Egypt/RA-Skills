# Shortcuts Automator

Run and manage macOS Shortcuts directly from OpenClaw.

## Overview

This skill enables OpenClaw to interact with macOS Shortcuts (formerly Automator) directly from conversation. Use it to list, run, view, and manage your shortcuts.

## Quick Start

```bash
# List all available shortcuts
shortcuts list

# Run a specific shortcut by name
shortcuts run "My Shortcut Name"

# View details of a shortcut
shortcuts view "My Shortcut Name"

# Sign a shortcut for automation (if needed)
shortcuts sign "My Shortcut Name"
```

## Available Commands

### shortcuts list

Lists all shortcuts available in your Shortcuts library.

```bash
shortcuts list
```

**Use when:** "what shortcuts do I have", "list shortcuts", "show me my shortcuts"

---

### shortcuts run \<name\>

Runs a shortcut by its exact name.

```bash
shortcuts run "Morning Routine"
shortcuts run "Send Email"
```

**Parameters:**
- `name` — Exact name of the shortcut (use quotes if the name contains spaces)

**Use when:** "run shortcut X", "execute shortcut X", "run automation X"

**Notes:**
- Some shortcuts require input (text, files, etc.)
- Shortcuts run with your user permissions
- Output from the shortcut is returned as text

---

### shortcuts view \<name\>

Shows detailed information about a shortcut, including its actions and workflow.

```bash
shortcuts view "Morning Routine"
```

**Use when:** "what does shortcut X do", "show me shortcut X", "tell me about shortcut X"

---

### shortcuts sign \<name\>

Signs a shortcut to allow it to run from the command line.

```bash
shortcuts sign "My Shortcut"
```

**Use when:** Shortcut fails to run with "not signed" error.

---

## Examples

```bash
# List all shortcuts
shortcuts list

# Run a specific shortcut
shortcuts run "Morning Routine"

# View what a shortcut does
shortcuts view "Send Daily Email"

# Sign a shortcut for CLI execution
shortcuts sign "My Automation Shortcut"
```

## Security Considerations

⚠️ **Important:** Shortcuts can execute shell commands, access files, and control other apps.

- **Only run trusted shortcuts** — Review your shortcuts before running them
- Shortcuts have access to your files, emails, and other data depending on their actions
- Be cautious with shortcuts from unknown sources
- Regularly review your shortcuts in the Shortcuts app

## macOS Permissions

On first use, macOS may prompt you to grant permissions:

1. **Automation Access:** System Settings → Privacy & Security → Automation → Enable OpenClaw
2. **Accessibility:** If shortcuts interact with other apps, you may need to grant accessibility permissions
3. **Full Disk Access:** Some shortcuts may require this for file operations

If you see "Permission denied" errors, check these settings in **System Settings → Privacy & Security**.

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| "No shortcuts found" | Create shortcuts in the Shortcuts app or check permissions |
| "Shortcut not found" | Use exact name from `shortcuts list` (check capitalization) |
| "Not signed" | Run `shortcuts sign "Name"` |
| "Permission denied" | Enable OpenClaw in System Settings → Privacy & Security → Automation |
