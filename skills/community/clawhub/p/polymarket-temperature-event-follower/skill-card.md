## Description:

Automated trader for Polymarket weather highest temperature markets that scans global markets and executes buys during a local morning window when YES prices are favorable, with SkillPay billing integration, error handling, and state persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefantaylor5](https://clawhub.ai/user/stefantaylor5)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and developers use this skill to monitor Polymarket weather markets and run an automated, configurable buying strategy for high-temperature event contracts. It supports dry-run testing before live trading with wallet credentials and funded accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money Polymarket orders and incur trading losses.

Mitigation: Start with dry-run mode, review the threshold and order logic before live use, and fund only a dedicated wallet with a small amount.

Risk: Wallet and Polymarket API credentials are sensitive, and credentials printed in logs should be treated as exposed.

Mitigation: Use an isolated environment, avoid primary wallets, rotate exposed credentials, and keep secrets out of shared logs and repositories.

Risk: Billing and order execution are separate, so a submitted order may remain active even if billing fails afterward.

Mitigation: Monitor SkillPay balance and bot logs, verify billing behavior in dry-run or minimal live tests, and stop the bot if billing warnings appear.

Risk: Unpinned dependencies and network API calls increase operational and supply-chain risk.

Mitigation: Pin and review dependencies, run in a constrained virtual environment, and limit API credentials and wallet funding to the minimum required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stefantaylor5/skills/polymarket-temperature-event-follower)
- [Polymarket](https://polymarket.com)
- [Polymarket settings](https://polymarket.com/settings)
- [SkillPay dashboard](https://skillpay.me/dashboard)
- [English usage guide](artifact/SKILL-en.md)
- [Background knowledge](artifact/background-knowledge-EN.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python scripts, shell commands, and environment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions, trading-bot code, configuration examples, dry-run/live command guidance, logs, and persisted state files.]

## Skill Version(s):

1.0.1 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
