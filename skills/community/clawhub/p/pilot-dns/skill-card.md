## Description:

Pilot Dns helps agents manage Pilot Protocol human-friendly hostnames, aliases, and namespaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set agent hostnames, resolve human-readable Pilot Protocol names to node IDs, look up node hostnames, and inspect known peers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose a pilotctl connect command that contacts another agent.

Mitigation: Review any proposed connect command before allowing it, especially the destination hostname, timeout, and message.

Risk: The skill relies on pilotctl and a running Pilot Protocol daemon for hostname management.

Mitigation: Install the required Pilot Protocol components and confirm the daemon state before executing generated commands.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill listing](https://clawhub.ai/teoslayer/skills/pilot-dns)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented pilotctl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
