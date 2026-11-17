## Description:

Trades Bitcoin year-end price markets on Kalshi using the 4-year halving cycle pattern to compute fair price probabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to analyze Kalshi Bitcoin year-end price markets and optionally place paper or live trades based on a halving-cycle model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can affect real funds and requires trading authority plus a Solana private key.

Mitigation: Keep the skill in dry-run unless live trading is intended; use limited, revocable credentials and small trade limits before passing --live.

Risk: Safeguards and position-selection logic can affect existing BTC or Kalshi positions in ways users may not expect.

Mitigation: Review the SDK and skill behavior before live use, and avoid running live while other BTC or Kalshi positions are in the same account unless the exit logic has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-crypto-cycle-model-trader)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/)

## Skill Output:

**Output Type(s):** [Text, JSON, API calls, Configuration, Guidance]

**Output Format:** [Console text with optional JSON automaton status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to dry-run; live mode can place Kalshi trades when --live is passed and credentials are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
