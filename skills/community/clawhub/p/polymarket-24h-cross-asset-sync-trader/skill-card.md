## Description:

Identifies cross-asset correlation divergences in 5-minute crypto "Up or Down" markets on Polymarket and trades the outlier toward the group consensus with conviction-based sizing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators can use this skill to identify and place simulated or live Polymarket trades based on short-window crypto market divergence signals. Live use requires independent strategy review, credential controls, and account-level trading limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that live-trading safeguards and signal logic do not fully match the user-facing description.

Mitigation: Use paper mode unless the strategy and safeguards have been independently reviewed and corrected.

Risk: Running with --live can authorize automated real-money Polymarket orders.

Mitigation: Require explicit operator approval for live mode, keep external account limits in place, and set conservative position tunables.

Risk: SIMMER_API_KEY is a high-value trading credential.

Mitigation: Scope the key as tightly as possible, store it only in the runtime secret store, and rotate it after testing or suspected exposure.

Risk: The skill depends on simmer-sdk for market discovery and order execution.

Mitigation: Pin or otherwise control the dependency version before deployment.

## Reference(s):

- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console logs and trading API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to simulated trading unless run with --live.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
