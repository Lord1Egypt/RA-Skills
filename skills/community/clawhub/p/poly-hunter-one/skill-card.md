## Description:

庄家异动探测器 monitors active Polymarket markets and returns the three topics with the largest recent price movements after SkillPay payment confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqw1377-prog](https://clawhub.ai/user/xqw1377-prog)

### License/Terms of Use:


## Use Case:

Web3 investors and market analysts use this skill to request a paid JSON summary of the three active Polymarket markets with the largest recent price movements. The skill is exposed as a FastAPI endpoint that returns payment status until a SkillPay charge is confirmed, then returns market-mover data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships a hardcoded payment-service bearer key.

Mitigation: Remove the embedded SkillPay key, rotate the exposed key, and require deployment-time secret configuration before use.

Risk: Payment authorization controls are weak for real paid access.

Mitigation: Bind and consume paid charge IDs server-side before returning paid intelligence.

Risk: The payment API host and dependencies require review before real payment use.

Mitigation: Restrict the payment API host and upgrade vulnerable dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xqw1377-prog/skills/poly-hunter-one)
- [ClawHub publisher profile](https://clawhub.ai/user/xqw1377-prog)
- [Polymarket CLOB markets endpoint](https://clob.polymarket.com/markets)

## Skill Output:

**Output Type(s):** [JSON, Analysis, API Calls]

**Output Format:** [FastAPI JSON response with payment status or top-three Polymarket mover records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SkillPay charge confirmation before returning market-mover data.]

## Skill Version(s):

9.9.9 (source: server release metadata; artifact skill.yaml declares 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
