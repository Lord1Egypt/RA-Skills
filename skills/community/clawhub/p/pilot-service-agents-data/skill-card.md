## Description:

General open-data APIs that did not fit a narrower category, including PubChem compounds/substances and the REST Countries full catalog.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agents use this skill to discover and query Pilot Protocol service agents for broad public dataset lookups, including PubChem compound/substance data and REST Countries catalog data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and summary prompts are sent through the Pilot Protocol network, and summaries are described as Gemini-generated.

Mitigation: Do not send private, confidential, regulated, or otherwise sensitive data in filters or free-text prompts.

Risk: The available service-agent catalog and each agent's filter contract can change over time.

Mitigation: Run a fresh list-agents query and send /help to the selected agent before relying on a query shape.

Risk: Public dataset responses may be incomplete, truncated, or dependent on upstream public data services.

Mitigation: Check the count, total, truncated flag, next cursor, and upstream_url fields before using returned data in decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-data)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance, Text, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Pilot Protocol command patterns and expected response shapes; actual dataset responses are returned by external service agents.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
