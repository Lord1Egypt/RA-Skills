## Description:

Backs up the local OpenClaw configuration directory, including hidden files, to a timestamped sibling directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijiangtai](https://clawhub.ai/user/lijiangtai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create a full timestamped local snapshot of ~/.openclaw before changes, migration, or recovery work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup may contain credentials, logs, workspace files, and agent state copied from ~/.openclaw.

Mitigation: Treat backup directories as sensitive, preserve restrictive permissions, and avoid sharing them.

Risk: A backup that is assumed valid without checking may not support a later restore.

Mitigation: Verify backup contents and integrity before relying on a snapshot for recovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijiangtai/skills/openclaw-all-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local backup instructions and command output for timestamped OpenClaw snapshots.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
