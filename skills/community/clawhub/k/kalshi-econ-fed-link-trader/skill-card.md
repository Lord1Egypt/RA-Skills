## Description:

Cross-market strategy that uses CPI bin prices to estimate CPI level, then adjusts Fed rate market positions via a sensitivity model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to evaluate CPI-implied signals against Kalshi Fed rate markets and manage paper or explicitly enabled live trading runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute real financial trades when run with --live and configured credentials.

Mitigation: Keep dry-run mode unless live trading is intended; cap position size, trades per run, slippage, and liquidity through tunables before enabling live runs.

Risk: SIMMER_API_KEY and SOLANA_PRIVATE_KEY are high-value credentials.

Mitigation: Use a dedicated low-balance wallet and scoped API key where possible; rotate credentials if they are exposed.

Risk: The trading model uses a static CPI-to-Fed sensitivity table that may not match current market conditions.

Mitigation: Review the model assumptions and compare signals against current macro data before relying on trade recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-econ-fed-link-trader)
- [Publisher profile](https://clawhub.ai/user/diagnostikon)
- [Simmer skills homepage](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal output with optional JSON automaton status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry run by default; live trading requires --live and configured SIMMER_API_KEY and SOLANA_PRIVATE_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
