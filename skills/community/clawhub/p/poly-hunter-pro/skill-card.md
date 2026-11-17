## Description:

Monitors active Polymarket markets for major price movements and returns the top movers after SkillPay payment confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xqw1377-prog](https://clawhub.ai/user/xqw1377-prog)

### License/Terms of Use:


## Use Case:

Web3 investors and market analysts use this skill to request a paid snapshot of high-movement active Polymarket markets. It is intended to support market monitoring workflows, not to replace independent financial review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment handling exposes a built-in payment credential and does not safely scope charge IDs to a single paid invocation.

Mitigation: Remove the embedded SkillPay key from source, rotate the credential, allowlist payment API hosts, and bind each charge ID to exactly one paid invocation before real billing use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xqw1377-prog/skills/poly-hunter-pro)
- [Publisher profile](https://clawhub.ai/user/xqw1377-prog)
- [Polymarket markets endpoint](https://clob.polymarket.com/markets)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON API response with payment status and market-mover data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires payment confirmation before returning market data.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
