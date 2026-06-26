## Description: <br>
LongPort Quant Trader helps agents configure and use LongPort-based quantitative trading scripts for Hong Kong and U.S. equities, including mean-reversion and momentum strategies, monitoring, reporting, and Feishu notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fxm1618-gmail](https://clawhub.ai/user/fxm1618-gmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal investors and quantitative trading practitioners can use this skill to set up, review, and operate LongPort trading workflows for scanning markets, generating strategy signals, tracking performance, and sending notifications. Live trading should be gated behind paper-trading validation and credential review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place brokerage orders with LongPort credentials. <br>
Mitigation: Use paper trading or read-only review first, audit all order paths, and require an explicit live-trading opt-in before providing production credentials. <br>
Risk: Credential handling and message-recipient controls are not adequate for the requested authority. <br>
Mitigation: Remove and rotate any hardcoded LongPort or Feishu secrets, configure recipients explicitly, and store API keys only in protected environment variables or a managed secret store. <br>
Risk: Logs and state files may expose sensitive financial data. <br>
Mitigation: Treat logs, reports, portfolio state, and notification payloads as sensitive data with restricted access, retention limits, and redaction where possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fxm1618-gmail/longport-quant-trader) <br>
- [Publisher profile](https://clawhub.ai/user/fxm1618-gmail) <br>
- [LongPort Open Platform](https://open.longportapp.com) <br>
- [LongPort API documentation](https://open.longportapp.com/docs) <br>
- [LongPort API account credentials](https://open.longportapp.com/account) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-style text with Python configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading signals, order/status summaries, performance metrics, setup steps, and credential configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
