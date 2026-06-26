## Description: <br>
Interact with Lighter protocol, a ZK rollup orderbook DEX, to trade, check prices, manage positions, and query account data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aviclaw](https://clawhub.ai/user/aviclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading operators use this skill to query Lighter market data, inspect account and position state, and run signed order workflows after configuring Lighter credentials. <br>

### Deployment Geography for Use: <br>
Global, subject to Lighter service terms and jurisdiction restrictions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live mainnet trades with signing credentials and does not provide a built-in dry-run or confirmation safeguard. <br>
Mitigation: Use read-only flows by default, simulate trades before signing, and require manual confirmation before running any live order command. <br>
Risk: Signed order placement depends on the external Lighter SDK. <br>
Mitigation: Verify and pin the SDK before installing or using it for trading. <br>
Risk: Trading credentials and account keys could authorize financial actions if exposed or misused. <br>
Mitigation: Use a burner or limited-permission account where possible, keep keys out of logs, and store secrets outside committed files. <br>


## Reference(s): <br>
- [Lighter API docs](https://apidocs.lighter.xyz/docs/get-started-for-programmers-1) <br>
- [Lighter mainnet API endpoint](https://mainnet.zklighter.elliot.ai) <br>
- [Lighter Python SDK](https://github.com/elliottech/lighter-python) <br>
- [ClawHub skill page](https://clawhub.ai/aviclaw/lighter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python script references, and configuration details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request examples and credential setup guidance for read-only and signed trading flows.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
