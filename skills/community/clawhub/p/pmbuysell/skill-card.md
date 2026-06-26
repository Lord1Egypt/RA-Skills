## Description: <br>
Executes Polymarket (pmbuysell) trade/balance via CLI or Python API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yutou123](https://clawhub.ai/user/yutou123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to configure Polymarket accounts, place market buy or sell orders, query USDC balances and positions, and call the same workflows from Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live Polymarket trades using configured wallet keys. <br>
Mitigation: Use a dedicated low-balance wallet and require human approval outside the skill before every live order. <br>
Risk: Wallet private keys, funder addresses, and derived API credentials are read from local environment/configuration files. <br>
Mitigation: Protect the .env and data directories, restrict filesystem access, and avoid sharing logs or workspaces that may contain secrets. <br>
Risk: External trading dependencies and network calls can affect order behavior and availability. <br>
Mitigation: Pin and review dependencies, install only the skill requirements, and verify market slug, side, amount, and account configuration before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yutou123/pmbuysell) <br>
- [Publisher Profile](https://clawhub.ai/user/yutou123) <br>
- [Polymarket CLOB Endpoint](https://clob.polymarket.com) <br>
- [Polymarket Relayer Endpoint](https://relayer-v2.polymarket.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with CLI commands, Python examples, configuration snippets, and JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command results use JSON fields such as ok, message, usdc_balance, order_message, requested_amount, auto_amount, and conditional positions.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
