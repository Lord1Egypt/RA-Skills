## Description:

Control macOS GUI apps visually by taking screenshots, clicking, scrolling, and typing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kekejun](https://clawhub.ai/user/kekejun)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to let an AI agent inspect and operate visible macOS desktop applications through a screenshot, OCR, action, and verification loop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read the screen and control mouse and keyboard input across macOS applications once permissions are granted.

Mitigation: Grant Screen Recording and Accessibility only to a trusted host process, keep sensitive windows closed, and require explicit approval before send, purchase, delete, settings, account, or financial actions.

Risk: Screenshots and OCR element maps are written to shared /tmp paths.

Mitigation: Avoid displaying secrets while using the skill and clear temporary files after sessions that may expose sensitive information.

Risk: The documented install command includes system-wide pip installation guidance.

Mitigation: Prefer a virtual environment for dependency installation.

Risk: The type command uses the system clipboard to paste text.

Mitigation: Do not use the skill to type passwords, secrets, or other confidential values.

## Reference(s):

- [mac-use ClawHub page](https://clawhub.ai/kekejun/skills/mac-use)
- [kekejun ClawHub publisher profile](https://clawhub.ai/user/kekejun)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper writes screenshots and OCR element maps to shared /tmp paths for agent inspection.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
