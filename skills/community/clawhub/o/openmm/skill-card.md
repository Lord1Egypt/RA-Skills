## Description: <br>
Open-source market making for AI agents. Multi-exchange trading, grid strategies, and real-time market data. CLI + MCP + Skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent users use this skill to configure OpenMM, query multi-exchange market data, manage orders, and run grid trading workflows through CLI, MCP, and agent skill instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect agents or chat commands to live exchange accounts with authority to place and cancel real orders. <br>
Mitigation: Use testnet or small, separate API keys first, disable withdrawals and transfers, apply IP allowlists where possible, and require human confirmation before live trading actions. <br>
Risk: Grid trading and cancel-all commands can materially change account positions or cancel active orders. <br>
Mitigation: Dry-run grid strategies before execution, review the trade plan, and enable mutating tools only when they are needed for the workflow. <br>
Risk: Exchange credentials are required for account and trading operations. <br>
Mitigation: Store credentials in environment variables, use least-privilege exchange permissions, and avoid sharing or committing secrets. <br>


## Reference(s): <br>
- [OpenMM ClawHub listing](https://clawhub.ai/adacapo21/openmm) <br>
- [OpenMM homepage](https://github.com/3rd-Eye-Labs/OpenMM) <br>
- [OpenMM documentation](https://deepwiki.com/3rd-Eye-Labs/OpenMM) <br>
- [OpenMM npm package](https://www.npmjs.com/package/@3rd-eye-labs/openmm) <br>
- [OpenMM MCP server](https://github.com/QBT-Labs/OpenMM-MCP) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash, JSON, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-formatted CLI output guidance for agent parsing.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
