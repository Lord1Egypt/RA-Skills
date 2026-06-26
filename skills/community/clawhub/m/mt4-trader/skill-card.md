## Description: <br>
MT4 Trader Bridge enables Python-to-MetaTrader 4 Expert Advisor communication through file-based JSON requests for market data, order management, risk controls, alerts, and grid strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apuba](https://clawhub.ai/user/apuba) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading automation users use this skill to connect an agent or Python scripts to MT4 for quotes, account and position summaries, order placement, stop-loss and take-profit management, price alerts, and grid-strategy operations. It is intended for supervised trading workflows where account permissions and execution limits are controlled outside the skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place and close live MT4 trades, including broad account-changing actions. <br>
Mitigation: Use a demo or tightly limited account first, keep auto trading off unless actively supervised, and require explicit confirmations and hard limits before allowing an agent or chat channel to place trades. <br>
Risk: The release relies on external compiled .ex4 trading components. <br>
Mitigation: Verify the external .ex4 files independently before installation and only deploy files obtained from the expected source. <br>
Risk: Bulk-close and grid commands can materially change account exposure. <br>
Mitigation: Restrict or disable bulk-close and grid operations unless the operator has reviewed symbol scope, position state, and loss limits. <br>


## Reference(s): <br>
- [MT4 Bridge API Reference](references/api_docs.md) <br>
- [ClawHub skill page](https://clawhub.ai/apuba/mt4-trader) <br>
- [External MT4 compiled component download page](https://gitee.com/3603317/skill-plugin/tree/master/mt4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON-file bridge conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing trading workflow guidance and local Python command patterns; actual MT4 execution depends on installed EA components and user account permissions.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
