## Description:

珠宝行业营销文案合规审查，用于审核珠宝或饰品营销文案、商品详情页、直播话术、社交文案和活动海报文案中的广告法及行业监管风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cullolo](https://clawhub.ai/user/cullolo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, ecommerce, compliance, and operations teams use this skill to review China-focused jewelry and accessories advertising copy before publication. It flags red, orange, and yellow risk terms, explains the likely issue, and suggests safer wording for internal review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved compliance reports can retain user-provided marketing copy or campaign details in workspace files.

Mitigation: Use an approved retention process for generated reports and avoid submitting confidential copy unless the workspace is authorized for that data.

Risk: User-provided complaint terms can be persisted into the word library and influence future reviews.

Mitigation: Restrict word-library changes to reviewed maintainers or require approval before adding complaint-derived terms.

## Reference(s):

- [珠宝营销文案合规词库](references/word-library.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown compliance report with color-coded risk annotations, a risk detail table, revision suggestions, and an overall conclusion.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a Markdown report file in a compliance-reports directory for review and archiving.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
