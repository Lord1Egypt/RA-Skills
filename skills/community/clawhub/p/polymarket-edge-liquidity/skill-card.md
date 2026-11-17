## Description:

Trades active Polymarket-imported markets on Simmer when estimated edge and liquidity filters pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drserkandedeoglu](https://clawhub.ai/user/drserkandedeoglu)

### License/Terms of Use:


## Use Case:

Developers and trading automation operators use this skill to scan active Polymarket-imported markets on Simmer, filter by estimated edge and liquidity, and either dry-run or submit trades with recorded reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place trades while probability and trade-amount validation are weak.

Mitigation: Keep dry-run enabled until behavior is reviewed, then use a dedicated low-privilege Simmer API key with spending or transaction limits before enabling live trades.

Risk: The trading SDK dependency is unpinned, so dependency updates could change runtime behavior.

Mitigation: Pin and review the `simmer-sdk` dependency before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/drserkandedeoglu/skills/polymarket-edge-liquidity)
- [ClawHub publisher profile](https://clawhub.ai/user/drserkandedeoglu)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Configuration]

**Output Format:** [Console text from a Python command-line script, with Simmer API calls when live mode is enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; dry-run mode is the default unless --live is provided.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
