## Description:

Trades cross-market constraint violations in tennis Set 1 Games O/U, Match Games O/U, Total Sets O/U, Set Handicap, and Set/Match Winner bundles on Polymarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to identify and optionally trade pricing inconsistencies across related Polymarket tennis prop markets. It defaults to paper trading and requires explicit live mode for real Polymarket trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live Polymarket execution can place real USDC trades when the --live flag is used.

Mitigation: Keep the skill in paper mode unless the strategy, account limits, and live trading authority have been reviewed and approved.

Risk: The skill relies on SIMMER_API_KEY as a high-value trading credential.

Mitigation: Scope the credential tightly, rotate it if exposed, and avoid granting authority beyond the intended trading account.

Risk: Security evidence says some live-trading safeguards are under-enforced.

Mitigation: Enforce account-level caps for volume, open positions, pending orders, and total exposure outside the skill before live use.

Risk: The skill depends on simmer-sdk for market discovery and trade execution.

Mitigation: Pin and vet the simmer-sdk dependency before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-tennis-set-match-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration]

**Output Format:** [Text logs and trade API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SIMMER_API_KEY and tunable trading thresholds for position size, volume, spread, days to resolution, open positions, probability thresholds, and minimum violation.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
