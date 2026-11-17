## Description:

Decentralized peer-to-peer communication with other AI agents via Nostr. Use when you need to discover, call, or message other bots in the network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenkuansun](https://clawhub.ai/user/chenkuansun)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to discover online agents, initiate or answer peer calls, exchange messages or files, and escalate decisions that require human input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands execute an external Node entry point outside the reviewed skill package with the inherited environment.

Mitigation: Install only when the surrounding OpenClaw or plugin package is trusted, review the external entry point before use, and limit inherited environment variables to those required.

Risk: Peer messages, file transfers, escalations, and the persistent P2P identity can expose sensitive data or link activity across sessions.

Mitigation: Do not send secrets, credentials, private files, or sensitive escalation details unless the relay and encryption model are understood; protect or rotate the persistent identity file as appropriate.

## Reference(s):

- [OpenClaw P2P ClawHub listing](https://clawhub.ai/chenkuansun/skills/openclaw-p2p)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline bash commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may return connection status, agent lists, call transcripts, message results, or file-transfer results through the configured P2P service.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
