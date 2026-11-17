## Description:

Pilot Relay helps agents send store-and-forward messages to offline peers over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send asynchronous relay messages, inspect daemon status, retrieve inbox messages, and clear processed messages when peers may be offline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages are sent over the configured Pilot Protocol relay network.

Mitigation: Use the skill only when Pilot Protocol relay messaging is intended, and treat message contents as data being sent to another agent through that network.

Risk: Inbox clearing can remove stored messages after retrieval.

Mitigation: Run inbox clearing only after confirming important messages were processed or preserved.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [Pilot Relay on ClawHub](https://clawhub.ai/teoslayer/skills/pilot-relay)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the pilotctl binary, a running Pilot Protocol daemon, registry connectivity, and a trust relationship between sender and recipient.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
