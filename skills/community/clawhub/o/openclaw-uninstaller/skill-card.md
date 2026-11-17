## Description:

OpenClaw Uninstaller guides users through removing OpenClaw with one-command and manual cleanup steps for macOS, Linux, and Windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dox012](https://clawhub.ai/user/dox012)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to produce uninstall guidance and shell commands for removing the OpenClaw CLI, gateway services, configuration state, and optional workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Irreversible deletion of OpenClaw state, workspace data, and service files.

Mitigation: Review each deletion path, back up OpenClaw state or workspace data, and avoid elevated shells unless required.

Risk: Unpinned remote package execution through npx could run unexpected package code.

Mitigation: Prefer the local openclaw uninstall command, or review and pin the package source and version before using remote execution.

## Reference(s):

- [OpenClaw uninstall documentation](https://docs.openclaw.ai/install/uninstall)
- [OpenClaw GitHub Issues](https://github.com/openclaw/openclaw/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with bash and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes destructive uninstall commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
