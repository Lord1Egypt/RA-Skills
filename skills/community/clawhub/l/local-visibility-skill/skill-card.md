## Description:

Expert guidance on AI visibility and local SEO from Local Falcon, including optimization for AI search platforms, local pack rankings, Google Business Profile, geo-grid tracking, and Local Falcon MCP-assisted analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wearelocalfalcon](https://clawhub.ai/user/wearelocalfalcon)

### License/Terms of Use:

MIT

## Use Case:

External users, agencies, enterprise marketers, SMB owners, developers, and AI agents use this skill to interpret local SEO and AI visibility signals, distinguish map metrics from AI visibility metrics, and produce prioritized optimization guidance. When Local Falcon MCP tools are connected, the skill can guide data-driven scan, campaign, competitor, and account analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can instruct agents to install or run external MCP packages with a Local Falcon API key.

Mitigation: Use a pinned, verified MCP package version and avoid storing API keys in broadly readable configuration files.

Risk: MCP-assisted workflows can trigger billable scans or change account state through campaigns, locations, and Falcon Guard actions.

Mitigation: Require explicit user approval before scans, campaigns, Falcon Guard changes, or other credit-consuming or account-changing actions.

Risk: Local SEO and AI visibility recommendations may be misleading if SoLV map metrics and SAIV AI visibility metrics are confused.

Mitigation: Keep SoLV and SAIV separate in analysis and ask the user to clarify which visibility channel they are evaluating when ambiguous.

## Reference(s):

- [Local Falcon documentation](https://docs.localfalcon.com)
- [Local Falcon platform](https://www.localfalcon.com)
- [Local Falcon MCP package](https://www.npmjs.com/package/@local-falcon/mcp)
- [Local Falcon API credentials](https://www.localfalcon.com/api/credentials/)
- [Metrics glossary](references/metrics-glossary.md)
- [AI platforms deep dive](references/ai-platforms.md)
- [MCP workflows](references/mcp-workflows.md)
- [Prompt templates](references/prompt-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with tables, checklists, inline shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Local Falcon MCP tools when available and should require explicit approval before billable scans, campaigns, or account-changing actions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
