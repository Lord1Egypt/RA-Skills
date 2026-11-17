## Description:

Infra Wrapper is a Bash-based local logging utility for recording, searching, summarizing, and exporting infrastructure wrapper activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers can use this skill to log Terragrunt, OpenTofu, Terraform, and related infrastructure wrapper activities, then inspect recent entries, search history, view basic statistics, or export accumulated logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs may include secrets, credentials, backend URLs, or sensitive production details that are stored in plaintext logs or exported files.

Mitigation: Treat the tool as a local notes/history logger and avoid entering sensitive values unless plaintext storage under ~/.local/share/infra-wrapper is acceptable.

Risk: The release describes Terragrunt-style orchestration, but the artifact behavior mainly records and exports local text entries.

Mitigation: Review the artifact before installing and do not rely on it to execute, validate, or orchestrate infrastructure changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain1/skills/infra-wrapper)
- [Publisher profile](https://clawhub.ai/user/bytesagain1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The wrapped command writes plaintext logs and export files under ~/.local/share/infra-wrapper.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
