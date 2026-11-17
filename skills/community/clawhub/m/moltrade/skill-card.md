## Description:

Operate the Moltrade trading bot for configuration, backtesting, test-mode runs, Nostr signal broadcast, exchange adapters, and strategy integration in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-chen2050](https://clawhub.ai/user/ai-chen2050)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to configure and run Moltrade trading workflows, including backtests, test-mode bot runs, live trading preparation, copy trading, signal broadcast, and exchange or strategy integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading and credential handling can affect real funds when broad exchange or wallet keys are used.

Mitigation: Use an isolated environment, least-privilege keys, and testnet or test mode first; never paste wallet private keys or broad trading keys into chat.

Risk: The release relies on upstream repository content and dependencies that require user review.

Mitigation: Review the upstream Moltrade repository and dependencies before installation or deployment.

Risk: Binance Square posts are public and may publish trading content externally.

Mitigation: Require a manual final review before publishing any Binance Square post.

## Reference(s):

- [Moltrade homepage](https://github.com/hetu-project/moltrade.git)
- [ClawHub skill page](https://clawhub.ai/ai-chen2050/skills/moltrade)
- [Binance authentication reference](binance/spot/references/authentication.md)
- [Binance testnet](https://testnet.binance.vision)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted configuration guidance, backtest or test-mode run commands, exchange adapter instructions, strategy integration steps, and public posting guidance.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
