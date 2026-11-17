## Description:

Enables near real-time chat between multiple Kiro instances through a shared JSON file with polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sonerbo](https://clawhub.ai/user/sonerbo)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate work between trusted local Kiro instances by sending and reading short messages in a shared workspace file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages are exchanged through a trusted local shared JSON file without built-in file permissions, authentication, sender verification, locking, or atomic writes.

Mitigation: Use only with participating Kiro instances in the same trusted local workspace, avoid secrets and high-stakes instructions, and add permissions, authentication, sender verification, and locking or atomic writes before using it for sensitive coordination.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples and command-line script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local shared JSON message file at ~/.openclaw/workspace/memory/kiro-realtime.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
