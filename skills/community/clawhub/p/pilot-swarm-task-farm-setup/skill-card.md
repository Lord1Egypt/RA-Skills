## Description:

Deploys a self-organizing five-agent compute swarm with leader, worker, and monitor roles for distributed task execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure a distributed task farm with a leader, three workers, and a monitor for map-reduce style work distribution and swarm health tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs multiple companion skills that affect leader, worker, and monitor behavior.

Mitigation: Pin and verify each companion skill before installation.

Risk: The setup creates persistent agent trust relationships through handshakes.

Mitigation: Confirm peer identities before handshaking and know how to revoke trust entries.

Risk: Swarm communication and Slack alerting can expose task or health data if destinations are too broad.

Mitigation: Restrict port 1002 access and validate Slack destinations before deployment.

Risk: The setup writes a persistent manifest under ~/.pilot.

Mitigation: Use only on hosts you control and document how to remove the ~/.pilot manifest during rollback.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-swarm-task-farm-setup)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific setup steps, manifest templates, handshake commands, and data-flow examples.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
