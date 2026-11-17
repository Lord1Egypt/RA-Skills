## Description:

Automated Polymarket trading skill based on price momentum signals that executes trades when market trends are detected.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[skybinjf](https://clawhub.ai/user/skybinjf)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill as a customizable AION template for monitoring Polymarket opportunities, testing momentum-based signals, and optionally executing trades after configuration and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dry-run mode may still perform real account redemptions.

Mitigation: Confirm redemption behavior before installation or disable auto-redemption until dry-run boundaries are verified.

Risk: Scheduled or continuous execution can repeatedly act on live market data and accounts.

Mitigation: Disable scheduled runs unless explicitly authorized and test single executions before enabling continuous operation.

Risk: Live trading can spend real funds using the configured AION or wallet credentials.

Mitigation: Use least-privilege credentials, set conservative position limits, and require explicit review before using live mode.

Risk: Dependencies are version-ranged rather than pinned.

Mitigation: Pin and verify dependency versions before production or funded trading use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/skybinjf/skills/momentum-polymarket-trader)
- [AION Documentation](https://docs-t.aionmarket.com/)
- [AION Building Skills Guide](https://docs-t.aionmarket.com/essentials/building-skills)
- [Polymarket API](https://docs.polymarket.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code]

**Output Format:** [Markdown documentation with shell and Python code blocks; runtime text logs and trade decision summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AION_API_KEY; optional live trading, continuous mode, wallet, RPC, position-size, and edge-threshold configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
