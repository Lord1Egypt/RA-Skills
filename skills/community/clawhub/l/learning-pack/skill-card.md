## Description:

A beginner-oriented OpenClaw learning pack that introduces 10 core skills for file operations, search, shell execution, user interaction, sub-agent workflows, and Git integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tpc1009](https://clawhub.ai/user/tpc1009)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and new OpenClaw users use this pack to learn common agent tool patterns, including reading and editing files, searching workspaces, running shell commands, asking users questions, coordinating sub-agents, and using Git helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pack includes broad command execution and file mutation guidance that can affect local workspaces.

Mitigation: Review the package before installing and use workspace, file, and command permissions that match the task.

Risk: The Git helper can stage all changes and create commits, which may include secrets or unrelated files.

Mitigation: Check git status and review the diff before using auto-commit behavior, and do not push until the commit contents have been verified.

Risk: Sub-agent and messaging workflows can pass along sensitive context if used carelessly.

Mitigation: Do not paste access tokens, passwords, or API keys into chat, and review delegated task scope before sharing repository context.

## Reference(s):

- [Learning Pack on ClawHub](https://clawhub.ai/tpc1009/skills/learning-pack)
- [QUICKSTART.md](QUICKSTART.md)
- [Aider Git Integration](https://github.com/Aider-AI/aider)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Atlassian Git Workflows](https://www.atlassian.com/git/tutorials/comparing-workflows)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline YAML, shell, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for OpenClaw tool usage and a Git helper script that can create branches, inspect status, and commit staged workspace changes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and artifact clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
