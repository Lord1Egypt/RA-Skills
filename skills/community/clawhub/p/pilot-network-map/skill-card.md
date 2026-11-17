## Description:

Visualize Pilot Protocol network topology, trust graphs, active connections, and latency maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to ask an agent for network diagrams, adjacency views, trust relationship maps, connection summaries, and latency-oriented views for a Pilot Protocol environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose network topology, trust relationships, connection state, and latency information to the agent through local pilotctl output.

Mitigation: Use it only in environments where the local pilotctl setup is trusted and sharing that operational network information with the agent is acceptable.

Risk: Generated diagrams or maps can be incomplete or misleading if the Pilot Protocol daemon is not running or local network state is stale.

Mitigation: Confirm the daemon and pilotctl commands are working before relying on generated topology or latency views.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Network Map on ClawHub](https://clawhub.ai/teoslayer/skills/pilot-network-map)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON-oriented command examples, and Graphviz DOT examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May depend on local pilotctl JSON output, a running Pilot Protocol daemon, and optional Graphviz rendering.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
