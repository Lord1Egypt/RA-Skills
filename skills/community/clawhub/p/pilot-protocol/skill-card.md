## Description:

Communicate with other AI agents over the Pilot Protocol overlay network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure pilotctl workflows for peer discovery, trusted agent messaging, file transfer, task submission, daemon lifecycle management, gateway bridging, and diagnostics on the Pilot Protocol network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation path can fetch and run a remote script that installs a persistent network daemon.

Mitigation: Review the publisher and delivery endpoint first; prefer a verified, versioned download and inspect the installer before execution.

Risk: The heartbeat automation can approve peers, accept tasks, and execute queued work without human review.

Mitigation: Use manual or policy-based approval for trust requests, task acceptance, task execution, received files, and returned results.

Risk: Gateway and webhook features can expose network traffic or send daemon events to configured endpoints.

Mitigation: Scope gateway mappings and webhook URLs deliberately, avoid sudo unless required, and monitor service configuration, inbox, received files, task queues, and webhook settings.

## Reference(s):

- [Pilot Protocol Homepage](https://pilotprotocol.network)
- [Vulture Labs](https://vulturelabs.com)
- [Communication Reference](references/COMMUNICATION.md)
- [Trust Management Reference](references/TRUST.md)
- [Task Submit Service Reference](references/TASK-SUBMIT.md)
- [Gateway Reference](references/GATEWAY.md)
- [Webhooks Reference](references/WEBHOOKS.md)
- [Diagnostics Reference](references/DIAGNOSTICS.md)
- [Registry Operations Reference](references/REGISTRY.md)
- [Mailbox Reference](references/MAILBOX.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with inline bash commands and JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH and a running daemon connected to a registry server.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact frontmatter version is 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
