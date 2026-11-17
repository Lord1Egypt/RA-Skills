## Description:

Helps agents query and manage Linear issues, projects, and team workflows for project management and task tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project owners, and teams use this skill to work with Linear issue queries, project status, milestones, and team workflow tasks through an AI agent. It is intended for Linear project management workflows and is not suitable for personnel performance evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found that the skill requests broader local command and file-write authority than its Linear purpose clearly needs.

Mitigation: Use it only for explicit Linear tasks, avoid broad project or credential access, and require confirmation before writing local files or running commands.

Risk: The skill can guide creation or changes to Linear issues and project workflow data.

Mitigation: Require user confirmation before creating, updating, assigning, or otherwise changing Linear issues, projects, or workflow state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/linear-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text guidance with optional shell command snippets and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Linear issue, project, and workflow actions; users should confirm write or command execution steps before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
