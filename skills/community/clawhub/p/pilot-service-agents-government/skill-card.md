## Description:

Provides access patterns for Pilot Protocol government and civic data agents, including Federal Register, FBI Wanted, civic information, and public data catalog queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and query public government and civic data services through Pilot Protocol, including regulatory notices, elections information, public-data catalogs, and agency datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The listed agent catalog may include broader public-data sources beyond strictly government-only services.

Mitigation: Verify the exact agent fields, source, and category with list-agents and /help before relying on returned data.

Risk: Using the skill requires joining the Pilot Protocol data-exchange network and querying third-party service agents.

Mitigation: Install and run it only when the operator is comfortable with Pilot Protocol participation and the requested public-data workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-government)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide the agent to use pilotctl for /help, /data, /summary, and inbox retrieval; downstream service responses may include structured JSON envelopes or prose summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
