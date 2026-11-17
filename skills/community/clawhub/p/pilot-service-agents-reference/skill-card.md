## Description:

Provides lightweight utility lookup guidance for Pilot Protocol service agents covering dictionaries, jokes, colors, currencies, random facts, D&D data, and similar reference tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover and query low-stakes Pilot Protocol reference agents for word tools, trivia, jokes, colors, public facts, and ECB currency-rate lookups. It is not intended for live market data, detailed country profiles, or knowledge-graph entity lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries may be sent to remote lookup agents and upstream public APIs.

Mitigation: Avoid private or sensitive queries and inspect each agent's /help output before sending data.

Risk: The reference category covers broad utility lookups and can overlap with more specialized domains.

Mitigation: Use the finance, data, or knowledge skills for live market data, detailed country profiles, or knowledge-graph lookups.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-reference)
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH and a Pilot Protocol daemon joined to network 9.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
