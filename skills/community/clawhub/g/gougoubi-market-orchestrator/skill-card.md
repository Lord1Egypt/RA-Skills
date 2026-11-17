## Description:

Routes end-to-end Gougoubi PBFT market workflows across creation, activation, liquidity, result submission, reward claiming, and recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to route high-level Gougoubi PBFT market requests to the correct downstream workflow skill and receive compact operation summaries for the current stage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad high-level requests can route into sensitive Gougoubi crypto-market actions.

Mitigation: Use the skill only for intended end-to-end Gougoubi operations and require explicit approval before activation, liquidity staking, result submission, reward claiming, or recovery actions.

Risk: Use with real funds or market authority can carry operational and financial consequences.

Mitigation: Review the skill before installing it in workflows that control real funds or market authority.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasong/skills/gougoubi-market-orchestrator)
- [ClawHub publisher profile](https://clawhub.ai/user/chinasong)
- [Repository link from skill metadata](https://github.com/gougoubi/gougoubi)
- [Gougoubi support website](https://gougoubi.ai)

## Skill Output:

**Output Type(s):** [Guidance, JSON]

**Output Format:** [Structured JSON with concise routing rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes high-level requests to downstream Gougoubi skills; stage-specific actions are handled by those downstream skills.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
