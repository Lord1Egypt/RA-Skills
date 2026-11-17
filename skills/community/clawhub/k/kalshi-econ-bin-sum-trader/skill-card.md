## Description:

Trades CPI range bin markets on Kalshi using the constraint that mutually exclusive bins must sum to ~100%. Normalizes and trades the most mispriced bin when deviation exceeds tolerance. Requires SIMMER_API_KEY and simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to identify CPI range-bin pricing deviations on Kalshi, review dry-run trade proposals, and optionally execute live trades when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode gives the skill high-impact trading and wallet authority.

Mitigation: Use dry-run mode until SDK version, credential handling, grouping logic, safeguard behavior, and exit ownership rules are reviewed.

Risk: Live trading can spend real USDC and affect accounts that contain unrelated CPI positions.

Mitigation: Use a dedicated low-balance account or wallet with tightly limited trading credentials, and avoid accounts containing unrelated CPI positions.

Risk: Misconfigured position size, slippage, liquidity, or trade-count settings can increase financial exposure.

Mitigation: Review and set the tunable limits before live execution, especially max position size, max trades per run, slippage maximum, and minimum liquidity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/kalshi-econ-bin-sum-trader)
- [Simmer Skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, configuration details, and runtime text or JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run output; live mode can execute trades only when the --live flag and required credentials are provided.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
