## Description:

实时监控 Polymarket 活跃市场的大额资金和价格异动，并在 SkillPay 支付确认后返回异动话题分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqw1377-prog](https://clawhub.ai/user/xqw1377-prog)

### License/Terms of Use:


## Use Case:

Web3 traders and market analysts use this skill to identify the three active Polymarket markets with the largest recent absolute price movements after a SkillPay payment check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an exposed SkillPay billing API key.

Mitigation: Revoke the exposed key and move billing credentials to a trusted secret source before production use.

Risk: Payment verification is under-scoped for a paid workflow.

Mitigation: Bind each paid charge ID to the correct user, product, amount, currency, and one-time redemption before returning paid results.

Risk: The payment flow depends on external SkillPay hosts.

Mitigation: Allowlist expected SkillPay hosts and install only when the publisher and billing flow are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xqw1377-prog/skills/poly-hunter-final)
- [Publisher profile](https://clawhub.ai/user/xqw1377-prog)
- [Polymarket CLOB markets endpoint](https://clob.polymarket.com/markets)

## Skill Output:

**Output Type(s):** [JSON data, Text]

**Output Format:** [JSON response containing payment status, optional payment URL, and Polymarket mover records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to Polymarket and SkillPay; successful payment status is required before market data is returned.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact skill.yaml declares 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
