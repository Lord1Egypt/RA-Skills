## Description:

PRISM API SDK provides market-data access, canonical asset resolution, and finance endpoints for AI agents, Claude Code, Cursor, and trading-bot workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strykragent](https://clawhub.ai/user/strykragent)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent builders use this skill to install and configure the PRISM SDK, then query market, asset-resolution, DeFi, macro, and related financial-data endpoints from agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned npm packages or MCP repository code can change runtime behavior over time.

Mitigation: Verify the npm package and MCP repository before installation, and prefer pinned package versions or repository commits.

Risk: API keys and project data may be exposed more broadly than needed when configuring market-data access.

Mitigation: Provide only the Prism API key and project data required for the intended workflow, and avoid sharing unrelated credentials.

Risk: Financial market data can influence downstream analysis even though the skill has no evidence of trading capability.

Mitigation: Treat outputs as market-data inputs for review, and keep any trading or portfolio actions under separate human-approved controls.

## Reference(s):

- [PRISM API](https://prismapi.ai)
- [PRISM API Documentation](https://prismapi.ai/docs)
- [PRISM API Docs](https://api.prismapi.ai/docs)
- [prismapi-sdk on npm](https://www.npmjs.com/package/prismapi-sdk)
- [PRISM OS SDK GitHub Repository](https://github.com/Strykr-Prism/PRISM-OS-SDK)
- [PRISM MCP Server GitHub Repository](https://github.com/Strykr-Prism/PRISM-MCP-Server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and TypeScript code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include npm installation commands, API configuration guidance, SDK usage examples, and risk notes for handling market-data API access.]

## Skill Version(s):

0.2.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
