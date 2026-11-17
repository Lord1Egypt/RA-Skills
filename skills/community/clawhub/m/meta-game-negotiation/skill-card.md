## Description:

Meta Game Negotiation supports game-theory negotiation workflows such as Nash bargaining, Rubinstein bargaining, Shapley value analysis, and minimax approximation with added self-checking and reflection steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to structure negotiation analysis, select an appropriate game-theory method, and add review steps before relying on the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may overestimate the completeness of the advertised self-evolving negotiation behavior.

Mitigation: Review outputs against the original game-negotiation workflow and require human approval before using recommendations in consequential negotiations.

Risk: Cross-session learning can persist arbitrary notes.

Mitigation: Keep learned_patterns.json under user control and do not treat stored notes as instructions without human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-game-negotiation)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown text with optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
