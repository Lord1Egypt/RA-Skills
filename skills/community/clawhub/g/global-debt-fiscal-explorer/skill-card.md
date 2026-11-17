## Description:

Global Debt & Fiscal Explorer helps agents query national debt, government revenue, public expenditure, fiscal balance, debt service, and debt sustainability indicators for countries or regions through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research analysts use this skill to retrieve fiscal indicators, compare countries, review debt sustainability signals, and prepare AgentPMT MCP or REST calls for the debt-fiscal-management product.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes unpinned remote installer commands that could change after review.

Mitigation: Verify the publisher and package version before installation, and prefer OpenClaw or ClawHub installation routes where possible.

Risk: The skill routes usage through AgentPMT as an external paid fiscal-data service.

Mitigation: Install only when that external service relationship is acceptable, and keep secrets, wallet material, signatures, and payment headers out of prompts and logs.

Risk: Fiscal data availability varies by country and the latest World Bank indicators may lag the current year.

Mitigation: Check returned dates, data availability summaries, and live schema details before using results for high-stakes fiscal analysis.

## Reference(s):

- [AgentPMT marketplace: debt-fiscal-management](https://www.agentpmt.com/marketplace/debt-fiscal-management)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/global-debt-fiscal-explorer)
- [Generated action schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [guidance, JSON, shell commands, configuration]

**Output Format:** [Markdown instructions with JSON request examples and shell command setup snippets; remote tool responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines one paid AgentPMT action, query_fiscal_data, with optional country_or_region, fiscal_aspect, calculate_debt_ratios, and time_period parameters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
