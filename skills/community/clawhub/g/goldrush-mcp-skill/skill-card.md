## Description: <br>
Use GoldRush MCP through UXC for multichain wallet balances, transfers, portfolio history, NFT ownership, token approvals, prices, and chain metadata via stdio MCP with injected API-key auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure and query GoldRush MCP for focused blockchain data lookups, including wallet balances, transfers, portfolio history, NFT ownership, token approvals, prices, and chain metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GoldRush API keys and wallet-history queries can expose sensitive operational or personal information. <br>
Mitigation: Use a dedicated least-privilege GoldRush API key, avoid unauthorized address lookups, keep wallet-history scans narrow, and remove the UXC credential or link when it is no longer needed. <br>
Risk: The skill starts the GoldRush MCP server through an npm package fetched with an @latest specifier. <br>
Mitigation: Review or pin the npm package before operational use, and expect a slower first run while npx downloads the package. <br>


## Reference(s): <br>
- [GoldRush MCP Server documentation](https://goldrush.dev/docs/goldrush-mcp-server) <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [ClawHub release page](https://clawhub.ai/jolestar/goldrush-mcp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON output-handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes help-first inspection, scoped wallet or chain queries, stable JSON envelope parsing, and API-key injection through GOLDRUSH_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
