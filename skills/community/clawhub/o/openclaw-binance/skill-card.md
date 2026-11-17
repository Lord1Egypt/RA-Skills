## Description:

OpenClaw Binance monitors Binance market data, analyzes basic trading-strategy performance metrics, writes Markdown risk reports, and can send risk alerts through configured channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yibaig](https://clawhub.ai/user/yibaig)

### License/Terms of Use:

MIT

## Use Case:

Developers and trading-operations users can use this skill to monitor Binance market data, review generated strategy-risk reports, and receive alerts for further human assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to store Binance API credentials in plaintext even though the reviewed behavior appears to use public market data.

Mitigation: Avoid real Binance keys unless needed; if testing requires credentials, use a dedicated read-only key with withdrawals and trading disabled, IP restrictions enabled, and config.json kept out of source control and shared workspaces.

Risk: The Feishu webhook URL is a secret that could be exposed through local configuration or shared workspaces.

Mitigation: Store the webhook outside version control, restrict access to the workspace, and rotate the webhook if it is exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yibaig/skills/openclaw-binance)
- [ClawHub Publisher Profile](https://clawhub.ai/user/yibaig)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown report files, console text, and webhook alert messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under data/binance_trades and can post Feishu webhook alerts when configured.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact manifest and README list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
