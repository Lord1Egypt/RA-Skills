## Description:

Trades distribution-sum violations in social media post-count range markets on Polymarket, where range bins for the same person and date range should sum to about 100%, and detects local anomalies where a bin deviates sharply from its neighbors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and agent operators use this skill to scan Polymarket social media post-count range markets, identify distribution-sum violations or neighbor-bin anomalies, and produce paper or live trade actions through the Simmer SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades and expose funded accounts to financial loss.

Mitigation: Keep the skill in paper mode unless live trading is intentional, cap funded account exposure to money the operator is prepared to risk, and use the SIMMER_MAX_POSITION, SIMMER_MIN_TRADE, and SIMMER_MAX_POSITIONS tunables conservatively.

Risk: The authoritative security summary states that some documented risk controls are incomplete or unenforced.

Mitigation: Independently verify market grouping logic, volume and liquidity checks, position exposure limits, and the exact Simmer SDK version before enabling live trading.

Risk: SIMMER_API_KEY grants trading authority and is a high-value credential.

Mitigation: Store the key only in the intended runtime secret store, restrict its account permissions and funding where possible, and rotate it if it may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-ladder-social-posts-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and trade instructions produced by a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and tunable trading thresholds; defaults to paper trading unless --live is supplied.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
