## Description:

Install or operate a standalone local OpenClaw manager skill that adds shadow-first thread observation, durable session/run state, a loopback-only sidecar, attention management, snapshots, connector normalization, and capability reports for real work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zephyrchen0754](https://clawhub.ai/user/zephyrchen0754)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users, developers, and teams use this skill to run a local manager for real work threads, including shadow-first observation, resumable session/run state, attention views, connector normalization, snapshots, and capability reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unauthenticated local sidecar can read and change local work records.

Mitigation: Keep the sidecar bound to 127.0.0.1 and do not enable 0.0.0.0 or :: binding without adding authentication.

Risk: Run-evidence exports and snapshots can include raw message and event data.

Mitigation: Review generated snapshots and reports before sharing them outside the local environment.

Risk: The skill stores chat-derived work state on disk through a local manager process.

Mitigation: Install only where local storage of work state is acceptable and protect the configured manager state root.

## Reference(s):

- [OpenClaw Manager Skill Page](https://clawhub.ai/zephyrchen0754/skills/humanclaw-made-openclaw-manager)
- [Architecture](docs/architecture.md)
- [Session Model](docs/session-model.md)
- [Event Schema](docs/event-schema.md)
- [Connector Protocol](docs/connector-protocol.md)
- [Capability Facts](docs/capability-facts.md)
- [Security Model](SECURITY.md)
- [Security Audit Response](docs/security-audit-response.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with command examples plus local JSONL, HTML, and markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local state, event logs, checkpoints, snapshots, and capability reports under the configured manager state root.]

## Skill Version(s):

0.3.2 (source: skill.yaml, package.json, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
