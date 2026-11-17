## Description:

Global Labor Employment Data helps agents query labor force participation, unemployment rates, sector employment breakdowns, gender gaps, and youth employment data through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to query and compare country, regional, and global labor market indicators for workforce research, gender equity analysis, youth employment tracking, and SDG 8 monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses AgentPMT remote calls that can consume credits and may transmit user-provided query parameters.

Mitigation: Use only the minimum country, region, and filter inputs needed; avoid sending secrets or sensitive personal data, and confirm credit usage before repeated calls.

Risk: Setup instructions include mutable, unpinned install commands and related setup skills.

Mitigation: Review the package, source revision, and related setup skills before running setup commands or installing dependencies.

Risk: Labor market results may lag the current year because source data availability varies by country.

Mitigation: Check the returned data year, source, and warnings before using results for time-sensitive decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/global-labor-employment-data)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/labor-market-employment)
- [Action Schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [guidance, JSON, shell commands, configuration]

**Output Format:** [Markdown instructions with JSON request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [AgentPMT remote tool calls return JSON labor indicators, trends, comparisons, and insights when invoked through an enabled account connection.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
