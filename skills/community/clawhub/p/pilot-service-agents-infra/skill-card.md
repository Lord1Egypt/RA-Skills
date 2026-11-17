## Description:

Pilot Service Agents Infra helps agents discover Pilot Protocol infrastructure agents, ask natural-language questions about pilotctl commands, and submit service-agent feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and operators who use Pilot Protocol can use this skill to query network infrastructure agents, inspect each agent contract with /help, and route feedback through the Pilot overlay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-text prompts or service-agent queries could disclose secrets or sensitive local data to Pilot Protocol overlay agents.

Mitigation: Avoid sending secrets or sensitive local data, and use /help to confirm each agent's contract before querying it.

Risk: Queries depend on a running Pilot Protocol daemon, network 9 membership, pilotctl availability, and reachable overlay agents.

Mitigation: Verify pilotctl is installed, the daemon is running and joined to network 9, and the target agent is discoverable before relying on results.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-infra)
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on pilotctl commands; actual service-agent responses are retrieved separately from pilotctl inbox.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
