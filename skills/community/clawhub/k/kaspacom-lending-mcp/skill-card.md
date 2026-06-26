## Description: <br>
Use KaspaCom Lending through the KaspaCom DeFi MCP/CLI for market discovery, position checks, and lending actions like supply, borrow, and repay on IGRA and Kasplex environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marciano147](https://clawhub.ai/user/marciano147) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to discover KaspaCom lending markets, inspect wallet lending positions, check health factors, and prepare supply, borrow, and repay commands for IGRA and Kasplex environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes real supply, borrow, and repay commands that can affect wallet balances and lending positions. <br>
Mitigation: Confirm the wallet, network, token, amount, health-factor impact, and expected transaction result before signing, and prefer read-only market or position checks unless a transaction is explicitly intended. <br>
Risk: The skill depends on the KaspaCom DeFi MCP/CLI package for lending operations. <br>
Mitigation: Install and use the package only when the publisher and package source are trusted. <br>


## Reference(s): <br>
- [KaspaCom Lending MCP on ClawHub](https://clawhub.ai/marciano147/kaspacom-lending-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet, network, token, amount, collateral, borrow, repay, and health-factor guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
