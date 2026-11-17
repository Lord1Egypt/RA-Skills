## Description:

Provides access to Pilot Protocol climate and energy-grid service agents for UK carbon intensity, Electricity Maps zones, and Open-Meteo climate data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agents use this skill to discover and query Pilot Protocol climate service agents for carbon-intensity feeds, electricity-zone metadata, current electricity mix, and climate time series.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and filters sent through pilotctl may be visible to the remote service agents involved.

Mitigation: Avoid sending sensitive or proprietary data in filters or free-text requests, and inspect the target agent's /help contract before use.

Risk: Summary and free-text responses are Gemini-generated prose and may be incomplete or misleading.

Mitigation: Prefer /data structured responses for operational decisions and verify summaries against returned items and upstream source data.

Risk: The documented agent catalog is a snapshot and regional coverage varies.

Mitigation: Run a fresh list-agents query and confirm each selected agent's /help schema before relying on availability or coverage.

Risk: The skill depends on Pilot Protocol setup, pilotctl, network 9 membership, and the list-agents directory agent.

Mitigation: Confirm the local daemon, binary path, network membership, and list-agents reachability before querying service agents.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-climate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and inbox reads for asynchronous agent responses.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
