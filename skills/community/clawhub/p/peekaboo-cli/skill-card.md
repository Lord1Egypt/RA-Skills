## Description:

macOS UI automation CLI tool for screen capture, window control, element clicking, text input, UI testing, screen capture, window management, and app control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryso](https://clawhub.ai/user/terryso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and automation-focused agent users use this skill to operate macOS applications through Peekaboo CLI commands for UI capture, window management, element interaction, text entry, menu navigation, clipboard workflows, and scripted desktop tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture screen contents and UI metadata from live macOS apps and windows.

Mitigation: Use it only with trusted apps and windows, avoid sensitive screens, and verify Screen Recording and Accessibility permissions before command execution.

Risk: The skill can control live applications through clicks, typing, hotkeys, menus, clipboard changes, and scripted flows.

Mitigation: Review commands before execution, prefer dry runs for agent or script workflows, and scope commands to specific apps, windows, or elements whenever possible.

Risk: Credentials or sensitive text could be exposed through command arguments, clipboard operations, captured screenshots, or generated command output.

Mitigation: Do not pass real passwords or API keys on the command line, avoid sensitive screens during capture, and limit clipboard and paste operations to intended data.

Risk: Long-running daemon, MCP server, or autonomous agent workflows can continue exposing desktop automation capability after the immediate task.

Mitigation: Use trusted tasks and bounded settings, cap or dry-run agent workflows where appropriate, and stop daemon or MCP server processes when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terryso/skills/peekaboo-cli)
- [Peekaboo CLI installation](https://github.com/steipete/Peekaboo#install)
- [UI Capture](references/see.md)
- [Element Click](references/click.md)
- [Text Input](references/type.md)
- [App Management](references/app.md)
- [Window Management](references/window.md)
- [Permissions](references/permissions.md)
- [Autonomous Agent](references/agent.md)
- [MCP Server](references/mcp.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Many Peekaboo commands support --json or --json-output for scripting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
