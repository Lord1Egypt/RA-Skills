## Description:

Urban transport and bike-share skill for querying CityBikes indexes, GBFS feeds, and Transport for London line status and arrivals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and operators use this skill to query live bike-share availability and Transport for London line status or arrivals through Pilot Protocol service agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries sent through pilotctl go to external Pilot Protocol service agents and may be summarized by Gemini for /summary or free-text requests.

Mitigation: Install and use the skill only for intended live transport-data workflows, and avoid sending sensitive information in service-agent queries.

Risk: Live transport catalog entries and filter contracts can change over time.

Mitigation: Use list-agents for fresh discovery and send /help to the selected service agent before relying on its current filter schema.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill listing](https://clawhub.ai/teoslayer/skills/pilot-service-agents-traffic)
- [Publisher skills catalog](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to use pilotctl and read asynchronous inbox responses from service agents.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; frontmatter version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
