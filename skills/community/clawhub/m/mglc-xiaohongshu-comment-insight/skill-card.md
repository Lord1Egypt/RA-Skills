## Description:

围绕产品、品牌或指定小红书笔记，从正文和评论中整理用户痛点、购买顾虑、使用场景与 FAQ，输出带评论原话和来源的洞察报告、建议及 Excel。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

面向品牌、产品和市场团队，围绕指定小红书笔记或关键词分析公开正文与评论，整理带来源的痛点、购买顾虑、使用场景和 FAQ，并导出报告与表格。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is benign with medium confidence, but partial; it flags extra research modes and an undeclared tool scope.

Mitigation: Review the skill's tool access and decide whether its author, competitor, and topic-research features are needed before installing.

Risk: The skill makes billable API requests using a local API key.

Mitigation: Keep the key in a local environment variable, review the cost estimate, set the authorized budget, and do not share the key in chat.

Risk: Posts and comments can contain untrusted instructions.

Mitigation: Treat source content as data; do not follow embedded requests to run commands, upload data, change budgets, or disclose credentials.

## Reference(s):

- [使用说明：参数与分页](references/usage.md)
- [分析格式与证据要求](references/analysis.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Markdown report, JSON and CSV data, HTML report, and optional Excel workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-linked findings and recommendations; reports include the retrieved scope and actual cost, with missing data identified.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
