## Description:

Monitors gold prices, records baseline and opening prices, and generates notification guidance when price movement crosses a configured threshold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatyouprompt](https://clawhub.ai/user/whatyouprompt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to check Au99.99 gold prices, compare them with saved baselines, and receive concise buy, sell, or hold notifications. It is suitable for scheduled OpenClaw runs where the operator wants threshold-based price alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide buy, sell, or hold guidance based on an unauthenticated price feed and source-description mismatches.

Mitigation: Review carefully before installation, avoid relying on it for financial decisions, and switch to an authenticated HTTPS source with aligned source labels and trusted price validation before high-stakes use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whatyouprompt/skills/gold-price-monitor)
- [Publisher profile](https://clawhub.ai/user/whatyouprompt)
- [Sina Finance](https://finance.sina.com.cn/)
- [China Construction Bank gold quotation XML endpoint](https://www2.ccb.com/cn/home/news/gjshjjc01.xml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs price fields, threshold status, alert flag, recommendation text, and timestamped status messages.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
