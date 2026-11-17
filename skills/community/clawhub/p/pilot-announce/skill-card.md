## Description:

One-to-many announcements with read receipts over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to broadcast important updates, system announcements, or policy changes to multiple trusted Pilot Protocol peers while tracking delivery or acknowledgement where the underlying environment supports it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Announcement workflows may be mistaken for verified read receipts when the underlying pilotctl environment does not separately provide receipt-status confirmation.

Mitigation: Confirm receipt and acknowledgement through a verified pilotctl receipt-status workflow before relying on announcements for incident, policy, or compliance decisions.

Risk: Announcements can expose secrets or sensitive incident details through recipient selection, transport behavior, or logs in the Pilot Protocol environment.

Mitigation: Avoid sending secrets or sensitive incident details unless transport protections, recipient trust, and logging behavior have been confirmed for the deployment.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-announce)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilotctl binary, a running Pilot Protocol daemon, trust relationships with recipients, and topic subscriptions for publish/subscribe workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
