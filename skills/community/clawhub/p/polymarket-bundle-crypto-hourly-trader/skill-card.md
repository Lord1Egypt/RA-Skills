## Description:

Trades Polymarket crypto hourly Up/Down markets when sub-interval consensus appears to disagree with the hourly market price.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators can use this skill to run a configurable crypto hourly-market strategy that searches for bundle consensus opportunities and submits simulated or live trade requests through Simmer. It is intended for users who understand automated prediction-market trading and can review the strategy before risking funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trade with real funds when run in live mode.

Mitigation: Keep live mode disabled until reviewed, use a least-privilege or sandbox credential where possible, and cap account exposure before enabling live trading.

Risk: The security evidence says paper-trading boundaries and risk controls are weak.

Mitigation: Review the execution path before use, avoid reusing the same long-running process for paper and live runs, and independently verify safeguards before relying on them.

Risk: The security guidance warns not to rely on documented volume or concurrent-position limits without verification.

Mitigation: Fix or independently test those limits, monitor open positions externally, and use conservative position-size settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-crypto-hourly-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Console logs, Python execution, environment-variable configuration, and simulated or live trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; configurable trade limits are exposed through SIMMER_* environment variables.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
