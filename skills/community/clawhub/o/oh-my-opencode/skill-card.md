## Description:

Oh My OpenCode helps agents install, configure, and operate the oh-my-opencode OpenCode plugin for multi-agent delegation, autonomous work modes, category-based routing, tmux integration, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcoso](https://clawhub.ai/user/mcoso)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up and operate oh-my-opencode workflows in OpenCode, including autonomous task execution, planned multi-agent work, model/provider routing, hooks, skills, MCPs, tmux integration, and diagnostics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage broad autonomous and background agent behavior in a user's repository.

Mitigation: Keep autonomous and background hooks disabled or approval-gated when working in repositories with secrets or sensitive business code.

Risk: Installation and diagnostics may involve unpinned package execution or remote installer commands.

Mitigation: Review commands before running them, prefer pinned package versions where possible, and avoid piping remote installers directly into a shell.

Risk: Diagnostic commands may execute registry-hosted code.

Mitigation: Run diagnostics only in environments where executing the referenced package code is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mcoso/skills/oh-my-opencode)
- [Oh My OpenCode Repository](https://github.com/code-yeongyu/oh-my-opencode)
- [Configuration Reference](references/configuration.md)
- [Troubleshooting Guide](references/troubleshooting.md)
- [Oh My OpenCode Schema](https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json)
- [OpenCode Documentation](https://opencode.ai/docs/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenCode CLI commands, oh-my-opencode configuration examples, workflow guidance, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
