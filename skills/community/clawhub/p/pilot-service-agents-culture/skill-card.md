## Description:

Museum and cultural collections service agents for searching the Art Institute of Chicago and Metropolitan Museum of Art catalogs and fetching object metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and agents use this skill to discover culture-category Pilot Protocol service agents, inspect each agent's filter contract, and query museum collection records or summaries through pilotctl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Museum search queries are sent through the Pilot Protocol service-agent network.

Mitigation: Use the skill only when that network path is acceptable for the query, and avoid sending sensitive or private search terms.

Risk: Agent contracts and available catalog agents can change over time.

Mitigation: Run list-agents and send /help to the selected agent before sending /data or /summary requests.

Risk: Gemini-generated summaries may be incomplete or inaccurate.

Mitigation: Prefer structured /data responses for source records and review generated summaries before relying on them.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-culture)
- [Pilot Skills Index](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot Protocol daemon joined to network 9, and reachable Pilot service agents.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
