## Description:

Connect an OpenClaw gateway to a MeshCore LoRa mesh node in minutes — install the maintained channel plugin (@fintlp/openclaw-meshcore), run the probe-first setup wizard, and verify the first DM over radio. Use when a user wants their AI agent reachable via MeshCore, off-grid messaging, or LoRa mesh comms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fintlp](https://clawhub.ai/user/fintlp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect an OpenClaw agent to a reachable MeshCore node for off-grid messaging and to verify DM connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because three local references could not be resolved.

Mitigation: Review the unresolved references and proceed only if comfortable with that limitation.

Risk: When group monitoring uses digest mode, full admitted message text is stored locally in plain JSON.

Mitigation: Keep group monitoring disabled unless needed and protect the digest log as sensitive data.

Risk: A paired MeshCore DM can lead to activity on the agent's other channels.

Mitigation: Pair only trusted senders and retain the access policies of the destination channels.

## Reference(s):

- [MeshCore plugin issue tracker](https://github.com/fintlp/openclaw-meshcore/issues)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
