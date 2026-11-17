## Description:

Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmbell09-lang](https://clawhub.ai/user/rmbell09-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to monitor and control existing tmux sessions for interactive command-line tools, including sending keys, reading pane output, and checking session status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and manipulate existing interactive tmux sessions, including reading pane output and sending control keys.

Mitigation: Install only when tmux remote control is intended, use narrowly named session and pane targets, and avoid shared or sensitive sessions.

Risk: Commands such as prompt approval, interrupt or EOF keys, session termination, and full scrollback capture can affect running work or expose sensitive terminal history.

Mitigation: Require explicit confirmation before approving prompts, sending interrupt or EOF keys, killing sessions, or dumping pane history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rmbell09-lang/skills/lucky-tmux)
- [Publisher profile](https://clawhub.ai/user/rmbell09-lang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tmux on darwin or linux; command examples operate on named tmux sessions and panes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
