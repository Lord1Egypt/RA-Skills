## Description:

Capture macOS screenshots for the whole screen, a specific app window, or a precisely targeted desktop window using built-in system tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mallocfeng](https://clawhub.ai/user/mallocfeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill on macOS to capture full-screen screenshots or targeted app/window screenshots, save them in the workspace, and return local paths unless the user explicitly requests chat delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic keyword matching can capture the wrong visible window.

Mitigation: List candidate matches first and select an explicit match with --index when multiple windows could match.

Risk: Screenshots can contain confidential on-screen information.

Mitigation: Save screenshots locally by default, inspect saved files before sharing, and attach them to chat only when the user explicitly requests it.

Risk: Granting macOS Screen Recording access expands what the host process can observe.

Mitigation: Review the skill before installation and grant Screen Recording permission only to the intended host process when screenshots are needed.

## Reference(s):

- [Success Notes](references/success-notes.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with inline shell commands and local PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS with swift, screencapture, and python3; screenshot images are saved locally by default.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
