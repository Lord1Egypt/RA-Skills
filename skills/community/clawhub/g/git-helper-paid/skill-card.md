## Description:

Git辅助 helps developers run common Git workflows such as status, pull, push, branch, and log, with AI-assisted review and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to inspect repository status, pull or push changes, manage branches, view logs, and generate Git-related review or quality guidance in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-changing Git actions can alter local work or remote branches.

Mitigation: Use only in trusted repositories and require explicit confirmation before pull, push, branch changes, or other modifying actions.

Risk: The skill requests command and write capability without clear confirmation boundaries in the artifact.

Mitigation: Review the skill before installation and run it with the least privileges needed for the intended Git workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/git-helper-paid)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON-style summaries with Git command output and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository-changing Git command results when an agent is allowed to execute commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
