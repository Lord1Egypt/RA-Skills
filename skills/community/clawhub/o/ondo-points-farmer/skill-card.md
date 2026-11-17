## Description:

Automates Ondo Perps trading across high-liquidity markets and provides tools for tracking and estimating Points rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcii](https://clawhub.ai/user/0xcii)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and DeFi users use this skill to configure and run an Ondo Perps trading bot, monitor account points, and estimate reward outcomes from trading volume.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The farmer can place repeated live market orders and incur trading fees or losses.

Mitigation: Run it only with funds you intend to risk, start with minimal position size and cycle count, and monitor execution closely.

Risk: The skill requires Ondo Perps API credentials for account actions.

Mitigation: Use a dedicated limited-permission API key, store it in environment variables, and rotate or revoke it after use.

Risk: The estimator command is informational, while the farmer command performs live trading.

Mitigation: Verify which script is being run and test the estimator separately before executing the farmer.

Risk: Automated volume farming may violate platform rules or produce unexpected account outcomes.

Mitigation: Review Ondo Perps terms and program rules before use and stop execution if behavior differs from expectations.

## Reference(s):

- [Ondo Perps App](https://app.ondoperps.xyz)
- [Ondo Perps API](https://api.ondoperps.xyz)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ondo Perps API credentials and may place live market orders when the farmer script is run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
