## Description:

Route routine updates of an existing local or remote OpenClaw Gateway to its installation owner, with automatic session recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Gateway operators and developers use this skill to identify the owner of an existing installation, route an update through that owner's workflow, and verify recovery and service health afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An update could target the wrong Gateway installation or bypass the workflow responsible for a managed deployment.

Mitigation: Identify the host, runtime, profile, service, and update owner, then follow that owner's runbook and deployment safeguards.

Risk: Interrupting or clearing active sessions during an update could discard work or prevent recovery.

Mitigation: Use the owner's graceful drain and recovery-preserving restart flow; do not cancel tasks, abort sessions, or clear queues to force idleness.

## Reference(s):

- [Openclaw Update on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-update)
- [Publisher profile: hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with workflow-specific shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and steps depend on the identified installation owner and deployment workflow.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
