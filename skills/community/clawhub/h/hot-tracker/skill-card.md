## Description:

Hot Tracker scans and ranks current hot topics across Chinese social platforms, de-duplicates noisy posts, and returns an objective Top 10 trend list with scoring and source context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content analysts use this skill to monitor cross-platform Chinese social trends, rank topics by discussion, reach, sharing, freshness, emotion, and controversy, and understand why topics are trending without adopting a position.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to run automatically for broad hot-topic prompts and may use network access when available.

Mitigation: Use explicit prompts to constrain platforms, time windows, or topic scope when tighter boundaries are required.

Risk: Trend outputs and bundled content templates can influence publication decisions and may include source, copyright, advertising, AIGC, or platform-compliance risk.

Mitigation: Verify representative sources and review copyright, advertising, AIGC labeling, and platform compliance before publishing content based on the output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/e2e5g/skills/hot-tracker)
- [Analysis Framework](references/analysis-framework.md)
- [Data Format Specification](references/data-format.md)
- [Output Template](references/output-template.md)
- [Timeliness Framework](references/timeliness-framework.md)
- [Compliance Rules](references/compliance-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance]

**Output Format:** [Markdown trend reports and JSON ranking outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is a Top 10 hot-topic ranking with scores, noise notes, neutrality notes, confidence, and representative sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
