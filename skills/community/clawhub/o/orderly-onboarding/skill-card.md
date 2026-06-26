## Description: <br>
Agent onboarding for Orderly Network - omnichain perpetual futures infrastructure, MCP server, skills, and developer quickstart <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarnadas](https://clawhub.ai/user/Tarnadas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and engineers use this skill to orient agents around Orderly Network, install related MCP and skill tooling, and find the right documentation or workflow for DEX, SDK, API, and trading-bot development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation commands use npx/npm packages and may change local agent or MCP configuration. <br>
Mitigation: Review package names and source before installing, prefer pinned versions and local installs where practical, and inspect MCP or agent configuration changes. <br>
Risk: The skill covers leveraged perpetual futures workflows where incorrect setup or use can lead to rapid liquidation or loss of funds. <br>
Mitigation: Use testnet first, confirm trading and authentication flows, and review leveraged-trading risks before using real funds. <br>


## Reference(s): <br>
- [Orderly Network Documentation](https://orderly.network/docs) <br>
- [Orderly Network SDK Repository](https://github.com/orderlynetwork/js-sdk) <br>
- [Orderly Example DEX Repository](https://github.com/orderlynetwork/example-dex) <br>
- [Orderly MCP Server on npm](https://www.npmjs.com/package/@orderly.network/mcp-server) <br>
- [Orderly Skills on npm](https://www.npmjs.com/package/@orderly.network/skills) <br>
- [Orderly Tokenomics Documentation](https://orderly.network/docs/introduction/tokenomics) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and TOML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include package installation commands, MCP client configuration snippets, and links to Orderly documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
