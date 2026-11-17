## Description:

Run programs that survive OpenClaw exec session cleanup and gateway restarts via tmux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darwin7381](https://clawhub.ai/user/darwin7381)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run dev servers, tunnels, workers, build tasks, or interactive programs in tmux so they can continue after exec cleanup, session timeouts, or gateway restarts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tmux sessions can keep tunnels, servers, workers, or other commands running after the current exec session ends.

Mitigation: Use this only for explicitly intended long-running tasks, review active sessions, and stop sessions with the documented tmux cleanup commands when finished.

Risk: Long-running commands may inherit sensitive environment variables when the tmux session is created.

Mitigation: Scope environment variables to the command that needs them, avoid unnecessary secrets, and clean up sessions that no longer need access.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
