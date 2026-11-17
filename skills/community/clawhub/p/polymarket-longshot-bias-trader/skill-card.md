## Description:

Systematically trades against longshot bias by selling overpriced low-probability outcomes and buying underpriced near-certainties on Polymarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt a Polymarket trading agent that searches liquid prediction markets for extreme probability prices, sizes positions from configured thresholds, and submits paper or explicit live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can expose users to larger or riskier Polymarket positions than expected.

Mitigation: Use paper mode by default and avoid --live with meaningful funds until the volume filter, position sizing cap, open-position accounting, and dependency pinning are fixed or enforced externally.

Risk: A required trading credential grants authority to place orders.

Mitigation: Protect SIMMER_API_KEY as a high-value secret and use the lowest practical account permissions and funding level.

## Reference(s):

- [Skill page](https://clawhub.ai/diagnostikon/skills/polymarket-longshot-bias-trader)
- [Publisher profile](https://clawhub.ai/user/diagnostikon)
- [simmer-sdk PyPI package](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and the simmer-sdk dependency; defaults to paper trading unless invoked with --live.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
