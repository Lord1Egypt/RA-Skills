## Description:

描述一个项目想法，AI 从市场/技术/商业/风险四个维度系统评估，输出评估报告、竞品速查、MVP 建议，帮你决策「值不值得做」。

This skill is ready for commercial/non-commercial use.

## Publisher:

[antonia-sz](https://clawhub.ai/user/antonia-sz)

### License/Terms of Use:

MIT-0

## Use Case:

External users, product managers, founders, and developers use this skill to evaluate product or startup ideas across market demand, technical feasibility, business value, and risk before deciding whether to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API configuration can send credentials and project details to an unintended or arbitrary LLM endpoint.

Mitigation: Review the configured endpoint before use, set a provider-specific key intentionally, and use only non-sensitive project descriptions unless the endpoint is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antonia-sz/skills/project-evaluator)
- [Publisher profile](https://clawhub.ai/user/antonia-sz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown project evaluation report with scoring tables, competitor notes, MVP suggestions, and a final recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write the report to a user-specified Markdown file when --output is provided.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
