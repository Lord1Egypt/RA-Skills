## Description:

Global Poverty & Inequality Data: Query World Bank poverty and inequality data by country or region name, returning poverty headcount thresholds, Gini index, income shares, and extreme poverty metrics through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query country, regional, income-group, or global poverty and inequality metrics from World Bank data for development analysis, poverty research, inequality studies, SDG monitoring, and policy research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on remote, paid AgentPMT API use and mutable live schema or instruction responses.

Mitigation: Install only if AgentPMT is trusted, prefer pinned setup packages, and review local schema before approving changes from live schema or examples.

Risk: World Bank poverty and inequality data may lag current conditions and can have country or indicator gaps.

Mitigation: Check returned years, source attribution, and data notes before using results for analysis or policy decisions.

## Reference(s):

- [Global Poverty Inequality Data schema](./schema.md)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/global-poverty-inequality-data)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-poverty-inequality-data)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can include indicator data, trends, regional comparisons, insights, SDG alignment, data notes, and error guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
