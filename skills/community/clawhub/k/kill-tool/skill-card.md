## Description:

Terminate processes by sending signals. Use for stopping unresponsive programs, managing background tasks, and process lifecycle control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to stop running processes by PID, including graceful SIGTERM termination and forceful SIGKILL termination when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Force-killing a process can discard unsaved work or prevent normal cleanup.

Mitigation: Prefer graceful termination first, confirm the target PID, and use SIGKILL only when a process will not stop normally.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose process termination commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
