## Description:

Pilot Event Bus helps agents aggregate, broadcast, and subscribe to shared Pilot Protocol event topics for coordinated workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate fleets of agents through shared Pilot Protocol topics, including event publication, subscription, trust listing, discovery, and trust setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trust setup can grant an agent access to participate in Pilot Protocol coordination flows.

Mitigation: Do not run the handshake command automatically; verify the hostname and the reason for the trust request before approving it.

Risk: Copy-pasted shell examples can mishandle dynamic values or overwrite a fixed temporary events file.

Mitigation: Quote dynamic values when adapting commands and replace the fixed /tmp/events.json path with a deliberate per-run location.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-event-bus)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use pilotctl JSON output and require pilotctl, a running Pilot Protocol daemon, and mutual trust between participating agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
