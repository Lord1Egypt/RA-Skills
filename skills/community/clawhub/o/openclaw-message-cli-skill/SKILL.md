---
name: openclaw-message-cli-skill
description: Use when the user explicitly wants to send outbound messages with the OpenClaw CLI rather than built-in tools, especially for `openclaw message send` commands with a specific channel, target, and message body.
---

# OpenClaw Message CLI Skill

Use this skill when the task is specifically about sending a message with the OpenClaw CLI.

Prefer the built-in messaging tool when available. Use this skill only when the user explicitly asks for CLI usage, shell commands, scripting, or automation around `openclaw message send`.

## Command Pattern

Use:

```bash
openclaw message send --channel <channel> --target <target> --message "..."
```

## Examples

```bash
openclaw message send --channel whatsapp --target <target> --message "hi"
openclaw message send --channel telegram --target <target> --message "hi"
```

## Checks

- verify the requested channel exists before sending
- verify the target format matches the selected channel
- quote message text safely, especially when it contains shell-sensitive characters

## Scope

Use this skill for direct outbound client delivery with the OpenClaw CLI.
Do not use it for normal agent replies inside the current session.
