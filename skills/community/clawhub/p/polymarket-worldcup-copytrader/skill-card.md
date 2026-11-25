## Description:

Copy the top World Cup traders on Polymarket — auto-curated daily by Simmer. No wallet list to configure; the skill sources leaders via PolyNode's slippage-adjusted copy-PnL screen. Regular mode (daily rebalance). Free tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users configure Simmer credentials and use the agent to follow a daily curated set of World Cup traders on Polymarket. They can inspect a dry-run trade plan or enable automated trading on the Simmer simulation venue or Polymarket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The live trading path can redeem resolved positions across the account, beyond the skill's stated World Cup copytrading purpose.

Mitigation: Review whether account-wide redemption is acceptable before enabling live trading, and consider using the skill without that behavior.

Risk: The security scan was partial because two local path-like references in SKILL.md could not be resolved.

Mitigation: Resolve and review the missing referenced components before installation or live use.

Risk: The SDK dependency is unpinned beyond a minimum version.

Mitigation: Review and control the installed SDK version before running the skill with trading credentials.

## Reference(s):

- [World Cup Copytrader release](https://clawhub.ai/simmer/skills/polymarket-worldcup-copytrader)
- [Publisher profile](https://clawhub.ai/user/simmer)

## Skill Output:

**Output Type(s):** [Text, Trade plans, Configuration guidance]

**Output Format:** [Plain-text CLI status and trade-plan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run; live mode can place trades on the selected venue.]

## Skill Version(s):

0.1.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
