## Description:

Connects to remote ConnectOnion agents by address, delegates user tasks, and supports ConnectOnion environment setup for agent networking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openonion](https://clawhub.ai/user/openonion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use oo to connect to ConnectOnion agents by 0x address, delegate tasks, and handle follow-up turns through direct or relay networking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may execute local setup commands, install packages, initialize an agent identity, and open remote network connections.

Mitigation: Run only in a sandbox or trusted environment, and require explicit user approval before package installation, identity creation, or remote connection attempts.

Risk: Delegated tasks can disclose prompts or sensitive context to remote agents.

Mitigation: Avoid sending secrets, credentials, private files, or confidential business context in delegated prompts.

Risk: Remote-agent networking can interact with private-network endpoints through direct connection attempts.

Mitigation: Review the target address and connection path before use, and restrict network access where private-network probing is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openonion/skills/oo)
- [openonion publisher profile](https://clawhub.ai/user/openonion)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command blocks; remote-agent responses are returned as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parses CO_ marker lines from delegated-agent runs and may continue for multi-turn tasks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
