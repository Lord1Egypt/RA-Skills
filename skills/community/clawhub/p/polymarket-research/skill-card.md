## Description:

Research any Polymarket topic — get market data, probabilities, volumes, and top holders in one snapshot. Read-only, no trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market researchers use this skill to collect a read-only snapshot of matching Polymarket markets, including probabilities, trading volume, resolution details, and available top-holder data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the supplied Simmer API key for API requests, and the external simmer-sdk dependency was not inspected.

Mitigation: Keep SIMMER_API_KEY in environment configuration, use an isolated Python environment, and review the SDK version before running the skill.

## Reference(s):

- [Polymarket Research on ClawHub](https://clawhub.ai/simmer/skills/polymarket-research)
- [Publisher profile: simmer](https://clawhub.ai/user/simmer)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Plain-text market research snapshot]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only results with probabilities, volume, resolution dates, and available top-holder summaries; market count and filters are configurable.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
