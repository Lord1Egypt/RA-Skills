## Description:

Helps agents review past decisions for hindsight bias by comparing current judgments with what was knowable at the time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill during post-mortems to compare a past decision with the information available at the time, separate decision quality from outcome, and plan future decision records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Predictions or attributed judgments shared in a forum may expose confidential details.

Mitigation: Choose where decision notes are kept, review the audience, and remove confidential details before sharing.

Risk: Retrospective judgments may unfairly credit or blame a decision-maker when outcome knowledge replaces the contemporaneous record.

Mitigation: Review contemporaneous records first, assess decision quality separately from outcome, and use a blind post-mortem when possible.

## Reference(s):

- [Primary sources](artifact/references/sources.md)
- [Hindsight Bias overview](https://www.deciqai.com/c/hindsight-bias)
- [ClawHub release](https://clawhub.ai/deciqai/skills/hindsight-bias)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown decision review with structured prompts and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates memory distortion, inevitability, and foreseeability; evaluates decision process apart from outcome.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
