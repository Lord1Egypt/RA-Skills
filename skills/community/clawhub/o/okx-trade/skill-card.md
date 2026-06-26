## Description: <br>
Setup, install, and use OKX Agent Trade Kit for AI-powered OKX market data, account, portfolio, bot, and trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chingchiu169](https://clawhub.ai/user/chingchiu169) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install and configure OKX Agent Trade Kit, connect AI clients through Skills or MCP, query market data, and operate OKX trading, portfolio, and bot tools with appropriate safety controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect AI clients to OKX credentials and money-moving trading tools that can affect real funds. <br>
Mitigation: Install only when intentional, start with demo or read-only mode, use a dedicated sub-account with no withdrawal permission, and require manual confirmation for live orders, leverage changes, or bot actions. <br>
Risk: OKX API credentials are stored in ~/.okx/config.toml and could be exposed if file access is not controlled. <br>
Mitigation: Protect and restrict access to ~/.okx/config.toml, never paste API keys into chat, and grant only the minimum API permissions needed. <br>
Risk: The setup installs external OKX packages for MCP and CLI operation. <br>
Mitigation: Verify the external OKX packages before installing and review commands before execution. <br>


## Reference(s): <br>
- [OKX Agent Trade Kit Documentation](https://www.okx.com/docs-v5/agent_en/) <br>
- [OKX Agent Trade Kit GitHub Repository](https://github.com/okx/agent-trade-kit) <br>
- [MCP Client Setup](references/mcp-setup.md) <br>
- [Tools Reference](references/tools-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and TOML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safety guidance for demo mode, read-only mode, sub-account credentials, and manual confirmation before live trading actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
