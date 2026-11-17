## Description:

Trades CPI bin markets on Kalshi accounting for systematic upward revision bias (~0.03 pp) in initial CPI releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to identify and optionally trade Kalshi CPI bin-market opportunities based on a configured CPI revision-drift model. It defaults to dry-run mode and requires explicit live execution before real USDC trades are placed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can spend real funds through Kalshi/DFlow when trading credentials and a Solana private key are available.

Mitigation: Keep the skill in dry-run mode unless live trading is intended, cap position sizing with the provided tunables, and use isolated funded credentials for live operation.

Risk: The skill process requires both trading API credentials and a Solana private key.

Mitigation: Treat both credentials as high value, scope and rotate them where possible, and avoid installing the skill in environments that do not need live trading.

Risk: The security guidance flags SDK dependency review and fail-open safeguard behavior as concerns for funded environments.

Mitigation: Pin and review simmer-sdk before live use, and require missing market context to block rather than authorize new trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-econ-revision-drift-trader)
- [Simmer skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Console text and JSON status reports, with Markdown setup guidance and Python code artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live trading requires the --live flag and configured credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
