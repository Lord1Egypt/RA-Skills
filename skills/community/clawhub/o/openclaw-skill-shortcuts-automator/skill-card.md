## Description:

Run and manage macOS Shortcuts from OpenClaw by listing shortcuts, executing named shortcuts, viewing details, and signing shortcuts for automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage local macOS Shortcuts from an OpenClaw conversation, including listing available shortcuts, running named shortcuts, inspecting shortcut details, and enabling command-line execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad shortcut triggers and shell-style command examples could lead to unintended or unsafe shortcut execution.

Mitigation: Review this skill before installation, use it only with trusted local shortcuts, and require explicit confirmation before running or signing shortcuts.

Risk: Shortcut names assembled into shell command strings could execute the wrong shortcut or unsafe input.

Mitigation: Validate shortcut names from `shortcuts list` and pass names as separate process arguments.

Risk: macOS Shortcuts can access files, emails, calendar data, other apps, and shell commands with the user's permissions.

Mitigation: Review each shortcut in the Shortcuts app and grant only the macOS Automation, Accessibility, or Full Disk Access permissions needed for the intended workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance, text]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate on local macOS Shortcuts and may return shortcut output as text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
