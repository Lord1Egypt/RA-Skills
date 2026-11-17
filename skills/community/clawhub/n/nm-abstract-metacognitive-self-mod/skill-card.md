## Description:

Analyze past skill improvements to detect regressions and improve the improvement process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after groups of skill changes, regressions, or declining effectiveness to analyze outcomes, identify patterns, and prepare recommendations for improving future changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic trace capture may retain sensitive workflow details without warning or filtering; the security analysis is partial.

Mitigation: Review which workflow details are recorded before use, limit capture to approved information and the least detailed available mode, and check storage and retention controls.

## Reference(s):

- [Skill project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)
- [ClawHub release](https://clawhub.ai/athola/skills/nm-abstract-metacognitive-self-mod)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Written analysis report and structured improvement-memory entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include outcome summaries, causal hypotheses, trend analysis, and proposed strategy changes.]

## Skill Version(s):

1.10.3 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
