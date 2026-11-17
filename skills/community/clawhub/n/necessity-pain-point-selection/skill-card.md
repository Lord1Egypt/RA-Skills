## Description:

Helps utility-product merchants turn customer reviews and complaints into structured pain labels, product selection specs, improvement backlogs, and validation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce merchants use this skill to analyze own or competitor reviews for utility products, identify recurring buyer pains, and convert them into sourcing requirements, product fixes, QC checks, and validation metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad review-analysis trigger may activate for adjacent tasks such as marketing copy, review-app setup, fashion or luxury positioning, or generic sentiment dashboards.

Mitigation: Redirect those requests to a more suitable workflow and use this skill only for actionable review mining and product decision tasks.

Risk: Review data may include content the user is not allowed to process or platform data with collection restrictions.

Mitigation: Use only review data the user is allowed to process, such as own exports, authorized tools, permitted public review access, or legal de-identified datasets.

Risk: Complaint counts can overstate overall buyer dissatisfaction if rating distribution and review volume are not checked.

Mitigation: Validate pain-label frequency against rating distribution, returns, and pre/post complaint rates before using recommendations for sourcing or product changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rijoyai/skills/necessity-pain-point-selection)
- [Pain Point Framework](references/pain_point_framework.md)
- [Review Mining Guide](references/review_mining_guide.md)
- [Rijoy](https://www.rijoy.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables and optional inline shell commands; optional JSON or tabular summaries from the bulk review extractor.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask 5-8 scoping questions when review context is missing; bulk review analysis accepts CSV, TXT, or stdin review text.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
