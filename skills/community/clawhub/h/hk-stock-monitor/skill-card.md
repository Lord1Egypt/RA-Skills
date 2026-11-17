## Description:

Tracks Hong Kong and A-share equities with realtime quotes, technical analysis, price-move alerts, and Feishu notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[merlini0116](https://clawhub.ai/user/merlini0116)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, traders, and developers use this skill to monitor configured Hong Kong and A-share stocks, generate concise technical-analysis reports, and send threshold-based alerts during trading hours.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardcoded Feishu destinations and an embedded QVeris API key may send data to an unintended chat or expose credentials.

Mitigation: Replace the Feishu chat ID in every script, remove and rotate the embedded API key, and require secrets through environment variables before installation or use.

Risk: Cron-based monitoring can repeatedly send stock data or alerts to external services before destinations are verified.

Mitigation: Disable scheduled jobs until message targets, data handling expectations, and account permissions have been reviewed.

Risk: Generated stock analysis and buy/sell suggestions can be incorrect or misleading.

Mitigation: Treat reports and alerts as informational signals only and require human review before making investment decisions.

Risk: Shell subprocess calls are used for external messaging.

Mitigation: Prefer direct APIs or hardened subprocess invocation before use in accounts that hold private investment or business data.

## Reference(s):

- [Stock configuration reference](references/stocks.md)
- [Sina Finance](https://finance.sina.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style terminal reports, alert messages, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local monitoring state, history, and report files when scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
