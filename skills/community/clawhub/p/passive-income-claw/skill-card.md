## Description:

Passive Income Claw scans Binance Earn opportunities, recommends options based on user preferences, and can execute subscriptions or redemptions within configured authorization limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipi6688](https://clawhub.ai/user/pipi6688)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to scan Binance Earn products, compare direct earn and borrow-to-earn strategies, and manage subscriptions or redemptions under configured account limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic Binance Earn or margin-borrowing actions can change the user's account without strong enforced safeguards.

Mitigation: Use a least-privilege Binance API key with withdrawals, futures, and spot trading disabled, keep confirmation-first mode enabled, and review configured limits before any execution.

Risk: Margin borrow-to-earn can create debt exposure and liquidation risk.

Mitigation: Enable margin only deliberately, reject borrow paths below the documented net-yield and margin-level thresholds, and re-check account health before execution.

Risk: Cron or auto mode can repeatedly perform account-changing actions under the configured limits.

Mitigation: Use cron or auto mode only after reviewing asset whitelists, operation whitelists, single-operation limits, and daily limits.

## Reference(s):

- [Passive Income Claw on ClawHub](https://clawhub.ai/pipi6688/skills/passive-income-claw)
- [Binance API Key Management](https://www.binance.com/en/my/settings/api-management)
- [Binance API Endpoint](https://api.binance.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON helper-script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Binance API credentials and may create or update profile, snapshot, and execution log files.]

## Skill Version(s):

0.7.0 (source: evidence.json release metadata; artifact/SKILL.md frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
