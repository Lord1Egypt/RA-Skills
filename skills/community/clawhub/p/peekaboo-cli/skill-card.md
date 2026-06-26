## Description: <br>
macOS UI automation CLI tool for screen capture, window control, element clicking, text input, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terryso](https://clawhub.ai/user/terryso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to operate macOS desktop applications through Peekaboo CLI commands for UI testing, screen capture, app control, window management, and scripted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent view and operate a macOS desktop, including screenshots, clicks, typing, app control, and autonomous agent runs. <br>
Mitigation: Require explicit user confirmation before screenshots, external AI analysis, desktop control, app quits, credential entry, daemon/MCP use, or autonomous runs. <br>
Risk: Desktop screenshots, clipboard content, cached snapshots, and provider credentials may expose sensitive information. <br>
Mitigation: Avoid sensitive work during capture, review and clean ~/.peekaboo caches after use, and inspect stored provider credentials after sensitive sessions. <br>
Risk: Commands may change user state through typing, clipboard changes, file moves or deletes, app quits, and window actions. <br>
Mitigation: Prefer dry-run, status, list, and permission-check commands first; confirm destructive or state-changing commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terryso/peekaboo-cli) <br>
- [Peekaboo installation](https://github.com/steipete/Peekaboo#install) <br>
- [UI Capture](references/see.md) <br>
- [Element Click](references/click.md) <br>
- [Text Input](references/type.md) <br>
- [App Management](references/app.md) <br>
- [Window Management](references/window.md) <br>
- [Permissions](references/permissions.md) <br>
- [Autonomous Agent](references/agent.md) <br>
- [MCP Server](references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend JSON-output Peekaboo commands for agent integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
