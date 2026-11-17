## Description:

Queries global digital economy and connectivity indicators, including internet penetration, mobile subscriptions, broadband access, ICT trade metrics, infrastructure data, trend analysis, and digital divide comparisons through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, analysts, and policy teams use this skill to request country or regional digital economy indicators, compare connectivity trends, and assess digital divide signals from World Bank World Development Indicators data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on AgentPMT's hosted, paid digital-economy data tool and related setup skills.

Mitigation: Install only when that hosted tool is intended, review setup skills before use, and prefer pinned or trusted installation routes where available.

Risk: Endpoints, schemas, setup steps, and examples may become stale after the artifact's last updated date.

Mitigation: Reinstall from ClawHub or skills.sh before relying on production integrations when freshness is important.

Risk: The marketing text mentions e-government readiness, but the security guidance and artifact notes state EGDI is not available from the World Bank data used here.

Mitigation: Do not rely on this skill for actual EGDI or e-government readiness scores; use it only for the listed World Bank digital economy indicators.

Risk: The inspected artifacts contain quality and supply-chain cautions even though no hidden execution, persistence, or destructive behavior was found.

Mitigation: Review and scan the skill before deployment, keep tool inputs scoped to the task, and avoid placing secrets, wallet keys, mnemonics, signatures, or payment headers in prompts or logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/global-digital-economy-connectivity-data)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/digital-economy-technology)
- [Generated Action Schema](artifact/schema.md)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance, API Calls]

**Output Format:** [Markdown guidance with JSON request examples and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Hosted AgentPMT calls may require enabled account access and credits; returned data can include indicator values, units, source years, trends, comparisons, insights, and warnings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
