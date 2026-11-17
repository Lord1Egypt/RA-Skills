## Description:

Interactive terminal control via tmux for TUI apps, prompts, and long-running CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imbeasting](https://clawhub.ai/user/imbeasting)

### License/Terms of Use:


## Use Case:

Developers and QA testers use this skill to operate interactive terminal sessions, capture TUI output, and manage long-running CLI or server processes with tmux.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Captured terminal output may expose sensitive data from interactive sessions.

Mitigation: Review captured panes before sharing logs or reports, and avoid exposing secrets in terminal output.

Risk: Long-running tmux sessions may leave background processes active after the agent workflow finishes.

Mitigation: Stop processes with Ctrl-C where appropriate and kill tmux sessions after use.

## Reference(s):

- [tmux-terminal on ClawHub](https://clawhub.ai/imbeasting/skills/imbeasting-tmux-terminal)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
