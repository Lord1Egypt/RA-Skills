---
name: shortcuts-automator
description: Run and manage macOS Shortcuts directly from OpenClaw. Use when user wants to: (1) Run a specific shortcut by name, (2) List all available shortcuts, (3) View details of a shortcut, (4) Sign/unsign shortcuts for automation, (5) Execute any macOS Shortcut workflow. Triggers include "run shortcut", "execute shortcut", "list shortcuts", "run automation", "show shortcuts", "what shortcuts do I have".
---

# Shortcuts Automator

## Overview

This skill enables OpenClaw to interact with macOS Shortcuts (formerly Automator) directly from conversation. It provides CLI commands to list, run, view, and manage shortcuts.

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

## Commands

### shortcuts list

Lists all shortcuts available in the user's Shortcuts library.

```bash
shortcuts list
```

**Output:** Returns a list of all shortcut names with folder information.

**Use when:** User asks "what shortcuts do I have", "list shortcuts", "show me my shortcuts", "what automations can I run".

### shortcuts run <name>

Runs a shortcut by its exact name. The shortcut must exist in the user's Shortcuts folder.

```bash
shortcuts run "Morning Routine"
shortcuts run "Send Email"
```

**Parameters:**
- `<name>`: Exact name of the shortcut (use quotes if name contains spaces)

**Use when:** User says "run shortcut X", "execute shortcut X", "run automation X", "trigger shortcut X".

**Notes:**
- Some shortcuts require input (text, files, etc.) - will prompt or pass through
- Shortcuts run with user permissions
- Output from the shortcut is returned as text

### shortcuts view <name>

Shows detailed information about a shortcut, including its actions and workflow.

```bash
shortcuts view "Morning Routine"
```

**Output:** Returns the shortcut's description, actions, and workflow steps.

**Use when:** User asks "what does shortcut X do", "show me shortcut X", "view automation X", "tell me about shortcut X".

### shortcuts sign <name>

Signs a shortcut to allow it to run from the command line (required for some automation scenarios).

```bash
shortcuts sign "My Shortcut"
```

**Use when:** Shortcut fails to run with "not signed" error, or user wants to enable CLI execution.

## Error Handling

### "No shortcuts found"

**Cause:** Shortcuts library is empty or inaccessible.

**Solution:** 
- Create shortcuts in the Shortcuts app
- Check Shortcuts app permissions in System Settings > Privacy & Security

### "Shortcut not found" / "Could not find shortcut"

**Cause:** Shortcut name doesn't match exactly or shortcut was deleted.

**Solution:**
- Run `shortcuts list` to see exact names
- Use the exact name including capitalization
- Check if the shortcut is in a specific folder (use folder name: "Folder/Shortcut Name")

### "Not allowed to run" / "Shortcut not signed"

**Cause:** Shortcut needs to be signed for CLI execution.

**Solution:**
```bash
shortcuts sign "Shortcut Name"
```
Or enable in Shortcuts app: Right-click shortcut > Toggle "Allow Running from Command Line"

### "Permission denied" / "Automation access denied"

**Cause:** OpenClaw doesn't have permission to control Shortcuts.

**Solution:**
- Open System Settings > Privacy & Security > Automation
- Enable OpenClaw/your app in the list

### Shortcut hangs or times out

**Cause:** Shortcut may be waiting for input or stuck in a loop.

**Solution:**
- Use `shortcuts view` to inspect the shortcut's actions
- Check if the shortcut requires user interaction
- Add timeout when calling: `timeout 30 shortcuts run "Name"`

## Examples

**User says:** "Run my morning routine shortcut"
```bash
shortcuts run "Morning Routine"
```

**User shortcuts do I have?"
```bash
shortcuts list
```

**User says:** "Show me what the email shortcut does"
```bash
shortcuts view "Send Daily Email"
```

**User says:** "I need to sign a shortcut for automation"
```bash
shortcuts sign "My Automation Shortcut"
```

## Security Considerations

⚠️ **Important:** Shortcuts can execute shell commands, access files, and control other apps.

- **Only run trusted shortcuts** — Review your shortcuts before running them
- Shortcuts have access to your files, emails, calendar, and other data depending on their actions
- Be cautious with shortcuts from unknown sources or those that include shell commands
- Regularly review your shortcuts in the Shortcuts app
- Shortcuts run with your user permissions, so they can access anything you can
