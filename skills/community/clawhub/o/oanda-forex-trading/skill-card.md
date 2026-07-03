## Description: <br>
Oanda Forex Trading lets agents retrieve OANDA forex market data and manage practice or live account orders, positions, and trades through AgentPMT-hosted calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs OANDA currency quotes, historical candles, account summaries, and controlled order or position management for practice or live forex workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place, modify, cancel, and close OANDA trades, including live-money trades, without a built-in confirmation gate. <br>
Mitigation: Prefer practice credentials, verify whether the connected account is live, and require explicit user confirmation before any place, modify, cancel, close-trade, or close-position action. <br>
Risk: Good-Til-Cancelled limit and stop orders may remain active after the agent session ends. <br>
Mitigation: Set broker-side limits where possible and review pending orders after agent workflows complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/oanda-forex-trading) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/oanda-forex-trading-2) <br>
- [Generated action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown instructions with JSON request examples and schema tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces AgentPMT MCP and REST call guidance for OANDA market data and trading actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
