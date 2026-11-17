## Description:

Controls Claude Code through tmux sessions for long-running development tasks, including starting sessions, sending commands, monitoring progress, and responding to prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanzhidongyzby](https://clawhub.ai/user/fanzhidongyzby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to run and supervise Claude Code tasks in tmux sessions for long-running development workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Claude Code unattended through tmux while bypassing permission checks and auto-approving prompts.

Mitigation: Use only in a tightly scoped project sandbox with disposable credentials, keep permission checks enabled by default, and require human review before sending confirmations.

Risk: Installer and account setup commands can change the host environment or introduce unreviewed code.

Mitigation: Avoid curl-to-shell installation, install dependencies through normal administrative processes, and provision non-root accounts according to local policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanzhidongyzby/skills/openclaw-claudecode)
- [Publisher profile](https://clawhub.ai/user/fanzhidongyzby)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides tmux session setup, Claude Code command dispatch, progress monitoring, and cleanup.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
