## Description:

Workspace Cleaner helps an OpenClaw agent review and reduce workspace bootstrap files by proposing archive or deletion changes that require user confirmation before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to audit persistent workspace context files, reduce duplicated or stale instructions, archive useful material into memory directories, and delete expired bootstrap files after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite or delete persistent agent control files using broad cleanup criteria.

Mitigation: Require a full proposed diff, backups, and explicit archive destinations before approving changes.

Risk: Deleting BOOTSTRAP.md or behavioral and safety instructions can affect future agent behavior.

Mitigation: Require separate confirmation before deleting those files or instructions, and prefer archiving when uncertainty remains.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/axelhu/skills/openclaw-workspace-cleaner)
- [ClawHub publisher profile](https://clawhub.ai/user/axelhu)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown plan and summary with optional workspace file edits after confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before modifying or deleting workspace files.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
