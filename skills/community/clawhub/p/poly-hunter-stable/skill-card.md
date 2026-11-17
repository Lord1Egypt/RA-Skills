## Description:

Monitors active Polymarket markets for the largest recent price movements and returns payment-gated market mover data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqw1377-prog](https://clawhub.ai/user/xqw1377-prog)

### License/Terms of Use:


## Use Case:

External Web3 and prediction-market analysts use this skill to identify active Polymarket markets with the largest recent price changes after completing the configured SkillPay payment flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A built-in SkillPay API credential could expose billing access if deployed as-is.

Mitigation: Remove and rotate the embedded key, and require SKILLPAY_API_KEY to be supplied by the deployment environment.

Risk: Billing controls may be weak because access depends on the current charge_id status flow.

Mitigation: Review and harden per-use charge validation before relying on this skill for paid access enforcement.

Risk: The configured SkillPay API base can be overridden by deployment settings.

Mitigation: Restrict SKILLPAY_API_BASE to the intended provider before installation or deployment.

Risk: The pinned requests dependency was flagged for review in the server security guidance.

Mitigation: Update requests to an approved patched version during deployment review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xqw1377-prog/skills/poly-hunter-stable)
- [Publisher Profile](https://clawhub.ai/user/xqw1377-prog)
- [Polymarket CLOB Markets Endpoint](https://clob.polymarket.com/markets)
- [SkillPay API Base](https://api.skillpay.me)

## Skill Output:

**Output Type(s):** [JSON, text]

**Output Format:** [FastAPI JSON response containing payment status or top market mover records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns either a SkillPay charge and payment status or up to three active Polymarket market records with current price, previous price, delta, absolute delta, volume, and status.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
