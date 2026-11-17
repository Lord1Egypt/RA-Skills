## Description:

Run bounded GameLearningRuntime QA against an authorized game, training adapter, replay, or live probe and produce inspectable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game QA teams use this skill to run authorized, finite checks on GameLearningRuntime projects and distinguish regression, training, and live-acceptance evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running QA checks on an unauthorized project or without bounds may disrupt a game or training environment.

Mitigation: Confirm project authorization and limit each check, especially training and live probes.

Risk: Reports may expose proprietary traces, secrets, or local machine paths.

Mitigation: Review and redact generated reports before sharing; publish only evidence authorized by the project owner.

Risk: Passing smoke or synthetic checks may be mistaken for proof of live-game quality.

Mitigation: Label missing live acceptance and training evidence explicitly; do not claim release quality from this report alone.

## Reference(s):

- [glr-qa ClawHub release](https://clawhub.ai/loonghao/skills/glr-qa)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, HTML]

**Output Format:** [Markdown guidance and commands; dated JSON results and self-contained HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports separate completed checks from missing live or training evidence.]

## Skill Version(s):

0.26.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
