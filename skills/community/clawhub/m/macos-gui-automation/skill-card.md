## Description:

Automates macOS GUI tasks through screen capture, OCR text reading, mouse and keyboard control, window management, and app launching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhdragon](https://clawhub.ai/user/dhdragon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let an agent inspect visible macOS UI state and issue bounded mouse, keyboard, window, and app-control commands during desktop automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen reading and GUI input control can expose sensitive content or trigger unintended actions.

Mitigation: Use only on bounded, non-sensitive tasks; avoid passwords, messages, financial pages, and admin prompts; review each request before allowing clicks, typing, or app control.

Risk: Temporary screenshots used for OCR can persist on disk after the task.

Mitigation: Delete temporary screenshots after use and avoid capturing sensitive screens.

Risk: Absolute coordinates and OCR limitations can target the wrong UI element.

Mitigation: Verify screen state and coordinates before actions, prefer limited screenshot regions, and use small reversible steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dhdragon/skills/macos-gui-automation)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coordinate-based GUI actions, OCR output, and temporary screenshot paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
