## Description:

Revises existing Chinese or English explanatory prose to make logical steps easier to follow while preserving its voice, vocabulary, claims, and concise style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and editors use this skill to clarify reasoning in existing Chinese or English prose without simplifying terminology or changing the author's position. It abstains when the passage is already easy to follow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive source prose may be shared with a separate blind-review subagent.

Mitigation: Avoid sensitive text unless the review flow is acceptable; otherwise use a rewrite workflow without delegation.

Risk: A rewrite can subtly change a claim, attribution, or tone despite automated checks.

Mitigation: Review each revised passage against the original and resolve all reported flags before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/vincentjiang06/skills/logic-pacer)
- [Editing anti-patterns](artifact/references/anti-patterns.md)
- [Reasoning and writing mechanisms](artifact/references/mechanisms.md)
- [Blind step-followability review](artifact/references/step-followability-probe.md)
- [Worked example](artifact/references/worked-example-quetelet.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Revised prose with a short review-flag block, or a one-line abstention]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports possible fidelity and length issues; indicates when blind review was not run.]

## Skill Version(s):

1.1.0 (source: skill metadata, CHANGELOG, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
