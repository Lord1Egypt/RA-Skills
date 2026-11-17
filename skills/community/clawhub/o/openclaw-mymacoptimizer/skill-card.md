## Description:

Controls the local My Mac Optimizer macOS application for system monitoring, optimization, junk cleaning, app uninstalling, and large-file cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maximouribarri](https://clawhub.ai/user/maximouribarri)

### License/Terms of Use:


## Use Case:

Mac users and support operators use this skill to ask an agent to inspect system status and invoke local My Mac Optimizer cleanup, optimization, app removal, and file trashing actions after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a local My Mac Optimizer app that exposes the 127.0.0.1:8000 API.

Mitigation: Install and use the skill only when the local My Mac Optimizer app is trusted.

Risk: Cleanup, uninstall, and file-delete actions can remove applications or user files.

Mitigation: Confirm exactly what will be removed before allowing destructive commands to run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maximouribarri/skills/openclaw-mymacoptimizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Destructive cleanup, uninstall, and file deletion actions require user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
