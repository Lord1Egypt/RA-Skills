## Description:

Control macOS via CLI using MacPilot for automating UI actions, managing windows, handling file dialogs, capturing screenshots, OCR, and system tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adhikjoshi](https://clawhub.ai/user/adhikjoshi)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to let AI coding agents operate macOS through MacPilot CLI commands for app control, UI inspection, file dialogs, screenshots, OCR, window management, shell tasks, and system workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad macOS automation can control visible apps, run shell commands, read screen contents, and access clipboard history.

Mitigation: Review before installing, prefer manual or version-pinned installation, keep installation project-scoped when possible, and grant Accessibility or Screen Recording only when that level of control is intended.

Risk: Dialog automation can click sensitive actions such as Allow, Confirm, or Replace.

Mitigation: Avoid auto-clicking sensitive dialog actions unless the requested task explicitly requires it and the dialog contents have been verified.

Risk: Screenshot, OCR, and screen recording features may expose visible private or sensitive information.

Mitigation: Grant Screen Recording only for workflows that require visual capture, and limit use to screens and applications appropriate for agent access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adhikjoshi/skills/macpilot)
- [MacPilot repository](https://github.com/adhikjoshi/macpilot)
- [MacPilot releases](https://github.com/adhikjoshi/macpilot/releases)
- [Skills CLI repository](https://github.com/vercel-labs/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MacPilot commands commonly support --json for structured command output.]

## Skill Version(s):

0.7.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
