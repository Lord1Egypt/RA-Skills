## Description:

Guides developers in using git worktree with coding agents to run multiple development tasks in parallel across isolated worktrees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunwenpinghao](https://clawhub.ai/user/hunwenpinghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to split independent implementation tasks into separate Git worktrees, run coding agents concurrently, and manage review, merge, and cleanup steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow examples include running coding agents with permission safeguards disabled and inheriting the user's full shell environment.

Mitigation: Run agents with normal approvals or inside a sandbox/container, pass only the environment variables needed for the task, and review pushes or pull requests before merging.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hunwenpinghao/skills/parallel-coding)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
