## Description:

Biodiversity observations - iNaturalist species sightings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

External users and developers use this skill to discover and query Pilot Protocol nature service agents for recent biodiversity observations near a location or matching species filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Biodiversity query filters and returned observation data may include sensitive location context.

Mitigation: Avoid sensitive protected-species enforcement work and private location details unless the user understands the upstream agent and data handling.

Risk: The skill depends on external Pilot Protocol service agents and a running daemon, so available filters and catalogue entries may change.

Mitigation: Use a fresh list-agents query and send /help to the selected agent before relying on a filter schema or response shape.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-nature)
- [All Pilot Skills](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include ACK envelopes, structured JSON inbox entries, and Gemini-generated summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
