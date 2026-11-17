## Description:

Automated trader for Polymarket weather highest temperature markets that uses Simmer SDK market discovery, local 9-10 AM entry windows, configurable price thresholds, and optional Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stefantaylor5](https://clawhub.ai/user/stefantaylor5)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure and run a Polymarket weather trading bot that discovers highest-temperature markets through Simmer, evaluates time-window and price-threshold signals, and can place buy orders or report dry-run signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect real-money Polymarket positions when run with live trading credentials.

Mitigation: Start in dry-run mode, use isolated low-balance credentials, and set conservative position limits before enabling live execution.

Risk: Managed execution and default redemption behavior can affect an account beyond a single proposed trade.

Mitigation: Keep WALLET_PRIVATE_KEY unset unless the runtime is trusted, review managed-wallet settings, and disable SIMMER_SNIPER2_ENABLE_REDEEM unless automatic redemption is intended.

Risk: Trading decisions depend on market discovery, city timezone detection, current price data, and configurable thresholds.

Mitigation: Review logs and dry-run signals before deployment, verify recognized market locations, and monitor skipped markets and executed trades.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stefantaylor5/skills/polymarket-weather-high-temp-sniper)
- [Simmer Dashboard](https://simmer.markets/dashboard)
- [Simmer Agent Registration](https://simmer.markets/agents/register)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Console text, Markdown instructions, environment configuration, and JSON automaton reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send Telegram notifications when configured and may update local runtime state.]

## Skill Version(s):

1.0.4 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
