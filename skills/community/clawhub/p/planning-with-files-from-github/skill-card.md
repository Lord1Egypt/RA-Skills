## Description:

This skill helps agents plan and recover complex, multi-step work by creating and maintaining persistent markdown planning files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingcd](https://clawhub.ai/user/yingcd)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to structure complex implementation, research, and multi-session tasks with durable task plans, findings, and progress logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The startup script uses unsafe template substitution that can turn a crafted task description into local command execution.

Mitigation: Review before installing, use only in trusted workspaces, and avoid starting planning sessions from untrusted task text until init-session.sh uses data-safe templating.

Risk: Planning files may retain project details after the task completes.

Mitigation: Delete task_plan.md, findings.md, and progress.md when the recorded task details should not persist.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yingcd/skills/planning-with-files-from-github)
- [Publisher profile](https://clawhub.ai/user/yingcd)
- [Workflow reference](artifact/references/workflow.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown files with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates task_plan.md, findings.md, and progress.md in the active workspace when its initialization script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
