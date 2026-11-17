## Description:

实时监控 Polymarket 活跃市场的价格异动，并在 SkillPay 支付确认后返回变动最大的市场话题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqw1377-prog](https://clawhub.ai/user/xqw1377-prog)

### License/Terms of Use:


## Use Case:

Web3 market analysts and traders use this skill to request paid Polymarket market-mover summaries and identify active markets with the largest recent price changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A hardcoded SkillPay API credential is shipped with the artifact.

Mitigation: Remove the embedded credential, rotate the exposed key, and require the runtime to read SKILLPAY_API_KEY from the environment.

Risk: Payment API traffic can be directed to an environment-configured endpoint.

Mitigation: Restrict SkillPay API hosts to approved HTTPS origins before installation or deployment.

Risk: The HTTP dependency is pinned to an older version identified by the security guidance.

Mitigation: Update the pinned HTTP dependency before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xqw1377-prog/skills/poly-hunter)
- [Polymarket markets API endpoint](https://clob.polymarket.com/markets)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON API response with payment status and market-mover records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SkillPay charge confirmation before returning market data.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
