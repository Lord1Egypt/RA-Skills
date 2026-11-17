## Description:

Runs shell commands inside a dedicated tmux session named claw and returns captured shell output to the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biosaylom](https://clawhub.ai/user/biosaylom)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run local shell commands through a persistent tmux session and inspect the resulting output during agent-assisted workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local shell execution can read, modify, or delete local data accessible to the skill process.

Mitigation: Use only when broad shell access is intended, preferably in a disposable or least-privileged environment.

Risk: Dangerous-command warnings are incomplete and should not be treated as a security boundary.

Mitigation: Review commands before execution and require explicit user approval for destructive or privileged operations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [JSON object containing the submitted command and captured shell output, or an error object for blocked commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a dedicated tmux session named claw and captures recent pane output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
