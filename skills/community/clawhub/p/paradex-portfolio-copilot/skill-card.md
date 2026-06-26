## Description: <br>
Provides conversational Paradex portfolio briefings by combining account summary, positions, balances, transfers, market data, and funding information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sv](https://clawhub.ai/user/sv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Paradex users use this skill to ask natural-language questions about portfolio status, positions, balances, P&L, daily activity, and account risk. It turns read-only account and market data into concise briefings and follow-up prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as account or briefing requests could expose private Paradex financial account data when the user intended a different account or context. <br>
Mitigation: Use explicit Paradex prompts, confirm ambiguous account requests before retrieving data, and grant only read-only Paradex MCP permissions where possible. <br>
Risk: Portfolio and P&L answers may be point-in-time or approximate because prices, positions, and funding change continuously and realized P&L is not directly available from current tools. <br>
Mitigation: Label estimates clearly, avoid presenting the briefing as trading advice, and direct users to the Paradex UI for complete closed-trade history. <br>


## Reference(s): <br>
- [Portfolio Copilot on ClawHub](https://clawhub.ai/sv/paradex-portfolio-copilot) <br>
- [Briefing Format Templates](references/briefing-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise natural-language briefing, with Markdown tables for larger position lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include approximations for time-period P&L and should state when realized P&L is not available from current tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
