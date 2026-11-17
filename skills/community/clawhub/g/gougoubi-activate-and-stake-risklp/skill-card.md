## Description:

Activates Gougoubi proposal conditions and adds fixed risk LP per selected condition in a deterministic workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to activate Gougoubi proposal conditions and add a fixed risk LP amount across all, only-created, or single-condition scopes. It is intended for combined activation and LP workflows, not result submission, reward claiming, or condition creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can automatically join a committee with a stake without a clear opt-in or spending limit.

Mitigation: Require explicit confirmation of the stake, token, chain, wallet, contract addresses, fees, and maximum total spend before live execution.

Risk: Live activation and risk LP actions can create unwanted financial exposure if run against the wrong proposal, scope, or condition.

Mitigation: Review dry-run output first, confirm the proposal address and selected scope, and avoid live execution unless local scripts enforce the confirmed limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasong/skills/gougoubi-activate-and-stake-risklp)
- [Publisher profile](https://clawhub.ai/user/chinasong)
- [Gougoubi repository](https://github.com/gougoubi/gougoubi)
- [Gougoubi website](https://gougoubi.ai)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON with optional shell commands for local script entry points]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes activation and risk LP counts, per-condition successes and failures, warnings, and next actions.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
