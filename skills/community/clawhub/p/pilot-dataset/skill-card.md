## Description:

Exchange structured datasets with schema negotiation and metadata over Pilot Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to exchange CSV, JSON, or Parquet datasets with schema negotiation, format preferences, and lineage metadata over Pilot Protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataset transfer examples can send local files to another peer, which could expose proprietary, personal, regulated, or otherwise sensitive data.

Mitigation: Before running send-file commands, confirm the peer destination, dataset path, and metadata, and redact or exclude data that should not leave the environment.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-dataset)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilot-protocol skill, pilotctl on PATH, a running Pilot daemon, jq, and optionally python3 for format conversion.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
