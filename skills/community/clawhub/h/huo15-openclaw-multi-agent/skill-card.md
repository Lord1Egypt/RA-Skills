## Description:

Huo15 Openclaw Multi Agent helps agents coordinate parallel OpenClaw subagent workflows for task assignment, worker execution, and result collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to split independent OpenClaw work into parallel worker tasks, configure subagent coordination, and summarize completed results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task text and completion results may be persisted in local activity files.

Mitigation: Do not include secrets, credentials, private customer data, or other sensitive material in task descriptions or completion results.

Risk: Shell helper scripts use task and worker identifiers in local file operations.

Mitigation: Use simple trusted identifiers and review generated file paths before running helper scripts.

Risk: Local deletion commands in the helper scripts can remove activity files.

Mitigation: Review script behavior before installation and back up important OpenClaw activity data before running cleanup operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-multi-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local OpenClaw activity files when bundled shell scripts are run.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
