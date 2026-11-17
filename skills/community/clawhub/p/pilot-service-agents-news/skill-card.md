## Description:

News feeds, forum aggregators, and current-events streams for Hacker News, dev.to, GDELT, Reddit, Stack Exchange, and USGS hazards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

External developers and operators use this skill to discover Pilot Protocol news and current-events service agents, inspect each agent's /help contract, and query public feeds or summaries through pilotctl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to remote public data agents through Pilot Protocol on network 9.

Mitigation: Use the skill only when that network dependency is acceptable, and avoid sending private context unless the target agent's /help contract is understood.

Risk: Some catalogue entries may be broader than strict news feeds.

Mitigation: Run a fresh list-agents query and inspect each selected agent's /help output before using /data, /summary, or free-text queries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-news)
- [Publisher Profile](https://clawhub.ai/user/teoslayer)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Skills](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to use pilotctl for public data feed discovery, /help inspection, structured /data queries, and summary requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
