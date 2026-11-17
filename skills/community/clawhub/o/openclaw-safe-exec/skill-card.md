## Description:

Protects agent workflows from prompt injection in shell command output by wrapping untrusted command streams with UUID-delimited boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmceleney](https://clawhub.ai/user/jmceleney)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to wrap shell commands that may return untrusted external data, such as API responses, remote CLI output, or user-generated files. It helps agents treat command output as data rather than instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A caller-controlled UUID can weaken the boundary protection if an untrusted value is supplied through the --uuid option.

Mitigation: Do not expose or use --uuid with untrusted values; prefer generated UUIDs or remove and strictly validate that option before relying on the wrapper as a security control.

Risk: The wrapper reduces prompt-injection risk in command output but does not make prompt injection impossible.

Mitigation: Review command output and agent behavior before deployment, and treat the wrapper as one control rather than a complete security boundary.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command usage guidance and integration instructions for wrapping untrusted shell output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
