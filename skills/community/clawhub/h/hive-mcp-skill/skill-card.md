## Description: <br>
Use Hive Intelligence MCP through UXC for broad crypto market, onchain, portfolio, and risk workflows with help-first discovery and convenience-layer guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover Hive Intelligence MCP endpoint groups, inspect endpoint schemas, and invoke narrow crypto market, onchain, wallet, portfolio, and risk workflows through UXC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto market queries, wallet addresses, and portfolio lookup inputs are sent to Hive's remote MCP service. <br>
Mitigation: Install only with a trusted UXC setup, keep inputs narrow, inspect endpoint schemas before invocation, and require separate review before any endpoint that could write to an account or change data. <br>


## Reference(s): <br>
- [Hive MCP docs](https://hiveintelligence.xyz/crypto-market-data-mcp) <br>
- [Usage patterns](references/usage-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON argument examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs agents to use UXC, parse the JSON output envelope, and inspect endpoint schemas before invocation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
