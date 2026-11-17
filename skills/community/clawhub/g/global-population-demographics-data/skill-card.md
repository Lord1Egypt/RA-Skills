## Description:

Query population totals, growth rates, age structure, fertility rates, migration data, and urban-rural indicators through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to query country or region demographic data, compare population profiles, analyze fertility and migration trends, and build demographic reports from World Bank Data360 indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on AgentPMT-hosted remote calls and live schema or instruction lookups that can change after release.

Mitigation: Use ClawHub-reviewed setup routes, fetch the live schema before production integration, and verify remotely returned instructions before relying on them.

Risk: Account secrets, wallet private keys, mnemonics, signatures, or payment headers may be exposed if copied into prompts or logs.

Mitigation: Use the referenced setup skills for credential handling and keep secrets and payment material out of prompts and logs.

Risk: The artifact recommends unpinned external setup installs.

Mitigation: Prefer pinned or ClawHub-reviewed installation routes when configuring AgentPMT access.

Risk: World Bank demographic indicators may lag the current year or be unavailable for some countries and periods.

Mitigation: Check returned years and availability notes, and avoid presenting unavailable or older observations as current data.

## Reference(s):

- [Generated action schema](artifact/schema.md)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-population-demographics-data)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/population-demographics)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON]

**Output Format:** [Markdown instructions with JSON request examples and remote JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines one query_population_data action with country_or_region, demographic_aspect, calculate_dependency_ratios, include_urban_rural, and time_period parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
