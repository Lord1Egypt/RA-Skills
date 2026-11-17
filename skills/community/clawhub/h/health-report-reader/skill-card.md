## Description:

Interprets health checkup reports from images, structured values, or natural-language descriptions and generates risk-graded explanations, recommendations, and interactive HTML visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and health-support agents use this skill to turn health checkup reports into readable indicator summaries, risk tiers, trend analysis, and practical follow-up guidance. The output is educational and should not replace professional medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may load unpinned third-party web code while displaying sensitive medical information.

Mitigation: Review generated HTML before opening it with real health data, and prefer self-contained reports without remote scripts or styles.

Risk: Health interpretations may be mistaken for medical diagnosis.

Mitigation: Keep the educational-use disclaimer in outputs and direct abnormal or critical findings to qualified medical professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/health-report-reader)
- [README](README.md)
- [Indicator reference library](references/indicators.md)
- [HTML report template](references/template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Plain-language interpretation with optional Markdown and static HTML report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chart.js visualizations, responsive layout, print styles, risk tiers, recommendations, and medical disclaimer text.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
