## Description: <br>
Guides agents through discovering and using the official Kraken CLI for market data, paper trading, MCP integration, and optional authenticated trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to set up Kraken CLI workflows for live market data, paper trading, and MCP client configuration. Users can also follow the credential guidance when enabling authenticated Kraken API access for live trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading or broad MCP scopes can expose account actions that may have financial impact. <br>
Mitigation: Start with paper trading or market,paper MCP scope, and enable account or live trading tools only when they are explicitly needed. <br>
Risk: Kraken API credentials can grant sensitive account access if over-permissioned or exposed. <br>
Mitigation: Use least-privilege Kraken API keys and prefer the documented setup or environment-variable flows instead of passing secrets directly in shell commands. <br>
Risk: The skill points users to an external CLI maintained outside this skill artifact. <br>
Mitigation: Install from the official Kraken CLI documentation and review the CLI behavior before using it in production workflows. <br>


## Reference(s): <br>
- [Kraken CLI repository](https://github.com/krakenfx/kraken-cli) <br>
- [Kraken CLI installation instructions](https://github.com/krakenfx/kraken-cli#installation) <br>
- [Kraken](https://www.kraken.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no bundled executable code.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
