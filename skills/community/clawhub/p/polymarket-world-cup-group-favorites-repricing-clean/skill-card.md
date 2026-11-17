## Description:

Buy pre-tournament World Cup outright favorites and capture group-stage repricing before knockout phase.

This skill is for research and development only.

## Publisher:

[alyna123t](https://clawhub.ai/user/alyna123t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prediction-market researchers use this skill to scan 2026 World Cup outright-winner markets, identify favorite-team repricing opportunities before the group stage, and optionally manage exit timing around the knockout phase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can use a sensitive Simmer API key for trading and account access.

Mitigation: Use a least-privilege API key with spending or trading limits, and start in dry-run or sim mode before live execution.

Risk: The trading SDK dependency is not pinned to an exact reviewed version.

Mitigation: Pin simmer-sdk to a reviewed version before production use.

Risk: Account status output can display balances and open positions.

Mitigation: Run status commands only in trusted environments and avoid sharing logs that contain account details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alyna123t/skills/polymarket-world-cup-group-favorites-repricing-clean)
- [Strategy source](https://x.com/airdrops_io/status/2061459289059754392)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text status output, JSON configuration or position output, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run and sim modes are available; live trading requires SIMMER_API_KEY and explicit live-mode execution.]

## Skill Version(s):

0.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
