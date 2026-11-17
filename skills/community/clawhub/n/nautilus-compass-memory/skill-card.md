## Description:

Local-first long-term memory for AI agents over MCP, with typed retrieval, shared persistence, and drift detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunxiaoxx](https://clawhub.ai/user/chunxiaoxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retain decisions, pitfalls, and other useful context across sessions and share it across agents. They can retrieve relevant memories and check for drift against prior failure patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted gateway receives memory content and recall queries.

Mitigation: Use the local daemon for sensitive memories or when data must remain on the machine.

Risk: External installers can add hooks and modify agent configuration files.

Mitigation: Review installer behavior before running it and retain the configuration backups.

Risk: Persistent memories may be shared across sessions or agents in ways users did not intend.

Mitigation: Choose deliberately what information should persist and what should be shared.

## Reference(s):

- [Project repository and local installation instructions](https://github.com/chunxiaoxx/nautilus-compass)
- [Hosted MCP gateway](https://compass.nautilus.social/mcp/)
- [Hosted gateway signup](https://compass.nautilus.social/signup)
- [ClawHub listing](https://clawhub.ai/chunxiaoxx/skills/nautilus-compass-memory)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text and MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent memory records, retrieved context, and drift check results.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
