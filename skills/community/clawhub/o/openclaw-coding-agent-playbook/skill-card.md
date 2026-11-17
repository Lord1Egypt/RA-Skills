## Description:

Delegate coding tasks to Codex, Claude Code, Pi, or OpenCode from bash with safe launch modes, background monitoring, and repo-isolated review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielsinewe](https://clawhub.ai/user/danielsinewe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate implementation, review, refactoring, triage, and verification work to coding agents while keeping sessions scoped and observable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends bypassed or highly automated permission modes for coding agents that can edit files and run commands.

Mitigation: Supervise delegated sessions, use trusted repositories, prefer disposable worktrees or containers, minimize exposed environment variables, avoid secrets, and choose safer permission modes unless full automation is intentional.

Risk: Delegated coding sessions can affect the active repository when run in the wrong working directory.

Mitigation: Keep each session scoped to one repository and use a temporary clone or worktree for pull request review and high-risk changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielsinewe/skills/openclaw-coding-agent-playbook)
- [danielsinewe publisher profile](https://clawhub.ai/user/danielsinewe)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with bash command examples and workflow checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before execution because delegated agents may edit files or run commands.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
