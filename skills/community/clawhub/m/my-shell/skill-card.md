## Description:

Runs shell commands inside a dedicated tmux session named claw, captures output, and prompts before potentially destructive commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idienet](https://clawhub.ai/user/idienet)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run local shell commands in a dedicated tmux session and read captured output during development, inspection, and operational tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This skill provides broad local shell execution.

Mitigation: Install only when local shell execution is intentional, and run it in a tightly limited environment.

Risk: The security scan reports weak command controls.

Mitigation: Add a real approval or sandbox boundary for dangerous commands before general use.

Risk: The security scan reports malformed metadata containing an unexpected overwrite command.

Mitigation: Fix the metadata JSON and remove the overwrite command before general use.

Risk: The security guidance identifies shell-string command execution as unsafe.

Mitigation: Replace shell-string execution with argument-array execution where commands are invoked by the implementation.

## Reference(s):

- [My Shell on ClawHub](https://clawhub.ai/idienet/skills/my-shell)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Text returned from captured shell output, with command metadata when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands execute through a dedicated tmux session named claw.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
