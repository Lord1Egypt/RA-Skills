## Description:

Munger Decision helps agents analyze decision scenarios with Charlie Munger-style mental models, recommend relevant models, guide structured dialogue, and generate Markdown decision reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdz0451](https://clawhub.ai/user/cdz0451)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and decision-support users use this skill to frame investment, product, hiring, and strategy questions through structured mental-model prompts and receive a concise Markdown analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision sessions may be stored without clear retention bounds.

Mitigation: Avoid confidential investment, hiring, or strategy details until retention, cleanup, and input handling limits are documented or fixed.

Risk: Mislabeled decision-model data can mislead analysis.

Mitigation: Treat recommendations as decision-framing prompts and validate model labels and content before relying on the output.

Risk: Users may mistake the generated report for authoritative advice.

Mitigation: Require human review for investment, hiring, and strategy decisions, and present outputs as draft guidance.

## Reference(s):

- [Munger Decision ClawHub page](https://clawhub.ai/cdz0451/skills/munger-decision)
- [Artifact README](artifact/README.md)
- [Mental model reference index](artifact/references/INDEX.md)
- [Mental model definitions](artifact/references/models.md)
- [Usage examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown decision report with structured questions and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session-based decision framing; outputs should not be treated as authoritative financial, hiring, or strategy advice.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
