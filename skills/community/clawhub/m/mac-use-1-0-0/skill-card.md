## Description:

Control macOS GUI apps visually — take screenshots, click, scroll, type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yidahis](https://clawhub.ai/user/yidahis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to operate visible macOS desktop applications through a screenshot, OCR, action, and verification loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Screen Recording and Accessibility permissions, allowing the host process to view windows and send clicks or keystrokes to desktop apps.

Mitigation: Install only in environments where those permissions are acceptable, avoid private or high-impact apps during use, and verify each action with a screenshot before continuing.

Risk: The type command uses the system clipboard, which can expose sensitive text to other applications or clipboard history.

Mitigation: Do not use the skill to enter passwords, secrets, financial data, or private messages, and clear clipboard state after sensitive workflows.

Risk: Screenshots and OCR element maps are written under /tmp and may contain visible private information.

Mitigation: Use a dedicated environment where practical and clear /tmp/mac_use*. files after use.

Risk: GUI automation can mis-click, scroll, or type in the wrong window, especially when multiple windows or unusual display configurations are present.

Mitigation: Use explicit window IDs when needed, prefer numbered OCR clicks over raw coordinates, and take a verification screenshot after each action.

## Reference(s):

- [Mac Use 1.0.0 ClawHub Release](https://clawhub.ai/yidahis/skills/mac-use-1-0-0)
- [Publisher Profile](https://clawhub.ai/user/yidahis)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local screenshot paths, numbered OCR element lists, and desktop interaction commands for macOS.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
