## Description:

Trades ETH price bin markets on Kalshi by exploiting the constraint that all bins must sum to 100%. When the sum deviates, identifies mispriced bins and trades toward rebalance. Requires SIMMER_API_KEY and simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to identify and optionally trade Kalshi ETH price-bin mispricings based on the expected 100% sum constraint across mutually exclusive bins. It supports paper-mode analysis by default and live execution only when explicitly run with the live flag.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money trades when live mode is enabled.

Mitigation: Use paper mode by default, enable --live only after reviewing the strategy, credentials, and configured trade limits, and keep max position size and max trades per run conservative.

Risk: The package requests a raw Solana private key in addition to the Simmer API key.

Mitigation: Avoid providing SOLANA_PRIVATE_KEY unless live execution is required and the package has been reviewed for credential handling.

Risk: Security evidence reports that safeguards may fail open when market safety context is unavailable.

Mitigation: Fix the safeguard behavior before live use so missing context blocks trading rather than allowing execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-eth-bin-distribution-trader)
- [Simmer Skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text logs with optional JSON automaton status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paper mode is the default; live mode may execute trades when explicitly enabled with --live.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
